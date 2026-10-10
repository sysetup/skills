# Optional local automation

Use Python 3.11+ and this package's requirements.txt. Run from a separate working directory so inputs and generated outputs do not alter the skill's exact manifest. Set TOOLKIT to the absolute path of this skill's scripts/toolkit.py before running the examples. No sibling skill, mutable shared runtime or network is needed.

```sh
TOOLKIT=/absolute/path/to/this-skill/scripts/toolkit.py
```

```sh
python -B "$TOOLKIT" scaffold agent --harness generic --objective "Complete the stated objective" --id example-task > spec.json
python -B "$TOOLKIT" validate spec.json
python -B "$TOOLKIT" render spec.json --out staged-result
python -B "$TOOLKIT" validate spec.json --native-root staged-result/native
python -B "$TOOLKIT" check-contract InstructionSpec spec.json
python -B "$TOOLKIT" migrate legacy.yaml --harness generic
```

Only `agent` is accepted, including saved specs, native validation and legacy migration. Unsupported legacy source formats are refused. No routing or sibling-surface generation is exposed. Local validation is for this skill's own work, not generic auditing.

Inspect help for exact options. An optional `--binding binding.json` selects native representation, artifact name, allowed native metadata and input values. `validate --native-root staged-result/native` checks saved native text against its specification; it never executes the native body. `--behavioral-evidence` attaches independently produced evidence but never runs a model or promotes native execution.

Input contracts accept strict JSON or YAML; some emitted native commands use TOML. Render writes a new staging directory only and refuses overwrite. It does not install into a live host. Return codes: 0 for successful configured checks (inspect inconclusive/not-run states), 1 for validation findings, 2 for invalid input, ownership refusal or filesystem errors.

`--resources` can only name this package's own references directory. It cannot substitute another package's adapter/schema registry or widen ownership. Generated snapshots are not authorable source: change canonical repository inputs and rebuild.
