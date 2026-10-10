# prompt-style

Installable ChatGPT Skill package. Runtime behavior and the seven predefined styles are defined in `SKILL.md`; ChatGPT UI metadata is in `agents/openai.yaml`; regression scenarios are in `evals/evals.json`.

The skill requires no scripts, external connectors, or runtime dependencies. Session style is conversation state rather than cross-conversation memory, so it must not be represented as persistent across separate chats.
