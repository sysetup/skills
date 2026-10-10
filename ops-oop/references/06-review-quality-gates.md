# OO Review and Quality Gates

Use this reference for design review, code review, quality-attribute analysis, lifecycle traceability, and architecture/requirements standards framing.

## Table of contents

- [Review order](#review-order)
- [Semantic review gates](#semantic-review-gates)
- [C++ OO review gates](#cpp-oo-review-gates)
- [Quality attributes](#quality-attributes)
- [Metrics](#metrics)
- [Standards crosswalk](#standards-crosswalk)
- [Evidence states](#evidence-states)

## Review order

Review highest-consequence issues first:

1. wrong behavior or missing requirement;
2. invalid state/invariant failure;
3. ownership/lifetime/resource defect;
4. unsafe polymorphism/substitution;
5. error/concurrency contract;
6. architecture/dependency defect;
7. changeability/testability;
8. performance/resource usage;
9. style/readability.

Do not bury correctness defects under formatting comments.

## Semantic review gates

### Responsibility

- Can each major type/module state its purpose in one sentence?
- Are domain rules located where their required information and invariants live?
- Is orchestration separated from domain decision logic when useful?

### Encapsulation

- Can clients create invalid states through public APIs?
- Do getters/setters expose representation that should remain controlled?
- Are transaction/state-machine rules enforced at the correct boundary?

### Dependency

- Does high-level policy depend directly on volatile infrastructure?
- Are interfaces introduced where there is real variation/boundary pressure?
- Are abstractions owned by the clients that need them rather than by implementation convenience?

### Substitution

- Can clients use all implementations without type tests or special cases?
- Are preconditions/error behavior/side effects compatible?
- Is destruction safe through base interfaces?

### Evolution

- Does one requirement change trigger edits across unrelated classes?
- Does a new variation require modifying central switches in many places?
- Is the chosen extension point stable enough to deserve abstraction now?

## C++ OO review gates

Inspect:

- Rule-of-Zero opportunity before custom special members;
- copy/move semantics consistent with identity/ownership;
- `unique_ptr` vs `shared_ptr` semantics;
- possible shared ownership cycles;
- borrowed views/reference lifetime;
- polymorphic base destructor correctness;
- `override` correctness and accidental hiding;
- object slicing;
- virtual calls during construction/destruction;
- exception safety and RAII;
- ABI/public-header implications when library interfaces are changed;
- thread-safety of shared mutable objects.

## Quality attributes

Use ISO/IEC 25010:2023 as a product-quality reference model when a systematic quality-attribute review is useful. Do not convert the standard into universal numeric thresholds; derive measurable acceptance criteria from system context.

For each relevant attribute ask what observable scenario defines success. Example:

`Under 2,000 concurrent checkout sessions, the pricing component shall complete p95 price calculation within 25 ms on the target deployment profile.`

A class-level elegance improvement that violates system performance, reliability, security, or portability is not an improvement.

## Metrics

Use metrics as triage signals, not verdicts:

- cyclomatic/cognitive complexity;
- coupling/fan-in/fan-out;
- inheritance depth;
- class/module size;
- change frequency/churn;
- defect concentration;
- test coverage.

Investigate outliers in context. Avoid universal thresholds such as "class > N lines is bad" without empirical/project justification.

## Standards crosswalk

These standards frame lifecycle and evidence; they do not prescribe one OO design method.

| Need | Primary reference | How this skill uses it |
|---|---|---|
| software lifecycle process | ISO/IEC/IEEE 12207:2026 | place OO work inside development, operation, maintenance, disposal and supporting processes |
| system lifecycle context | ISO/IEC/IEEE 15288:2023 | connect software design to system-level lifecycle/stakeholder context |
| requirements engineering | ISO/IEC/IEEE 29148:2018 | trace responsibilities/design to requirements; verify current edition before compliance claims |
| architecture descriptions | ISO/IEC/IEEE 42010:2022 | organize architecture concerns, stakeholders, viewpoints/views and rationale |
| product quality | ISO/IEC 25010:2023 | structure quality-attribute requirements/evaluation |
| lifecycle documentation | ISO/IEC/IEEE 15289:2019 | structure information items when project governance requires it |
| software engineering body of knowledge | SWEBOK Guide V4.0a | broader consensus map; not a normative standard |
| OO notation | OMG UML 2.5.1 | communication/modeling notation when useful |

Standards applicability must be established by the project. A standards citation is not compliance evidence.

## Evidence states

For significant reviews distinguish:

- **proposed:** design/check not yet executed;
- **implemented:** change exists in code/design artifact;
- **tested:** specified test/check executed with recorded result;
- **reviewed:** independent or designated review performed;
- **accepted:** authorized project role accepted the evidence/change.

Do not collapse these into a generic "done" state in high-assurance work.
