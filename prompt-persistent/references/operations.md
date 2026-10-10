# Local operations and preservation ledger

The six specialized generators own **create, project/render, convert, and migrate** for their surfaces. `prompt-persistent` additionally owns the already-declared structural `consolidate` operation for persistent instructions. `prompt-enhance` owns semantic transformation of an existing prompt. `prompt-linter` owns audit-only diagnosis. Generator-local checks of newly created, projected, converted, or migrated work remain part of that generator workflow. No routing result or sibling installation is required for a Skill's core responsibility.

## Create
Read the trusted request. Infer the explicit surface locally. Record the objective, target harness, scope, activation, authority, input trust, output, and permissions. Ask only for information that blocks a safe native result; otherwise state assumptions and produce a bounded draft. Do not grant filesystem, shell, network, or tool access by default. Obtain actual repository evidence for commands and paths. Use the selected host adapter only after semantic requirements are clear.

## Enhance
Semantic improvement of an existing prompt belongs to `prompt-enhance`, not a surface generator. Improvement includes optimize, refine, strengthen, correct, fix, polish, harden, or rewrite for reliability while preserving the prompt's objective and surface. A generator must not silently treat an enhancement request as permission to redesign or replace the artifact. The enhancer may use a source surface's schema or adapter as evidence when available, but it does not acquire that surface's generation ownership.

## Audit
Audit-only review belongs to `prompt-linter`. Return findings with severity, exact evidence, affected capability, and minimal correction advice. Do not silently rewrite an audit-only request. A linter may identify the source adapter and reconstruct a provisional semantic spec with uncertainty, but the final improved artifact is not its deliverable unless the operation is explicitly changed to enhancement.

## Consolidate persistent instructions
`consolidate` is structural preservation work owned only by `prompt-persistent`: combine, reorganize, compact, deduplicate, or unify existing persistent instructions while preserving intent, scope, restrictions, authority boundaries, and semantic coverage. Build a source-to-destination coverage ledger before rewriting so every material rule is retained, merged with an equivalent rule, or explicitly accounted for. A request to improve effectiveness, reliability, precision, behavior, or another substantive property is semantic enhancement and belongs to `prompt-enhance`. A bare prompt-focused `refactor` remains the legacy alias for enhancement unless the request explicitly limits the work to structural consolidation with no semantic modification.

## Convert and migrate
Decode source host metadata into semantics before selecting the target representation. Build a capability ledger: capability, source evidence, target support level, transformation, loss, and approval. A missing capability is not an invitation to delete it. Required unsupported capabilities block emission. Optional losses need explicit acceptance and remain labelled lossy afterward. Do not infer acceptance from the operation name.

Keep source native payloads in a migration report, not in new privileged instructions. Emit a separate binding for target filenames, metadata, and variable tokens. Preserve meaningful scope and activation: manual actions are not model-selected by default. Host migration must never widen permissions automatically.

## Compound operations
Keep distinct phases explicit. If a request combines migration with semantic improvement, preserve an intermediate artifact or ledger so migration loss and enhancement changes can be reviewed separately. Do not make a sibling Skill a hidden runtime dependency.

## Legacy compatibility
Legacy `optimize` and prompt-focused `refactor` route intents are canonicalized to `enhance` by the router. Machine-readable legacy specs may still contain those operation strings for compatibility, but surface generators reject them as semantic-transformation ownership when asked to render or validate through their CLI.
