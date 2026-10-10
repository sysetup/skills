# Execution pack scaffold

Instantiate the sections below using the inspected task. Replace all angle-bracket
fields in materialized contracts. Keep a provisional branch explicitly identified
in the plan instead of filling it with invented details. Separate sections into
the portable layout in references/contracts.md when the pack would be too large.

## execution-prompt.md — Master coordinator prompt

Execute the defined job using the pack rooted at `<authorized-pack-root>`.
Current envelope: `<path/revision>`. Current plan: `<path/revision>`.
Preserve the outcome and source obligations in that envelope.

Read `<current-index>`, `<issues>`, `<acceptance>` and `<operational-protocol>`.
Reconcile new attempt reports and interrupted assignments before scheduling.
Validate current input/output revisions, predecessor checks, acceptance gates
and permission references. Claim one runnable task or the conflict-free set
allowed by `<capacity-policy>`. Use `<serial/parallel/hybrid procedure>`.

Dispatch the task's concrete prompt with an attempt ID, owner and assignment
generation. When spawning is unavailable, provide the exact next task prompt
for a separate fresh session and checkpoint coordinator state. Workers write
their own reports; you alone update the shared register.

Use `<job-specific state/retry/reassignment/invalidation rules>`.
Schedule `<integration tasks>` with their declared assembly checks. Evaluate
`<whole-job check>` against the original outcome and current coverage evidence.
Record human decisions with attribution; preserve pending gates. Close only when
`<concrete closure rule>` holds. End with a durable checkpoint and next action.

## envelope.md — Bound source and authority

- Job ID / source locator and identity:
- Outcome observable / deliverable location / final check:
- Source obligations with requirement IDs and quoted or exact located spans:
- Exclusions and settled decisions:
- Authorized workspace, tools and effects with actual permission references:
- Acceptance policy / authority / already satisfied gates:
- Derived execution decisions, assumptions and blocking gaps:

## research.md — Evidence-to-decision register

| Question | Source/version/date | Observation | Inference/decision | Uncertainty/owner |
|---|---|---|---|---|

## plan.md — Architecture and executable frontier

- Plan revision / superseded revision:
- Selected strategy / reason / rejected alternative:
- Capacity and context estimates with uncertainty:
- Stage increments, integration seams and final assembly:
- Materialized frontier / provisional stages / expansion tasks and gates:

| Task | Stage/kind | Requirements | Predecessors | Reads | Writes | Output/interface | Owner | Consumer/control | Fit basis |
|---|---|---|---|---|---|---|---|---|---|

| Seam | Obligations | Risk/consequence | Reversibility/uncertainty | Available evidence | Selected control | Owner/rationale | Residual issue/gate |
|---|---|---|---|---|---|---|---|

Carry each selected control into the integration prompt and master readiness
rule. Keep quality review separate from authorization to perform an effect.

## tasks/<task-id>/prompt.md — Fresh-session contract

You are assigned `<task-id>` in `<job-id>`, stage `<stage-id>`, plan `<revision>`.
Work from the explicit pack root `<root>`, subject to current host/workspace
instructions. Your dispatch must supply `<attempt-id/owner/generation>`.

Produce `<one bounded result>` satisfying `<requirement IDs/source spans>`.
Read `<exact minimum input paths/spans/revisions>`. Verify `<predecessor checks
and acceptance gates>` and inspect existing partial state before writing.
Only write `<allowed paths/resources>`. Use `<allowed tools/effects and actual
authorization>`. Leave `<forbidden paths/resources>` to their owners.

Follow `<concrete inspected procedure>`. Output `<artifact/path/format/interface>`
for `<consumer/integrator>`. Verify it using `<observable method/command/rubric>`;
record evidence in `<attempt evidence path>`. Do not promote failed, stale or
inconclusive work. Apply `<bounded retries and issue routing>`.

Checkpoint `<checkpoint path>` before context pressure or a long effect and on
every stop, including success. Record finished work, exact next action, input
identities, touched paths, check outcomes, provisional output, issues, authority
and replay hazards. Use `<rollback/compensation/reconciliation>` for partial work.
Stop on `<specific conditions>` and report `<return fields and destination>`.
Execute this task only; let the coordinator schedule subsequent work.

## register.md — Coordinator-owned events and current index

| Event | Plan/task/attempt | Owner/generation | Prior -> current | Inputs/outputs | Evidence | Reason/supersedes |
|---|---|---|---|---|---|---|

Initialize production evidence as `not-run`. Instantiate the job's state and
scheduling rules here or in an explicitly named generated protocol section.

## issues.md / decisions.md / acceptance.md

| Issue | Affected requirement/task/seam | Evidence | Owner | Blocked dependents | Next action | Disposition/check |
|---|---|---|---|---|---|---|

| Decision | Evidence/assumption | Authority/source | Plan impact | Supersedes |
|---|---|---|---|---|

| Gate | Scope/revision | Required authority | Decision | Actual decision source | Conditions |
|---|---|---|---|---|---|

## coverage.md — Satisfaction and final closure

| Requirement | Producing output | Integration | Final check | Current evidence | Acceptance/gap |
|---|---|---|---|---|---|

Final result identity: `<path/revision/identity>`.
Verification outcome: `<not-run/pass/fail/inconclusive>`.
Human acceptance: `<pending/accept/reject and attributed source>`.
Remaining blockers / next safe session: `<concrete records>`.
