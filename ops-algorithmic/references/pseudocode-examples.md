# Algorithmic Pseudocode Guide

Source specification: GUIDE@core; edition: 1.0. Local edition: 1.0.

These synthetic examples give developers nonbinding guidance on algorithm selection, correctness, and resource costs. They are language-neutral illustrations, not executable implementations or measured performance results. No external client.

## Notation and contracts

- Sequences use zero-based indices; `[left, right)` excludes `right`. Iteration over an empty interval performs no work. Inputs remain unchanged during an operation.
- `REQUIRE condition` checks at runtime and stops with an input error when false; it is never a removable assertion. Check types before comparisons or indexing; integers exclude booleans and fractional values. `ERROR overflow` stops without returning a result.
- `NONE` is a distinct nonnumeric value. Sequences, hash sets, and FIFO queues are abstract data structures; indexed access is O(1), and queue insertion/removal is O(1) amortized.
- Before allocation, validate finite sequence shapes, representable lengths and capacity budgets. Let `INDEX_MAX >= 1` be the largest supported length/index counter; all lengths are at most `INDEX_MAX`. Allocation failure returns an error, not a partial result.
- Numeric examples use a declared integer interval `[MIN, MAX]` with `MIN <= 0 <= MAX`. Arithmetic is bounded; check before evaluating a potentially overflowing expression. Complexity counts bounded-word operations; arbitrary-precision implementations must include operand-size costs.

The checked primitives below are shared by the numeric examples. The guard expressions stay within the declared interval for validated operands, including when `y = MIN`; subtraction never negates `y`.

```text
CheckedAdd(x, y):
    REQUIRE x and y are integers in [MIN, MAX]
    IF y > 0:
        IF x > MAX - y: ERROR overflow
    IF y < 0:
        IF x < MIN - y: ERROR overflow
    RETURN x + y

CheckedSubtract(x, y):
    REQUIRE x and y are integers in [MIN, MAX]
    IF y > 0:
        IF x < MIN + y: ERROR overflow
    IF y < 0:
        IF x > MAX + y: ERROR overflow
    RETURN x - y
```

## 1. Remove an avoidable quadratic duplicate search

Require a finite sequence with a consistent equality relation. The baseline uses O(n^2) comparisons in the worst case and O(1) auxiliary space.

```text
HasDuplicateQuadratic(values):
    n <- length(values)
    FOR i IN [0, n):
        FOR j IN [i + 1, n):
            IF values[i] = values[j]: RETURN true
    RETURN false

HasDuplicate(values):
    seen <- empty hash set
    FOR EACH value IN values:
        IF value IN seen: RETURN true
        INSERT value INTO seen
    RETURN false
```

The hash version requires hashable values with equal values producing equal hashes. It uses expected O(n) time and O(n) auxiliary space when hashing and equality cost O(1). Adversarial collisions can degrade it. Sorting or the baseline may be preferable for deterministic bounds, limited memory, or tiny inputs.

## 2. Amortize repeated range-sum queries

For immutable integer values, q direct scans cost O(qn). Prefix sums cost O(n) to build, O(1) per query, and O(n) storage. The result is an immutable object created only by `BuildPrefixSum`; callers cannot supply or modify its internal prefix array.

```text
BuildPrefixSum(values):
    n <- length(values)
    REQUIRE n < INDEX_MAX
    prefix <- sequence of n + 1 zeros
    FOR i IN [0, n):
        prefix[i + 1] <- CheckedAdd(prefix[i], values[i])
    RETURN immutable PrefixSum(n, prefix)

RangeSum(sums, left, right):
    REQUIRE sums is an object returned by BuildPrefixSum
    REQUIRE left and right are integers
    REQUIRE 0 <= left <= right <= sums.n
    RETURN CheckedSubtract(sums.prefix[right], sums.prefix[left])
```

Invariant: `prefix[k]` equals the exact sum of `values[0:k]` and lies in `[MIN, MAX]`. Check `n < INDEX_MAX` before computing `n + 1`. Construction fails on any unrepresentable prefix, even if the final sum would fit. A query can overflow even when every stored prefix fits, so subtraction is checked separately. Empty ranges return zero; updates require rebuilding or another data structure.

## 3. Preserve a loop invariant explicitly

Require a finite sequence sorted in nondecreasing order under a total order shared with the target. Validate ordering once at an untrusted boundary in O(n), or obtain the sequence from a trusted sorting operation; the search itself is O(log n) time and O(1) auxiliary space.

```text
BinarySearch(sorted, target):
    low <- 0
    high <- length(sorted)
    WHILE low < high:
        mid <- low + floor((high - low) / 2)
        IF sorted[mid] < target:
            low <- mid + 1
        ELSE:
            high <- mid
    IF low < length(sorted):
        IF sorted[low] = target: RETURN low
    RETURN NONE
```

Invariant: `0 <= low <= high <= n`; indices below `low` hold values less than the target, and indices at or above `high` hold values greater than or equal to it. Each iteration shrinks `high - low`. The midpoint avoids `low + high` overflow; `mid < high` keeps access and `mid + 1` valid. Return the first matching index, or `NONE` if absent.

## 4. Make control flow explicit

Express conditional mutation directly rather than embedding it in a boolean expression. Require a boolean flag and an output sequence with capacity for one additional item when enabled.

```text
AppendIfEnabled(enabled, output, value):
    REQUIRE enabled is a boolean
    IF enabled:
        REQUIRE length(output) < INDEX_MAX
        APPEND value TO output
```

Appending to a dynamic array is typically amortized O(1); a resize can cost O(n). The benefit here is visible intent, not an asymptotic improvement.

## 5. Select graph representation from density and operations

Use adjacency lists for a sparse, unweighted graph; all edges have unit cost. Define `V` as the vertex count and `E` as the number of adjacency entries, including duplicates. Validate the entire graph before traversal, including unreachable components. Require a finite sequence of finite adjacency lists within the declared capacity budget.

```text
BfsDistances(graph, source, DISTANCE_MAX):
    n <- length(graph)
    REQUIRE n >= 1
    REQUIRE source is an integer
    REQUIRE 0 <= source < n
    REQUIRE DISTANCE_MAX is a nonnegative integer
    REQUIRE n - 1 <= DISTANCE_MAX
    FOR EACH neighbors IN graph:
        FOR EACH next IN neighbors:
            REQUIRE next is an integer
            REQUIRE 0 <= next < n

    distance <- sequence of n NONE values
    frontier <- empty FIFO queue
    distance[source] <- 0
    ENQUEUE source INTO frontier
    WHILE frontier is not empty:
        node <- DEQUEUE frontier
        FOR EACH next IN graph[node]:
            IF distance[next] = NONE:
                distance[next] <- CheckedAdd(distance[node], 1)
                                  using bounds [0, DISTANCE_MAX]
                ENQUEUE next INTO frontier
    RETURN distance
```

Invariant: discovered vertices are enqueued once, in nondecreasing distance order. Each first discovery yields a shortest path of at most `V - 1` edges. The distance bound prevents overflow; self-loops and duplicate edges do not enqueue a discovered vertex again. Unreachable vertices retain `NONE`. Validation and traversal together take O(V + E) time, with O(V) auxiliary space and O(V + E) total storage including the input. A dense matrix uses O(V^2) storage and can suit frequent edge-existence queries.

## 6. Distinguish asymptotic growth from finite-input speed

Insertion sort has O(n^2) worst-case time; merge sort has O(n log n) worst-case time. Tiny nearly sorted sequences may favor insertion sort because constants and locality matter. A contract such as `n <= 16` can justify that choice; an unbounded workload needs a different analysis. Measure on the intended workload before claiming a runtime advantage.

## 7. Include numeric limits in correctness

Widening an accumulator alone does not prove safety for an arbitrarily long sequence. Use the checked primitive for every addition, or prove an input bound that makes all intermediate sums representable.

```text
SumValues(values):
    total <- 0
    FOR EACH value IN values:
        total <- CheckedAdd(total, value)
    RETURN total
```

Invariant: `total` is the exact sum of the processed prefix within `[MIN, MAX]`. This O(n)-time, O(1)-auxiliary-space algorithm rejects intermediate overflow rather than wrapping, saturating, or silently changing arithmetic semantics.

## Boundary cases and verification

Use the synthetic interval `MIN = -8`, `MAX = 7` for numeric cases and `INDEX_MAX = 7` for length cases. These small limits expose the same boundary errors as wider machine types without large allocations. Each row specifies expected behavior, not an execution result.

| Algorithm | Input or condition | Expected outcome |
| --- | --- | --- |
| Both duplicate searches | `[]`; `[4]`; `[1, 2, 3]`; `[1, 2, 1]` | `false`; `false`; `false`; `true` |
| Prefix sum | `[3, -1, 4, 1]`, query `[1, 3)` | `3` |
| Prefix sum | `[]`, query `[0, 0)` | `0` |
| Prefix sum | `[7]`, queries `[0, 1)` and `[1, 1)` | `7` and `0` |
| Prefix sum | `[-8]`, query `[0, 1)` | `-8` |
| Prefix sum construction | `[7, 1]`; `[-8, -1]`; `[7, 1, -1]` | Overflow error before storing the second prefix |
| Prefix sum query | `[-8, 7, 1]`, query `[1, 3)` | Overflow error: `0 - (-8) = 8` |
| Prefix sum query | `[7, -8, -1]`, query `[1, 3)` | Overflow error: `-2 - 7 = -9` |
| Prefix sum query | Length 1; bounds `(-1, 0)`, `(1, 0)`, `(0, 2)`, `(0.5, 1)`, `(false, 1)` | Input error before indexing |
| Prefix sum construction | Six zeros; seven zeros | Success with seven prefix slots; input error before allocation |
| Binary search | `[]`, target `1`; `[3]`, target `3`; `[1, 3, 3, 7]`, target `3` | `NONE`; `0`; `1` |
| Binary search | `[1, 3]`, targets `0`, `2`, `4` | `NONE` for each |
| Binary search input boundary | `[3, 1]` | Reject unsorted input before search |
| Conditional append | `[]`, value `42`, flag `false` or `true` | `[]` or `[42]` |
| Conditional append | Length `INDEX_MAX`, flag `true` | Input error before append |
| BFS | `[[]]`, source `0`, distance limit `0` | `[0]` |
| BFS | `[[0, 1, 1], [0], []]`, source `0`, distance limit `2` | `[0, 1, NONE]` |
| BFS | `[[1], [2], []]`, source `0`, distance limit `2` or `1` | `[0, 1, 2]` or input error before traversal |
| BFS | `[]`, source `0`; `[[]]`, source `-1`, `1`, or `0.5` | Input error before indexing |
| BFS | `[[1], [-1]]`; `[[2], []]`; `[[], [2]]`; `[[false]]`; `[[0.5]]`, source `0` | Input error, including invalid edges in unreachable components |
| Sum | `[]`; `[7, -8]`; `[-8, 7]` | `0`; `-1`; `-1` |
| Sum | `[7, 1]`; `[-8, -1]`; `[7, 1, -1]` | Overflow error at the second addition |
| Numeric inputs | A fractional, boolean, or out-of-interval value | Input error before arithmetic |

Trace invariants and these cases after edits. For an executable translation, compare successful range queries with direct exact sums, duplicate detection with the pairwise baseline, and BFS distances with an independent shortest-path oracle on small graphs. Exhaustively compare checked arithmetic with exact arithmetic over a small declared interval. Test invalid types and indices, and ensure rejection precedes unsafe operations. Run language-appropriate analyzers and sanitizers when available; report model checks separately from implementation execution and measured performance.

## Maintenance

Responsibility: the `ops-algorithmic` package maintainer. Review when algorithm contracts, numeric assumptions, or examples change; publish material changes through the package version and Git history.
