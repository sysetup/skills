# Domain, Requirements, and Responsibility Modeling

Use this reference when converting requirements or use cases into an OO model, identifying classes/responsibilities, or reviewing a domain model.

## Table of contents

- [Start from behavior](#start-from-behavior)
- [Traceability thread](#traceability-thread)
- [Discover concepts without class-per-noun modeling](#discover-concepts-without-class-per-noun-modeling)
- [Responsibility-driven modeling](#responsibility-driven-modeling)
- [Model state and invariants](#model-state-and-invariants)
- [Boundaries and persistence](#boundaries-and-persistence)
- [UML usage](#uml-usage)
- [Worked example](#worked-example)

## Start from behavior

Begin with scenarios that describe actor intent and externally observable results. For each scenario identify:

- trigger;
- preconditions;
- normal flow;
- domain decisions;
- state changes;
- external interactions;
- failure/alternate flows;
- quality constraints.

Do not create classes yet. First determine which decisions the software must make.

## Traceability thread

Maintain this chain for design-significant behavior:

`stakeholder need -> requirement/use case -> domain rule -> responsibility -> object/module -> operation -> test/evidence`

If the code introduces a policy or constraint with no upstream reason, label it as a design assumption or technical decision instead of pretending it came from requirements.

## Discover concepts without class-per-noun modeling

Nouns are vocabulary candidates, not class mandates. For each candidate concept ask:

1. Does it have behavior or invariant worth protecting?
2. Does it own a lifecycle or identity?
3. Is it a value with domain semantics?
4. Is it only a label/DTO/database row?
5. Does another existing abstraction already own this responsibility?

Avoid creating classes such as `Manager`, `Processor`, or `Helper` before their responsibility can be stated precisely.

## Responsibility-driven modeling

Use CRC-like reasoning (Class/Responsibility/Collaborator) as a lightweight discovery tool.

For each candidate type record:

- **Purpose:** one sentence.
- **Responsibilities:** 1-5 behavioral statements.
- **Knowledge:** information it legitimately owns.
- **Invariants:** conditions it protects.
- **Collaborators:** why each dependency is needed.
- **Lifecycle:** owner and creation/destruction rules.

Prefer the Information Expert heuristic: place behavior near the information required to perform it, unless doing so would create undesirable coupling or violate a stronger boundary.

Use a Controller/Application Service to coordinate a use case when no domain object naturally owns the orchestration. Keep domain rules out of transport/UI controllers.

## Model state and invariants

When behavior depends on lifecycle state, write legal states and transitions before adding booleans.

Instead of:

```text
record Order
    public paid, shipped, cancelled
# Independent flags permit contradictory combinations.
```

prefer an explicit state model when combinations matter:

```text
class Order
    private state := awaitingPayment
    markPaid()
        require state = awaitingPayment
        state := paid
    ship()
        require state = paid
        state := shipped
    cancel()
        require state = awaitingPayment
        state := cancelled
# Invalid transitions fail before mutation.
# Cancellation after payment requires a separate refund contract.
```

The operations should enforce legal transitions. An enum alone does not create a valid state machine; behavior must protect transition rules.

## Boundaries and persistence

Do not make persistence shape the domain model by default. Database identity, lazy-loading proxies, serialization fields, and ORM requirements are infrastructure concerns unless the domain actually depends on them.

Use repositories or data mappers when the domain must retrieve/store aggregates or entities without knowing storage details. Do not introduce a repository for every table; the boundary should follow domain consistency and use-case needs.

Treat aggregate boundaries as consistency/transaction boundaries, not object graph convenience. Keep aggregate roots small enough that invariants can be enforced without loading an unbounded graph.

## UML usage

Use UML selectively:

- **Class diagram:** stable type relationships and ownership/composition.
- **Sequence diagram:** responsibility allocation and runtime collaboration.
- **State machine:** lifecycle-dependent behavior.
- **Package/component view:** dependency direction and architecture boundaries.

Do not create diagrams that duplicate code without clarifying a decision. UML 2.5.1 is the current formal OMG UML specification as of this skill's source snapshot; verify if project governance requires a specific version.

## Worked example

Requirement: "A customer may place an order only when every requested item can be reserved; payment authorization must occur before the reservation is committed."

Poor noun mapping:

`Customer`, `Order`, `Item`, `Reservation`, `Payment` classes with getters/setters and a giant `OrderManager`.

Responsibility analysis:

- `Order` owns order line invariants and lifecycle state.
- `InventoryReservationService` decides whether required quantities can be reserved.
- `PaymentGateway` abstracts external authorization.
- `PlaceOrder` application service coordinates the use case and transaction boundary.

```text
class PlaceOrder
    private transaction
    construct(candidate)
        if candidate is absent: fail InvalidDependency
        transaction := candidate
    execute(draft)
        validate draft and monetary bounds
        return transaction.placeOnce(draft.requestId, draft)

interface OrderPlacementTransaction
    placeOnce(requestId, draft) -> placed | unavailable | declined | pendingRecovery
    guarantees placed only after reservation, payment authorization, and persistence succeed
    guarantees retries with the same requestId cannot duplicate placement
    on partial external failure: retain recovery state and return pendingRecovery
```

The transaction boundary owns inventory, payment, and persistence coordination. External effects generally require idempotency and a recovery protocol; do not imply atomic rollback across independent services. Implement that protocol for the actual infrastructure before claiming the placement contract is satisfied.
