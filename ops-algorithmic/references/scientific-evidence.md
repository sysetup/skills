# Scientific Evidence Base

## How to use this file

Use these sources to justify engineering rules without overstating them. Distinguish mathematical results, controlled experiments, observational studies, systematic reviews, and standards. Report study population/task when it materially limits generalization.

## Evidence-to-rule map

| Engineering rule | Evidence and interpretation | Strength / limitation |
|---|---|---|
| Prove properties and invariants for nontrivial algorithms | Floyd (1967) and Hoare (1969) established formal frameworks for proving program properties, including assertions, pre/postconditions, and loop reasoning. | Mathematical/theoretical foundation; applicability depends on how formally the artifact is specified. |
| Treat control-flow complexity as a measurable property, not a full quality oracle | McCabe (1976) defined cyclomatic complexity from the control-flow graph. Lavazza, Morasca & Gatto (2023) found structural measures alone produced understandability models with roughly 30% average prediction error in their study. | Strong definition; empirical limitation shows the metric is incomplete as a human-comprehension proxy. |
| Prefer semantically descriptive identifiers when they add useful information | Schankin et al. (2018) studied 88 Java developers; descriptive compound identifiers led to semantic defects being found about 14% faster than shorter, less descriptive identifiers. | Controlled web-based experiment; result concerned semantic-defect comprehension, not every naming task. |
| Do not maximize identifier length blindly | Binkley, Lawrie, Maex & Morrell (2009) studied 158 programmers and found that longer production-code identifiers took more time to process and reduced correctness in a simple recall task. | Controlled task; supports information-efficient naming rather than "longer is always better." |
| Remove small syntax patterns that predictably mislead readers | Gopstein et al. (2017) experimentally tested candidate "atoms of confusion" with 73 participants, then transformations on larger programs with 43 participants; several patterns significantly increased misunderstanding versus behaviorally equivalent clarified code. | Controlled experiments; patterns originated partly from C/obfuscated-code contexts, so transfer requires language/context judgment. |
| Preserve visible block structure and formatting consistency, but avoid aesthetic dogma | Miara et al. (1983) found indentation level affected comprehension in a Pascal experiment. Oliveira et al. (2023) systematically reviewed 15 human-centric studies, finding positive evidence for some formatting choices but many null, conflicting, or outdated results. | Systematic review is the best summary; evidence does not justify universal camelCase/snake_case or brace-style mandates. |
| Treat readability as multi-factor, not reducible to one structural metric | Buse & Weimer (2010) collected judgments from 120 annotators, built a readability model, and reported correlations with changes/defect measures over >2.2M LOC. Later work, including Lavazza et al. (2023), shows structural metrics alone remain incomplete. | Human + repository evidence; correlations are not causation and models are context dependent. |
| Combine algorithm analysis with experiments for robust performance engineering | Experimental algorithmics/algorithm engineering literature explicitly treats design, implementation, and empirical evaluation as complementary steps in producing robust efficient software. | Field-level methodology; experiments require reproducible workloads and fair baselines. |
| Use multiple verification mechanisms | Basili & Selby (1987) compared code reading, functional testing, and structural testing with 32 professional programmers and 42 advanced students; effectiveness differed by subject group, program, and fault class. | Controlled experiment, but historical languages/tools and unit-scale programs limit direct quantitative transfer. |
| Use review as complementary quality assurance | McIntosh et al. (2014) studied Qt, VTK, and ITK and found review coverage/participation significantly associated with post-release defect outcomes. | Observational case study; association should not be stated as causal proof. |
| Treat maintainability as a quality characteristic that should be specified/evaluated | ISO/IEC 25010:2023 defines a product quality model with nine characteristics and supports quality requirements, design objectives, testing objectives, quality control, and acceptance criteria. | International standard; normative model, not a controlled causal experiment. |

## Interpretation safeguards

- Do not use an old controlled experiment as if it directly measures modern IDEs, languages, teams, or hardware.
- Prefer systematic reviews and replications over one isolated study when they conflict.
- Preserve quantitative details only when the source and task support them.
- State "associated with" for observational repository studies unless a causal design supports stronger language.
- Treat Big-O and proofs as mathematical claims under explicit models/assumptions; treat wall-clock speed as empirical.
- Prefer local project evidence (profiles, traces, benchmarks, defect history) over generic folklore when making a project-specific decision.
