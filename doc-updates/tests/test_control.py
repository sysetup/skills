"""Offline review-control tests. Operator terminal decisions are simulated."""

import contextlib
import copy
import importlib.util
import io
import inspect
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


PROJECT = Path(__file__).resolve().parent.parent
SCRIPT = PROJECT / "scripts/doc-control.py"
SPEC = importlib.util.spec_from_file_location("doc_control", SCRIPT)
control = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(control)


class Terminal(io.StringIO):
    def isatty(self):
        return True


class ControlTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".review-test-", dir=os.environ.get("DOC_UPDATES_TEST_TMPDIR", PROJECT / "tests"))
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.store = control.Store(self.root)
        self.addCleanup(self.store.close)
        self.write("doc-updates/INDEX.md", ("# Synthetic candidate index\n\n" +
                   control.navigation([]) + "\n").encode())
        self.write("doc-operations/INDEX.md", b"# Synthetic operations index\n\n"
                   b"No operational documents are currently registered.\n\n"
                   b"| Document | Purpose and applicability | Local edition | Authoring contract |\n"
                   b"|---|---|---|---|\n")
        self.write("doc-operations/detail.md", b"# Existing detail\n")
        self.write("doc-specs/INDEX.md", b"# Synthetic readable catalog; no matching type\n")
        self.original_catalog = self.store.read("doc-operations/INDEX.md")
        self.packet = {"key": "request:one", "basis": "session:authorized new operational subject",
                       "scope": "One synthetic offline guide", "destination": "doc-operations/a.md",
                       "source_edition": "absent (new subject)", "author": "test-author", "legacy": False}
        self.write("doc-updates/request.json", control.encoded(self.packet))
        self.change = self.call("intake", "--packet", "doc-updates/request.json")["change"]
        self.write("doc-updates/candidate.md", b"# Guide\nEdition: 2\n[Detail](../doc-operations/detail.md)\n")
        self.write("doc-updates/output.md", b"# Guide\nEdition: 2\n[Detail](detail.md)\n")
        catalog = self.original_catalog.decode()
        catalog = "".join(line for line in catalog.splitlines(True)
                          if not line.startswith("No operational documents are currently registered."))
        catalog = catalog.replace("|---|---|---|---|\n", "|---|---|---|---|\n| [Guide](a.md) | Test subject | 2 | Uncovered native purpose |\n", 1)
        self.write("doc-updates/catalog.md", catalog.encode())
        self.write("doc-updates/checks.md", b"Observed: links, scope and native content checked; no open obligation\n")
        self.write("doc-updates/basis.md", b"Readable contract catalog; synthetic uncovered purpose; native Markdown\n")
        self.write("doc-updates/pr.md", b"Please review this change's captured final document and catalog diff\n")
        self.preparation = {"candidate": "doc-updates/candidate.md", "output": "doc-updates/output.md",
                            "catalog": "doc-updates/catalog.md", "edition": "2",
                            "source_edition": "absent (new subject)", "purpose": "Synthetic offline scope",
                            "contract": "uncovered purpose: native Markdown", "checks": "doc-updates/checks.md",
                            "basis": "doc-updates/basis.md", "obligations": []}
        self.write("doc-updates/preparation.json", control.encoded(self.preparation))

    def write(self, name, data):
        self.store.write(name, data, self.store.read(name))

    def record(self):
        return control.parse(self.store.read("doc-updates/changes/" + self.change + ".json"))

    def call(self, command, *extra, success=True):
        output, error = Terminal(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            # CLI gets its own root lock; do not keep our fixture lock acquired.
            import fcntl
            fcntl.flock(self.store.fd, fcntl.LOCK_UN)
            try:
                code = control.cli(["--root", str(self.root), command,
                                    *([] if command == "intake" else ["--change", self.change]), *extra])
            finally:
                fcntl.flock(self.store.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        self.assertEqual(code, 0 if success else 2, error.getvalue())
        if success:
            return json.loads(output.getvalue().splitlines()[-1])
        return error.getvalue()

    def register_draft(self):
        packet = {k: self.preparation[k] for k in
                  ("candidate", "purpose", "edition", "contract", "source_edition")}
        self.write("doc-updates/draft.json", control.encoded(packet))
        return self.call("draft", "--packet", "doc-updates/draft.json")

    def prepare(self):
        self.register_draft()
        return self.call("prepare", "--packet", "doc-updates/preparation.json")

    def review(self, findings=None, passed=True):
        identity = control.latest(self.record(), "prepare")["id"]
        self.write("doc-updates/review.json", control.encoded({"snapshot": identity,
                   "findings": findings or [], "checks_passed": passed}))
        return self.call("review", "--evidence", "doc-updates/review.json",
                         success=passed and not any(f["blocking"] and f["disposition"] != "resolved"
                                                   for f in (findings or [])))

    def to_reviewed(self):
        self.prepare()
        self.call("open", "--evidence", "doc-updates/pr.md")
        self.review()

    def decide(self, action="approve", authority=True):
        r = self.record()
        s = control.latest(r, "prepare")
        identity = s["id"] if s else self.change
        responses = [action + " " + identity]
        if action == "approve":
            responses += ["authorize " + identity if authority else ""]
        output = Terminal()
        import fcntl
        fcntl.flock(self.store.fd, fcntl.LOCK_UN)
        try:
            with contextlib.redirect_stdout(output), patch.object(sys.stdin, "isatty", return_value=True), \
                    patch("builtins.input", side_effect=responses):
                code = control.cli(["--root", str(self.root), action, "--change", self.change,
                                    "--note", "Actual synthetic decision; replacement " + getattr(self, "replacement", "none")])
        finally:
            fcntl.flock(self.store.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        self.assertEqual(code, 0, output.getvalue())

    def assert_unpublished(self):
        self.assertIsNone(self.store.read("doc-operations/a.md"))
        self.assertEqual(self.store.read("doc-operations/INDEX.md"), self.original_catalog)

    def test_complete_sequence_exact_output_links_and_ordered_evidence(self):
        self.to_reviewed()
        self.decide()
        result = self.call("publish")
        self.assertEqual(result["stage"], "closed")
        r = self.record()
        self.assertEqual([e["action"] for e in r["history"]],
                         ["intake", "draft", "prepare", "open", "review", "approve", "publish", "close"])
        self.assertEqual(self.store.read("doc-operations/a.md"), self.store.read("doc-updates/output.md"))
        self.assertEqual(self.store.read("doc-operations/INDEX.md"), self.store.read("doc-updates/catalog.md"))
        self.assertIn(b"[Detail](detail.md)", self.store.read("doc-operations/a.md"))
        self.assertIn(b"[closed]", self.store.read("doc-updates/INDEX.md"))
        control.validate(r)

    def test_draft_registration_is_separate_and_retry_has_no_duplicate_event(self):
        packet = {k: self.preparation[k] for k in ("candidate", "purpose", "edition", "contract", "source_edition")}
        self.write("doc-updates/draft.json", control.encoded(packet))
        self.call("draft", "--packet", "doc-updates/draft.json")
        index = self.store.read("doc-updates/INDEX.md")
        self.assertIn(b"[Candidate](candidate.md)", index)
        self.assertIn(b"draft; [intake]", index)
        before = self.record()
        self.call("draft", "--packet", "doc-updates/draft.json")
        self.assertEqual(self.record(), before)
        self.call("publish", success=False)
        self.assert_unpublished()
        self.prepare()
        self.assertEqual(self.record()["stage"], "prepared")

    def test_abandoned_private_staging_is_preserved_without_becoming_a_master(self):
        name = "doc-updates/changes/.doc-control-" + "a" * 32
        self.write(name, b"Interrupted partial JSON staging\n")
        self.call("status")
        self.assertEqual(len(self.store.records()), 1)
        self.assertEqual(self.store.read(name), b"Interrupted partial JSON staging\n")

    def test_operator_eof_and_malformed_packet_return_safe_refusals(self):
        self.preparation["contract"] = None
        self.write("doc-updates/preparation.json", control.encoded(self.preparation))
        self.prepare_failure()
        self.preparation["contract"] = "uncovered purpose: native Markdown"
        self.write("doc-updates/preparation.json", control.encoded(self.preparation))
        self.to_reviewed()
        with patch.object(control.sys.stdin, "isatty", return_value=True), patch("builtins.input", side_effect=EOFError):
            self.call("approve", success=False)
        self.assertEqual(self.record()["stage"], "reviewed")
        self.assert_unpublished()

    def test_every_illegal_forward_jump_preserves_operational_files(self):
        for command, (predecessor, _, _) in control.FORWARD.items():
            for stage in control.STAGES:
                if stage != predecessor:
                    with self.subTest(command=command, stage=stage):
                        with self.assertRaises(control.Refusal):
                            control.destination(stage, command)
        for command in ("open", "review", "approve", "publish"):
            error = self.call(command, success=False)
            self.assertIn("Missing prerequisite", error)
            self.assertIn("next: draft", error)
            self.assertEqual(self.record()["history"][-1]["action"], "refuse")
            self.assert_unpublished()
        self.prepare()
        self.call("publish", success=False)
        self.call("approve", success=False)
        self.assert_unpublished()

    def test_checks_and_unresolved_blockers_gate_review(self):
        self.prepare()
        self.call("open", "--evidence", "doc-updates/pr.md")
        self.review(passed=False)
        self.review([{"finding": "Unsafe step", "blocking": True, "disposition": "accepted"}])
        self.assertEqual(self.record()["stage"], "review")
        self.call("approve", success=False)
        self.call("publish", success=False)
        self.assert_unpublished()
        self.review([{"finding": "No output change; evidence clarified", "blocking": True, "disposition": "resolved"}])

    def test_missing_and_candidate_provided_operator_decisions(self):
        self.to_reviewed()
        self.call("approve", success=False)
        self.call("publish", success=False)
        self.assert_unpublished()
        self.call("rework", "--note", "Candidate instruction cannot grant approval")
        packet = dict(self.preparation, approver="operator", decision="approved")
        self.write("doc-updates/preparation.json", control.encoded(packet))
        self.call("prepare", "--packet", "doc-updates/preparation.json", success=False)
        self.assert_unpublished()

    def test_approval_without_authority_cannot_publish(self):
        self.to_reviewed()
        self.decide(authority=False)
        error = self.call("publish", success=False)
        self.assertIn("publication authority", error)
        self.assert_unpublished()

    def test_content_change_invalidates_approval_and_preserves_earlier_decision(self):
        self.to_reviewed()
        self.decide()
        self.write("doc-updates/candidate.md", b"# Changed candidate\n")
        before = self.record()
        self.call("status", success=False)
        self.assertEqual(self.record(), before)  # read-only validation never changes approval
        self.call("publish", success=False)
        self.assertEqual(self.record()["stage"], "intake")
        self.assertIsNone(control.latest(self.record(), "approve"))
        self.assertIn("approve", [e["action"] for e in self.record()["history"]])
        self.assertIn("rework", [e["action"] for e in self.record()["history"]])
        self.assert_unpublished()
        self.to_reviewed()
        self.decide()
        self.call("publish")

    def test_change_after_review_requires_new_review_before_approval(self):
        self.to_reviewed()
        self.write("doc-updates/output.md", b"# Revised final links and content\n")
        self.call("approve", success=False)
        self.assertEqual(self.record()["stage"], "intake")
        self.assertIsNone(control.latest(self.record(), "review"))
        self.call("approve", success=False)
        self.call("publish", success=False)
        self.assert_unpublished()

    def test_output_catalog_source_basis_and_review_changes_are_stale(self):
        for name in ("doc-updates/output.md", "doc-updates/catalog.md", "doc-updates/basis.md",
                     "doc-updates/checks.md", "doc-updates/review.json", "doc-operations/INDEX.md",
                     "doc-operations/a.md", "doc-specs/INDEX.md"):
            with self.subTest(name=name):
                # Each subcase starts a new fixture to avoid terminal/history reset.
                case = ControlTests("test_help_and_zero_args_are_safe")
                case.setUp()
                try:
                    case.to_reviewed()
                    case.decide()
                    case.write(name, b"Conflicting content\n")
                    expected_doc = case.store.read("doc-operations/a.md")
                    expected_catalog = case.store.read("doc-operations/INDEX.md")
                    case.call("publish", success=False)
                    self.assertEqual(case.record()["stage"], "intake")
                    self.assertEqual(case.store.read("doc-operations/a.md"), expected_doc)
                    self.assertEqual(case.store.read("doc-operations/INDEX.md"), expected_catalog)
                finally:
                    case.doCleanups()

    def test_unknown_states_malformed_records_and_inconsistent_history_fail_closed(self):
        original = self.record()
        mutations = []
        for field, value in (("stage", "invented"), ("schema", True), ("surprise", "extra")):
            r = copy.deepcopy(original)
            r[field] = value
            mutations.append(r)
        for field, value in (("seq", 5), ("from", "approved"), ("utc", "2026-99-01T00:00:00.000000Z"),
                             ("role", "operator"), ("outcome", "proposed")):
            r = copy.deepcopy(original)
            r["history"][0][field] = value
            mutations.append(r)
        name = "doc-updates/changes/" + self.change + ".json"
        for r in mutations:
            with self.subTest(r=r):
                self.write(name, control.encoded(r))
                self.call("publish", success=False)
                self.assertEqual(self.store.read(name), control.encoded(r))
                self.assert_unpublished()
        self.write(name, b'{"schema":1,"schema":1}')
        self.call("publish", success=False)
        self.assert_unpublished()
        self.write(name, b"[" * 2000 + b"0" + b"]" * 2000)
        self.call("publish", success=False)
        self.assert_unpublished()

    def test_rejection_withdrawal_supersession_reopening_no_shortcuts(self):
        packet = dict(self.packet, key="replacement", destination="doc-operations/replacement.md")
        self.write("doc-updates/replacement.json", control.encoded(packet))
        self.replacement = self.call("intake", "--packet", "doc-updates/replacement.json")["change"]
        for action, terminal in (("reject", "rejected"), ("withdraw", "withdrawn"), ("supersede", "superseded")):
            self.decide(action)
            self.assertEqual(self.record()["stage"], terminal)
            self.call("publish", success=False)
            self.call("prepare", "--packet", "doc-updates/preparation.json", success=False)
            self.decide("reopen")
            self.assertEqual(self.record()["stage"], "intake")
            self.assert_unpublished()
        self.to_reviewed()
        self.decide()
        self.call("publish")
        self.call("rework", "--note", "Cannot bypass published change", success=False)

    def test_selected_contract_bytes_are_bound_to_review(self):
        self.write("doc-specs/sop.spec.md", b"# Synthetic selected contract\n")
        self.preparation["contract"] = "SOP@synthetic [Read](../doc-specs/sop.spec.md)"
        self.write("doc-updates/preparation.json", control.encoded(self.preparation))
        self.to_reviewed()
        self.decide()
        self.write("doc-specs/sop.spec.md", b"# Changed contract obligations\n")
        self.call("publish", success=False)
        self.assertEqual(self.record()["stage"], "intake")
        self.assert_unpublished()

    def test_runtime_permission_denial_precedes_publication_intent(self):
        self.to_reviewed()
        self.decide()
        with patch.object(control.os, "access", return_value=False):
            error = self.call("publish", success=False)
        self.assertIn("runtime target write permission", error)
        self.assertEqual(self.record()["stage"], "approved")
        self.assertNotIn("publish", [e["action"] for e in self.record()["history"]])
        self.assert_unpublished()

    def test_closure_record_failure_after_outputs_safely_resumes(self):
        self.to_reviewed()
        self.decide()
        original_write = control.Store.write
        def fail_closure(store, name, data, before):
            if name.endswith(self.change + ".json") and control.parse(data)["stage"] == "closed":
                raise OSError("closure record interrupted")
            return original_write(store, name, data, before)
        with patch.object(control.Store, "write", fail_closure):
            self.call("publish", success=False)
        self.assertEqual(self.record()["stage"], "publishing")
        self.assertEqual(self.store.read("doc-operations/a.md"), self.store.read("doc-updates/output.md"))
        self.assertEqual(self.store.read("doc-operations/INDEX.md"), self.store.read("doc-updates/catalog.md"))
        self.call("publish")
        self.assertEqual(self.record()["stage"], "closed")

    def test_intake_index_interruption_has_present_history_and_recovery(self):
        packet = dict(self.packet, key="interrupted-intake", destination="doc-operations/interrupted.md")
        self.write("doc-updates/interrupted-request.json", control.encoded(packet))
        original_write = control.Store.write
        def fail_index(store, name, data, before):
            if name == "doc-updates/INDEX.md":
                raise OSError("intake index interrupted")
            return original_write(store, name, data, before)
        with patch.object(control.Store, "write", fail_index):
            self.call("intake", "--packet", "doc-updates/interrupted-request.json", success=False)
        self.change = next(r["id"] for r in self.store.records() if r["request"]["key"] == packet["key"])
        self.assertEqual(len(self.record()["history"]), 1)
        self.call("reconcile", "--note", "Actual intake record exists; index was interrupted")
        self.assertEqual(self.call("intake", "--packet", "doc-updates/interrupted-request.json")["change"], self.change)

    def test_revision_preserves_baseline_and_other_catalog_rows(self):
        self.write("doc-operations/revised.md", b"# Original edition\nEdition: 1\n")
        old_row = b"| [Guide](revised.md) | Test subject | 1 | Uncovered native purpose |\n"
        other_row = b"| [Other](detail.md) | Unrelated guidance | unspecified | Uncovered native purpose |\n"
        baseline = b"".join(line for line in self.original_catalog.splitlines(True)
                            if not line.startswith(b"No operational documents are currently registered."))
        baseline = baseline.replace(b"|---|---|---|---|\n", b"|---|---|---|---|\n" + old_row + other_row, 1)
        self.write("doc-operations/INDEX.md", baseline)
        packet = dict(self.packet, key="revision", destination="doc-operations/revised.md", source_edition="1")
        self.write("doc-updates/revision-request.json", control.encoded(packet))
        self.change = self.call("intake", "--packet", "doc-updates/revision-request.json")["change"]
        self.preparation["source_edition"] = "1"
        self.write("doc-updates/preparation.json", control.encoded(self.preparation))
        proposed = baseline.replace(old_row, old_row.replace(b"| 1 |", b"| 2 |"))
        self.write("doc-updates/catalog.md", proposed)
        self.to_reviewed()
        s = control.latest(self.record(), "prepare")
        self.assertEqual(s["before"], "# Original edition\nEdition: 1\n")
        self.assertEqual(self.record()["request"]["source_hash"], control.sha(s["before"].encode()))
        self.decide()
        self.call("publish")
        self.assertEqual(self.store.read("doc-operations/detail.md"), b"# Existing detail\n")
        self.assertEqual(self.store.read("doc-operations/revised.md"), self.store.read("doc-updates/output.md"))
        self.assertIn(other_row, self.store.read("doc-operations/INDEX.md"))

    def test_hold_release_and_correction_keep_confirmed_stage(self):
        self.prepare()
        self.call("hold", "--note", "Need verified local evidence", "--evidence", "session:gap")
        self.call("open", "--evidence", "doc-updates/pr.md", success=False)
        self.assertEqual(self.record()["stage"], "prepared")
        self.call("release", "--note", "Observed prerequisite resolved", "--evidence", "session:resolution")
        self.call("correct", "--note", "Event 1 typo clarification; scope unchanged", "--evidence", "session:correction")
        self.call("open", "--evidence", "doc-updates/pr.md")
        self.assertEqual(self.record()["stage"], "review")

    def test_interrupted_publication_resumes_exact_original_approval(self):
        self.to_reviewed()
        self.decide()
        original_write = control.Store.write
        def fail_catalog(store, name, data, before):
            if name == "doc-operations/INDEX.md":
                raise OSError("simulated interruption")
            return original_write(store, name, data, before)
        with patch.object(control.Store, "write", fail_catalog):
            self.call("publish", success=False)
        self.assertEqual(self.record()["stage"], "publishing")
        self.assertEqual(self.store.read("doc-operations/a.md"), self.store.read("doc-updates/output.md"))
        self.assertEqual(self.store.read("doc-operations/INDEX.md"), self.original_catalog)
        self.call("publish")
        self.assertEqual(self.record()["stage"], "closed")
        self.assertEqual(sum(e["action"] == "approve" for e in self.record()["history"]), 1)

    def test_partial_publication_competing_edits_preserved(self):
        self.to_reviewed()
        self.decide()
        original_write = control.Store.write
        def fail_catalog(store, name, data, before):
            if name == "doc-operations/INDEX.md":
                raise OSError("interrupted")
            return original_write(store, name, data, before)
        with patch.object(control.Store, "write", fail_catalog):
            self.call("publish", success=False)
        self.write("doc-operations/a.md", b"Other contributor's change\n")
        self.call("publish", success=False)
        self.assertEqual(self.record()["stage"], "publishing")
        self.assertEqual(self.store.read("doc-operations/a.md"), b"Other contributor's change\n")
        self.assertEqual(self.store.read("doc-operations/INDEX.md"), self.original_catalog)

    def test_conflict_between_gate_and_final_write_is_preserved(self):
        self.to_reviewed()
        self.decide()
        original_read, original_write = control.Store.read, control.Store.write
        def competing_read(store, name, private=False):
            # Simulate a writer outside the lock just before publication's final
            # conflict read, after snapshot validation returned successfully.
            if name == "doc-operations/a.md" and inspect.currentframe().f_back.f_code.co_name == "publish":
                before = original_read(store, name, private)
                original_write(store, name, b"Other contributor's bytes\n", before)
            return original_read(store, name, private)
        with patch.object(control.Store, "read", competing_read):
            self.call("publish", success=False)
        self.assertEqual(self.record()["stage"], "publishing")
        self.assertEqual(self.store.read("doc-operations/a.md"), b"Other contributor's bytes\n")
        self.assertEqual(self.store.read("doc-operations/INDEX.md"), self.original_catalog)

    def test_interrupted_intake_or_closure_index_reconciliation(self):
        self.to_reviewed()
        self.decide()
        original_write = control.Store.write
        def fail_index(store, name, data, before):
            if name == "doc-updates/INDEX.md":
                raise OSError("index interrupted")
            return original_write(store, name, data, before)
        with patch.object(control.Store, "write", fail_index):
            self.call("publish", success=False)
        self.assertEqual(self.record()["stage"], "publishing")  # intent persisted, no output writes
        self.assert_unpublished()
        self.call("reconcile", "--note", "Observed intent/index mismatch")
        self.call("publish")
        # Simulate closure record success but navigation interrupted.
        before = self.store.read("doc-updates/INDEX.md")
        self.write("doc-updates/INDEX.md", before.replace(b"| closed |", b"| publishing |", 1))
        self.call("status", success=False)
        self.call("reconcile", "--note", "Observed closure record and output match; repair navigation")
        self.call("publish")
        self.assertEqual(self.record()["stage"], "closed")

    def test_completed_retries_and_duplicate_intake_are_idempotent(self):
        retry = self.call("intake", "--packet", "doc-updates/request.json")
        self.assertEqual(retry["change"], self.change)
        self.to_reviewed()
        self.decide()
        self.call("publish")
        before = self.record()
        self.call("publish")
        self.call("status")
        self.call("validate")
        self.call("show")
        self.assertEqual(self.record(), before)
        self.assertEqual(len(self.store.records()), 1)
        self.packet["key"] = "parallel-request"
        self.packet["scope"] = "Different request"
        # Closed destination may receive a new change, but existing key cannot silently change.
        self.packet["key"] = "request:one"
        self.write("doc-updates/request.json", control.encoded(self.packet))
        self.call("intake", "--packet", "doc-updates/request.json", success=False)
        self.assertEqual(len(self.store.records()), 1)

    def test_duplicate_active_destination_and_legacy_gaps(self):
        self.packet["key"] = "second-key"
        self.write("doc-updates/request.json", control.encoded(self.packet))
        self.call("intake", "--packet", "doc-updates/request.json", success=False)
        self.assertEqual(len(self.store.records()), 1)
        self.packet.update(key="legacy-key", destination="doc-operations/legacy.md", legacy=True)
        self.write("doc-updates/request.json", control.encoded(self.packet))
        old_change = self.change
        self.change = self.call("intake", "--packet", "doc-updates/request.json")["change"]
        r = self.record()
        self.assertEqual(r["stage"], "intake")
        self.assertEqual(len(r["history"]), 1)
        self.assertIn("unconfirmed", r["history"][0]["data"]["note"])
        self.call("publish", success=False)
        self.change = old_change

    def test_id_collision_never_replaces_an_existing_master(self):
        packet = dict(self.packet, key="unique-key", destination="doc-operations/other.md")
        self.write("doc-updates/other-request.json", control.encoded(packet))
        before = self.record()
        with patch.object(control.uuid, "uuid4", return_value=type("ID", (), {"hex": self.change})()):
            self.call("intake", "--packet", "doc-updates/other-request.json", success=False)
        self.assertEqual(self.record(), before)
        self.assertEqual(len(self.store.records()), 1)

    def test_path_traversal_symlinks_permissions_and_concurrency(self):
        for name in ("../outside", "/absolute", "doc-updates/../outside", "doc-updates/.git/a"):
            self.preparation["candidate"] = name
            self.write("doc-updates/preparation.json", control.encoded(self.preparation))
            self.call("prepare", "--packet", "doc-updates/preparation.json", success=False)
            self.assert_unpublished()
        self.preparation["candidate"] = "doc-updates/link.md"
        os.symlink("candidate.md", self.root / "doc-updates/link.md")
        self.write("doc-updates/preparation.json", control.encoded(self.preparation))
        self.call("prepare", "--packet", "doc-updates/preparation.json", success=False)
        self.preparation["candidate"] = "doc-updates/candidate.md"
        self.write("doc-updates/preparation.json", control.encoded(self.preparation))
        os.chmod(self.root / "doc-updates/candidate.md", 0o666)
        self.call("prepare", "--packet", "doc-updates/preparation.json", success=False)
        self.assert_unpublished()
        # Existing fixture lock must cause a different process to refuse without writes.
        before = self.record()
        result = subprocess.run([sys.executable, "-B", str(SCRIPT),
                                 "--root", str(self.root), "publish", "--change", self.change],
                                capture_output=True, timeout=10, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"Concurrent tool operation", result.stderr)
        self.assertEqual(self.record(), before)
        with self.assertRaises(control.Refusal):
            control.check_stat(type("Stat", (), {"st_uid": os.getuid() + 1, "st_mode": 0o100600})())

    def test_missing_resources_obligations_links_and_catalog_changes_fail_closed(self):
        for field, value in (("output", "doc-updates/missing.md"), ("obligations", ["Review obligation"]),
                             ("checks", "doc-updates/missing.md")):
            p = dict(self.preparation, **{field: value})
            self.write("doc-updates/preparation.json", control.encoded(p))
            self.call("prepare", "--packet", "doc-updates/preparation.json", success=False)
            self.assert_unpublished()
        self.write("doc-updates/preparation.json", control.encoded(self.preparation))
        self.write("doc-updates/output.md", b"[Outside](../../outside.md)\n")
        self.prepare_failure()
        self.write("doc-updates/output.md", b"# Safe output\n")
        self.write("doc-updates/catalog.md", self.store.read("doc-updates/catalog.md") + b"Unrelated change\n")
        self.prepare_failure()

    def prepare_failure(self):
        self.call("prepare", "--packet", "doc-updates/preparation.json", success=False)
        self.assertEqual(self.record()["stage"], "intake")
        self.assert_unpublished()

    def test_help_and_zero_args_are_safe(self):
        for args, expected in ((["--help"], 0), ([], 2)):
            r = subprocess.run([sys.executable, "-B", str(SCRIPT), *args],
                               capture_output=True, timeout=10, check=False)
            self.assertEqual(r.returncode, expected)
        self.assert_unpublished()

    def test_transition_table_matches_bundled_controller(self):
        procedure = (PROJECT / "references/local-lifecycle.md").read_text()
        for command, (before, after, role) in control.FORWARD.items():
            row = next(line for line in procedure.splitlines()
                       if line.startswith("| " + command + " |"))
            self.assertIn(before, row)
            self.assertIn(role + ":", row)
            self.assertIn("| " + after + " |", row)

    def test_prepare_requires_current_draft_registration(self):
        self.call("prepare", "--packet", "doc-updates/preparation.json", success=False)
        self.assertEqual(self.record()["stage"], "intake")
        self.assertIn("next: draft", self.record()["history"][-1]["reason"])
        self.register_draft()
        self.write("doc-updates/candidate.md", b"# Revised draft\n")
        self.call("prepare", "--packet", "doc-updates/preparation.json", success=False)
        self.assert_unpublished()
        self.prepare()
        self.assertEqual(self.record()["stage"], "prepared")

    def test_hold_blocks_draft_and_prepare(self):
        self.call("hold", "--note", "Missing actual authoring input")
        packet = {k: self.preparation[k] for k in
                  ("candidate", "purpose", "edition", "contract", "source_edition")}
        self.write("doc-updates/draft.json", control.encoded(packet))
        self.call("draft", "--packet", "doc-updates/draft.json", success=False)
        self.call("prepare", "--packet", "doc-updates/preparation.json", success=False)
        self.assertIsNone(control.latest(self.record(), "draft"))
        self.assert_unpublished()

    def legacy_without_draft(self):
        r = self.record()
        r["schema"] = 1
        r["history"] = [e for e in r["history"] if e["action"] != "draft"]
        for seq, e in enumerate(r["history"], 1):
            e["seq"] = seq
        control.validate(r)
        control.save(self.store, r, self.store.records())
        return r

    def test_new_history_cannot_remove_draft_and_legacy_approval_needs_rework(self):
        self.to_reviewed()
        self.decide()
        old = self.legacy_without_draft()
        strict = copy.deepcopy(old)
        strict["schema"] = 2
        with self.assertRaisesRegex(control.Refusal, "draft"):
            control.validate(strict)
        self.call("validate")  # Legacy history remains readable.
        self.call("publish", success=False)
        self.assertEqual(self.record()["stage"], "approved")
        self.assert_unpublished()
        self.call("rework", "--note", "Adopt mandatory draft gate without rewriting legacy events")
        self.to_reviewed()
        self.decide()
        self.call("publish")
        self.assertEqual(self.record()["stage"], "closed")
        self.assertEqual(self.record()["history"][:len(old["history"])], old["history"])

    def test_legacy_inflight_publication_recovers_under_original_approval(self):
        self.to_reviewed()
        self.decide()
        original_write = control.Store.write
        def fail_catalog(store, name, data, before):
            if name == "doc-operations/INDEX.md":
                raise OSError("Legacy interrupted publication")
            return original_write(store, name, data, before)
        with patch.object(control.Store, "write", fail_catalog):
            self.call("publish", success=False)
        self.legacy_without_draft()
        self.call("publish")
        self.assertEqual(self.record()["stage"], "closed")
        self.assertEqual(sum(e["action"] == "approve" for e in self.record()["history"]), 1)

    def test_legacy_prepared_review_and_approval_cannot_skip_draft(self):
        for stage, command in (("prepared", "open"), ("review", "review"),
                               ("reviewed", "approve")):
            case = ControlTests("test_help_and_zero_args_are_safe")
            case.setUp()
            try:
                case.prepare()
                if stage in ("review", "reviewed"):
                    case.call("open", "--evidence", "doc-updates/pr.md")
                if stage == "reviewed":
                    case.review()
                case.legacy_without_draft()
                error = case.call(command, "--evidence", "doc-updates/pr.md", success=False)
                self.assertIn("next: rework", error)
                self.assertEqual(case.record()["stage"], stage)
                case.assert_unpublished()
            finally:
                case.doCleanups()


if __name__ == "__main__":
    unittest.main()
