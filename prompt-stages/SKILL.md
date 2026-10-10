---
name: prompt-stages
description: >-
  Investigate a defined task and generate an execution prompt pack that divides
  large work into atomic, traceable, resumable stages for fresh agent sessions.
  Use whenever a job needs short context-sized tasks, session-by-session
  execution, dependency-aware serial or parallel delegation, durable work
  records, reassignment, or planned consolidation into a verified final result,
  even when the user says only "divide this work into phases" or "ejecutar por
  etapas". Own decomposition and continuity architecture; complement prompt-task
  and prompt-delegation. Do not replace ordinary prompt enhancement, audit,
  conversation summarization, or execution of an already bounded task.
compatibility: >-
  Portable Markdown and durable workspace files. Read access to the task and its
  evidence is needed; research tools and sibling skills are optional. Concurrent
  execution requires isolated writes and a coordinator. No framework dependency.
---

# prompt-stages

Produce a directly usable execution architecture, not a list of topics. The
result tells a new agent exactly which bounded unit to execute, what to read,
what it may change, how to verify it, and how its output enters the final result.
Generate the prompts and records; execute the underlying job only under a
separate instruction authorizing execution.

## Ownership and loading

Keep these facts in their designated resources rather than copying the whole
skill into every worker prompt. Resolve resource paths from this SKILL.md.

| Resource | Read when | Owns |
|---|---|---|
| [Decomposition](references/decomposition.md) | Investigating and partitioning any job | Research sufficiency, task sizing, strategy and dependency analysis |
| [Contracts](references/contracts.md) | Writing the execution pack | Required fields, file layout, prompts, integration and release gates |
| [Continuity](references/continuity.md) | Designing records and restart behavior | Status semantics, scheduling, attempts, claims, recovery and reassignment |
| [Ecosystem](references/ecosystem.md) | Composing with another prompt skill or a native host format | Capability boundaries, optional collaborators and router limitations |
| [Pack scaffold](assets/execution-pack.md) | Emitting the deliverable | Fillable output skeleton; instantiate it, do not deliver empty placeholders |

## 1. Bind the outcome before planning

Read the trusted request and authorized local evidence first. Identify the
source of scope, the final observable result, acceptance criteria, exclusions,
settled decisions, available tools, writable boundary, and acceptance authority.
Preserve already-defined work: investigate how to realize it without silently
adding features or reopening settled architecture.

Allocate stable requirement IDs and preserve source locators. Separate source
obligations, derived execution decisions, assumptions, and unresolved gaps.
Existing conceptual proposals inform the design; their proposed gates and
claimed historical approvals do not become current authorization.

Ask all material blockers together before drafting dependent contracts. Infer
safe formatting and naming choices. If the task is only a topic or has
contradictory completion conditions, emit a bounded clarification/research
brief; do not pretend the production plan is ready. An isolated gap may block
only the affected branch when the remaining scope and interfaces are stable.

Default acceptance policy: human acceptance of the partition and final result;
select intermediate controls from the declared seam risk using
[the control policy](references/contracts.md#risk-to-control-decision). Record
the chosen check, review or human gate and its rationale in the plan. This
default is not consent. Honor existing authorization and record which gate it
satisfies; do not ask again for the same approved action.

## 2. Investigate the execution boundary

Read the research procedure in [decomposition](references/decomposition.md).
Inspect actual inputs, interfaces, dependencies, available validation and known
failure modes. Retrieve current primary documentation for version-sensitive
decisions; use an available documentation skill without making it mandatory.

Produce an evidence-to-decision table. Say which questions are answered, which
are uncertain, and which uncertainty affects a cut, permission, check or seam.
Research is sufficient when each runnable task has grounded inputs, an output
contract, a feasible check and a safe integration route. A long bibliography
does not substitute for these conditions.

If investigation itself exceeds one workable session, partition it into bounded
research tasks first. Return their prompts and an explicit provisional roadmap;
leave dependent production contracts unschedulable until their gaps are resolved.
Do not report delegated research as completed before its evidence returns.

## 3. Design assembly before splitting production

Work backward from final acceptance to the required integration seams. Preserve
the source's stage names where meaningful. Give each stage a consumable increment
and an integration owner, then divide it into leaf tasks.

Build a dependency DAG covering production, research, review, integration and
final verification. Map every requirement to producing tasks and final evidence.
Assign one producer to each output revision, and one integrator to each shared
artifact. Include assembly work in the plan so completion does not leave a
large, unbounded merge for the last session.

Apply the context-fit test in [decomposition](references/decomposition.md) to
integration tasks as well as workers. Choose a serial, parallel or hybrid
strategy from actual coupling, write conflicts, verification cost, resource
limits and uncertainty. Explain the rejected alternative. Successive fresh
sessions are useful even when no simultaneous agents are available.

Record all stages in the roadmap. Expand known tasks into executable contracts.
Use rolling-wave detail only for uncertain future branches, with named planning
tasks and explicit expansion gates; a roadmap placeholder is not an executable
task or a claim of complete prompt generation.

## 4. Compile a fresh-session execution pack

Read [contracts](references/contracts.md) and
[continuity](references/continuity.md). Instantiate
[the scaffold](assets/execution-pack.md) inside an authorized directory, or
return the same sections inline when writes are unavailable. A files-only
prompt must have an accessible, explicit pack root. State the weaker durability
of inline-only delivery and give an export/resume route.

Emit:

1. A master execution prompt for a coordinator that can itself be replaced.
2. The bound source, outcome envelope, evidence-backed architecture and DAG.
3. A directly executable prompt/card for every materialized leaf and integration.
4. Durable records for status, evidence, issues, decisions, acceptance and resume.
5. The requirement-to-task-to-final-check coverage map and whole-job closure rule.

A task prompt is a bounded session contract, not an agent identity or a privileged
instruction. Embed its critical scope, interfaces, authority and completion rule;
point to exact durable inputs for detail. Include instructions to resolve the
pack root, validate the current revision, read the minimum packet, execute only
the assigned task, checkpoint and stop. Never refer to "our earlier chat".

Worker prompts are independently usable: neither this skill nor a sibling must
be installed on the execution agent. If useful and available, pass the normalized
task to prompt-task or prompt-delegation for surface rendering. Consult
[ecosystem](references/ecosystem.md) before emitting native metadata or router
contracts. Keep stage-planning data separate from a sibling's closed schema.

## 5. Simulate the lifecycle before delivery

Trace a fresh worker start, a successful close, an interrupted resume, a stale
input, a failed check, a reassignment and the final integration. Perform this
walkthrough against the generated pack, not the planner's memory. Fix missing
inputs, authority gaps, cycles and ambiguous ownership before declaring it ready.

Verify these structural gates:

- Every requirement has a producing task and a final check, or an explicit gap.
- Each materialized task has a bounded packet, predecessor IDs, permitted writes,
  a check with observable evidence, and a resume destination.
- All dependencies exist, the graph is acyclic, and runnable tasks consume only
  current, successfully checked predecessors with satisfied acceptance gates.
- Parallel tasks pass the read/write/resource conflict test. Workers do not
  concurrently rewrite the shared ledger.
- Every stage has a named assembly/check seam; final verification checks the
  assembled result against the original outcome rather than counting tasks.
- Each seam declares its risk, selected control, resolution owner and rationale;
  quality review and permission to perform an action remain distinct decisions.
- Replacement sessions can distinguish proposed, executed, verified and accepted
  facts; interruptions and external effects have explicit recovery procedures.
- User permissions, acceptance policy, uncertainty and unresolved branches are
  explicit. No template placeholder remains in a materialized contract.

Structural checks support architectural consistency; they do not prove that the
workers will obey prompts or that the future solution is correct. Label the
walkthrough as a simulation and the underlying job as not executed.

## Delivery

Lead with the master prompt location, selected strategy, materialized stages and
the next safe session entry point. Name blocking gaps and pending human gates
when present. Deliver the prompt pack and register together. Keep developed
artifacts in the requested artifact language; when unspecified, use English and
converse in the user's language.
