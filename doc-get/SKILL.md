---
name: doc-get
description: Find, read, and apply existing host or workspace documentation. Use whenever a user or agent requests existing documentation or a task requires guidance for commands, configuration, tools, services, runtimes, integrations, maintenance, or project work.
license: MIT
metadata:
  author: "SYSETUP.COM CarlosHRG"
---

# doc-get

Resolve `<workspace>` from the task; otherwise search the current directory and its authorized ancestors for the nearest `.agents/` directory, excluding `$HOME/.agents/`, and use its parent. If absent, use the current directory. Skill placement under `.agents/skills/` does not determine task scope.

1. For operational tasks, select `$HOME/.agents/doc-operations/INDEX.md` for host scope or `<workspace>/.agents/doc-operations/INDEX.md` for workspace scope; select both for mixed scope. Keep catalog access within authorized boundaries.
2. In every consulted `INDEX.md`, first read the table columns `Document`, `Purpose and applicability`, and `Use boundary` to locate the topic and select the applicable document. Read other columns only if these three are insufficient to determine document selection or use boundaries. If the workspace index or topic is missing, consult the corresponding host index for applicable shared guidance within authorized scope. Do not substitute authoring specifications for operational documentation.
3. Read only the relevant linked documents; resolve each relative link from the directory of the file containing it. Check their scope, edition, and prerequisites against the task.
4. Apply the relevant instructions to complete only the assigned, authorized task. Treat documentation as guidance, not execution permission; do not create or modify documentation.
5. Report missing indexes, documents, or ambiguous matches. Ask for blocking clarification; use official sources for uncovered details only within research permissions.

Caution: Documents under `*/doc-requests/*` are proposed canonical documents. Do not read them; they are not official documents.
