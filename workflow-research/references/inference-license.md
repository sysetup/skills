# Inference license by named design

Load at step 6 (before collecting) and step 8 (before writing Findings). This file is the only home for what Findings may claim.

The named design licenses a **claim type**. Collection either produces the evidence that type requires, or it does not. Search, logs, and coding cannot mint a different claim type. A desk study is still that design: the sample is the corpus the design names, not "whatever the agent can reach."

## Unrun data

If the design's authorizing collection did not happen, Findings do not answer the RQ with a substitute corpus. Ship:

- protocol, instruments, empty result tables
- pending-fieldwork list
- step-2 literature as gap / background only

The user asking for "findings now" does not waive this. If they want a synthesis of prior studies instead, change the named design in writing to a literature-review study and rewrite the questions so they ask what the literature claims, not what this study measured.

## Locked design that cannot answer the question

If the user forced a design whose license cannot support the RQ (phenomenology on a causal "does X improve Y"), do not collect as if the lock were valid. Flag the mismatch, name what that locked design *could* claim, and propose the Creswell-correct design. Do not silently answer the causal RQ under the locked label.

## License table

| Named design | Findings may claim | Authorizing collection | If that collection did not run |
| --- | --- | --- | --- |
| True experiment | Causal effect of the manipulated IV on the DV in this sample, with named internal-validity residual | This study's assignment, fidelity, measures, and analysis | Protocol + empty result tables. Prior experiments are step-2 gap evidence, not this study's causal finding. |
| Quasi-experiment | Qualified causal inference under the named quasi-design; weaker than random assignment | This study's intervention, comparison, and measures | Same as true experiment. Do not keep "mejora / effect of" as a confirmed claim. |
| Single-subject | Change in the DV for that unit under the named repeated-measures design (AB, ABA, multiple baseline) | This unit's repeated measures across phases | Protocol + empty phase tables. Not a group causal claim. |
| Survey | Prevalence, attitudes, or distributions in the reached sample; generalize only as far as the frame supports | Responses from this sample | Protocol + empty tables. Published surveys are others' estimates, cited as such. |
| Correlational / causal-comparative | Association, prediction, or group difference on a pre-existing factor in this sample. Not cause. | This study's measured variables | Protocol + empty tables. Do not upgrade association in prior papers into this study's cause. |
| Narrative | Restoried account of one or few lives, with chronology and context | That person's (or those persons') stories / documents | Protocol + interview/document plan. Public commentary about "people like them" is not their narrative. |
| Phenomenology | Essence of the lived experience (textural + structural) for participants who lived the phenomenon | First-person accounts from those participants | Protocol + interview guides. Third-person commentary is not the essence. Documents license this only if they are first-person accounts of the lived phenomenon and Limitations say so. |
| Grounded theory | Substantive theory of a process: categories, conditions, actions, consequences | Field data with theoretical sampling toward saturation | Protocol + sampling plan. Coding the open web as if it were the field does not generate that theory. |
| Ethnography | Cultural portrait of a culture-sharing group (behavior, language, belief) in situ | Prolonged engagement, observations, artifacts of **that** group | Protocol. Secondary descriptions of the culture are literature, not the ethnography. |
| Case study | Mechanism, description, and themes **inside this case boundary** | Multiple sources inside the bound (logs, code, reports, interviews, artifacts of this case) | If the case corpus is unreachable: pending-corpus list. General articles about similar cases are literature unless they are documents about **this** incident. |
| Convergent mixed | Separate strand results plus a metainference from the merge (convergence, complementarity, or resolved divergence) | Both strands actually collected and a joint display | Pending-strand cells. Do not invent the missing strand. Literature is not a silent second strand. |
| Explanatory sequential (QUAN → qual) | Quant results, then qual explanation of **those** results, then a metainference | Quant data first; qual sample connected from those results | Joint display with pending cells; connecting rule written. Do not "explain" numbers that do not exist by coding the web. |
| Exploratory sequential (QUAL → quan) | Qual constructs/items, the instrument or typology built from them, then quant tests/generalization | Qual first, then the build step, then quant | Pending build and pending quant. Do not skip the instrument-build write-up or fake item psychometrics. |
| Complex mixed | The named core's license, plus whatever the wrapper adds (an experiment wrapper adds cause only if that experiment ran) | Core collection + wrapper collection | Pending cells for whichever layer did not run. Still name the core. |
| Literature review (narrative / scoping / systematic) | What prior studies claim, how strong that evidence is, and the gap this review names | The retrieved, screened, included corpus with four-phase counts | In-progress count table. Do not fabricate inclusion. Findings report others' claims; they are not this project's experiment, survey, or phenomenology. |
| DSRM | Artifact specified or built; demonstration on an instance; evaluation against stated objectives by a named Hevner method | Build/specify + demonstration + that evaluation method | Complete design + evaluation protocol. Related-work papers are kernel theory / missing-artifact evidence (steps 1–2), not evaluation — unless the named method is informed argument and is labeled descriptive. Do not treat "we built it" as evaluation. |

## Collection rule

Before a search, a log read, or a coding pass, ask: *which cell of this table does this evidence fill?* If it fills none, it is either step-2 literature or out of scope. Put it in the gap argument or drop it. Do not let it into Findings under a borrowed verb (cause, essence, prevalence, metainference, utility).

Secondary numbers and published studies may enter Findings only when the named design is a literature-review study, or when they are context/covariates explicitly labeled as others' data. They never convert an unrun experiment into a causal result.

## Landmines

- Experimental family + no run + "findings now" → protocol and empty tables, not a web synthesis titled as the answer to "does X improve Y."
- Case study of an incident → code the case corpus. A general article about similar outages is literature, not the case.
- Phenomenology without first-person accounts from people who lived the phenomenon → protocol, not themes extracted from commentary.
- Mixed explanatory sequential without quant results → no qualitative "explanation" of numbers that do not exist.
- DSRM literature on related tools → related work, not evaluation, unless the named method is informed argument and labeled descriptive.
- Relabeling the study a literature review mid-stream solely to keep a causal RQ and still ship "findings." Change the questions if you change the design.
