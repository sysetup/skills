# Document specification authoring usage guide

## Purpose, audience, and boundaries

This guide helps document authors and requesting agents distinguish document
purposes and handoffs. Its advice is nonbinding; obligations cited from
`$HOME/.agents/AGENTS.md` and selected specifications retain their authority.
It has no external client. Its authoring basis is `GUIDE@core` at
`$HOME/.agents/doc-specs/00-governance/guide--core.spec.md`.

The skill entrypoint defines installed paths and authorized development
mapping. The authoring procedure owns the method. This guide adds illustrative
decision cues, not modes, task-execution policy, revision controls, or another
authoring workflow.

## Choose the purpose before the label

Use the current `$HOME/.agents/doc-specs/INDEX.md` rather than these examples
as the selection source. The examples below are synthetic, not records of
host operations or claims that those operations are authorized.

| Illustrative request | Reasoned selection cue and limit |
|---|---|
| Explain a service's parameters for lookup | A technical reference may fit because the reader needs definitions and behavior, rather than an ordered operation. Confirm the current catalog boundary. |
| Restore one identified service after a bounded failure | An operational runbook may fit because the reader needs target checks, actions, deviations, and recovery. Missing target or command evidence limits execution readiness. |
| Teach a beginner a concept through isolated practice | A tutorial may fit because the outcome is learning through checkpoints. A filename such as `RUNBOOK.md` does not change that purpose. |
| Coordinate a response with branching roles and decisions | A playbook may fit; the incident subject determines whether a specialized variant is required. Avoid a generic variant whose boundary excludes the subject. |
| Describe this repository's entrypoints | A repository overview may fit. An installation manual or governance policy would impose a different reader task. |

Selection by purpose costs a small initial classification step but avoids
obligations borrowed from an unrelated document type. When the facts needed
to distinguish candidates are missing, use the procedure's input-gap route
rather than guessing from the title.

## Separate authoring from the surrounding workflow

A new host operational request first enters `doc-updates` for intake.
`doc-specs` drafts and checks within that request, then returns content to
`doc-updates` for mandatory draft registration and the remaining PR gates.
Recommend carrying the actual contract identity, source basis, performed
checks, and gaps in that handoff so the recipient can register supported
facts. The required host destination comes from the governing instructions;
this recommendation adds no registration fields or publication controls.

A project document stays with the project that owns its subject. Sharing the
host does not make it host operational documentation. For revisions, let
`doc-updates` establish the maintenance context and request authoring support
here; repeating a separate maintenance workflow would risk competing source
and publication decisions.

For operational work, `doc-operations` consults current operational guidance.
Reading a specification to draft a document is part of authoring and does
not turn `doc-specs` into the operational-document consumption skill. A
document's commands remain instructions for an authorized reader; writing
them is not evidence that they ran.

## Uncovered native artifacts

A skill definition or another native artifact can have required metadata
that differs from a cataloged finished document. Confirm whether the catalog
actually covers that artifact. If it does not, state the gap and use the
native format without claiming compliance with an unrelated specification.
Separately authored guides or procedures still receive their own applicable
contracts. This preserves native format validity while keeping documentary
obligations visible.

## Maintenance

The governing instructions assign no guide maintainer; ownership is
unresolved and requires assignment when maintenance is authorized. Review
the guide when responsibilities, catalog boundaries, or the installed layout
change. Make material changes visible through the revised guide and the
authorized session's change report; no review cadence is invented.
