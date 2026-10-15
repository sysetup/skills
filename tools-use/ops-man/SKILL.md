---
name: ops-man
description: >-
  Retrieve authoritative host-local man page text for installed commands,
  system calls, or library functions. Use when an agent must verify exact CLI
  syntax or flags, disambiguate manual sections, or consult local system
  documentation directly or through ops-tools.
compatibility: Debian with GNU man and col installed; no installation is performed.
license: MIT
metadata:
  version: "1.2.0"
---

# Host manual lookup

Retrieve installed manual pages as plain text with the local man database. Resolve bundled paths from the directory containing this file. Applicable host standards and procedures are consulted separately through doc-get.

For a routine lookup, invoke `bash scripts/man_page_lookup.sh COMMAND [SECTION] [MAX_TOKENS]`. The command is a manual name, not a path. A manual lookup does not authorize executing the documented operation.

Read the [usage guide](references/man-page-usage-guide.md) only when disambiguating sections, handling truncated output, or troubleshooting missing dependencies or entries. When the required source is unavailable, report the gap; use other documentation only under the task's source and authorization rules. API documentation absent from the local manual database belongs to the task's dedicated documentation capability.

## Usage

`bash scripts/man_page_lookup.sh [OPTIONS]... COMMAND [SECTION] [MAX_TOKENS]`

| Input | Contract |
| --- | --- |
| COMMAND | Required manual name; no leading hyphen, slash, or consecutive dots. |
| SECTION | Optional; default 0 searches installed sections. Labels such as 2, 8, n, and 3posix are accepted. |
| MAX_TOKENS | Optional approximate budget, default 6000, range 100 to 100000. |
| -h, --help | Print help to stdout and exit 0. |
| -V, --version | Print script version to stdout and exit 0. |

Examples: `bash scripts/man_page_lookup.sh ls`, `bash scripts/man_page_lookup.sh open 2`, `bash scripts/man_page_lookup.sh printf 3posix 8000`.

| Status | Meaning |
| --- | --- |
| 0 | Success. |
| 2 | Usage or validation error, including zero arguments. |
| 3 | Missing man or col dependency. |
| 4 | Manual entry absent or rendering failed. |

## Execution boundaries

The script validates manual names, sections, and budgets before lookup. Its man subprocess runs under `env -i` with a minimal PATH and fixed locale, avoiding caller-supplied MANOPT, MANPAGER, or PAGER. col removes overstrike formatting; output truncation is approximate, not tokenizer accounting. No files, network requests, or privileged operations are performed. Installed manual availability and successful rendering do not prove operation correctness.
