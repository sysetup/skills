---
name: doc-specs
description: >-
  Select and apply the read-only document authoring specifications in
  $HOME/.agents/doc-specs/ to create host or project documents grounded in
  actual evidence. Use whenever drafting a document, report, proposal,
  runbook, guide, or structured documentary deliverable, even without an
  explicit skill request. Also use for specification selection and content
  checks requested by doc-updates during a revision. Owns selection,
  authoring, and contract-based review; doc-operations owns documentation
  access for task execution, and doc-updates owns existing-document
  maintenance and the complete host operational-document PR lifecycle. Does not maintain
  the specification library or execute the operations described.
---

# Document specification selection and authoring

## Authority and paths

Read `$HOME/.agents/AGENTS.md` as the governing host instructions. This skill
implements its specification-authoring responsibility; it introduces no
document mode, preliminary work-document requirement, or policy exemption.

| Installed location | Role in this workflow |
|---|---|
| `$HOME/.agents/doc-specs/INDEX.md` | Current catalog for choosing an authoring contract. |
| `$HOME/.agents/doc-specs/` | Read-only specifications; never a finished-document destination. |
| `$HOME/.agents/skills/doc-specs/` | This entrypoint and its bundled authoring resources. |
| `$HOME/.agents/skills/doc-operations/SKILL.md` | Documentation consultation for authorized host or project work. |
| `$HOME/.agents/skills/doc-updates/SKILL.md` | Document maintenance and host operational-document PR ownership. |
| `$HOME/.agents/doc-updates/` | Host operational documents prepared under the update workflow. |
| Authorized project context | Documents about that specific project. |

Resolve `$HOME` for the adopting account; do not replace it with a development
checkout or infer an operational target from this machine. In an explicitly
authorized development checkout, map the installed `.agents/` tree to that
checkout for reads and checks; map installed `AGENTS.md` to `dev-AGENTS.md`
when that source is designated. Keep installed paths in authored guidance.
Resolve catalog links relative to the catalog directory and bundled links
relative to their containing skill file. Check resolved targets, including
symlinks, remain inside their respective authorized roots before access.

## Workflow and handoffs

Read [the authoring procedure](references/document-authoring.md) for
selection, drafting, contract checks, and dependency handling. It is the
single method for new documents and for authoring support during a revision.
Read [the usage guide](references/usage-guide.md) only for selection examples
or clarification of the handoffs.

- **New document:** Apply the authoring procedure to each requested
  deliverable. Draft from established facts and review against the full
  selected contract before delivery.
- **Existing document:** Route maintenance through
  `$HOME/.agents/skills/doc-updates/SKILL.md`. Supply specification selection,
  requested content, and contract checks to that workflow without taking
  ownership of source preservation, revision management, or publication.
- **Host operational document or instruction:** Route the request to
  `doc-updates` before drafting so it registers intake. Supply contract
  selection, drafting and content checks within that workflow; return content,
  basis and gaps for its mandatory draft registration and preparation.
  `doc-updates` alone owns all PR gates and authorized publication.
  Do not directly deliver into `doc-operations/`.
- **Project document:** Deliver in the authorized context of its owning
  project. Host registration does not apply merely because the project runs
  on this host.
- **Operational task:** Use `doc-operations` for documentation consultation
  and the task's own authorized workflow for execution. Authoring a runbook
  or plan does not authorize performing its steps.

Other skills' unfinished or contradictory instructions do not change this
assignment. Report an incompatible handoff against the governing host
instructions and continue independent authoring; do not repair those skills
or silently invent their workflow.

## Delivery boundary

Report the applied specification ID and source, document location or handoff,
checks actually performed, results, and material gaps. Separate planned
checks from observations and documentary completeness from execution,
approval, acceptance, publication, and runtime skill activation. Claim no
full contract compliance while required obligations remain unresolved.
