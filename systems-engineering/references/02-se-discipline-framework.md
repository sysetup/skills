# 02 SE Discipline Framework

## Contents
- [Use this reference when](#use-this-reference-when)
- [Working definition](#working-definition)
- [Core tenets](#core-tenets)
- [Top-down design and bottom-up integration](#top-down-design-and-bottom-up-integration)
- [Simple framework for applying the discipline](#simple-framework-for-applying-the-discipline)
- [The ASE loop](#the-ase-loop)
- [Benefits to expect when applied correctly](#benefits-to-expect-when-applied-correctly)
- [Customer and developer perspectives](#customer-and-developer-perspectives)
- [Tailoring principle](#tailoring-principle)
- [Diagnostic questions](#diagnostic-questions)

## Use this reference when

Use this file when the user needs the systems-engineering mindset itself: what makes the
discipline different from traditional design, why it saves cost and schedule later, and how to
apply the analysis-synthesis-evaluation loop without losing lifecycle control.

## Working definition

Systems engineering is a top-down, lifecycle-oriented, requirements-centered discipline used to
define, balance, integrate, realize, verify, validate, support, and retire complex systems.

It is both:
- a **technical discipline** that produces architecture, requirements, interfaces, and design
  control; and
- a **management discipline** that directs, reviews, plans, audits, and balances the technical
  effort.

## Core tenets

### 1. Start top-down

Start with the system as a whole, its mission, its environment, and its interfaces. Decompose
only after the whole-system need is understood.

### 2. Treat requirements engineering as foundational

Poor requirements cannot be repaired by good design. Early effort must focus on getting the right
requirements, excluding irrelevant ones, and preserving traceability.

### 3. Keep lifecycle focus

Evaluate decisions across acquisition, integration, operation, support, modification, and
retirement. Avoid acquisition-only optimization.

### 4. Optimize and balance the whole system

A collection of locally optimized subsystems does not guarantee an optimized system. Subsystems
may need to be deliberately sub-optimal so the system can be balanced and fit for purpose.

### 5. Integrate disciplines

Complex systems require many technical and non-technical disciplines. Systems engineering defines
how those efforts relate and how their outputs are integrated.

### 6. Manage as well as engineer

Systems engineering is inseparable from planning, review, risk management, configuration
management, and control of technical progress.

## Top-down design and bottom-up integration

Use the pair together:
- **Top-down design** to decompose the system into manageable elements and define interfaces.
- **Bottom-up integration** to assemble verified components into assemblies, subsystems, and the
  final system.

If the top-down decomposition is weak, bottom-up integration becomes expensive and unstable.

## Simple framework for applying the discipline

### Processes
The doing element. Examples:
- needs and requirements definition;
- conceptual design;
- preliminary design;
- detailed design and development;
- construction, production, integration, and support.

### Management
The controlling element. Examples:
- technical reviews and audits;
- test and evaluation planning;
- technical risk management;
- configuration management;
- systems engineering management planning.

### Tools
The enabling element. Examples:
- RBS;
- FFBD;
- WBS;
- context diagrams;
- trade studies;
- prototyping and simulation;
- standards and maturity models.

### Related disciplines
The collaborating element. Examples:
- project management;
- ILS;
- QA;
- requirements engineering;
- hardware, software, logistics, and specialty engineering.

## The ASE loop

Use the recursive **analysis -> synthesis -> evaluation** loop at every level.

### Analysis
Answer:
- what is required;
- how well it must be done;
- why it matters;
- what constraints and interfaces apply.

### Synthesis
Propose how the requirement set can be realized. This includes architecture selection, option
generation, and the creation of candidate designs.

### Evaluation
Compare requirements, alternatives, trade-offs, risks, and lifecycle implications. Confirm or
reject the current design direction. Re-open analysis when the evidence does not support the
current synthesis.

### Recursion rule
Apply the ASE loop:
- at system level;
- again at subsystem level;
- again at assembly level;
- again at component level if necessary.

## Benefits to expect when applied correctly

### Lower lifecycle cost
Early systems-engineering effort is applied when design changes are cheapest. This reduces the
cost of late rework, support surprises, and disposal problems.

### Better schedule performance
Clear requirements and early trade resolution reduce churn, redesign, and the need to revisit
major decisions late.

### Lower technical risk
The discipline exposes feasibility issues, requirement conflicts, interface mismatches, and
supportability risks before they become embedded in production.

### Higher quality
Quality here means fitness for purpose. A better system is one that more completely satisfies the
documented needs and requirements.

## Customer and developer perspectives

### Customer-side emphasis
- define business, stakeholder, and system requirements;
- validate that the right system is being pursued;
- monitor supplier progress and risk.

### Developer-side emphasis
- design, integrate, and verify the system;
- manage interfaces, baselines, and technical evidence;
- deliver a realizable solution that can be accepted and supported.

## Tailoring principle

Systems engineering applies to all systems, but never in identical depth. Tailor the effort to:
- scale;
- complexity;
- novelty;
- risk;
- stakeholder exposure;
- contractual context;
- lifecycle consequence.

Do not under-tailor merely because the discipline is broad. Do not over-tailor merely because the
system is small.

## Diagnostic questions

Use these to determine whether the discipline is being applied properly.

1. Is the whole system framed before components are discussed?
2. Are needs, requirements, design choices, and tests connected by traceability?
3. Are lifecycle costs and support implications visible in the trade space?
4. Are interfaces explicit and owned?
5. Are subsystem teams being balanced against system constraints?
6. Is the technical program being reviewed progressively rather than only at the end?
7. Is the approach tailored to the actual project rather than copied from habit?
