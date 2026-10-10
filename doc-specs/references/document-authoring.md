# Document specification selection, authoring, and review procedure

## Purpose and applicability

Produce evidence-based host or project documents from the current canonical
specifications. This procedure covers new-document authoring and the
selection, drafting, and review support requested by a document-update
workflow. It has no external client. Its authoring basis is `SOP@core` at
`$HOME/.agents/doc-specs/01-processes/sop--core.spec.md`.

The governing instructions are `$HOME/.agents/AGENTS.md`; the skill entrypoint
owns path resolution and workflow boundaries. This procedure does not
execute documented tasks, maintain the specification library, consume host
runbooks for operational readiness, manage revisions, register documents, or
publish them. No alternative authoring method is designated for a covered
document type. An uncovered type follows the explicit abnormal route below.

## Roles and decision authority

The author selects contracts, uses authorized evidence, drafts, and checks
the document. The requesting user or agent supplies the purpose and resolves
material scope or input questions within their actual authority. A reviewer
or receiving role participates only when assigned; authorship or review does
not establish approval authority.

`doc-updates` owns maintenance and the entire host operational-document PR
lifecycle. Obtain its real intake before drafting host guidance. The procedure's maintenance owner is not assigned by the
governing instructions. Record that gap when ownership matters; assignment
requires an actual decision, not an inferred account-owner mandate.

## Inputs and readiness

Establish the requested deliverable, reader, supported decision or action,
subject, scope, existing source if revising, authorized evidence, and intended
destination. Read the current `$HOME/.agents/doc-specs/INDEX.md` and the full
selected contract. Use authorized read access and only the tools necessary
for the requested document; no renderer, generator, dependency installation,
mode setting, or skill-loading evidence is an implicit prerequisite.

Read additional authoring sources when the catalog or selected contract
requires them. Evidence gathering follows the task's actual access limits.
Bundle only questions whose answers materially change selection, factual
correctness, required content, or delivery. Independent drafting can continue
when the contract permits unresolved facts to remain explicit.

## Ordered authoring workflow

The author performs A1–A5; an assigned reviewer may perform A4. A6 hands off
to the actual recipient without executing the documented operation.

| Step and entry | Action or decision | Output and next route |
|---|---|---|
| A1 — Document request or authoring-support request | Establish purpose, audience, subject, boundaries, and destination from the request and authorized sources. If adequate coverage already exists, reuse it; route changes to `doc-updates` and provide only requested authoring support. | Host operational scope to doc-updates intake before A3; contract selection to A2; unresolved material classification questions to the requester. |
| A2 — Scope established | Select and read the contract using the selection rules below. | Contract identity and applicable obligations to A3; unavailable inputs or uncovered types to the abnormal routes. |
| A3 — Contract and sufficient inputs available | Draft the requested content using the authoring rules below; expose gaps as the contract requires. | Document and factual basis to A4. |
| A4 — Draft or content supplied by `doc-updates` | Apply the review rules below. Return defects to A2 for selection errors or A3 for content errors. | Checked content, actual results, and remaining gaps to A5. |
| A5 — Checks recorded | Identify the applied specification ID and actual source, authorized destination, and any unresolved mandatory obligation. Do not claim full compliance while one remains. | Document and honest completion account to A6. |
| A6 — Authoring support ready | Deliver a project document in its authorized context, or return host content and its basis to the owning `doc-updates` request for mandatory draft registration and the remaining PR gates. Return revision support to the requesting update workflow. | Authoring handoff complete; host-document delivery remains pending until saving and registration are confirmed, or their blocker is reported. |

### Selection rules

Select by the catalog's purpose and use boundary, not by a filename, acronym,
directory, or presentation format. Prefer the applicable specialized variant
when its conditions hold; establish facts that distinguish variants rather
than choosing a generic contract that excludes the subject. Select each
authorized deliverable independently and reconsider when its purpose changes.

Follow the actual catalog link using the entrypoint's path rules. Read the
entire linked `*.spec.md`, confirm its Specification ID and selection boundary,
and derive required inputs and content from it. A row or filename alone
cannot supply the finished-document contract. Do not copy a fixed catalog
inventory into this skill; it would become a competing selection source.

Consult `$HOME/.agents/doc-specs/authoring/families.json` for the library's
authoritative family responsibilities. Its `00-governance` through
`05-evidence` directories organize specifications; do not reproduce those
family trees beneath operational components. Select an operational
classification before its intended destination using
[doc-updates' placement contract](../../doc-updates/references/local-lifecycle.md#classification-and-intended-placement).
Return that coherent destination and unresolved placement questions with
the authoring handoff. Family/contract selection remains independent of
directory placement; a specification-library incompatibility holds only
dependent authoring and is reported without modifying that library.

### Authoring rules

Apply the contract's finished-document obligations, content definitions,
forms, and quality criteria to established subject-specific facts. Preserve
required, conditional, optional, and normative distinctions. For unresolved
conditions, use the contract's treatment of uncertainty; do not silently
drop conditional content whose applicability is unknown.

Identify unknown or conflicting facts, their effect, the resolving action,
and an assigned owner only when known. Never invent commands, editions,
dates, owners, references, signatures, approvals, or results. A specification
supplies content obligations, not project facts or execution permission.

Use the selected contract's structure and metadata rules. The library's
common conventions are in `$HOME/.agents/doc-specs/README.md`; consult them
when their terminology needs clarification. Do not transplant specification
instructions, empty template sections, or generic control blocks into the
finished document. Referenced companion documents are not automatic extra
deliverables.

Preserve native format authority. When a requested native artifact has no
applicable catalog type, identify that uncovered scope and apply its actual
native requirements. When an applicable contract conflicts with an explicit
native requirement, report the specific conflict and follow governing
instructions; do not silently claim both contracts are satisfied.

### Review rules

Check selection, evidence, required inputs, applicable content obligations,
reader tasks, structure, metadata, uncertainty treatment, and real reference
targets against the full selected contract. For an authorized document set,
also check consistency and traceability between its members. Use available,
applicable, authorized checks; name what was inspected or run.

Keep evidence, inference, and recommendations distinct. Separate planned
actions from observations, and technical checks from usability, operational
execution, approval, acceptance, publication, or certification. A structural
check does not establish those other outcomes.

## Holds and abnormal routes

| Condition | Author's response and resumption basis |
|---|---|
| Catalog or selected applicable contract is missing, empty, inaccessible, inconsistent, or outside its allowed root | Stop dependent authoring. Name the actual entry or path, failed dependency, and bounded access or correction needed. Resume after the input is observably available and usable. Do not substitute another library or create a replacement contract. |
| Readable catalog has no applicable type | Report the uncovered purpose. Apply explicit task requirements and compatible native or project conventions without claiming specification compliance. Do not force an unrelated type or edit the library to add one. |
| Required facts are missing or contradictory | Follow the contract's unresolved-fact rules. Hold content or favorable readiness claims that require those facts; continue only independent supported content. Ask the requester for the specific resolving evidence or decision. |
| A check fails or selection changes | Return to A2 or A3, then repeat the affected review. Preserve actual failure information when the selected contract requires it; do not present a retest as an earlier success. |
| Saving, registration, revision, or publication exceeds authoring scope, authorization, or runtime permissions | Hand the prepared content and exact unresolved condition to `doc-updates`. Do not bypass the boundary by editing a read-only directory. An incompatible recipient workflow remains a reported handoff gap. |

No production-execution hold is released by this procedure because production
execution is outside its scope. Read-only selection and independent drafting
do not require performing the operations described in the document.

## Completion, records, and maintenance

Authoring completes when requested content and its actual contract checks
are delivered to the authorized recipient, with unresolved obligations
visible. Report the specification ID and source, location or handoff, checks,
results, gaps, and any authorized exception in the session or the task's
existing evidence record. Host registration and PR progression remain exclusively the update
workflow's responsibility. Do not invent signoffs or require
additional logs, retention rules, or review roles absent from the task or
selected contract.

Review this procedure when the governing responsibility, installed layout,
catalog conventions, or handoff contract changes. An authorized maintainer
updates the affected skill resources and makes material changes visible in
the actual change report. Ownership remains unassigned until established.
