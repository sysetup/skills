# Verification and Performance Evidence

## Correctness ladder

Use the strongest proportionate combination available:

1. **Reasoning:** contract, invariants, termination, type/ownership model, numerical bounds.
2. **Examples:** representative concrete cases for fast sanity checking.
3. **Boundary tests:** empty, singleton, maximum/minimum, duplicates, degenerate shapes, invalid inputs.
4. **Property/invariant tests:** statements that must hold across many generated inputs.
5. **Differential tests:** compare optimized code against a simpler trusted implementation for many inputs.
6. **Static analysis/type checking:** detect classes of defects without execution.
7. **Dynamic analysis:** sanitizers, race detectors, memory tools, undefined-behavior checks.
8. **Fuzzing:** parsers, protocols, stateful interfaces, security-sensitive input handling, and other broad input spaces.
9. **Formal proof/model checking:** use when the risk, tractability, or contract warrants it.

No single rung replaces all others.

## C/C++ verification defaults

When tools are available, compile with strict diagnostics appropriate to the project and use sanitizers on test runs. Typical development checks include AddressSanitizer and UndefinedBehaviorSanitizer; use ThreadSanitizer for concurrent code when supported.

Do not prescribe compiler flags blindly when they conflict with project policy, platform support, ABI, or performance instrumentation. Record the exact build mode used for verification.

## Reference implementation pattern

For a sophisticated optimized algorithm, retain or construct a simple implementation when feasible and compare outputs over randomized small instances.

This pattern is powerful because the slow reference can be easy to reason about while the optimized version can be stress-tested automatically. Limit generated sizes so the baseline remains tractable.

## Performance claim classes

Label claims accurately:

- **Proved asymptotic improvement:** supported by complexity analysis.
- **Proved operation-bound improvement:** supported by a finite mathematical bound under stated assumptions.
- **Measured improvement:** supported by benchmark/profile data on a stated environment/workload.
- **Expected improvement:** plausible from architecture or workload reasoning but not measured; present as a hypothesis.

Never turn an expected improvement into a measured claim.

## Benchmark design

For consequential performance work:

1. Define the decision the benchmark must answer.
2. Preserve a baseline implementation/build.
3. Use release/optimized builds unless debugging behavior itself is under study.
4. Use representative input sizes and distributions, including stressful shapes.
5. Control or record hardware, OS, compiler/runtime, build flags, core/thread count, and relevant environment.
6. Separate setup from the operation under test when setup is not part of production cost.
7. Warm up JIT/runtime/cache effects when the platform requires it; for native code, account for cache state if relevant.
8. Run enough repetitions to characterize variability.
9. Report a distribution or robust summary, not only the best run.
10. Measure memory/allocation/I/O/contention when those resources are part of the optimization target.
11. Profile to attribute the improvement to the intended bottleneck.
12. Reject benchmark changes that alter semantics or input work unfairly.

## Microbenchmark warning

A microbenchmark can isolate a mechanism but cannot prove end-to-end benefit. Confirm important local wins in the real workload or a realistic integration benchmark.

Compiler dead-code elimination, constant folding, unrealistic hot-cache data, and missing synchronization/I/O can invalidate a microbenchmark. Ensure the computed result is observably consumed and the benchmark performs production-equivalent work.

## Testing evidence

Controlled experiments have shown that different defect-detection techniques find different fault classes and that effectiveness depends on program and participant context. Use this as a reason to diversify verification, not as a universal ranking of testing methods.

Mutation testing can be used to assess whether a test suite detects injected faults, but it has computational cost and equivalent-mutant limitations. Apply it selectively when the assurance gain justifies the cost.

## Review evidence

Independent code reading/review is a distinct defect-detection mechanism. Historical controlled experiments and modern observational studies associate review participation/coverage with software quality. Treat observational associations as non-causal, but use review as a complementary verification layer for nontrivial or high-risk changes.
