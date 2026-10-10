# Code Comprehension and Maintainability

## Principle

Make the program's surface structure help a reader reconstruct the algorithm, invariants, and domain intent with minimal avoidable inference.

## Naming

Prefer identifiers that encode stable semantic roles: `remainingCapacity`, `shortestDistance`, `pendingRequests`, `parentIndex`.

Avoid both extremes:

- cryptic abbreviations that force reconstruction of meaning;
- sentence-length identifiers that repeat surrounding context and slow scanning.

Use the domain's established vocabulary consistently. Keep a term mapped to one concept and one concept mapped to one preferred term inside a bounded context.

Empirical work supports descriptive naming for semantic comprehension, while other experimental work shows excessively long identifiers can impose memory/processing cost. Therefore optimize *information value*, not raw identifier length. See `scientific-evidence.md`.

## Control flow

Prefer constructs whose operational meaning is visible without precedence tricks or side-effect tracing.

Avoid, especially in C/C++ when an explicit equivalent is clearer:

- assignments embedded in larger conditions unless idiomatic and unmistakable;
- reliance on obscure operator precedence;
- pre/post-increment mixed with other reads/writes of the same state;
- short-circuit boolean expressions used primarily as control-flow substitutes;
- multiple state mutations inside one expression;
- clever comma/ternary chains that compress decisions.

Research on "atoms of confusion" demonstrates that very small, functionally valid source patterns can significantly increase misunderstanding relative to clarified equivalents. The rule is not "verbose is always better"; the rule is to remove syntax that creates a predictable interpretation trap.

## Nesting and decision structure

Reduce unnecessary nesting by handling exceptional/terminal cases early when that preserves a clear main path. Extract a function when a block represents a named concept with its own contract or invariant.

Do not split functions solely to satisfy an arbitrary line-count or cyclomatic-complexity threshold. Structural metrics correlate imperfectly with actual human understanding; use them to locate review candidates, then inspect semantics and context.

## Comments

Write comments that preserve information unavailable or expensive to reconstruct from syntax:

- why this algorithm/data structure is selected;
- loop or representation invariants;
- non-obvious boundary conventions;
- units and numerical stability reasoning;
- complexity-sensitive behavior;
- external protocol/standard constraints;
- workarounds and the condition that permits their removal.

Delete comments that merely translate each statement into prose. Update or remove stale comments immediately; incorrect documentation is negative information.

## Formatting

Use automated formatting and repository conventions to make structure predictable. Preserve indentation aligned with syntactic blocks.

Do not claim universal scientific superiority for `camelCase` versus `snake_case`, brace placement, or a particular indentation width. A 2023 systematic review found some positive formatting effects but also null, conflicting, and outdated evidence. Consistency and structural visibility are stronger rules than aesthetic dogma.

## Complexity metrics

Use cyclomatic complexity to quantify independent control-flow paths and to identify code that may deserve decomposition/testing attention. Do not equate a single metric value with maintainability or comprehensibility.

Recent empirical work found that models based only on structural code measures, including cognitive complexity, had substantial prediction error for understandability. Human expertise, task, semantics, documentation, and context matter.

## Maintainability mechanisms

Preserve the reasoning that future edits must respect:

- keep invariant-related data and operations close;
- expose complexity guarantees that callers depend on;
- keep policy choices separable from mechanics when they vary independently;
- isolate volatile third-party APIs behind narrow boundaries when change risk justifies it;
- avoid duplicated business rules even when the code text differs;
- design tests around externally meaningful behavior and invariants rather than private implementation trivia;
- prefer the smallest abstraction that removes a real source of change coupling.

## Review questions

Ask a reviewer to explain, without executing the code:

1. What problem does this component solve?
2. What are the main invariants?
3. Why is this algorithm/data structure used?
4. What are its complexity and degradation modes?
5. Which edge cases change control flow?
6. What must remain true after a maintenance edit?

If the code cannot support accurate answers, improve the expression or documentation even if the implementation is functionally correct.
