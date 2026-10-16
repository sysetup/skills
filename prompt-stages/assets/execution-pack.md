# Execution pack scaffold

Use the compact form for a small job. Fill every materialized field from inspected evidence, with stable task IDs and exact section locators. Remove unused fields rather than adding empty records. Field meanings belong to [execution contracts](../references/contracts.md#leaf-prompt-fields); the forms below provide the output layout. Use the expanded form in [execution contracts](../references/contracts.md#expanded-layout) when volume or separate worker reports justify multiple files.

## Compact pack: execution-pack.md

### Master prompt

Execute the job recorded in this pack at `<authorized-root>/execution-pack.md`, revision `<revision>`. Read the outcome/authority, current plan, status, issues, and acceptance sections. Reconcile interrupted work and attempt reports before scheduling.

Select one ready task or an authorized conflict-free set. Check current input revisions, predecessor evidence, required gates, permissions, and exclusive ownership. Supply each assignment's task ID, owner, attempt, and generation. If worker dispatch is unavailable, return the exact next prompt for a fresh session.

Apply the job's stated retry, invalidation, and recovery rules. Workers write only assigned outputs and reports; the coordinator updates shared state. Schedule integration and final checks. Close only when the assembled result satisfies the original requirements with current evidence and all required gates. Checkpoint before stopping.

### Outcome and authority

- Source locator/revision and material obligations with requirement IDs:
- Final result and observable acceptance criteria:
- Settled decisions, exclusions, constraints, and assumptions:
- Authorized workspace, tools, writes, effects, and permission sources:
- Required human gates, actual decisions, and unresolved blockers:

### Evidence and plan

Record only sources that change execution decisions. Include the selected strategy and rationale, context-fit assumptions, stage increments, integration owners, and provisional branches with expansion tasks.

| Task / kind | Outcome / requirements | Inputs / revisions | Predecessors | Reads / writes | Owner / consumer | Check / gate |
| --- | --- | --- | --- | --- | --- | --- |

For each integration seam, state consequence, reversibility, uncertainty, selected check/review/gate, owner, and rationale.

### Task T1

Replace this sample heading with a stable ID and repeat for each materialized task, including integration and final verification.

Execute `<task-id>` from `<pack-root/path#task-section>`, plan `<revision>`, assignment `<owner/attempt/generation>`. Obey current host/workspace instructions. Produce `<one bounded outcome>` for `<requirements/consumer>`.

Read `<exact input paths or section locators and revisions>`; check `<predecessor evidence/gates>` and existing partial state. Write only `<owned resources>` using `<authorized tools/effects>`. Follow `<procedure grounded in evidence>` and return `<output path/format/interface>`.

Verify using `<observable method or verified command>`. Record actual results at `<evidence locator>`; failed, stale, or inconclusive outputs cannot be promoted. Stop on `<missing input, authority conflict, unsafe effect, retry bound>` and route the issue to `<owner>`.

Checkpoint at `<exact locator>` before context pressure, long effects, and every stop. Include input identities, changed paths, completed steps, checks, partial outputs, issues, next action, and replay hazards. Recover using `<partial-state inspection/rollback/reconciliation>` before retrying. Return `<task/attempt/generation/status/artifacts/evidence/issues/next action>`. Execute only this assignment.

### Status, checkpoints, and evidence

Initialize future work as planned with evidence `not-run`. Distinguish task status, evidence outcome, and human acceptance. Set job-specific bounded retries and stale-input propagation. For reassignment, confirm the old writer has stopped or use enforced fencing before granting writes.

| Task / attempt / generation | Owner | Status | Input / output revisions | Check / outcome / evidence | Checkpoint / next action |
| --- | --- | --- | --- | --- | --- |

### Issues, decisions, and acceptance

Record an issue's evidence, affected tasks, owner, required disposition, and closure check. Record decisions with their authority and scope; do not infer human acceptance. Keep failed checks and superseded decisions available when updating the current state.

### Coverage and closure

| Requirement | Producing output | Integration | Final check / current evidence | Acceptance / gap |
| --- | --- | --- | --- | --- |

Record the assembled result identity, final verification, any required human acceptance, unresolved blockers, and next safe session entry point. A count of completed tasks does not establish whole-job completion.

## Expanded pack

Split the compact sections using the layout in [execution contracts](../references/contracts.md#expanded-layout). Preserve task and requirement IDs, exact locators, ownership, input currency, and the closure rule. Give each worker its own attempt checkpoint/evidence path; retain one writer for the shared register. Inline the chosen scheduling and recovery rules in the delivered pack so execution does not depend on access to this scaffold.
