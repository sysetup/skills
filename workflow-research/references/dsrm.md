# Design Science Research (on-demand track)

Load this file when the problem is to **design, build, or evaluate an engineering artifact**, not when the problem is to measure, interpret, or mix behavioral evidence. Do not stretch quantitative, qualitative, or mixed methods to cover artifact creation.

Pinned sources: Peffers, Tuunanen, Rothenberger, and Chatterjee, *A Design Science Research Methodology for Information Systems Research*, JMIS 24(3), 2007; Hevner, March, Park, and Ram, *Design Science in Information Systems Research*, MIS Quarterly 28(1), 2004. Artifact types follow March and Smith (1995) as used by Hevner.

## When this track is the design

Use DSRM when the contribution is a **construct, model, method, instantiation**, or an architecture/algorithm/tool that instantiates one of those. Typical asks: "design a protocol/architecture/algorithm," "build then evaluate a tool," "propose a method and show it works."

Stay on Creswell when the contribution is explanation, prevalence, lived meaning, or integrated behavioral inference with no artifact to evaluate.

A DSRM study may **embed** a Creswell strand as the evaluation method (e.g. a survey of utility, a case study of use). Name that strand. Do not relabel the whole study mixed methods unless two analytic strands are integrated on purpose.

## Operating overlay (Peffers DSRM)

Map these six activities onto the Creswell eight-step loop in `SKILL.md`. Iterate when evaluation fails the objectives. State the entry point. Gate 0 still applies if slots are empty.

1. **Problem identification and motivation** — name the problem, who is blocked, and why a solution has value. Use literature to show existing artifacts fail or are missing. Name kernel theories that constrain the design; do not treat them as tested behavioral hypotheses unless an evaluation strand tests them. Skill steps 1–2.
2. **Objectives of a solution** — infer measurable or testable objectives from the problem. Quantitative ("reduce X by…") or qualitative ("support a class of interaction that does not exist"). Skill steps 3–4 (purpose + design/evaluation questions).
3. **Design and development** — specify artifact type, functions, architecture; then build. Skill steps 5–6.
4. **Demonstration** — use the artifact on one or more problem instances. Proof of use, not yet a full evaluation. Skill step 6.
5. **Evaluation** — observe and measure how well the artifact meets the objectives from step 2. Name the method (below). Skill step 7 (validation of the artifact against objectives).
6. **Communication** — report problem, artifact, utility, rigor, and limits to the audience. Skill step 8.

Entry points (Peffers): problem-centered (start at 1), objective-centered (start at 2), design- and development-centered (start at 3 with an existing artifact), client/context-initiated (start at 4). Do not skip evaluation.

## Purpose script

The purpose of this design science study is to **{design / develop / instantiate / evaluate}** a **{construct / model / method / instantiation}** that **{objective}** for **{context / users}**, in order to **{problem need}**.

Questions (keep all three classes)

- Design — What artifact, with which functions and structure, addresses {problem}?
- Demonstration — Does the artifact operate on {instance}?
- Evaluation — To what extent does the artifact meet {objectives}, by {named evaluation method}?

Do not write causal-behavioral hypotheses unless a Creswell evaluation strand actually tests them.

## Artifact types (name one primary)

- **Construct** — vocabulary and conceptualizations.
- **Model** — representations of relationships among constructs (architectures, metamodels).
- **Method** — algorithms, practices, processes.
- **Instantiation** — a working system, prototype, or implemented tool.

A design theory (Gregor and Hevner) is an optional additional contribution, not a substitute for the artifact.

## Evaluation (Hevner methods — pick one primary)

Match method to what the agent can actually run. Name residual evaluation the user must still perform.

| Class | Methods | Use when |
| --- | --- | --- |
| Observational | Case study, field study | Artifact used in a real setting the study can access |
| Analytical | Static, architecture, optimization, dynamic analysis | Structure, fit, or bounds can be shown without users |
| Experimental | Controlled experiment, simulation | Conditions can be manipulated or data generated transparently |
| Testing | Functional (black box), structural (white box) | Instantiation exists and can be executed |
| Descriptive | Informed argument, scenarios | Knowledge base or constructed scenarios are the only available evidence; weakest; say so |

Criteria typically include functionality, completeness, consistency, accuracy, performance, reliability, usability, and fit. Select the subset the objectives require. Do not invent runtime metrics, user counts, or field outcomes.

## Hevner guidelines as gates

Fail closed if any of these is missing.

1. A named, viable artifact (not only an opinion).
2. A relevant problem (who is blocked, why it matters).
3. Evaluation of utility, quality, or efficacy by a named method.
4. A stated contribution (artifact, foundations, and/or methodology).
5. Rigorous construction and evaluation procedures a second researcher could audit.
6. Design treated as a search (alternatives considered, constraints named).
7. Communication fit for the audience (technical and, if required, managerial).

## Agent execution

Claim license: `references/inference-license.md`. Related-work papers motivate the problem; they are not evaluation unless the named Hevner method is informed argument and is labeled descriptive.

- Build or specify the artifact in the workspace when that is the job. Demonstration may be tests, a walkthrough, or a worked instance.
- If the artifact cannot be built here, deliver a complete design plus an evaluation protocol. Do not fake screenshots, benchmarks, or deployments.
- Desk DSRM is allowed: informed argument and architectural analysis against retrieved sources, plus any executable checks on local code. Label descriptive evaluation as descriptive.
- Record design alternatives that were rejected and why (search process).
- Keep the execution log and, when code or corpora exist, the replication package.

## Anti-patterns

- Shipping a design with no evaluation and calling it research.
- Treating "we built it" as demonstration and evaluation combined.
- Relabeling a literature review as DSRM.
- Using DSRM to avoid validity threats that a Creswell evaluation strand would have to face.
