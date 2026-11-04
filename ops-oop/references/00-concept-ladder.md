# Object-Oriented Concept Ladder

Use this reference when teaching OO concepts, diagnosing conceptual confusion, or deciding how far to escalate an explanation.

## Table of contents

- [Learning rule](#learning-rule)
- [L0: objects, values, identity, and abstraction](#l0-objects-values-identity-and-abstraction)
- [L1: classes, invariants, encapsulation, and lifetime](#l1-classes-invariants-encapsulation-and-lifetime)
- [L2: responsibilities and collaboration](#l2-responsibilities-and-collaboration)
- [L3: subtyping and polymorphism](#l3-subtyping-and-polymorphism)
- [L4: patterns and boundaries](#l4-patterns-and-boundaries)
- [L5: evolution and assurance](#l5-evolution-and-assurance)
- [Diagnostic questions](#diagnostic-questions)

## Learning rule

Teach the concept that removes the current ambiguity, then apply it immediately. Do not dump a taxonomy before the agent has a design decision that needs it.

A useful progression is:

`observable behavior -> invariant -> responsibility -> collaboration -> variation -> architecture -> evolution`

### Language-neutral example used throughout

```text
class BankAccount
    private balance
    construct(opening)
        if opening is not a non-negative integer: fail InvalidBalance
        balance := opening
    withdraw(amount)
        if amount is not a positive integer or amount > balance: fail InvalidWithdrawal
        balance := balance - amount
    balanceAmount() -> balance
invariant: balance is a non-negative integer
failure guarantee: rejected withdrawals leave balance unchanged
```

The important OO fact is not that `BankAccount` is a class. It earns a type boundary because it protects the rule that a balance cannot be created negative and withdrawals cannot violate the allowed state.

## L0: objects, values, identity, and abstraction

### Object

Reason about an object as a runtime participant that combines state, behavior, and a lifetime. The exact implementation may be a class instance, actor, component, proxy, or value object; do not reduce the concept to heap allocation.

### Value

A value is understood by its content rather than persistent identity. Prefer values for quantities, money, coordinates, dates, IDs, configuration, and immutable domain concepts when identity adds no behavior.

```text
value Money
    cents: integer
    currency: CurrencyCode
    equality(other) := cents = other.cents and currency = other.currency
```

### Entity

An entity has continuity of identity across state changes. Model identity explicitly rather than assuming pointer identity equals domain identity.

### Abstraction

An abstraction omits irrelevant detail so clients can reason in domain or policy terms. Good abstractions expose the decisions clients need and hide representation choices that should be independently changeable.

## L1: classes, invariants, encapsulation, and lifetime

### Class

Treat a class as a mechanism for defining a type boundary, not the goal of OO design. A useful class normally owns at least one of these:

- an invariant;
- a resource lifetime;
- a coherent responsibility;
- a polymorphic contract;
- a stable boundary around volatile implementation.

### Invariant

An invariant is a condition that must hold whenever the object is observable in a valid state. Constructors/factories establish it; public operations preserve it.

Weak design:

```text
record Rectangle
    public width
    public height
# Clients can assign invalid dimensions without validation.
```

If negative dimensions are invalid, the public representation permits invalid state.

Stronger design:

```text
class Rectangle
    private width, height
    construct(w, h)
        if either dimension is non-finite or non-positive: fail InvalidDimension
        if w * h is not representable: fail AreaOverflow
        width := w
        height := h
    area() -> width * height
invariant: dimensions and area are finite and positive
```

### Encapsulation

Encapsulation is control over valid state and implementation dependencies, not merely `private` fields. Trivial setters for every field often re-expose representation and move invariants to callers.

### Lifetime

Lifecycle design is part of OO design in every language. Determine who owns an object, when it becomes valid, how long borrows may survive, and how resources are released. Use the target runtime's deterministic cleanup mechanism; garbage collection alone does not define external-resource release.

## L2: responsibilities and collaboration

Ask four questions for every candidate object:

1. What decisions does it own?
2. What information does it know?
3. Which invariant does it protect?
4. With whom must it collaborate to fulfill its responsibility?

Prefer responsibility descriptions written as verbs: `prices an order`, `authorizes a payment`, `selects a retry policy`.

A class whose description is only "stores X" may be a value/data carrier rather than a behavioral object; that can be correct, but it should be intentional.

### Cohesion

High cohesion means operations and state serve one understandable purpose. A type that changes for pricing, persistence, logging, authorization, and UI formatting has several competing responsibilities.

### Coupling

Coupling is unavoidable; manage its direction and semantic weight. Coupling to a stable domain abstraction is cheaper than coupling policy directly to a volatile SDK, database schema, or UI toolkit.

## L3: subtyping and polymorphism

### Subtyping

Use a subtype only when clients of the base contract can use the subtype without knowing which concrete type they received.

Bad sign: a client receives a `Shape` collaborator but immediately checks whether it is a `Circle` to decide what operations are legal.

### Dynamic polymorphism

Use virtual dispatch when implementation must vary at runtime behind a stable contract and independent compilation/deployment or heterogeneous collections justify the cost/complexity.

```text
interface Compressor
    compress(input, output)
    guarantees output decodes to input on success
    declares output state and resource cleanup on failure
```

### Static polymorphism

Use the target language's static contracts or generic mechanisms when variation is known before execution and static composition is appropriate.

```text
algorithm archive(compressor, input, output)
    requires compressor implements the Compressor contract
    compressor.compress(input, output)
# Bind the implementation statically when the target language supports it.
```

Do not choose dynamic dispatch merely because OO is requested; OO reasoning and runtime inheritance are not synonymous.

## L4: patterns and boundaries

Patterns become useful when a recurring design force is visible. Examples:

- replaceable algorithm -> Strategy;
- object creation varies by family/configuration -> Factory;
- incompatible external API -> Adapter;
- state changes alter legal behavior -> State;
- request must be queued/undone/audited -> Command;
- dependent observers need notification -> Observer/Event mechanism.

Architectural boundaries matter more than pattern names. Keep business policy from depending directly on framework, transport, persistence, or device APIs when those details are expected to change independently.

## L5: evolution and assurance

A design is not finished when it compiles. Evaluate:

- how behavior is tested;
- how invariants are observed;
- where seams permit safe replacement;
- whether change requires edits across many unrelated modules;
- whether public contracts are compatible;
- whether standards or safety evidence constrain implementation choices.

For legacy systems, first gain control of behavior, then improve structure. Large rewrites erase evidence and increase simultaneous uncertainty.

## Diagnostic questions

Use these questions to select the next concept level:

| Symptom | Investigate first |
|---|---|
| Invalid combinations of fields | invariant + encapsulation |
| Many classes forward calls without decisions | responsibility allocation |
| Runtime type checks or type switches | substitution/design boundary |
| Repeated constructor/cleanup bugs | ownership + deterministic cleanup |
| Deep override hierarchy | inheritance contract + composition alternative |
| Many flags select behavior | Strategy/State/policy object |
| Tests break on harmless refactorings | collaboration granularity + mock usage |
| Changes touch many modules | cohesion, dependency direction, architecture boundary |
| Critical-system restriction conflicts with language idiom | regulated profile + exact standard edition |
