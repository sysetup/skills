# Assessment and planning guide

Load this reference when `Outcome` is `assessment` or `plan`, or before beginning a port whose business case, scope, dead-code exclusions, pilot slice, or approval gates are not yet established.

## Go/no-go assessment criteria

A cross-language migration is justified only when the measurable cost or risk of retaining the current language exceeds the real transition and parallel-run overhead. Treat the decision as an engineering and operational thesis rather than a syntax preference.

- **Valid measurable drivers**: Runtime end-of-life, recurring memory or security defect classes, chronic build or runtime performance bottlenecks, or critical maintainability and talent constraints.
- **Disqualifiers requiring deferral or retention**: Technology fashion without baseline metrics, no accountable system owner, or rapidly shifting business requirements in the target module.
- **Parallel-run cost accounting**: Include dual-toolchain CI, cross-language interface maintenance, dual monitoring, and developer context-switching overhead in the estimate.

## Domain-by-domain classification and dead-code pruning

Evaluate each module independently rather than imposing a monolithic all-at-once port.

1. Classify every module in scope:
    - **Migrate**: High pain or value, bounded interfaces, clear parity oracle.
    - **Retain**: Stable, low-change, low-risk code whose port yields negative return.
    - **Retire**: Unused features, dead routes, orphaned helpers, or duplicated subsystems.
    - **Defer**: High-churn or unowned components whose requirements must stabilize first.
1. Prune dead code before mapping or translating. Cross-check static entry points and symbol references against sanitized runtime logs or execution traces to avoid porting unused paths.
1. Choose the pilot slice deliberately: pick a module with visible maintenance value, clear behavior, and minimal external dependencies rather than the riskiest core subsystem.

## Static and runtime discovery

Close the understanding, oversight, and execution gaps before writing rules or estimates.

1. Run static analysis across all authorized repositories and consumers to inventory source files, build manifests, third-party dependencies, symbol graphs, cyclic imports, configuration formats, external protocols, and shared data schemas.
1. Contrast static findings with sanitized runtime traces or representative executions to uncover dynamic dispatch, implicit object shapes, reflection, global state, environment dependencies, and undocumented side effects.
1. Identify explicit ownership for parity verification, acceptance review, deployment, and rollback.

## Architectural mode and micro-freeze discipline

Lock these three governance choices before exiting planning:

| Decision | Options and impact |
| --- | --- |
| `Architecture mode` | Choose `structural-port` (preserve module layout; rulebook acts as type/idiom lookup tables plus gap inventory) or `idiomatic-redesign` (re-architect for target idioms; rulebook acts as a target design document). Never mix both implicitly in the same slice. |
| `Execution scale` | Choose `lightweight` (small self-contained module, single-agent verification loop) or `full-loop` (large/multi-module or production-critical codebase requiring mechanical disk queues, isolated worktrees, adversarial review, and staged rollout). |
| Feature micro-freeze | Freeze complex new business logic in the actively migrating slice, or isolate behavioral parity commits from new-feature commits so regressions remain attributable. |

## Decision gates and mechanical completeness criteria

Place explicit human approval gates where decisions become expensive or irreversible:

1. **Feasibility gate**: Approved baseline metrics, module classification, dead-code exclusions, `Architecture mode`, and `Execution scale`.
1. **Pilot gate**: Observed parity, maintainability, and performance evidence from the low-dependency pilot before authorizing broader fan-out.
1. **Irreversible-boundary gate**: Explicit sign-off before changing public API contracts, wire protocols, persistent storage schemas, production routing, or retiring legacy code.
1. **Mechanical completeness criteria**: Define objective exit checks up front (for example: zero unexplained parity diffs, zero remaining `TODO(port)` or `UNKNOWN` items, zero references to deprecated legacy entry points, security audit clean, and agreed benchmark thresholds met).
