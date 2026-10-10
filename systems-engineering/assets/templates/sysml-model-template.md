# SysML Model Views Template

<!--
Use this template to produce controlled SysML-style views in Mermaid.
BDD shows composition. IBD shows internal parts, ports, and flows.
Requirements diagram is a projection, not native SysML; declare relationship directions.
Keep names identical to the CI and requirement registers.
-->

## 1. Model frame
- System of interest:
- Abstraction level:
- Baseline / approval state:
- Notation convention and limits: illustrative Mermaid, not a native SysML export.
- Numeric properties: distinguish specified targets from demonstrated values.
- Model elements in scope:

## 2. Block definition diagram (BDD)

```mermaid
classDiagram
  class SOI {
    <<system>>
  }
  class SubsystemA {
    <<block>>
  }
  class SubsystemB {
    <<block>>
  }
  SOI *-- SubsystemA
  SOI *-- SubsystemB
```

## 3. Internal block diagram (IBD)

```mermaid
flowchart LR
  subgraph SOI[System of Interest]
    A[Subsystem A]
    B[Subsystem B]
    A -->|IF-01 item flow| B
    B -->|IF-02 status| A
  end
```

## 4. Requirements diagram

```mermaid
flowchart TB
  SYR[SYR-001] -->|source need| NEED[NEED-001]
  CI[CI or block] -->|satisfy| SYR
  VT[VT-001] -->|verify| SYR
```

## 5. Model register

| Element | SysML kind | Parent | Ports / connectors | Linked req | Notes |
|---|---|---|---|---|---|
| [name] | [system/block/itemFlow/requirement/test] | [parent] | [ids] | [ids] | [note] |

## 6. N2 sketch (optional)

|  | A | B | C |
|---|---|---|---|
| A | A | [A->B] | [A->C] |
| B | [B->A] | B | [B->C] |
| C | [C->A] | [C->B] | C |

## Minimal example

Illustrative only; not a record of execution, approval, or measured performance.

```mermaid
classDiagram
  class DeliveryUAV {
    <<system>>
    assumed_endurance_target_min : 25
  }
  class Airframe {
    <<block>>
  }
  class Avionics {
    <<block>>
  }
  class PayloadBay {
    <<block>>
  }
  DeliveryUAV *-- Airframe
  DeliveryUAV *-- Avionics
  DeliveryUAV *-- PayloadBay
```

```mermaid
flowchart LR
  subgraph UAV[Delivery UAV]
    AF[Airframe]
    AV[Avionics]
    PB[Payload Bay]
    AF -->|structural power bus IF-01| AV
    AV -->|release command IF-02| PB
    PB -->|custody status IF-03| AV
  end
```
