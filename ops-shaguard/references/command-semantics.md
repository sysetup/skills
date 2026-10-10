# Bundled shaguard 1.0.0 command semantics

Resolve the bundled script as described in [SKILL.md](../SKILL.md).
Every subcommand below is an argument to `bash "$SHAGUARD_SCRIPT"`;
`shaguard` in its built-in help is a program label, not a PATH lookup.
The bundled implementation is authoritative if this reference differs.

## Subcommand rules

### `hash FILE...`

Use for one or more existing paths that resolve to regular files. On success, output is a GNU-style SHA-256 record per operand, with line-safe escaping for backslashes/newlines/carriage returns.

Important 1.0.0 behavior:

- The algorithm is fixed to SHA-256.
- A path exactly equal to `-` is treated as the real file named `-` in the current directory when that file exists; it is emitted as `./-`. Use `stdin` for standard input.
- The regular-file test follows a symlink operand. Therefore `hash symlink-to-file` hashes the target bytes. Do not claim that `hash` rejects symlinks. If the objective requires a non-symlink operand, inspect that precondition separately and abstain if it is not satisfied.
- A later failure can occur after earlier records have already been printed; require exit 0 before accepting the set as complete.
- Do not assume arbitrary `hash` output is ready for `verify`: an absolute operand produces an absolute record path, which `verify` rejects.

### `stdin`

Use only for bytes supplied on standard input. It accepts no arguments and hashes the byte stream, not a filesystem path.

In a pipeline, preserve the upstream producer's status as well as `shaguard`'s status; `shaguard` can verify only the bytes it actually receives and cannot prove that the producer completed successfully. Do not feed `stdin` output to `verify` expecting stream semantics: `verify` interprets the record path `-` as a real file named `-`.

### `compare EXPECTED_SHA256 FILE`

Use when the caller has a reference digest that is already trusted for the intended purpose. The expected digest must be exactly 64 hexadecimal characters; uppercase is accepted and normalized internally.

Interpret:

- exit 0: the file bytes read match the supplied digest;
- exit 4: the bytes differ from the supplied digest;
- exit 5: the file could not be treated/read as the required regular-file operand.

Do not infer malware, publisher identity, or provenance from any of these results. As with `hash`, a symlink operand resolving to a regular file is followed in 1.0.0.

### `manifest [-f] [-n] [-o FILE] [-x GLOB]... ROOT`

Use to enumerate selected regular files beneath `ROOT` and create SHA-256 records for them.

Apply these verified semantics:

- Default output is `ROOT/SHA256SUMS` after resolving `ROOT` physically.
- `-o FILE` changes the output. A relative `FILE` is resolved relative to the caller's current working directory, **not** relative to `ROOT`; use an explicit path when location matters.
- `-x GLOB` is repeatable and matches the whole relative-path string without the leading `./` using Bash `[[ ... == pattern ]]` matching. Quote the glob in the invoking shell; `*` can span `/` in this matching context.
- `-f` permits replacement when the output already exists at the tool's pre-write check.
- Without `-f`, a pre-existing output is rejected with exit 2. Do not bypass this guard.
- `-n` performs a dry run: it enumerates and prints selected relative paths using shell-safe rendering, performs no hashing, and installs no manifest. It still checks the SHA-256 backend and manifest dependencies and creates/removes a temporary file-list internally.
- In actual generation, the resolved output manifest is automatically skipped when it lies inside `ROOT`.
- 1.0.0 dry-run does **not** apply that automatic self-exclusion to an already-existing output file; do not treat the dry-run list as byte-for-byte predictive in that case.
- Enumeration is `find . -xdev -type f -print0`; it stays on one filesystem, selects regular files only, and does not follow symlinks.
- With `sort -z`, traversal output is sorted. If `sort -z` is unavailable, generation continues with a warning and filesystem-dependent record order.
- Filenames with spaces, tabs, backslashes, carriage returns, and newlines are preserved through NUL-delimited traversal and GNU checksum escaping.
- Each selected path is checked for symlink components before and after hashing. Treat a reported symlink transition as an I/O/safety failure; do not retry by following the link.
- The manifest is written to a temporary file in the destination directory and then installed with `mv -f`, giving same-directory atomic replacement of the manifest file itself. This does not make the entire source tree an atomic snapshot or guarantee crash durability.
- The process uses `umask 077`; newly generated manifest files are therefore created with restrictive permissions unless the environment changes the underlying semantics.
- If no regular file is selected during real generation, the command exits 2. A dry run with zero selected files may still exit 0 and report zero.

Concurrency caveat: absence of `-f` is not a race-free no-clobber primitive. The existence check occurs before hashing, while final installation uses `mv -f`; a concurrent writer could create the destination in between. Use a controlled/quiescent output directory when concurrent hostile writers are in scope.

Preserve the invocation (`ROOT`, `-x` patterns, and output path) separately when auditability requires reconstructing scope; the manifest records do not encode the root path or exclusion patterns.

### `verify [-q] [-r ROOT] MANIFEST`

Treat `MANIFEST` as hostile input. Do not pre-interpret its lines as shell syntax.

Apply these verified semantics:

- Default root is the directory containing the manifest path as resolved by the program. Use `-r ROOT` when the manifest is stored elsewhere.
- `-q` suppresses successful `OK` lines and the final success summary; failures are still reported.
- Blank lines and `#` comment lines are ignored.
- Records must be GNU `sha256sum`-compatible: 64 hex digits, valid separator/mode, and a non-empty filename. Uppercase hex and `*` mode are accepted.
- GNU backslash escaping is decoded without `eval`; malformed escaping is rejected.
- Leading `./` is normalized away; empty and `.` path components are normalized; absolute paths and any `..` component are rejected.
- Duplicate paths are rejected **after** normalization, so syntactic aliases such as `a` and `./a` collide.
- Every existing path component, including the target, is checked for symlinks before hashing and checked again after hashing. A symlink component or symlink transition is exit 6.
- Only paths that test as regular files are hashed. A listed path that is absent or not a regular file is reported as `MISSING`; a read/hash failure is reported as `UNREADABLE`.
- Mismatches, missing targets, and unreadable targets are accumulated and produce exit 4 after record processing. Malformed/unsafe records, duplicate paths, symlink-policy violations, or a manifest with no checksum records produce exit 6.
- A relative path `-` is accepted in 1.0.0 as the real file named `-` under the verification root. It is not interpreted as stdin.
- Successful verification means every **listed record** matched. It does not enumerate the root and therefore does not detect additional unlisted files.

Do not rewrite an unsafe manifest silently to make it pass. Report the rejected condition and require an operator decision if the manifest itself must be corrected or regenerated.

### `selftest`

Use to check the selected local SHA-256 backend against the implemented known-answer vector for the bytes `abc`.

Success demonstrates only that this backend produced the expected digest for that vector during this run. It is not a comprehensive system test, race analysis, provenance check, or security certification.

### `version` and `help`

Use `version` to identify the program version and fixed algorithm. Use `help` or `help COMMAND` to inspect the implemented CLI. Zero arguments print main help and exit 0 without performing an integrity operation.
`help COMMAND` accepts every command listed in the main help, including
`help help`; an unknown command remains a usage error (exit 2).

## Exit-status interpretation

Preserve these meanings; never collapse every non-zero status into "bad checksum":

| Exit | Meaning in 1.0.0 | Operational response |
| ---: | --- | --- |
| 0 | Requested operation succeeded. | Interpret only within the subcommand's scope. |
| 1 | Internal/general runtime error. | Treat as tool/backend failure, not integrity mismatch. |
| 2 | Usage or invalid CLI input. Also used by `manifest` for an existing output without `-f` and for zero selected files in real generation. | Correct the invocation or scope; do not report integrity failure. |
| 3 | Required dependency missing. | Report the missing local dependency; do not install or escalate implicitly. |
| 4 | Integrity comparison failure. `compare`: digest mismatch. `verify`: one or more mismatch/missing/unreadable records. | Report the exact emitted classification; do not generalize to maliciousness. |
| 5 | I/O error. | Report the affected path/operation and stop or remediate access/storage conditions. |
| 6 | Malformed/unsafe manifest or manifest path-policy violation. Includes duplicate normalized paths and symlink-policy rejection. | Treat the manifest as rejected; do not weaken controls. |

Signal traps may terminate the process with 129 (HUP), 130 (INT), or 143 (TERM). Treat those as interrupted operations, not checksum results.

## Assurance limits

Communicate these limits whenever they affect the requested conclusion:

- Integrity covers regular-file **content bytes** only. Permissions, ownership, ACLs, xattrs, timestamps, empty directories, devices, and other metadata/object types are outside the model.
- Manifest generation excludes symlinks; verification rejects symlink components for listed targets. This does not imply that `hash` or `compare` reject symlink operands.
- `find -xdev` excludes files on other mounted filesystems beneath the root. Handle each required filesystem separately.
- Tree generation is not a filesystem snapshot. A file can change while being read, and pre/post symlink checks do not establish race freedom against a concurrently hostile filesystem.
- `verify` checks listed records only; it does not prove absence of additional files.
- A trusted digest/manifest needs an independent authentic channel when malicious substitution is plausible.
- Functional tests and `selftest` are evidence of observed behavior, not formal security certification.
- Report `shellcheck` or `shfmt` as passed only when there is direct evidence that the corresponding gate actually ran successfully. If unavailable, say **not executed**.
