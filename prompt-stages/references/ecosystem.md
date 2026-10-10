# Prompt ecosystem interoperability

Inspection baseline: 2026-10-05. All 13 installed `prompt-*` skills were inspected,
including `prompt-handoff` and `prompt-style`, which were absent from the session's
available-skill catalog. Availability in a later runtime must be checked there;
these host paths are provenance, not portable dependencies.

`prompt-stages` owns investigation-backed decomposition and durable session
architecture for one defined outcome. General surface generation, enhancement
and audit keep their existing owners. This skill is independently usable.

| Skill | Existing responsibility | Composition |
|---|---|---|
| prompt-task | One-shot/session task prompts | Render a materialized serial task contract |
| prompt-delegation | Bounded worker assignment and return evidence | Render materialized worker contracts after the DAG and ownership are decided |
| prompt-action | Reusable actions and skills | Author/migrate the reusable capability itself, not a job's stage schedule |
| prompt-agent | Agent identity and privileged instruction layers | Only if the user separately requests an agent definition |
| prompt-api | Application/API-bound prompt templates | Optional application binding of a pack; preserve variables and role semantics |
| prompt-persistent | Persistent scoped instructions and consolidation | Job records are data; solution assembly is not persistent-instruction consolidation |
| prompt-enhance | Improve an existing prompt's semantics | Improve a supplied stage prompt when requested; preserve its objective and contracts |
| prompt-linter | Audit without rewriting | Optional independent audit; local pack validation still belongs here |
| prompt-router | Classify and stop | Optional surface classification, never mandatory orchestration |
| prompt-handoff | Explicit conversation continuation compaction | Only for an explicitly requested conversation handoff; task checkpoints use project state |
| prompt-dictamen | Compile the settled technical Dictamen | Use its output as settled input; investigate execution boundaries without reopening decisions |
| prompt-style | Presentation/style transformation | Optional final presentation that preserves IDs, authority and literal contracts |
| prompt-zip | Explicit verified archive delivery | Final packaging only when requested |

If the user asks only to improve or audit an existing prompt, preserve that
operation. Add decomposition only when multi-session architecture is requested
or is part of the actual deliverable. Do not redirect every long prompt here.

## The current router is a closed contract

The inspected `prompt-router/references/catalog.json` has six generator surfaces:
agent, API, delegation, persistent, reusable_action and task. Its
`references/contracts/RouteDecision.schema.json` version 2.1.0 excludes
`prompt-stages` from the handler enum and utility mappings. Its contract rejects
unknown fields. Do not emit `handler=prompt-stages` in that schema, invent a
seventh surface, or append stage-specific fields to RouteDecision/InstructionSpec.

For a new pack, a coordinator/serial session can use the task surface and worker
contracts the delegation surface. Keep the DAG, register and stage architecture
in separate portable artifacts. Creating this SKILL.md supports explicit invocation
and description-based discovery when the host loads it; it does not register a
new router handler or install a host command.

Router integration would require separately scoped catalog, schema, classifier,
validation and tests. Do not modify installed skills while creating a workspace
skill. If a sibling is missing, render the portable contract here and state any
native-format limitation; do not claim an unavailable conversion or tool ran.

## Optional research collaborators

Use workflow-research for a substantial domain investigation; use docs-context7
for available version-specific library documentation. Use workflow-ask when the
user requires upfront questions. Domain skills can determine the underlying
verification method; their scope, authority and fact sources remain separate.
No collaborator is needed merely to schedule known contracts from local evidence.

For bounded specialist research, delegate a question/corpus and expected evidence,
not the entire unbounded job. Actual delegation depends on current permission,
runtime capacity and applicable instructions. Record received evidence before
making a downstream decision.

## Inspection provenance

Installed sources were read under `$HOME/.agents/skills/prompt-*/SKILL.md`.
Additional evidence: prompt-delegation/references/surface.md;
prompt-enhance/references/suite-interoperability.md;
prompt-router/references/contracts.md, catalog.json and
contracts/RouteDecision.schema.json. The creator did not modify these sources.
