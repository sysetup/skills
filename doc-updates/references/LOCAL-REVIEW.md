# Local documentation review product guide

Guide revision 2; local lifecycle edition 1; new control-record schema 2
(reads retained schema 1). For authorized
account operators and agents on Debian/Linux with Python 3.11+ and `fcntl`.
No external client. Basis: `PRODUCT-GUIDE@core` in the separate specification
library. This guide documents [doc-control.py](../scripts/doc-control.py); normative gates
are in [this skill's transition table](local-lifecycle.md#authoritative-transition-table).
No alternative publication method is designated.

## Installation and safety contract

The doc-manager installer acquires this skill from its pinned remote repository
and delivers its script, lifecycle procedure and this guide within
`skills/doc-updates/` at the chosen documentation root. It does not activate host instructions, migrate
live records or grant write authority. Manually integrate `dev-AGENTS.md` into
the complete baseline only with separate authority. Keep installed guidance
under `$HOME/.agents/`; never infer production targets from development.

Use Python explicitly; no executable-bit change, Git, GitHub, database,
network or dependency is required by the local review workflow. Every command
selects an explicit authorized root. Root/descendants/files must be owned by
the invoking account and not group/other writable. Ancestors must be directories
without shared write permissions unless sticky (such as `/tmp`). Symlinks at
any accessed component fail closed. Records are private (0600), new directories
0700, output replacements 0600. Account-owned hard-linked input files are
accepted (including installer staging links); replacement never edits their
inode in place. An advisory root-directory lock serializes cooperating tool
and installer operations; a competing lock fails immediately. Direct writers
outside the lock remain outside this enforcement boundary.

Paths are root-relative ASCII components using letters/digits/dot/underscore/
hyphen. Traversal and `.git` are forbidden. Maximum 1,000 changes per root,
8 MiB per file/record; exhausted limits hold for separately scoped maintenance.
The workflow publishes one document and its catalog row per change; multiple
documents use separate changes and cross-links assessed by review.

```bash
python3 -B "$HOME/.agents/skills/doc-updates/scripts/doc-control.py" --help
python3 -B "$HOME/.agents/skills/doc-updates/scripts/doc-control.py" --root "$HOME/.agents" status --change CHANGE_ID
```

Zero arguments exit 2 with usage and no writes. Success exits 0; refusals,
input and filesystem failures exit 2. There are no force/skip/auto-approve
commands. Messages are English; agents notify the operator in the session's
language before dependent work continues.

## Intake before authoring

Write an authorized intake packet in `doc-updates/` with exactly these fields:

| Field | Meaning |
|---|---|
| `key` | Stable unique request reference, retained on retries. |
| `basis` | Actual authorized request/evidence reference; no fabricated authority. |
| `scope` | Bounded content change. |
| `destination` | Exact document path under `doc-operations/`, excluding `INDEX.md`; mapping changes use supersession/new intake. |
| `source_edition` | Known current edition or `unspecified`; for confirmed new subject, `absent (new subject)`. |
| `author` | Actually established role identifier, avoiding unnecessary personal data. |
| `legacy` | Boolean; true denotes legacy work with missing lifecycle evidence. |

Use `intake --packet doc-updates/request.json`. It captures observed source
SHA-256 (or null for absence), assigns a random 128-bit ID, records actual UTC
time and immediately indexes the pending request. No candidate is needed or
fictitiously indexed. Identical key/packet retries return the existing ID;
incompatible reuse is refused. An active request for the same destination
requires reuse or explicit supersession.

## Preparation and local PR

`doc-updates` registers intake before requesting drafting through `doc-specs`,
then owns saving, draft registration, preparation and the remaining PR gates.
Select/read the actual contract or record the readable catalog's uncovered
purpose. Record performed checks, obligations, source edition and reference
conversions honestly. Authoring handoffs grant no release authority.

Immediately after saving any candidate, including ready content, use `draft --change ID
--packet doc-updates/draft.json`. Its packet has exactly `candidate`, `purpose`,
`edition`, `contract`, `source_edition` with the meanings below. It registers
all seven candidate fields at intake without claiming preparation/review.
The event records the observed draft digest; unchanged retries are no-ops.
Draft registration is mandatory. If candidate bytes or registration fields
change, rerun draft at intake before preparation.

Write a preparation packet with exactly these fields:

| Field | Meaning |
|---|---|
| `candidate` | Existing candidate path under `doc-updates/`. |
| `output` | Existing UTF-8 final publication file under `doc-updates/`; may equal candidate if its bytes already suit the destination. Convert links before review. |
| `catalog` | Existing UTF-8 proposed complete operational `INDEX.md` bytes under `doc-updates/`. |
| `edition`, `source_edition` | Explicit proposed published and observed source editions; unknown is `unspecified`, absence uses the intake literal. |
| `purpose`, `contract` | Purpose/applicability; contract identity plus Markdown link to `../doc-specs/...spec.md`, or literal prefix `uncovered purpose:` followed by native basis. |
| `checks`, `basis` | Nonempty local evidence files under `doc-updates/`: performed checks/results and selected authoring/source basis. |
| `obligations` | List of unresolved mandatory obligations; must be empty. |

Use `prepare --change ID --packet doc-updates/preparation.json` only after
matching draft registration. It fixes
candidate digest, final output bytes, full catalog before/after bytes, source
before bytes/absence, edition, mapping and evidence digests. The snapshot ID
is SHA-256 of canonical JSON for those fields, excluding its own ID and mutable
history. Snapshots are retained inside prepare events, avoiding duplicate
snapshot trees. Recorded baselines provide recovery readiness, not rollback
authority. The source edition remains explicit rather than inferred from time.

The catalog change must add/replace exactly one four-field row linking the
destination and edition, remove the original empty-coverage statement when
appropriate and preserve all other bytes. Do not add unrelated blank lines.
Inline Markdown links/images in final output/catalog must resolve inside the
root or use HTTP(S), mailto or fragments. The tool does not validate reference
links, HTML, anchors, substantive accuracy or contract completeness; review
must cover them. It executes no content-embedded check commands. Check reports
are agent assertions plus actual structural/path/digest validation, not
independent certification.

`show --change ID` displays exact document/catalog diffs and snapshot ID.
`open --change ID --evidence doc-updates/pr.md` opens the local PR with explicit
nonempty review-request evidence bound to that snapshot. Preparation never
opens a PR automatically.

## Agent review and operator decision

The reviewer may be the author; this is not independent human review. Inspect
the exact snapshot, request, source, publication diff, editions, links,
contract obligations, checks and recovery. Write a JSON review report with
exactly `snapshot` (ID), `checks_passed` (true only for passed checks), and
`findings` (list). Each finding has exactly `finding` (text), `blocking`
(boolean) and `disposition` (`resolved`, `accepted`, `open`). Blocking findings
must be `resolved`; accepted blockers cannot pass.

Use `review --change ID --evidence doc-updates/review.json`. Failure retains
review stage and refusal history. Content fixes require rework and a new
prepare/open/review sequence. The actual specification index and selected
contract (when covered) are digest-bound authoring sources. Current
basis/check/review evidence files must
retain their snapshot-bound digests; editing a completed report makes it stale.

The **operator**, never the agent, runs from a terminal after inspecting `show`:

```bash
python3 -B "$HOME/.agents/skills/doc-updates/scripts/doc-control.py" --root "$HOME/.agents" approve --change CHANGE_ID
```

Terminal stdin/stdout and exact response `approve SNAPSHOT_ID` are required.
A second distinct response `authorize SNAPSHOT_ID` grants writes to the
displayed document and operational catalog. Leaving it empty records approval
without authority; publication then fails closed. If authority is missing,
rework/review and capture the correctly scoped decision. Existing applicable
authority covering both needs no redundant approval. Authority must still
apply at execution; record a hold if revoked or in doubt. Filesystem permissions
independently determine runtime write access.

The event captures decision, snapshot, scope, channel and local account UID.
No imported approver field, candidate decision or piped approval passes the
supported CLI. Terminal possession is not authenticated human identity.
Agents must not impersonate the operator through a terminal. Actors with file
access can forge records or bypass the tool; hashes/history are neither
independently authenticated nor tamper-proof. Mandatory instructions and
supported gates are not host access controls; none are configured here.

## Publication and recovery

`publish --change ID` calls the same gate internally, validates current
schema/history/content/authority, records intent before writes and rechecks
conflicts immediately before each write. Private same-directory temporary
files, fsync and atomic replacement/exclusive creation apply exactly approved
document/catalog bytes. There is no multi-file atomicity. After observing
matching bytes, valid links and catalog edition, it records closure and
regenerates updates navigation. It never executes documented operational tasks.
Printed `closed` reports observed result; the agent reports location, edition
and checks in the session.

On interruption inspect `status`/`validate`. At `publishing`, each output
must equal its original or approved bytes. Partial work remains incomplete.
With current original authority and runtime permission, retry `publish` to
finish only missing approved writes and reconciliation. Exact completed retries
create no event or write. Other bytes indicate competing changes: preserve
them, hold and resolve explicitly. Never reset a modified source.

Index/history mismatch requires `reconcile --change ID --note REASON` after
actual inspection. It appends reconciliation evidence and derives navigation
without changing output/approval. It also recovers closure-record success
followed by index-write failure. If refusal cannot be recorded, the diagnostic
states that limitation; preserve actual partial state.

An abruptly killed atomic writer can leave `.doc-control-<random-id>` staging
files. Private regular staging files in `changes/` are validated for ownership
and preserved, never treated as masters; retry uses canonical records and
actual output bytes. Inspect retained staging before separately authorized
cleanup. Malformed schema/history cannot be automatically repaired. Obtain separately
scoped maintenance, retain damaged evidence and append a corrective event
when valid history can again be established. Never silently rewrite valid
historical events. No command rolls back operational files. Changing approved
output during recovery requires renewed review/approval; reversing a published
edition requires new intake through all gates.

## Holds and terminal routes

`status`, `validate`, `show` are read-only, including stale detection; they
never publish/change approval. Mutations validate history/navigation first.
Safely recordable failures append `refuse` with action, reason, retained stage
and next permitted action. Stale reviewed inputs detected by a mutation
explicitly invalidate checks/review/approval and return active work to intake;
earlier evidence stays in history. Invalid history may prevent refusal recording.
The agent must notify missing prerequisites before dependent work. Urgency,
silence, broad authoring permission and commits never supply approval.

Use `rework --change ID --note REASON --evidence REFERENCE` for unpublished
rework, updating source/basis/checks explicitly before repeating all gates.
`hold` records an exact prerequisite; `release` records observed resolution
through note/evidence. Stage remains fixed and active holds block forward work.
`correct` names original event/error and actual corrected fact; it annotates
history without silently changing output/approval. `reconcile` derives only
navigation. These commands do not substantively certify free-text evidence.

`reject`, `withdraw`, `supersede`, `reopen` are operator terminal commands
with `--change ID --note REASON`. Exact command + snapshot/ID responses are
required. Supersession names an existing replacement change ID in the reason. They retain
content/history, authorize no deletion, and cannot shortcut publication.
Reopening returns to intake and refuses competing active destinations; all
gates must pass again. Closed changes cannot reopen/rework.

## Record contract and migration

`doc-updates/changes/<id>.json` contains exactly `schema`, `id`, `request`,
`stage`, `history`. Request is the intake fields plus observed `source_hash`.
Events contain exactly `seq`, `utc`, `role`, `actor`, `from`, `to`, `action`,
`outcome`, `evidence`, `reason`, `data`. Action-specific data is strictly
validated/replayed. Unknown fields/states, duplicate JSON keys, invalid UTC
times, nonchronological order, skipped predecessors and stale identities fail
closed. Roles/evidence remain relevant, local and non-sensitive. Current stage
must equal history replay; holds/refusals/rework retain explicit reasons.

One `doc-control:start` / `doc-control:end` marker pair bounds generated
index navigation. Outside legacy content is preserved. Navigation must equal
records before further transitions; `reconcile` is the recovery exception.
Pending intake requests have no fictitious document row. Prepared candidates
retain the seven existing fields and record link; candidate files remain
retained after publication. No competing ledger/database/board exists.

For legacy installations, with **separately scoped maintenance authority**:

1. Inspect the installed procedure/fragment/catalogs and skill against
   doc-manager procedure revision 3 and this skill's lifecycle edition 1.
   Differing managed files are refused by the installer; preserve sources and
   receipts, reconcile changed managed files explicitly, then rerun the reviewed
   installer. Never reset live catalogs or histories.
2. Add the empty generated section from the shipped updates template exactly
   once, preserving existing rows. Template deployment preserves populated
   live catalogs rather than overwriting them.
3. Register authorized legacy changes at present actual intake time using
   `legacy: true`, actual source edition/digest and explicit lifecycle gaps.
   Preserve original preparation state/source links in legacy rows and link
   the new record. Never backfill review, approval, checks or timestamps.
4. Reconcile duplicate legacy navigation into one controlled seven-field
   candidate entry only after actual preparation. Retain historical facts in
   its record/legacy note; complete missing gates before future publication.
   Installed guidance is not retroactively reviewed/approved.
5. Preserve retained schema 1 records. Before new publication lacking draft
   evidence, rework and repeat draft, preparation, review and operator approval.
   Finish already publishing outputs only under the original current approval;
   inspect partial outputs before any retry. Root-level legacy controller/guide
   files are not installed or removed by the new installer. Stop using them
   after activation; archive or remove them only under scoped maintenance.
6. Manually integrate the activation fragment into the complete baseline with
   authority. Installation, preparation and receipts approve no real candidate.

No live migration/adoption occurs in development tests. Maintainer, retention
interval and cadence remain unassigned until authorized. Review this skill's table,
tool, tests, guide and doc-manager installer inventory together on schema/policy changes.
Preserve dependency pins/licenses; report actual upstream conflicts rather
than inventing overrides or editing installed skills.
