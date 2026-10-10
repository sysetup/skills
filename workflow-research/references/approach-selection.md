# Approach selection

Creswell research approach = worldview × design × methods. All three must be named. Select after Gate 0 slots are filled. Start from the research problem and questions, not from a favorite method.

## Worldviews (Creswell four)

Pick the worldview that actually governs the study.

**Postpositivist**
- Core claims: a reality exists out there but is known only imperfectly; determination, reductionism, empirical observation and measurement, theory verification or falsification.
- Shapes the study: operational variables, hypotheses, controls, reliability and validity of measures, causal language only with a counterfactual.
- Default for quantitative. Write: worldview name, core claims, how it shaped methods, researcher/sponsor stance.

**Constructivist**
- Core claims: multiple meanings; knowledge is socially and historically constructed; the researcher generates or inducts patterns; theory generate rather than theory test.
- Shapes the study: open questions, purposeful samples, interviews/observations, themes or theory as product, reflexivity.
- Default for qualitative meaning studies.

**Transformative**
- Core claims: research is not neutral; power, justice, and marginalized voices; inquiry is tied to an agenda for change; participants are collaborators when feasible.
- Shapes the study: problem framed as inequity or rights; questions about voice, access, and harm; reciprocal benefit; extra ethics.
- Use when the problem is oppression, inequity, or rights — qualitative, mixed, or (rarely) quantitative.

**Pragmatic**
- Core claims: not committed to one ontology; "what works" for the question; plural methods; research in real-world practice; consequences of action matter.
- Shapes the study: named reason to mix (or to build an artifact); integration point; practical significance alongside statistical or thematic findings.
- Default for mixed methods and for DSRM.

Academic audiences get the four-line write. Operational audiences keep the name plus one because-clause.

## Three approaches — differences (Creswell)

| Dimension | Qualitative | Quantitative | Mixed methods |
| --- | --- | --- | --- |
| Typical worldview | Constructivist or transformative | Postpositivist | Pragmatic (or transformative) |
| Aim | Understand meaning, process, context | Measure, compare, predict, test | Combine strands so integration answers what one strand cannot |
| Role of literature | Orients; stays light enough that field meanings can lead | Major; justifies variables and hypotheses up front | Both, plus a mixing rationale |
| Role of theory | Lens, sensitizing concepts, or end-product (grounded theory) | Tested or specified as a variable model | Governs one or both strands; state which |
| Purpose verbs | explore, understand, describe, generate | test, measure, compare, examine the relationship | overall intent + strand intents + integration intent |
| Questions | Open, evolving; no yes/no; no H0/H1 | Specific; descriptive / comparative / relational; hypotheses when testing | Quant Q + qual Q + integration Q |
| Design catalog | Narrative, phenomenology, grounded theory, ethnography, case study | Experimental family or nonexperimental family (survey, correlational) | Convergent; explanatory sequential; exploratory sequential |
| Sample | Small N, purposeful | Large N when estimating a population; power or precision for tests | Both; connecting or nesting rules for sequential designs |
| Data | Interviews, observations, documents, audiovisuals | Instruments, closed items, structured observations, secondary numbers | Both, plus an integration artifact |
| Analysis | Coding, themes, description, theory building | Descriptive and inferential stats, effect sizes, model fit | Separate analyses + joint display + metainference |
| Validation | Credibility, transferability, dependability, confirmability | Internal, external, construct, statistical-conclusion validity | Each strand plus integration validity |
| Writing | Flexible, evidence-near excerpts | Structured, tables, estimates, limits of inference | Combined spine; integration section is mandatory |
| Researcher role | Instrument; reflexivity required | Standardize and control; disclose conflicts | Both roles, sequenced or concurrent |

Do not mix rows. A study that "has some interviews and a survey" is mixed methods only if there is a named design, a reason to mix, an integration procedure, and a metainference.

## Quantitative designs — two families

### Experimental family

Use when the question is causal ("improve", "effect of", "impact", "cause"). Need manipulation of an independent variable, a comparison, and a validity-threat plan.

- **True experiment** — random assignment to conditions. Named variants: posttest-only control group; pretest–posttest control group; Solomon four-group; factorial.
- **Quasi-experiment** — intervention without full randomization. Named variants: nonequivalent control group; interrupted time series; regression discontinuity.
- **Single-subject** — only when the unit is one or a few cases with repeated measures and a design name (AB, ABA, multiple baseline).

If randomization is not feasible, name quasi-experiment and weaken causal verbs. Do not keep "mejora / effect of" as a confirmed claim under a survey design.

### Nonexperimental family

Use when there is no manipulation.

- **Survey** — attitudes, traits, practices in a population at a point (cross-sectional) or over time (longitudinal). Need a defined population and a sampling frame or a justified convenience frame.
- **Correlational** — relationships without manipulation, including prediction and causal-comparative (group differences on a pre-existing characteristic). Do not write causal verbs.

## Qualitative designs (Creswell and Poth five)

Pick one primary. Do not stack.

| Design | Unit | End product | Use when |
| --- | --- | --- | --- |
| Narrative | One or few lives | Restoried account with chronology and context | Lived stories across time |
| Phenomenology | Shared lived experience | Textural + structural description of the essence | "What is it like to live through X" |
| Grounded theory | Process or action | Substantive theory with categories and relations | Generate or refine a theory of a process |
| Ethnography | Culture-sharing group | Cultural portrait (behavior, language, belief) | Shared culture in situ |
| Case study | Bounded system (or multiple cases) | In-depth case description and themes | A bounded case that must be understood in context |

## Mixed methods designs (Creswell three core)

- **Convergent** — quant + qual in the same window; analyze separately; merge; resolve divergence.
- **Explanatory sequential (QUAN → qual)** — quantify first; sample the qual phase from the quant results; qual explains the numbers.
- **Exploratory sequential (QUAL → quan)** — qual first; build an instrument or typology; quant tests or generalizes.

**Complex** — wrap a core design inside an experiment, participatory/transformative project, evaluation, or case/longitudinal frame. Still name the core.

Mixed methods is valid only with an integration reason (triangulation, complementarity, development, expansion, or social-justice intervention) and a planned integration point.

## Selection criteria (Creswell order)

1. Research problem and questions.
2. Personal or team training, access, and time.
3. Audience expectations (discipline, committee, journal, client).

If 1 conflicts with 2 or 3, change resources or change the question. Do not keep a question the design cannot answer.

## Decision tree

```
Slots 1–6 filled? If no → SKILL.md Gate 0. Stop.

Contribution is a construct / model / method / instantiation to build and evaluate?
  Yes → DSRM (references/dsrm.md). Worldview typically pragmatic.
  No  → continue.

What must the answer do?
  Measure, compare, predict, or test a hypothesized effect
    → Quantitative. Worldview postpositivist unless the user locked transformative.
      Is an intervention manipulated?
        Yes, and random assignment is feasible → true experiment. Name the variant.
        Yes, randomization not feasible → quasi-experiment. Name the variant.
        No → nonexperimental: survey (prevalence/attitudes) and/or correlational (relationships).
  Explain a bounded incident, failure, success, or system from artifacts (logs, code, reports, one site)
    → Qualitative **case study**. The case is the incident or system. Not phenomenology unless the question is lived experience. Not an experiment unless an intervention is manipulated.
  Understand meaning, lived experience, process, culture, or a bounded case
    → Qualitative.
      Lived stories of one or a few → narrative.
      Essence of a shared lived experience → phenomenology.
      Theory of a process from the field → grounded theory.
      Culture-sharing group in situ → ethnography.
      Bounded case (or few cases) in depth → case study.
      Oppression / rights / voice as the problem → keep the design; set worldview transformative.
  Need both magnitude (or test) AND meaning (or explanation), and integration adds a named function
    → Mixed. Worldview pragmatic (transformative if mixing serves justice).
      Parallel then merge → convergent.
      First measure, then explain why → explanatory sequential.
      First explore / build items, then measure → exploratory sequential.
```

## Prompt illustrations of the tree

These illustrate the tree above. They are not a second Gate 0. Slot filling stays in `SKILL.md`. What Findings may then claim is `references/inference-license.md`.

- "Does X improve / cause / affect Y in population Z" → quantitative experimental family (true if randomization is feasible; quasi if not). Hypotheses required.
- "Lived experience / what it is like / meaning of {phenomenon} for {people}" → qualitative phenomenology.
- "First measure, then explain why" → mixed explanatory sequential (QUAN → qual).
- "First explore, then measure / build an instrument" → mixed exploratory sequential.
- "Investiga por qué falló / why did this error happen / look into this incident" → qualitative case study of the bounded incident. Not phenomenology unless the question is lived experience.
- "Investiga el éxito de X / what made X succeed" → case study, or mixed if magnitude and mechanism are both required.
- "Estado del arte / systematic review / lit review for a thesis on X" → literature-review study (narrative, scoping, or systematic). Not mixed methods unless two analytic strands will actually be integrated.
- "Design / build / evaluate an artifact" → DSRM (`references/dsrm.md`), not a stretch of the three approaches.

Topic-noun-only prompts never reach this tree; they stop at Gate 0.

## Methods layer

Methods = data collection + analysis + interpretation + validation. Procedures live in the track files. This table is the contract those files must satisfy.

| Layer | Quantitative | Qualitative | Mixed |
| --- | --- | --- | --- |
| Data | Instruments, closed items, observations with protocol, secondary datasets | Interviews, observations, documents, audiovisuals | Both, plus an integration artifact |
| Analysis | Descriptive and inferential stats, effect sizes, model fit | Coding, themes, description, theory building | Separate analyses + joint display + metainference |
| Validation | Internal, external, construct, statistical-conclusion | Credibility, transferability, dependability, confirmability | Validity of each strand plus integration validity |

## Design science routing

If the problem is to design, build, or evaluate an engineering artifact, stop using this catalog as the primary design. Load `references/dsrm.md`. A DSRM evaluation strand may still pick a row from this file. Name that as evaluation, not as the study's primary approach.
