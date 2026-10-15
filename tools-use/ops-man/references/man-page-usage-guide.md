# Man Page Lookup - Usage Guide

Extended reference for `ops-man`.

## Man Page Structure

Most installed man pages follow a recognizable structure:

| Section Header | Purpose |
|:---------------|:--------|
| `NAME` | Canonical name and one-line summary |
| `SYNOPSIS` | Invocation syntax |
| `DESCRIPTION` | Detailed behavior |
| `OPTIONS` | Flags and option semantics |
| `EXIT STATUS` | Return codes |
| `ENVIRONMENT` | Relevant environment variables |
| `FILES` | Config or data paths |
| `EXAMPLES` | Worked examples |
| `SEE ALSO` | Related pages |

`SYNOPSIS` and `OPTIONS` are usually the most useful sections for agent
workflows.

## Common Section Labels

| Label | Scope | Example |
|------:|:------|:--------|
| `1` | User commands | `ls(1)` |
| `2` | System calls | `open(2)` |
| `3` | Library functions | `printf(3)` |
| `5` | File formats | `fstab(5)` |
| `7` | Conventions and misc | `regex(7)` |
| `8` | Administration commands | `iptables(8)` |
| `n` | New-format man pages on some systems | Host-dependent |
| `3posix` | POSIX library pages on some systems | Host-dependent |

Not every host installs every label. The skill accepts extended labels, but the
lookup still depends on what the host actually ships.

## Recommended Lookup Strategy

1. Start with `bash scripts/man_page_lookup.sh <command>`.
2. If the name is ambiguous, add the section:
   `bash scripts/man_page_lookup.sh <command> <section>`.
3. Increase `max_tokens` only when the agent truly needs a larger slice of the
   page.

## Troubleshooting

| Symptom | Likely Cause | Suggested Fix |
|:--------|:-------------|:--------------|
| Exit code `3` | `man` or `col` missing | Install the packages that provide them. On Debian/Ubuntu: `man-db` and `bsdextrautils`. |
| Exit code `4` for a known topic | The relevant manual set is not installed | Install the package that ships the page, then retry. |
| Wrong page | Ambiguous name across sections | Re-run with an explicit section label. |
| Truncated output | Token budget too small | Re-run with a larger `max_tokens` value. |

## Security Notes

- The skill accepts only manual page names, not arbitrary file paths.
- The script rejects slash-based input to avoid `man` local-file mode.
- The lookup runs with a sanitized environment so caller-supplied `MANOPT`,
  `MANPAGER`, or `PAGER` values do not alter behavior.
- The script is read-only and does not write files or use the network.
