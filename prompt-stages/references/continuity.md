# Durable state, scheduling and recovery

## Single authority, distributed reports

The coordinator owns the plan, shared register, assignments and acceptance index.
Workers write only their declared outputs and attempt reports/checkpoints.
Integrators own promotion to their declared seam. Human decisions are recorded
by reference to an actual human message or record; an agent can transcribe that
decision with attribution but cannot invent acceptance.

Use a durable event record with: event ID, job/plan revision, task ID, attempt ID,
actor, assignment generation, prior/new status, input/output identities, evidence
locator, timestamp when available, reason and superseded-event link. Append
corrections rather than erasing failed checks. A current summary/index is a
derived view; rebuild it from the latest applicable events after a crash.

A worker checkpoint is a proposed fact until the coordinator reconciles it into
the register. A cold worker may inspect predecessor reports for evidence but
does not treat an unrecorded completion claim as scheduling authority. Keep old
events and read targeted spans through an index so the log need not fill context.

## Separate status from evidence and acceptance

| Task status | Meaning | Next legal action |
|---|---|---|
| planned | Contract exists; prerequisites may be pending | Coordinator computes readiness |
| running | Assigned attempt has exclusive write ownership | That owner works/checkpoints |
| interrupted | Partial work with a continuation point | Reconcile actual state, resume under a new assignment |
| blocked | Missing input, authority, unresolved contradiction or exhausted retry cap | Route named issue to its resolution owner |
| locally-closed | Declared output and exit checks passed on recorded inputs | Review/integration, subject to gates |
| stale | An input or output identity changed; prior evidence no longer establishes currency | Revalidate or recompute affected result |
| superseded | A new plan/task revision replaces this contract | Preserve history; use the replacement IDs |

Evidence outcome: `not-run`, `pass`, `fail`, `inconclusive`. Acceptance decision:
`pending`, `accept`, `reject`, `not-required`, with authority and scope. Task
status does not encode human acceptance. A rejected integration reopens with
the rejection criterion as input; evidence is retained and a new attempt records
the repair. Reuse the task ID for retries; allocate new child IDs for a split or
changed contract and link `supersedes` without recycling IDs.

## Scheduling and exclusive assignment

Compute readiness from the current DAG and current register, not chat memory.
A task is runnable only if its materialized contract is current, inputs exist,
each predecessor is locally-closed with passing evidence for the consumed
revision, required acceptance gates are satisfied, permissions cover the action,
and no blocking issue or conflicting assignment exists.

The coordinator records a claim before dispatch: owner/session, task, attempt,
generation, allowed writes and optional lease policy. With one coordinator,
serial dispatch records suffice. Multiple coordinators require a real atomic
claim/lock or transaction supplied by the host; a Markdown row is not a lock.
If such enforcement is unavailable, retain one coordinator and serialize writes.

A timeout does not prove the prior writer stopped. Before reassignment, confirm
that it has stopped or fence it through an enforced isolated workspace/claim
generation. Reject reports from revoked generations. If neither control is
available, leave the task blocked until exclusive ownership can be established.
Logical IDs and prompt instructions alone cannot stop a stale writer.

## Checkpoint early and on every stop

Persist before a long step, after a meaningful reversible result and before
ending the session. A checkpoint contains: task/attempt/plan revision, observed
status, read input identities, changed paths, finished steps, exact next action,
checks and outcomes, partial-output location, issue IDs, pending authority,
replay hazards and rollback/compensation route. Save a final checkpoint on
success as well as interruption.

A crash may leave `running` with no final checkpoint. A replacement inspects
actual artifacts and the last recorded intent, compares identities, determines
whether partial work is usable and records the recovery decision before writes.
Absence of an error is not passing evidence. Completed output without recorded
checks needs verification, not an automatic rerun or promotion.

## Retry, invalidation and reassignment

| Event | Response |
|---|---|
| Context pressure | Checkpoint while room remains; resume or split unfinished work under a plan revision |
| Missing input / permission | Record issue, owner, required disposition and which dependents are blocked |
| Failed exit check | Preserve evidence; repair inside scope with a bounded retry budget; keep the criterion unchanged |
| Repeated same failure | Escalate to a named specialist or human under existing authority; record diagnostic evidence and next decision |
| Foreign task defect | File a cross-task issue; the owner or authorized integrator repairs it |
| Input identity changed | Mark the consumer stale and traverse affected downstream edges; revalidate until currency is restored |
| Reassignment | Revoke/fence the old claim, inspect partial state, assign new owner/attempt, preserve task identity and issue history |
| Changed outcome | Record scope-change request and stop affected work until disposition; do not call it repartitioning |

Default to two repair attempts per unchanged check unless the job/runtime sets
another bound. The bound limits futile loops; it does not authorize exceeding
budgets or weaken acceptance. Reassignment does not silently reset the failure
count. An issue record states severity, affected requirement/task/seam, evidence,
owner, proposed next action, dependent tasks, disposition and verification to
close it. Independent tasks may continue when no shared risk blocks them.

Capture artifact identity at consumption and promotion. Prefer a version/commit
and locally computed digest when available; otherwise record locator, revision,
size and `digest unavailable`, noting weaker identity. Never fabricate a digest
or call it an authorization signature. Freeze immutable output revisions before
consumers use them; a repaired output invalidates affected consumer evidence.

## External effects are replay hazards

Separate preparation, human authorization where required, and actuation. Before
an external send, publish, deployment or other nonlocal effect, persist an intent
with target reference, authorized scope and idempotency/reconciliation policy.
Afterward persist the observed receipt/outcome. Keep sensitive values in secret
references, not prompts or ledgers.

If a crash leaves the effect's outcome unknown, inspect authoritative external
state through permitted read-only access before retrying. Use a supported
idempotency key only when its actual semantics are verified. Without a safe
reconciliation route, block that effect for a human decision. Checkpoints do not
guarantee exactly-once execution, and rollback of local files cannot undo a send.

## Cold coordinator recovery

Read the envelope, current plan/index, acceptance and issue records; reconcile
finished attempt reports; invalidate changed inputs; audit active claims; compute
the runnable frontier; dispatch at most the authorized capacity. Preserve accepted
current outputs rather than restarting the job. This procedure works from files
alone; host session IDs may help locate evidence but are not the only state.
