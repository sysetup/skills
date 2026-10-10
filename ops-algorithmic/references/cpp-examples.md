# C++20 Canonical Examples

Each example emphasizes algorithm selection before syntactic polish. Blocks marked `compile-example` are standalone and are checked by `scripts/verify_cpp_examples.py`.

## 1. Remove an avoidable quadratic duplicate search

### Baseline: clear but quadratic

The nested loops are readable, but they perform O(n^2) comparisons in the worst case.

```cpp compile-example
#include <cstddef>
#include <vector>

bool hasDuplicateQuadratic(const std::vector<int>& values) {
    for (std::size_t i = 0; i < values.size(); ++i) {
        for (std::size_t j = i + 1; j < values.size(); ++j) {
            if (values[i] == values[j]) {
                return true;
            }
        }
    }
    return false;
}

int main() {
    return hasDuplicateQuadratic({1, 2, 3, 2}) ? 0 : 1;
}
```

### Algorithm-first improvement: expected linear time

Use a hash set when extra memory and expected-time hashing are acceptable. The algorithm becomes expected O(n) time and O(n) auxiliary space.

```cpp compile-example
#include <unordered_set>
#include <vector>

bool hasDuplicate(const std::vector<int>& values) {
    std::unordered_set<int> seen;
    seen.reserve(values.size());

    for (int value : values) {
        if (!seen.insert(value).second) {
            return true;
        }
    }
    return false;
}

int main() {
    return hasDuplicate({1, 2, 3, 2}) ? 0 : 1;
}
```

Do not call the hash version universally superior. If memory is constrained, deterministic worst-case behavior is required, or n is tiny and tightly bounded, sorting or even the simple baseline can be justified.

## 2. Amortize repeated range-sum queries

If q queries each scan up to n elements, the direct approach is O(qn). Prefix sums pay O(n) once and answer each query in O(1), for O(n + q) total time.

```cpp compile-example
#include <cassert>
#include <cstddef>
#include <vector>

class PrefixSum {
public:
    explicit PrefixSum(const std::vector<long long>& values)
        : prefix_(values.size() + 1, 0) {
        for (std::size_t i = 0; i < values.size(); ++i) {
            prefix_[i + 1] = prefix_[i] + values[i];
        }
    }

    // Returns the sum over the half-open interval [left, right).
    long long range(std::size_t left, std::size_t right) const {
        assert(left <= right);
        assert(right < prefix_.size());
        return prefix_[right] - prefix_[left];
    }

private:
    std::vector<long long> prefix_;
};

int main() {
    PrefixSum sums({3, -1, 4, 2});
    return sums.range(1, 4) == 5 ? 0 : 1;
}
```

The comment records the non-obvious interval convention; it does not narrate syntax.

## 3. Preserve a loop invariant explicitly

Binary search is O(log n), but boundary mistakes are common. Use a half-open interval invariant: the target, if present, remains within `[low, high)`.

```cpp compile-example
#include <cstddef>
#include <optional>
#include <vector>

std::optional<std::size_t> binarySearch(
    const std::vector<int>& sorted,
    int target) {
    std::size_t low = 0;
    std::size_t high = sorted.size();

    // Invariant: if target exists, at least one occurrence is in [low, high).
    while (low < high) {
        const std::size_t mid = low + (high - low) / 2;
        if (sorted[mid] < target) {
            low = mid + 1;
        } else {
            high = mid;
        }
    }

    if (low < sorted.size() && sorted[low] == target) {
        return low;
    }
    return std::nullopt;
}

int main() {
    const std::vector<int> values{1, 3, 3, 7, 9};
    const auto found = binarySearch(values, 3);
    return found && *found == 1 ? 0 : 1;
}
```

## 4. Prefer explicit control flow over a confusion-prone expression

A short-circuit expression can be legal yet conceal that it is being used for control flow.

### Avoid when control flow is the real intent

```cpp compile-example
#include <vector>

void appendIfEnabled(bool enabled, std::vector<int>& out) {
    enabled && (out.push_back(42), true);
}

int main() {
    std::vector<int> out;
    appendIfEnabled(true, out);
    return out.size() == 1 ? 0 : 1;
}
```

### Prefer

```cpp compile-example
#include <vector>

void appendIfEnabled(bool enabled, std::vector<int>& out) {
    if (enabled) {
        out.push_back(42);
    }
}

int main() {
    std::vector<int> out;
    appendIfEnabled(true, out);
    return out.size() == 1 ? 0 : 1;
}
```

Both are O(1). The advantage is human interpretation, not asymptotic speed.

## 5. Select graph representation from density and operations

For a sparse graph, adjacency lists keep traversal at O(V + E) storage/time. A V x V boolean matrix can be appropriate when the graph is dense or constant-time edge existence dominates and memory permits it.

```cpp compile-example
#include <cstddef>
#include <queue>
#include <vector>

std::vector<int> bfsDistances(
    const std::vector<std::vector<std::size_t>>& graph,
    std::size_t source) {
    std::vector<int> distance(graph.size(), -1);
    std::queue<std::size_t> frontier;

    distance[source] = 0;
    frontier.push(source);

    while (!frontier.empty()) {
        const std::size_t node = frontier.front();
        frontier.pop();

        for (std::size_t next : graph[node]) {
            if (distance[next] == -1) {
                distance[next] = distance[node] + 1;
                frontier.push(next);
            }
        }
    }
    return distance;
}

int main() {
    const std::vector<std::vector<std::size_t>> graph{{1, 2}, {2}, {3}, {}};
    const auto d = bfsDistances(graph, 0);
    return d[3] == 2 ? 0 : 1;
}
```

## 6. Do not confuse asymptotic dominance with finite-input speed

Insertion sort is O(n^2), while a comparison sort such as `std::sort` is O(n log n). For large arbitrary inputs, the latter has superior growth. Yet tiny nearly sorted arrays may favor a simple quadratic routine because constants and locality dominate.

The engineering decision must state the size regime. If a hard contract guarantees `n <= 16`, a small simple algorithm can be rational. If n can grow to millions, accepting O(n^2) because the code looks simpler is usually indefensible.

## 7. Make numeric overflow part of correctness

Do not let an O(n) algorithm be "fast" but wrong because the accumulator type is too narrow.

```cpp compile-example
#include <cstdint>
#include <vector>

std::int64_t sumValues(const std::vector<std::int32_t>& values) {
    std::int64_t total = 0;
    for (std::int32_t value : values) {
        total += value;
    }
    return total;
}

int main() {
    const auto result = sumValues({2'000'000'000, 2'000'000'000});
    return result == 4'000'000'000LL ? 0 : 1;
}
```

Algorithmic quality includes semantic correctness under numeric limits.
