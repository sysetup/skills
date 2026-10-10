# Writing and ethics

## Proposal / report spine

Use this order unless the user or venue mandates another.

1. Title
2. Abstract (problem, approach, method, expected or actual contribution)
3. Introduction — hook, problem evidence, literatures addressing it, deficiencies, significance for audiences (Creswell introduction logic)
4. Purpose statement
5. Questions and/or hypotheses
6. Worldview and theory (short)
7. Methods (sampling, instruments, procedure, analysis)
8. Consistency matrix (body or appendix; required)
9. Validation / trustworthiness / integration validity
10. Timeline
11. Findings (if executed)
12. Integration / discussion
13. Limitations, ethics, next actions
14. References actually used
15. Instruments appendix
16. Execution log / replication package if analysis ran

Keep academic ceremony only when the audience is a committee or journal. For product, policy, or newsroom work, keep the same logic in shorter headings. Never drop validity and source quality. The matrix is required on protocol/thesis work; a desk study may attach a compact matrix or omit it when findings-first is the deliverable.

## Ethical minimum (always)

- Identify human-subjects risk. If humans are involved, require consent language, withdrawal, confidentiality, data-minimization, and a plan for distress or power imbalance.
- Do not scrape or quote private individuals in a way that identifies them without a legal and ethical basis.
- Flag vulnerable populations. Transformative studies need extra care about voice, benefit, and harm. Studies of people who lost work (e.g. replacement by automation) treat economic and psychological risk as first-class.
- Separate the agent's synthesis from the user's unpublished data. Do not leak secrets into public-sounding prose.
- Cite. Do not invent references. If a source cannot be verified, drop it or mark unverified.
- For AI-assisted research, disclose that an agent drafted or searched, and that human verification is required for high-stakes claims.

## Algorithmic instrument bias

The agent is an instrument, not a neutral window on the literature. Name the threats that can actually bite this study and the control for each. Log them in `assets/research-protocol.md` §6.

| Threat | What it does | Control |
| --- | --- | --- |
| Confirmation from prompting | Search strings and inclusion follow the user's preferred answer | Include contrary strings; keep a rejected-source note for disconfirming hits |
| Recency in indexes | Ranked search overweights recent or popular pages | Date-bound queries; retrieve canonical older primary sources |
| Homogenization of summaries | Paraphrase collapses disagreement into false consensus | Keep rival claims on the map; quote, do not only paraphrase |
| Authority laundering | Generated synthesis is treated as a source | Every empirical claim cites a retrieved source; never cite the model |
| Coverage holes | Languages, paywalls, or unindexed literature missing | State corpus limits in Limitations; do not imply exhaustive coverage |

Reflexivity minimum: one short paragraph on how the prompt, tools, and coding rules could have shaped the corpus. Qualitative studies still keep the human-site bias log in `references/qualitative.md`; this section covers the agent as instrument for every approach.

## Writing rules

- Purpose statement first, then questions. Questions must not wander outside the purpose.
- Introductions follow deficiency logic, not chronology of everything ever written.
- Methods are procedures a second researcher could attempt to replicate or audit.
- Findings answer questions only under the named design's inference license (`references/inference-license.md`). Discussion interprets. Recommendations are optional and labeled as such.
- Limitations are design-true, not modest theater.
- The consistency matrix is the alignment check for Creswell's purpose–question–methods consistency. Do not attribute the matrix itself to Creswell.

## Audience adaptation

Intensity follows `SKILL.md` (Artifacts by deliverable). Do not promote a desk inquiry into a thesis spine, and do not strip alignment from a committee chapter.

- Thesis / article — full spine, purpose scripts, matrix, ethics section, instruments.
- Client memo — problem, method in one paragraph, findings, confidence, what was not studied; attach a compact matrix.
- Rapid desk inquiry / executed "investiga" — lead with answers to the questions; then approach line, purpose, RQ, ranked evidence, inference, recommendation, validity note, sources, execution log, limits. Four PRISMA-adapted counts when the corpus is literature. Compact matrix if it fits; skip empty instrument and timeline sections instead of shipping instructional brackets.
- Clarification-stop — six questions only. No spine, no fake protocol.
