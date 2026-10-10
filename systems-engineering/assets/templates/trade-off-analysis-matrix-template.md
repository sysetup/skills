# Trade-Off Analysis Matrix Template

## Scope and hard gates
- System, alternatives, decision authority, and baseline:
- Source of weights, preferences, assumptions, and uncertain data:
- Required margins, units, environment, and sensitivity cases:

| Criterion ID | Mandatory requirement / threshold | Candidate | Value / condition | Source / basis | Gate result | Disposition |
|---|---|---|---|---|---|---|
| [id] | [threshold/unit/envelope] | [candidate] | [observed/estimated/unknown] | [source] | [pass/fail/unknown] | [retain/reject/pending] |

A known mandatory failure rejects an option. Unknown compliance remains pending, not pass and
not proven failure. Do not let a favorable score override a hard gate. Do not silently promote
an important/desirable preference to a mandatory threshold after scoring.

## Pugh matrix

Keep every datum rating S. Score candidates +, S, or - relative to the same datum and preference
direction; document the evidence or labeled assumption behind every rating. Count signs separately.
Net = Count + minus Count -. Weighted net = sum(weight * rating), with + = 1, S = 0, - = -1.
Use nonnegative weights. An ordinal weighted net is a decision aid, not an objective physical metric.

| Criterion | Weight | Datum | Candidate A | Candidate B |
|---|---:|---|---|---|
| [criterion] | [weight] | S | [rating] | [rating] |
| Count + | | [count] | [count] | [count] |
| Count - | | [count] | [count] | [count] |
| Net | | [net] | [net] | [net] |
| Weighted net | | [sum] | [sum] | [sum] |

## Weighted score detail (separate absolute-rating method)

Define the 1-5 scale and preference direction for each criterion; do not mix it with Pugh signs.
State normalization and use the same scale/weights for every candidate. Show products and totals.

| Criterion | Weight | A score 1-5 | A weighted | B score 1-5 | B weighted | C score 1-5 | C weighted |
|---|---:|---:|---:|---:|---:|---:|---:|
| [criterion] | [weight] | [score] | [product] | [score] | [product] | [score] | [product] |
| Total | | | [sum] | | [sum] | | [sum] |

## Decision record
- Gate evidence and unresolved exclusions:
- Provisional ranking / ties / preference uncertainty:
- Weight, score, and datum sensitivity:
- Cost, schedule, support, obsolescence, data rights, integration, and retirement implications:
- Recommendation with conditions; authorized decision and record, or pending:

## Minimal example (illustrative ratings, not a supplier assessment)

All values below are assumed for an arithmetic exercise. Higher scores are preferred. Weights
are not normalized; multiplying every weight by the same positive constant preserves the rank.

| Criterion | Weight | A score 1-5 | A weighted | B score 1-5 | B weighted | C score 1-5 | C weighted |
|---|---:|---:|---:|---:|---:|---:|---:|
| Acquisition affordability | 1 | 5 | 5 | 3 | 3 | 1 | 1 |
| Support suitability | 2 | 3 | 6 | 4 | 8 | 5 | 10 |
| Total | | | 11 | | 11 | | 11 |

These weights produce a tie; no unique winner is justified. Candidate compliance is unassessed.
