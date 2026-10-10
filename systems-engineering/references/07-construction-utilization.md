# 07 Construction and Utilization

## Contents
- [Use this reference when](#use-this-reference-when)
- [Construction and production intent](#construction-and-production-intent)
- [Production and construction planning inputs](#production-and-construction-planning-inputs)
- [V-model mapping](#v-model-mapping)
- [Verification methods](#verification-methods)
- [Configuration audits during build](#configuration-audits-during-build)
- [Test and evaluation across the lifecycle](#test-and-evaluation-across-the-lifecycle)
- [FQR: formal qualification review](#fqr-formal-qualification-review)
- [Transition to service](#transition-to-service)
- [Support hierarchy during utilization](#support-hierarchy-during-utilization)
- [Modifications and upgrades](#modifications-and-upgrades)
- [Retirement and disposal](#retirement-and-disposal)
- [Through-life checklist](#through-life-checklist)
- [Evidence control](#evidence-control)

## Use this reference when

Use this file when the problem is about producing the system, verifying the as-built result,
transitioning to service, running the support system, managing modifications, or planning
retirement and disposal.

## Construction and production intent

By this stage the ability to influence architecture cheaply is rapidly diminishing. The dominant
systems-engineering task is to confirm that the system being built is the system that was designed
and specified.

## Production and construction planning inputs

Plan early for:
- plant, facilities, and specialized equipment;
- long-lead items and storage conditions;
- material shelf-life and handling constraints;
- skilled human resources and sequencing;
- integration and support-system readiness.

Work with production specialists and ILS specialists in parallel with design, not after design.

## V-model mapping

The left side of the V specifies and decomposes. The right side verifies and validates against
the matching left-side product.

| Left-side product | Right-side activity |
|---|---|
| Stakeholder / business need | Validation and OT&E |
| System requirements | System verification and AT&E |
| Allocated subsystem specifications | Subsystem verification |
| Detailed design / configuration items | CI verification and DT&E |
| Implementation | Integration test |

The T&E labels above are illustrative program categories, not a universal bijection with V
levels. Tailor their scope in the SEMP and keep product verification distinct from user validation.

Write the plan with `assets/templates/vv-plan-template.md`. Procedure detail lives in
`references/11-mbse-interfaces-vv.md`.

## Verification methods

Use one or more of the standard methods according to the requirement.

### Inspection
Use direct observation when a requirement can be confirmed visually or dimensionally.

### Analysis
Use justified mathematical/engineering models, calculations, and suitable data with stated
assumptions and uncertainty. Reviewing a certificate is not automatically an engineering analysis;
classify document inspection and third-party claims accurately.

### Test
Use controlled procedures, instruments, measurement, and data collection when performance must be
measured under defined conditions.

### Demonstration
Use operational showing or walk-through when simple successful behavior is the key evidence.

## Configuration audits during build

### Functional configuration audit (FCA)

Use the verification record to confirm that the documented functional and performance description
matches the realized system.

### Physical configuration audit (PCA)

Confirm that the as-built physical system matches the physical documentation.

Important rule: some physical evidence exists only during construction or production. Audit while
buried interfaces, hidden services, or transient assemblies are still observable.

## Test and evaluation across the lifecycle

### DT&E
Developmental test and evaluation supports design and development. Use it to detect technical
problems early, confirm redesign, and retire technical uncertainty progressively.

### AT&E
Acceptance test and evaluation verifies the delivered system against the system requirement set so
the customer can accept it.

### OT&E
Operational test and evaluation validates the capability in realistic operational use, with real
users, support arrangements, and environment.

## FQR: formal qualification review

Use FQR where the governing project defines such a review; record tailored entry/exit criteria
and authority. A review checklist or a passing test is not itself customer acceptance or
authorization to enter service. Inspect actual evidence and the authorized decision.

## Transition to service

Before introduction to service, confirm that the enabling system exists, including:
- facilities;
- trained personnel;
- training systems;
- maintenance and engineering support arrangements;
- supply support and spare parts;
- support equipment;
- operating procedures and instructions.

Do not declare service entry merely because the material system exists.

## Support hierarchy during utilization

### Operational support
Routine user-level care and basic actions needed to keep the system functioning day to day.

### Maintenance support
Preventive and corrective actions that restore the system without materially changing its design.

### Engineering support
Deeper support that depends on design knowledge, controlled data, and often modification or upgrade
activity.

Engineering support must be designed into the lifecycle. It will not appear automatically later.

## Modifications and upgrades

Treat each significant modification as a controlled mini systems-engineering effort.

Trigger modification work when:
- users raise new requirements;
- the environment changes;
- obsolescence erodes supportability;
- testing reveals latent defects;
- support cost or effort becomes unacceptable.

Where possible, build expandability and upgradeability into the original design so later changes
are less disruptive.

## Retirement and disposal

Typical disposal drivers include:
- need no longer exists;
- system is too difficult or costly to support;
- replacement capability is entering service;
- changed mission makes the current system unsuitable.

Possible end states include:
- resale or transfer;
- scrapping or destruction;
- material recycling;
- repurposing into training aids, museum pieces, or other secondary roles.

### Disposal cautions
Check for:
- hazardous materials;
- sensitive or classified information;
- environmental laws and disposal constraints;
- obligations to preserve records or training value.

A system's operational retirement may be the start of a different lifecycle in another role.

## Through-life checklist

1. Is the as-built configuration known and documented?
2. Do verification records support the baseline and acceptance claim?
3. Are facilities, personnel, training, support, and procedures ready for service entry?
4. Is engineering support enabled by accurate data?
5. Are modification triggers and change pathways controlled?
6. Is there a credible disposal or repurposing path?

## Evidence control

Apply reference 12: separate expected records, actual runs, checked outcomes, risk acceptance,
and operational authorization. Report failed/inconclusive results and configuration limitations.
