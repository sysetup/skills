# Host documentation updates index and registration guide

## Purpose, authority, and scope

This index registers new and revised operational documents prepared for the adopting account's host (`$HOSTNAME`). It helps users and agents locate those documents, identify their source and authoring basis, and distinguish preparation from actual publication. It has no external client.

The governing instructions are in `$HOME/.agents/AGENTS.md`. They require documents created for host operation to be saved in `$HOME/.agents/doc-updates/` and registered in this index. Current operational guidance remains in the read-only `$HOME/.agents/doc-operations/` directory, accessed through its [operational index](../doc-operations/INDEX.md).

This index provides navigation and registration guidance. Its own recommendations are nonbinding; obligations attributed to the governing instructions retain their authority. Registration, a completed document, or a successful check does not establish approval, acceptance, publication, or authority to execute the documented operations.

The installed location is `$HOME/.agents/doc-updates/INDEX.md`. Links to working documents are relative to its containing directory, `$HOME/.agents/doc-updates/`. Links to specifications and operational sources use the sibling directory layout. Resolve these links within `$HOME/.agents/`; the same relative layout supports checks from a development workspace without treating its location as a host installation path.

Project-specific documents belong in the paths corresponding to their project's work context. This catalog covers host operational documents, not project deliverables, proposed specification changes, or a general action backlog. Specifications remain read-only authoring contracts; this directory is not their development board. This index is the catalog itself and is not registered as an operational document in its own table.

## Document catalog

No host operational documents are currently registered. This synthetic fixture starts with only this index. Replace this statement when the first in-scope document is saved and registered; do not add sample rows or entries for documents that do not exist.

| Document | Purpose and applicability | Local edition | Authoring contract | Source or change basis | Operational destination | Document state and evidence |
|---|---|---|---|---|---|---|

For each new or revised host operational document, the catalog should provide:

- **Document:** A descriptive title linked to the existing working document using a relative path within `$HOME/.agents/doc-updates/`. Preserve its established document identifier, if any, across revisions. A proposal without a document is not a catalog entry.
- **Purpose and applicability:** The task or process covered, the host component concerned, and material scope or version limits. For a revision, identify the intended improvement without asserting that it has already changed the host.
- **Local edition:** The document's established revision, version, or dated edition. If none is established, say `unspecified`; do not derive an edition from a tool version or filesystem timestamp. Keep simultaneously retained revisions distinguishable.
- **Authoring contract:** The selected specification identity and a relative link to its actual contract under `$HOME/.agents/doc-specs/`. If the catalog has no applicable type, state the uncovered purpose and the governing native conventions; do not claim compliance with an unrelated contract. If an applicable contract is unavailable, record that dependency explicitly.
- **Source or change basis:** The real request, observation, or other evidence motivating the document. For a revision, link the existing operational source and identify the source edition used, or state the edition gap. For a new subject, state that no prior operational document was identified. Do not invent a source record or identifier.
- **Operational destination:** The intended path under `$HOME/.agents/doc-operations/`, when established, labeled as intended until actual publication occurs. Otherwise say `unresolved` and identify the placement decision needed. A destination is not permission to write there.
- **Document state and evidence:** The supported preparation state and the checks or decisions that actually exist. Record the responsible author or maintainer only when assigned; otherwise state the assignment gap. Include an actual publication locator and edition only after publication is verified. Keep proposed checks and pending decisions distinct from completed ones.

These fields help readers locate and assess the prepared documents; their detailed content and evidence remain in the linked documents or actual supporting records. Use concise cell text and existing references rather than duplicating operational instructions or creating a separate ledger.

## Registration and revision guidance

Document authoring follows the applicable contracts selected from the [specification index](../doc-specs/INDEX.md), using `$HOME/.agents/skills/doc-specs/SKILL.md`. Specifications define content obligations, not host facts. Documentation creation, consultation, and updating retain their respective workflow responsibilities; this index does not reproduce or replace skill procedures.

For a new host operational document, save the document in `$HOME/.agents/doc-updates/` and register its actual location and supported facts here, as required by the governing instructions. Reuse an existing document covering the same subject when appropriate to avoid competing guidance.

For a revision, consult the current operational source without editing `$HOME/.agents/doc-operations/`. Prepare the changed copy in `$HOME/.agents/doc-updates/`, preserving the source identity, source edition where known, and a clear distinction between the current source and the prepared revision. This allows review of what changed without presenting the candidate as the current operational edition.

Registration should accompany saving or revising a document. Update the catalog when its location, edition, applicability, destination, or supported state changes. Unknown assignments, editions, destinations, or decisions should remain explicit, with their consequence and resolving action. Do not invent owners, priorities, dates, approvals, or evidence to fill a row.

## Preparation state and publication boundary

Use a preparation state only when supported:

- **`draft`:** The document exists and is still being authored or revised.
- **`prepared`:** The author reports the requested content complete. Identify checks actually performed and any unresolved review or decision; preparation alone does not establish approval or publication.
- **`blocked`:** Further document work depends on an unmet input, unavailable contract, unresolved decision, or other named condition. State the condition, its effect, and the resolving action or assigned role; do not assume that a person is the blocker.
- **`superseded`:** Another identified prepared revision replaces this one. Link the replacement and retain the real relationship; this does not mean the operational source has been replaced.
- **`withdrawn`:** Further work on this candidate has been stopped by an actual decision. Identify that decision and its reason; withdrawal does not authorize deletion.

If the preparation state cannot be established, say `unconfirmed` and identify the missing evidence. Record actual review, approval, acceptance, and publication decisions separately from preparation state; one does not imply another.

Publication is not an automatic move after preparation. `$HOME/.agents/doc-operations/` remains read-only during ordinary host operation. A change to its documents or catalog requires actual authorization for that scope and runtime write permission. This index supplies neither and does not prescribe a separate publication workflow.

When separately authorized publication has actually occurred, reconcile the record with the verified operational location, edition, decision or authorization basis, and applicable entry in the operational catalog. If a working copy is retained, keep its link and identify its relationship to the published edition. If it is no longer present, replace the working link with the verified published locator and label the entry as retained publication history. Do not leave a broken working link, invent publication evidence, or treat an intended destination as an existing file.

Documents in this directory are available for authoring, review, and traceability. Their presence or registration does not make them current host operational guidance; consult `$HOME/.agents/doc-operations/INDEX.md` for that purpose.

## Maintenance and checks

This registration guide uses [Engineering guide (`GUIDE@core`)](../doc-specs/00-governance/guide--core.spec.md) as its authoring basis while retaining the catalog's native index format. It is not an action item register or a configuration item register.

The governing instructions do not assign an index maintainer. Ownership remains unresolved; establish that assignment when authorizing maintenance rather than inferring it from authorship. This gap prevents reliance on an assigned review cadence; document authors can still register their authorized work.

Review the index when a document is created, revised, relocated, superseded, withdrawn, or actually published, and when governing paths or responsibilities change. Check that document and specification links resolve to their stated targets, retained editions are distinguishable, source references remain traceable, and recorded decisions match real evidence. A missing or inconsistent link should be reported with its affected entry and resolving action rather than silently repaired by inventing a destination.

Make material changes visible in the relevant catalog fields and the authorized session's completion report. Keep the empty-catalog statement consistent with actual registered content. No additional log, backup tree, or publication ledger is required by this index.
