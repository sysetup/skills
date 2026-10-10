# Interface Control Document (ICD) Template

<!--
Use this template for one controlled interface between two named parties.
Keep it consistent with the context-diagram register (external) or the IBD (internal).
-->

## 1. Identification
- Interface ID:
- Interface name:
- Version / date:
- Baseline / approval state:
- Source and authority for proposed limits:
- Party A (name, role, owner):
- Party B (name, role, owner):
- Direction:
- Exchange type (data / energy / material / mechanical / human / service):

## 2. Purpose and related requirements
- Why the interface exists:
- Linked requirement IDs:
- Linked context or IBD connector IDs:

## 3. Physical or medium definition
- Mating / connector / medium:
- Location:
- Environmental limits at the interface:
- Safety or isolation constraints:

## 4. Functional / logical definition
- Protocol or sequence:
- Message, fluid, power, or mechanical characteristics:
- Timing, rate, latency, or throughput:
- Units, ranges, and validity:
- Error, timeout, and degraded-mode behavior:

## 5. Control and security
- Authentication / authorization if applicable:
- Integrity or safety interlocks:
- Who may change the interface:

## 6. Verification
- Method:
- Success criteria:
- Event ID:
- Expected evidence:
- Actual evidence locator (none until obtained):
- State / result:
- Run configuration, review record, and acceptance authority:

## 7. Open items

| ID | Description | Owner | Need date | Status |
|---|---|---|---|---|
| ICD-OI-001 | [item] | [owner] | [date] | [open/closed] |

## Minimal example

Illustrative only; not a record of execution, approval, or measured performance.

- Interface ID: IF-AV-PB-01
- Name: payload-release command
- Party A: avionics CI (command source)
- Party B: payload CI (release actuator)
- Direction: A -> B command; B -> A status
- Exchange type: data + discrete inhibit
- Protocol: 50 Hz command word; release allowed only when geo-fence valid AND inhibit discrete is inactive
- Timing: command-to-release ≤ 200 ms
- Error: invalid command is rejected; status = `REJECTED`; no mechanical motion
- Verification: test VT-014 command-and-inhibit test
- Linked requirements: SYR-014 (timing), SYR-015 (inhibit), SYR-016 (invalid command); define these obligations in the project register.
- State / result: planned / not-run; actual evidence: none.
- All numeric limits and the interface design above are illustrative assumptions pending approval.
