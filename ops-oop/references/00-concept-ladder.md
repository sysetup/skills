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

### C++ example used throughout

```cpp
#include <cstdint>
#include <stdexcept>

class BankAccount {
public:
    explicit BankAccount(std::int64_t opening_cents)
        : balance_cents_(opening_cents) {
        if (opening_cents < 0) {
            throw std::invalid_argument("negative opening balance");
        }
    }

    void withdraw(std::int64_t cents) {
        if (cents <= 0 || cents > balance_cents_) {
            throw std::invalid_argument("invalid withdrawal");
        }
        balance_cents_ -= cents;
    }

    [[nodiscard]] std::int64_t balance_cents() const noexcept {
        return balance_cents_;
    }

private:
    std::int64_t balance_cents_;
};
```

The important OO fact is not that `BankAccount` is a class. It earns a type boundary because it protects the rule that a balance cannot be created negative and withdrawals cannot violate the allowed state.

## L0: objects, values, identity, and abstraction

### Object

Reason about an object as a runtime participant that combines state, behavior, and a lifetime. The exact implementation may be a class instance, actor, component, proxy, or value object; do not reduce the concept to heap allocation.

### Value

A value is understood by its content rather than persistent identity. Prefer values for quantities, money, coordinates, dates, IDs, configuration, and immutable domain concepts when identity adds no behavior.

```cpp
struct Money {
    std::int64_t cents{};
    friend auto operator<=>(const Money&, const Money&) = default;
};
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

```cpp
struct Rectangle {
    double width;
    double height;
};
```

If negative dimensions are invalid, the public representation permits invalid state.

Stronger design:

```cpp
class Rectangle {
public:
    Rectangle(double width, double height)
        : width_(require_positive(width)),
          height_(require_positive(height)) {}

    [[nodiscard]] double area() const noexcept {
        return width_ * height_;
    }

private:
    static double require_positive(double value) {
        if (value <= 0.0) throw std::invalid_argument("non-positive dimension");
        return value;
    }

    double width_;
    double height_;
};
```

### Encapsulation

Encapsulation is control over valid state and implementation dependencies, not merely `private` fields. Trivial setters for every field often re-expose representation and move invariants to callers.

### Lifetime

In C++, lifecycle design is inseparable from OO design. Determine who owns an object, when it becomes valid, how long borrows may survive, and how resources are released. Use RAII to align resource lifetime with object lifetime.

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

Bad sign: a client receives `Shape&` but immediately checks whether it is a `Circle` to decide what operations are legal.

### Dynamic polymorphism

Use virtual dispatch when implementation must vary at runtime behind a stable contract and independent compilation/deployment or heterogeneous collections justify the cost/complexity.

```cpp
class Compressor {
public:
    virtual ~Compressor() = default;
    virtual void compress(InputView input, OutputSink& output) = 0;
};
```

### Static polymorphism

Use templates/concepts when variation is known at compile time and zero-overhead/generic composition is appropriate.

```cpp
template <class T>
concept Compressor = requires(T c, InputView in, OutputSink& out) {
    c.compress(in, out);
};

template <Compressor C>
void archive(C& compressor, InputView input, OutputSink& output) {
    compressor.compress(input, output);
}
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
| `dynamic_cast` or type switches | substitution/design boundary |
| Repeated constructor/cleanup bugs | ownership + RAII |
| Deep override hierarchy | inheritance contract + composition alternative |
| Many flags select behavior | Strategy/State/policy object |
| Tests break on harmless refactorings | collaboration granularity + mock usage |
| Changes touch many modules | cohesion, dependency direction, architecture boundary |
| Critical-system restriction conflicts with modern C++ idiom | regulated profile + exact standard edition |
