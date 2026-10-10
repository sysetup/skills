# Canonical loop artifacts

Authoritative shapes: the local `schemas/` directory. This file is the quick
map used by `evals_tool.py`, `validate_artifacts.py`, and `report.py`.

## Workspace layout

```
<skill-name>-workspace/          # sibling of the skill directory
└── iteration-N/
    └── <descriptive-eval-name>/ # named for what it tests, not "eval-0"
        ├── eval_metadata.json   # {eval_id, eval_name, prompt, assertions}
        ├── with_skill/outputs/
        ├── without_skill/outputs/   # new-skill baseline
        └── old_skill/outputs/       # improving-skill baseline (snapshot)
```

## evals/evals.json

`{skill_name, evals[]{id, prompt, expected_output, files?, expectations?}}`.
`id` is a unique integer; `prompt` is the user's task; `expectations` are
verifiable statements. Drafting prose may say "assertions"; the schema field
is `expectations`.

## grading.json

`expectations[]` items must use exactly `text`, `passed`, `evidence` — not
`name`/`met`/`details`. Artifact reporting renders these exact fields.
Programmatically checkable expectations should be checked by a script, not
eyeballed.

## timing.json

`{total_tokens, duration_ms}` captured from the task notification
immediately when each run completes; the data is not recoverable later.

## benchmark.json

Generate it with `scripts/aggregate_benchmark.py` rather than writing it by
hand.
`runs[].configuration` must be `with_skill`, `without_skill`, or `old_skill`;
the viewer uses this exact string for grouping. Put each with_skill run
before its baseline counterpart.
