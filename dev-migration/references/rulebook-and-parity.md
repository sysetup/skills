# Rulebook, gap inventory, and parity judge guide

Load this reference before translating code to establish the behavioral referee, author the migration rulebook and gap inventory in the correct order, and run the disposable stress test.

## Prerequisite: build and validate the parity judge

Never start translating without an objective mechanical judge that evaluates the original and target implementations on equal terms. The original codebase is the executable ground truth, including undocumented quirks unless the requester approves an explicit behavioral delta.

1. **Categorize existing tests**: Separate tests expressible through external interfaces (CLI, API, library boundary, fixtures) from tests coupled to source-language internals that will not exist after the port.
1. **Port or construct the harness**:
    - When external tests exist, adapt them into a language-agnostic parity harness (black-box runner, golden files, or differential script) comparing outputs, exit codes, error classes, and observable side effects from equivalent clean state.
    - When tests are missing or sparse, build characterization tests and real-world scenario fixtures directly from the running original. For stateful or numerical systems, add temporary non-invasive probes or state checkpoints to verify intermediate invariants as well as final outputs.
    - Sanitize all fixtures and golden payloads to remove credentials, tokens, internal hosts, and PII.
1. **Prevent assertion weakening and self-grading**: Have an independent review pass verify that adapted tests did not weaken assertions, drop boundary cases, or assume target bugs. Never let the same agent context that translates a slice author post-hoc tests as the sole proof of parity.
1. **Mutation-validate the judge**:
    - Run the judge against the unmodified original and confirm every scoped parity check passes.
    - Run the judge against a deliberately broken variant (changed output, exit code, or edge case) and confirm it fails. A judge that cannot catch breakage blocks translation.

## Step order: rulebook before gap inventory

Author the rulebook first, then build the gap inventory for every construct the rulebook's defaults cannot handle cleanly, and audit both together before translating. Front-load human architectural decisions here so downstream execution looks up rules instead of improvising.

### Author the rulebook (`RULEBOOK.md` in target workspace)

Shape the rulebook to the confirmed `Architecture mode` and incorporate applicable target-language style, lint, and security conventions from the workspace or host standards:

- **`structural-port`**: Concrete lookup tables mapping source types, error handling, memory/resource lifecycle, nullability, concurrency, module layout, logging, and standard-library equivalents to target idioms, plus explicit pointers to the gap inventory for hard boundaries.
- **`idiomatic-redesign`**: Target architecture design document specifying module boundaries, explicit interfaces and data contracts, target-language idioms (avoiding literal line-by-line carryover of legacy anti-patterns), error taxonomy, and migration pipeline stages (symbol resolution, semantic/type enrichment, structural transformation, idiom mapping).
- **Explicit ambiguity policy**: Require translators to mark any case uncovered by the rulebook with `TODO(port): <reason>` and add an `UNKNOWN` row to the gap inventory rather than guessing silently.

### Build the gap inventory (`gap-inventory.tsv` or Markdown table in target workspace)

Catalog every structural mismatch where target-language requirements exceed source guarantees:

| Gap class | Concrete examples to inventory |
| --- | --- |
| Memory and ownership | Manual allocation/free versus ownership, lifetimes, borrowing, or garbage collection |
| Contracts and typing | Dynamic duck-typing or implicit dicts versus explicit interfaces, algebraic types, or strict nullability |
| Semantic edge cases | Integer overflow, floating-point precision, string encoding, timezone/locale handling, regex dialect, map iteration order |
| Runtime and state | Global mutable state, cyclic imports, lazy evaluation, implicit initialization order, signal or transaction boundaries |
| External boundaries | FFI/C ABI seams, `unsafe` isolation requirements, serialization formats, OS-specific syscalls |

### Joint skeptic audit

Before running the stress test, inspect the dependency map, rulebook, and gap inventory together with an adversarial skeptic pass checking for:

- Contradictory translation rules or unmapped gap classes.
- Unresolved cyclic dependencies in the planned slice order.
- Implicit architectural changes lacking requester approval.
- Missing security defaults (unsafe pointer usage, unchecked deserialization, disabled TLS verification, unbounded allocations).

## Disposable stress test (shakedown cruise)

Test the rules on a small, high-risk subset before fanning out across the codebase.

- **`structural-port`**: Select 3–5 representative risky files (or 1 representative unit in `lightweight` scale). Translate them strictly using the rulebook, independently produce an idiomatic senior-level target translation of the same files, diff both results, and turn every meaningful gap or friction point into a concrete rulebook amendment.
- **`idiomatic-redesign`**: Challenge the design document with adversarial review against the hardest gap-inventory items, then run one disposable end-to-end vertical slice through the parity judge to verify interfaces, build ergonomics, and performance assumptions.
- **Mandatory discard rule**: Throw away the disposable stress-test code after extracting rule updates. The stress test refines the process and rules; it is not incremental production code.
