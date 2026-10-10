# Document revision, saving, and registration procedure

## Purpose and applicability

Local edition: 4; revises local edition 3.

Maintain an existing document when an authorized request, new evidence, or
observed discrepancy requires a revision. Also receive newly authored host
operational documents for saving and registration. This procedure has no
external client. Its authoring basis is `SOP@core` at
`$HOME/.agents/doc-specs/01-processes/sop--core.spec.md`.

The governing instructions are `$HOME/.agents/AGENTS.md`; the skill
entrypoint owns path resolution and responsibility boundaries. The recurring
workflow covers revisions, source preservation, affected references, and
required host registration. It does not create authoring contracts, manage
a specification-development board, publish operational guidance, or execute
documented operations. No alternative update method is designated.

## Roles and decision authority

The updating author establishes the current basis, coordinates authoring
support, applies authorized changes, and verifies the saved result. The
requesting user or agent resolves scope and evidence gaps within their actual
authority. `doc-specs` supplies contract selection, requested content, and
content checks; `doc-operations` supplies consultation for operational tasks.
An assigned reviewer or recipient participates only when established by the
task. Participation, authorship, and a catalog row grant no approval rights.

The governing instructions do not assign a maintenance owner for this
procedure or the host updates catalog. State that gap when an ownership
decision is needed; do not infer an account-owner mandate or a review
cadence. Existing authorization for bounded revisions and registration
remains usable without inventing an approving role.

## Inputs and readiness

Establish the requested change and outcome, subject and audience, actual
source and known edition, available evidence, authorized destination,
affected references, and current overlapping edits. For a new host-document
handoff, receive the prepared content, actual authoring basis, completed
checks, and unresolved obligations instead of inventing an earlier source.

Use `$HOME/.agents/skills/doc-specs/SKILL.md` for the current authoring
contract and its unresolved-input rules. Read
`$HOME/.agents/doc-updates/INDEX.md` for host registration. The index owns
catalog fields and preparation-state meanings; use its current guidance
rather than maintaining another schema in this procedure.

Confirm authorized read/write scope and resolved path containment. Inspect
existing content before overwriting or creating a candidate, and preserve
unrelated changes, native metadata, established identity, and history.
Use the task's existing recovery method when one is required. Missing
recovery readiness holds the affected replacement; it does not authorize a
new backup location, recursive permission changes, or a broad reset.

## Ordered workflow and handoffs

The updating author performs U1–U8; an assigned reviewer may perform U5.

| Step and entry | Action or decision | Output and next route |
|---|---|---|
| U1 — Authorized revision or new host-document handoff | Inspect the request, actual source or prepared content, discovery entry, supporting evidence, and overlapping edits. Classify by purpose and established context using the destination rules below. | Bounded change and destination to U2; material uncertainty to the requester. |
| U2 — Basis and scope established | Identify affected facts, edition and identity, incoming/outgoing references, consumer effects, and required recovery. Reuse an existing candidate covering the same source and requested change when compatible; inspect it before replacement. | Revision design and preservation requirements to U3; unresolved conflicts to the abnormal route. |
| U3 — Sufficient authorized inputs | Request selection, affected drafting, and contract-based review through `doc-specs`. Revise only the authorized content; retain unresolved facts as the actual contract permits. For a new handoff, use its prepared content and verify the supplied authoring basis. | Revised or received content and its actual checks to U4; missing dependencies hold affected content. |
| U4 — Content ready for placement | Reconcile links for the actual destination, preserving their meaning. Identify affected discovery entries and source/revision relationships. For host documents, prepare registration against the current updates index. | Coherent document and required catalog change to U5. |
| U5 — Reviewable change | Verify scope, source preservation, identity, editions, metadata, paths, references, content-check results, and any required recovery readiness. | Checked change to U6; defects return to U2–U4. |
| U6 — Checked change and current authority | Recheck the source, destination, and affected catalog basis for overlapping changes. With actual runtime permission, save only the bounded document change and required registration using the permitted edit mechanism. | Observed saved state to U7; changed basis or insufficient permission holds replacement. |
| U7 — Save attempted | Inspect actual document and catalog content. Verify required registration, link targets, retained editions, source integrity, and preservation of unrelated work. Resolve an interrupted or inconsistent save before dependent use. | Verified result or explicit incomplete handoff to U8; failures follow the abnormal route. |
| U8 — Results established | Report source and edition, actual authoring basis, changes, saved location, registration, checks, outcomes, and unresolved conditions in the session or established task record. | Completed authorized update or a named remaining dependency. |

### Destination and preservation rules

| Document purpose and current basis | Authorized update destination and preservation |
|---|---|
| Current host operational document in `doc-operations/` | Read the source without editing it or its index. Save the changed copy in `$HOME/.agents/doc-updates/` and register it in that directory's `INDEX.md`. Preserve source identity, known source edition, and a traceable source link. |
| Existing prepared host operational document in `doc-updates/` | Revise its authorized candidate and reconcile its actual catalog entry. Preserve the original operational source relationship; inspecting a candidate does not prove that its source remains current. |
| New host operational document received from `doc-specs` | Save and register it in `$HOME/.agents/doc-updates/`. Record its real creation basis and lack of an identified prior source using the index guidance. |
| Document about a specific project | Revise it in the authorized context of its owning project and reconcile existing project discovery/references when in scope. Running on the host does not create a host catalog obligation. |
| Explicitly requested native-artifact edit at its native destination | Classify by actual purpose and preserve the established native layout and explicit task destination. Use `doc-specs` for applicable authoring requirements and any uncovered-purpose/native-format route. Native format does not waive required host operational document saving and registration or canonical read-only boundaries. |
| Specification-library or operational-publication change | Outside ordinary updating. Identify the separate authorized maintenance or publication task; this procedure does not supply that workflow or mutate those read-only trees. |

When copying a document, reassess relative links from the copy's directory:
links that resolved in the source may point elsewhere in the candidate.
Verify targets in their authorized roots and use the installed layout in
guidance. Keep source links distinguishable from candidate links and
intended operational destinations. Do not invent a destination or source
edition to fill registration fields.

When the task is a partial revision, preserve unrelated content. If an
applicable contract exposes an unrelated defect outside scope, report its
effect on compliance rather than silently rewriting the whole document.
Avoid competing candidates; retain multiple editions only when established
by the request or existing practice, with their relationships explicit.

Saving the document and updating its required registration form one logical
change. Do not claim transactional atomicity from separate file writes.
If only one succeeds, report the actual partial state and follow recovery
before claiming completion. Use only indispensable temporary material in
the authorized context; no extra proposal trees, mirrors, publication
ledgers, or audit documents are required by this procedure.

## Holds and abnormal routes

| Condition | Containment and resumption basis |
|---|---|
| Source, destination, or required link is unavailable or escapes authorized roots | Hold dependent access or saving. Name the path, effect, and bounded correction or access decision needed. Resume after the target is verifiably usable. |
| Material facts, source edition, classification, or change scope are unclear | Keep the gap explicit. Hold only content or claims requiring that information; ask the requester for resolving evidence or a scope decision. An unknown edition need not block independent work when the contract and registration guide permit stating it. |
| Applicable authoring contract is unavailable, or no catalog type applies | Follow `doc-specs` dependency handling. An unavailable applicable contract holds dependent authoring; a readable catalog with no applicable type follows its uncovered-purpose route, without inventing compliance. |
| Source, candidate, or catalog changed since inspection | Stop affected replacement and compare actual changes. Preserve unrelated edits; resume after a reconciled basis or the requester's bounded conflict decision. |
| Document save succeeds but registration fails, or placement is interrupted | Inspect what changed before retrying. Mark the handoff incomplete. Reconcile the authorized document/catalog pair or use an established authorized recovery method; verify the result. Do not discard unrelated work. |
| Required check fails or content remains inconsistent | Return to the affected design, authoring, reference, or registration step. Avoid dependent use of known inconsistent guidance; record the failed check and actual correction or remaining gap. |
| Permission, extra scope, or required recovery is missing | Stop the affected mutation and report the specific missing authorization or resource. Do not seek privileged access or expand write roots as an automatic fallback. Root/sudo work remains human-executed under the host baseline. |
| Move, deletion, or publication is requested | Establish explicit authority and consumer/reference effects. Ordinary preparation authorizes none of these; route publication separately and preserve the read-only boundary here. |

Continue independent authorized work while a dependent route is held. A
registration state, completed check, silence, or intended destination cannot
release an authority hold.

## Completion, records, and maintenance

An existing-document update is complete when the bounded revision is saved
in its authorized context, unrelated work and required identity/history
are preserved, affected references are coherent, and required checks and
remaining gaps are reported. A host operational document additionally
requires verified saving in `$HOME/.agents/doc-updates/` and registration in
its `INDEX.md`. An incomplete save or registration remains a handoff gap.

Report the actual basis, applied specification ID and source or uncovered
native purpose, locations, changes, checks, outcomes, and unresolved
decisions. Use the host updates index for required registration and the
session or established task record for the completion account. Preserve
existing confidentiality and access constraints; no new retention period,
signoff, or separate log is implied. Do not present preparation as current
operational guidance, publication, approval, acceptance, or execution.

Review this procedure when governing responsibilities, installed layout,
authoring handoffs, registration guidance, or access boundaries change. An
authorized maintainer updates its affected resources and reports material
changes in the session or established change record. Maintenance ownership
remains unassigned until an actual decision establishes it.
