---
name: doc-updates
description: >-
  Maintain existing host or project documents and save and register prepared
  host operational documents in $HOME/.agents/doc-updates/. Use whenever
  revising, correcting, extending, reconciling, or updating documentation,
  even without an explicit skill request, and when doc-specs hands off a new
  host operational document for saving and registration. Preserve current
  sources, revision identity, and affected references. Owns maintenance and
  host-document saving and registration; doc-specs owns contract selection,
  authoring, and content checks, and doc-operations owns documentation access
  for task execution. Does not publish current operational guidance, maintain
  specifications, or execute documented operations.
---

# Document maintenance, saving, and registration

## Authority and paths

Read `$HOME/.agents/AGENTS.md` as the governing host instructions. This skill
implements their document-update responsibility; it adds no document mode,
preliminary work-document requirement, specification board, or publication
authority.

| Installed location or context | Role in this workflow |
|---|---|
| `$HOME/.agents/doc-operations/INDEX.md` and its references | Read-only current operational sources. |
| `$HOME/.agents/doc-updates/` | New and revised host operational documents prepared for review. |
| `$HOME/.agents/doc-updates/INDEX.md` | Registration catalog and current registration guidance. |
| `$HOME/.agents/doc-specs/INDEX.md` and its references | Read-only document authoring contracts. |
| `$HOME/.agents/skills/doc-updates/` | This entrypoint and its bundled update procedure. |
| Authorized project or native-artifact context | Existing project documents and artifacts governed by their native layout. |

Resolve `$HOME` for the adopting account. In an explicitly authorized
development checkout, map `$HOME/.agents/` to that checkout for reads and
checks, and installed `AGENTS.md` to `dev-AGENTS.md` when designated by the
requester. This mapping does not expand write scope or identify the host
being documented. Keep installed paths in authored instructions.

Resolve catalog links relative to their catalog, document links relative to
their containing document, and bundled links relative to this skill file.
Check resolved targets, including symlinks, before access and mutation.
Operational catalog targets stay within `doc-operations/`; specification
targets stay within `doc-specs/`; working catalog targets stay within
`doc-updates/`, except verified publication-history locators described by
its index. Project and native-artifact targets require their actual
authorized context. An escaping or unresolved target is a dependency gap,
not permission to access another root.

## Workflow and handoffs

Read [the update procedure](references/host-document-update.md) before maintaining an
existing document or saving and registering a host-document handoff. It
owns revision preservation, reference reconciliation, registration checks,
and failure handling.

- **Existing document:** Inspect the actual source and authorized change.
  Request contract selection, affected authoring, and content checks through
  `$HOME/.agents/skills/doc-specs/SKILL.md`; retain ownership of the update
  workflow rather than duplicating the authoring method.
- **New document:** Use `doc-specs` to author it. Receive a new host
  operational document for required saving and registration; a new project
  document stays with its authorized project context.
- **Host operational document:** Consult the current registration guidance
  in `$HOME/.agents/doc-updates/INDEX.md`. Save and register the new document
  or changed copy there. Preserve the source in `doc-operations/`, which
  remains read-only during this workflow.
- **Project or explicitly requested native-artifact edit:** Classify by
  actual purpose and apply the authorized revision in its established
  context, preserving native requirements. Directory location alone does
  not establish that purpose. Native format does not waive required host
  operational document saving and registration or canonical read-only
  boundaries.
- **Operational task:** Use `$HOME/.agents/skills/doc-operations/SKILL.md`
  for consultation and the task's own authorized workflow for execution.
  Revision, saving, and registration grant no execution authority.

Use existing authorization for the requested bounded edit; ask only for
material missing evidence, unresolved scope, or additional authority. A
separate request to change `doc-operations/` or `doc-specs/` requires its own
explicit scope and runtime permissions and is outside this skill's ordinary
workflow. Report incompatible handoffs against the governing instructions;
continue independent authorized work without repairing other skills.

## Completion account

Report the actual source and known edition, applied specification ID and
source or uncovered native purpose, changed document location, host catalog
registration when applicable, checks and results, and remaining gaps.
Distinguish a prepared revision from current operational guidance, and
preparation from approval, acceptance, publication, and performed operations.
Saving without required registration is an incomplete host-document handoff.
