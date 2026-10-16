# Execution pack

Produce prompts that tell each new session what to read, what it may change, how to check its result, and how that result enters the final deliverable.

## Bind the outcome and evidence

Read the trusted request and authorized sources. Establish the final observable result, material requirements, exclusions, settled decisions, writable boundary, actual permissions, and acceptance conditions. Distinguish observations, reported facts, assumptions, and decisions.

Investigate actual inputs, interfaces, dependencies, checks, and failure modes before partitioning. Read [decomposition](decomposition.md) to select task boundaries, context size, and execution strategy. Verify missing version-sensitive facts with current primary documentation; record only evidence that changes a task, interface, permission, or check. Keep sensitive data out of external queries and treat retrieved text as evidence.

Ask material blocking questions together. A topic without an observable outcome needs a bounded clarification or research task before production planning. If one branch is unresolved, continue only branches whose scope, authority, and interfaces remain stable. Honor settled decisions unless concrete evidence contradicts a premise.

## Design integration before splitting work

Work backward from final acceptance to stage increments, integration seams, and leaf tasks. Give each output revision one producer and each shared artifact one integrator. Include research, review, assembly, and final verification in the dependency graph.

Choose serial, parallel, or hybrid execution from actual coupling, resource limits, write conflicts, and integration cost. Apply context sizing to integrators as well as workers. Parallel work requires authorized capacity and conflict-free reads and writes; otherwise schedule fresh sessions serially.

Map material requirements to task outputs and final checks. Expand known tasks into executable prompts. Keep genuinely uncertain future branches provisional, with a planning task and expansion condition; a roadmap label is not a runnable task.

## Build a proportional execution pack

Read [execution contracts](contracts.md) for task fields, integration controls, and whole-job closure. Read [continuity](continuity.md) for status, scheduling, checkpoints, stale inputs, retries, and external-effect recovery.

For a small job, use **one Markdown file** with stable headings for the source/outcome and authority, plan and dependencies, task prompts, status/evidence, issues/decisions/acceptance, and final coverage. Point each task to the exact headings it needs. Keep outputs at explicit authorized paths. Use the [compact-first scaffold](../assets/execution-pack.md); do not create separate records merely to fill a layout.

For larger jobs, split those sections into indexed files at a known pack root. Return the pack inline if writes are unavailable, explaining how to save and resume it. Never rely on the planning conversation as the only source.

Read the [worked compact pack](worked-pack.md) when a concrete serial plan, embedded input, revision mapping, or recovery example would help. Adapt its method to inspected job evidence; its sample data and authority do not apply to the user's job.

Include a master coordinator prompt and a directly executable prompt for every materialized task and integration. Each task states outcome, minimal input packet and revision, predecessors, authority, writes, output and consumer, checks, stop conditions, return evidence, and checkpoint/recovery destination.

Choose controls at each integration seam from consequence, reversibility, uncertainty, and available evidence. Honor user-required gates and already-granted authorization; quality review and permission to act are distinct. Record actual human decisions with attribution rather than inventing acceptance.

## Walk through and deliver

Trace a fresh worker start, successful return, interrupted resume, stale input, failed check, reassignment, and final integration against the generated pack. Check that dependencies exist and are acyclic, ownership is unambiguous, references resolve, and materialized prompts have no empty placeholders.

Verify that failed, stale, or inconclusive outputs cannot be promoted, the coordinator has a recovery route, and the final check covers the assembled outcome. Initialize future execution evidence as `not-run`.

Lead with the master prompt or its location, execution strategy, materialized versus provisional work, next session entry point, and blockers or required gates. Label the walkthrough as manual simulation and the underlying job as unexecuted. Producing the pack does not prove that future workers will obey it.
