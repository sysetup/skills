---
name: workflow-ask
description: >
  Gather all blocking questions in one native harness questionnaire before
  work. Triggers: "ask me questions", "no back-and-forth",
  "gather requirements first". Text fallback only if native UI is missing
  or disabled. Do not use for ordinary ambiguity or "proceed without questions".
version: "1.1.0"
license: MIT
allowed-tools:
  - read
  - python
  - bash
metadata:
  short-description: Native upfront blockers.
  version: "1.1.0"
---

# workflow-ask

On invocation, collect every material blocker in one native questionnaire
before work. Do not paste markdown questions while a native channel exists.
Emit the textual fallback **only** for a missing, disabled, or
non-interactive native channel.

The `read` tool is required to load
[references/question-channel.md](references/question-channel.md) from
`SKILL_ROOT` before asking. The `bash` tool is required to run
`scripts/load-skill.sh` because the load gate is a read-only, least privilege Bash CLI.
The `python` tool is required to run `scripts/validate-question-set.py`
because JSON schema checks cannot be done with read/write.

## Path resolution

```
SKILL_ROOT     = <directory containing this SKILL.md>
REFERENCES_DIR = ${SKILL_ROOT}/references
SCRIPTS_DIR    = ${SKILL_ROOT}/scripts
ASSETS_DIR     = ${SKILL_ROOT}/assets
SCHEMAS_DIR    = ${SKILL_ROOT}/schemas
```

Resolve from `SKILL_ROOT`, never from the process cwd.

Load check: `${SCRIPTS_DIR}/load-skill.sh workflow-ask`
must print `OK: loaded workflow-ask` and exit 0.

Before asking, read `references/question-channel.md`.

## Core rule

Inspect the prompt, attachments, and in-scope read-only context first.
Do not ask for details already present or safely inferred. Ask remaining
blockers together in one native questionnaire (one textual message for a
missing native channel). Do not drip questions unless an answer creates
a new unpredicted ambiguity. With no remaining material blocker, invent
nothing and start the work.

Ask only questions that change correctness, safety, or expected output.
Cap the card to the highest-impact blockers; convert the rest to
assumptions or defaults. Do not block on names, wording, spacing, default
sizes, existing layout, or inferred implementation details.

## Safety boundaries

Never request secrets, tokens, passwords, private keys, certificates,
PII, or internal sensitive values. Ask for placeholders, environment
variable names, or secret-manager references.

For destructive, privileged, production, networked, or irreversible
actions, the recommended default is no-op, read-only, dry-run, or
deny-by-default. Dismissed cards and `use defaults` are not approval
for risky work. Urgent requests: ask only items without which the
task cannot be completed safely or correctly.

## Logical question set

Build the inventory internally. Do not show it until a channel is chosen.

| Field | Contract |
| --- | --- |
| `id` | stable slug |
| `text` | one complete question |
| `kind` | `single-select` \| `multi-select` \| `confirm` \| `free-text` |
| `required` | true only for true blockers |
| `options` | distinct choices; first is the recommended default |
| `default` | safe recommended choice |
| `rationale` | why this is a blocker (keep internal) |

Prefer closed choices. Mark the first label with `(Recommended)`.

```
python3 ${SCRIPTS_DIR}/validate-question-set.py validate FILE
python3 ${SCRIPTS_DIR}/validate-question-set.py render-native FILE
python3 ${SCRIPTS_DIR}/validate-question-set.py render-native --target codex FILE
python3 ${SCRIPTS_DIR}/validate-question-set.py render-fallback FILE
```

Empty inventory: `NO_QUESTIONS: proceed` (exit 0). Invalid JSON, unknown
`kind`, missing fields, secrets, missing file, or permission denied:
exit 1 with `FAIL:`. Zero arguments: usage, exit 2. `--help`: exit 0.

Copy `assets/question-set.example.json`. Schema:
`schemas/question-set.schema.json`.

## Delivery protocol

1. Inspect context. Nothing material missing → skip asking.
2. Build the logical set. Run `validate` on it.
3. Discover the native channel via `references/question-channel.md`
   using live tools and live schema. Do not assume a harness from memory.
4. Native present → select the matching `render-native --target`, map,
   call native, one status sentence, follow the response-lifecycle rules in
   `references/question-channel.md` §6 until answers arrive.
5. Native schema error → repair from the live schema and retry once.
6. Fall back to the textual questionnaire in
   `references/question-channel.md` **only** for absent, disabled, or
   non-interactive native. Schema mistakes are not a fallback reason.
7. Apply answers (defaults for unanswered optional items) and start.

## User accepts defaults

Proceed with the stated recommended defaults. Do not ask more questions
unless a new blocker appears. For risky actions, accepting defaults
means the safest bounded behavior, not permission to mutate or bypass
gates.

Treat `use defaults`, a dismissed card, or skipped optional answers as
accepting defaults.

## Trigger examples

Use this skill for: "Ask all your questions first, then implement the
fix."; "No back-and-forth; gather the requirements before starting."

Do not use this skill for: "Proceed with reasonable assumptions.";
"Do not ask questions unless blocked."; routine tasks already answered
by local context.

## Final response

Mention assumptions only for items that materially affected the work.
