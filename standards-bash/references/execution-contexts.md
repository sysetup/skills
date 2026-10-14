# Bash execution contexts and failure semantics

## Choose the caller model first

| Context | Interface | Preserve or establish |
| --- | --- | --- |
| Interactive command or pipeline | Current shell and user-visible output | Existing options, working directory, jobs, descriptors, and sensitive environment. |
| Login or interactive startup module | Bash's actual startup sequence | Repeated sourcing, startup latency, silent non-interactive loading, PATH uniqueness, and caller shell state. |
| Sourced library | Function return values and documented globals | No top-level actions, exit, unscoped traps, global option changes, or automatic main execution. |
| Standalone CLI | Arguments, stdout, stderr, and exit status | Help, safe zero arguments, explicit validation before action, cleanup, and bounded work. |
| Cron, systemd, or CI entrypoint | Runner configuration and declared task contract | Explicit interpreter, environment, working directory, timeout, concurrency, and reporting. |

For Bash startup, verify login and interactive conditions separately against the installed Bash manual and inspected configuration. Do not assume .bashrc runs for every invocation or that all startup files are interchangeable. Trace actual include order and guard conditions before changing a module.

## Strict mode is context-specific

In a new standalone script, set -Eeuo pipefail can be a useful baseline after expected nonzero statuses are handled explicitly. It is not a correctness proof. Do not add it globally to sourced libraries or startup files, and do not change IFS globally to compensate for unsafe parsing.

Errexit is conditional: tests, conditionals, boolean lists, pipelines, and function invocation context affect whether a failure terminates execution. Check critical commands explicitly. Treat grep no-match and other expected nonzero statuses according to the contract rather than swallowing all failures.

With pipefail, an early-closing consumer can make a producer report SIGPIPE; distinguish intended early termination from a failed pipeline. A failure inside process substitution is not automatically the enclosing command's failure. For a required producer, capture and check its status or use a checked intermediate artifact instead of assuming mapfile or a loop proved successful enumeration.

ERR traps inherit context-sensitive rules and do not replace explicit error checks. Reserve EXIT cleanup for an executable that owns the process; library cleanup should release only resources acquired by its callable operation.

## Preserve data boundaries

Use read -r and a locally scoped IFS for the actual record grammar. File names need NUL-delimited discovery when enumerated; arrays preserve argument boundaries but do not repair an incorrectly parsed input. Do not parse filenames by whitespace or infer safe paths from a string prefix.

getopts handles short options; support long options with a deliberate parser such as case when required. Validate missing values, repeated options, operands, numeric ranges, and unknown flags before modifying state. A value beginning with a hyphen remains data; use a command's supported end-of-options marker where applicable.

Split declarations and fallible assignments when exit status matters: local or readonly can hide a command substitution's status. Avoid pipelines whose last successful command conceals an earlier failure. Ordinary command substitution also strips trailing newlines; do not use it to preserve arbitrary byte streams.

## Source and executable contracts

A sourced file should expose functions or intended definitions without executing a CLI. Use return for callable failure, and document required globals, files, descriptors, and side effects. Do not export internal state unnecessarily.

An executable may use main and a BASH_SOURCE guard when the same file intentionally supports sourcing. A library does not need an otherwise meaningless main. Document functions in the project's comment format; shdoc annotations are selected only when extraction is required, not imposed on every script.

For an explicitly root-only executable, check the required effective identity inside the program before state changes. Preserve established root-first help gating where required by host policy. Do not infer execution permission from that check; the agent still delegates privileged execution to the user.

## Filesystem and process boundaries

Resolve the intended project or operation root, not an arbitrary working directory. Relative and absolute paths can both be legitimate inputs; validate the resolved target against the authorized scope. Reject unexpected symlinks or validate their resolved destinations. Lexical prefix checks do not establish containment.

Create temporary files in private storage and in the destination filesystem when atomic replacement matters. An atomic rename does not imply crash durability, correct ownership, or absence of symlink races. Preserve required permissions and metadata and use locking when simultaneous writers are possible. Where required durability or race resistance cannot be met by a small Bash implementation, use a suitable established native mechanism.

Before overwriting generated files, distinguish task-owned outputs from authored documents. Map source names to outputs without collisions, propagate enumeration and generation errors, and publish completed results without exposing partial writes. Cleanup needs an explicit ownership inventory; a broad extension glob does not establish ownership.

For asynchronous work, record each owned PID and wait for each result; bound concurrency and interruption handling. A lock or timeout is useful only when its exact failure and release behavior fits the job contract. Verify those behaviors with the installed utility's documentation.
