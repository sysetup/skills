---
name: doc-get
description: Find, read, and apply existing host or workspace documentation. Use whenever a user or agent requests existing documentation or a task requires guidance for commands, configuration, tools, services, runtimes, integrations, maintenance, or project work.
---

# doc-get

1. Read `$HOME/.agents/doc-operations/INDEX.md` for host tasks or `$PWD/.agents/doc-operations/INDEX.md` for workspace project tasks; read both for mixed scope.
2. Locate the topic and applicable document in the selected index. If workspace coverage is missing, consult the host index for applicable shared guidance.
3. Read the relevant linked documents; resolve relative links from each index's directory. Check their scope, edition, and prerequisites against the task.
4. Apply the relevant instructions to complete only the assigned, authorized task. Treat documentation as guidance, not execution permission; do not create or modify documentation.
5. Report missing indexes, documents, or ambiguous matches. Ask for blocking clarification; use official sources for uncovered details only within research permissions.
