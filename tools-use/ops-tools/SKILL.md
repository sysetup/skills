---
name: ops-tools
description: >-
  Select, check, and use local commands and project utilities for a concrete
  task. Use when a task needs host command selection, workspace inspection, process or
  filesystem orchestration, and local verification. Check only the tools
  needed by the task; consult applicable operational documents through doc-get.
  Do not use for answers that need no tools or for remote connector management.
compatibility: GNU Bash 4.3+ on Debian with GNU userland; selected commands must already be available.
license: MIT
metadata:
  version: "2.0.0"
---

# Local task tools

Start from the requested outcome, authorized targets, and required evidence. Availability proves that a command can be found, not that its execution is authorized. Resolve bundled paths from the directory containing this file.

1. Inspect the relevant workspace sources and identify the smallest suitable command or existing project entrypoint.
2. Use `doc-get` to locate applicable approved host or workspace standards and procedures. Report a missing document; a proposal in `doc-operations/pull-request/` is not an operational source. Do not establish language standards inside this skill.
3. Check only the selected tools: `command -v NAME` distinguishes normal shell resolution; `type -P NAME` checks an external executable. Use a Bash builtin directly when it satisfies the task.
4. Verify unfamiliar or version-sensitive options with installed help or manuals. For local manual text, read the sibling [ops-man](../ops-man/SKILL.md) and invoke its lookup script. Tool selection does not require a subagent.
5. Execute the authorized operation and the smallest relevant verification. Report actual results, missing dependencies, and unresolved checks. Leave work requiring a missing tool unrun; do not install or substitute it silently.

Read [tool selection](references/tool-selection.md) when choosing among mechanisms, [safety](references/safety.md) when effects, sensitive inputs, or authority need resolution, and [diagnostic contracts](references/output-contract.md) only when using the optional scripts.

## Optional diagnostics

Package checking and broad inventory are maintenance actions, not prerequisites for a task:

- `bash scripts/load-skill.sh ops-tools` checks bundled files, package identity, and script syntax without executing the scripts. It is a shallow consistency check, not a complete YAML validator or behavioral evaluation.
- `bash scripts/discover-host-tools.sh git rg` probes only named external commands without executing them.
- `bash scripts/discover-host-tools.sh --all` probes the bundled catalog only when a broad inventory is requested. A custom catalog uses `--catalog FILE`.

Both scripts are read-only, require only Bash, print to stdout, and use statuses `0` success, `1` runtime/package error, `2` usage error. Help and zero arguments do not inspect targets. Diagnostic output can contain local executable paths; keep it inside the authorized session.

## Compatibility

Edition 2 removes task-text classification and generated recommendation artifacts. The inventory interface now accepts explicit command names or a catalog and emits text to stdout; file-output and format options from edition 1 are retired. Use the documented interface instead of old automation. No configuration discovery or framework-documentation integration belongs to this package.
