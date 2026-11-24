# Model Selection and Cost Hygiene

Verify that Dijkstra actually matches the engineering problem before building a graph. Choosing the wrong graph model produces confident but operationally invalid plans.

## Fast Model Decision Table

| Problem signature | Correct model | Why Dijkstra does or does not apply |
| --- | --- | --- |
| Minimum additive cost from one source to one target, nearest target, or all nodes, with weights `>= 0` | **Dijkstra** (`scripts/solve.node.mjs`) | Exact match; greedy settlement holds because non-negative edges cannot reduce an already settled distance. |
| Need Plan A, Plan B, and Plan C loopless alternatives with weights `>= 0` | **Yen's algorithm over Dijkstra** (`k-paths`) | Reuses Dijkstra on spur subgraphs while forbidding root nodes and prior edges. |
| Minimize primary non-negative cost subject to 1+ small discrete integer caps (restarts, hops, PRs) | **Constrained Dijkstra on expanded state graph** (`--budget dim=max`) | Expands states `(node, b1..bk)` within explicit `--max-states` bounds. |
| Maximize path reliability under independent edge probabilities `p` in `(0, 1]` | **Dijkstra on `-ln(p)`** (`--reliability`) | `max prod(p_i)` is mathematically equivalent to `min sum(-ln(p_i))` with `-ln(p_i) >= 0`. |
| All edges have identical positive weight (pure hop count) | **BFS** (Dijkstra also valid) | BFS runs in `O(V + E)` without heap overhead; solver still works and flags equal weights automatically. |
| Directed Acyclic Graph (DAG), including negative weights or longest-path / critical-path scheduling | **Topological DP (critical path)** | Build/CI pipelines and distributed traces require executing all prerequisites (longest chain), not picking one cheapest alternative. |
| General graph with one or more negative edge weights | **Bellman-Ford** (or Johnson for all-pairs) | Negative edges break Dijkstra's settlement invariant. Never clamp or shift negative weights to force Dijkstra. |
| Maximize minimum link bandwidth or minimize maximum single-edge latency | **Bottleneck / minimax path** | Objective is `min max(w_i)` or `max min(w_i)`, not additive `sum(w_i)`; requires a distinct relaxation rule. |
| Connect all nodes with minimum total wiring/peering cost | **Minimum Spanning Tree (Kruskal/Prim)** | Minimizes total tree cost across all nodes, not source-to-target route cost. |
| Real-time dynamic routing with changing congestion or feedback loops | **Snapshot model + recomputation policy** | Dijkstra solves a static snapshot; live routing requires a defined measurement window and anti-oscillation policy. |

## Cost-Function Hygiene Rules

Apply these rules whenever designing weights for SDLC and DevOps graphs:

1. **Use one physical or well-defined additive unit per run.** Valid examples: milliseconds (`ms`), minutes of downtime (`downtime_min`), egress dollars (`usd`), hop count (`hops`), or byte deltas (`kb`).
1. **Never fabricate hybrid composite scores.** Do not invent formulas like `0.4 * latency_ms + 0.6 * subjective_risk_score` unless the requester explicitly supplies a calibrated, documented business cost model in common units (for example expected dollars of outage cost).
1. **Keep secondary hard limits separate.** Express hard ceilings such as maximum restarts, maintenance window minutes, or allowed breaking changes via `--budget <dim=max>` rather than inflating weights arbitrarily.
1. **State measurement scope and defaults explicitly.** Record the snapshot window for empirical latencies/probabilities, and pass `--default-weight <n>` explicitly rather than letting missing weights default silently.
1. **Preserve zero-cost and parallel edges.** Zero-cost transitions (for example an in-place alias or no-op shim) and multiple parallel edges between the same endpoints (for example direct fiber vs. VPN backup) are valid; assign distinct edge `id` values so exclusions (`--avoid-edge`) and audit trails stay unambiguous.
1. **Never shift negative weights.** Adding a constant `+C` to every edge distorts the optimum because paths with more hops pay `C` more times than shorter paths. Reject negative weights and switch to Bellman-Ford or DAG topological DP.
