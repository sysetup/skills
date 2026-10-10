# Implementation boundaries

The system is the Bash script bundled at `scripts/bin/shaguard`, resolved
relative to the loaded skill. It has no installation or network component.
The dispatcher validates CLI arguments and selects a SHA-256 backend:
`sha256sum`, with BusyBox's equivalent applet as fallback.

| Path | Processing |
| --- | --- |
| `hash`, `compare`, `stdin` | Read file/stream bytes, hash, emit digest or comparison |
| `manifest` | Validate root/options, enumerate regular files, hash, write temporary manifest, rename into place |
| `verify` | Parse records, normalize paths, reject unsafe/duplicate/symlink paths, hash listed files, compare |

CLI arguments, filenames, filesystem state, and manifest records are input
boundaries. Manifest text is potentially hostile; GNU escaping is decoded
without shell evaluation. Traversal uses NUL-delimited filenames and stays
within one filesystem. Temporary files are tracked for cleanup, with
`umask 077`; manifest replacement uses a temporary file in its destination
directory. These controls do not create a snapshot or establish race freedom.

The exact path policy, exit meanings, symlink differences between commands,
and concurrency limits live in [command semantics](command-semantics.md).
Keep those facts there rather than maintaining conflicting policy lists.

The behavioral suite at `scripts/tests/test_shaguard.sh` checks safe
zero-argument behavior, the known-answer vector, hashes, digest comparison,
manifest generation/exclusion, escaped filenames, mutation detection,
traversal and symlink rejection, dry-run behavior, and overwrite protection.
See [scripts/README.md](../scripts/README.md) for current validation commands.
