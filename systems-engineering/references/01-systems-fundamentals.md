# 01 Systems Fundamentals

## Contents
- [Use this reference when](#use-this-reference-when)
- [Core definitions](#core-definitions)
- [Classify the system before designing it](#classify-the-system-before-designing-it)
- [Capability system versus material system](#capability-system-versus-material-system)
- [Logical and physical viewpoints](#logical-and-physical-viewpoints)
- [Product and architecture hierarchy](#product-and-architecture-hierarchy)
- [End products and enabling products](#end-products-and-enabling-products)
- [System versus subsystem versus system of systems](#system-versus-subsystem-versus-system-of-systems)
- [Problem domain versus solution domain](#problem-domain-versus-solution-domain)
- [Lifecycle map](#lifecycle-map)
- [Scoping workflow](#scoping-workflow)
- [Failure patterns to catch early](#failure-patterns-to-catch-early)
- [Mini-examples](#mini-examples)

## Use this reference when

Use this file when the immediate problem is not yet a design problem but a framing problem:
what is the system, where is the boundary, what is inside or outside scope, which environment
matters, and at what level the user is actually working.

## Core definitions

- **System**: a set of elements that interact to achieve a stated purpose.
- **Mission**: the stated purpose of the system; the basis for design entry and the eventual
  test of fitness for purpose.
- **System of interest (SOI)**: the selected system elements and their interactions inside the
  chosen boundary.
- **Boundary**: the line that separates the SOI from external systems and the environment.
- **Operating environment**: the context in which the SOI receives inputs, returns outputs, and
  encounters real constraints.
- **External interface**: any required interaction across the system boundary.
- **Wider system of interest (WSOI)**: a broader framing useful when the SOI is nested inside a
  larger capability or enterprise context.

## Classify the system before designing it

### Open versus closed

Treat useful engineered systems as **open systems**. They interact with their environments,
accept inputs, produce outputs, and must interface successfully across their boundaries.

### Natural versus human-made versus human-modified

This skill focuses on **human-made** and **human-modified** systems. Natural systems are useful
comparators, but they are not the target of the course's systems-engineering process.

### Physical versus conceptual

A conceptual description is necessary, but the engineered target is a **physical or realizable
solution**, which may include software, facilities, procedures, training systems, and support
arrangements in addition to hardware.

### Precedented versus unprecedented

A precedented system is composed mostly of known elements. An unprecedented system depends more
heavily on research and development. Use this distinction to calibrate risk, tailoring, and the
feasibility of waterfall-style progression.

## Capability system versus material system

Do not reduce a system to hardware and software alone.

A capability system may include:
- organizations;
- personnel;
- collective training;
- facilities;
- data;
- support equipment, consumables, and spares;
- procedures and policies;
- major material systems.

Use **material system** when the user is actually engineering only the major equipment element.
Use **capability system** when people, facilities, logistics, doctrine, training, and other
non-material enablers are part of the decision.

## Logical and physical viewpoints

### Logical or functional viewpoint

Use the logical viewpoint to answer:
- what must the system do;
- how well must it do it;
- under what conditions must it perform;
- with which external systems must it interact;
- why does this matter to stakeholders.

This viewpoint dominates the problem domain and early systems engineering.

### Physical viewpoint

Use the physical viewpoint to answer:
- how the system will be realized;
- what the elements are;
- how they are manufactured, integrated, tested, and supported.

This viewpoint dominates the solution domain once the logical architecture is stable enough to
allocate into physical groupings.

## Product and architecture hierarchy

A common physical hierarchy is:
- system;
- subsystem;
- assembly;
- component.

A common logical hierarchy is:
- mission;
- major functions or goals;
- subordinate functions or objectives;
- leaf functions or allocated requirements.

Map the logical hierarchy to the physical hierarchy deliberately. Do not assume that the physical
partition is obvious merely because the functions are known.

## End products and enabling products

Treat the system as more than the operational end item. Include enabling products such as:
- test products;
- training products;
- support products;
- disposal products.

This prevents designs that are operationally attractive but impossible to verify, field, support,
or retire.

## System versus subsystem versus system of systems

### Treat an element as a subsystem when
- it exists only to serve the parent system;
- it is not managerially independent;
- it is not operationally independent;
- its optimization must be subordinate to system optimization.

### Treat an element as a system in a system of systems when
- it is managerially independent;
- it is operationally independent;
- it may have been optimized for its own purpose before joining the larger whole.

A system of systems is often not globally optimized because its constituent systems were already
optimized locally. Capture that tension explicitly in trade studies and governance.

## Problem domain versus solution domain

- **Problem domain**: customer and stakeholder side; mostly logical descriptions; heavy focus on
  need, context, constraints, and required effects.
- **Solution domain**: developer side; mostly physical descriptions; heavy focus on realization,
  interfaces, configuration items, production, and integration.

Do not let solution-domain thinking dominate before the problem domain is stable enough.

## Lifecycle map

### Pre-acquisition
- business planning and business case;
- feasibility and option exploration;
- early mission framing.

### Acquisition
- conceptual design;
- preliminary design;
- detailed design and development;
- construction and production.

### Utilization
- operational use;
- system support;
- modifications and upgrades.

### Retirement
- withdrawal from service;
- disposal, reuse, or replacement.

## Scoping workflow

1. State the mission in one or two sentences.
2. Name the SOI explicitly.
3. Draw the initial boundary.
4. List external systems and interfaces.
5. Decide whether the current question is capability-system or material-system level.
6. Decide whether the current architecture is a system or a system of systems.
7. Separate logical statements from physical commitments.
8. Locate the lifecycle phase.
9. Confirm which parties own the problem and which parties own realization.

## Failure patterns to catch early

- The boundary is vague, so requirements and responsibilities drift.
- A subsystem is treated like a system and optimized in isolation.
- The design jumps straight to components before the mission is stable.
- External interfaces are assumed rather than defined.
- Capability-level enablers are ignored because only the material system is visible.
- The problem domain is skipped and the first physical idea becomes the baseline by accident.

## Mini-examples

### Domestic alarm
Use a context diagram to separate the alarm from the house power system, telephone network,
monitoring agent, and intruder. The alarm is the SOI, not the whole house.

### Aircraft capability
Treat aircrew, ground crew, training, facilities, support equipment, data, and maintenance as
part of the capability system even if the material aircraft is the development focus.

### Software platform
Treat software as part of a realizable system. Even when the product is intangible, the system
still has interfaces, environments, support needs, users, data, and lifecycle obligations.
