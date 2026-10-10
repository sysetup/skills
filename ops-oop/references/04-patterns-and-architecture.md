# Patterns and OO Architecture

Use this reference when selecting design patterns, defining domain/application/infrastructure boundaries, or evaluating architectural variability.

## Table of contents

- [Pattern selection rule](#pattern-selection-rule)
- [Pattern force matrix](#pattern-force-matrix)
- [Patterns that deserve extra skepticism](#patterns-that-deserve-extra-skepticism)
- [Architecture boundaries](#architecture-boundaries)
- [DDD tactical design](#ddd-tactical-design)
- [Example: runtime strategy](#example-runtime-strategy)

## Pattern selection rule

Name the force, variation axis, and consequence before naming a pattern. If direct composition or a function is clearer, use it.

A pattern is justified when it makes future change more localized, makes a contract explicit, or removes repeated decision logic. It is not justified by familiarity alone.

## Pattern force matrix

| Force | Candidate mechanism | Watch for |
|---|---|---|
| replace algorithm/policy | Strategy, callable, template policy | one-method hierarchy may be heavier than a callable |
| create family based on configuration | Factory Method / Abstract Factory | factory layer can become service locator |
| adapt external interface | Adapter | do not leak vendor types through adapter boundary |
| add orthogonal behavior dynamically | Decorator | excessive wrapping obscures identity/debugging |
| tree/part-whole uniformity | Composite | leaf/container semantics must truly align |
| behavior changes with lifecycle state | State | simple enum + switch may be clearer for small closed state sets |
| queue/log/undo request | Command | avoid command classes when plain callable data is enough |
| notify dependents | Observer/event | lifetime, ordering, reentrancy, and unsubscribe semantics matter |
| build complex immutable object | Builder | avoid for trivial constructors |
| traverse operations over stable type set | Visitor | couples operations to closed hierarchy; poor fit when variants change frequently |
| wrap subsystem with simpler API | Facade | facade should reduce dependency surface, not become a god object |

## Patterns that deserve extra skepticism

### Singleton

Global lifetime and global access hide dependencies, complicate test isolation, and create initialization/concurrency hazards. Prefer explicit ownership and dependency injection. Use a process-wide singleton only when uniqueness is truly a system invariant and global access is intentionally accepted.

### Service locator

A locator reduces constructor parameters by moving dependency knowledge to hidden runtime lookup. It often weakens static reasoning and testability. Prefer explicit dependencies at composition roots.

### Template Method

Inheritance-based algorithm skeletons can create fragile base-class coupling. Prefer composition/Strategy when steps vary independently or when the base must expose protected hooks.

## Architecture boundaries

Use OO at the architecture level to control dependency direction:

- **Domain:** business concepts, rules, invariants.
- **Application/use-case layer:** orchestration, transaction/use-case coordination.
- **Ports/interfaces:** contracts required by policy.
- **Infrastructure/adapters:** database, messaging, filesystem, web, devices, vendor SDKs.

High-level policy defines the interfaces it needs; infrastructure implements/adapts them. Keep framework annotations/types from contaminating domain code unless integration simplicity clearly outweighs isolation.

Avoid turning architecture into a layer-count ritual. A small program may need only modules and a few values. Add boundaries where volatility, testability, deployment, regulation, or team ownership makes them valuable.

## DDD tactical design

Use Domain-Driven Design tactics when domain complexity justifies them:

- **Entity:** identity matters.
- **Value Object:** equality by value; preferably immutable or mutation-contained.
- **Aggregate:** consistency boundary around a root.
- **Repository:** collection-like abstraction for aggregate persistence when useful.
- **Domain Service:** domain operation not naturally owned by one entity/value.
- **Domain Event:** records a meaningful domain occurrence.

Do not apply every DDD pattern to CRUD systems. DDD pays for itself when business rules and language complexity dominate infrastructure complexity.

## Example: runtime strategy

```cpp
class PricingPolicy {
public:
    virtual ~PricingPolicy() = default;
    virtual Money price(const Cart&) const = 0;
};

class Checkout {
public:
    explicit Checkout(std::unique_ptr<PricingPolicy> pricing)
        : pricing_(std::move(pricing)) {}

    Receipt execute(const Cart& cart) {
        return Receipt{pricing_->price(cart)};
    }

private:
    std::unique_ptr<PricingPolicy> pricing_;
};
```

Use this design when pricing policy varies at runtime or deployment time. If only compile-time variation is required, a template/callable policy may remove heap allocation and virtual dispatch. If there is only one stable policy, a direct function/member may be best.
