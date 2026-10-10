# Host statements, guidelines, standards and rules.
**General Operations (DevOps)**

## Documentation authority and specifications
- **Canonical Specifications:** `$HOME/.agents/doc-specs/INDEX.md` and its references are the read-only canonical library of document authoring specifications. It defines contracts, not project facts or a destination for finished documents.
- **Specification Compliance:** Absolutely every document you need, want, or wish to create must be based on the specifications listed at the following path: `$HOME/.agents/doc-specs/`.
- **Specification Skill:** Use `$HOME/.agents/skills/doc-specs/SKILL.md` to take full advantage of the specifications and create all kinds of documents.
- **Update documents Skill:** Use `$HOME/.agents/skills/doc-updates/SKILL.md` to take full advantage of the statements, guidelines, standards and rules to update all kinds of documents.
- `$HOME/.agents/doc-operations/` is a read-only directory used to access existing documentation and follow instructions regarding all tasks and/or processes on this host; any document created for the operation of this host (`$HOSTNAME`) must be saved in `$HOME/.agents/doc-updates/` and registered in `$HOME/.agents/doc-updates/INDEX.md`.
- Documents intended to cover topics related to specific projects should be created in host paths corresponding to the appropriate context for the work being performed.

## Host Operational Guidance
- **Canonical host documentation:** `$HOME/.agents/doc-operations/INDEX.md` holds current operational documentation for the host: tasks, installed tools, commands, configurations, shared services, runtimes, integrations, and maintenance. Its catalog describes actual coverage; it does not establish facts about undocumented host components.
- **Accessing and Using Documentation:**: Before performing any complex work or basic task on this host, you must consult the canonical documentation specified in `$HOME/.agents/doc-operations/INDEX.md` list, enter to the canonical relative documentation and follow each of the established and ordered guidelines. If there is no documentation related to the task in the `$HOME/.agents/doc-operations/INDEX.md` list, you must consult the official documentation provided by Context7, the official documentation from the owners of the tools or processes, and/or Context7 itself before executing the task. Finally, you must report to the user or agent who requested the task that no documentation existed to perform it and that decisions were made based on specific official documentation taken from the user manuals of the operating system or process tools, as well as publicly defined standards not from this host from reliable, recognized, secure, and effective sources.
- **Accessing documents Skill:** Use `$HOME/.agents/skills/doc-operations/SKILL.md` to take full advantage of the statements, guidelines, standards and rules to accessing and using all kinds of documentation.
