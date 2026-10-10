# Testing, Refactoring, and Legacy OO Systems

Use this reference for TDD, behavior-preserving refactoring, test doubles, characterization tests, legacy seams, and modernization.

## Table of contents

- [Testing goal](#testing-goal)
- [Contract tests for polymorphism](#contract-tests-for-polymorphism)
- [Test doubles](#test-doubles)
- [Refactoring loop](#refactoring-loop)
- [Legacy-code sequence](#legacy-code-sequence)
- [Common refactorings](#common-refactorings)
- [Rewrite threshold](#rewrite-threshold)

## Testing goal

Tests provide evidence about observable behavior and enable change. Do not optimize for raw unit-test count. Choose test scope based on the risk and boundary being verified.

For OO code, tests should cover:

- invariants and state transitions;
- error/failure behavior;
- polymorphic contract behavior;
- ownership/lifetime-sensitive behavior when externally observable;
- integration boundaries where adapters translate semantics.

## Contract tests for polymorphism

When several implementations promise one interface, define a reusable contract test suite and run it for each implementation.

Conceptual C++ fixture:

```cpp
template <class MakeStore>
void run_key_value_store_contract(MakeStore make_store) {
    auto store = make_store();
    store.put("x", "1");
    assert(store.get("x") == "1");
    store.erase("x");
    assert(!store.get("x"));
}
```

Implementation-specific tests may be additional, but the shared suite checks substitution semantics.

## Test doubles

Use test doubles at meaningful seams:

- external services;
- time/randomness/environment;
- slow or nondeterministic infrastructure;
- architecture ports;
- hard-to-reproduce fault boundaries.

Avoid mocking every collaborator call. Interaction-heavy tests couple to implementation choreography and can block safe refactoring.

Prefer fakes when stateful behavior is easier to understand than call expectation scripts.

## Refactoring loop

Use this control loop:

1. establish passing tests for relevant behavior;
2. make one structural change;
3. compile/static-check;
4. run focused tests;
5. run broader regression tests as risk requires;
6. commit/record a rollback point;
7. repeat.

Separate behavior change from refactoring when possible. Mixing them makes failures harder to diagnose and review.

## Legacy-code sequence

When code lacks tests and has difficult dependencies:

1. identify the behavior that must change;
2. locate a seam where behavior can be observed or dependency replaced;
3. add characterization tests around current behavior, including surprising behavior that consumers may rely on;
4. introduce the smallest dependency-breaking refactor;
5. add/strengthen tests for desired behavior;
6. make the feature/fix;
7. improve deeper structure only where evidence and scope justify it.

Do not start with a broad architecture rewrite merely because the code is unpleasant. First reduce uncertainty.

## Common refactorings

Apply refactorings in response to a specific design pressure:

- Extract Function/Method: isolate coherent behavior or decision.
- Extract Class: separate independent responsibility/invariant.
- Move Function/Method: place behavior near owned information.
- Replace Conditional with Polymorphism: when open-ended behavior variants justify substitution.
- Replace Inheritance with Delegation: when subtype semantics are weak but reuse/composition is useful.
- Introduce Parameter Object / value type: group semantically coherent values and enforce invariants.
- Replace Primitive with Value Object: when units/rules/meaning deserve a type.
- Encapsulate Collection: protect collection invariants and hide representation.
- Introduce seam/adapter: isolate volatile external dependency.

Do not apply a refactoring because a catalog lists it. Tie it to the defect being reduced.

## Rewrite threshold

A rewrite can be justified when constraints make incremental change uneconomic, but require evidence such as:

- unsupported platform or language with unacceptable risk;
- architecture cannot meet mandatory quality/safety constraints;
- behavior can be specified/tested sufficiently to control replacement risk;
- migration/compatibility strategy exists;
- organization can sustain parallel operation or staged cutover.

If those conditions are missing, incremental modernization is usually more controllable than a clean-slate rewrite.
