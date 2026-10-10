# Algorithm and Data-Structure Selection

## Purpose

Use this reference to decide *what computation to perform* before deciding how to spell it in source code.

## Selection sequence

1. Define the input scale and operation mix.
2. Identify the dominant resource.
3. Establish the simplest correct baseline.
4. Search for a change in representation, preprocessing, reuse, or algorithmic family that removes repeated work.
5. Compare worst-case/expected/amortized behavior and memory.
6. Account for finite-input constants and machine effects.
7. Select the candidate that satisfies the full contract, not merely the smallest asymptotic symbol.

## High-value transformations

### Remove repeated scans

If the program repeatedly searches the same data, consider indexing or preprocessing.

- Repeated membership tests: linear scan -> hash set for expected O(1) membership, or balanced tree for O(log n) worst-case operations plus ordering.
- Repeated range aggregates on immutable data: per-query scan O(n) -> prefix preprocessing O(n), then O(1) per additive range query.
- Repeated static graph reachability or distance questions: evaluate whether preprocessing, components, shortest-path trees, or specialized indexes amortize their cost.

Do not preprocess by reflex. Let preprocessing cost `P`, old per-operation cost `A`, new per-operation cost `B`, and operation count `q`. Require the workload to justify approximately `P + qB < qA`, subject to memory and update costs.

### Replace recomputation with state reuse

Use memoization or dynamic programming when subproblems overlap and their result is reusable. State the state definition, transition, base cases, evaluation order, and memory footprint.

Prefer bottom-up or compressed-state formulations when they reduce recursion overhead or memory without obscuring the invariant. Prefer memoization when only a sparse subset of states is reached.

### Match the data structure to the operation mix

Do not choose containers by familiarity.

| Need | Typical candidate | Important caveat |
|---|---|---|
| append + indexed access | dynamic array/vector | middle insertion/erase moves elements |
| FIFO | queue/deque | do not emulate by erasing vector front repeatedly |
| membership, no order | hash set | expected bounds; adversarial hashing and memory overhead matter |
| sorted iteration / predecessor / range by key | balanced ordered tree | O(log n) operations, pointer/locality overhead |
| min/max frontier | heap / priority queue | arbitrary deletion/update may need handles or alternate structure |
| dense integer-key membership | bitset/bitmap/flat array | exploit bounded universe; can beat hashing by locality |
| graph, sparse | adjacency list | O(V+E) storage |
| graph, dense / constant edge test | matrix/bit-matrix | O(V^2) storage; bit packing can change constants drastically |

### Reduce nested search by exploiting order or structure

Before accepting O(n^2) pairwise work, ask whether sorting, hashing, two pointers, sweep lines, prefix/suffix information, divide-and-conquer, or spatial/interval indexing can remove a dimension of repeated work.

Do not mechanically replace every O(n^2) loop. If n is tightly bounded, the simpler algorithm may have lower latency, smaller code, deterministic behavior, and less memory. Record the bound that makes that decision safe.

### Batch expensive boundaries

For databases, filesystems, networks, accelerators, kernels, or RPCs, the dominant cost may be boundary crossings rather than arithmetic. Reduce round trips and unnecessary serialization/copies before optimizing inner-loop instructions.

A mathematically faster local loop cannot compensate for an avoidable N+1 query pattern or one network request per element.

### Use streaming when materialization is unnecessary

If the result can be produced incrementally, avoid holding the full input/intermediate state. State latency and backpressure implications. Streaming may change space from O(n) to O(1) or O(window), but may constrain reordering and retries.

### Use approximation only under an explicit error contract

Approximation, sampling, probabilistic data structures, randomized algorithms, and heuristics can be superior when exactness is not required. State error probability/bound, confidence, reproducibility/seed behavior, and pathological cases.

## Complexity accounting

Always name what n means. For multi-dimensional workloads, use the relevant variables instead of collapsing everything into n.

Examples:

- Graph traversal: O(V + E), not merely O(n).
- Dijkstra with a binary heap and adjacency lists: commonly O((V + E) log V), often written O(E log V) for connected sparse graphs; preconditions include nonnegative edge weights.
- Sorting plus scan: O(n log n) time, but account for extra memory and stability requirements of the selected sort.
- Hash lookup: expected O(1) is not a universal worst-case guarantee.

Distinguish auxiliary space from input/output storage when it matters.

## Finite-machine performance

After choosing a sound algorithmic family, consider:

- cache locality and contiguous traversal;
- allocation count and object/header overhead;
- branch predictability;
- vectorization and data dependencies;
- copying and serialization;
- virtual dispatch/indirection;
- lock contention and false sharing;
- NUMA placement;
- I/O access pattern;
- compiler optimization and build mode.

Treat these as measurable effects. Do not infer them from code appearance alone.

## Concurrency decision rule

Parallelize only after identifying independent or safely synchronized work and a workload large enough to amortize scheduling, communication, synchronization, and merge costs.

State:

- partitioning strategy;
- shared state and ownership;
- synchronization mechanism;
- deterministic/non-deterministic behavior;
- work/span or equivalent scalability reasoning when useful;
- expected bottleneck after parallelization.

Do not use concurrency to mask an avoidable algorithmic inefficiency.
