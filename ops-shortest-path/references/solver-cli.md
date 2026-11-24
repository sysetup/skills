# Solver CLI Reference

`scripts/solve.node.mjs` is a zero-dependency Node.js ESM solver designed for non-interactive agent execution. Structured results go to `stdout`; error JSON diagnostics go to `stderr`.

## Invocation Pattern

Always resolve `SOLVER` from the verified directory containing `SKILL.md` and keep the caller's working directory unchanged:

```bash
node "$SOLVER" <command> [options]
```

Run `node "$SOLVER" --help` for concise usage or `node "$SOLVER" selftest` to verify the solver in a new environment.

## Commands

| Command | Required options | Behavior |
| --- | --- | --- |
| `path` | `--input`, `--from`, `--to` | Minimum-cost path from one source to one target. |
| `nearest` | `--input`, `--from`, `--targets` | Stops at the first settled target in the non-empty set; pass `--all-targets` to settle every target. |
| `distances` | `--input`, `--from` | All-distances reachability map from `--from`, sorted by cost, hops, and node ID. |
| `k-paths` | `--input`, `--from`, `--to` | Top-K loopless shortest paths via Yen's algorithm (`--k 1..20`, default `3`). Does not accept `--budget`. |
| `validate` | `--input` | Validates graph structure, strict numeric types, non-negativity, and applicability notes without searching. |
| `selftest` | none | Runs 8 built-in deterministic verification checks and prints a JSON report. |

## Options

| Flag | Values / Default | Purpose |
| --- | --- | --- |
| `--input <file\|->` | File path or `-` | Read graph from a regular file or `stdin`. |
| `--input-format <fmt>` | `auto` (default), `json`, `csv`, `dot` | Override auto-detection by extension or content prefix. |
| `--from <node>` | Node ID string | Source node ID (required for search commands). |
| `--to <node>` | Node ID string | Target node ID (`path`, `k-paths`). |
| `--targets <a,b,c>` | Comma-separated, repeatable | Non-empty target set (`nearest`). |
| `--all-targets` | Boolean flag | Settle all targets in `nearest` instead of stopping at the closest one. |
| `--k <1..20>` | Integer (default `3`) | Maximum number of loopless paths for `k-paths`. |
| `--undirected` | Boolean flag | Treat every edge as bidirectional. |
| `--reverse` | Boolean flag | Reverse edge direction before search (all-sources toward `--from`). |
| `--avoid-node <id[,id2]>` | Repeatable | Exclude node(s) for failover and *what-if* analysis. |
| `--avoid-edge <id[,id2]>` | Repeatable | Exclude specific edge ID(s), including individual parallel edges. |
| `--budget <dim=max>` | Repeatable (`path`, `nearest`, `distances`) | Enforce non-negative integer budget cap on `edge.costs[dim]`. |
| `--reliability` | Boolean flag | Parse edge probabilities in `(0, 1]` as `-ln(p)` costs, skip `p = 0`, and report composite reliability. |
| `--default-weight <n>` | Non-negative number | Explicit weight for unweighted DOT edges (recorded in `assumptions`). |
| `--max-cost <n>` | Non-negative number | Prune candidate states whose cumulative cost exceeds `n`. |
| `--max-states <n>` | Positive integer (default `200000`) | Hard cap on settled states before returning exit `5`. |
| `--max-heap <n>` | Positive integer (default `500000`) | Hard cap on priority queue entries before returning exit `5`. |
| `--max-input-bytes <n>` | Positive integer (default `2097152`) | Hard cap on raw input payload size before returning exit `5`. |
| `--format <fmt>` | `json` (default), `mermaid`, `table` | Select output format on `stdout`. |

## Input Formats

### JSON (recommended for full features)

```json
{
  "directed": true,
  "unit": "downtime_min",
  "nodes": ["v1.0", "v2.0", "v3.0"],
  "edges": [
    {
      "id": "mig-1-2",
      "from": "v1.0",
      "to": "v2.0",
      "weight": 6,
      "label": "online dual-write",
      "costs": { "restarts": 0 }
    }
  ]
}
```

- `nodes` is optional; when provided, every edge endpoint must exist in `nodes` (catches typos fail-closed).
- `weight` (or `probability` under `--reliability`) must be a finite JSON number; strings, booleans, `null`, `NaN`, and `Infinity` are rejected.
- `id` is optional; omitted IDs default deterministically to `e1`, `e2`, and so on.

### CSV edge-list

Supports standard headers (`from,to,weight[,id][,label][,cost:<dim>]`) or headerless `from,to,weight[,id[,label]]`:

```csv
from,to,weight,id,label,cost:restarts
v1.0,v2.0,6,mig-1-2,online dual-write,0
v2.0,v3.0,7,mig-2-3,rolling cutover,1
```

### Graphviz DOT subset

Supports `digraph` (`->`) and `graph` (`--`), comments, chained edges (`a -> b -> c [weight=2];`), and `weight`, `cost`, `probability`, `label`, and `id` attributes. Unweighted edges fail closed unless `--default-weight <n>` is supplied explicitly.

## Output Formats and Exit Codes

- `json`: Returns `status`, `command`, `options`, `result` (including ordered `edges` with `step`, `id`, `weight`, `cumulativeCost`), `graph` diagnostics, and `assumptions`.
- `mermaid`: Emits a valid `flowchart LR` (or `graph LR`) highlighting the optimal path with thick edges (`==>`) and sanitized labels. Graphs with more than 80 edges render the optimal-route subgraph with a comment noting truncation.
- `table`: Emits a compact Markdown table of route steps or distance rankings.

| Exit code | Status | Meaning |
| --- | --- | --- |
| `0` | `found` / `valid` / `ok` | Computation, validation, or selftest succeeded. |
| `1` | `unreachable` | Valid model, no feasible path satisfies the constraints. |
| `2` | `cli_error` | Missing/invalid CLI flags or unreadable input file. |
| `3` | `invalid_input` | Syntax error, invalid type, undeclared node, overflow, or empty target set. |
| `4` | `inapplicable_model` | Negative edge weight detected; switch to Bellman-Ford or DAG DP. |
| `5` | `resource_limit` | Exceeded `--max-states`, `--max-heap`, or `--max-input-bytes` limit. |
