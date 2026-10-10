# Failure Mode and Effects Analysis (FMEA) Template

## Governing method and rating basis
- Domain, analysis type, applicable method/edition, and scope:
- Approved S/O/D scales or other required prioritization scheme, source, and owner:
- Exposure, assumptions, rating rationale, and data limitations:
- Action rules and risk-acceptance authority:

RPN = S × O × D only when the chosen method uses it. Do not impose a universal numeric
threshold. Do not substitute RPN for AIAG/VDA Action Priority or other domain-specific methods.
Escalate credible safety/regulatory hazards independently of an RPN. Missing rating evidence stays
open; a worked 1-10 scale example is not a domain-approved scale or a quantitative failure probability.

## FMEA register

| ID | Item / CI | Function | Failure mode | Cause | Local effect | Next-higher effect | End effect | S | O | D | RPN | Current detection | Mitigation | Owner | Residual S | Residual O | Residual D | Residual RPN | Residual basis | Evidence | Linked req |
|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---:|---:|---:|---:|---|---|---|
| FM-001 | [item] | [function] | [mode] | [cause] | [effect] | [effect] | [effect] | [S] | [O] | [D] | [product] | [control] | [action] | [owner] | [S] | [O] | [D] | [product] | [projected/demonstrated] | [actual evidence or none] | [id] |

## Rating and action rationale

| FMEA ID | Current rating basis | Residual rating basis | Severity rationale | Verification event / owner | Due gate | Acceptance decision |
|---|---|---|---|---|---|---|
| FM-001 | [source and justification of each factor] | [forecast or measured basis for each factor] | [why consequence changes or stays] | [event/owner] | [gate] | [actual decision or pending] |

Calculate both products from stated factors. Do not reduce severity merely for improved detection
or lower occurrence. A lower forecast product does not close an action. For demonstrated residual
risk, inspect the mitigation evidence and retain baseline, conditions, review, and acceptance record.

## Minimal example (synthetic arithmetic only)

Illustrative ratings: S=9 denotes a hazardous loss-of-control consequence; O=4 and D=6 are assumed
exercise ratings, not empirical probabilities or approved scales. Proposed O=2 and D=4 are targets.

| ID | Item / CI | Function | Failure mode | Cause | Local effect | Next-higher effect | End effect | S | O | D | RPN | Current detection | Mitigation | Owner | Residual S | Residual O | Residual D | Residual RPN | Residual basis | Evidence | Linked req |
|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---:|---:|---:|---:|---|---|---|
| FM-001 | propulsion | sustain controlled flight | motor stops | motor/drive failure | thrust loss | loss of control | hazardous descent | 9 | 4 | 6 | 216 | assumed temperature monitoring | evaluate propulsion fault tolerance and segregated energy; prove control margin | propulsion lead | 9 | 2 | 4 | 72 | projected | none | SYR-001 |

Severity remains 9 because the hazardous consequence has not been shown to change. Dual ESCs or
batteries do not independently solve every motor failure. Current and residual figures are
illustrative; action effectiveness, scales, and acceptance remain OPEN.
