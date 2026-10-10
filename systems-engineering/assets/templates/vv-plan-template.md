# Verification and Validation Plan Template

Verification addresses specifications; validation addresses stakeholder needs in intended use.
Treat the V-model as a planning relation, not proof that activities occurred.

## 1. Scope
- System / lifecycle phase:
- Requirement baseline and approval state:
- Configuration under test and procedure version:
- Authority, sample plan, environment, exclusions, and applicable DT&E / AT&E / OT&E categories:

## 2. V-model map

| Left-side product | Requirement IDs | Right-side activity | Method | Event ID |
|---|---|---|---|---|
| [need/STR/SyRS/subsystem spec/CI design] | [ids] | [validation/system/subsystem/CI verification/integration] | [inspection/analysis/test/demonstration] | [event] |

## 3. Verification event register

| Event ID | Requirement ID | Method | Procedure / setup | Success criteria | Environment / limitations | Expected evidence | Actual evidence | State | Result |
|---|---|---|---|---|---|---|---|---|---|
| VT-001 | [id] | [method] | [procedure/version] | [measurable criteria] | [envelope/sample/limits] | [planned artifact] | none | planned | not-run |

## 4. Validation questions and events

| Validation ID | Stakeholder need | How we will know the need is met | Related verification events | Residual uncertainty | Expected evidence | Actual evidence | State | Result |
|---|---|---|---|---|---|---|---|---|
| VAL-001 | [need] | [operational criterion and approved sample plan] | [events] | [limits] | [record] | none | planned | not-run |

Do not place a validation-question row beneath the verification-register header. Validation can
also use a full event-register row when its own method, setup, criteria, and scope are provided.

## 5. Execution, review, and acceptance records

| Event ID | Run record | Run date | Configuration | Review record | Acceptance record |
|---|---|---|---|---|---|
| VT-001 | none | none | [configuration/version] | none | none |

Use proposed/planned/executed/checked/accepted/superseded and not-run/pass/fail/inconclusive.
A checked result can fail. Accepted evidence requires the authorized decision, not an agent's
self-approval. Preserve unsuccessful runs and retests separately. See reference 12.

## 6. Optional automated coverage contract for complete packages

Copy the source/need/requirement registers into or link them from the delivered package. A
self-contained checked example is in `tests/e2e-delivery-uav.md`.
Declare one row per obligation; compare it to the original requirement before running the checker.

| Requirement ID | Obligation ID | Observable | Trigger | Interface ID | Comparator | Limit | Unit | Conditions |
|---|---|---|---|---|---|---|---|---|
| [requirement] | [unique obligation] | [observable] | [start/stop] | [interface or none] | [<=/>=/==] | [value/state] | [unit] | [defined envelope] |

| Event ID | Requirement ID | Obligation ID | Observable | Trigger | Interface ID | Comparator | Limit | Unit | Conditions |
|---|---|---|---|---|---|---|---|---|---|
| [event] | [requirement] | [obligation] | [actually measured observable] | [actually measured trigger] | [actual interface or none] | [comparator] | [limit] | [unit] | [actual conditions] |

## 7. Entry, exit, and failure controls
- Entry: required approval, calibrated tools, authorized safe setup, baselines, procedure, criteria.
- Exit: criterion-level results, anomalies and dispositions, review records, remaining uncertainty.
- Failure: preserve results, record corrective action and authority, create a separate retest record.
- Coverage summary: gap / partial / planned / verified / accepted; do not combine these counts.

## Minimal example (illustrative, not an executed test)

| Event ID | Requirement ID | Method | Procedure / setup | Success criteria | Environment / limitations | Expected evidence | Actual evidence | State | Result |
|---|---|---|---|---|---|---|---|---|---|
| VT-001 | SYR-001 | test | Measure dispatch-to-custody time over a 5 km route with 1.5 kg payload | <= 20 min per run | dry daylight; wind <= 8 m/s; sample plan pending approval | FT-001 | none | planned | not-run |

| Validation ID | Stakeholder need | How we will know the need is met | Related verification events | Residual uncertainty | Expected evidence | Actual evidence | State | Result |
|---|---|---|---|---|---|---|---|---|
| VAL-001 | NEED-001 timely medical delivery | clinician custody <= 20 min on 10 of 10 proposed trials | VT-001 | sample plan unapproved; no lifetime reliability claim | OT-001 | none | planned | not-run |
