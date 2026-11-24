# Execution loops and multi-agent discipline guide

Load this reference during translation, compilation, smoke testing, and behavioral parity loops. The core principle is to fix the process and rules that produce code rather than hand-patching recurring defects file by file.

## Scale calibration (`lightweight` vs. `full-loop`)

Match operational ceremony to codebase size and risk while keeping mechanical parity and non-self-grading mandatory at every scale.

| Dimension | `lightweight` (small or single-module port) | `full-loop` (large, multi-module, or production-critical port) |
| --- | --- | --- |
| Queue tracking | Ordered slice checklist in workspace or task plan | Mechanical disk-backed queue rebuilt from verified artifacts on disk |
| Concurrency | Single agent in one isolated branch or workspace copy | Authorized parallel workers in isolated `git worktree` checkouts, one writer per file |
| Compiler placement | Run compiler or type-checker on every slice | Fast checkers inside the loop; slow whole-workspace compilers deferred or serialized via one build gate |
| Review | Independent rule-check pass against `RULEBOOK.md` and judge | Separate-context adversarial reviewer(s) citing rulebook rules plus third-reviewer or human tie-breaker |
| Model tiering | Single active model | Lighter/faster models for high-volume mechanical translation and fixes; highest-capability model for rules, gap audits, and adversarial review |

## Mechanical, resumable translation loop

1. **Order by dependencies and complexity**: Start with dependency-free leaf modules (data structures, pure utilities, parsers), then climb the dependency graph from simple to complex. Break or isolate cycles before porting cyclic clusters together.
1. **Drive the queue from disk**: In `full-loop` ports, determine pending work mechanically by checking which target files exist and passed their stage gate on disk. Rebuilding the queue from workspace state makes long migrations resumable after interruption without trusting chat history.
1. **Keep batches small and reversible**: Limit each batch to reviewable, cohesive units. Record each verified revision so any regression has a clean rollback point.
1. **Flag uncertainty instead of improvising**: Instruct translators to mark unclear idioms, missing contracts, or edge cases with `TODO(port): <reason>` and log an `UNKNOWN` item in the gap inventory so downstream compile and review passes resolve them systematically.
1. **Isolate parallel workspaces**: When parallel delegation is authorized, assign disjoint slices in separate branches or `git worktree` directories. Never let concurrent workers run `git stash`, `git reset`, or overlapping writes in a shared working tree.

## Compiler placement and build serialization

Decide where compilation sits based on toolchain latency:

- **Fast incremental type-checkers or compilers** (seconds per unit, such as TypeScript `tsc` or Python type-checks): Run inside each translation loop so syntax and contract errors fail immediately.
- **Slow whole-workspace compilers** (minutes per build, such as large Rust `cargo` or C++ builds): Defer whole-workspace compilation until after a translation batch finishes, or route rebuilds through a single serialized build gate so concurrent workers do not contend on build locks and caches.

## Compile, smoke-test, and behavioral parity loops

Run the same mechanical loop structure across compile, smoke-test, and full behavioral parity stages:

1. **Invoke the mechanical referee once per pass**: Run the compiler, smoke-test suite, or sharded parity suite to produce an objective, deterministic failure list.
1. **Cluster failures by root cause**: Group compiler errors, runtime crashes, and parity diffs by underlying pattern (for example: cyclic imports, shared type-signature mismatch, error-code mapping, numeric edge case) instead of attacking isolated symptoms in random order.
1. **Escalate recurring patterns upstream**:
    - Isolated single-file issue -> assign a bounded fixer pass and re-verify.
    - Same defect repeating across multiple files or tests -> stop fan-out, amend the governing rule in `RULEBOOK.md` (or resolve the `UNKNOWN` entry in the gap inventory), and regenerate or re-check every slice touched by that rule.
1. **Stop on regression**: Never accumulate new batches on top of broken parity. Fix or roll back the regressing batch before continuing.
1. **Expand edge-case coverage when suites are thin**: If inherited tests cover only happy paths, run additional differential scenarios, property-based invariant checks, and adversarial edge-case probes against both the original and target implementations (never relying on green unit tests alone).

## Independent adversarial review and tie-breaking

- **Separate contexts**: Reviewers inspect target diffs against the original source, `RULEBOOK.md`, and `gap-inventory` in an independent context with no sunk-cost bias from implementation.
- **Rule-cited findings**: Require every review finding to cite the violated rulebook rule, gap entry, or observable behavioral discrepancy so violations become concrete queue items rather than vague style debates.
- **Disagreement resolution**: When two independent reviewers disagree or a safety/architecture boundary is contested, escalate to a third reviewer pass or the human owner rather than averaging or silently accepting the weaker check.
- **No self-grading**: An implementer may fix a failing judge check, but it cannot relax, delete, or rewrite judge assertions to make a failing slice pass.
