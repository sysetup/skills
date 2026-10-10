# 04 Requirements Engineering

## Contents
- [Use this reference when](#use-this-reference-when)
- [Purpose](#purpose)
- [Core process](#core-process)
- [Elicitation and elaboration](#elicitation-and-elaboration)
- [Elicitation methods](#elicitation-methods)
- [Natural-language ingestion](#natural-language-ingestion)
- [Requirement quality checklist](#requirement-quality-checklist)
- [RBS: requirements breakdown structure](#rbs-requirements-breakdown-structure)
- [FFBD: functional flow block diagram](#ffbd-functional-flow-block-diagram)
- [Additional analytical tools](#additional-analytical-tools)
- [Traceability](#traceability)
- [Requirements management](#requirements-management)
- [Verification and validation discipline](#verification-and-validation-discipline)
- [Practical execution checklist](#practical-execution-checklist)
- [Evidence and semantic trace review](#evidence-and-semantic-trace-review)

## Use this reference when

Use this file when the user needs to collect, elaborate, structure, validate, trace, manage, or
change requirements in a controlled way.

## Purpose

Requirements engineering is the formal process used to move from business and stakeholder intent
to controlled requirement sets that are complete enough to drive design and controlled enough to
survive change.

It exists to ensure that:
- all relevant requirements are included;
- irrelevant requirements are excluded;
- ambiguities are reduced early;
- change impact can be seen before baselines move.

## Core process

Use this cycle repeatedly:
1. identify and capture requirements;
2. analyze what they mean;
3. define them in controlled form;
4. validate that the set still supports stakeholder need;
5. manage change through the lifecycle.

## Elicitation and elaboration

### Elicitation

An elicited element is directly attributable to a source. Common sources:
- workshops;
- interviews;
- regulations and mandated constraints;
- documented stakeholder statements.

Treat elicited content as explicit, not inferred.

### Elaboration

Elaboration is the analytic step that converts intent into a more complete and actionable set.
Two mechanisms dominate.

#### Decomposition
Break a high-level function or requirement into lower-level functions or requirements that are
explicitly demanded by the parent.

#### Derivation
Infer a necessary lower-level function or requirement not directly stated by stakeholders but
required if the parent set is to be achieved.

Derivation is powerful and dangerous. Record rationale and traceability rigorously.

## Elicitation methods

Use methods in order of their likely value for the current stage.

### High-yield methods
- structured workshops;
- structured interviews;
- operational scenarios and vignettes;
- use cases;
- facilitated review of draft artifacts.

### Useful supporting methods
- surveys and questionnaires for breadth, not precision;
- prototypes, models, and simulations when stakeholders need something concrete;
- observation and work-study techniques;
- document review;
- market analysis and competitive system analysis;
- reverse engineering and benchmarking.

### Selection guidance
- Use workshops when multiple stakeholders must reconcile competing views quickly.
- Use scenarios when users understand stories better than abstract functions.
- Use prototypes or models when behavior is hard to imagine from text alone.
- Use observation when claimed work and actual work may differ.

## Natural-language ingestion

When the user provides informal text rather than a register:
1. Frame the SOI and mission.
2. Preserve the original wording and source locator; classify needs, obligations, facts, notes, and conflicts. Split compound obligations only.
3. Allocate IDs (`NEED-`, `STR-`, `SYR-`).
4. Rewrite only proposed obligations as `[subject] shall [verb] [object] [conditions] [measure]`; do not turn every input row into an approved requirement.
5. Classify type and name a verification method.
6. Record source, parent, rationale, origin (`elicited/derived/assumed`), approval state, and a forward design or test hook. Keep original and proposed wording distinct.

For tens to hundreds of statements, ingest into a table grouped by RBS area. Do not write an
essay per item. Mark missing measures as `OPEN-MEASURE`. Full edge-case rules live in
`references/11-mbse-interfaces-vv.md`.

## Requirement quality checklist

For each requirement, ask:
- Is the source known?
- Is the statement singular and precise?
- Does it use SHALL with one obligation?
- Is the parent relationship known?
- Is the verification method feasible?
- Is rationale recorded when derivation is involved?
- Does the statement duplicate another requirement?
- Does it impose design unnecessarily?
- Does it conflict with a sibling requirement?
- Is it physically and logically feasible under stated constraints?

## RBS: requirements breakdown structure

Use an RBS to create the logical hierarchy in which requirements live.

### Working rules
- Keep the hierarchy visible and readable at each level.
- Use unique, verb-based labels.
- Keep phrase length short and consistent.
- Number hierarchically.
- Keep child sets cognitively manageable; five to seven items per node is a useful heuristic,
  not a law.

### What the RBS gives you
- a shared frame for collaborative requirement writing;
- a disciplined location for each requirement;
- a basis for requirements flowdown;
- a backbone for traceability.

## FFBD: functional flow block diagram

Use an FFBD to complement the RBS by showing flow, sequence, branching, concurrency, and the
operational ordering of functions.

### Working rules
- Number functions consistently with the RBS.
- Keep one level of flow readable on a single page when possible.
- Capture workshop drafts quickly, then formalize.
- Use FFBDs to expose interface timing and sequencing issues.

## Additional analytical tools

Use other tools when the domain needs them, including:
- context diagrams;
- N2 diagrams;
- structured analysis;
- data-flow and control-flow diagrams;
- IDEF-style diagrams;
- behavior diagrams;
- simulation and modeling artifacts.

## Traceability

### Forward traceability

Trace from parent requirement to child requirement, design decision, or verification evidence.
Use it to prove that endorsed higher-level requirements are being addressed.

### Backward traceability

Trace from child requirement or design element back to at least one parent. Use it to prove that
the child exists for an endorsed reason.

### Why it matters
- change impact assessment;
- prevention of requirements creep;
- identification of orphan requirements;
- support for configuration control;
- credible acceptance and audit evidence.

### Failure conditions
- a parent with no downstream realization;
- a child with no endorsed parent;
- duplicated requirements that diverge over time;
- trace links that exist only in prose and not in controlled artifacts.

## Requirements management

Expect requirements to evolve. Estimate change exposure from the project's own data; do not assert
an unsourced percentage of requirements that will change.

A useful requirements-management tool should support:
- capture and storage;
- browsing and reporting;
- forward and backward traceability;
- glossary and template support;
- import and export;
- change control and change impact assessment;
- allocation from logical to physical structures.

Do not let the tool dictate poor engineering. The tool should support the process, not replace it.

## Verification and validation discipline

- **Verification** asks whether the system or design meets the specification.
- **Validation** asks whether the system solves the stakeholder and business need.

Keep both in view while writing requirements. A requirement set can be internally well written and
still fail to validate.

## Practical execution checklist

1. Identify sources and core stakeholders.
2. Capture elicited content.
3. Decompose and derive carefully.
4. Organize the set in an RBS.
5. Use FFBDs and scenarios to expose sequence and interface logic.
6. Write requirement statements with verification and rationale.
7. Remove duplication and resolve conflict.
8. Establish traceability links.
9. Review and rework until the set is coherent.
10. Submit the coherent set to the authorized baseline owner. Record approval, version, date, and
    unresolved exceptions; do not self-approve on the user's behalf.

## Evidence and semantic trace review

Apply `references/12-evidence-and-assurance.md`. Inspect the linked test procedure, not just its
identifier: subject, observable, trigger, interface/direction, threshold, units, and conditions
must address the obligation. Maintain separate planned coverage and demonstrated compliance.
Use `OPEN-MEASURE`, `OPEN-SOURCE`, or `OPEN-APPROVAL` when the required information is missing.
A quantitative target introduced for an example is illustrative, not an elicited requirement.
