# 03 Needs and Requirements

## Contents
- [Use this reference when](#use-this-reference-when)
- [Distinguish needs from requirements](#distinguish-needs-from-requirements)
- [Requirement levels and dominant viewpoints](#requirement-levels-and-dominant-viewpoints)
- [Artifact chain](#artifact-chain)
- [Problem-domain to solution-domain transition](#problem-domain-to-solution-domain-transition)
- [Requirement categories](#requirement-categories)
- [Requirement statement anatomy](#requirement-statement-anatomy)
- [What versus how](#what-versus-how)
- [Role definitions](#role-definitions)
- [Why formal requirements matter](#why-formal-requirements-matter)
- [Operating heuristics](#operating-heuristics)
- [Mini trace example](#mini-trace-example)

## Use this reference when

Use this file when the user is mixing business need, stakeholder expectation, and system
specification language, or when the current question is really about which level of requirement
exists and who should own it.

## Distinguish needs from requirements

- **Need**: a capability statement expressed in the language of business management or
  stakeholders.
- **Requirement**: a formal, structured, agreed-to obligation for an entity to perform a
  function, possess a quality, or operate within stated constraints.

Label candidate obligations as draft/proposed until the authorized owner agrees them.
A single need can generate multiple requirements. Needs are not detailed enough to contract,
verify, or allocate directly without further analysis.

## Requirement levels and dominant viewpoints

| Level | Typical owner | Dominant language | Primary artifacts | Main question |
|---|---|---|---|---|
| Enterprise | enterprise leadership | strategic | conops | why does this capability matter? |
| Business management | business managers | problem and mission | PLCD, BRS | what does the business need and constrain? |
| Business operations | operational stakeholders | operational | LCD, STRS | what do stakeholders need to succeed? |
| System | requirements and systems engineers | logical system | SyRS, RBS, verification approach | what must the system do and how well? |
| Subsystem and below | designers and specialists | physical realization | development specs, detailed design docs | how will specific elements satisfy allocated requirements? |

## Artifact chain

### ConOps

A concept of operations communicates intended use from the relevant stakeholder perspective.
The enterprise-to-system sequence below is a useful project convention, not a universal restriction
on ConOps scope or naming.

### PLCD

The preliminary lifecycle concept document captures early views of:
- acquisition concept;
- operational concept or OpsCon;
- deployment concept;
- support concept;
- retirement concept.

### BRS

The business requirements specification formalizes business needs and constraints.

### LCD

The lifecycle concept document is the refined operational and lifecycle concept package used by
stakeholders.

### STRS

The stakeholder requirements specification formalizes stakeholder needs and operational concerns.

### SyRS

The system requirements specification formalizes what the system must do, how well it must do it,
under what conditions it must perform, what interfaces it must support, and how compliance will
be verified.

## Problem-domain to solution-domain transition

- Enterprise, business-management, and business-operations views remain mostly in the **problem
  domain**.
- System and lower-level physical design work increasingly enter the **solution domain**.

Do not drag detailed realization choices into the problem domain unless interoperability,
regulation, or stakeholder intent truly requires them.

## Requirement categories

### Functional requirements

State what the system must do or provide.

### Non-functional requirements

State qualities, properties, conditions, or constraints such as reliability, maintainability,
performance bounds, environmental limits, or usability expectations.

### Other useful groupings

Use additional labels when they help control the set, for example:
- interface;
- operational;
- stakeholder;
- environmental;
- regulatory;
- safety;
- design;
- support.

These groupings help organize the set. They do not replace the need for precise requirement
statements.

## Requirement statement anatomy

A strong requirement package contains more than the statement itself. Capture:
- the requirement statement;
- any performance statement or threshold;
- the verification method;
- rationale or explanatory notes;
- operating conditions or assumptions;
- related external systems and interfaces.

Write requirements in a consistent structure regardless of level. Higher-level artifacts can be
less formal in tone, but they should still support controlled transformation downstream.

## What versus how

The system level should lean toward **what**, not **how**. However, do not turn this into a dogma.
Specify **how** when:
- a mandated interface demands it;
- regulation or standard demands it;
- stakeholder intent requires a specific implementation;
- ambiguity would otherwise create avoidable risk.

If the higher-level stakeholder truly needs a particular implementation, say so explicitly rather
than hiding it as a vague functional statement.

## Role definitions

### User
A person who interacts with the system in operation or support. Users are part of the broader
system and can include operators and maintainers.

### Actor
An alternative term for a user when describing participation in system behavior or scenarios.

### Customer
The organization paying for the system to be developed or acquired.

### Acquirer
The customer-side entity responsible for acquiring the system.

### Developer
The entity responsible for developing the products that make up the system.

### Contractor
The organization under contract to the customer to perform the development.

### Stakeholder
Anyone with the right to influence requirements, or more broadly anyone affected by the system.
Not every affected person must be elevated into the core stakeholder set.

## Why formal requirements matter

Use requirements to:
- define scope;
- reconcile stakeholder viewpoints;
- justify expenditure and effort;
- track progress;
- determine completion and acceptance.

Without an endorsed requirement set, progress claims and acceptance criteria become arbitrary.

## Operating heuristics

1. Keep the level clear: business language belongs above system specification language.
2. Preserve lineage from ConOps and lifecycle concepts into formal requirements.
3. Use the highest level that resolves the current question.
4. Do not allocate physical implementation detail before the system-level need is stable.
5. Demand explicit owners for each artifact and requirement level.
6. Prepare each level so it can be transformed, not merely admired.

## Mini trace example

- Need: improve border surveillance coverage.
- Business requirement: close the surveillance capability gap over named regions.
- Stakeholder requirement: provide persistent detection, classification, and reporting under
  operational weather and crew constraints.
- System requirement: detect, classify, and report relevant targets within stated ranges,
  conditions, interfaces, and verification methods.
