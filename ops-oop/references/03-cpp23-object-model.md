# C++23 Object Model and OO Implementation Guidance

Use this reference for C++ ownership/lifetime, RAII, special members, polymorphism, interfaces, copying/moving, PImpl, type erasure, and exception-safety decisions.

## Table of contents

- [Baseline](#baseline)
- [Rule of Zero first](#rule-of-zero-first)
- [Ownership decision table](#ownership-decision-table)
- [Construction and invariants](#construction-and-invariants)
- [Copy and move semantics](#copy-and-move-semantics)
- [Dynamic polymorphism](#dynamic-polymorphism)
- [Static polymorphism and alternatives](#static-polymorphism-and-alternatives)
- [Object slicing](#object-slicing)
- [PImpl and ABI isolation](#pimpl-and-abi-isolation)
- [Exception safety](#exception-safety)
- [Concurrency and object invariants](#concurrency-and-object-invariants)

## Baseline

Examples target ISO C++23 as published in ISO/IEC 14882:2024. Use features only when they make the design clearer and respect the repository's configured standard. If a project is restricted to C++20/C++17, translate examples rather than forcing newer syntax.

Use the C++ Core Guidelines and SEI CERT C++ as advisory sources when they match project policy. In regulated projects, the project's mandated profile has authority over generic examples.

## Rule of Zero first

Prefer members whose types manage their own resources so the containing class needs no custom destructor/copy/move logic.

```cpp
class Document {
public:
    explicit Document(std::string text) : text_(std::move(text)) {}

private:
    std::string text_;
    std::vector<Section> sections_;
};
```

Write custom special members only when the type's semantics require them. Resource-managing classes should normally encapsulate one resource/lifetime policy and make copyability/movability intentional.

## Ownership decision table

| Requirement | Preferred representation |
|---|---|
| object is a direct part of owner | value member |
| exclusive dynamic ownership | `std::unique_ptr<T>` |
| genuinely shared lifetime | `std::shared_ptr<T>` with cycle analysis |
| non-owning required reference | `T&` / `const T&` |
| nullable non-owning reference | `T*` with documented borrowing semantics |
| contiguous borrowed range | `std::span<T>` / `std::span<const T>` |
| borrowed character sequence | `std::string_view` when source lifetime is sufficient |

Do not return/store views that outlive their source. Lifetime reasoning is more important than compact syntax.

## Construction and invariants

Construct fully valid objects whenever practical. Use named factories when construction can fail or requires multi-step policy.

Avoid calling virtual functions from constructors/destructors when expecting derived dispatch; the dynamic behavior during construction/destruction is intentionally limited and often violates designer expectations.

Keep constructors from publishing `this` to collaborators before invariants are established.

## Copy and move semantics

Decide whether identity/lifetime semantics permit copying.

- Value types: usually copyable/movable.
- Unique owners: usually move-only.
- Identity-bearing entities: copying may be forbidden or must define whether identity is copied or regenerated.
- Polymorphic bases: copying through base values risks slicing; consider `clone()` only when polymorphic copying is a real requirement.

```cpp
class Connection {
public:
    Connection(const Connection&) = delete;
    Connection& operator=(const Connection&) = delete;
    Connection(Connection&&) noexcept = default;
    Connection& operator=(Connection&&) noexcept = default;
};
```

## Dynamic polymorphism

Define small role-oriented interfaces. If clients delete through a base pointer, provide a virtual destructor.

```cpp
class Clock {
public:
    virtual ~Clock() = default;
    virtual TimePoint now() const = 0;
};
```

Mark overrides:

```cpp
class SystemClock final : public Clock {
public:
    TimePoint now() const override;
};
```

Do not make every concrete class polymorphic. Virtual dispatch adds semantic and lifecycle constraints even when runtime overhead is negligible.

## Static polymorphism and alternatives

Consider alternatives before introducing inheritance:

### Concepts/templates

Use when variation is compile-time and generic algorithms are desired.

```cpp
template <class T>
concept HashProvider = requires(const T& t, std::span<const std::byte> bytes) {
    { t.hash(bytes) } -> std::same_as<Digest>;
};
```

### `std::variant`

Use for a closed set of alternatives when exhaustive handling is beneficial.

### Type erasure

Use when runtime polymorphism is needed without exposing inheritance in the public API, especially for value-like wrappers or ABI boundaries. Accept the additional implementation complexity only when it solves a real interface problem.

### Function objects / `std::function`

Use for single-operation policies/callbacks instead of creating one-method class hierarchies when ownership/performance constraints permit.

## Object slicing

Passing/storing a derived object by base value discards the derived part.

```cpp
void render(Shape shape); // suspicious if Shape is polymorphic
```

Prefer references/pointers for polymorphic objects:

```cpp
void render(const Shape& shape);
```

For ownership, prefer smart pointers or a value-type erasure wrapper rather than raw owning pointers.

## PImpl and ABI isolation

PImpl can reduce compile dependencies and preserve binary compatibility, but it adds allocation/indirection and implementation complexity. Use it when ABI stability or dependency hiding is valuable, not as a default form of encapsulation.

```cpp
class Engine {
public:
    Engine();
    ~Engine();
    Engine(Engine&&) noexcept;
    Engine& operator=(Engine&&) noexcept;

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};
```

Define the destructor where `Impl` is complete.

## Exception safety

Select a guarantee appropriate to the operation:

- **no-fail/noexcept:** operation cannot fail through exceptions;
- **strong:** failure leaves observable state unchanged;
- **basic:** invariants hold and resources do not leak, but state may change;
- **no guarantee:** avoid for reusable components unless explicitly justified.

RAII is the foundation: acquire resources in objects whose destructors release them. Do not manually pair allocation/free across multiple return/throw paths.

Mark `noexcept` when semantically true, especially move operations used by containers, but do not suppress real failure paths merely to satisfy style rules.

## Concurrency and object invariants

Thread safety is part of the public contract when objects are shared. Document whether:

- instances are thread-confined;
- const operations are safe concurrently;
- external synchronization is required;
- each operation is atomic with respect to invariants;
- callbacks may re-enter the object.

Do not protect each field independently when correctness depends on a multi-field invariant. Synchronization should protect the invariant boundary.
