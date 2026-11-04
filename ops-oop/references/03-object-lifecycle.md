# Object Lifecycle and Implementation Contracts

Use this reference for construction, ownership, borrowing, copying, polymorphism, cleanup, errors, and concurrency in any implementation language.

## Construction and invariants

Validate before publishing an instance. Reject absent required collaborators and invalid domain values at the boundary. Keep collaborators alive for every operation that uses them; do not expose a partially constructed object or invoke overridable behavior before invariants hold.

## Ownership and access

| Requirement | Contract |
| --- | --- |
| Direct part of an object | Owner controls its lifecycle and valid state. |
| Exclusive external resource | One owner acquires and releases it on every exit path. |
| Shared lifetime | Define joint ownership, cleanup, and cycle handling explicitly. |
| Required borrowed collaborator | Non-null; the owner outlives all borrowed access. |
| Optional collaborator | Represent absence explicitly and handle it before use. |
| Borrowed range or view | Bound its extent and lifetime; do not retain invalidated access. |

Prefer composition with managed members. Use the language's deterministic cleanup mechanism for files, locks, connections, or similar external resources; garbage collection alone is insufficient.

```text
class ResourceSession
    private resource
    private closed := false
    construct(provider)
        if provider is absent: fail InvalidDependency
        resource := provider.acquire()  # Acquisition failure creates no session.
    use(request)
        if closed: fail ClosedSession
        return resource.perform(request)
    close()
        if closed: return
        resource.release()
        closed := true
contract: release failure preserves a documented recoverable state
caller: ensure close is attempted on both success and failure
```

## Identity and copying

Copy immutable values by value. Decide whether entity copying preserves or creates identity. For exclusive resources, forbid copying or define explicit transfer semantics. Polymorphic copying must preserve the concrete behavior if clients depend on it.

## Substitution and binding

Define small role interfaces with common input, output, failure, ownership, and timing contracts. Bind statically when variability is known before execution; use runtime substitution only when required. Preserve the concrete behavior when passing or storing a polymorphic object.

## Error guarantees

Select and document one guarantee per operation: cannot fail under stated preconditions; failure preserves observable state; or failure preserves invariants with a declared partial effect. Do not promise rollback for irreversible external actions. Use idempotency and explicit recovery state for retriable distributed effects.

## Concurrency

Specify confinement, synchronization, atomicity, and callback reentrancy. Protect the full invariant across related fields. A lock per field is insufficient when a valid state depends on several fields changing together.
