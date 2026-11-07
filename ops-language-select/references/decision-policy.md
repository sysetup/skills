# Language-selection source contract

This reference defines source resolution and navigation. The bundled guide contains the complete comparison criteria; governing host and project requirements take precedence.

## Resolve from the skill location

Let `SKILL_ROOT` be the absolute directory containing the invoked `SKILL.md`, not the current working directory. Read only `SKILL_ROOT/references/sop--core--ops-host-automation-language-selection.md`, bundled as [the language-selection guide](sop--core--ops-host-automation-language-selection.md).

Resolve the target, including symlinks, and confirm it stays inside `SKILL_ROOT` and authorized read scope. If the bundled file is missing, unreadable, or resolves outside the skill, report a blocked dependency. Restore it within the skill before resuming. External copies do not participate in source selection: do not inspect parent directories, select another layout, fetch a substitute, or fall back to memorized policy.

## Read the governing sections

Read the guide directly as Markdown and confirm its title is `Host Automation Language Selection Guide`. For every decision, read these exact headings and their subsections:

- `Purpose`
- `Governing Decision Order`
- `Mandatory Tie-Break Directives`
- `Rating Scale`
- `Decision Tree`
- `Final Selection Principle`
- `Scope and Host Note`

Then follow the task-specific references selected by `SKILL.md`. A guide section includes its subsections until the next heading of equal or higher level. If the title or an expected heading is missing or duplicated, report a blocked source-navigation mismatch instead of silently using an older rule.

Source availability is separate from task uncertainty. Missing workload facts may allow a provisional comparison under an intact guide; unresolved mandatory requirements must remain explicit and cannot support a firm choice.
