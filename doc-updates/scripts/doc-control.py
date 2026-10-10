#!/usr/bin/env python3
"""Offline host-document review control. Python 3.11+, Linux, no dependencies."""

import argparse
from datetime import datetime, timezone
import difflib
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import uuid

LIMIT = 8 * 1024 * 1024
START = "<!-- doc-control:start -->"
END = "<!-- doc-control:end -->"
STAGES = ("intake", "prepared", "review", "reviewed", "approved", "publishing",
          "closed", "rejected", "withdrawn", "superseded")
# Mirrors references/local-lifecycle.md in this skill; tests check the mapping.
FORWARD = {"prepare": ("intake", "prepared", "author"),
           "open": ("prepared", "review", "author"),
           "review": ("review", "reviewed", "reviewer"),
           "approve": ("reviewed", "approved", "operator"),
           "publish": ("approved", "publishing", "publisher"),
           "close": ("publishing", "closed", "publisher")}
NEXT = {a: command for command, (a, _, _) in FORWARD.items()}
NEXT.update(publishing="publish (inspect and resume)", closed="status (verified retry)",
            rejected="reopen", withdrawn="reopen", superseded="reopen")


class Refusal(Exception):
    pass


class StaleSnapshot(Refusal):
    pass


def require(ok, message):
    if not ok:
        raise Refusal(message)


def fresh(ok, message):
    if not ok:
        raise StaleSnapshot(message)


def fields(value, names):
    require(type(value) is dict and set(value) == set(names), "Unknown or missing fields")


def text(value):
    require(type(value) is str and 0 < len(value) <= 4096 and
            not any(ord(c) < 32 for c in value), "Missing or unsafe text evidence")
    return value


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode()


def parse(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "Duplicate JSON field")
            result[key] = value
        return result
    try:
        return json.loads(data, object_pairs_hook=unique,
                          parse_constant=lambda _: require(False, "Invalid JSON constant"))
    except (ValueError, UnicodeError, RecursionError) as error:
        raise Refusal("Malformed JSON") from error


def path_name(name, prefix=None):
    require(type(name) is str and re.fullmatch(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*", name)
            and all(p not in (".", "..", ".git") for p in name.split("/")), "Unsafe path")
    if prefix:
        require(name.startswith(prefix + "/") and name != prefix + "/INDEX.md",
                "Path outside document scope")
    return name


def check_stat(st, directory=False, private=False):
    require(st.st_uid == os.getuid() and
            (stat.S_ISDIR(st.st_mode) if directory else stat.S_ISREG(st.st_mode)) and
            not st.st_mode & (0o077 if private else 0o022), "Unsafe ownership, type or permissions")
    if not directory:
        require(st.st_size <= LIMIT, "Oversized file")


def operational_destination(name):
    """Admission policy only; retained paths still use path_name for replay."""
    path_name(name, "doc-operations")
    parts = name.split("/")
    require(len(parts) >= 3, "Operational destination requires a classification directory")
    require(parts[1].casefold() not in ("subjects", "topics", "components"),
            "Universal wrapper is not an operational classification")
    return name


class Store:
    """Pinned, no-follow directory access; lock serializes cooperating tool users."""

    def __init__(self, root):
        self.root = Path(root).absolute()
        require(self.root != Path("/") and ".." not in self.root.parts, "Unsafe root")
        for parent in [*reversed(self.root.parents), self.root]:
            st = parent.lstat()
            require(stat.S_ISDIR(st.st_mode) and
                    (not st.st_mode & 0o022 or st.st_mode & stat.S_ISVTX), "Unsafe root ancestor")
        check_stat(self.root.stat(), directory=True)
        self.fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            os.close(self.fd)
            raise Refusal("Concurrent tool operation; retry after lock release") from error

    def close(self):
        os.close(self.fd)

    def parent(self, name, create=False):
        path_name(name)
        fd = os.dup(self.fd)
        try:
            for part in name.split("/")[:-1]:
                if create:
                    try:
                        os.mkdir(part, 0o700, dir_fd=fd)
                        os.fsync(fd)
                    except FileExistsError:
                        pass
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = child
                check_stat(os.fstat(fd), directory=True)
            return fd
        except BaseException:
            os.close(fd)
            raise

    def read(self, name, private=False):
        try:
            fd = self.parent(name)
        except FileNotFoundError:
            return None
        try:
            try:
                entry = os.open(name.split("/")[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                dir_fd=fd)
            except FileNotFoundError:
                return None
            with os.fdopen(entry, "rb") as stream:
                check_stat(os.fstat(stream.fileno()), private=private)
                data = stream.read(LIMIT + 1)
                require(len(data) <= LIMIT, "File size limit")
                return data
        finally:
            os.close(fd)

    def write(self, name, data, before):
        require(len(data) <= LIMIT, "File size limit")
        fd = self.parent(name, create=True)
        temporary = ".doc-control-" + uuid.uuid4().hex
        try:
            descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                 0o600, dir_fd=fd)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            require(self.read(name) == before, "Conflicting filesystem change; preserved")
            if before is None:
                os.link(temporary, name.split("/")[-1], src_dir_fd=fd, dst_dir_fd=fd,
                        follow_symlinks=False)
            else:
                os.replace(temporary, name.split("/")[-1], src_dir_fd=fd, dst_dir_fd=fd)
            os.fsync(fd)
        finally:
            try:
                os.unlink(temporary, dir_fd=fd)
            except FileNotFoundError:
                pass
            os.close(fd)

    def evidence(self, name):
        data = self.read(path_name(name, "doc-updates"))
        require(data is not None and data.strip(), "Missing evidence resource")
        return {"path": name, "sha256": sha(data)}

    def writable(self, name):
        """Check nearest existing parent without creating publication directories."""
        path_name(name)
        fd = os.dup(self.fd)
        try:
            for part in name.split("/")[:-1]:
                require(os.access(".", os.W_OK | os.X_OK, dir_fd=fd, effective_ids=True),
                        "Missing runtime target write permission")
                try:
                    child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                except FileNotFoundError:
                    return
                os.close(fd)
                fd = child
                check_stat(os.fstat(fd), directory=True)
            require(os.access(".", os.W_OK | os.X_OK, dir_fd=fd, effective_ids=True),
                    "Missing runtime target write permission")
        finally:
            os.close(fd)

    def records(self):
        try:
            fd = self.parent("doc-updates/changes/.inventory")
        except FileNotFoundError:
            return []
        try:
            names = sorted(os.listdir(fd))
        finally:
            os.close(fd)
        require(len(names) <= 1000, "Change count limit")
        result = []
        for name in names:
            if re.fullmatch(r"\.doc-control-[0-9a-f]{32}", name):
                # A killed atomic writer can leave private staging. Preserve it;
                # only the canonical <id>.json file is authoritative.
                self.read("doc-updates/changes/" + name, private=True)
                continue
            require(re.fullmatch(r"[0-9a-f]{32}\.json", name), "Unexpected control resource")
            record = parse(self.read("doc-updates/changes/" + name, private=True))
            validate(record)
            require(name == record["id"] + ".json", "Record ID mismatch")
            result.append(record)
        keys = [r["request"]["key"] for r in result]
        require(len(keys) == len(set(keys)), "Duplicate request masters")
        active = [r["request"]["destination"] for r in result
                  if r["stage"] not in ("closed", "rejected", "withdrawn", "superseded")]
        require(len(active) == len(set(active)), "Competing active changes")
        return result


def evidence_shape(value):
    fields(value, ("path", "sha256"))
    path_name(value["path"], "doc-updates")
    require(type(value["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", value["sha256"]),
            "Invalid evidence digest")


def snapshot_shape(s):
    fields(s, ("candidate", "candidate_hash", "output_resource", "catalog_resource", "output", "catalog", "destination", "before",
               "catalog_before", "edition", "source_edition", "purpose", "contract", "checks",
               "basis", "authoring_sources", "id"))
    path_name(s["candidate"], "doc-updates")
    path_name(s["output_resource"], "doc-updates")
    path_name(s["catalog_resource"], "doc-updates")
    path_name(s["destination"], "doc-operations")
    for key in ("output", "catalog", "catalog_before"):
        require(type(s[key]) is str and bool(s[key].strip()), "Missing snapshot bytes")
    require(s["before"] is None or type(s["before"]) is str, "Invalid source baseline")
    for key in ("edition", "source_edition", "purpose", "contract"):
        text(s[key])
    require(type(s["candidate_hash"]) is str and
            re.fullmatch(r"[0-9a-f]{64}", s["candidate_hash"]), "Invalid candidate identity")
    evidence_shape(s["basis"])
    evidence_shape(s["checks"])
    fields(s["authoring_sources"], contract_sources(s["contract"]))
    for value in s["authoring_sources"].values():
        require(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value), "Invalid authoring source digest")
    require(s["id"] == sha(encoded({k: v for k, v in s.items() if k != "id"})),
            "Snapshot identity mismatch")


def draft_check(draft, snapshot):
    require(draft is not None, "Missing prerequisite draft; next: draft")
    require(all(draft[k] == snapshot[k] for k in
                ("candidate", "candidate_hash", "purpose", "edition", "contract",
                 "source_edition", "destination")) and
            draft["source_hash"] == (None if snapshot["before"] is None else
                                      sha(snapshot["before"].encode())),
            "Draft registration changed; next: draft with current candidate/basis")


def latest(record, action):
    for event in reversed(record["history"]):
        if event["action"] in ("rework", "reopen"):
            return None
        if event["action"] == action:
            return event["data"]
    return None


def destination(stage, action):
    if action in FORWARD:
        before, after, role = FORWARD[action]
        require(stage == before, "Missing prerequisite stage: " + before)
        return after, role
    if action == "intake":
        require(stage is None, "Intake already registered")
        return "intake", "author"
    if action == "draft":
        require(stage == "intake", "Draft registration requires intake; next: rework")
        return "intake", "author"
    if action in ("refuse", "hold", "release", "correct", "reconcile"):
        require(stage in STAGES, "Missing intake")
        return stage, "author"
    if action == "rework":
        require(stage in ("intake", "prepared", "review", "reviewed", "approved"),
                "Rework requires an unpublished active change")
        return "intake", "author"
    if action in ("reject", "withdraw", "supersede"):
        require(stage in ("intake", "prepared", "review", "reviewed", "approved"),
                "Terminal decision unavailable at this stage")
        return {"reject": "rejected", "withdraw": "withdrawn", "supersede": "superseded"}[action], "operator"
    if action == "reopen":
        require(stage in ("rejected", "withdrawn", "superseded"), "Not a reopenable change")
        return "intake", "operator"
    raise Refusal("Unknown action")


def validate(record):
    fields(record, ("schema", "id", "request", "stage", "history"))
    require(type(record["schema"]) is int and record["schema"] in (1, 2) and
            type(record["id"]) is str and re.fullmatch(r"[0-9a-f]{32}", record["id"]), "Invalid record identity")
    q = record["request"]
    fields(q, ("key", "basis", "scope", "destination", "source_edition", "source_hash", "author", "legacy"))
    for key in ("key", "basis", "scope", "source_edition", "author"):
        text(q[key])
    path_name(q["destination"], "doc-operations")
    require(type(q["legacy"]) is bool, "Invalid legacy evidence gap")
    require(q["source_hash"] is None or type(q["source_hash"]) is str and
            re.fullmatch(r"[0-9a-f]{64}", q["source_hash"]), "Invalid source digest")
    require(type(record["history"]) is list and record["history"], "Missing history")
    stage, timestamp, snapshot, reviewed, authorized = None, "", None, False, False
    draft = None
    held, rebased = False, False
    for seq, event in enumerate(record["history"], 1):
        fields(event, ("seq", "utc", "role", "actor", "from", "to", "action", "outcome", "evidence", "reason", "data"))
        require(type(event["seq"]) is int and event["seq"] == seq and event["from"] == stage,
                "Inconsistent history order or predecessor")
        date = event["utc"]
        require(type(date) is str and re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{6}Z", date),
                "Invalid UTC timestamp")
        try:
            datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError as error:
            raise Refusal("Invalid UTC timestamp") from error
        require(date >= timestamp, "Nonchronological history")
        timestamp = date
        after, role = destination(stage, event["action"])
        if event["action"] in FORWARD or (record["schema"] == 2 and event["action"] == "draft"):
            require(not held, "Forward history contains an unreleased hold")
        require(event["to"] == after and event["role"] == role, "Invalid transition or role")
        for key in ("actor", "outcome", "evidence"):
            text(event[key])
        require(type(event["reason"]) is str, "Invalid hold reason")
        require(event["outcome"] == ("refused" if event["action"] == "refuse" else "observed"),
                "Invalid action outcome")
        if event["action"] in ("refuse", "hold", "rework"):
            text(event["reason"])
        d = event["data"]
        action = event["action"]
        if action == "draft":
            fields(d, ("candidate", "candidate_hash", "purpose", "edition", "contract", "source_edition", "source_hash", "destination"))
            path_name(d["candidate"], "doc-updates")
            for key in ("purpose", "edition", "contract", "source_edition"):
                text(d[key])
            require(d["destination"] == q["destination"] and type(d["candidate_hash"]) is str
                    and re.fullmatch(r"[0-9a-f]{64}", d["candidate_hash"]), "Invalid draft registration")
            require(d["source_hash"] is None or type(d["source_hash"]) is str and
                    re.fullmatch(r"[0-9a-f]{64}", d["source_hash"]), "Invalid draft source identity")
            draft = d
        elif action == "prepare":
            snapshot_shape(d)
            if record["schema"] == 2:
                draft_check(draft, d)
            require(d["destination"] == q["destination"], "Changed publication mapping")
            if not rebased:
                require((None if d["before"] is None else sha(d["before"].encode())) == q["source_hash"]
                        and d["source_edition"] == q["source_edition"], "Inconsistent intake/source snapshot")
            snapshot, reviewed, authorized = d, False, False
        elif action in ("open", "review"):
            fields(d, ("snapshot", "evidence") if action == "open" else
                   ("snapshot", "evidence", "findings", "checks_passed"))
            require(snapshot and d["snapshot"] == snapshot["id"], "Stale review identity")
            evidence_shape(d["evidence"])
            if action == "review":
                require(type(d["findings"]) is list and d["checks_passed"] is True,
                        "Missing successful checks")
                for finding in d["findings"]:
                    fields(finding, ("finding", "blocking", "disposition"))
                    text(finding["finding"])
                    require(type(finding["blocking"]) is bool and finding["disposition"] in
                            ("resolved", "accepted", "open") and
                            (not finding["blocking"] or finding["disposition"] == "resolved"),
                            "Unresolved blocking finding")
                reviewed = True
        elif action in ("approve", "reject", "withdraw", "supersede", "reopen"):
            fields(d, ("snapshot", "scope", "authority", "capture", "decision"))
            require(d["capture"] == "operator-terminal" and d["decision"] == action,
                    "Untrusted decision capture")
            text(d["scope"])
            require(type(d["authority"]) is bool, "Invalid authority")
            if action == "approve":
                require(snapshot and reviewed and d["snapshot"] == snapshot["id"] and
                        d["scope"] == q["destination"] + " + doc-operations/INDEX.md",
                        "Missing reviewed decision scope")
                authorized = d["authority"]
            else:
                text(event["reason"])
                require(d["snapshot"] == (snapshot["id"] if snapshot else record["id"]),
                        "Stale terminal decision identity")
        elif action in ("publish", "close"):
            fields(d, ("snapshot", "evidence"))
            require(snapshot and d["snapshot"] == snapshot["id"], "Missing publication snapshot")
            require(authorized, "Missing publication authority")
            text(d["evidence"])
        else:
            fields(d, ("note",))
            text(d["note"])
        if action in ("rework", "reopen"):
            snapshot, reviewed, authorized = None, False, False
            draft = None
            held, rebased = False, True
        if action == "hold":
            held = True
        if action == "release":
            require(held, "Release without a recorded hold")
            held = False
        stage = after
    require(record["stage"] == stage, "Unknown or inconsistent current stage")
    return record


def event(record, action, actor, evidence, data, reason=""):
    after, role = destination(record["stage"], action)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    require(not record["history"] or timestamp >= record["history"][-1]["utc"],
            "UTC clock moved backwards; hold until chronological")
    record["history"].append({"seq": len(record["history"]) + 1, "utc": timestamp,
                              "role": role, "actor": text(actor), "from": record["stage"],
                              "to": after, "action": action, "outcome": "refused" if action == "refuse" else "observed",
                              "evidence": text(evidence), "reason": reason, "data": data})
    record["stage"] = after
    validate(record)


def navigation(records):
    lines = [START, "", "### Local change requests", "",
             "| Change | Request scope | Lifecycle stage | Next action |",
             "|---|---|---|---|"]
    def cell(s):
        return s.replace("|", "&#124;").replace("[", "&#91;").replace("]", "&#93;").replace("<", "&lt;")
    for r in records:
        lines.append(f'| [{r["id"]}](changes/{r["id"]}.json) | {cell(r["request"]["scope"])} | {r["stage"]} | {next_action(r)} |')
    lines += ["", "### Registered controlled candidates", "",
              "| Document | Purpose and applicability | Local edition | Authoring contract | Source or change basis | Operational destination | Document state and evidence |",
              "|---|---|---|---|---|---|---|"]
    for r in records:
        s = next((e["data"] for e in reversed(r["history"]) if e["action"] in ("prepare", "draft")), None)
        if s:
            state = "blocked" if hold_reason(r) else {"intake": "draft", "withdrawn": "withdrawn", "superseded": "superseded"}.get(r["stage"], "prepared")
            absent = s["before"] is None if "before" in s else s["source_hash"] is None
            source = "absent (new subject)" if absent else f'[Source](../{s["destination"]})'
            contract = s["contract"].replace("|", "&#124;").replace("<", "&lt;")
            lines.append(f'| [Candidate]({s["candidate"][12:]}) | {cell(s["purpose"])} | {cell(s["edition"])} | {contract} | {cell(r["request"]["basis"])}; {source}; source edition {cell(s["source_edition"])} | {"verified" if r["stage"] == "closed" else "intended"}: {s["destination"]} | {state}; [{r["stage"]}](changes/{r["id"]}.json) |')
    return "\n".join(lines) + "\n\n" + END


def index_output(store, records):
    before = store.read("doc-updates/INDEX.md")
    require(before is not None, "Missing updates index")
    value = before.decode("utf-8")
    require(value.count(START) == 1 and value.count(END) == 1 and value.index(START) < value.index(END),
            "Missing or malformed navigation markers; explicitly migrate preserved catalog")
    start, end = value.index(START), value.index(END) + len(END)
    return before, (value[:start] + navigation(records) + value[end:]).encode()


def coherent(store, records):
    before, after = index_output(store, records)
    require(before == after, "Interrupted or edited updates register; next: reconcile")


def save(store, record, records):
    validate(record)
    if record["stage"] not in ("closed", "rejected", "withdrawn", "superseded"):
        require(not any(r["id"] != record["id"] and r["request"]["destination"] == record["request"]["destination"]
                        and r["stage"] not in ("closed", "rejected", "withdrawn", "superseded") for r in records),
                "Competing active change; supersede or resolve before reopening")
    name = "doc-updates/changes/" + record["id"] + ".json"
    store.write(name, encoded(record), store.read(name, private=True))
    all_records = sorted([r for r in records if r["id"] != record["id"]] + [record], key=lambda r: r["id"])
    before, after = index_output(store, all_records)
    if before != after:
        store.write("doc-updates/INDEX.md", after, before)


def links(store, content, location, outputs):
    """Inline relative Markdown links/images only; semantic review covers other syntax."""
    for target in re.findall(r"!?\[[^\]\n]*\]\(([^)\s]+)\)", content):
        if target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0]
        require(not target.startswith(("/", "$", "~")), "Absolute link outside supported layout")
        resolved = os.path.normpath(str(PurePosixPath(location).parent / target))
        path_name(resolved)
        require(resolved in outputs or store.read(resolved) is not None, "Missing linked resource")


def catalog_check(before, after, destination, edition):
    """One exact four-field row replacement/addition; preserve all unrelated bytes."""
    name = destination[len("doc-operations/"):]
    def row(line):
        return line.startswith("| ") and f"]({name})" in line
    old_rows = [line for line in before.splitlines(True) if row(line)]
    new_rows = [line for line in after.splitlines(True) if row(line)]
    require(len(old_rows) <= 1 and len(new_rows) == 1, "Ambiguous or missing operational row")
    cells = new_rows[0].strip().split("|")[1:-1]
    require(len(cells) == 4 and cells[2].strip() == edition and all(c.strip() for c in cells),
            "Invalid operational row or published edition")
    cleaned_before = "".join(line for line in before.splitlines(True) if not row(line) and
                             not line.startswith("No operational documents are currently registered."))
    cleaned_after = "".join(line for line in after.splitlines(True) if not row(line) and
                            not line.startswith("No operational documents are currently registered."))
    require(cleaned_before == cleaned_after, "Catalog change includes unrelated guidance")
    require(not any(line.startswith("No operational documents are currently registered.")
                    for line in after.splitlines()), "Stale empty operational catalog statement")


def contract_sources(contract):
    text(contract)
    if contract.startswith("uncovered purpose:"):
        return ["doc-specs/INDEX.md"]
    match = re.search(r"\[[^\]]+\]\(\.\./(doc-specs/[A-Za-z0-9_./-]+\.spec\.md)\)", contract)
    require(match, "Missing selected contract link or explicit uncovered purpose")
    return ["doc-specs/INDEX.md", path_name(match[1], "doc-specs")]


def authoring_sources(store, contract):
    result = {}
    for name in contract_sources(contract):
        data = store.read(name)
        require(data and data.strip(), "Missing authoring catalog/contract resource")
        result[name] = sha(data)
    return result


def current(store, r, recovery=False, closed=False):
    s = latest(r, "prepare")
    require(s is not None, "Missing prepared snapshot")
    snapshot_shape(s)
    fresh(store.read(s["candidate"]) is not None and sha(store.read(s["candidate"])) == s["candidate_hash"],
            "Stale candidate; next: rework")
    fresh(store.read(s["output_resource"]) == s["output"].encode() and
            store.read(s["catalog_resource"]) == s["catalog"].encode(),
            "Stale publishable content; next: rework")
    for e in (s["basis"], s["checks"]):
        fresh(store.evidence(e["path"]) == e, "Stale check or authoring basis; next: rework")
    fresh(authoring_sources(store, s["contract"]) == s["authoring_sources"],
            "Stale authoring source catalog/contract; next: rework")
    for action in ("open", "review"):
        data = latest(r, action)
        if data:
            fresh(store.evidence(data["evidence"]["path"]) == data["evidence"],
                    "Stale review evidence; next: rework")
    before = None if s["before"] is None else s["before"].encode()
    document, catalog = store.read(s["destination"]), store.read("doc-operations/INDEX.md")
    output, catalog_output = s["output"].encode(), s["catalog"].encode()
    if closed:
        require(document == output and catalog == catalog_output, "Closed publication no longer matches approved output")
    elif recovery:
        require(document in (before, output) and catalog in (s["catalog_before"].encode(), catalog_output),
                "Conflicting partial publication; preserve edits and resolve separately")
    else:
        fresh(document == before and catalog == s["catalog_before"].encode(), "Stale source or catalog baseline; next: rework")
    catalog_check(s["catalog_before"], s["catalog"], s["destination"], s["edition"])
    links(store, s["contract"], "doc-updates/INDEX.md", set())
    outputs = {s["destination"], "doc-operations/INDEX.md"}
    links(store, s["output"], s["destination"], outputs)
    links(store, s["catalog"], "doc-operations/INDEX.md", outputs)
    return s


def capture(action, snapshot, scope):
    require(sys.stdin.isatty() and sys.stdout.isatty(), "Operator decision requires operator-performed terminal action")
    print(f"Decision: {action}; snapshot: {snapshot}; scope: {scope}")
    try:
        response = input(f"Operator: type '{action} {snapshot}' to decide: ")
        require(response == action + " " + snapshot, "No explicit operator decision")
        authority = False
        if action == "approve":
            authority = input(f"To authorize writes to this scope, type 'authorize {snapshot}' (otherwise leave empty): ") == "authorize " + snapshot
    except (EOFError, KeyboardInterrupt) as error:
        raise Refusal("No complete operator decision; terminal interaction interrupted") from error
    return {"snapshot": snapshot, "scope": scope, "authority": authority,
            "capture": "operator-terminal", "decision": action}


def hold_reason(record):
    for e in reversed(record["history"]):
        if e["action"] in ("release", "rework", "reopen"):
            return None
        if e["action"] == "hold":
            return e["reason"]
    return None


def next_action(record):
    if hold_reason(record):
        return "release (with observed prerequisite evidence)"
    if record["stage"] == "intake" and latest(record, "draft") is None:
        return "draft"
    if record["stage"] in ("prepared", "review", "reviewed", "approved"):
        try:
            draft_check(latest(record, "draft"), latest(record, "prepare"))
        except Refusal:
            return "rework (then register current draft)"
    return NEXT[record["stage"]]


def publish(store, record, records, actor):
    if record["stage"] == "closed":
        current(store, record, closed=True)
        coherent(store, records)
        return
    require(record["stage"] in ("approved", "publishing"), "Missing prerequisite stage: approved")
    require(not hold_reason(record), "Unreleased hold; next: release with observed resumption evidence")
    approval = latest(record, "approve")
    require(approval and approval["authority"], "Missing target publication authority; next: rework and obtain scoped approval")
    s = current(store, record, recovery=record["stage"] == "publishing")
    if record["stage"] == "approved":
        operational_destination(s["destination"])
    for name in (s["destination"], "doc-operations/INDEX.md"):
        store.writable(name)
    # Readable baselines in the immutable snapshot provide recovery evidence.
    if record["stage"] == "approved":
        draft_check(latest(record, "draft"), s)
        coherent(store, records)
        event(record, "publish", actor, "prepublication validation and recorded baseline recovery",
              {"snapshot": s["id"], "evidence": "intent; runtime write access will be tested by filesystem"})
        save(store, record, records)  # durable intent precedes either operational write
    current(store, record, recovery=True)  # same gate immediately before writes
    for name, content in ((s["destination"], s["output"].encode()),
                          ("doc-operations/INDEX.md", s["catalog"].encode())):
        current(store, record, recovery=True)
        before = store.read(name)
        baseline = (None if s["before"] is None else s["before"].encode()) if name == s["destination"] else s["catalog_before"].encode()
        require(before in (baseline, content), "Conflicting change before final write; preserved")
        if before != content:
            store.write(name, content, before)
    current(store, record, closed=True)
    event(record, "close", actor, "observed SHA-256 outputs, links and catalog edition verified",
          {"snapshot": s["id"], "evidence": "document and operational catalog equal approved bytes"})
    save(store, record, records)


def run(store, args):
    records = store.records()
    if args.command == "intake":
        packet = parse(store.read(path_name(args.packet, "doc-updates")))
        fields(packet, ("key", "basis", "scope", "destination", "source_edition", "author", "legacy"))
        existing = next((r for r in records if r["request"]["key"] == packet["key"]), None)
        if existing:
            require(all(existing["request"][k] == v for k, v in packet.items()), "Incompatible duplicate request key")
            coherent(store, records)
            return existing
        operational_destination(packet["destination"])
        require(not any(r["request"]["destination"] == packet["destination"] and
                        r["stage"] not in ("closed", "rejected", "withdrawn", "superseded") for r in records),
                "Compatible active request exists; inspect and reuse its ID")
        coherent(store, records)
        before = store.read(path_name(packet["destination"], "doc-operations"))
        require((before is not None) or packet["source_edition"] == "absent (new subject)", "Confirm new subject source absence")
        packet["source_hash"] = None if before is None else sha(before)
        record = {"schema": 2, "id": uuid.uuid4().hex, "request": packet, "stage": None, "history": []}
        require(not any(r["id"] == record["id"] for r in records), "Change ID collision; retry intake with same request")
        event(record, "intake", packet["author"], args.packet, {"note": "authorized incoming request registered; legacy evidence unconfirmed" if packet["legacy"] else "authorized incoming request registered"})
        save(store, record, records)
        return record
    require(args.change and re.fullmatch(r"[0-9a-f]{32}", args.change), "A valid change ID is required")
    record = next((r for r in records if r["id"] == args.change), None)
    require(record is not None, "Unknown change ID")
    if args.command in ("status", "validate", "show"):
        coherent(store, records)
        if record["stage"] in ("prepared", "review", "reviewed", "approved", "publishing", "closed"):
            current(store, record, recovery=record["stage"] == "publishing", closed=record["stage"] == "closed")
        if args.command == "show":
            s = latest(record, "prepare")
            require(s, "Missing prepared snapshot")
            print("Snapshot: " + s["id"])
            print("".join(difflib.unified_diff((s["before"] or "").splitlines(True), s["output"].splitlines(True), fromfile="operational baseline", tofile=s["destination"])))
            print("".join(difflib.unified_diff(s["catalog_before"].splitlines(True), s["catalog"].splitlines(True), fromfile="catalog baseline", tofile="approved catalog output")))
        return record
    try:
        if args.command not in ("reconcile", "publish"):
            coherent(store, records)
        if args.command in FORWARD and args.command != "publish":
            destination(record["stage"], args.command)
            require(not hold_reason(record), "Unreleased hold; next: release with observed resumption evidence")
        if args.command == "draft":
            destination(record["stage"], "draft")
            operational_destination(record["request"]["destination"])
            require(not hold_reason(record), "Unreleased hold; next: release with observed resumption evidence")
            p = parse(store.read(path_name(args.packet, "doc-updates")))
            fields(p, ("candidate", "purpose", "edition", "contract", "source_edition"))
            candidate = store.read(path_name(p["candidate"], "doc-updates"))
            require(candidate and candidate.strip(), "Missing draft candidate")
            authoring_sources(store, p["contract"])
            source = store.read(record["request"]["destination"])
            data = dict(p, candidate_hash=sha(candidate), destination=record["request"]["destination"],
                        source_hash=None if source is None else sha(source))
            require(source is not None or p["source_edition"] == "absent (new subject)", "Confirm draft source absence")
            if latest(record, "draft") == data:
                return record
            event(record, "draft", args.actor, args.packet, data)
        elif args.command == "prepare":
            operational_destination(record["request"]["destination"])
            p = parse(store.read(path_name(args.packet, "doc-updates")))
            fields(p, ("candidate", "output", "catalog", "edition", "source_edition", "purpose", "contract", "checks", "basis", "obligations"))
            require(p["obligations"] == [], "Unresolved mandatory authoring obligations")
            candidate = store.read(path_name(p["candidate"], "doc-updates"))
            output = store.read(path_name(p["output"], "doc-updates"))
            catalog = store.read(path_name(p["catalog"], "doc-updates"))
            before = store.read(record["request"]["destination"])
            baseline = store.read("doc-operations/INDEX.md")
            require(candidate and output and catalog and baseline, "Missing candidate or publication resources")
            if not any(e["action"] in ("rework", "reopen") for e in record["history"]):
                require((None if before is None else sha(before)) == record["request"]["source_hash"],
                        "Source changed after intake; next: rework")
            s = {"candidate": p["candidate"], "candidate_hash": sha(candidate), "output": output.decode(),
                 "output_resource": p["output"], "catalog_resource": p["catalog"],
                 "catalog": catalog.decode(), "destination": record["request"]["destination"],
                 "before": None if before is None else before.decode(), "catalog_before": baseline.decode(),
                 "edition": p["edition"], "source_edition": p["source_edition"], "purpose": p["purpose"],
                 "contract": p["contract"], "checks": store.evidence(p["checks"]), "basis": store.evidence(p["basis"]),
                 "authoring_sources": authoring_sources(store, p["contract"])}
            require(before is not None or s["source_edition"] == "absent (new subject)", "Missing source absence evidence")
            draft_check(latest(record, "draft"), s)
            s["id"] = sha(encoded(s))
            event(record, "prepare", args.actor, args.packet, s)
            current(store, record)
        elif args.command in ("open", "review"):
            s = current(store, record)
            draft_check(latest(record, "draft"), s)
            data = {"snapshot": s["id"], "evidence": store.evidence(args.evidence)}
            if args.command == "review":
                p = parse(store.read(args.evidence))
                fields(p, ("snapshot", "findings", "checks_passed"))
                require(p["snapshot"] == s["id"], "Review report is not bound to snapshot")
                data.update(findings=p["findings"], checks_passed=p["checks_passed"])
            event(record, args.command, args.actor, args.evidence, data)
        elif args.command in ("approve", "reject", "withdraw", "supersede", "reopen"):
            destination(record["stage"], args.command)
            if args.command == "supersede":
                require(any(r["id"] != record["id"] and r["id"] in args.note for r in records),
                        "Supersession requires an existing replacement change ID in its reason")
            s = current(store, record) if args.command == "approve" else latest(record, "prepare")
            if args.command == "approve":
                draft_check(latest(record, "draft"), s)
            identity = s["id"] if s else record["id"]
            scope = record["request"]["destination"] + " + doc-operations/INDEX.md"
            if args.command == "approve":
                print("Use show to inspect exact publication diffs before deciding.")
            data = capture(args.command, identity, scope)
            event(record, args.command, "local-account:" + str(os.getuid()), "operator-terminal response captured in this event", data,
                  args.note if args.command != "approve" else "")
        elif args.command == "publish":
            publish(store, record, records, args.actor)
            return record
        elif args.command in ("rework", "hold", "release", "correct", "reconcile"):
            if args.command == "release":
                require(hold_reason(record), "No temporary hold to release")
            event(record, args.command, args.actor, args.evidence, {"note": text(args.note)},
                  args.note if args.command in ("rework", "hold") else "")
        else:
            raise Refusal("Unknown command")
        save(store, record, records)
    except (Refusal, OSError, ValueError, TypeError, EOFError, KeyboardInterrupt) as error:
        # Re-read after publication: intent or even closure may already be durable.
        try:
            durable = parse(store.read("doc-updates/changes/" + record["id"] + ".json", private=True))
            validate(durable)
            reason = str(error) if isinstance(error, Refusal) else "Filesystem or malformed input failure"
            if isinstance(error, StaleSnapshot) and durable["stage"] in ("prepared", "review", "reviewed", "approved"):
                event(durable, "rework", args.actor, "detected snapshot invalidation",
                      {"note": "Checks, review and approval invalidated; earlier evidence retained"}, reason)
            event(durable, "refuse", args.actor, "tool validation of requested " + args.command,
                  {"note": "Rejected attempt: " + args.command}, reason)
            save(store, durable, records)
            stage = durable["stage"]
            raise Refusal(f"Attempted bypass/action refused: {reason}; stage: {stage}; next: {next_action(durable)}; refusal recorded") from error
        except Refusal as refusal:
            if "refusal recorded" in str(refusal):
                raise
            raise Refusal("Action refused; refusal could not be durably recorded; preserve state and inspect/reconcile") from error
        except (OSError, ValueError, TypeError):
            raise Refusal("Action refused; refusal could not be durably recorded; preserve state and inspect/reconcile") from error
    return record


def cli(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Explicit authorized documentation root")
    parser.add_argument("command", choices=("intake", "draft", "prepare", "open", "review", "approve", "publish", "status", "validate", "show", "rework", "reject", "withdraw", "supersede", "reopen", "hold", "release", "correct", "reconcile"))
    parser.add_argument("--change", help="Stable change ID")
    parser.add_argument("--packet", help="Root-relative intake/preparation JSON")
    parser.add_argument("--evidence", default="session:explicit-request", help="Local evidence path for open/review; reference for other actions")
    parser.add_argument("--actor", default="executing-agent", help="Actually established agent role identifier")
    parser.add_argument("--note", default="", help="Hold, rework, correction, terminal or reconciliation reason")
    args = parser.parse_args(argv)
    store = None
    try:
        store = Store(args.root)
        record = run(store, args)
        print(json.dumps({"change": record["id"], "stage": record["stage"], "next": next_action(record),
                          "hold": hold_reason(record),
                          "snapshot": (latest(record, "prepare") or {}).get("id")}, sort_keys=True))
        return 0
    except (Refusal, OSError, ValueError, TypeError, KeyError, EOFError, KeyboardInterrupt) as error:
        message = str(error) if isinstance(error, Refusal) else "Input/filesystem failure; inspect preserved state"
        if "refusal recorded" not in message and "could not be durably recorded" not in message:
            message += "; refusal could not be durably recorded; next: inspect valid state/resources and reconcile if needed"
        print(message, file=sys.stderr)
        return 2
    finally:
        if store:
            store.close()


if __name__ == "__main__":
    sys.exit(cli())
