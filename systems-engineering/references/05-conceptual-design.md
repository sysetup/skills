# 05 Conceptual Design

## Contents
- [Use this reference when](#use-this-reference-when)
- [Objective of conceptual design](#objective-of-conceptual-design)
- [Entry condition](#entry-condition)
- [Step 1: identify the right stakeholders](#step-1-identify-the-right-stakeholders)
- [Step 2: identify constraints early](#step-2-identify-constraints-early)
- [Step 3: define mission, goals, objectives, and scenarios](#step-3-define-mission-goals-objectives-and-scenarios)
- [Step 4: define validation intent early](#step-4-define-validation-intent-early)
- [Step 5: define lifecycle concepts](#step-5-define-lifecycle-concepts)
- [Step 6: frame context, boundaries, and interfaces](#step-6-frame-context-boundaries-and-interfaces)
- [Step 7: transform need into formal requirement sets](#step-7-transform-need-into-formal-requirement-sets)
- [Step 8: structure the system requirements](#step-8-structure-the-system-requirements)
- [Step 9: review the requirement set](#step-9-review-the-requirement-set)
- [Step 10: conduct system-level synthesis](#step-10-conduct-system-level-synthesis)
- [Mandatory, important, desirable classification](#mandatory-important-desirable-classification)
- [Conceptual-design deliverables](#conceptual-design-deliverables)
- [SDR: system design review](#sdr-system-design-review)
- [Functional baseline](#functional-baseline)

## Use this reference when

Use this file when the user is moving from recognized need to a system-level understanding of the
required solution, or when the immediate deliverable is a mission package, lifecycle concept,
BRS, STRS, SyRS, trade study, or SDR-ready decision packet.

## Objective of conceptual design

Conceptual design is the formal transition from the business world to the project world. It must
finish with a coherent logical description of the system and a defensible preferred system-level
solution direction.

## Entry condition

Enter conceptual design when a capability gap or business need has been recognized and there is a
credible case to explore or acquire a solution.

## Step 1: identify the right stakeholders

Identify affected and influencing stakeholders, including safety/public-interest perspectives.
Select representatives and decision rights deliberately; do not exclude affected groups merely
because they lack formal approval power. Typical categories:
- management affected by the need;
- operational users;
- engineering and technical representatives;
- test and acceptance personnel;
- maintenance and logistics representatives;
- support and disposal stakeholders.

Do not build an unbounded stakeholder list. Curate the working group deliberately.

## Step 2: identify constraints early

Capture at least four classes of constraints.

### Business constraints
- policy;
- procedures;
- standards;
- existing relationships or contracts.

### Project constraints
- budget;
- schedule;
- resource limits.

### External constraints
- law and regulation;
- workforce availability;
- mandated infrastructure or interoperability conditions.

### Design constraints
- technology maturity and availability;
- design-tool limits;
- production and construction limits.

## Step 3: define mission, goals, objectives, and scenarios

### Mission
State the system mission briefly and unambiguously.

### Goals and objectives
Expand the mission into a hierarchy of goals and then objectives. This provides the top levels of
the logical structure that later feeds the RBS.

### Scenarios and vignettes
Describe how the system will be used, supported, and stressed. Use scenarios to expose:
- actors;
- environment;
- external systems;
- failure modes;
- operational nuances;
- support expectations.

Use FFBDs, diagrams, models, or short narrative vignettes to make scenarios concrete.

## Step 4: define validation intent early

Ask how stakeholders will be convinced that their expectations are satisfied. Record top-level
validation criteria while needs are being discussed, not after the design is fixed.

Use this to develop a hierarchy of:
- measures of effectiveness;
- measures of performance;
- related verification expectations.

## Step 5: define lifecycle concepts

Capture the intended lifecycle in concept form.

### Acquisition concept
How the system will be acquired, contracted, or sourced.

### Operational concept or OpsCon
How the system will be employed by users to solve the need.

### Deployment concept
How the system will be transitioned into service.

### Support concept
How support, maintenance, engineering support, training, facilities, and supply will operate.

### Retirement concept
How the system will be withdrawn, disposed of, or repurposed.

Start these in the PLCD. Refine them into the LCD as stakeholder understanding improves.

## Step 6: frame context, boundaries, and interfaces

Use a context diagram to show:
- the SOI in the center;
- external systems and environment;
- named interfaces crossing the boundary.

The context diagram should make clear:
- what the system is responsible for;
- what it expects from external systems;
- what it must provide to external systems;
- which interfaces are mandated and which remain open to trade.

## Step 7: transform need into formal requirement sets

### Business analysis
Transform business needs into the BRS.

### Stakeholder requirements analysis
Transform business needs and lifecycle concepts into the LCD and STRS.

### System requirements analysis
Transform the STRS into the SyRS.

At system level, answer at least these questions:
- what must the system do;
- how well must it do it;
- under what conditions must it perform;
- what external systems are involved;
- how will each requirement be verified.

## Step 8: structure the system requirements

Use the RBS to organize the SyRS. Reuse and refine earlier logical structures instead of starting
from a blank page if a workable hierarchy already exists.

Write requirements with:
- statement;
- source;
- verification method;
- rationale;
- placement in the RBS;
- traceability back to the STRS.

## Step 9: review the requirement set

Use one or more **system requirements reviews (SRRs)** to perform a work -> review -> rework
cycle until the set is stable enough to support system synthesis.

Reject false efficiency. One weak review is not a substitute for several disciplined reviews.

## Step 10: conduct system-level synthesis

Send the draft system requirement set into the solution space and compare candidate solutions.

For each candidate, examine:
- level of compliance;
- discrepancies or non-compliances;
- enhanced capabilities offered;
- cost;
- schedule;
- risk;
- support and disposal implications.

Expect negotiation and offer definition with the preferred supplier or in-house solution team.
The SyRS must be refined until what is required and what is offered are aligned enough to proceed.

## Mandatory, important, desirable classification

When the design space is not yet closed, use mandatory, important, and desirable levels to
support trade studies.

### Usage rule
- Reject demonstrated failures of applicable mandatory requirements; record unknowns as pending, not as pass or proven failure.
- Compare surviving options against important and desirable criteria, plus cost, schedule, risk,
  supportability, and lifecycle implications.
- Replace the graded statement with an agreed final value before baselining the final SyRS.

## Conceptual-design deliverables

Expect a package resembling:
- stakeholder list and roles;
- constraints register;
- mission, goals, objectives;
- scenarios or vignettes;
- context diagram and interface list;
- PLCD or LCD;
- BRS and STRS;
- draft then refined SyRS;
- SRR records;
- trade study or synthesis decision;
- SDR package.

## SDR: system design review

Use SDR to confirm readiness to proceed into preliminary design and to establish the functional
baseline.

Check at least:
- business, stakeholder, and system requirement coherence;
- traceability from STRS to SyRS;
- external interface and interoperability issues;
- preferred solution logic and negotiation outcome;
- technical-program planning for the next phase.

Run SDR as a professional technical meeting with agenda, chair, minutes, action items, and clear
decision authority.

## Functional baseline

Treat the SyRS and associated approved system-level logical architecture as the core of the
**functional baseline**. Do not move into subsystem allocation while the functional baseline is
still materially unstable.
