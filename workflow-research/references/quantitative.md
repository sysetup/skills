# Quantitative methods

Load for experimental or nonexperimental plans. Worldview default: postpositivist.

Causal language rule: use "cause", "impact", "effect of", "mejora" as a confirmed claim only when the design has a credible counterfactual (typically random assignment or a strong quasi-design). Correlational and survey results use associate, predict, differ, co-vary.

## Experimental family

### True experiment checklist

1. Participants — eligibility, recruitment, random assignment procedure (unit of randomization: person, class, site).
2. Design name and diagram in words — groups × time × treatment. Prefer pretest–posttest control group when a baseline is available; posttest-only when pretest would itself treat; factorial when two or more IVs are crossed; Solomon four-group when pretest sensitization is a plausible threat.
3. Independent variable — operational definition, levels (e.g. GenAI-assisted with protocol vs business-as-usual), dose, duration, fidelity check (what counts as receiving the treatment).
4. Dependent variable(s) — operational definition, instrument, metric, timing. Academic performance is not a variable until it is a score, rubric, or GPA window.
5. Covariates / controls — prior achievement, hours of study, prior tool use. Pre-specify.
6. Procedure — sequence, blinding if any, contamination controls (especially for tools students can share), attrition rule (intent-to-treat vs per-protocol).
7. Analysis — match to the design: independent t or Mann–Whitney (posttest-only, two groups); mixed ANOVA or ANCOVA (pretest–posttest); factorial ANOVA; linear mixed model if clustered (students in classes). Effect size (Cohen's d, η², or equivalent) and assumption checks. Alpha pre-specified. No fishing.
8. Validity threats — name only those that can bite this design; state the control or residual risk (section below).

### Quasi-experiment extras

Name the design (nonequivalent groups, interrupted time series, regression discontinuity). Add threats: selection, selection–maturation, regression to the mean. Do not relabel a quasi-design a true experiment.

## Nonexperimental family

### Survey plan checklist

1. Design — cross-sectional or longitudinal. Justify.
2. Population — inclusion rules, setting, time window.
3. Sampling — frame, strategy (simple, stratified, cluster, systematic, convenience), planned n, power or precision rationale if estimable. If power cannot be computed, say so and use a precision or named rule-of-thumb without fake numbers.
4. Instrumentation — source of items, construct map, scales, reliability evidence from prior use, translation or adaptation notes, pilot plan. Draft the instrument with `assets/instruments.md`.
5. Variables — independent, dependent, control, mediating, moderating. Each operational definition.
6. Procedure — recruitment, mode (web, phone, paper, intercept), timing, nonresponse plan.
7. Analysis — descriptive stats, missing-data rule, inferential tests or models matched to the hypotheses, effect sizes, assumption checks.
8. Interpretation — what a significant or non-significant result would mean; what it would not mean.

### Correlational / causal-comparative

- State the relationship or pre-existing grouping.
- Control variables named.
- No manipulation, no causal verbs.
- Analysis: correlation, regression, path/SEM only if the n and measurement model support it; group comparison on a non-manipulated factor is causal-comparative, not an experiment.

## Sample size

Compute power when σ, effect size, and α can be justified from literature or a pilot. If not, write `power: not computed` and a precision target (e.g. 95% CI half-width) or a cited convention. Never invent n as if it were already collected. Clustered experiments power on the number of clusters, not only on heads.

## Reliability and construct validity of measures

Plan at least one reliability estimate appropriate to the instrument: Cronbach's alpha or ω for scales, test–retest if stability matters, inter-rater if human scoring. Construct: content evidence (blueprint vs items), criterion if a gold standard exists, convergent/discriminant if multiple constructs. Mono-operation and mono-method bias are construct-validity threats — name them when a single exam or a single self-report carries the DV.

## Internal validity threats to scan

History, maturation, testing, instrumentation, statistical regression, selection, mortality/attrition, selection–maturation interaction, diffusion of treatment, compensatory rivalry, resentful demoralization, experimenter effects.

Name only the threats that can actually bite this design. State the control or the residual risk. For interventions that are copyable tools (generative AI, shared notes), diffusion is usually first-class — control by section-level assignment, usage logs, or honor-code plus contamination items, and still list residual risk.

## External, construct, statistical-conclusion

- External — persons, settings, times, treatment variations the result may not travel to.
- Construct — whether the measure is the construct; mono-operation and mono-method bias.
- Statistical conclusion — low power, violated assumptions, fishing, unreliable measures. Do not invent p-values.

## Agent execution

Claim license: `references/inference-license.md`.

- If the user supplies a dataset, analyze it. State software or method. Report assumptions and missingness.
- If no dataset exists, do not simulate fake respondents. Deliver the protocol, instruments, empty result tables, consistency matrix, and timeline.
- Secondary quantitative data (public stats, papers with usable numbers) may enter Findings only as others' estimates, as context/covariates, or when the named design is a literature-review study. They do not license this study's causal Findings under an experimental family that was not run. Cite the source of every number.
