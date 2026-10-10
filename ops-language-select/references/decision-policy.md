# SOP source contract

This reference owns source resolution and navigation only. The bundled SOP owns every language-selection rule, score, tie-break, and operational control.

## Resolve from the skill location

Let `SKILL_ROOT` be the absolute directory containing the invoked `SKILL.md`, not the current working directory. For both development and installed use, read only `SKILL_ROOT/references/sop--core--ops-host-automation-language-selection.md`, bundled as [the language-selection SOP](sop--core--ops-host-automation-language-selection.md).

Resolve the target, including symlinks, and confirm it stays inside `SKILL_ROOT` and authorized read scope. If the bundled file is missing, unreadable, or resolves outside the skill, report a blocked dependency. Restore it within the skill before resuming. External copies do not participate in source selection: do not inspect parent directories, select another layout, fetch a substitute, or fall back to memorized policy.

## Read the controlled content

Read the SOP as Markdown containing labeled JSON fences. Parse JSON rather than interpreting its escaped newlines as document structure. No executable helper is required: use the host's read capability, and a JSON parser if the encoded guide is not readable directly. Read each required fence once; repeated or malformed required blocks are ambiguous and block the decision.

| Fence | Required content |
|---|---|
| `record-metadata` | Confirm `id` is `OPS-HOST-AUTOMATION-LANGUAGE-SELECTION`; inspect `record_revision`, `lifecycle_state`, and `approval_refs` without inferring approval. |
| `data:process` | Read `purpose_scope` and `roles` for scope and ownership. |
| `data:readiness` | Read `inputs_outputs`, `equipment_materials`, `safety_regulatory`, and `prerequisites` for inputs, access and artifact controls. |
| `data:procedure` | Decode `procedure` as the Markdown guide; read `holds` and `abnormal` as operational controls. |

Missing fields, wrong identity, malformed JSON, or an unreadable required section block a source-backed decision. Report the discrepancy; do not substitute another policy. Source availability is separate from task uncertainty: missing workload facts may allow a provisional decision under an intact SOP, while a missing SOP does not.

## Governing sections

Read these exact headings in the decoded `data:procedure.procedure` for every decision:

- `Purpose`
- `Governing Decision Order`
- `Mandatory Tie-Break Directives`
- `Rating Scale`
- `Decision Tree`
- `Final Selection Principle`
- `Scope and Host Note`

Then follow the task-specific references selected by `SKILL.md`. A guide section includes its subsections until the next heading of equal or higher level. If an expected heading is missing or duplicated, report a source-navigation mismatch instead of silently using an older rule.

The skill's decision record is a conversational application of this content. Formal release, host changes, and retained operational evidence remain governed by the SOP and the active user's authorization.
