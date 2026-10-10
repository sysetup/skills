# 08 SE Management

## Contents
- [Use this reference when](#use-this-reference-when)
- [Evaluation management](#evaluation-management)
- [Configuration management](#configuration-management)
- [Technical risk management](#technical-risk-management)
- [Technical review and audit program](#technical-review-and-audit-program)
- [Development strategies](#development-strategies)
- [Tailoring rules](#tailoring-rules)
- [SEMP: systems engineering management plan](#semp-systems-engineering-management-plan)
- [Related disciplines and interfaces](#related-disciplines-and-interfaces)
- [Management checklist](#management-checklist)

## Use this reference when

Use this file when the user needs to plan or control the technical program itself: evaluation,
configuration management, technical risk, technical reviews, development strategy, tailoring,
SEMP construction, or coordination with adjacent disciplines.

## Evaluation management

Evaluation is not an end-of-project afterthought. Plan and manage it from the start because it
consumes:
- facilities;
- test equipment;
- trained people;
- approved procedures;
- access to external systems and environments;
- cost and schedule margin.

If evaluation is not planned, the team will face a bad choice between late schedule or inadequate
evidence. Avoid that situation through early planning.

## Configuration management

Configuration management keeps design, product, software, interfaces, and documents under visible,
controlled version discipline.

### The four basic elements

#### 1. Configuration identification
Define what is under control: documents, baselines, hardware, software, interfaces, and selected
versions of all of them.

#### 2. Status accounting
Be able to state the current approved configuration and how it changed over time.

#### 3. Change management or control
Bring the right parties together to review change proposals, their cost and schedule impact, and
their technical consequences before moving the baseline.

#### 4. Auditing
Check that people are using the agreed documentation and that realized products match the approved
design and process.

### CM failure modes
- different parties are using different baselines;
- changes are made without visibility to downstream builders or support teams;
- audit evidence is weak or late;
- support organizations inherit a fleet with undocumented variation.

## Technical risk management

Technical risk is the chance that technical issues will adversely affect objectives. Assess each
risk at least by:
- likelihood;
- consequence or impact;
- resulting risk priority, under the chosen scale.

Do not confuse risk priority with FMEA severity, which rates the effect rather than the product
of likelihood and consequence.

### Common technical-risk sources
- immature technology;
- unrealistic function or performance claims;
- supportability gaps;
- manufacturability difficulty;
- inadequate quantities or production scalability;
- interface complexity;
- unstable requirements.

When the user asks for failure modes, or when a function is safety- or mission-critical, add an
FMEA using `assets/templates/fmea-template.md`. Identify the domain method, approved scales,
exposure, and decision authority first. Use RPN = S * O * D only where appropriate; no universal
RPN or severity cutoff applies. Escalate credible safety concerns independently of the product.
Keep projected residual ratings distinct from demonstrated results and authorized risk acceptance.
Procedure detail lives in `references/11-mbse-interfaces-vv.md` and the evidence gates in reference 12.

### Treatment options
- **avoid** by choosing a different design approach;
- **reduce** by lowering likelihood or impact;
- **transfer** to a party better placed to manage it;
- **accept deliberately** only through the authorized authority, within applicable legal/safety constraints, with a recorded rationale.

### Design-side mitigators
Use where appropriate:
- spare capacity;
- redundancy;
- design diversity;
- progressive reviews and evaluation;
- early trade studies.

Watch for common-mode failure when redundant elements share the same weakness.

## Technical review and audit program

Use progressive reviews at logical transition points rather than waiting until the end.

### Typical review set
- SDR at system-level design stabilization;
- PDR at subsystem allocation and upper physical design maturity;
- CDR at detailed-design completion and production readiness;
- FQR at formal qualification and acceptance.

### Meeting discipline
Treat reviews as professional technical meetings with:
- agenda;
- chair;
- minutes;
- action items;
- clear decision authority;
- timing based on technical readiness, not political convenience.

Bad news does not improve with age. Do not hold reviews early just to preserve schedule optics.

## Development strategies

### Waterfall
Use when:
- requirements are well understood and reasonably stable;
- technology is mature and available;
- time and money exist to solve the whole problem in one pass.

### Incremental
Use when:
- the full solution is understood broadly;
- resources do not allow one-pass realization;
- future phases can be designed in from the start.

### Evolutionary
Use when:
- not all requirements are known in detail at the start;
- growth, extension, or reconfiguration is expected;
- the team can accept that future change may be constrained by the initial form.

Tailor strategy to the actual project. Systems engineering is not one size fits all.

## Tailoring rules

Tailor based on:
- scale;
- complexity;
- novelty;
- consequence of failure;
- lifecycle length;
- stakeholder exposure;
- contractual form;
- need for formal evidence.

Do not discard discipline just because the project is small. Tailor depth, not rigor.

## SEMP: systems engineering management plan

The plan is important, but the planning process is more important. Build the SEMP by deciding how
the project will actually execute systems engineering, then record the decisions.

Include at least:
- mission and scope framing;
- lifecycle strategy;
- organization and roles;
- review and audit program;
- requirements-engineering approach;
- evaluation approach;
- configuration-management approach;
- technical-risk approach;
- integration with project management and ILS;
- tailoring rationale;
- update and maintenance cadence.

Keep the SEMP live. It must evolve with the project.

## Related disciplines and interfaces

### Project management
Work closely on scope, schedule, cost, and coordination of the technical program.

### Integrated logistics support
Work together from the earliest needs and requirements discussions so supportability is designed
in, not bolted on.

### Quality assurance
Coordinate on process integrity, audits, acceptance discipline, and evidence credibility.

### Requirements engineering
Stay tightly coupled; requirements are the technical foundation for planning, design, and
acceptance.

### Specialty engineering
Coordinate hardware, software, production, logistics, safety, EMC, environmental, and domain
specialists as part of the integrated effort.

## Management checklist

1. Is evaluation planned early enough to influence cost and schedule?
2. Is configuration visibility clear across all parties?
3. Are major technical risks visible, assessed, and owned?
4. Are reviews timed to technical maturity rather than calendar theater?
5. Is the development strategy appropriate to the real project context?
6. Is the SEMP an active management instrument rather than a static artifact?
7. Are PM, ILS, QA, and specialty disciplines integrated from the start?
