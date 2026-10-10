# Design Review Checklist Template

<!--
Use this checklist to prepare for SDR, PDR, CDR, and FQR.
Delete irrelevant rows for a given review. Keep action items and evidence references explicit.
-->

| Review | Check item | Evidence reference | Status | Action owner |
|---|---|---|---|---|
| SDR | mission, constraints, context, and lifecycle concepts are coherent | [ref] | [open/closed] | [owner] |
| SDR | STRS -> SyRS traceability is complete enough to baseline | [ref] | [open/closed] | [owner] |
| PDR | subsystem partition and CI strategy are defensible | [ref] | [open/closed] | [owner] |
| PDR | major interfaces are identified and controlled | [ref] | [open/closed] | [owner] |
| CDR | detailed design is complete enough for build | [ref] | [open/closed] | [owner] |
| CDR | production or construction data is ready | [ref] | [open/closed] | [owner] |
| FQR | acceptance evidence supports customer acceptance | [ref] | [open/closed] | [owner] |
| FQR | transition-to-service enablers are ready | [ref] | [open/closed] | [owner] |

## Minimal example

Illustrative only; not a record of execution, approval, or measured performance.

| Review | Check item | Evidence reference | Status | Action owner |
|---|---|---|---|---|
| PDR | reporting subsystem interface to communications network is defined | ICD-02 | open | subsystem lead |
| CDR | installation wiring schedule matches product baseline | expected DWG-145; not inspected | open | chief engineer |

Record reviewer, scope, version, date, actual decision, and acceptance authority before closing
a check. Passing a checklist does not authorize a baseline or prove system-level compliance.
