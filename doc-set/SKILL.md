---
name: doc-set
description: Create documents using doc-specs and register them in pull-request indexes. Use whenever a user or agent requests a document, report, proposal, runbook, guide, or other documentary deliverable, including an explicit output path.
---

# doc-set

1. Identify the document's type, purpose, host or workspace scope, and explicit destination from the task.
2. Read `$HOME/.agents/doc-specs/INDEX.md`; select and read the matching specification and required references. Keep `doc-specs` read-only. Ask if the specification or scope cannot be resolved.
3. Apply the specification's structure, naming, and validation rules using verified task context. Do not execute documented operations.
4. Use an explicit destination when provided; otherwise use `$HOME/.agents/doc-operations/pull-request/` for global host documents or `$PWD/.agents/doc-operations/pull-request/` for workspace project documents.
5. Create missing destination directories and save the document. For default destinations, update their `INDEX.md`, creating it from the template below if absent; for explicit destinations, follow the task's indexing requirements.
6. Preserve existing index entries and structure. Add or update one row per saved document with a relative document link, the specification link, and verified metadata; mark unknown values `Unspecified`.

## New index template

```markdown
# Document Index

| Type | Document | Path | Purpose and applicability | Responsibility | Edition | Use boundary | Specification |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

