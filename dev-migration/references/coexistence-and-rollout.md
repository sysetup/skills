# Coexistence, final verification, and rollout guide

Load this reference when porting a live or production-serving system incrementally, designing cross-language coexistence boundaries, running final parity and security audits, or gating gradual rollout and legacy retirement.

## Cross-language coexistence patterns

Avoid big-bang cutovers on live systems. Combine incremental replacement patterns only where cross-language operation is actually required:

| Pattern | When to apply | Safety requirements |
| --- | --- | --- |
| Strangler Fig facade or router | Replacing endpoints, CLI subcommands, or service slices while the original stays live | Route specific slices through an explicit facade; keep legacy routes intact until target stability is proven. |
| Anti-Corruption Layer (ACL) | Target code must coexist with legacy data models, wire formats, or C/FFI boundaries | Isolate translation between old and new domain types behind strict typed wrappers so legacy anti-patterns do not leak into target internals. |
| Shadow traffic (parallel execution) | Validating real-world request parity before switching primary traffic | Obtain explicit authorization; sanitize sensitive payloads; strictly isolate or disable external writes and side effects in the shadow target; diff responses and latencies mechanically. |
| Feature flags and canary rollout | Shifting live traffic progressively from original to target | Roll out in small percentages with automated metric thresholds (error rate, latency, memory, parity alerts) and an immediate one-step switchback path. |

## Final parity, security, and performance verification

Clean compilation and green unit tests do not establish production readiness. Before approving cutover, verify every applicable gate against the final candidate revision:

1. **Full behavioral parity**: Run the complete portable test suite, characterization and golden-file checks, differential real-world scenarios, and boundary tests (numeric overflow, floating-point tolerances, null/error handling, encoding, concurrency, and side-effect ordering). Require zero unexplained differences and zero unresolved `TODO(port)` or `UNKNOWN` markers.
1. **Target-language security and safety audit**:
    - Audit FFI seams, memory-safety escape hatches (for example, `unsafe` blocks), pointer lifetimes, and deserialization boundaries.
    - Verify secure defaults (explicit input validation, bounded reads/allocations, strict TLS verification, least privilege, no hardcoded secrets, safe bind addresses).
    - Verify target dependency pinning, lockfile integrity, and vulnerability scans under host standards.
1. **Non-functional benchmarks**: Measure the agreed target metrics (startup time, throughput, tail latency, memory footprint, binary size, compile time) on identical workloads against the recorded baseline revision.

## Rollout gates, switchback, and legacy retirement

All live rollout, traffic switching, and retirement actions require explicit user authorization.

1. **Pre-cutover checklist**: Confirm observability dashboards, structured redacted logs, alerting thresholds, and a tested rollback or switchback procedure to the untouched original baseline.
1. **Threshold-driven progression**: Advance canary or traffic splits only when error, parity, latency, and resource metrics stay within agreed bounds over the required soak window. On any threshold breach or unexpected behavioral divergence, halt progression immediately and switch back.
1. **Controlled retirement**: Keep the legacy path inactive but recoverable through the agreed stabilization window. Delete legacy code, build pipelines, and coexistence adapters only after demonstrated production stability, zero active consumers, and explicit owner approval.
