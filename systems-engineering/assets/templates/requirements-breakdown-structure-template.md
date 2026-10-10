# Requirements Breakdown Structure (RBS) Template

<!--
Use this template to decompose mission -> goals -> objectives -> lower-level functions.
Keep each node verb-based and unique. Use hierarchical numbering. Keep child sets small enough to reason about.
Map each leaf to requirement IDs and verification intent.
-->

## Blank structure

- 0.0 **Mission** — [state the system purpose in one sentence]
  - 1.0 [major function or goal]
    - 1.1 [sub-function or objective]
      - 1.1.1 [leaf function]
      - 1.1.2 [leaf function]
    - 1.2 [sub-function or objective]
  - 2.0 [major function or goal]
  - 3.0 [major function or goal]

## Node register

| RBS node | Verb phrase | Parent | Source type (elicited/decomposed/derived) | Requirement IDs | Verification note | Rationale |
|---|---|---|---|---|---|---|
| 0.0 | [mission] | - | elicited | [ids] | [note] | [note] |
| 1.0 | [major function] | 0.0 | [type] | [ids] | [note] | [note] |

## Minimal example

Illustrative only; not a record of execution, approval, or measured performance.

- 0.0 **Protect residence**
  - 1.0 Deter intrusion
  - 2.0 Detect entry
    - 2.1 Sense breach
    - 2.2 Confirm event
  - 3.0 Classify event
  - 4.0 Report alarm
  - 5.0 Support owner use
