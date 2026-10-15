# Local tool selection

Choose a mechanism from the inspected task, not from keyword classes. Candidates below are neither an installed inventory nor execution permission.

| Task | First suitable mechanism | Boundary |
| --- | --- | --- |
| Resolve shell behavior | Bash help, command, type, printf | Preserve the current shell; do not source unknown code. |
| Locate workspace files | rg; find when needed | Bound the root and preserve filename delimiters. |
| Transform line records | read -r, grep, sed, awk | Stream when practical; do not treat filenames as whitespace-separated words. |
| Read structured data | Existing format-aware parser | Keep syntax parsing out of regex and shell evaluation. |
| Orchestrate batches | Arrays, find, xargs, existing project runner | Check producers and workers; bound concurrency. |
| Generate or replace files | Existing native mechanism | Validate roots, ownership, symlinks, overwrite effects, and recovery. |
| Track processes | wait, jobs, timeout, ps | Track owned PIDs; avoid broad name-based termination. |
| Inspect services or logs | Native service CLI, systemctl, journalctl | Use named authorized targets; delegate privileged operations to the user. |
| Prepare scheduled work | Existing runner or service model | Establish interpreter, environment, working directory, timeout, and overlap policy. |
| Inspect startup configuration | Bash manual and inspected include graph | Distinguish login and interactive modes; preserve caller state. |
| Verify code | Existing project checks and applicable installed checkers | Consult applicable standards through doc-get; select checks by the changed artifact. |
| Inspect command syntax | --help, installed manuals via ops-man | Verify the installed version; missing manual text is an evidence gap. |
| Deliver changes | git and existing delivery interface | Stage only task changes; remote publication needs its own authority. |

A builtin or native command is preferable to a wrapper that adds no useful behavior. Avoid rereading large inputs, a subprocess per record, and unbounded background jobs. Select a different existing mechanism when transactional replacement, complex parsing, or durable service state would make shell orchestration fragile. No performance improvement is claimed without measurement.

Use doc-get for applicable approved operational sources and doc-set for requested standalone document authoring. Their source selection and authoring contracts remain independent of tool execution.
