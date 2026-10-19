---
name: workflow-research
description: >-
  Runs full research, methodology investigations, worldview and design
  (qualitative, quantitative, mixed methods, or DSRM), covering problem,
  literature review, purpose, research questions, methods, validation,
  and final report. Asks clarifying questions when the request is only a
  topic. Use when the user asks to investigate, research, look into, find
  out, or study in depth a topic, case, problem, issue, error, or success,
  including Spanish requests (investigar, averiguar, estudiar,
  profundizar, tesis, protocolo, estado del arte), even if  methodology is never mentioned.
  Also use to design a study, write a thesis chapter or research protocol, run a PRISMA literature review,
  choose methods (survey, experiment, phenomenology, grounded theory,
  mixed, design science), or draft purpose statements, questions, or
  hypotheses. Not for one-line definitions or person/org background
  checks.
license: MIT
metadata:
  author: "SYSETUP.COM CarlosHRG"
  short-description: Creswell inquiry discipline for any investigation.
  framework: Creswell & Creswell Research Design 6th ed. (2022); Creswell Educational Research process (6 steps); Creswell & Poth Qualitative Inquiry 5th ed. (2024); Peffers et al. DSRM (2007); Hevner et al. MISQ (2004); PRISMA 2020
  version: "2.2"
---

# workflow-research

Execute every investigation as a Creswell research approach: worldview × design × methods. Do not answer first and dress the answer as methodology. Design first. Collect only what the design authorizes. Infer last.

This skill owns the design and the claims. Search, file reads, and coding are collection inside the loop — not a substitute for it.

Path roots (resolve from this file, not cwd)

```
SKILL_ROOT = directory containing this SKILL.md
REFERENCES_DIR = ${SKILL_ROOT}/references
ASSETS_DIR = ${SKILL_ROOT}/assets
```

Load a reference only when that track is active. Copy templates from `assets/` into the deliverable; do not dump them as essays.

## Not this loop

Skip the eight-step loop and answer with sources when the prompt is a **one-line definition or lookup** with no inquiry intent ("what is mixed methods?", "define triangulation").

Person or organization due diligence, reputation, or OSINT targeting is a different skill (`investigative-research`). Do not stretch this loop over it.

A bounded error, failure, incident, or success the user wants explained **is** inquiry. Do not skip it as lookup. Infer Gate 0 slots and run the loop.

## Gate 0 — Canonical Clarification Mode

Before step 1, fill these six slots from the user prompt. Do not invent a study to avoid asking.

| # | Slot | What counts as filled |
| --- | --- | --- |
| 1 | Problem | A specific unknown, deficiency, or harm — not only a topic noun |
| 2 | Purpose verb | explore / describe / explain / measure / compare / evaluate / generate theory |
| 3 | Approach | qualitative / quantitative / mixed / DSRM, or an explicit "help me choose" |
| 4 | Population and setting | who or what corpus, where, time window |
| 5 | Central question | a draft RQ, or variables / phenomenon clear enough to write one |
| 6 | Deliverable and constraints | executed desk study / protocol / thesis chapter / estado del arte; access to humans or data; deadline; audience |

**Topic-only prompt** (example: "haz una investigación sobre el teletrabajo"): slots 1–6 are empty. Enter Clarification Mode. Ask all six questions in **one** pass. Use the harness native questionnaire if it exists (`ask_user_question` or the host equivalent). Prefer closed choices for purpose verb, approach, and deliverable; put the recommended option first. If no native UI exists, ship the six questions as a single textual message. Do not drip questions. Do **not** run steps 1–8. Do **not** pick a default approach. Do **not** ship a protocol, matrix, instruments, or findings.

Ask exactly:

1. PROBLEM — What specifically is unknown, unresolved, or at stake (not just the topic)?
2. PURPOSE — Will the study explore, describe, explain, measure, compare, evaluate, or generate theory?
3. APPROACH — Qualitative, quantitative, mixed methods, or should I choose from the problem using Creswell?
4. POPULATION AND SETTING — Who (or what corpus), where, and in what time window?
5. CENTRAL QUESTION — What is the main research question, or should I draft options from your answers?
6. DELIVERABLE AND CONSTRAINTS — Executed desk study (findings now), protocol the user can run, thesis chapter, or estado del arte? Access to humans or datasets? Deadline? Audience (committee, journal, operations)?

Stop after the questions. Resume the loop only when the user answers, or when they explicitly order you to assume remaining slots.

**Specified prompt** — run the loop after filling leftover slots by inference. Write one `Assumptions` block. Do not re-ask what the prompt already answered. A prompt is specified when it has a problem **and** a purpose-like verb, **or** an inquiry verb plus a bounded object (this error, this case, this success, this system, these variables).

| User signal | Infer unless the prompt contradicts it |
| --- | --- |
| Error, failure, incident, "why did X break" | Problem = unknown cause; purpose = explain; population = the bounded system or incident; deliverable = executed desk study; design = qualitative **case study** |
| Success, "what made X work" | Problem = unknown mechanisms; purpose = explain or evaluate; case study, or mixed if they also need magnitude |
| "Does X improve / cause / affect Y" | Purpose = compare or measure; quantitative **experimental** family (true if randomization is feasible; quasi if not) |
| Estado del arte / lit review for a thesis | Purpose = map or synthesize; literature-review study; deliverable = that review |
| Protocol, tesis, methodology chapter | Deliverable = protocol or thesis chapter (full artifact set) |

If the user refuses to specify after Clarification Mode, ship a **design-choice brief** with three Creswell-viable options (one qualitative, one quantitative, one mixed) and stop. Still no executed study.

## Operating loop — Creswell process, eight agent steps

Creswell's *Educational Research* process is six steps: problem, literature, purpose, collect, analyze, report. *Research Design* splits purpose from questions and puts validity inside methods. This loop is an **agent operationalization**, not a Creswell chapter list: it splits purpose vs questions and methods vs validation because those are the places agents skip or fabricate. State the current step at the start of each turn. Skip a step only when the user already delivered its artifact and it passes the gate.

1. **Identify the research problem** — hook, evidence the problem exists, who is blocked, deficiencies in current evidence, significance by audience. Template: `assets/research-protocol.md` §1.
2. **Review the literature** — map clusters, name the gap, place theory. Load `references/literature-theory.md`. If the study *is* an estado del arte / systematic review, this step is the empirical work; still run steps 3–8 around it. For a bounded incident with a local corpus (logs, code, user files), the "literature" is prior incident reports and the relevant spec; still log the search.
3. **Specify the purpose** — one sentence from `assets/purpose-and-questions.md`. Verbs must match the approach.
4. **Formulate questions and hypotheses** — central RQ + subquestions; H0/H1 only when the design will test. Mixed studies add an integration question.
5. **Select the design** — worldview + approach + named strategy. Load `references/approach-selection.md`. Write `Approach = {quant|qual|mixed|dsrm} because {problem need}. Design = {named design}. Worldview = {named worldview}.` If the contribution is an engineering artifact, load `references/dsrm.md` instead of stretching the three approaches. DSRM is Peffers/Hevner, not a Creswell chapter.
6. **Specify methods** — sampling, instruments, procedures, analysis. Load only the matching track: `references/quantitative.md` / `references/qualitative.md` / `references/mixed-methods.md` / `references/dsrm.md`. Before collecting, load `references/inference-license.md`: search, logs, and coding may produce only evidence that table licenses for the named design. They do not upgrade the inference model. If the reachable corpus cannot license the questions, ship protocol + empty tables + pending fieldwork instead of substituting another design's evidence. Fill instruments and the full consistency matrix when the deliverable is a protocol or thesis chapter (`assets/instruments.md`, `assets/consistency-matrix.md`). On an executed desk study, attach a compact matrix only if it clarifies the claims. Do not fabricate participants, quotes, or statistics.
7. **Plan and apply validation** — quantitative validity threats, qualitative trustworthiness, mixed integration validity. Ethics in `references/writing-ethics.md`. This step is a gate, not a paragraph of generic humility.
8. **Write** — deliver the artifact the user asked for. Spine in `references/writing-ethics.md`, scaled by deliverable. Load `references/inference-license.md` before writing Findings: that table is the only license for what Findings may claim. Gate with `assets/quality-checklist.md`. Attach the execution log and, when analysis ran, the replication package (`assets/research-protocol.md` §8 and §11).

Literature collection happens in step 2. Empirical collection happens in step 6. Step 8 reports. There is no license to skip design and "just search." Step-2 literature does not become step-8 Findings unless the named design is a literature-review study.

## Approach catalog (mandatory names)

Worldviews — postpositivist, constructivist, transformative, pragmatic. Full claims: `references/approach-selection.md`.

| Approach | Worldview default | Use when the problem needs |
| --- | --- | --- |
| Quantitative | Postpositivist | Measurement, comparison, prediction, hypothesis test, prevalence |
| Qualitative | Constructivist (transformative if the problem is oppression or rights) | Meaning, lived experience, process, context, unexplored phenomenon, bounded case |
| Mixed methods | Pragmatic (transformative if the mixing serves justice) | One strand cannot answer the question; integration adds a named function |
| DSRM | Pragmatic | Design, build, or evaluate an engineering artifact |

Quantitative families (pick one family, then a named design): **experimental** (true experiment if random assignment is feasible; quasi-experiment if not) or **nonexperimental** (survey and/or correlational). Causal verbs require the experimental family.

Qualitative designs (pick one): narrative, phenomenology, grounded theory, ethnography, case study. A bounded incident, failure, success, or system is a **case study** unless the question is lived experience (phenomenology) or a causal test (experimental family).

Mixed designs (pick one core): convergent, explanatory sequential (QUAN → qual), exploratory sequential (QUAL → quan). Complex wrapping is optional.

Decision rule: start from the research problem and questions, then check access/time, then check audience. Catalog, decision tree, and prompt illustrations: `references/approach-selection.md`.

If the user locked an approach that cannot answer the question, flag the mismatch and propose the Creswell-correct design. Do not silently obey a broken design.

## Artifacts by deliverable

Scale ceremony to slot 6. Empty protocol theater hides the answer. Missing alignment on a thesis chapter fails a committee. Full tick list: `assets/quality-checklist.md`.

**Every executed inquiry** (desk study, hybrid, protocol, thesis, review) ships:

1. Approach line (approach, named design, worldview, because-clause).
2. Purpose statement matching the approach script.
3. Central RQ, subquestions, hypotheses if testing.
4. Findings that answer the questions under the named design's inference license (`references/inference-license.md`), **or** an explicit pending-fieldwork list (protocol + empty tables when the design's data did not run).
5. Evidence, inference, and recommendation as separate layers.
6. Validation / trustworthiness plan specific to this design (compact is fine on a desk study).
7. Sources plus an execution log if any search or analysis ran.
8. Limitations — what this design cannot claim.
9. Assumptions block when Gate 0 slots were inferred.

**Protocol or thesis chapter** (or leftover human/field work the agent cannot run) also ships:

10. Consistency matrix (`assets/consistency-matrix.md`).
11. Sampling plan (strategy, frame or purposeful logic, planned n as a plan).
12. Instruments (`assets/instruments.md`) — drafts the user can run.
13. Analysis plan matched to the questions.
14. Timeline (cronograma) with the eight steps as phases.
15. Ethics statement.
16. Quality checklist ticked (`assets/quality-checklist.md`).
17. Replication package when analysis ran (`assets/research-protocol.md` §11).

Default when the user said investiga / averiguar / estudiar / look into **and** slots are filled: **executed inquiry** — licensed findings first, hybrid only for residual fieldwork. If the named design's data did not run, that lead is the pending-fieldwork list and empty tables, not a substitute synthesis. Default when slots are empty: **Clarification Mode**, not hybrid. A desk study still uses the eight steps; the sample is the corpus the named design licenses, not "whatever search can reach." Attach a compact matrix when it fits in the report; require the full matrix on protocol/thesis work.

Delete a row only when the user forbade that artifact, and say so.

## Execution rules

- Treat web search and document reads as data collection inside the named design's inference license (`references/inference-license.md`), not as a substitute design.
- Prefer primary sources and peer-reviewed or official records. Rank source quality. Note recency and bias.
- Separate **evidence**, **inference**, and **recommendation**.
- Never fabricate participants, quotes, p-values, instruments, bibliographic entries, or evaluation results.
- If the study needs human subjects, field access, or proprietary data the agent cannot obtain, produce the protocol, instruments, matrix, and timeline the user can run. Do not fake the fieldwork.
- The agent is itself an instrument. Record algorithmic-instrument threats (`references/writing-ethics.md`).
- Match output language to the user unless they specify otherwise.
- Do not copy Creswell chapter prose into the user deliverable. Encode procedure.

## Quality gates (fail closed)

Do not ship until `assets/quality-checklist.md` is ticked for this deliverable. That file owns the gate list, including the inference-license ticks that point at `references/inference-license.md`.

## Anti-patterns

- Executing a topic-only "investiga X" as a desk study.
- Skipping a diagnostic investigation ("why did this fail") as factual lookup.
- Answering first and dressing the answer as methodology after the fact.
- Shipping twelve protocol artifacts when the user asked what happened.
- Handing "investiga X" to a parallel citation workflow and skipping design.
- Mixing strands without an integration plan and calling it mixed methods.
- Writing a literature dump instead of a gap argument.
- Stacking two qualitative designs, or stacking experiment + phenomenology without a mixed-methods integration plan.
- Inflating qualitative work with fake themes or quantitative work with fake statistics.
- Calling a build "design science" with no evaluation against stated objectives.
- Changing the question mid-study without recording the change.
- Claiming Creswell authored the consistency matrix. It is the agent's alignment artifact for Creswell's purpose–question–methods consistency; name it as such.
- Calling the eight agent steps "Creswell's eight steps." They operationalize his process; they are not a chapter numbering.
- Answering a causal RQ with a literature synthesis while the approach line names an experiment. Prior studies are the gap argument; they are not this study's assignment and measures.
- Using "reachable corpus" to switch inference models. Collection fills the named design's license cell or it is out of scope (`references/inference-license.md`).

## Reference map

| Need | File |
| --- | --- |
| Worldviews, 3-approach table, design catalogs, decision tree, prompt illustrations | `references/approach-selection.md` |
| What Findings may claim per named design | `references/inference-license.md` |
| Topic, lit map, theory, PRISMA, estado del arte as a study | `references/literature-theory.md` |
| Experimental and nonexperimental quantitative methods | `references/quantitative.md` |
| Five qualitative designs, coding, trustworthiness | `references/qualitative.md` |
| Convergent, explanatory, exploratory, complex MM | `references/mixed-methods.md` |
| Artifact studies (Peffers DSRM / Hevner) | `references/dsrm.md` |
| Proposal spine, ethics, instrument bias, writing | `references/writing-ethics.md` |
| Purpose / question scripts | `assets/purpose-and-questions.md` |
| Protocol skeleton, timeline, execution log, replication | `assets/research-protocol.md` |
| Consistency matrix | `assets/consistency-matrix.md` |
| Interview, survey, observation, document instruments | `assets/instruments.md` |
| Ship checklist | `assets/quality-checklist.md` |
