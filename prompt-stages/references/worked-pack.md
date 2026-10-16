# Worked compact pack

This fictional pack illustrates a complete serial plan. No task or check below has been executed. If deliberately used as a practice job, save the content from Master prompt onward as `execution-pack.md` in an authorized workspace. The pack root is the directory containing that file; all paths below resolve from it. Confirm that the listed output paths are unused before writing. This example supplies no authority outside that root.

## Master prompt

Execute the job in this pack at plan revision 1. Read Outcome and authority, Source revision 1, Plan, and Status and recovery. Act as the sole coordinator and run one task at a time in dependency order. Obey current host and workspace instructions. Confirm the required read/write authorization before execution; if missing, record a blocker and stop dependent work.

Before each assignment, verify its input revisions, predecessor evidence, and exclusive write ownership. Record the owner, attempt, and generation in Status and recovery; use a new attempt identifier for each retry. The worker changes only its declared outputs and checkpoint; the coordinator alone updates this pack. Reconcile reports and record actual check outcomes before advancing. No worker dispatch is required: a new session may take the next ready assignment from this file.

## Outcome and authority

Produce `deliverable/summary.md` from the embedded source. R1: preserve both names and counts exactly. R2: show their sum, 5, with a source locator. No network, external messages, deployment, or modification of preexisting user files is part of the job. Output paths must be unused or already owned by this practice job. Required writes are limited to this pack, `deliverable/`, and `work/`; the receiving session must confirm that these are authorized. Human acceptance is not required by this fictional contract; actual governing gates still apply.

## Source revision 1

The following table is the complete authoritative input for this example. Its identity is `execution-pack.md#source-revision-1`, revision 1; no external attachment is needed.

| Name | Count |
| --- | --- |
| Alpha | 2 |
| Beta | 3 |

## Plan

Use serial sessions because T2 consumes T1 and T3 checks the assembled result. The read packet fits this small pack plus two outputs; no fixed context capacity is assumed. There are three materialized tasks and no provisional branches. The seams are reversible local document writes with fixed input, so direct content inspection is sufficient. The T3 reviewer owns final verification and the coordinator owns promotion; producer completion alone cannot close the job.

| Task | Requirements / result | Inputs | Predecessors | Writes | Consumer |
| --- | --- | --- | --- | --- | --- |
| T1 | R1 / normalized table | Source revision 1 | None | `work/table.md`, `work/t1-checkpoint.md` | T2, T3 |
| T2 | R1, R2 / assembled summary | T1 output revision 1 and source revision 1 | T1 with passing evidence | `deliverable/summary.md`, `work/t2-checkpoint.md` | T3 |
| T3 | R1, R2 / final verification record | Source revision 1, T1 and T2 current outputs | T1, T2 with passing evidence | `work/final-review.md`, `work/t3-checkpoint.md` | Coordinator |

## Task T1

Read Master prompt, Outcome and authority, Source revision 1, Plan, and Status and recovery in this pack. Verify your coordinator-recorded T1 owner, attempt, and generation. Copy the two source rows into `work/table.md`, retaining names, order, integer values, and the source locator. Inspect that the resulting table contains exactly Alpha = 2 and Beta = 3 with no additional rows. Record the actual comparison and output revision in `work/t1-checkpoint.md`. Return assignment identity, output path/revision, check outcome, issues, and the next action: coordinator reconciliation before T2.

## Task T2

Read Master prompt, Outcome and authority, Source revision 1, Plan, Status and recovery, and the passing current T1 checkpoint. Verify your T2 assignment and that `work/table.md` matches T1's recorded output. Write `deliverable/summary.md` with both rows, a total of 5, and a citation to `execution-pack.md#source-revision-1`, revision 1. Compare both rows against source revision 1 and recompute 2 + 3. Record actual outcomes and the summary revision in `work/t2-checkpoint.md`. Return assignment identity, artifacts, evidence, issues, and the next action: coordinator reconciliation before T3.

## Task T3

Read Master prompt, Outcome and authority, Source revision 1, Plan, Status and recovery, both predecessor checkpoints, and both current outputs. Verify your T3 assignment and consumed revisions. Compare the assembled summary with the source independently: exactly the two original names/counts, total 5, and the revision-specific source locator. Write `work/final-review.md` with one result per requirement, consumed output revisions, and any missing or conflicting content; checkpoint at `work/t3-checkpoint.md`. Return the evidence and actual outcome. Do not edit a producer's output: return defects to its owner and require revalidation of affected successors.

## Status and recovery

Initial state: T1, T2, T3 are `planned`; all evidence is `not-run`; no assignments or execution claims exist. The coordinator records subsequent owner/attempt/generation, input/output revisions, status, evidence locator, issues, and exact next action here as attributed events. Preserve earlier events and failed checks. A worker report is evidence for reconciliation, not authority to schedule its successor.

At every stop, write the assigned checkpoint with actual input revisions, partial outputs, completed steps, checks, issues, and next action. Missing inputs or authority block affected work. On interruption, the coordinator confirms the old writer stopped, inspects partial state, and records recovery before assigning a new attempt. Reject reports from revoked generations. Reuse an intact current output after verifying it rather than blindly recreating it. A changed source or producer output marks its consumers stale and blocks promotion until rechecked. Keep one writer per resource; if termination cannot be established, do not reassign writes.

Allow at most two reversible local repairs per unchanged check; no paid or external effects are authorized. Record each failure and repair; reassignment retains the count. Escalate an exhausted bound or contradictory source to the caller. Record issues here with affected requirement/tasks, evidence, owner, needed decision, and closure check. There are no unresolved issues at initialization; that is not a claim of passing checks.

## Coverage and closure

| Requirement | Producer / integration | Final evidence | Initial disposition |
| --- | --- | --- | --- |
| R1 | T1 table, T2 summary | T3 row comparison in `work/final-review.md` | not-run |
| R2 | T2 sum and source citation | T3 recomputation and locator inspection in `work/final-review.md` | not-run |

Close only after T3 supplies passing evidence for both requirements on the current assembled summary, no blocking issue remains, all governing gates are satisfied, and the coordinator records the final output identity and resume location. Before execution, the next entry point is Master prompt followed by Task T1; no check has passed merely because this pack exists.
