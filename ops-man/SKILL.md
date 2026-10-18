---
name: ops-man
description: >-
  Retrieve authoritative host-local man page text for installed commands,
  system calls, or library functions. Use when an agent must verify exact CLI
  syntax or flags, disambiguate manual sections, or consult installed POSIX
  manuals and local system documentation. Works independently of other skills.
compatibility: Debian with Bash, GNU coreutils, man-db and col installed; no installation is performed.
license: MIT
metadata:
  version: "1.2.2"
---

# Host manual lookup

Retrieve installed manual pages as plain text with the local man database. Resolve `<skill-dir>` to the absolute directory containing this file; do not assume that it is the caller's working directory. The [bundled script](scripts/man_page_lookup.sh) and usage guide provide the complete lookup workflow; no other skill or documentation catalog is required.

For a routine lookup, invoke `bash "<skill-dir>/scripts/man_page_lookup.sh" COMMAND [SECTION] [MAX_TOKENS]`. The command is a manual name, not a path. Apply the active user, host, project, and runtime instructions; a manual lookup does not authorize executing the documented operation.

Keep this capability limited to local manual retrieval. General tool selection, host procedure retrieval, document authoring, and framework/API research remain separate task responsibilities.

When host policy requires POSIX documentation, request the applicable installed POSIX section explicitly; the default search does not establish POSIX provenance. If the required entry is absent, report the gap and stop dependent work. Continue only independent work permitted by host policy. Dependency installation requires explicit user authorization; delegate every root or sudo operation to the user.

Read the [usage guide](references/man-page-usage-guide.md) only when disambiguating sections, handling truncated output, or troubleshooting missing dependencies or entries. When the required source is unavailable, report the gap; use other documentation only under the task's source and authorization rules. API documentation absent from the local manual database belongs to the task's dedicated documentation capability.

## Usage

`bash "<skill-dir>/scripts/man_page_lookup.sh" [OPTIONS]... COMMAND [SECTION] [MAX_TOKENS]`

| Input | Contract |
| --- | --- |
| COMMAND | Required manual name; no leading hyphen, slash, or consecutive dots. |
| SECTION | Optional; default 0 searches installed sections. Labels such as 2, 8, n, and 3posix are accepted. |
| MAX_TOKENS | Optional approximate budget, default 6000; decimal 100 to 100000 without leading zeros. Explicitly empty optional arguments are invalid. |
| -h, --help | Print help to stdout and exit 0. |
| -V, --version | Print script version to stdout and exit 0. |

Examples: `bash "<skill-dir>/scripts/man_page_lookup.sh" ls`, `bash "<skill-dir>/scripts/man_page_lookup.sh" open 2`, `bash "<skill-dir>/scripts/man_page_lookup.sh" printf 3posix 8000`. Example pages and POSIX sections require their corresponding manual packages to be present.

| Status | Meaning |
| --- | --- |
| 0 | Success. |
| 2 | Usage or validation error, including zero arguments. |
| 3 | Missing man or col dependency. |
| 4 | Manual entry absent or rendering failed. |

## Execution boundaries

The script validates manual names, sections, and budgets before lookup. Its man subprocess runs under `env -i` with a reduced PATH and fixed locale, avoiding caller-supplied MANOPT, MANPAGER, or PAGER. col removes overstrike formatting; output truncation is approximate, not tokenizer accounting. Use a trusted host PATH and installed manual database: environment filtering is not a subprocess sandbox. The wrapper requests no file changes, network operations, or elevated privileges; installed tools retain their own configuration and cache behavior. Installed manual availability and successful rendering do not prove operation correctness.
