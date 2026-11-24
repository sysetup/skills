# Implementing and Auditing Dijkstra in Source Code

Load this reference when the task is to implement, review, debug, or optimize Dijkstra's algorithm inside a project codebase rather than running the bundled operational solver. Adapt idioms and data structures to the target project's language and conventions.

## Core Relaxation and Termination Procedure

The procedure below returns one optimal path (not all equal-cost ties). Initialize `dist[source] = 0`, all other distances as a distinct unreached sentinel, and a min-heap holding `(0, next_serial(), source)`. Including a monotonic `serial` guarantees equal priorities never compare arbitrary node objects.

```text
while heap is not empty:
    enforce configured state, queue, memory, and time limits
    (d, _, u) = pop_min(heap)
    if d != dist[u]: continue                  # skip stale heap entry
    mark u settled                             # d is now final
    if u is a requested target: return reconstruct(u), d
    for each edge (u, v, weight, edge_id):
        candidate = checked_add(d, weight)     # fail on overflow or non-finite sum
        if dist[v] is unreached or candidate < dist[v]:
            enforce storage limits before mutating state or pushing
            dist[v] = candidate
            predecessor[v] = (u, edge_id)
            push(heap, (candidate, next_serial(), v))
```

## Non-Negotiable Correctness Invariants

1. **Validate every edge before any early return.** Even when `source == target`, reject malformed endpoints, non-numeric weights, `NaN`, infinity, and negative weights across the full explicit graph. For implicit graphs, verify a non-negativity invariant for the transition generator and validate every generated edge.
1. **Update predecessors only on strict improvement (`candidate < dist[v]`).** Rewriting predecessors on equal cost (`<=`) can create cycles across zero-weight edges and break path reconstruction.
1. **Terminate on settlement, never on discovery.** Pushing a target into the heap does not prove its cost is final; stop only when the target is popped as the minimum non-stale entry.
1. **Preserve parallel edge identity.** Store `(predecessor_node, edge_id)` when multiple edges can connect `(u, v)` so reconstruction identifies the exact chosen edge.
1. **Use checked arithmetic and a distinct unreached marker.** Integer overflow or IEEE-754 infinity is a numeric failure, never an unreachable route. Prefer exact integer units (`ms`, cents, bytes) when feasible. For floating-point costs, state the precision model and avoid epsilon hacks that suppress genuine improvements.
1. **Guard predecessor reconstruction against cycles.** Track visited nodes during backtracking so corrupted state terminates deterministically with an error.
1. **Keep the graph snapshot immutable during a run.** Mutating edge weights mid-search invalidates settlement guarantees.

## Target Modes and Unreachability

- **Single target**: stop when the target is settled; return `[source]` at cost `0` when `source == target` after full validation.
- **Target set (nearest target)**: reject an empty target set as invalid (never treat it as all-distances mode); stop on the first settled member. Finding distances to every requested target requires settling each one or exhausting the queue.
- **All-distances**: exhaust the priority queue; report unreachable only after full exhaustion under valid inputs. Never label a limit-truncated or `--max-cost`-pruned search as unreachable.

## Complexity and Resource Bounds

| Representation | Time complexity | Auxiliary space (excluding graph `O(V + E)`) | Practical guidance |
| --- | --- | --- | --- |
| Adjacency list + lazy binary heap | `O(V + E log(E + 1))` | `O(V + E)` | Default choice in Python (`heapq`), Rust (`BinaryHeap`), JS/TS, Go, and C++ (`priority_queue`); simpler and fast in practice. |
| Adjacency list + indexed heap (`decrease-key`) | `O((V + E) log(V + 1))` | `O(V)` | Use when graphs are dense or memory caps forbid duplicate stale entries in the heap. |
| Expanded state graph with `k` discrete integer budgets `B1..Bk` | Apply bounds to `V'` and `E'` | `states <= V * (B1 + 1) * ... * (Bk + 1)` | Bound total states before running; the state bound multiplies `(Bi + 1)` per budget, not `V * k`. Continuous budgets require justified discretization or another solver. |

Include input validation and path reconstruction costs in total runtime budgets. Do not claim wall-clock speedups from asymptotic bounds alone; benchmark representative workloads when performance matters.

## Code Review and Verification Checklist

Test every non-trivial implementation against these cases before claiming correctness:

- Nominal weighted route where a multi-hop path beats a direct expensive edge.
- `source == target` on a valid graph (cost `0`, singleton path) and on a graph containing an unrelated negative edge (must still fail validation).
- Zero-weight edges and zero-weight cycles (must terminate cleanly without cyclic predecessors).
- Parallel edges between the same endpoints (must select the cheaper edge and preserve its `edge_id`).
- Negative edge weight, `NaN`, `Infinity`, and non-numeric weight types (must fail closed).
- Arithmetic overflow near `MAX_SAFE_INTEGER` / `INT64_MAX` (must fail explicitly, not wrap or report unreachable).
- Unreachable target vs. state/heap limit hit (must return distinct observable statuses).
- Multi-target `nearest` mode and explicit empty target set rejection.
