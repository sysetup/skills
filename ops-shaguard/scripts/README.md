# Bundled shaguard script

This directory belongs to `ops-shaguard`. Keep it with `SKILL.md`, including when copying or packaging the skill. There is no installation step, PATH entry, service, or system configuration.

Resolve `SHAGUARD_SCRIPT` using [SKILL.md](../SKILL.md), then invoke it through Bash. The program label `shaguard` in built-in help refers to this script. Dependencies are listed in the skill's compatibility field. The script checks them at runtime and requires neither root nor network access.

Read [command semantics](../references/command-semantics.md) for options, exit codes, path handling, overwrite behavior, and assurance limits. The implementation in `bin/shaguard` is the authoritative executable source.
