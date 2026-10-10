# Output Contracts

Use these structures when the user requests a substantial OO engineering artifact. Adapt rather than forcing every section.

## Table of contents

- [OO design proposal](#oo-design-proposal)
- [Code/design review](#codedesign-review)
- [Refactoring plan](#refactoring-plan)
- [Domain model](#domain-model)
- [Regulated assessment](#regulated-assessment)
- [Traceability matrix](#traceability-matrix)

## OO design proposal

```markdown
# [Feature/System] OO Design

## Context and constraints
- purpose / scenario
- language/runtime/toolchain
- quality attributes
- external interfaces

## Requirements and design forces
| ID | Requirement/force | Source | Priority |

## Domain/object model
| Type/module | Role | Invariant | Ownership/lifetime | Collaborators |

## Contracts
- public interfaces
- pre/postconditions
- error semantics
- concurrency assumptions

## Key interactions
[sequence/state description]

## Alternatives and trade-offs
| Option | Advantages | Costs/Risks | Decision |

## Verification
- tests
- static/dynamic analysis
- integration checks

## Open issues and risks
```

## Code/design review

Order findings by semantic risk.

```markdown
# OO Review

## Scope
## Critical findings
### [ID] [Short title]
- Evidence: file/symbol/behavior
- Problem: violated invariant/ownership/contract/etc.
- Consequence: observable risk
- Repair: concrete design/code change
- Verification: test/check that proves the repair

## Important design findings
## Maintainability/testability findings
## Positive constraints worth preserving
## Checks performed and limitations
```

Do not label taste preferences as critical findings.

## Refactoring plan

```markdown
# Refactoring Plan

## Behavior to preserve
## Risk map
## Existing tests/evidence
## Seam to establish
## Steps
1. transformation
   - expected behavior: unchanged
   - verification: ...
   - rollback point: ...
## Final design target
## Deferred improvements
```

## Domain model

```markdown
# Domain Model

## Ubiquitous language
| Term | Meaning | Ambiguity to avoid |

## Concepts
| Concept | Kind (value/entity/service/event) | Identity | Invariant |

## Responsibilities and collaborators
## State transitions
## Aggregate/consistency boundaries (if DDD is warranted)
## Persistence/infrastructure boundary
## Scenario walkthroughs
```

## Regulated assessment

```markdown
# OO Assurance Assessment

## Applicability
- governing standard/profile + exact edition
- assurance level
- language subset/version
- project tailoring

## Evidence register
| Requirement/rule/objective | Artifact/evidence | State | Result | Gap/deviation | Owner/approval |

## OO-specific concerns
## Toolchain/static-analysis status
## Verification and independence needs
## Open compliance gaps
```

Never use this template to claim certification. It organizes evidence and gaps.

## Traceability matrix

```markdown
| Requirement | Domain rule | Responsibility | Type/module | Operation | Test/evidence | Status |
|---|---|---|---|---|---|---|
```

A trace link is valid only when the downstream artifact actually satisfies the upstream obligation; matching names/IDs alone is insufficient.
