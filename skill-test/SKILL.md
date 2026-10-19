---
name: skill-test
version: "2.0.0"
description: >
  Execute and certify the canonical evaluation loop for any
  generated skill: canonical preflight, evals setup, run-layout checks,
  grading/timing validation, and benchmark validation. Use whenever the user
  asks to test, audit, certify, or run evals on a SKILL.md or skill package,
  or after a skill is drafted or improved.
license: MIT
metadata:
  author: "SYSETUP.COM CarlosHRG"
---

# skill-test — canonical evaluation-loop harness

Act as the testing complement of skill creation and improvement workflows.
Never execute the target skill and never rescore by hand: run the pipeline
scripts and read the stage results.

## Tool justification

`read` inspects the target tree; `python` runs the stage scripts; `write` is
needed only for `evals_tool.py init/scaffold`, which creates the canonical
evals file and workspace. Scripts write stage results only under
`--reports-dir`; scaffolding writes only inside the skill's own
`evals/` and `<skill-name>-workspace/`.

## Canonical alignment

- Every artifact shape is defined by this skill's [schemas/](schemas/).
- The evaluation workflow spawns with-skill and baseline runs in the same
  turn, then grades, aggregates, reviews, and improves; this skill prepares,
  validates, and reports on that loop without launching the runs.
- The human-review viewer is outside this harness; report validated artifacts
  and hand off to the workflow responsible for review.
- Fail-only-on-canon: preflight FAILs only on explicit canonical
  requirements; everything else is advice. Read
  [references/canonical-contract.md](references/canonical-contract.md)
  before overriding any stage result.

## Invocation

```
SKILL_ROOT  = <directory containing this SKILL.md>
SCRIPTS_DIR = ${SKILL_ROOT}/scripts
```

Requires Python 3.10+ and PyYAML. All stage results default to `./reports`
under the process cwd (override with `--reports-dir`).

## Stage 0 — Canonical preflight

Validate one SKILL.md against the canonical contract (name/description,
bundled references, security floor). Extra frontmatter fields, body length,
and missing optional resources never fail. Exit 1 lists the FAIL reasons.

```
python3 ${SCRIPTS_DIR}/preflight.py <target-SKILL.md>
```

Security floor details: [references/security-preflight.md](references/security-preflight.md).

## Stage 1 — Evals setup

```
python3 ${SCRIPTS_DIR}/evals_tool.py init <skill-dir>
python3 ${SCRIPTS_DIR}/evals_tool.py validate <skill-dir>/evals/evals.json
python3 ${SCRIPTS_DIR}/evals_tool.py scaffold <skill-dir> --eval-id 1 \
  --name descriptive-kebab-name --iteration 1 [--baseline without|old] [--prompt TEXT]
```

`init` creates `evals/evals.json` (refuses to overwrite). `validate` checks
the canonical schema, unique ids, and `skill_name` match. `scaffold` creates
`<skill-name>-workspace/iteration-N/<eval-name>/{with_skill,<baseline>}/outputs/`
plus `eval_metadata.json`; use `--baseline old` when improving an existing
skill (baseline dir `old_skill`). Then tell the calling agent to launch all
with-skill and baseline runs in the same turn.

## Stage 2 — Run-layout check

```
python3 ${SCRIPTS_DIR}/validate_artifacts.py iteration <workspace>/iteration-N
python3 ${SCRIPTS_DIR}/validate_artifacts.py metadata <eval-dir>/eval_metadata.json
```

FAILs on missing `eval_metadata.json`, `with_skill/outputs/`, or baseline
`outputs/`; pending `grading.json` files are warnings. Remind the user that
timing data (`total_tokens`, `duration_ms`) must be captured from task
notifications immediately — it is not recoverable later.

## Stage 3 — Grading and timing validation

```
python3 ${SCRIPTS_DIR}/validate_artifacts.py grading <run-dir>/grading.json
python3 ${SCRIPTS_DIR}/validate_artifacts.py timing <run-dir>/timing.json
```

`grading.json` expectations must use exactly `text`, `passed`, `evidence`
(`name`/`met`/`details` break artifact reporting). Run one validation
per run directory as runs complete; do not wait to batch everything.

## Stage 4 — Benchmark and final report

Generate the benchmark with the local aggregator (do not hand-write it):

```
python3 ${SCRIPTS_DIR}/aggregate_benchmark.py \
  <workspace>/iteration-N --skill-name <name>
```

The aggregator writes `benchmark.json` and `benchmark.md` in the iteration
directory from the completed `grading.json` and `timing.json` artifacts.

Then validate and aggregate:

```
python3 ${SCRIPTS_DIR}/validate_artifacts.py benchmark <workspace>/iteration-N/benchmark.json
python3 ${SCRIPTS_DIR}/report.py --skill-name <name>
```

Artifact map: [references/loop-artifacts.md](references/loop-artifacts.md).
Schemas: [schemas/](schemas/). Templates: [templates/](templates/).

## Verdicts

Each stage is `PASS`, `FAIL`, or records `WARNING`/`ADVICE` findings. The
final report says `READY FOR EVAL LOOP` or `BLOCKED: <first failing stage>`.
There are no certification levels: behavioral claims exist only when real
runs recorded them; never invent pass rates.

## Chat summary

Print the overall verdict, then each stage status with its top findings and
locations, then: `Artifacts generated in <reports-dir>/ - See report.md`.
