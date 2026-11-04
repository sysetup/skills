# ops-OOP

This package installs an AI skill for full-lifecycle object-oriented software engineering. It uses language-neutral algorithms and pseudocode to explain object-oriented contracts. Regulated profiles are conditional and do not activate unless the project requires them.

## Main files

- `SKILL.md` - activation, workflow, decision rules, quality gates, and navigation.
- `references/00-concept-ladder.md` - didactic concept progression from basic object semantics to assurance.
- `references/01-domain-requirements-modeling.md` - requirements-to-responsibilities/domain modeling.
- `references/02-design-principles.md` - SOLID/GRASP/RDD, cohesion/coupling, inheritance/composition, LSP.
- `references/03-object-lifecycle.md` - ownership, lifetime, polymorphism, and failure guarantees.
- `references/04-patterns-and-architecture.md` - GoF force selection, DDD tactics, architecture boundaries.
- `references/05-testing-refactoring-legacy.md` - testing, contract tests, refactoring, legacy seams.
- `references/06-review-quality-gates.md` - review ordering, quality attributes, standards crosswalk.
- `references/07-regulated-profiles.md` - MISRA, AUTOSAR legacy, ISO 26262, IEC 61508, DO-178C/DO-332/DO-330.
- `references/09-output-contracts.md` - reusable design/review/refactoring/assurance output structures.

## Design decisions

- Teaching examples specify behavior independently of language; actual implementations follow the project's runtime and adopted profile.
- The skill prefers composition/value semantics and introduces inheritance/patterns only when forces justify them.
- Standards compliance requires exact project applicability and evidence; the skill never equates a checklist or static-analysis pass with certification.
- Canonical references are summarized and cited; licensed standards/books are not reproduced.

## Maintenance

Re-verify mutable standard editions/status before updating compliance guidance. Run the host's canonical skill preflight/evaluation tooling after edits, then repackage the complete skill.
