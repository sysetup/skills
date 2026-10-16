# Bounded assignment

## Bound the work

Identify the delegator, recipient responsibility, one useful outcome, scope, exclusions, and integration consumer. Preserve settled decisions and distinguish verified facts from assumptions the worker must check.

Give exact input locators or include essential content when it will not be accessible. State allowed sources and relevant revisions. Do not imply that the worker receives the parent's history, tools, files, or credentials.

Define permitted reads, writes, tools, approvals, and external effects within the delegator's actual authority. Do not allow re-delegation unless authorized. Bound iterations, time, or cost only when meaningful and supported by the runtime.

## Make ownership explicit

For parallel assignments, allocate each mutable resource to an owner. Include file boundaries, baseline revisions, dependencies, shared processes or services, and the integration owner. Overlapping writes or reads of changing outputs require coordination, isolation, or serial execution.

Specify how the worker reports a defect in another assignment and who resolves conflicts. Do not let workers silently repair each other's resources. A prompt cannot guarantee scheduling, cancellation, locking, or termination of an old writer.

Bind reports to task, attempt, assignment generation, and consumed input revision. If worker B consumes A's output at revision 1 while A prepares revision 2, freeze revision 1 or make B wait; disjoint output files do not remove this read dependency. The parent rejects a revoked attempt's late report and marks dependent evidence stale when a consumed revision changes. Stop affected promotion until the current assignment and inputs are reconciled; independent work may continue.

## Define completion and return evidence

Include the expected output and destination, acceptance criteria, checks grounded in actual project evidence, and the parent's integration step. Ask for:

- Work completed and actual changed artifacts or paths.
- Checks run, observed results, and checks not run with reasons.
- Unresolved issues, assumptions, and the exact next action.

For resumable work, include a checkpoint destination, partial-output handling, and a recovery step before repeating side effects. Stop on missing required inputs, conflicting authority, unsafe effects, failed checks beyond the repair bound, or an unresolved dependency. Return the blocker and evidence instead of guessing success.

## Deliver the assignment

Use a short paragraph for a simple assignment and sections only when they clarify inputs, authority, evidence, or recovery. Remove secrets and unnecessary personal data. Preserve literal interfaces and output requirements when adapting an existing assignment.

If native delegation metadata is requested, verify the host's actual mechanism and format. Otherwise return directly usable text with concise caveats. Walk through worker start, successful return, and a relevant blocked case; label that walkthrough as manual, not executed worker behavior.
