# Verification of Bash tasks

## Match evidence to the contract

| Artifact or operation | Minimum relevant check | Additional checks when material |
| --- | --- | --- |
| Bash executable change | bash -n, ShellCheck, project formatter check | Help, zero arguments, invalid inputs, expected failures, effects, and repeat runs. |
| Sourced library | Syntax and static analysis; source in a disposable subprocess | Caller options, IFS, traps, directory, descriptors, output, and return behavior. |
| Startup configuration | Inspect the actual startup/include graph | Isolated login and interactive modes, repeated sourcing, PATH duplication, and latency-sensitive operations. |
| Pipeline or batch command | Inspect quoting, delimiters, and every required status | Empty input, special filenames, producer failure, partial work, and bounded concurrency. |
| Scheduled task or CI | Inspect runner and interpreter contracts | Restricted environment, working directory, timeout, overlap, exit reporting, and safe failure. |
| Filesystem operation | Validate roots, ownership, metadata, and replacement behavior | Symlinks, collisions, interruption, existing state, concurrent writers, and recovery. |
| Documentation-only edit | Compare comments against inspected behavior and review the diff | Syntax and relevant lint; verify that executable tokens and state are unchanged. |
| Privileged host operation | User-run commands and returned redacted checkpoints | Actual target-state verification after the authorized action; no agent-side sudo or root execution. |

Do not execute target code merely because a static check passes. Use trusted fixtures and disposable subprocesses for behavioral tests; check authorization before actions that touch the host, network, secrets, or production. In this editing environment, use its authorized patch mechanism and preserve the user's work.

An executable Bash proposal can still be checked statically through stdin or an authorized fixture. When the tools are available, run syntax, lint, and formatting checks before delivering generated code; lack of authorization to operate the target is not a reason to defer these non-executing checks. Preserve the original failed result and distinguish a corrected retest from the initial output.

## Tool checks

Check only tools needed for the selected validation. Use ShellCheck for static analysis, shfmt for formatting under the Bash criteria, and Bats for applicable behavior tests. Reuse project fixtures and configuration within those roles. If a required tool is unavailable, report it before continuing dependent work; leave its operation blocked/not-run without installing or substituting tools. Independently useful static work may continue after the limitation is reported.

For an inspected Bash script named script.sh, the usual non-mutating checks are:

```bash
bash -n script.sh
shellcheck script.sh
shfmt -i 2 -ci -bn -d script.sh
```

The name above is illustrative, not a bundled resource. Match the actual path and formatter configuration. A syntax pass does not prove runtime correctness; ShellCheck does not prove safe filesystem containment; shfmt does not validate behavior or enforce an 80-column maximum.

Apply format changes only through the authorized editing mechanism and within the requested scope. Suppress a lint finding narrowly with a specific reason, not to obtain a nominal clean result. Scan secrets within the task scope using the existing scanner where relevant; redact findings and distinguish heuristics from proof.

## Behavior and regression cases

Use Bats for behavior and regression cases when a behavior check is applicable. Choose tests for material properties, not implementation-shaped assertions. Cover expected use, boundary values, invalid or missing inputs, dependency absence, and the important failure or recovery path. Action-taking CLI help and zero arguments must be safe before dependency checks or state changes, except established root-first help gates.

Do not test privileged behavior by gaining privileges. Use inspection and controlled simulation of a callable privilege decision if the design supports it; actual privileged operation remains a user-run checkpoint. Document what simulation does not establish.

For sourced code, compare caller state before and after in an isolated process. For replacement or generation, test repeat runs, failure before publication, preservation of prior valid output, and output-name collisions. Test filename edge cases where the interface supports them.

## Documentation and delivery

Inline contracts state actual signatures, globals, return/exit statuses, stdout, stderr, side effects, and preconditions. Documentation-only changes do not introduce executable function bodies or hardening prologues. Standalone documents use doc-set and the selected doc-specs contract; a generated API page is still subject to its reference-document contract.

Report each relevant check as pass, fail, not-run, or inconclusive, with the command or method and material limitation. Preserve earlier failures when corrected and identify the retest. Static validation, behavioral evaluation, and user acceptance are different claims.

Before an authorized commit, inspect status and staged changes, stage only task-owned paths, and preserve unrelated modifications. Report the actual commit message and command; if Git or runtime permissions block it, provide the exact scoped commands instead of claiming success.

Recovery restores only the task's identified changes or generated artifacts after verifying ownership and authorization. Do not automatically discard the working tree on a failed check or use a broad reset as a rollback procedure.
