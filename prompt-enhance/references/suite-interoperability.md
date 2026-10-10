# Suite interoperability

The suite separates operation ownership from prompt surface and subject matter.

- **Create a new known-surface artifact:** use its surface generator (`prompt-task`, `prompt-agent`, `prompt-api`, `prompt-delegation`, `prompt-action`, or `prompt-persistent`).
- **Enhance an existing prompt:** use `prompt-enhance`, preserving the source surface.
- **Audit without rewriting:** use `prompt-linter`.
- **Choose a capability:** use `prompt-router`.
- **Prepare a settled technical Dictamen for execution:** use `prompt-dictamen`.
- **Compact a conversation for continuation:** use `prompt-handoff`.

A RouteDecision is optional. Version 2.1 decisions may include `handler` to name the selected capability. For enhancement, `kind` is `transformer`, `handler` is `prompt-enhance`, `generator` is null, and `surface` is advisory: it may identify the source surface but does not transfer ownership to the transformer.

Do not require sibling Skills for core operation. If a sibling is available, its artifacts may be consumed as evidence; if unavailable, operate from the supplied prompt and verified local context. Never claim that an unexecuted linter, validator, host parser, or live model evaluation ran.

For compound work, keep phases explicit. A migration and a semantic enhancement are distinct transformations; preserve an intermediate artifact or ledger so each phase can be reviewed without hiding scope or capability loss.
