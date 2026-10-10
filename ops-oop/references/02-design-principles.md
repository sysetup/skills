# Object Design Principles and Decision Rules

Use this reference for responsibility allocation, SOLID/GRASP analysis, inheritance/composition decisions, interface design, coupling/cohesion, and substitutability.

## Table of contents

- [Principles are heuristics](#principles-are-heuristics)
- [Cohesion and coupling](#cohesion-and-coupling)
- [SOLID as pressure diagnostics](#solid-as-pressure-diagnostics)
- [GRASP and responsibility-driven design](#grasp-and-responsibility-driven-design)
- [Composition vs inheritance](#composition-vs-inheritance)
- [LSP contract test](#lsp-contract-test)
- [Interface design](#interface-design)
- [Tell, do not merely ask](#tell-do-not-merely-ask)
- [Law of Demeter: use carefully](#law-of-demeter-use-carefully)
- [Design by contract mindset](#design-by-contract-mindset)

## Principles are heuristics

A principle is useful when it predicts a maintenance, correctness, or substitution problem. Do not contort a model to satisfy slogans. Resolve conflicts using domain correctness, explicit quality attributes, and change forces.

## Cohesion and coupling

### Cohesion

A cohesive abstraction has state and operations that serve one understandable purpose. Diagnose low cohesion when a type:

- contains unrelated state clusters used by disjoint methods;
- changes for unrelated stakeholders/requirements;
- mixes domain policy, persistence, presentation, and transport;
- accumulates feature flags for unrelated modes.

### Coupling

Measure semantic coupling, not only dependency count. A dependency is costly when the client relies on unstable representation, call order, shared mutable state, threading assumptions, vendor behavior, or a broad API.

Prefer dependencies on narrow stable contracts at volatility boundaries. Do not create interfaces around every class; an interface is valuable when it enables substitution, architecture direction, independent testing, deployment variation, or binary/API isolation.

## SOLID as pressure diagnostics

### SRP

Ask: "Which independent reasons could force this abstraction to change?" Split only when reasons are genuinely independent. Over-splitting creates navigation and orchestration cost.

### OCP

Identify the variation axis before designing extensibility. A stable plugin/policy boundary can be valuable when variation is expected and semantically coherent. Otherwise, prefer direct code and refactor when evidence appears.

### LSP

Validate behavioral expectations, not inheritance syntax. See the contract test below.

### ISP

Shape interfaces around client roles. Prefer several coherent role interfaces over one broad service interface when different clients depend on disjoint behavior.

### DIP

At architecture boundaries, high-level policy should define the abstraction it needs; volatile infrastructure adapts to that abstraction. Do not invert dependencies merely to add mocking seams inside stable leaf code.

## GRASP and responsibility-driven design

Use these GRASP-style questions:

- **Information Expert:** who already has the data needed for the decision?
- **Creator:** who naturally owns/aggregates/records the created object's lifecycle?
- **Controller:** who should receive a system event without becoming a god object?
- **Low Coupling / High Cohesion:** does responsibility placement reduce knowledge spread?
- **Polymorphism:** does a genuine variation in behavior justify interchangeable implementations?
- **Protected Variations:** which unstable element deserves a stable boundary?
- **Indirection:** is an intermediate abstraction buying meaningful decoupling or merely extra hops?

## Composition vs inheritance

Choose composition by default when the goal is behavior reuse, optional capability, runtime assembly, or independent lifecycle.

Consider inheritance only when all are true:

1. There is a meaningful "is-a" subtype relationship from the client's perspective.
2. The base contract is stable and intentionally extensible.
3. The subtype can preserve base semantics for all supported operations.
4. Base-class protected internals are not required for normal extension.
5. Construction/destruction and copying semantics are safe for polymorphic use.

If one fails, prefer composition, delegation, a policy object, type erasure, `std::variant`, or a template/concept.

## LSP contract test

For each subtype, inspect:

- accepted input domain;
- promised output/postconditions;
- invariants;
- exception/error behavior;
- ownership/lifetime effects;
- performance/timing expectations if contractual;
- thread-safety assumptions if contractual.

Example of a semantic violation:

```cpp
class File {
public:
    virtual ~File() = default;
    virtual void write(std::string_view bytes) = 0;
};

class ReadOnlyFile : public File {
public:
    void write(std::string_view) override {
        throw std::logic_error("read only");
    }
};
```

If `File` promises that `write` is supported, `ReadOnlyFile` is not a valid subtype. Separate readable/writable capabilities or redefine the abstraction.

## Interface design

Good OO interfaces:

- express domain intent rather than representation operations;
- expose the smallest coherent capability clients require;
- make ownership and mutation clear;
- define error semantics;
- avoid temporal coupling where possible;
- avoid leaking implementation types across architecture boundaries.

Prefer:

```cpp
cart.add(product, quantity);
```

over:

```cpp
cart.items().push_back(...); // representation and invariants escape
```

## Tell, do not merely ask

When an object owns the information and rule needed for a decision, ask it to perform the behavior rather than pulling state out and duplicating the rule elsewhere.

Do not apply this mechanically to pure data/value boundaries, serialization DTOs, analytical pipelines, or cases where a functional transformation is clearer.

## Law of Demeter: use carefully

Long navigation chains can reveal structural coupling, but chain length alone is not a defect. Fluent APIs and value transformations may be legitimate. Investigate whether the caller depends on internal object graph structure that should be hidden.

## Design by contract mindset

For important operations, reason explicitly about:

- preconditions: what callers must establish;
- postconditions: what the operation guarantees;
- invariants: what remains true across public operations;
- failure guarantees: what state remains if the operation fails.

C++ does not require a specific contract facility to apply this reasoning. Encode constraints through types, constructors, assertions where appropriate, tests, and API structure.
