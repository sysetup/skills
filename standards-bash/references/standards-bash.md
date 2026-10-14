# Bash criteria for Debian host tasks

These are the skill's default engineering criteria, subject to the precedence and authorization rules in SKILL.md. Apply each only to its stated artifact or operation; preserve compatible project conventions. They are not a newly issued host policy.

## Context and authority

| ID | Applicability | Criterion | Assessment basis |
| --- | --- | --- | --- |
| BSH-01 | Every task | Identify requested outcome, authorized target, execution context, and effects before selecting a command or changing code. | Scope statement and inspected target context. |
| BSH-02 | Privileged or production work | Distinguish authorization from runtime access; delegate root and sudo execution to the user and preserve checkpoints. | Proposed commands, their effects, and actual authorization or user-returned evidence. |
| BSH-03 | Existing implementation | Preserve behavior and applicable project conventions unless the requested correction requires a change. | Focused diff and relevant behavior checks. |
| BSH-04 | New executable | Target Bash explicitly; use `#!/bin/bash` on this Debian host unless the project specifies another verified interpreter path. | Interpreter declaration and target evidence. |
| BSH-05 | Sourced library or startup file | Do not introduce global shell options, IFS, traps, directory changes, exit, or unexpected output as incidental hardening or documentation. | Source diff and shell-state checks in a disposable subprocess. |

## Inputs, structure, and style

| ID | Applicability | Criterion | Assessment basis |
| --- | --- | --- | --- |
| BSH-06 | External arguments, environment, paths, or file data | Parse explicitly; validate types, allowed values, ranges, and combinations before side effects. Reject invalid state rather than unsafe coercion. | Boundary cases and invalid-input checks. |
| BSH-07 | Shell expansion or command construction | Quote data expansions; use arrays for argument lists and quoted `"$@"`; do not use eval or untrusted source as a parser. | Source inspection and ShellCheck. |
| BSH-08 | New functions and variables | Prefer snake_case functions and ordinary variables, UPPER_SNAKE constants and exported settings, and function-local variables. Preserve established namespaces in existing modules. | Source inspection and surrounding project style. |
| BSH-09 | New standalone script with orchestration | Use a main entrypoint when it clarifies control flow; separate validation from state changes and use a direct-execution guard when the file also supports sourcing. | Entrypoint and call-path inspection. |
| BSH-10 | Formatting | Prefer two-space indentation, LF endings, and `shfmt -i 2 -ci -bn` unless project configuration differs; keep Bash lines within 80 columns where practical without harming correctness. | Formatter diff plus manual review; shfmt does not enforce a line-length limit. |
| BSH-11 | CLI or public callable | Document actual arguments, outputs, effects, dependencies, and failure conditions in English; keep inline comments aligned with implementation. | Help, comment, and implementation comparison. |
| BSH-12 | New or changed action-taking CLI | Support -h and --help. Zero arguments show usage without changing state. For an explicitly root-only CLI, apply the established privilege gate before actions; if host policy requires root-first help gating, preserve it. | Authorized help and zero-argument tests; privilege checks tested without executing privileged actions. |
| BSH-13 | Return and exit behavior | Define meaningful, stable statuses; return from sourced functions rather than terminating the caller. Preserve existing exit-code contracts. | Failure-path tests and caller inspection. |

## Side effects and lifecycle

| ID | Applicability | Criterion | Assessment basis |
| --- | --- | --- | --- |
| BSH-14 | Repeated state changes | Detect the current state and converge safely; make repeat runs harmless within the documented scope. | Repeated-run and already-correct-state checks. |
| BSH-15 | Secrets and diagnostic output | Use protected secret references; redact sensitive values, avoid shell tracing with secrets, and keep stdout data distinct from stderr diagnostics. | Source, examples, and focused log or secret inspection. |
| BSH-16 | Temporary or replacement files | Use private temporary storage, cleanup, restrictive permissions where needed, and replacement within the target filesystem; account for symlinks, ownership, and concurrent writers. | Failure, interruption, permissions, and target-boundary checks. |
| BSH-17 | Removal, overwrite, or cleanup | Bound the operation to explicitly identified task-owned artifacts; validate canonical scope and symlink behavior and obtain authorization for destructive or production effects. | Target validation, ownership inventory, and dry-run or scoped inspection. |
| BSH-18 | Network operation | Require authorized explicit endpoints, TLS verification, finite timeouts and retry bounds; do not retry non-idempotent requests blindly. | Command configuration and relevant approved service contract. |
| BSH-19 | Dependency use | Use only dependencies needed by the selected action. If a required tool is unavailable, report it before continuing dependent work; leave that operation blocked without installation or substitution. | Reported dependency limitation and blocked/not-run operation. |
| BSH-20 | Artifact delivery | Run appropriate syntax, lint, format, and behavior checks; report failures and unavailable checks truthfully. | Executed evidence, not expected output or a template. |

## Interpretation and exceptions

The caller's interface controls whether a no-argument command is an action-taking CLI, a library function, a filter, or an existing scheduler entrypoint. Do not impose BSH-12 on every function or change an established scheduler contract silently. An explicit user-requested exception may override a style default within its scope, but not a governing security or runtime restriction. Record the exception and its validation impact; pending approval is not approval.

Use [execution contexts](execution-contexts.md) for shell semantics and [verification](verification.md) for checks. Consult the selected tool's local manual for installed-version behavior. The Google Shell Style Guide is a style reference, not evidence that strict mode, global IFS changes, or every criterion above is a Google requirement.

## Primary references

- [Local Google Shell Style Guide](upstream/google/shellguide.md): consult the relevant section for interpreter choice, function contracts, naming, arrays, or quoting. Unchanged original Markdown, commit `0acdb47ea7d3fe887af5ddd34f9a9b09a7b97566` (2026-10-14), retrieved 2026-10-14; [CC BY 3.0 license](upstream/google/LICENSE). Fallback only: [published guide](https://google.github.io/styleguide/shellguide.html) or [repository Markdown](https://github.com/google/styleguide/blob/gh-pages/shellguide.md).
- GNU Bash installed manual: startup, source, shell parameters, pipelines, traps, and the set builtin. Local `man bash` and builtin `help` control checks against the installed interpreter.
- ShellCheck: run locally for static diagnostics; it does not prove runtime correctness.
- shfmt: run locally for formatting; it does not verify behavior or line length.
- Bats: use for applicable behavior tests in isolated, authorized scope. Follow [verification](verification.md#behavior-and-regression-cases).
