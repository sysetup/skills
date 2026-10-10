# Bundled shaguard script

This directory belongs to `ops-shaguard`. Keep it with `SKILL.md`, including
when copying or packaging the skill.
There is no installation step, PATH entry, service, or system configuration.

Resolve `SHAGUARD_SCRIPT` using [SKILL.md](../SKILL.md), then invoke it through
Bash. The program label `shaguard` in built-in help refers to this script.
Dependencies are listed in the skill's compatibility field. The script checks
them at runtime and requires neither root nor network access.

Read [command semantics](../references/command-semantics.md) for options,
exit codes, path handling, overwrite behavior, and assurance limits. The
implementation in `bin/shaguard` is the authoritative executable source.

## Local verification

Run from the skill root. Keep temporary test data inside the workspace:

```bash
bash -n scripts/bin/shaguard
bash -n scripts/tests/test_shaguard.sh
TMPDIR="$PWD" bash scripts/tests/test_shaguard.sh
shellcheck scripts/bin/shaguard scripts/tests/test_shaguard.sh
shfmt -i 2 -ci -bn -d scripts/bin/shaguard scripts/tests/test_shaguard.sh
```

The behavioral suite creates a unique temporary tree and removes only its
own fixtures. It resolves the script relative to the test file, so the suite
can also be invoked by absolute path from another working directory. Report
unavailable checks as not executed; do not infer success from the
[historical validation record](docs/VALIDATION.md).
