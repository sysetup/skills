# Implementation boundaries

The system is the Bash script bundled at `scripts/bin/shaguard`, resolved
relative to the loaded skill. It has no installation or network component.
The dispatcher validates CLI arguments and selects a SHA-256 backend:
`sha256sum`, with BusyBox's equivalent applet as fallback.

| Path | Processing |
| --- | --- |
| `hash`, `compare`, `stdin` | Read file/stream bytes, hash, emit digest or comparison |
| `manifest` | Validate root/options, enumerate regular files, hash, publish a temporary manifest by exclusive hard link or authorized atomic replacement |
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
