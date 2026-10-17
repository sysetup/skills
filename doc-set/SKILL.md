---
name: doc-set
description: Create documents using doc-specs and register default outputs in doc-requests indexes. Use whenever a user or agent requests a document, report, proposal, runbook, guide, or other documentary deliverable, including an explicit output path.
---

# doc-set

Resolve `<workspace>` from the task; otherwise search the current directory and its authorized ancestors for the nearest `.agents/` directory, excluding `$HOME/.agents/`, and use its parent. If absent, use the current directory. Skill placement under `.agents/skills/` does not determine task scope.

## Document eligibility

Derive every authored document exclusively from an existing, applicable `doc-specs` specification and follow its content, structure, naming, and validation contract. Directory categories do not authorize additional document types.

Reserve host and workspace `doc-requests/` and `doc-operations/` for complete, concrete operational documents ready to guide production work. Exclude logs, problem and incident records, retrospective state or activity reports, research findings, and unfinished drafts, even when `doc-specs` defines those types. Keep review findings and authoring issues in the conversation. Maintain `INDEX.md` only as the required catalog. Document readiness does not grant execution or publication authority.

For difficult documents, resolve authoring requirements from the applicable specification. If no specification fits or required operational facts remain unresolved, report the gap to the user before dependent writes. Adapt the operational content to an existing eligible type or integrate it into an eligible document only when its specification permits; otherwise omit the proposed artifact. Do not invent specifications, relabel excluded records as operational documents, or delete existing files without explicit authorization.

## Workflow

1. Identify type, purpose, host or workspace scope, and destination. Create only requested, self-contained `doc-specs` documents; omit companion documents, third-party licenses, alternate references, cross-document citations or links, and auxiliary files.
2. For workspace scope, read the first existing catalog: `<workspace>/.agents/doc-specs/INDEX.md`. Use `$HOME/.agents/doc-specs/INDEX.md` for host scope or when workspace catalogs are absent. Select and read the matching specification and required references within authorized scope. Keep `doc-specs` read-only. Report missing catalogs or specifications and apply document eligibility; ask if scope remains unresolved.
3. Apply the specification's structure, naming, and validation rules using verified task context. Preserve concrete supplied or existing metadata; when the specification omits it, author a descriptive filename, `Local edition` (initially `1.0`, independent of the specification's edition), `Responsibility` (accountable role), and other required index fields from the work context. Mark every document body with `Source specification: <ID>; edition: <EDITION>`; use `Unspecified` for unverifiable specification editions and verify indexed metadata before delivery. If no validator is available, check the rules manually and report the validation limitation. Do not execute documented operations.
4. Use an explicit destination when provided; otherwise use `$HOME/.agents/doc-requests/` for global host documents or `<workspace>/.agents/doc-requests/` for workspace project documents.
5. Within `doc-requests` or `doc-operations`, register every document, including explicit destinations, in that root's `INDEX.md`; create it from the template if absent and use it as the sole entry point. Elsewhere, follow the task's indexing requirements.
6. Preserve existing index entries and structure. Match rows by normalized `Installed path`, resolving relative paths against the index directory; update the matching row or append one if absent. Report multiple matches before changing those rows. Record one row per saved document with a relative document link and verified metadata; reserve `Unspecified` for unverifiable source facts, not author-created metadata.

If issues come up:

1. Report save failures, directory errors, denied access, insufficient privileges, or sandbox restrictions to the requester. Stop dependent writes. For access restrictions, provide the directory owner with a command that creates the exact prepared document and required index update from their control panel; respect the authorized editing mechanism. For other failures, identify the cause and required correction before supplying that command. Resolve incomplete content or uncertain destinations first.

For documentation related to the global host treat `$HOME/.agents/doc-operations/` and its descendants as read-only; write there only when the user explicitly instructs it. Always write documents to `$HOME/.agents/doc-requests/` unless the user explicitly instructs writing to `doc-operations/`. This note takes precedence over all other destination, indexing, and hierarchy instructions in this skill.

## New index template

```markdown
# INDEX.md <doc-requests>|<doc-operations>

| Type | Document | Installed path | Purpose and applicability | Responsibility | Local edition | Use boundary |
| --- | --- | --- | --- | --- | --- | --- |
```

Use `Type` for the specification's document type; `Document` for the title linked to the saved document; `Installed path` for the intended approved location, outside `doc-requests/`; `Purpose and applicability` for the outcome and applicable context; `Responsibility` for the accountable role or owner; `Local edition` for the document's own version; and `Use boundary` for its limits and exclusions. If unspecified, derive `Installed path` by mapping the saved path from the `doc-requests/` root to the corresponding `doc-operations/` root, preserving the relative hierarchy.

In the `INDEX.md` file, do not add any notes, comments, or additional instructions outside the table.

## Directory hierarchy

Within `doc-requests` or `doc-operations`, select a category below by purpose, then group by domain, topic, technology, protocol, or convention: `<category>/<group>/…/<document>.md`. Use representative kebab-case names of at most four words, create only needed directories, and mirror the hierarchy in `Installed path`. Resolve incompatible explicit paths before writing.

| Directory | Responsibility |
| --- | --- |
| `00-governance/` | Policies, standards, and organizational advice. |
| `01-processes/` | Recurring procedures, runbooks, playbooks, and work instructions. |
| `02-plans/` | Planned scope, resources, sequencing, and readiness. |
| `03-specifications/` | Requirements, architecture, design, interfaces, test definitions, and product information. |
| `04-control/` | Production controls and matrices that meet document eligibility. |
