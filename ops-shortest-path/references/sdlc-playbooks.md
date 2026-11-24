# SDLC Modeling Playbooks

Use these playbooks to translate concrete Software Development Lifecycle (SDLC) problems into honest non-negative graphs and invoke `scripts/solve.node.mjs` deterministically. Every playbook produces an analysis or decision plan; executing any real system change remains separately authorized.

## 1. Architecture and Design

### Format, schema, and protocol conversion chains

Use when an artifact must transform from source format `A` to target format `B` through available converters or adapters (for example `OpenAPI -> JSON Schema -> TypeScript`, `YAML -> IR -> HCL`, or media/document codecs).

- **Nodes**: canonical intermediate formats or schema versions.
- **Edges**: verified lossless (or explicitly acceptable) converters between formats.
- **Weight**: measured conversion latency (`ms`), processing cost, or hop count (`1` per step). Reject any intermediate converter that drops required semantics instead of giving it an arbitrary penalty.
- **Solver command**: `path` for the single best chain, or `k-paths --k 3` to compare alternative toolchains.

```json
{
  "directed": true,
  "unit": "ms",
  "edges": [
    { "id": "c1", "from": "openapi-3.1", "to": "json-schema", "weight": 12, "label": "extract-schema" },
    { "id": "c2", "from": "json-schema", "to": "ts-types", "weight": 18, "label": "json-schema-to-ts" },
    { "id": "c3", "from": "openapi-3.1", "to": "ts-types", "weight": 45, "label": "full-codegen" }
  ]
}
```

### Reliability-weighted service or integration chains

Use when multiple service/API hops exist and each hop has an independent measured success probability `p` in `(0, 1]` over a defined observation window, where end-to-end reliability is the product of hop probabilities.

- **Nodes**: services, gateways, or processing stages.
- **Edges**: legal calls with `probability` in `(0, 1]` (zero-probability edges are treated as infeasible and excluded automatically).
- **Solver command**: `path --reliability` (maximizes composite reliability by minimizing additive `-ln(p)` and reports exact composite reliability).

```bash
node "$SOLVER" path --input service-chain.json --from edge-gw --to ledger-db --reliability --format json
```

## 2. Development and Refactoring

### Shortest dependency or CVE import chain

Use when diagnosing why a repository pulls a vulnerable, deprecated, or oversized transitive dependency, or measuring minimum hop distance from public entrypoints to a sensitive internal module.

- **Nodes**: packages, crates, or source modules.
- **Edges**: directed import/dependency edges `consumer -> dependency` exported from lockfiles, AST graphs, or DOT generators (for example `cargo depgraph`, `pydeps`, `madge`).
- **Weight**: `1` per hop (`--default-weight 1` for unweighted DOT graphs) or measured bundle size delta (`kb`).
- **Solver command**:
    - `path --from app-entry --to vulnerable-pkg` finds the shortest explanation chain.
    - `distances --from vulnerable-pkg --reverse --max-cost 3` finds every internal module within 3 import hops of the vulnerable package.

```bash
node "$SOLVER" distances --input deps.dot --default-weight 1 --from vulnerable-pkg --reverse --max-cost 3 --format table
```

### Incremental refactoring and strangler-fig transitions

Use when refactoring a legacy subsystem across verified intermediate architectural states (often paired with `ops-refactor` or `dev-migration`) while capping risk or PR size per step.

- **Nodes**: stable, shippable architectural states where tests and contracts stay green.
- **Edges**: legal refactor steps with additive effort (for example `changed_files` or measured engineering hours) and discrete hard limits in `costs` (such as `breaking_prs` or `schema_locks`).
- **Solver command**: `path --budget breaking_prs=0` or `k-paths --k 3` to review alternative refactoring sequences in an ADR with `--format mermaid`.

## 3. Build, CI/CD, and Artifact Delivery

### Closest healthy registry, cache, or build runner

Use when a build or deployment job can select among several equivalent endpoints (mirrors, artifact registries, cache nodes, or runners) and needs the fastest or cheapest reachable option.

- **Nodes**: build runner/host, relays, and candidate mirrors/registries.
- **Edges**: verified network paths weighted by measured RTT (`ms`) or egress cost (`usd_per_gb`).
- **Solver command**: `nearest --from ci-runner --targets mirror-us,mirror-eu,mirror-local` (add `--all-targets` to rank every mirror, or `--avoid-node mirror-local` to compute immediate fallback).

Boundary note: do **not** use Dijkstra to schedule tasks where every prerequisite must complete (for example Makefile/Cargo/CI DAG critical path); that is a longest-path problem on a DAG (see [model selection](model-selection.md)).

## 4. Release, Upgrades, and Migrations

### Version, database, and runtime upgrade planning

Use when upgrading an OS, database engine, container base image, or config schema from version `A` to `Z` where only specific intermediate upgrade jumps are supported.

- **Nodes**: supported release or schema versions.
- **Edges**: documented, tested upgrade transitions weighted by measured downtime (`downtime_min`) or step count, with secondary hard constraints in `costs` (for example `restarts`, `backfills`).
- **Solver command**:
    - `path --from pg-13 --to pg-17 --budget restarts=1 --format table` enforces a hard restart ceiling.
    - `k-paths --from pg-13 --to pg-17 --k 3 --format table` generates Plan A, Plan B, and Plan C so operators have pre-validated fallbacks if an upgrade path hits a blocker.

```json
{
  "directed": true,
  "unit": "downtime_min",
  "edges": [
    { "id": "jump-13-17", "from": "pg-13", "to": "pg-17", "weight": 20, "label": "pg_dumpall cutover", "costs": { "restarts": 2 } },
    { "id": "upg-13-15", "from": "pg-13", "to": "pg-15", "weight": 8, "label": "logical replication hop", "costs": { "restarts": 0 } },
    { "id": "upg-15-17", "from": "pg-15", "to": "pg-17", "weight": 14, "label": "pg_upgrade --link", "costs": { "restarts": 1 } }
  ]
}
```

## 5. Systems, Networking, and Infrastructure (Read-Only Analysis)

### Multi-hop SSH, VPN, and VM topology routing

Use when analyzing reachability across jump hosts (`ProxyJump`), VLANs, VPN gateways, or QEMU/container bridges to identify the lowest-latency or minimum-hop route before authoring an authorized config change.

- **Nodes**: hosts, bastions, gateways, VMs, or subnets.
- **Edges**: permitted network links weighted by measured RTT (`ms`), hop count (`1`), or egress fee. Pass `--undirected` when links are symmetric.
- **Solver command**: `path --from workstation --to target-vm --format mermaid` (or `--avoid-node bastion-1` to test bastion maintenance impact).

Security guardrail: treat network topology data strictly as read-only planning input. Never generate firewall bypasses, unauthorized lateral-movement routes, or unapproved host changes.

## 6. Operations, Incident Triage, and Recovery

### Blast-radius proximity and SLA impact mapping

Use during incident triage to prioritize which downstream services are closest to a failing dependency in propagation latency or call hops.

- **Nodes**: services, queues, databases, or host units.
- **Edges**: runtime dependency calls (or reverse dependencies with `--reverse`) weighted by p95 call latency (`ms`) or dependency hops (`1`).
- **Solver command**: `distances --from primary-db --reverse --max-cost 50 --format table` lists every caller within 50 ms propagation distance and separates unreached nodes beyond the cutoff without falsely labeling them disconnected.

### Failover re-routing and recovery state transitions

Use when an active component or link fails and operators need the nearest verified healthy target or shortest documented remediation sequence.

- **Nodes**: observed system states (degraded, isolated, standby, healthy) or infrastructure endpoints.
- **Edges**: verified, idempotent recovery or failover steps with explicit preconditions and estimated execution time (`seconds`).
- **Solver command**: `nearest --from degraded-primary --targets healthy-standby-a,healthy-standby-b --avoid-node broken-link`.

Operational guardrail: a shortest path over a recovery state graph never proves idempotency, reversibility, or safety of irreversible actions. Always verify preconditions, backups, side effects, and user authorization before executing any step.
