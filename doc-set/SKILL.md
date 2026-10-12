---
name: doc-set
description: Create documents using doc-specs and register default outputs in pull-request indexes. Use whenever a user or agent requests a document, report, proposal, runbook, guide, or other documentary deliverable, including an explicit output path.
---

# doc-set

Resolve `<workspace>` from the task; otherwise search the current directory and its authorized ancestors for the nearest `.agents/` directory, excluding `$HOME/.agents/`, and use its parent. If absent, use the current directory. Skill placement under `.agents/skills/` does not determine task scope.

1. Identify the document's type, purpose, host or workspace scope, and explicit destination from the task.
2. For workspace scope, read the first existing catalog: `<workspace>/.agents/doc-specs/INDEX.md`. Use `$HOME/.agents/doc-specs/INDEX.md` for host scope or when workspace catalogs are absent. Select and read the matching specification and required references within authorized scope. Keep `doc-specs` read-only. Report missing catalogs; ask if the specification or scope cannot be resolved.
3. Apply the specification's structure, naming, and validation rules using verified task context. Preserve concrete supplied or existing metadata; when the specification omits it, author a descriptive filename, `Local edition` (initially `1.0`, independent of the specification's edition), `Responsibility` (accountable role), and other required index fields from the work context. Keep document and index metadata consistent. If no validator is available, check the rules manually and report the validation limitation. Do not execute documented operations.
4. Use an explicit destination when provided; otherwise use `$HOME/.agents/doc-operations/pull-request/` for global host documents or `<workspace>/.agents/doc-operations/pull-request/` for workspace project documents.
5. For default destinations, select the family below, create missing family directories, and save the document there. Update only the selected root index: `$HOME/.agents/doc-operations/pull-request/INDEX.md` or `<workspace>/.agents/doc-operations/pull-request/INDEX.md`; create it from the template if absent. For explicit destinations, create missing destination directories, save the document, and follow the task's indexing requirements.
6. Preserve existing index entries and structure. Match rows by normalized `Installed path`, resolving relative paths against the index directory; update the matching row or append one if absent. Report multiple matches before changing those rows. Record one row per saved document with relative document and specification links and verified metadata; reserve `Unspecified` for unverifiable source facts, not author-created metadata.

If issues come up:

1. Report save failures, directory errors, denied access, insufficient privileges, or sandbox restrictions to the requester. Stop dependent writes. For access restrictions, provide the directory owner with a command that creates the exact prepared document and required index update from their control panel; respect the authorized editing mechanism. For other failures, identify the cause and required correction before supplying that command. Resolve incomplete content or uncertain destinations first.

## New index template

```markdown
# Document Index

| Type | Document | Installed path | Purpose and applicability | Responsibility | Local edition | Use boundary | Authoring contract, specification used |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Use `Type` for the specification's document type; `Document` for the title linked to the saved document; `Installed path` for the intended approved location, outside `pull-request/`; `Purpose and applicability` for the outcome and applicable context; `Responsibility` for the accountable role or owner; `Local edition` for the document's own version; `Use boundary` for its limits and exclusions; and `Authoring contract, specification used` for the linked specification and its edition. If unspecified, derive `Installed path` by removing only the staging `pull-request/` component from the saved path.

## Directory hierarchy

For default destinations, classify by purpose under the selected `pull-request/` root. Mirror the family in the intended installed path. Create only the required directory:

| Directory | Responsibility |
| --- | --- |
| `00-governance/` | Policies, standards, and organizational advice. |
| `01-processes/` | Recurring procedures, runbooks, playbooks, and work instructions. |
| `02-plans/` | Planned scope, resources, sequencing, and readiness. |
| `03-specifications/` | Requirements, architecture, design, interfaces, test definitions, and product information. |
| `04-control/` | Current records: registers, matrices, requests, decisions, and trade studies. |
| `05-evidence/` | Completed activities, observations, reviews, reports, releases, and handoffs. |
