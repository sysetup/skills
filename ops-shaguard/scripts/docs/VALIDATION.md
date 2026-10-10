# Historical validation record

This record predates integration into ops-shaguard. Its paths and tool
availability describe that earlier environment, not the current skill.

Date: 2026-09-17

Scope: `/mnt/data/shaguard` release candidate 1.0.0.

Executed checks:

- `bash -n bin/shaguard tests/test_shaguard.sh`: PASS.
- `bash tests/test_shaguard.sh`: PASS, 15 passed / 0 failed.
- SHA-256 known-answer vector using the direct backend: PASS.
- SHA-256 known-answer vector forcing the BusyBox backend: PASS.
- GNU `sha256sum -c` interoperability with a generated manifest: PASS.
- Extra edge checks for a file named `-`, quiet verification, absolute-path
  rejection, and duplicate manifest-path rejection: PASS.
- Manual style sanity: no tabs, no trailing whitespace, no Bash/test line over
  80 characters: PASS.
- Systems-engineering Markdown artifact checker: PASS, 0 errors / 0 warnings.

Unavailable gates in this execution environment:

- `shellcheck`: not installed, therefore not executed.
- `shfmt`: not installed, therefore not executed.

Those two unavailable gates are not reported as passed. The source was still
checked with `bash -n`, the behavioral suite, deterministic style checks, and
manual review against the project Bash conventions.

Assurance limits:

- These checks do not certify security or prove race freedom on a concurrently
  hostile filesystem.
- SHA-256 checksums prove content equality to a trusted digest, not publisher
  authenticity.
- High-assurance use should hash a read-only or quiescent snapshot and protect
  the manifest through an authenticated channel.
