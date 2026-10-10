# Native question channel

Read this file when this skill needs to ask the user anything. It is the
source of truth for discovering the current harness, mapping question types
onto that harness's live schema, and falling back to text.

The skill is harness-agnostic. The agent using it must **wake up and
investigate this session**, then use whatever interactive questionnaire that
harness actually exposes. A hint table is a shortcut, not a catalog of
allowed products and not a substitute for the live tool schema.

## 1. Why native first

A native question card lets the user answer with keyboard and/or mouse:
arrow keys, number/letter shortcuts, Tab, Space, Enter, click. That is
faster and less error-prone than typing numbered replies into chat.

Markdown questionnaires are the degraded channel. Use them only when the
native channel is missing or disabled.

## 2. Investigate this session

Do this investigation **every time** questions will be asked. Do not reuse
an earlier session's conclusion. Do not scan the host filesystem looking for
harnesses. Stay inside evidence already in this conversation.

Collect evidence in this order:

1. **Tools offered this turn.** This is the strongest signal. Read the tool
   list injected into the system/developer prompt, including MCP tools.
2. **Live schema** of each candidate (tool description, JSON schema,
   `search_tool` / equivalent docs). Never guess parameter names.
3. **Identity strings** in the system/developer prompt (product name,
   runtime name, "You are …"). Use them only to pick which hint to try
   first.
4. **Feature flags and config** mentioned in the prompt or harness docs
   already in context (for example a boolean that disables the question
   tool).
5. **Actor role.** If this actor is a subagent, background worker, or other
   session without a user-facing UI, do not ask the user here. Return the
   logical question set to the parent so the parent can run this protocol.

An unknown or future harness is valid. Run the same algorithm.

## 3. Candidate selection

Keep a tool as a candidate when its **name or description** indicates a
user-facing choice UI. Match case-insensitively against patterns such as:

- `ask_user`, `AskUser`, `ask_user_question`, `AskUserQuestion`
- `request_user_input`, `request_user`, `AskQuestion`
- `question`, `questionnaire`, `choice`, `select option`
- harness-owned `elicit` that presents a question card to the human

Drop a candidate when it is any of:

- a permission, sandbox, or approval prompt
- plan-mode approval / exit-plan tools
- third-party MCP elicitation (an MCP server asking the user, not the
  agent asking)
- a file, image, or path picker unless the blocker really is a file choice
- a tool whose description says it is disabled, headless-unsafe with no
  alternate UI, or not for clarifying requirements

If several candidates remain, prefer the one that, according to its live
schema:

1. Is permitted for these questions in the current mode and **waits for
   actual answers**, since this workflow gathers blockers before work
2. Accepts a **list of questions in one call**
3. Renders **selectable option labels**
4. Supports **multi-select** when the logical set needs it
5. Is **owned by the harness** rather than an unrelated MCP server

If no candidate remains, go to [§7 Fallback](#7-fallback-textual-questionnaire).

## 4. Disabled / unavailable

If §2 item 5 applies (no user-facing UI), stop. Return the logical question
set to the parent. Do not emit §7 in this transcript.

Otherwise treat the native channel as **disabled or missing** only when one
of these is true:

- No candidate survived §3
- The prompt, feature flag, or harness config in context says the question
  tool is off
- The native call returns unavailable, disabled, not permitted, or
  non-interactive
- The selected native tool cannot preserve the complete logical set's
  semantics (for example, Codex has no native multi-select); use one
  complete text fallback rather than silently changing a multi-select into
  a single-select

A schema validation error is **not** unavailability. Repair the payload and
retry native once.

A timeout while waiting for the user is **not** unavailability. Keep waiting
or follow the harness's timeout contract.

Headless / CI / ACP sessions: if the question tool is still listed, try it.
Fall back only if the call fails as non-interactive.

## 5. Map logical questions onto the live schema

Validate the logical set with
`scripts/validate-question-set.py validate FILE` before calling native.
Build the payload from the live schema, not from memory. Typical mappings:

| Logical kind | How to encode |
| --- | --- |
| `single-select` | One question, two or more options, multi-select off |
| `multi-select` | Same, multi-select on; phrase as "which of these apply?" |
| `confirm` | Two options (`Yes` / `No`, or `Proceed (Recommended)` / `Stop`) |
| `free-text` | Native string field if the schema has one; otherwise rely on the harness's automatic `Other` / custom-input row; if neither exists, add a last option `I'll provide a custom value` and, after they pick it, ask that one item as a follow-up **native** question or, only if native cannot take free text at all, as one textual line |
| recommended default | First option; append `(Recommended)` to the label; describe the consequence in the option description |
| required | No skip option |
| optional | First option is `Use recommended default (Recommended)` or an equivalent skip-to-default |

Rules that survive most schemas:

- Put the recommended option first.
- Do not add an `Other` option yourself when the harness already injects one.
- Keep option labels short (about 1–5 words). Put trade-offs in
  `description` (or the schema's equivalent).
- Use `preview` / mockup fields only for single-select comparisons the user
  needs to see (layouts, snippets). Skip them for preference questions.
- Respect live min/max counts for questions and options. If the tool caps
  questions per call, split into consecutive **native** batches. Do not dump
  the overflow as markdown.
- If the tool allows only one question per call, issue consecutive native
  calls for the remaining blockers. Still do not drip unpredicted extra
  questions.
- If options exceed the cap, keep the recommended choice, the strongest
  alternatives, and a custom/other path. Drop the lowest-impact options.
- Never put a destructive, privileged, or production-impacting action in
  the recommended option.
- Use the matching renderer only after generic validation:
  `render-native --target grok FILE` for Grok,
  `render-native --target codex FILE` for Codex `request_user_input`, and
  manual mapping from the live schema for other tools, including
  `request_user_input_async`. Plain `render-native` remains Grok for
  compatibility. A harness identity does not imply identical tool schemas.
- Codex `request_user_input` accepts at most 3 questions. It has no
  multi-select field; its automatic `Other` row supports free text. IDs are
  snake_case and short headers are required; the renderer converts kebab-case
  IDs and accepts an optional logical `header` of at most 12 characters.

Do not also paste the questionnaire as assistant markdown in the same turn
as a native call. One sentence of status is enough, for example: "Opening
the harness question card with N blockers."

## 6. Interpret answers

Distinguish delivery from answers using the live tool contract:

- A call that waits for user input returns answers; interpret those below.
- An asynchronous receipt such as `accepted: true` only confirms delivery.
  Keep the question interaction available until the user answers, explicitly
  accepts defaults, or cancels. Do not start answer-dependent work.
- If ending the turn closes unanswered cards, keep the turn active with the
  harness's supported input-aware wait/yield tool. Use bounded waits and
  check for incoming answers after each return; elapsed time or a preselected
  option is not an answer, dismissal, or acceptance of defaults. Do not emit
  a final response while such a card remains unresolved.
- Ending the turn to await a later reply is valid only when the live harness
  contract preserves answerable cards across turns. If a turn-scoped channel
  has no supported way to wait, it cannot support this upfront workflow;
  use another permitted native channel or treat it as non-interactive for
  §4. Do not change modes or enable tools to bypass session restrictions.

After actual answers or an explicit dismissal arrive:

- Map answers back onto the logical question ids.
- Multi-select values may arrive as a list or as a comma-separated string.
- Custom/`Other` text is a first-class answer.
- Empty, skipped, or dismissed optional answers take the recorded default.
- Empty required answers: if a safe default exists, use it and say so;
  otherwise ask that one remaining blocker again through the same native
  channel.

Then proceed with the work.

## 7. Fallback textual questionnaire

Use this format **only** after §4 says the native channel is missing or
disabled.

```md
Clarification needed before I start.

Native interactive questions are unavailable in this session
(<missing | disabled | non-interactive>), so this is the text fallback.

### Required
1. [Question]
   - Kind: single-select | multi-select | confirm | free-text
   - Options: [A] … | [B] … | [C] …
   - Default: [safe or reasonable default]

2. [Question]
   - Kind: …
   - Options: …
   - Default: …

### Optional
3. [Question]
   - Kind: …
   - Options: …
   - Default: [reasonable default]

If you want me to proceed with the defaults, reply: "use defaults".
```

Keep the same logical set, kinds, options, and defaults that would have gone
to the native tool. Number every question. Mark required only when the item
is a true blocker.

## 8. Known signatures (hints only)

These are **fast paths**. Verify against the live schema. Unknown harnesses
use §2–§5 unchanged. Do not treat this table as exclusive or complete.

| Identity cue in this session | Typical tool name | What to expect (verify live) |
| --- | --- | --- |
| Grok / xAI / Grok Build | `ask_user_question` | `questions[]` with `question`, `options[{label, description, preview?}]`, `multi_select`. Automatic `Other`. Recommended option first with `(Recommended)`. Preview is single-select only. May be toggled off by `features.ask_user_question` / `GROK_ASK_USER_QUESTION`. |
| Claude Code / Anthropic agent CLI | `AskUserQuestion` | `questions[]` (often 1–4) with `question`, `header`, `options` (often 2–4), `multiSelect`. Automatic `Other`. Recommended option first with `(Recommended)`. Preview may exist for single-select. |
| Codex CLI | `request_user_input` / `request_user_input_async` if offered | Verify mode and policy restrictions. The former waits for answers: 1–3 questions, `id`, short `header`, `question`, `options[{label, description}]`. The latter returns a delivery receipt: `questions[{title, options?: string[]}]`; map manually, include needed trade-offs in option strings, and omit options for free text. Both offer custom input and lack multi-select. Prefer the permitted answer-waiting tool; for async follow §6 because turn completion can close TUI cards. If neither is usable or multi-select is required, use §7. |
| Cursor / other IDEs | `AskQuestion` or similar if offered | Inspect the live schema. If nothing selectable is offered, go to §7. |

Name patterns in §3 still apply when the product is not in this table.

## 9. Failure handling

| Event | Action |
| --- | --- |
| Native call returns answers | Apply §6; start work once blockers are resolved |
| Schema / parameter error | Repair from live schema; retry native once |
| Tool missing, disabled, or non-interactive | §7 fallback |
| User dismisses the card / replies `use defaults` | Apply safe recommended defaults; start work |
| New blocker appears after answers | One additional native round (or §7 if still no native channel) |
| Subagent / no user UI | Return the logical set to the parent; do not fall back as if this transcript were the user |
