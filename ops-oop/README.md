# ops-OOP

This package installs an AI skill for full-lifecycle object-oriented software engineering. It uses language-neutral algorithms and pseudocode to explain object-oriented contracts. Regulated profiles are conditional and do not activate unless the project requires them.

## Main files

- `SKILL.md` - activation, workflow, decision rules, quality gates, and navigation.
- `references/01-concept-ladder.md` - didactic concept progression from basic object semantics to assurance.
- `references/02-domain-requirements-modeling.md` - requirements-to-responsibilities/domain modeling.
- `references/03-design-principles.md` - SOLID/GRASP/RDD, cohesion/coupling, inheritance/composition, LSP.
- `references/04-object-lifecycle.md` - ownership, lifetime, polymorphism, and failure guarantees.
- `references/05-patterns-and-architecture.md` - GoF force selection, DDD tactics, architecture boundaries.
- `references/06-testing-refactoring-legacy.md` - testing, contract tests, refactoring, legacy seams.
- `references/07-review-quality-gates.md` - review ordering, quality attributes, standards crosswalk.
- `references/08-regulated-profiles.md` - MISRA, AUTOSAR legacy, ISO 26262, IEC 61508, DO-178C/DO-332/DO-330.
- `references/09-output-contracts.md` - reusable design/review/refactoring/assurance output structures.

## Design decisions

- Teaching examples specify behavior independently of language; actual implementations follow the project's runtime and adopted profile.
- Bundled guidance supports hosts with or without local documentation. Apply
  available, authorized host/workspace guidance; otherwise use task requirements
  and repository evidence, stating unresolved assumptions. No documentation
  catalog or other skill is required.
- The skill prefers composition/value semantics and introduces inheritance/patterns only when forces justify them.
- Standards compliance requires exact project applicability and evidence; the skill never equates a checklist or static-analysis pass with certification.
- Canonical references are summarized and cited; licensed standards/books are not reproduced.

## Maintenance

Re-verify mutable standard editions/status before updating compliance guidance.
After edits, validate YAML metadata, bundled paths, Markdown links/anchors, and
consistent reference/level numbering. Use available, authorized host or project
checks; if tooling is absent, perform a manual structural review and report unrun
checks. Native activation and output quality require separate runtime evidence.
Repackage the complete skill directory.
