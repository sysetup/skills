# 09 Standards and Glossary

## Contents
- [Use this reference when](#use-this-reference-when)
- [Standards and source anchors](#standards-and-source-anchors)
- [Capability-framework crosswalk](#capability-framework-crosswalk)
- [Quick glossary](#quick-glossary)
- [Usage cautions](#usage-cautions)

## Use this reference when

Use this file when the user needs terminology, acronym expansion, or a standards crosswalk that
keeps the skill aligned with mainstream systems-engineering language.

## Standards and source anchors

This is a methodological orientation, not a normative crosswalk or certification. Confirm the
applicable jurisdiction, contract, exact edition, amendments, and licensed text for each project.
Do not infer compliance from use of this skill. No full paid standard is bundled.

Public sources inspected for this correction on 2026-09-14:

| ID | Source / inspected scope | Permitted use and limitation |
|---|---|---|
| SRC-NASA-5 | NASA Systems Engineering Handbook, web section 5.3 and 5.4 | Verification/validation planning, execution records and results; NASA guidance, not a universal mandate |
| SRC-NASA-6 | NASA Systems Engineering Handbook, web section 6.2 | Bidirectional requirement tracing and change control; not proof that any particular trace is correct |
| SRC-ISO-15288 | ISO/IEC/IEEE 15288:2023, official catalog abstract, edition 2 | Lifecycle-process orientation only; full normative clauses were not inspected |
| SRC-AIAG-2019 | AIAG announcement dated 2019-06-13, public description of AIAG & VDA FMEA Handbook | Confirms domain-specific Action Priority replaces RPN in that method; no scoring table or equivalence is reproduced |
| SRC-OPENAI-SKILLS | OpenAI skills documentation and linked build-skills guidance | Packaging/discovery orientation; host installation and execution are not certified by this bundle |

Source locators:
- SRC-NASA-5: https://www.nasa.gov/reference/5-0-product-realization/
- SRC-NASA-6: https://www.nasa.gov/reference/6-0-crosscutting-technical-management/
- SRC-ISO-15288: https://www.iso.org/standard/81702.html
- SRC-AIAG-2019: https://blog.aiag.org/new-aiag-vda-fmea-handbook-and-trainings-available
- SRC-OPENAI-SKILLS: https://developers.openai.com/api/docs/guides/tools-skills

Other inherited references (ANSI/EIA-632, INCOSE guidance, MIL-STD families, Blanchard/Fabrycky,
and maturity models) are source traditions only: no edition or clause was established here.
Do not cite them as if their actual text had been consulted. Identify and inspect the exact
publication before attributing a process or mandatory requirement to it.

Use `assets/templates/standards-applicability-template.md` to record source ID, edition/clause,
applicability rationale, obligation, artifact/evidence, reviewer, and assessment (`not-assessed`,
`gap`, `supported`, or `not-applicable` with rationale). Catalog-only access remains `not-assessed`
for clause compliance. Review gates and document names in this package are tailored conventions;
ISO/IEC/IEEE 15288 does not mandate this particular lifecycle, methodology, or artifact layout.
FMEA numeric thresholds are not universal, and low RPN is not acceptance of safety risk.

## Capability-framework crosswalk

These inherited acronyms are orientation only; verify the sponsoring authority's current
framework, terminology, edition, and applicability before using them as a completeness claim.

| Framework | Expansion | Practical use |
|---|---|---|
| DOTMLPF | doctrine, organization, training, materiel, leadership, personnel, facilities | useful US defense framing for capability-system completeness |
| FIC | fundamental inputs to capability | useful Australian capability framing; include command and management, organization, collective training, major systems, personnel, facilities, supply and support |
| DLoD | defence lines of development | useful UK capability framing for doctrine, organization, training, equipment, personnel, infrastructure, logistics, information |
| PRICIE | personnel, research and development, infrastructure, concepts and doctrine, information technology, equipment | useful Canadian capability framing |

## Quick glossary

### Acquirer
Customer-side entity responsible for acquiring the system.

### Allocated baseline
Approved allocation of functional/performance/interface requirements to configuration items,
including verification criteria. Associated preliminary design supports but is not itself the definition.

### Analysis
The ASE step that determines what is required, how well, and why.

### AT&E
Acceptance test and evaluation. Verification activity used to support customer acceptance.

### BDD
Block definition diagram. SysML view of system composition and classification.

### Baseline
Approved configuration state used for control and change decisions.

### BRS
Business requirements specification.

### Capability system
The broader operational capability including people, facilities, support, training, data,
organizations, procedures, and material systems.

### CDR
Critical design review. Final major design review before construction or production.

### CI
Configuration item. Identified hardware, software, or other configuration entity selected
for formal control; not necessarily a physical grouping.

### CM
Configuration management.

### ConOps
Concept of operations describing intended use from the relevant stakeholder perspective;
its level and scope are tailored, not restricted to enterprise level.

### Context diagram
Diagram showing the SOI, external systems, boundary, and interfaces.

### COTS
Commercial off-the-shelf item.

### Derivation
Inference of a necessary lower-level requirement not directly stated by stakeholders.

### Design space
Any room to move across system constraints and allocations, not just physical volume.

### DT&E
Developmental test and evaluation. Progressive evaluation during design and development.

### End products
Operational products delivered by the system realization effort.

### Enabling products
Products needed to test, train, support, and dispose of the system.

### FMEA
Failure mode and effects analysis. Function-level analysis of failure modes, causes, effects,
severity, occurrence, detection, and residual risk.

### FCA
Functional configuration audit. Audit confirming that documented function and performance match
the realized system.

### FFBD
Functional flow block diagram.

### FQR
Formal qualification review. Acceptance-oriented transition gate near service entry.

### Functional baseline
Approved system-level logical description, centered on the SyRS and related artifacts.

### IBD
Internal block diagram. SysML view of parts, ports, and item flows inside a block.

### ICD
Interface control document. Controlled agreement on an exchange between two named parties.

### ILS
Integrated logistics support.

### LCD
Lifecycle concept document.

### Logical architecture
The functional or logical view describing what the system must do and how well.

### Mission
Stated purpose of the system.

### MOE
Measure of effectiveness. Stakeholder-facing measure used to judge mission success.

### MOP
Measure of performance. Technical or system-facing measure supporting effectiveness.

### MOTS
Modified off-the-shelf item.

### N2 diagram
Matrix view of interfaces among elements. Diagonal cells are the elements; off-diagonal cells
are exchanges.

### OpsCon
Operational concept.

### OT&E
Operational test and evaluation. Validation-oriented operational evidence.

### PCA
Physical configuration audit. Audit confirming the physical system matches physical documentation.

### PDR
Preliminary design review.

### PLCD
Preliminary lifecycle concept document.

### Problem domain
The side of the effort dominated by need, stakeholder language, and logical description.

### Product baseline
Final detailed-design package used for production and construction.

### Pugh matrix
Qualitative pairwise trade matrix scored against a datum using S, +, and −.

### RBS
Requirements breakdown structure.

### SDR
System design review.

### SEMP
Systems engineering management plan.

### SOI
System of interest.

### Solution domain
The side of the effort dominated by realization, physical architecture, and implementation.

### SoS
System of systems.

### SRR
System requirements review.

### STRS
Stakeholder requirements specification.

### SysML
Systems Modeling Language. This bundle provides illustrative Mermaid projections of selected
concepts, not native SysML models or conformance-checked exports.

### Synthesis
The ASE step that proposes how the system can be realized.

### SyRS
System requirements specification.

### V-model
Lifecycle pairing of left-side specification products with right-side verification and
validation activities.

### Validation
Confirmation that the right system is being pursued or delivered against stakeholder and business
need.

### Verification
Confirmation that a system or design meets its specified requirements.

### WBS
Work breakdown structure.

### WSOI
Wider system of interest.

## Usage cautions

- Use glossary terms consistently. Do not swap verification and validation.
- Use capability-system language when non-material enablers materially affect success.
- Use standards as orientation and cross-checks, not as a substitute for thinking.
