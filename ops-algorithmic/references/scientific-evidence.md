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

## Key sources

1. Floyd, R. W. (1967). *Assigning Meanings to Programs*. Proceedings of Symposia in Applied Mathematics, 19, 19-32. DOI: 10.1090/psapm/019/0235771
2. Hoare, C. A. R. (1969). *An Axiomatic Basis for Computer Programming*. Communications of the ACM, 12(10), 576-580. DOI: 10.1145/363235.363259
3. McCabe, T. J. (1976). *A Complexity Measure*. IEEE Transactions on Software Engineering, SE-2(4), 308-320. DOI: 10.1109/TSE.1976.233837
4. Miara, R. J., Musselman, J. A., Navarro, J. A., & Shneiderman, B. (1983). *Program Indentation and Comprehensibility*. Communications of the ACM, 26(11), 861-867. DOI: 10.1145/182.358437
5. Basili, V. R., & Selby, R. W. (1987). *Comparing the Effectiveness of Software Testing Strategies*. IEEE Transactions on Software Engineering, SE-13(12), 1278-1296. DOI: 10.1109/TSE.1987.232881
6. Oman, P. W., & Cook, C. R. (1991). *A Programming Style Taxonomy*. Journal of Systems and Software, 15(3), 287-301. Use as a taxonomy/history source rather than proof that any one style is superior.
7. Takang, A. A., Grubb, P. A., & Macredie, R. D. (1996). *The Effects of Comments and Identifier Names on Program Comprehensibility: An Experimental Investigation*. Journal of Programming Languages, 4(3), 143-167.
8. Buse, R. P. L., & Weimer, W. (2010). *Learning a Metric for Code Readability*. IEEE Transactions on Software Engineering, 36(4), 546-558. DOI: 10.1109/TSE.2009.70
9. Gopstein, D., Iannacone, J., Yan, Y., DeLong, L., Zhuang, Y., Yeh, M. K.-C., & Cappos, J. (2017). *Understanding Misunderstandings in Source Code*. ESEC/FSE, 129-139. DOI: 10.1145/3106237.3106264
10. Schankin, A., Berger, A., Holt, D. V., Hofmeister, J. C., Riedel, T., & Beigl, M. (2018). *Descriptive Compound Identifier Names Improve Source Code Comprehension*. ICPC 2018, 31-40. DOI: 10.1145/3196321.3196332
11. Binkley, D., Lawrie, D., Maex, S., & Morrell, C. (2009). *Identifier Length and Limited Programmer Memory*. Science of Computer Programming, 74(7), 430-445. DOI: 10.1016/j.scico.2009.02.006
12. Zhu, Q., Panichella, A., & Zaidman, A. (2018). *A Systematic Literature Review of How Mutation Testing Supports Quality Assurance Processes*. Software Testing, Verification and Reliability, 28(6). DOI: 10.1002/stvr.1675
13. Oliveira, D., Santos, R., Madeiral, F., Masuhara, H., & Castor, F. (2023). *A Systematic Literature Review on the Impact of Formatting Elements on Code Legibility*. Journal of Systems and Software, 203, 111728. DOI: 10.1016/j.jss.2023.111728
14. Lavazza, L., Morasca, S., & Gatto, M. (2023). *An Empirical Study on Software Understandability and Its Dependence on Code Characteristics*. Empirical Software Engineering, 28, 155. DOI: 10.1007/s10664-023-10396-7
15. McIntosh, S., Kamei, Y., Adams, B., & Hassan, A. E. (2014). *The Impact of Code Review Coverage and Code Review Participation on Software Quality: A Case Study of the Qt, VTK, and ITK Projects*. MSR 2014, 192-201. DOI: 10.1145/2597073.2597076
16. Fleischer, R., Moret, B., & Schmidt, E. M. (eds.) (2002). *Experimental Algorithmics: From Algorithm Design to Robust and Efficient Software*. LNCS 2547. DOI: 10.1007/3-540-36383-1
17. ISO/IEC 25010:2023. *Systems and Software Engineering — Systems and Software Quality Requirements and Evaluation (SQuaRE) — Product Quality Model*.

## Interpretation safeguards

- Do not use an old controlled experiment as if it directly measures modern IDEs, languages, teams, or hardware.
- Prefer systematic reviews and replications over one isolated study when they conflict.
- Preserve quantitative details only when the source and task support them.
- State "associated with" for observational repository studies unless a causal design supports stronger language.
- Treat Big-O and proofs as mathematical claims under explicit models/assumptions; treat wall-clock speed as empirical.
- Prefer local project evidence (profiles, traces, benchmarks, defect history) over generic folklore when making a project-specific decision.
