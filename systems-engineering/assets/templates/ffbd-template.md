# Functional Flow Block Diagram (FFBD) Template

<!--
Use this template to capture sequence, branching, concurrency, and interface-sensitive behavior.
Number functions consistently with the RBS. Keep one level readable at a time.
Use the function table to capture inputs, outputs, and interfaces.
-->

## Blank Mermaid draft

```mermaid
flowchart LR
  A[1.0 Start scenario] --> B[2.0 Perform function]
  B --> C{3.0 Decision or event?}
  C -->|yes| D[4.0 Alternative path]
  C -->|no| E[5.0 Normal path]
  D --> F[6.0 End state]
  E --> F
```

## Function table

| Node | Function | Predecessor | Successor | Trigger/Input | Output | Interface/Actor |
|---|---|---|---|---|---|---|
| 1.0 | [function] | - | [node] | [input] | [output] | [interface] |

## Minimal example

Illustrative only; not a record of execution, approval, or measured performance.

```mermaid
flowchart LR
  A[1.0 Arm alarm] --> B[2.0 Vacate premises]
  B --> C{3.0 Entry occurs?}
  C -->|yes| D[4.0 Detect breach]
  D --> E[5.0 Classify alarm]
  E --> F[6.0 Report to monitoring agent]
```
