# General prompt-enhancement principles

Use this checklist selectively. A strong enhancement fixes material failure modes without inflating the prompt.

## Intent and scope

- State the objective so the executor can distinguish the requested result from background context.
- Preserve explicit scope, non-goals, business rules, chosen technologies, and authority constraints.
- Separate facts supplied by the user from assumptions or hypotheses.
- Do not convert a request into a different workflow, surface, or architecture for aesthetic consistency.

## Context and inputs

- Define inputs or placeholders only when they are actually needed.
- Distinguish trusted instructions from retrieved or user-supplied data when prompt injection or authority confusion is plausible.
- Remove irrelevant history, repeated instructions, and stale context that can distract execution.
- Do not invent missing product facts, credentials, endpoints, schemas, or source data.

## Instruction hierarchy

- Put governing objectives and hard constraints before subordinate procedure and examples when hierarchy is otherwise ambiguous.
- Resolve direct contradictions only when precedence or evidence establishes the intended rule.
- Keep examples illustrative unless the source explicitly makes them normative.
- Prefer positive operational guidance over repeated prohibitions when equivalent, while retaining necessary safety boundaries.

## Outputs and verification

- Define the output format when ambiguity would materially affect usability.
- Add acceptance criteria only when observable success conditions exist.
- Require evidence, citations, tests, or tool verification when the task depends on factual grounding or executable correctness.
- Distinguish static validation from live behavioral evaluation; never claim measured improvement without executed evidence.

## Tools, permissions, and uncertainty

- State tool permissions and approval boundaries when actions can change external state or require privilege.
- Add missing-input, empty-result, error, and uncertainty behavior when silence would cause unsafe guessing.
- Reject or repair impossible instructions rather than strengthening them.
- Do not grant permissions, credentials, or runtime enforcement by prose alone.

## Portability and target specificity

- Preserve confirmed provider/native syntax exactly when valid.
- Prefer portable semantics where provider-specific syntax is unnecessary.
- When target behavior is unknown or stale, retain a generic valid form and mark the unverified point instead of importing conventions from another platform.
