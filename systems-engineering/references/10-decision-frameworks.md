# 10 Decision Frameworks

## Contents
- [Use this reference when](#use-this-reference-when)
- [Framework 1: locate the real problem](#framework-1-locate-the-real-problem)
- [Framework 2: classify constraints before trading options](#framework-2-classify-constraints-before-trading-options)
- [Framework 3: mandatory, important, desirable screening](#framework-3-mandatory-important-desirable-screening)
- [Framework 4: COTS, MOTS, or new development](#framework-4-cots-mots-or-new-development)
- [Framework 5: subsystem balancing and design space](#framework-5-subsystem-balancing-and-design-space)
- [Framework 6: change-impact assessment](#framework-6-change-impact-assessment)
- [Framework 7: review-gate readiness](#framework-7-review-gate-readiness)
- [Framework 8: choose a development strategy](#framework-8-choose-a-development-strategy)
- [Framework 9: build the decision packet](#framework-9-build-the-decision-packet)
- [Framework 10: default systems-engineering closure questions](#framework-10-default-systems-engineering-closure-questions)

## Use this reference when

Use this file when the user needs a repeatable decision process rather than a descriptive summary:
phase identification, trade studies, COTS or MOTS versus development, change-impact assessment,
review readiness, or strategy selection.

## Framework 1: locate the real problem

Work in this order:
1. What lifecycle phase is the user actually in?
2. What abstraction level is the question really about?
3. What is the SOI?
4. Which external systems and interfaces matter?
5. Which baseline is currently controlling the work?

If any answer is missing, solve that missing framing problem first.

## Framework 2: classify constraints before trading options

Sort constraints into:
- business;
- project;
- external;
- design.

Then tag each as either:
- fixed;
- negotiable;
- assumed pending confirmation.

Do not compare solution options until fixed constraints are visible.

## Framework 3: mandatory, important, desirable screening

Use this when requirements are not yet fully closed.

### Step A: mandatory gate
Reject an option only when evidence demonstrates failure of an applicable mandatory requirement.
Record criterion ID, bound, units, environment, source, observed/estimated value, and disposition.
Use `unknown` when evidence is missing; unknown options cannot be selected as proven compliant.

### Step B: weighted comparison
Compare the survivors across important and desirable criteria.

### Step B2: Pugh matrix when pairwise comparison is needed

Select and name a datum; score the datum S on every criterion because it is compared with itself.
Record preference direction and the evidence or explicit assumption behind every comparison.
Score candidates S (same), + (better), or - (worse). Do not mix ordinal comparison with absolute
1-5 scoring, and do not invent cardinal meaning for an ordinal difference.

For each candidate compute separately:
- Count +: number of positive criterion ratings.
- Count -: number of negative criterion ratings.
- Net: Count + minus Count -.
- Weighted net (optional): sum(weight * rating), using + = 1, S = 0, - = -1.

Use nonnegative weights, the same criteria and datum for every candidate, and a documented
weight-elicitation method. Weights need not sum to one for a Pugh weighted net; state normalization
for other models. Recalculate every total. Keep rejected candidates out of winner selection;
show unknown candidates only as provisional comparisons. Never turn an important preference into
an undocumented mandatory gate after seeing scores. Report ties and sensitivity to weights,
uncertain ratings, and alternate datums. A provisional rank is not an approved selection.
Use `assets/templates/trade-off-analysis-matrix-template.md`.

### Step C: lifecycle cross-check
Before selecting the winner, force a review of:
- cost;
- schedule;
- technical risk;
- supportability;
- obsolescence;
- technical data adequacy;
- disposal impact.

## Framework 4: COTS, MOTS, or new development

### Ask these questions in order
1. Does a COTS item meet mandatory requirements and interfaces?
2. If not, can a controlled modification close the gap without destroying warranty, support, or
   data access?
3. If not, is new development justified by requirement criticality and lifecycle value?
4. Which option leaves the best whole-system balance after cost, schedule, risk, and support are
   considered?

### Default comparison factors
- functional compliance;
- performance compliance;
- interface compliance;
- cost and lead time;
- warranty and support agreements;
- technical data availability;
- obsolescence exposure;
- integration effort;
- through-life support burden.

## Framework 5: subsystem balancing and design space

When one subsystem struggles, do not immediately expand its budget or relax requirements locally.
Instead ask:
1. Which system-level constraints are driving the shortfall?
2. Which other subsystems have margin?
3. Can margin be reallocated without causing new system-level failures?
4. Does the new allocation still preserve whole-system balance?

Use this to avoid subsystem heroics that damage the integrated system.

## Framework 6: change-impact assessment

For every proposed change:
1. Identify the changed item and its current baseline.
2. Trace backward to the parent need or requirement.
3. Trace forward to child requirements, design items, interfaces, tests, support products, and
   review evidence.
4. Estimate cost, schedule, risk, and acceptance impact.
5. Present the change to the right decision authority with visible consequences.

## Framework 7: review-gate readiness

### SDR readiness
- mission, constraints, lifecycle concepts, and context are stable enough;
- STRS to SyRS traceability exists;
- preferred system-level solution is defensible;
- the functional baseline is ready to control.

### PDR readiness
- subsystem decomposition is coherent;
- major interfaces are identified;
- realization choices are defended;
- the allocated baseline is mature enough for detailed design.

### CDR readiness
- detailed design is complete enough for production;
- interfaces are fully understood;
- production or construction data is ready;
- unresolved technical risk is understood and acceptable.

### FQR readiness
- AT&E evidence exists;
- configuration is known;
- customer acceptance basis is explicit;
- transition-to-service enablers are ready.

## Framework 8: choose a development strategy

### Prefer waterfall when
- requirements are stable;
- the full system can be solved in one pass;
- technology is mature;
- time and money support a full one-pass solution.

### Prefer incremental when
- the full target is known broadly;
- delivery must occur in stages;
- later increments can be designed in from the start.

### Prefer evolutionary when
- future need is only partly known;
- change and learning are expected;
- the team accepts that future extensions may be constrained by the initial form.

## Framework 9: build the decision packet

When presenting a recommendation, include:
- decision statement;
- lifecycle phase and abstraction level;
- option set considered;
- mandatory gate result;
- trade summary;
- preferred option and rationale;
- affected baselines and interfaces;
- risks and mitigations;
- next review or approval action.

## Framework 10: default systems-engineering closure questions

Ask before concluding any major recommendation:
1. What higher-level need does this serve?
2. What lower-level realization or evidence does it drive?
3. Which interfaces does it touch?
4. Which baseline does it affect?
5. What verification proves it?
6. What validation question still remains?
7. What support and retirement implication follows from it?
