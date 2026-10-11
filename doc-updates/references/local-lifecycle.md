# Local operational-document lifecycle


Local edition: 2, replacing edition 1; retains mandatory draft registration
and adds classified operational placement. Authoring basis: `SOP@core` at
`$HOME/.agents/doc-specs/01-processes/sop--core.spec.md`. No external client.

This procedure belongs exclusively to `doc-updates` and governs every new or
revised host operational document or instruction intended for
`doc-consult/`. Read the skill entrypoint for authority and path scope.
Consultation, project deliverables, native instruction maintenance and
specification-library work retain their own scopes. Use
[the bundled controller](../scripts/doc-control.py) for transitions and
publication and [the CLI guide](LOCAL-REVIEW.md) for packets and recovery.
`doc-author` supplies authoring and contract checks within this workflow;
`doc-consult` supplies consultation. Neither owns PR gates.

A **local pull request** is an explicit local review request for one change
and immutable content snapshot, not a GitHub object. **Local merge/publication**
applies exactly the approved document and operational-catalog output, then
verifies it. No branches, GitHub, remote PRs, external service, or actual
`git merge` are required. Repository commit obligations are separate.

## Authoritative transition table

### Classification and intended placement

Classify the operational subject before selecting its destination. Reuse a
suitable existing classification or define a meaningful new immediate child
of `doc-consult/`; safe additional nesting beneath it is permitted.
Keep one canonical location and use operational-catalog guidance for
alternative names. Resolve material placement ambiguity before intake or
preparation rather than inventing a destination.

Keep directory classification separate from operational domains,
document family/contract, applicability, and component kind/provenance.
Domains may be multiple and extensible: governance, system, network, security,
runtimes, services, data, delivery, reliability, and additions such as tooling
or media. These are selection dimensions, not a closed directory taxonomy.
Consult the specification library's authoritative family registry through
`doc-specs`; its numbered family trees belong only to that library.

Ordinary destinations must be beneath a classification directory.
`doc-consult/INDEX.md` is the root catalog placement exception and remains
protected from ordinary destinations; update it only through the existing
separate proposed-catalog mechanism. Do not use `subjects/` or another
universal wrapper such as `topics/` or `components/`.

The controller checks path structure at new intake, draft registration,
preparation, and before new publication intent. Structural checks cannot prove
that a classification is meaningful: preparation and snapshot review assess
semantic placement, consistent candidate/intended destination, canonical
location, and destination-relative links. Use the existing purpose,
destination, checks, and review evidence; add no registry or publication layer.

Retained schemas and history use the existing safe path parser. Identical
intake retries and read-only inspection remain available for legacy paths.
New draft, preparation, and publication from `approved` reject retired flat
or wrapper destinations; remapping requires supersession and a classified
intake. Already `publishing` transactions may finish only their original
approved bytes under current original authority and all existing integrity,
containment, link, conflict, and symlink checks. Closed exact retries remain
no-ops. No installed document is migrated or deleted by this policy.

### Transition requirements

This is the single normative transition table; catalogs and the tool reference
it. Stages map to the operator's ordered sequence. Each failed action retains
the last confirmed stage and records a refusal/hold with the exact missing
prerequisite. Only the stated resumption condition permits retry.

| Action | Entry stage and prerequisites | Performing role and required action/evidence | Success stage | Failure route and exact resumption |
|---|---|---|---|---|
| intake | No record; actual authorized request, stable request key, bounded scope, explicit destination, source edition/digest or confirmed new subject | author: register before drafting; assign unique ID, record request basis and actual author; legacy gaps explicitly unconfirmed | intake | Hold intake; supply missing real basis/scope/source, or reuse compatible existing ID; never create a competing master. |
| draft | intake; actual saved candidate and selected authoring basis | author: register existing candidate and all seven fields with observed draft digest; no review snapshot or release claim | intake | Remain intake; restore named candidate/basis. Even a ready candidate requires draft registration before prepare. |
| prepare | intake; current draft registration and matching candidate/basis, coherent seven-field registration, performed content checks, no unresolved mandatory obligation | author: fix publication bytes and catalog diff, identify source/destination baselines and new edition; snapshot all publishable content and evidence | prepared | Remain intake; resolve the named obligation/resource, recheck affected content, then prepare. Drafting remains within intake. |
| open | prepared; unchanged snapshot and baselines, explicit review-request evidence | author: open local PR bound to exact candidate, source basis, publication mapping and catalog output | review | Remain prepared; supply review request or rework stale inputs and prepare again. |
| review | review; unchanged snapshot; applicable automatic checks passed; findings with dispositions, every blocker resolved | reviewer: agent reviews exact publication diff and contract obligations; record snapshot-bound report and checks actually performed | reviewed | Remain review; resolve every blocker and rerun affected checks/report; content changes require rework. |
| approve | reviewed; unchanged successfully reviewed snapshot; requesting operator actually decides | operator: inspect exact output/diffs; explicitly approve snapshot and decision scope, capture provenance; identify whether decision also grants target publication authority | approved | Remain reviewed; obtain explicit operator decision on this snapshot; candidate text, approver fields and validator success never suffice. |
| publish | approved; unchanged review/approval, explicit current target authority, runtime permission, successful prepublication checks, recorded recovery baselines | publisher: revalidate immediately before writes, durably record intent before applying exactly approved document/catalog bytes | publishing | Retain approved before intent or publishing after intent; resolve authority/permission, inspect actual partial outputs; never blindly replay. |
| close | publishing; actual document/catalog equal approved output, valid links/editions, registration/history reconciled | publisher: verify bytes, record observed result and reconcile updates navigation; report actual outcome | closed | Retain publishing or closed if closure record succeeded but navigation failed; inspect actual bytes and reconcile under original approval only if unchanged. |
| rework | intake, prepared, review, reviewed or approved; explicit reason or detected stale content/basis | author: record invalidation; preserve earlier checks/review/decisions in history, update basis explicitly | intake | No publication; prepare new snapshot, repeat open/review/approval. Mapping changes require a separately scoped superseding intake. |
| reject / withdraw / supersede | intake, prepared, review, reviewed or approved; explicit operator decision and reason; supersession identifies existing replacement change ID in reason | operator: capture actual decision on current snapshot/ID, retain candidate/source | rejected / withdrawn / superseded | Hold last stage until decision exists; never delete content or bypass gates. |
| reopen | rejected, withdrawn or superseded; explicit operator reopening decision and resolving basis | operator: retain prior evidence and reset affected gates; refuse competing active destination | intake | Resolve competing request or missing reopening evidence, then prepare/open/review/approve anew. |
| hold / release | any registered stage; hold names exact prerequisite; release records its observed resolution | author: keep lifecycle stage, record reason/resumption evidence; active hold blocks forward work | same stage | Hold only dependent work; release only when stated prerequisite is observably satisfied. |
| refuse / correct / reconcile | any registered stage; safely valid history; correction names original event and actual correction; reconciliation inspects actual record/index | author: append refusal or corrective/reconciliation event, regenerate navigation from records without changing approved bytes | same stage | If history/schema invalid, fail closed and report refusal could not be durably recorded; obtain bounded repair authority without rewriting past events. |

Preparation states (`draft`, `prepared`, `blocked`, `superseded`, `withdrawn`,
`unconfirmed`) are descriptive and separate from lifecycle stage. A temporary
hold never advances or erases that stage. Rejection is a lifecycle disposition,
not publication. Closed work is terminal; a new edition or reversal requires
a separately recorded controlled change through all gates.

## Records, validity and notifications

New records use schema 2, which verifies draft-before-prepare during history
replay. Schema 1 records remain readable without rewriting past events.
Unpublished schema 1 approvals lacking matching draft evidence require
`rework → draft → prepare → open → review → approve` before new publication.
Already publishing schema 1 changes may finish exactly the original approved
outputs under their original current authority; closed retries remain read-only.
The same mandatory draft gate applies to new preparation on either schema.

`doc-updates/changes/<change-id>.json` is the only authoritative control record
for each change. Register intake immediately. The updates index is human
navigation, including pending requests with no fictitious candidate entry.
Once a candidate is saved, registration retains all seven fields and links to the
record. Preserve the same ID across retries, sessions, decisions and recovery.
History captures actual UTC timestamps, ordered sequences, actor/role,
predecessor/result stage, action/outcome, evidence and hold/refusal reason.
Record actual source edition/digest or explicit absence, candidate/destination,
checks/findings, actual roles, decision scope/provenance, authority, intent and
observed publication. Correct mistakes with events; never invent legacy
timestamps, checks, reviews or approvals.

SHA-256 identities cover candidate bytes, exact final publication bytes
(including converted relative links), source and catalog baselines, edition,
mapping, actual specification catalog/selected contract, basis and check digests. Mutable history metadata is excluded to
avoid self-reference. Changes invalidate affected evidence; state-changing
actions detecting stale reviewed inputs record rework and require a new
snapshot and all gates. Read-only validation reports staleness without changing
approval. Earlier evidence remains history; labels/filenames are not identity.

The supported approval channel is an operator-performed terminal action with
an exact snapshot response. Agents must not impersonate the operator or run
that action themselves. Approval and target write authorization are distinct;
the same explicit decision can grant both for the exact scope. Use existing
applicable authorization; never demand redundant permission. If previously
approved scope lacks authority, rework/review and capture the correctly scoped
decision. Local account identifiers and free-text evidence are not independent
authentication; hashes/history are not tamper-proof audit evidence.

Before continuing dependent work after any attempted jump, notify the operator
in their language: attempted action, missing prerequisite, retained stage and
next permitted action. Record the refusal where safe. Never use urgency,
silence, initial authoring authorization, validator success or a commit as
approval. Policy amendments need separately scoped maintenance, not a bypass.

## Enforcement, recovery and adoption

The supported tool rejects invalid transitions and gates its own publication
operation. Agents must use it. Direct edits remain possible for actors with
sufficient filesystem access; no unconditional enforcement or authenticated
human audit is claimed. No host permission controls are installed here.
No tool operation executes tasks described by documents.

Publication uses a root lock, no-follow paths, account ownership checks and
private atomic replacements, but two output writes and record/index writes
are not globally atomic. Intent retains original bytes for recovery, not
authorization to roll back. On interruption inspect actual outputs: each
must be original baseline or approved output. Retry publication only with
unchanged candidate/review, current authority and permission; it may complete
the missing approved write and reconciliation. Other bytes indicate competing
edits: preserve them, hold and resolve explicitly. Never reset modified sources.
An already closed exact result is a no-op; index interruption uses `reconcile`.
Changing output to recover requires renewed review/approval. Withdrawal and
supersession never authorize deletion; reversal is a new controlled change.

Adoption is separately authorized. Manual delivery supports a new target only;
existing catalogs, candidates and histories require separately scoped maintenance.
The retired installer supplies no current deployment recovery. Delivery does
not activate host instructions. Follow the
migration steps in the tool guide: preserve legacy source/state, record present
intake with explicit lifecycle gaps, add navigation markers only under scoped
catalog maintenance, and complete missing gates before future publication.
Installation does not retroactively review or approve documents. Maintenance
ownership remains unassigned; establish it when needed and revise this skill's table,
tool, tests and doc-control delivery inventory together when requirements change.
