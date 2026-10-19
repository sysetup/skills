---
name: ops-algorithmic-dijkstra
description: Apply Dijkstra's algorithm and shortest-path graph principles to systems engineering, software architecture, OOP abstraction, control-flow optimization, algorithm design, and DevOps/SRE workflows. Use when designing algorithms, refactoring complex conditionals or nested loops, decoupling object graphs, planning migrations, analyzing IAM attack paths, or optimizing network and service routing.
license: MIT
metadata:
  author: "SYSETUP.COM CarlosHRG"
---
# Dijkstra Systems Engineering

Apply Shortest Path First (SPF) principles and top-down graph modeling to produce minimal, deterministic, and loosely coupled software and infrastructure solutions.

## When to Use

- Designing search, routing, scheduling, or optimization algorithms.
- Refactoring deeply nested `if/else` or `switch` branches and brute-force loops.
- Decoupling $O(V^2)$ object conversions, API adapters, or schema migrations.
- Evaluating architectural trade-offs, IAM attack paths, build pipelines, or service-mesh routing.

## Workflow

### 1. Top-Down Graph Abstraction

Before writing code, zoom out and model the problem domain as a directed weighted graph $G = (V, E)$:

- **Vertices ($V$):** Immutable system states, domain types, interfaces, modules, or infrastructure nodes.
- **Edges ($E$):** Valid transitions, `Adapter`/`Strategy`/`Command` implementations, API calls, or network links.
- **Weights ($w(u, v) \ge 0$):** Quantifiable non-negative cost (latency, memory allocation, I/O cardinality, precision loss, technical debt, or exploitability).

### 2. Select the Optimal Algorithm (Fail Closed on Constraints)

Verify edge weight invariants before selecting the solver:

- **Non-negative weighted graph ($w \ge 0$):** Use Dijkstra with a binary min-heap in $O((V + E) \log V)$ time and $O(V)$ space.
- **Unweighted graph ($w = 1$):** Downgrade to BFS in $O(V + E)$ to eliminate heap overhead.
- **Directed Acyclic Graph (DAG):** Use topological sort with linear dynamic programming in $O(V + E)$.
- **Single target with admissible lower bound $h(v)$:** Use A* to prune the search space.
- **Negative weights ($w < 0$):** Reject Dijkstra. Use Bellman-Ford in $O(V \cdot E)$ or Johnson's potential reweighting ($w'(u, v) = w(u, v) + h(u) - h(v) \ge 0$).
- **Dynamic telemetry weights:** Apply EWMA smoothing and hysteresis before recomputing SPF trees to prevent route flapping.

### 3. Apply Algorithm Design Primitives

Use advanced state-space transformations when standard graph modeling is insufficient:

- **Implicit State-Space Search:** Generate neighbors on the fly using canonical state hashes instead of materializing exponential graphs in memory.
- **Cyclic Dynamic Programming:** Resolve DP recurrences containing positive-weight cycles via min-heap relaxation.
- **Layered State Expansion:** Encode $k$ discrete constraints or budgets as $V' = V \times \{0 \dots k\}$ and solve in $O(k(V + E) \log(kV))$.
- **Multi-Source SPF:** Seed all origin nodes $s \in S$ with $d[s] = 0$ in the initial heap for single-pass proximity partitioning.
- **Monotone Semiring Adaptation:** Replace additive relaxation with $\max(d[u], w(u, v))$ for bottleneck minimax paths or $-\ln(p(u, v))$ for maximum reliability.

### 4. Refactor OOP Architecture and Control Flow

Translate graph invariants into lean, modular, object-oriented code:

- **Decouple Classes via Composable Edges:** Replace $O(V^2)$ direct conversions with a registry of single-purpose `Adapter` or `Strategy` objects, resolving multi-step transformations via SPF to uphold high cohesion, low coupling, and the Open/Closed Principle.
- **Replace Nested Conditionals with Guarded State Machines:** Convert complex `if/else` and `switch` trees into data-driven state transitions guarded by predicate objects to minimize cyclomatic complexity.
- **Replace Brute-Force Loops with Priority Pruning:** Substitute nested `for` loops or unguided backtracking with a single `while (!pq.empty())` loop, a `dist` map, and a `visited` set, terminating immediately when the target state is popped.
- **Automate Deterministic Rollbacks:** Model compensating actions (`undo()` / `compensate()`) as weighted edges to compute the minimum-cost recovery path to a valid state on exception.

### 5. Operationalize in DevOps and Security

- **Security and IAM:** Model permissions and firewall rules as a graph to identify and sever minimum-effort privilege escalation paths.
- **Build and Data Pipelines:** Resolve minimum-cost paths across remote caches, local compilation, and incremental schema migrations.
- **Observability and Networking:** Isolate critical-path latency in distributed traces and verify OSPF/service-mesh locality costs.

## Gotchas

- **Premature Node Settlement:** Never mark a node as final upon insertion into the queue; only settle it when extracted from the min-heap (or skip stale heap entries where `cost > dist[u]`).
- **State Mutability Bugs:** Ensure state objects used as graph vertices are strictly immutable and implement deterministic hashing and equality.
- **Over-Engineering Simple Paths:** Do not introduce priority queues when edge weights are uniform or static dependencies are acyclic.
