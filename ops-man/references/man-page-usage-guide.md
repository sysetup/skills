# Man Page Lookup - Usage Guide

Extended reference for `ops-man`.

## Man Page Structure

Most installed man pages follow a recognizable structure:

| Section Header | Purpose |
| :--- | :--- |
| `NAME` | Canonical name and one-line summary |
| `SYNOPSIS` | Invocation syntax |
| `DESCRIPTION` | Detailed behavior |
| `OPTIONS` | Flags and option semantics |
| `EXIT STATUS` | Return codes |
| `ENVIRONMENT` | Relevant environment variables |
| `FILES` | Config or data paths |
| `EXAMPLES` | Worked examples |
| `SEE ALSO` | Related pages |

`SYNOPSIS` and `OPTIONS` are usually the most useful sections for agent workflows. These headings are parts of one page, distinct from manual section labels such as `1` and `3`.

## Common Section Labels

| Label | Scope | Example |
| ---: | :--- | :--- |
| `1` | User commands | `ls(1)` |
| `2` | System calls | `open(2)` |
| `3` | Library functions | `printf(3)` |
| `5` | File formats | `fstab(5)` |
| `7` | Conventions and misc | `regex(7)` |
| `8` | Administration commands | `iptables(8)` |
| `n` | New-format man pages on some systems | Host-dependent |
| `1p` | POSIX utility pages on some systems | `printf(1p)`, if installed |
| `3posix` | POSIX library pages on some systems | Host-dependent |

Not every host installs every label. The skill accepts extended labels, but the lookup still depends on what the host actually ships. Selecting section `1` does not establish POSIX provenance; request the installed POSIX label explicitly when required.

## Recommended Lookup Strategy

1. Resolve `<skill-dir>` to the absolute directory containing SKILL.md. Select the section required by host policy. Use the default `bash "<skill-dir>/scripts/man_page_lookup.sh" <command>` only when no specific documentation source is required.
2. If the name is ambiguous, add the manual section: `bash "<skill-dir>/scripts/man_page_lookup.sh" <command> <section>`.
3. For truncated output, rerun with a larger budget, up to `100000`. The script returns a prefix of the page; it has no heading filter or continuation offset. Selecting another manual section changes the source page, not the heading within it.

## Troubleshooting

| Symptom | Likely Cause | Suggested Fix |
| :--- | :--- | :--- |
| Exit code `3` | `man` or `col` missing | Report the missing dependency. Debian package names are `man-db` and `bsdextrautils`; follow the installation boundary in SKILL.md. |
| Exit code `4` for a known topic | Entry absent or rendering failed | Report the gap. If the source is required, stop dependent work; do not silently substitute another section. Follow SKILL.md before any package installation. |
| Wrong page | Ambiguous name across sections | Re-run with an explicit section label. |
| Truncated output | Token budget too small | Re-run with a larger `max_tokens` value. |

## Security Notes

- The skill accepts only manual page names, not arbitrary file paths.
- The script rejects slash-based input to avoid `man` local-file mode.
- The man subprocess runs with a filtered environment so caller-supplied `MANOPT`, `MANPAGER`, or `PAGER` values do not alter its behavior.
- See SKILL.md for the trusted-tool and execution boundaries; environment filtering does not confine installed tools or their cache behavior.
