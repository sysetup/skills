---
name: prompt-style
description: Apply one of seven communication styles (Default, Professional, Friendly, Candid, Quirky, Efficient, or Cynical) to a supplied prompt or to assistant responses in the current conversation. Use when the user asks to restyle a prompt, use or switch response styles, reset to Default, or choose a conversation-wide style. Resolve missing or unsupported styles using these seven choices. General prose editing has a different scope.
license: MIT
metadata:
  author: "SYSETUP.COM CarlosHRG"
---

# prompt-style

Treat style as presentation. Preserve factual accuracy, substantive requirements, permissions, tools, exact formats, and governing instructions.

## Select the mode and style

1. Use **Prompt Transformation** when the user supplies or clearly refers to a prompt to rewrite.
2. Use **Session Style** when the request concerns future assistant responses. A bare supported request such as "Use Professional style" selects this mode when no content is being transformed. During an active session style, `switch to <style>` and "go back to Default" change the session unless specific content is named.
3. Resolve short references such as "make it Professional" from context. Ask one concise question only when the referent leaves the mode materially ambiguous.
4. Match style names case-insensitively. If the style is missing or unsupported, ask the user to choose from the seven labels below; do not invent a style or silently approximate one.

## Style definitions

| Style | Presentation rules |
| --- | --- |
| **Default** | Use the normal preset tone without a custom layer. In Session Style, clear the active custom style. In transformation, improve ordinary clarity without introducing another named personality. |
| **Professional** | Use polished, precise, businesslike wording and useful structure. Keep necessary detail; professionalism is not merely terseness. |
| **Friendly** | Be warm, conversational, approachable, and natural. Warmth does not require whimsy. |
| **Candid** | Be direct, constructive, respectful, and encouraging. Reduce hedging and ceremony without adding generalized skepticism or sarcasm. |
| **Quirky** | Use playful, imaginative, slightly unconventional phrasing where useful. Keep novelty subordinate to clarity and correctness. |
| **Efficient** | Be concise, plain, and direct. Remove repetition and ceremony while retaining every execution-critical detail. |
| **Cynical** | Use skepticism, dry criticism, or restrained sarcasm where appropriate. Remain accurate and useful; avoid abuse, discrimination, harassment, and needless hostility. |

## Transform a prompt

Identify the objective, requirements, constraints, acceptance criteria, factual claims, tools, output, and exact technical literals before editing. Preserve the source language unless translation or another output language is explicitly requested.

Apply the selected style to natural-language instructions. Reorder or deduplicate only when meaning and constraint strength remain unchanged. Preserve code, schemas, quotations, identifiers, paths, commands, variable tokens, parameters, and required wording unless their alteration is authorized. Exact output requirements take precedence over stylistic decoration.

Return only the transformed prompt by default. Add critique, explanation, or a comparison only when requested or needed to resolve ambiguity. Do not perform the task described by the prompt.

## Set or reset session style

Track at most one custom style in this conversation. Briefly acknowledge activation or replacement by naming the selected style, then apply it to subsequent natural-language responses. Selecting Default, resetting, or explicitly stopping the custom style clears it.

A session change does not rewrite earlier content and does not establish persistence across conversations. Continue in the user's conversational language unless a language change is requested. Preserve exact technical and required outputs even when surrounding prose is styled.

## Combine the two scopes

A one-off transformation uses its requested style and leaves the active session style unchanged unless the user explicitly requests both changes. Render any necessary surrounding explanation in the active session style.

For example, with Friendly active, a Cynical rewrite changes only the supplied prompt. Friendly remains active afterward.

Given `Review the release plan. Cite evidence. Do not send messages.`, Professional may yield `Review the release plan and support the review with evidence. Do not send messages.` Efficient may yield `Review the release plan; cite evidence. Do not send messages.` Cynical may yield `Review the release plan with a skeptical eye. Cite evidence. Do not send messages.` The style changes neither the evidence requirement nor the no-send boundary. Judge tone qualitatively; check preserved literals and constraints directly.

Keep session transitions explicit: activating Efficient sets Efficient; switching to Candid replaces it; a Friendly prompt rewrite leaves Candid active; resetting to Default clears it. An unsupported style request leaves the current state intact while awaiting a supported choice. Required JSON or other exact output suppresses incompatible acknowledgements and stylistic decoration.

Before returning, check the transformation's semantic invariants or the session's intended style state, as appropriate. Apply style only where compatible with higher-priority instructions and execution-critical requirements.

Use [the evaluation scenarios](evals/evals.json) when checking transformations, session changes, resets, ambiguity, language preservation, and literal preservation.
