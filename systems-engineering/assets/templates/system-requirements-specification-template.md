# System Requirements Specification (SyRS) Template

<!--
Use this template for the controlled system-level requirements package.
Keep statements testable. Include verification and rationale. Group by RBS area.
-->

## 1. Purpose and scope
- System of interest:
- Mission:
- Boundaries and exclusions:

## 2. External systems and operating context
- Environment summary:
- External systems:
- External interface list:

## 3. Requirement register

Write each statement as `[subject] shall [verb] [object] [conditions] [measure]`.
One obligation per row. Name a feasible verification method.

| ID | RBS area | Type | Requirement statement | Source | Parent | Origin | Approval | Verification method | Rationale |
|---|---|---|---|---|---|---|---|---|---|
| SYR-001 | [area] | [functional/non-functional/interface/etc.] | [statement] | [source/locator] | [parent] | [elicited/derived/assumed] | draft | [test/analysis/inspection/demonstration] | [rationale] |

## 4. Verification cross-reference

| Requirement ID | Verification event | Method | Success criteria | Expected evidence | Actual evidence | State | Result |
|---|---|---|---|---|---|---|---|
| SYR-001 | [event] | [method] | [criteria] | [planned record] | none | planned | not-run |

## Minimal example

Illustrative only; not a record of execution, approval, or measured performance.

| ID | RBS area | Type | Requirement statement | Source | Parent | Origin | Approval | Verification method | Rationale |
|---|---|---|---|---|---|---|---|---|---|
| SYR-001 | detect intrusion | functional | The system shall detect the approved test intrusion at each access point in AP-LIST-01 within 2 seconds under ENV-01 | example source | STR-004 | illustrative | draft | test | core mission function |
| SYR-002 | report alarm | interface | The system shall transmit alarm status to the monitoring agent over IF-ALARM-01 within 5 seconds of detection under ENV-01 | example source | STR-007 | illustrative | draft | demonstration | enables response |

The numeric limits and referenced lists in this minimal example are illustrative proposals.
Define the missing source, parent, test profiles, interfaces, and approval before actual use.
