---
name: ops-algorithmic
description: "Design, implement, review, debug, refactor, and optimize algorithms and software with an algorithm-first quality hierarchy: prove semantic correctness, select algorithms and data structures that fit the workload, minimize asymptotic and real resource cost, then maximize clarity, comprehensibility, maintainability, and measured performance. Use for any task that creates or modifies source code, implements algorithms, chooses data structures, designs loops or state transitions, fixes performance, reviews code quality, reduces complexity, or translates requirements into executable software. Apply across programming languages and frameworks. Trigger especially when clean-looking code may conceal a poor algorithmic choice, or when optimization claims require proof, testing, profiling, or benchmarking."
license: MIT
metadata:
  author: "SYSETUP.COM CarlosHRG"
---

# Algorithmic Software Engineering

## Operating principle

Treat source code as the executable expression of an algorithm, not as a substitute for algorithmic quality.

Optimize in this order:

1. Establish the contract and semantic correctness.
2. Select the mathematically and operationally appropriate algorithm and data structures.
3. Minimize dominant time, space, I/O, allocation, communication, synchronization, and data-movement costs under the actual constraints.
4. Express the selected algorithm so a competent maintainer can reconstruct its intent and invariants.
5. Localize change, preserve stable abstractions, and make future modification safe.
6. Tune constants, layout, branches, vectorization, caching, concurrency, or other low-level details only from evidence when they materially matter.

Reject the false trade-off "efficient or readable." First choose the right algorithm; then make that algorithm readable. Accept an asymptotically inferior algorithm only when the bounded workload, lower constants, memory limits, simplicity, determinism, or another explicit constraint makes it the better engineering choice.

## Execute the engineering loop

### 1. Define the computational contract

State before implementation:

- inputs, outputs, semantics, and error behavior;
- maximum and typical sizes;
- input distribution when known;
- latency, throughput, memory, storage, I/O, network, and energy constraints when relevant;
- update/query ratio, graph density, value range, ordering requirements, adversarial exposure, precision requirements, and concurrency model when relevant;
- correctness properties that may not be violated.

If a missing fact changes the algorithmic family, surface the assumption explicitly. Do not hide a material assumption inside code.

### 2. Identify the dominant cost

Model the work before optimizing syntax. Identify what scales with input or load: comparisons, hash operations, allocations, cache misses, disk seeks, network round trips, locks, copies, serialization, database queries, kernel transitions, or other expensive operations.

Distinguish:

- theoretical operation count from measured wall-clock cost;
- worst-case, average/expected, amortized, and best-case bounds;
- latency from throughput;
- CPU work from data movement and I/O;
- one-shot cost from repeated-query or repeated-update cost.

### 3. Generate credible algorithm/data-structure candidates

Consider at least the obvious baseline and a stronger candidate whenever complexity or scale is material. Compare candidates using the problem's actual constraints rather than aesthetic preference.

Load `references/algorithm-selection.md` when choosing among algorithmic families, data structures, preprocessing, memoization, dynamic programming, graph representations, batching, streaming, approximation, or concurrency.

### 4. Select and justify the algorithm

Prefer an improvement in the dominant complexity class or dominant expensive operation over local syntax-level optimization when the workload can reach the regime where that difference matters.

For every nontrivial selection, record:

- required preconditions;
- correctness idea or invariant;
- time complexity with the relevant case qualifier;
- auxiliary and total space complexity;
- important constant-factor or locality considerations;
- failure or degradation modes;
- reason the rejected alternative is inferior for this workload.

Do not claim that a lower Big-O bound automatically means lower runtime for every finite input. Do not claim that two implementations with the same Big-O bound are equivalent in practice. Use measurement when constants, locality, allocation, vectorization, contention, or I/O may decide the result.

### 5. Establish correctness before polishing

For loops, state the invariant when it is not obvious. For recursion, identify the decreasing measure or termination argument. For state machines, enumerate legal transitions and impossible states. For numerical code, analyze overflow, underflow, cancellation, rounding, and units. For concurrent code, identify ownership, synchronization, ordering, race freedom, and progress assumptions.

Use preconditions/postconditions or equivalent assertions where they improve verifiability. Preserve the reasoning in code or documentation when a future edit could silently break it.

Load `references/verification-performance.md` for verification patterns and evidence requirements.

### 6. Implement for human comprehension

Make the implementation reveal the selected algorithm.

- Name entities by domain role and invariant, not by incidental mechanics.
- Prefer explicit control flow when a compact expression is materially easier to misread.
- Keep side effects visible; avoid burying mutation in conditions or argument expressions.
- Keep nesting and decision structure only as complex as the algorithm requires; extract coherent concepts rather than mechanically splitting by line count.
- Use comments for rationale, invariants, non-obvious constraints, numerical reasoning, complexity, external protocol rules, or deliberate trade-offs. Do not narrate syntax.
- Follow the repository's formatter and naming convention. Do not replace an established convention merely because another style is personally preferred.
- Use metrics such as cyclomatic or cognitive complexity as warning signals, not as an oracle for understandability.

Load `references/code-comprehension.md` before making readability/style claims or when refactoring confusing control flow, identifiers, comments, or formatting.

### 7. Engineer maintainability without sacrificing the algorithm

Localize invariants and algorithm-specific assumptions. Separate policy from mechanism when they change for different reasons. Keep stable interfaces independent from replaceable implementation details. Prefer cohesive components and explicit dependencies over hidden global state.

Avoid speculative abstraction. Introduce an abstraction when it removes real duplication of knowledge, stabilizes a boundary, enables testing/substitution, or isolates a volatile decision. Do not add indirection merely to make the design look sophisticated.

Document complexity-sensitive contracts. If callers rely on ordering, stability, amortized behavior, memory ownership, iterator validity, thread safety, or exception guarantees, expose that fact at the interface boundary.

### 8. Verify behavior and performance

Use complementary verification techniques rather than a single metric or happy-path test.

At minimum for nontrivial code:

1. test nominal behavior;
2. test boundaries, empties, singletons, duplicates, extremes, invalid inputs, and overflow/precision cases that apply;
3. test adversarial or worst-shaped inputs when the algorithm has a degradation mode;
4. use a simple reference implementation or invariant/property checks when feasible;
5. compile/lint/type-check and run static or dynamic analyzers available for the language;
6. for C/C++, use sanitizers or equivalent memory/undefined-behavior tooling when available;
7. benchmark only after correctness is established if a performance claim matters.

For optimization, compare against a baseline on representative workloads. Keep environment and inputs comparable. Report enough information to distinguish noise from a meaningful improvement. Profile before low-level tuning.

### 9. Perform a final quality review

Before delivering code, answer these questions:

- Is the contract correct and complete enough for the chosen algorithm?
- Is there a better asymptotic or workload-specific algorithm that was missed?
- Is each data structure justified by access/update/order requirements?
- Can the correctness argument survive edge cases and numeric limits?
- Are worst-case or adversarial behaviors acceptable?
- Does the implementation expose rather than obscure the algorithm?
- Can a maintainer change the code without rediscovering hidden invariants?
- Do tests target the algorithm's actual failure modes?
- Are performance claims proved analytically, measured experimentally, or clearly labeled as hypotheses?

If any answer is no, revise before presenting the solution as high quality.

## Use the evidence hierarchy correctly

Separate four kinds of support:

1. **Mathematical guarantee** — proofs, invariants, asymptotic bounds, amortized analysis, numerical error bounds.
2. **Controlled empirical evidence** — human/program experiments with stated participants and tasks.
3. **Observational evidence** — repositories, defects, changes, production traces, or case studies; treat association as association.
4. **Engineering convention** — standards, style guides, or local practice; useful for consistency but not automatically a causal fact.

Never present a convention as scientifically proven. Never convert a correlation into causation. Never use a source-code metric as a complete proxy for human comprehension.

Load `references/scientific-evidence.md` when the user asks why a rule exists, requests scientific support, or when a recommendation depends on empirical human factors.

## Deliver a decision record with substantive coding work

For algorithmic implementations, optimizations, or reviews, include the relevant subset of:

1. **Contract and assumptions**
2. **Chosen algorithm and data structures**
3. **Why this choice beats credible alternatives for the stated workload**
4. **Correctness argument/invariants**
5. **Time and space complexity**
6. **Implementation**
7. **Verification performed or tests to run**
8. **Performance evidence or benchmark plan when performance is claimed**
9. **Residual risks and trade-offs**

Keep trivial tasks proportionate; do not bury a two-line fix under a formal report. Preserve the hierarchy even when the explanation is short.

## C++ canonical examples

Use `references/cpp-examples.md` for canonical examples showing algorithmic improvement before stylistic improvement, explicit invariants, confusing-versus-clear expressions, preprocessing trade-offs, and measurement-aware choices. The examples use C++20 but the reasoning transfers to other languages.

Run `python3 scripts/verify_cpp_examples.py` after editing those examples when a C++20 compiler is available.

## Reference map

- `references/algorithm-selection.md` — load for algorithm/data-structure selection and optimization trade-offs.
- `references/code-comprehension.md` — load for readability, naming, control-flow clarity, comments, formatting, and metric interpretation.
- `references/verification-performance.md` — load for correctness checks, testing, sanitizers, profiling, and benchmark design.
- `references/scientific-evidence.md` — load for evidence strength, study details, standards, and bibliographic support.
- `references/cpp-examples.md` — load when examples or implementation patterns help explain a decision.
