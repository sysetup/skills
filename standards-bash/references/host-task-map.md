# Host Bash task map

## Start at the host boundary

The wider system is a Debian host operated for reproducible delivery, reliable services, and system protection. The system of interest is the authorized Bash task, not the entire host. Select the affected resource, lifecycle activity, and execution context before descending to commands.

| Layer | Question | Decision |
| --- | --- | --- |
| Mission | What user outcome improves delivery, reliability, or protection? | Define observable success without assuming a production target. |
| Host subsystem | Is the target a shell session, filesystem, process, service, configuration, repository, or external endpoint? | Identify resource owners and boundaries. |
| Execution context | Interactive, login, sourced library, standalone CLI, scheduled task, or CI? | Load the applicable execution-context guidance. |
| Mechanism | Is a builtin, native utility, service interface, or existing script sufficient? | Choose the smallest correct tool chain. |
| Assurance | What can be inspected or tested safely? | Select checks and separate expected from actual effects. |
| Documentation | Is the requested artifact inline code documentation or a standalone document? | Inline contracts stay with code; standalone authoring and registration use doc-set. |

## Task and tool selection

Tools below are candidates, not an installed inventory or permission grant. Inspect local help or manuals for version-sensitive behavior. If a required tool is unavailable, report it before continuing dependent work; leave that operation blocked without installation or substitution.

| User task | First suitable tools | When and how | Where and boundary |
| --- | --- | --- | --- |
| Inspect shell behavior | Bash help, command, type, printf | Resolve builtin versus executable behavior and inspect argument expansion. | Authorized shell session; avoid sourcing unknown code. |
| Inspect or locate project files | rg when present; find otherwise | Bound the search root and preserve filename delimiters. | Authorized workspace; exclude unrelated paths and secrets. |
| Transform line-oriented text | read -r, printf, grep, sed, awk | Select by operation; stream once when practical instead of starting a process per record. | Inspected text inputs; distinguish records from shell words. |
| Parse JSON, YAML, CSV, or binary data | Existing format-aware parser | Keep Bash as orchestration; do not approximate structured syntax with regex. | Exact input format and verified parser; ask before adding dependencies. |
| Combine commands or handle batches | Bash arrays, pipelines, find, xargs | Preserve argument boundaries; use NUL delimiters for filenames and bound parallelism. | Authorized input inventory; propagate producer and worker failures. |
| Manage files or generate artifacts | mktemp, install, mv, cp, tar; rsync if appropriate | Validate source and destination, temporary ownership, overwrite effects, and recovery. | Explicit writable roots; destructive changes and privileged locations need authorization. |
| Manage jobs or subprocesses | jobs, wait, kill, timeout, ps, pgrep | Track owned PIDs, expected statuses, time bounds, and interruption cleanup. | Task-owned processes; do not kill processes by broad name matching. |
| Diagnose services or logs | systemctl, journalctl, native service CLI | Read bounded state first; determine service versus user scope and approved procedure. | Named authorized service; delegate privileged changes to the user. |
| Prepare scheduled automation | Existing cron or systemd model and Bash | Specify interpreter, working directory, environment, lock, runtime limit, and result reporting. | Approved job configuration; do not install or activate it incidentally. |
| Adjust login or interactive configuration | Bash startup-file rules and existing modules | Distinguish login/non-login and interactive/non-interactive loading; preserve shell state and repeated sourcing. | Explicit account and approved files; do not scan or alter other accounts. |
| Prepare packages or deployments | Existing package manager or project delivery interface | Inspect state and manifests; reuse approved idempotent deployment and rollback procedures. | Authorized target; package installation and production rollout are separate decisions. |
| Perform an authorized network request | Existing service client; curl when suitable | Specify endpoint, verification, finite timeouts, response validation, and safe retry semantics. | Approved destination only; public-documentation lookup permission does not authorize operational requests. |
| Manage source changes or CI | git, project runner, make when already used | Stage scoped changes; preserve unrelated work and existing pipeline entrypoints. | Target repository; pushing, publishing, and remote operations require their own authorization. |
| Verify Bash code | bash -n for syntax, ShellCheck for static analysis, shfmt for formatting, Bats for behavior | Run only checks applicable to the changed artifact and its context. | Disposable test scope; report missing required tools before continuing dependent work. |
| Produce documentation | doc-get, doc-set; optional selected generator | Resolve approved guidance, select an authoring specification, and register the document as required. | Host or workspace document hierarchy; staging proposals are not approved operating instructions. |

## Cost and complexity

A single builtin or native command is preferable to a wrapper that adds no behavior. A cohesive Bash script fits bounded filesystem and process orchestration. Persistent state, complex structured transformations, transactional requirements, or large computation can justify a different existing tool or language.

Optimize the dominant work: avoid rereading large inputs, repeated expensive subprocesses, unbounded jobs, and unnecessary network calls. Do not replace a mature streaming utility with a complicated Bash loop merely to remove fork/exec overhead. Benchmark only when a performance claim matters.

## Escalation and evidence

Inspect before changing state. A command being installed or executable proves neither authorization nor suitability. Read-only service inspection still needs an authorized target and may expose sensitive logs. Delegate every root or sudo operation to the user, including privileged diagnostic commands. If required context is outside the authorized boundary, request narrowly scoped access and continue only independent safe work.
