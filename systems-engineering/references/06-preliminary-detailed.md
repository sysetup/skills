# 06 Preliminary and Detailed Design

## Contents
- [Use this reference when](#use-this-reference-when)
- [Entry condition](#entry-condition)
- [Purpose of preliminary design](#purpose-of-preliminary-design)
- [Core tasks in preliminary design](#core-tasks-in-preliminary-design)
- [COTS, MOTS, or new development](#cots-mots-or-new-development)
- [Design-space management](#design-space-management)
- [Preliminary-design outputs](#preliminary-design-outputs)
- [Allocated baseline](#allocated-baseline)
- [PDR: preliminary design review](#pdr-preliminary-design-review)
- [Purpose of detailed design and development](#purpose-of-detailed-design-and-development)
- [Core tasks in detailed design](#core-tasks-in-detailed-design)
- [Detailed-design outputs](#detailed-design-outputs)
- [Product baseline](#product-baseline)
- [CDR: critical design review](#cdr-critical-design-review)
- [Typical failure patterns](#typical-failure-patterns)

## Use this reference when

Use this file when the user's problem has moved beyond system-level requirements and now concerns
subsystems, configuration items, interfaces, make-buy-modify decisions, allocated baselines,
PDR, detailed design, product baselines, or CDR readiness.

## Entry condition

Enter this phase only after the functional baseline is stable enough to allocate. Conceptual
design should already have produced a coherent SyRS and a preferred system-level solution
approach.

## Purpose of preliminary design

Preliminary design converts the functional baseline into an upper-level physical description of
the system. It is the bridge from logical architecture to physical architecture.

## Core tasks in preliminary design

### 1. identify subsystems and configuration items

Partition the system into realizable elements that can carry responsibility for sets of allocated
requirements. Select hardware, software, or other configuration items where formal control is needed.

### 2. allocate requirements downward

Allocate system-level requirements to subsystems and configuration items while maintaining
traceability. Expect the result to be subsystem-level requirement sets and development
specifications.

### 3. identify internal and external interfaces

Capture:
- physical interfaces;
- electrical interfaces;
- hydraulic or pneumatic interfaces;
- data and communication interfaces;
- human interaction interfaces.

External interfaces were exposed during conceptual design. Internal interfaces become much more
explicit here because they now constrain the realizable subsystem designs.

Capture each controlled exchange in an ICD using `assets/templates/icd-template.md`. Keep ICD
IDs consistent with the context-diagram register and the IBD connectors. Procedure detail lives
in `references/11-mbse-interfaces-vv.md`.

### 4. preserve traceability and control requirements creep

Use forward traceability to show where every system requirement is carried into the subsystem
structure.

Use backward traceability to prove that every subsystem requirement exists for an endorsed system
reason.

Reject features that make a subsystem impressive at the expense of system balance.

### 5. explore realization options for each subsystem

For each subsystem, decide whether to:
- procure off the shelf;
- modify an off-the-shelf item;
- develop from scratch.

## COTS, MOTS, or new development

### COTS

Potential advantages, to be confirmed with current supplier and integration evidence:
- known function and performance;
- known lead time and cost;
- existing support arrangements;
- existing tooling, training, test equipment, and spares.

Watch-outs:
- weak technical data;
- hidden integration limits;
- obsolescence risk;
- support market collapse.

### MOTS

Treat modification as real detailed design, not as a minor administrative step.

Watch-outs:
- invalidated warranty or support agreements;
- underestimated engineering effort;
- unavailable design data for the original item;
- unclear ownership of modified configuration.

### New development

Advantages:
- best theoretical fit to the requirement set;
- control over interfaces and design intent.

Watch-outs:
- time and cost exposure;
- immature technology or production methods;
- support system must be created, not assumed;
- an imperfect development result may still be worse than the near-fit COTS item it replaced.

## Design-space management

Do not let subsystem teams optimize in isolation. Use the whole-system constraint set to trade
room between subsystems.

Examples of design-space variables:
- weight;
- power;
- bandwidth;
- processing margin;
- physical space;
- thermal budget;
- cost;
- schedule margin.

Reallocate design space deliberately when one subsystem can still meet its requirement with margin
that another subsystem needs.

## Preliminary-design outputs

Expect a package resembling:
- subsystem decomposition;
- configuration-item list;
- allocated requirements;
- interface definitions;
- realization decisions for each subsystem;
- design rationale and option history;
- subsystem development specifications;
- allocated baseline package.

## Allocated baseline

The **allocated baseline** controls the approved functional/performance/interface requirements
allocated to configuration items, including verification criteria. Preliminary design supports
this allocation; physical design documentation alone is not the allocated requirement baseline.

## PDR: preliminary design review

Use PDR to determine whether the upper-level physical design is ready to enter detailed design.

Check at least:
- subsystem partition logic;
- adequacy of allocated requirements;
- interface definition maturity;
- option analysis and rationale;
- consistency with the functional baseline;
- technical risk exposure;
- manufacturability, maintainability, supportability, and disposability considerations.

Ask explicit questions such as:
- What other options were considered?
- Why was this one preferred?
- Which life-cycle issues influenced the choice?
- Which interfaces remain risky or immature?

## Purpose of detailed design and development

Detailed design completes the realization of the subsystems that must be modified or developed,
and it defines the integration needed to bring all subsystems together into the final system.

## Core tasks in detailed design

### 1. perform iterative engineering

Expect repeated design -> build -> test -> learn cycles. Detailed design is inherently iterative.
Do not pretend first-pass perfection.

### 2. use engineering aids

Use whichever tools fit the domain:
- prototypes;
- models;
- simulations;
- layout tools;
- reuse of proven designs;
- engineering analyses.

### 3. integrate the subsystem designs

Do not stop at local subsystem adequacy. Confirm that the integration of all subsystems still
satisfies the system requirement set.

### 4. define realization details

For hardware or mixed systems, define:
- parts lists;
- materials;
- process specifications;
- manufacturing or construction methods;
- detailed interface layouts;
- detailed support-enabling data.

For software-intensive systems, the analogous detailed build, integration, test, and release data
must be just as controlled.

## Detailed-design outputs

Expect a package resembling:
- finalized subsystem design documentation;
- detailed drawings, models, or code-level design data;
- parts, materials, and process specifications;
- interface control detail;
- integration approach;
- prototype and test evidence;
- production-ready design package.

## Product baseline

The **product baseline** captures the final detailed description of what will actually be built,
produced, integrated, and supported.

## CDR: critical design review

Use CDR to confirm that the design is complete enough, controlled enough, and evidenced enough to
enter construction and production.

Check at least:
- design completeness;
- documentation discipline;
- evidence of rigorous option consideration and iteration;
- readiness for manufacture, production, or construction;
- compatibility and interface completeness;
- alignment with the higher baselines.

Tailor CDR timing to the program. Prototypes and software builds may already exist; do not
assert that a design is still only on paper or that later controlled changes are impossible.

## Typical failure patterns

- subsystem features grow without parent justification;
- integration is assumed instead of designed;
- COTS technical data is weaker than expected;
- a modification is treated as trivial and under-scoped;
- interfaces are left to downstream teams to "work out";
- design-space margins are consumed by one subsystem without system-level permission.
