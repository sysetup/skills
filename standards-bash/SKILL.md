---
name: standards-bash
description: "Apply host Bash standards to interactive commands, pipelines, scripts, sourced libraries, login configuration, automation, debugging, refactoring, code review, tests, and CI. Use whenever Bash or shell behavior affects a requested task, including .sh files and extensionless Bash entrypoints. Classify execution context and authority before choosing tools or changing code; verify behavior with targeted checks. Route document creation to doc-set and existing operational guidance to doc-get."
compatibility: "GNU Bash on Debian with GNU userland; verification tools are checked when needed and are not installed automatically."
license: MIT
---

# Bash host operations and engineering

## Mission and boundaries

Support reproducible delivery, service reliability, and system protection through the smallest correct Bash operation. Start with the host outcome, identify the affected subsystem and execution context, then select tools and implementation. Bash orchestrates existing tools; it is not a substitute for a service's native interface or a structured-data parser.

Follow the user's scope, host instructions, runtime permissions, and applicable project standards. This skill's defaults fill gaps; they do not override those sources or authorize operations. Never execute root or sudo operations yourself: provide verified commands to the user and wait for required checkpoints.

Resolve bundled references from the directory containing this file, independently of the working directory. Inspect only authorized targets. A request for analysis or a documentation edit does not authorize remediation, network access, installation, or publication.

## Select the task and references

Read [Bash criteria](references/standards-bash.md) for any Bash task. Then load only the references needed for its context:

| Decision | Read | Result |
| --- | --- | --- |
| What host need, subsystem, tool, and boundary are involved? | [Host task map](references/host-task-map.md) | A bounded operation and the simplest suitable tool. |
| Is this interactive, executed, sourced, scheduled, or CI code? Are parsing or shell state relevant? | [Execution contexts](references/execution-contexts.md) | Correct state, argument, failure, and resource handling. |
| What proves the requested behavior, and what remains untested? | [Verification](references/verification.md) | Targeted evidence and explicit limits. |

Use `doc-get` for existing approved host or workspace procedures. Documents under `doc-operations/pull-request/` remain proposals and are not operational precedents. Use `doc-set` for a requested standalone guide, runbook, reference, ADR, or other document; it selects `doc-specs`, destination, metadata, and registration. Inline comments remain part of the code contract. No documentation site or documentation toolchain is required merely because Bash is involved.

## Execute from general to specific

1. **Frame the outcome.** Identify the host mission, requested result, target subsystem, authorized paths, and operational side effects. Separate observed facts from assumptions. Do not infer production scope from a file's presence.
2. **Inspect the context.** Read target files, project instructions, applicable approved procedures, and relevant tool help or manuals. Establish invocation mode, inputs, privileges, caller expectations, and available dependencies before editing or executing.
3. **Select the mechanism.** Prefer an existing native command or shell builtin. Use Bash for bounded process and filesystem orchestration; use an existing structured-data tool for its format. If the workload requires a different language or service, explain the boundary instead of forcing a Bash solution.
4. **Define acceptance.** State expected output or state, failures, safety properties, and the narrow checks that distinguish success. For changes, identify only the affected files and preserve unrelated work.
5. **Implement or operate.** Apply the context-specific criteria. Keep input validation, computation, and side effects distinct. Reuse existing interfaces; introduce functions or modules only when they clarify a real boundary.
6. **Verify and deliver.** Run applicable checks, report actual outcomes and unavailable checks, and provide material failure or recovery instructions. Follow the host's authorized version-control workflow; stage only this task's files.

## Decide whether to proceed

| Condition | Response |
| --- | --- |
| Missing fact changes authority, destruction risk, or the requested behavior | Ask the blocking questions together; continue only independent authorized work. |
| Routine detail is inferable from inspected context | Use the established pattern and state a material assumption if needed. |
| Required tool is unavailable | Report the missing tool before continuing dependent work; leave its operation blocked/not-run without installation or substitution. Continue only independent static work after reporting. |
| Task requires root or sudo | Delegate exact commands and material effects to the user; wait for required output. |
| Runtime blocks an authorized operation | Report the boundary and use the runtime's approval mechanism; do not bypass it. |
| Check fails after editing | Stop dependent actions, preserve the failure evidence, and correct the scoped defect. Do not automatically revert unrelated or pre-existing work. |

## Deliverable contract

Provide the requested command, scoped patch, or findings with the reason for the chosen approach and verification evidence. For operational commands, state prerequisites and material effects before execution. For privileged work, group only commands that share one execution checkpoint. Distinguish static validation, isolated behavioral tests, and actual host operation; none implies production acceptance.
