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

```cpp
struct Order {
    bool paid{};
    bool shipped{};
    bool cancelled{};
};
```

prefer an explicit state model when combinations matter:

```cpp
enum class OrderState {
    awaiting_payment,
    paid,
    shipped,
    cancelled
};

class Order {
public:
    void mark_paid();
    void ship();
    void cancel();

private:
    OrderState state_{OrderState::awaiting_payment};
};
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

```cpp
struct PlaceOrderResult {
    enum class Status { placed, unavailable, payment_declined } status;
};

class PlaceOrder {
public:
    PlaceOrder(InventoryReservationService& inventory,
               PaymentGateway& payments,
               OrderRepository& orders)
        : inventory_(inventory), payments_(payments), orders_(orders) {}

    PlaceOrderResult execute(const DraftOrder& draft) {
        auto reservation = inventory_.try_reserve(draft.lines());
        if (!reservation) return {PlaceOrderResult::Status::unavailable};

        if (!payments_.authorize(draft.total_cents())) {
            reservation->release();
            return {PlaceOrderResult::Status::payment_declined};
        }

        orders_.save(Order::from(draft, std::move(*reservation)));
        return {PlaceOrderResult::Status::placed};
    }

private:
    InventoryReservationService& inventory_; // non-owning collaborators
    PaymentGateway& payments_;
    OrderRepository& orders_;
};
```

The design can still change after transaction/error analysis. The point is that responsibilities are derived from the scenario, not from nouns alone.
