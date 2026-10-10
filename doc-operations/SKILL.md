---
name: doc-operations
description: >-
  Find, read, and apply existing documentation for authorized host or project
  tasks. Use whenever preparing any basic task or complex host work, including
  commands, configuration, installed tools, shared services, runtimes, integrations,
  maintenance, and operational work inside a project, even without an
  explicit documentation request. Consult $HOME/.agents/doc-operations/INDEX.md
  and applicable current documents; use specific official sources and report
  missing coverage when necessary. Owns documentation access and use, not
  document authoring, revision, saving, registration, or publication.
  doc-specs owns authoring contracts; doc-updates owns document maintenance
  and host-document saving and registration.
---

# Existing documentation access and use

## Authority and paths

Read `$HOME/.agents/AGENTS.md` as the governing host instructions. This skill
implements their documentation-consultation responsibility. The task's own
workflow performs authorized operations; consulting guidance grants no
execution permission and requires no preliminary work document.

| Installed location or context | Consultation role |
|---|---|
| `$HOME/.agents/doc-operations/INDEX.md` | Catalog of current host operational coverage. |
| `$HOME/.agents/doc-operations/` | Read-only current operational documents. |
| Authorized project context | Existing project instructions and documentation applicable to that project. |
| `$HOME/.agents/doc-specs/INDEX.md` | Authoring contracts, not host state or operational coverage. |
| `$HOME/.agents/doc-updates/` | Prepared host documents, not current operational guidance. |
| `$HOME/.agents/skills/doc-operations/` | This consultation entrypoint and bundled guide. |

Resolve `$HOME` for the adopting account. In an explicitly authorized
development checkout, map `$HOME/.agents/` to that checkout for reads and
checks, and installed `AGENTS.md` to `dev-AGENTS.md` when designated by the
requester. Keep installed paths in instructions; the checkout does not
identify the operational host.

Resolve catalog links relative to `$HOME/.agents/doc-operations/`, project
links relative to their containing document, and bundled links relative to
this skill file. Check resolved targets, including symlinks, before opening
them. Host operational catalog targets must remain inside `doc-operations/`;
project references require their actual authorized context. An escaping or
unresolved target is unavailable, not permission to read outside the scope.

## Consultation workflow

1. Establish the requested operation, actual host or project target,
   applicable versions, and authorized access from the request and available
   evidence. Keep unknown target facts explicit.
2. Read `$HOME/.agents/doc-operations/INDEX.md` before the task. Select by
   actual catalog purpose and applicability. An empty catalog means missing
   coverage; it says nothing about installed components. Do not invent
   entries or require a named policy or runbook absent from the catalog.
3. Read the complete applicable linked documents before executing their
   steps. Follow their established order, prerequisites, constraints,
   checks, and recovery instructions. For project work, also consult the
   applicable existing project instructions and documentation within the
   authorized project context; these supplement host consultation.
4. Compare guidance with authorized evidence for the actual target. A
   document, catalog row, tool specification, or skill does not prove a
   version, configuration, approval, release, or readiness condition.
   Resolve material conflicts rather than adapting a procedure silently.
5. When coverage is absent or unusable, consult applicable official sources
   before dependent execution and report the gap. Follow
   [the consultation guide](references/consultation-guide.md) for source
   selection, unavailable inputs, conflicts, or host/project overlap.
6. Return the selected guidance and actual readiness findings to the task's
   authorized execution workflow. Revisit consultation when another
   operation, tool, component, or version enters scope.

## Responsibility boundaries

- Use `$HOME/.agents/skills/doc-specs/SKILL.md` for selecting and applying
  document authoring contracts and creating documents.
- Use `$HOME/.agents/skills/doc-updates/SKILL.md` for existing-document
  maintenance and host-document saving in `$HOME/.agents/doc-updates/` and
  registration in its `INDEX.md`. Project documents belong in their
  authorized project context.
- Report documentation gaps in the session or the task's existing record.
  This skill does not create a board entry, revise documents, or publish
  guidance. Do not inspect `doc-updates/` as an operational readiness gate
  or consume its candidates as the current edition.
- If another skill's unfinished instructions conflict with the governing
  responsibilities, report the specific incompatible handoff. Continue
  independent consultation without repairing that skill or adopting its
  conflicting workflow.

## Completion account

Report the documents actually consulted, their known editions and
applicability, verified target facts, unresolved prerequisites, and affected
dependent work. If local coverage was absent or unusable, identify the
affected entry or path, the specific official sources actually used, and
the decisions based on them. If those sources could not be consulted, say
so and identify the remaining dependency. Separate documentary advice,
observed host facts, and proposed action; claim only checks and operations
that actually occurred. No additional report file or fixed output format
is required for routine consultation.
