# Traceability Matrix Template

Preserve source, parent, allocation, interface, verification, evidence, and approval state. Check
what each linked artifact actually says. An ID link or a planned event is not demonstrated compliance.

## Need to architecture to test

| Need ID | Requirement ID | Architecture / CI | Interface ID | Test / V&V event | Method | Coverage |
|---|---|---|---|---|---|---|
| [need] | [requirement] | [ci/block] | [interface or none] | [event or none] | [method] | [gap/partial/planned/verified/accepted] |

Use `planned` only when the full obligation has an adequate verification plan. Use `verified`
only after matching actual results are checked and pass; acceptance also needs an authorized
record. Use `partial` for incomplete facet coverage. Avoid the ambiguous standalone word "covered".

## Forward traceability

| Parent ID | Parent statement | Child / allocated ID | Relationship | Verification method | Notes |
|---|---|---|---|---|---|
| [id] | [statement] | [id] | [decompose/derive/allocate] | [method] | [rationale/approval] |

## Backward traceability

| Child ID | Child statement | Parent ID(s) | Why child exists | Baseline affected | Notes |
|---|---|---|---|---|---|
| [id] | [statement] | [parents] | [reason] | [version] | [approval/limits] |

## Coverage review
- Check requirement/test subject, observable, trigger, direction, interface, limit, unit, conditions.
- Check every facet and preserve unresolved facets as gaps.
- Parents with no child and children with no parent:
- Requirements with no plan / partial plan / complete plan:
- Requirements with checked passing evidence / authorized acceptance:
- Source and baseline versions; evidence locators; unresolved conflicts and owners:

## Minimal example (illustrative, no actual flight evidence)

| Need ID | Requirement ID | Architecture / CI | Interface ID | Test / V&V event | Method | Coverage |
|---|---|---|---|---|---|---|
| NEED-001 | SYR-001 | Airframe + Avionics | none | VT-001 | test | planned |

This row is a format example only. A self-contained coverage contract and complete definitions
are required for automated relationship checks; see `tests/e2e-delivery-uav.md`.
