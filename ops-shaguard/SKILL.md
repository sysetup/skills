---
name: ops-shaguard
description: >
  Generate and verify local SHA-256 content-integrity evidence using the
  shaguard Bash script bundled with this skill. Use whenever the user asks
  for file or stdin checksums, digest comparison, recursive checksum
  manifests, manifest verification, shaguard selftests, or diagnosis of
  shaguard results in local automation and CI. Resolve the bundled script
  from this skill; no system installation of shaguard is required.
compatibility: Linux, Bash 4+, sha256sum or BusyBox; manifest operations also require find, sort, mktemp, mv, dirname, and basename.
---

# Shaguard

## Resolve the bundled script

The implementation is [scripts/bin/shaguard](scripts/bin/shaguard).
`shaguard` is its program name, not an installed operating-system command.
Use this bundled implementation for every operation; do not search `PATH`
for shaguard, install it, create an alias, or substitute another copy.

Set `SKILL_MD_PATH` to the absolute path of the **loaded** `SKILL.md`,
obtained from the skill location supplied by the agent runtime. Do not
derive it from the current working directory or guess a host-specific path.
If the runtime did not provide a location, obtain it before executing.

Initialize in Bash, replacing the placeholder with that resolved location:

```bash
SKILL_MD_PATH='/absolute/path/to/ops-shaguard/SKILL.md'
if [[ "$SKILL_MD_PATH" != /* || ! -f "$SKILL_MD_PATH" ]]; then
  printf '%s\n' 'Error: an existing absolute SKILL.md path is required.' >&2
  exit 2
fi
SKILL_ROOT="$(cd -- "$(dirname -- "$SKILL_MD_PATH")" && pwd -P)" || exit 2
SHAGUARD_SCRIPT="${SKILL_ROOT}/scripts/bin/shaguard"
if [[ ! -f "$SHAGUARD_SCRIPT" || ! -r "$SHAGUARD_SCRIPT" ]]; then
  printf '%s\n' 'Error: the bundled shaguard script is missing or unreadable.' >&2
  exit 5
fi
bash "$SHAGUARD_SCRIPT" version
```

Expected version: `shaguard 1.0.0 (SHA-256)`. If it differs, inspect the
bundled implementation before relying on the version-specific reference.
If it is unavailable, report an incomplete skill package and stop.

Invoke it with `bash "$SHAGUARD_SCRIPT" SUBCOMMAND ...`. Preserve the
caller's working directory: relative operands and relative `manifest -o`
paths belong to the caller, not to the skill. When tool calls use separate
shells, pass the resolved absolute script path again or repeat initialization;
do not assume shell variables persist. Bash invocation also works when a
skill distribution does not preserve the script's executable bit.

## Choose and execute

Read the selected subcommand section and exit-status table in
[command semantics](references/command-semantics.md) before executing.
Use the bundled help for syntax: `bash "$SHAGUARD_SCRIPT" help COMMAND`.

| Objective | Invocation after initialization |
| --- | --- |
| Hash existing files | `bash "$SHAGUARD_SCRIPT" hash "$FILE"` |
| Hash supplied bytes | `printf '%s' 'abc' \| bash "$SHAGUARD_SCRIPT" stdin` |
| Compare a reference digest | `bash "$SHAGUARD_SCRIPT" compare "$EXPECTED_SHA256" "$FILE"` |
| Preview a recursive selection | `bash "$SHAGUARD_SCRIPT" manifest -n -x '*.tmp' "$ROOT"` |
| Create a manifest | `bash "$SHAGUARD_SCRIPT" manifest -o "$MANIFEST" "$ROOT"` |
| Verify listed records | `bash "$SHAGUARD_SCRIPT" verify -r "$ROOT" "$MANIFEST"` |
| Check the SHA-256 backend | `bash "$SHAGUARD_SCRIPT" selftest` |

1. Establish read scope, reference digest/manifest, and any output path from
   the request. `manifest` is the only subcommand creating a persistent
   artifact. Resolve output and overwrite intent from existing authorization;
   ask only if either remains ambiguous. Use `-f` only for an authorized
   replacement. A dry run still uses a temporary file internally.
2. Keep arguments separate and quoted, including exclusion globs. Run the
   script as a subprocess, never source it: it changes shell options and
   installs traps. Treat manifest contents as data, never shell syntax.
3. Capture stdout, stderr, and the final exit status. Partial hash records or
   earlier `OK` lines do not establish overall success. In pipelines capture
   the producer's status too; truncated input can still produce a valid hash.
4. Classify results with the reference's exit table. Dependency failure is
   exit 3; report it without installing packages or adding privileges/network
   access. Preserve path, symlink, duplicate, and overwrite protections.

## Interpret and report

A match establishes equality of the bytes read to the supplied reference.
It does not establish publisher identity or authenticity of that reference.
If both payload and reference can be replaced, require independent trust
before making an authenticity claim. A mismatch alone does not prove malware.

Report the operation, bundled version, effective root/input/output scope,
exit status, salient evidence, and any trust assumption. Verification covers
listed records only, not extra files. For mutable trees or metadata-sensitive
requests, consult the reference's assurance limits before drawing conclusions.
Stop on unsafe-manifest rejection rather than editing evidence to make it pass.

## Maintenance resources

- Read [scripts/README.md](scripts/README.md) when validating or packaging
  this skill. Distributions must retain the `scripts` directory.
- Read [architecture](references/architecture.md) for implementation
  boundaries and threat controls during maintenance.
- [scripts/docs/VALIDATION.md](scripts/docs/VALIDATION.md) records historical
  checks only; run current checks before claiming current results.
