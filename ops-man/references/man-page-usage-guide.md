# Man Page Lookup - Usage Guide

Extended reference for `ops-man`.

## Man Page Structure

Most installed man pages follow a recognizable structure:

| Section Header | Purpose |
| --- | --- |
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
| --- | --- | --- |
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

## Focused Excerpt Lookup (`--match=TEXT`)

Pass one or more `--match=TEXT` options before the positional arguments to search the full rendered manual once and return only relevant excerpts within the output budget:

```bash
bash "<skill-dir>/scripts/man_page_lookup.sh" --match=--color ls 1
bash "<skill-dir>/scripts/man_page_lookup.sh" --match=ServerAliveInterval ssh_config 5
bash "<skill-dir>/scripts/man_page_lookup.sh" --match=GuestExecStatus --match=guest-exec-status qemu-ga-ref 7
```

Key contract details and limits:

- **Single local render**: The page is rendered once through the same noninteractive `man | col -bx` pipeline and filtered before `MAX_TOKENS` is applied, avoiding premature prefix truncation on large pages.
- **Literal matching**: `--match=TEXT` matches exact single-line substrings without regular-expression interpretation. Leading hyphens (`--match=--color`) and punctuation (`[ ] ( ) * + ? . ^ $ \ |`) are treated as plain text. Matching is case-sensitive and cannot span rendered line breaks or roff line-wrap hyphenation.
- **Structural block extraction**: Each emitted excerpt preserves exact source wording and indentation and carries a header identifying its kind, section or enclosing entry, and line range:
    - `[definition]` — complete option, directive, object, command, or compact section block when headings and indentation establish its boundaries.
    - `[cross-reference]` — compact enclosing entry or related paragraph that adds conditions or interactions referencing the term.
    - `[context window]` — bounded `±4`-line window (or prose block without a defining entry) used when layout boundaries are ambiguous or span an unbroken block.
- **Merging and budget packing**: Overlapping excerpts are merged before emission. Primary definitions (and top hits for each matched term) take priority over secondary cross-references when `MAX_TOKENS` is tight; selected excerpts are emitted in document order.
- **Explicit gap reporting**: If no requested term matches anywhere on the page, the script exits `1` (preserving exit `4` for an absent manual). When some terms match and others do not, or when excerpts exceed `MAX_TOKENS`, the output prints explicit `MISSING MATCH TERMS`, `OMITTED EXCERPTS`, or `EXCERPT TRUNCATED` notices.

## Recommended Lookup Strategy

1. Resolve `<skill-dir>` to the absolute directory containing `SKILL.md`. Select the section required by host policy. Use the default `bash "<skill-dir>/scripts/man_page_lookup.sh" <command>` only when no specific documentation source is required.
1. If the name is ambiguous, add the manual section: `bash "<skill-dir>/scripts/man_page_lookup.sh" <command> <section>`.
1. For large pages or specific flags, directives, or protocol objects, prefer repeatable `--match=TEXT` before positional arguments so complete definitions are retrieved in one render without raising `MAX_TOKENS` blindly.
1. For truncated full-page output or omitted focused excerpts, rerun with a larger `MAX_TOKENS` budget, up to `100000`. Selecting another manual section changes the source page, not the heading within it.

## Troubleshooting

| Symptom | Likely Cause | Suggested Fix |
| --- | --- | --- |
| Exit code `1` | No `--match=TEXT` term matched the rendered page | Verify exact spelling and capitalization, try a shorter literal stem without wrapped punctuation, or run a broader lookup without `--match=TEXT`. |
| Exit code `2` | Invalid option syntax, empty `--match=`, or bad positional arguments | Place `--match=TEXT` before `COMMAND`, use `=TEXT` syntax, and verify `SECTION` and `MAX_TOKENS` bounds. |
| Exit code `3` | `man`, `col`, or `awk` (for `--match`) missing | Report the missing dependency. Debian package names are `man-db`, `bsdextrautils`, and `mawk`/`gawk`; follow the installation boundary in `SKILL.md`. |
| Exit code `4` for a known topic | Entry absent or rendering failed | Report the gap. If the source is required, stop dependent work; do not silently substitute another section. Follow `SKILL.md` before any package installation. |
| Wrong page | Ambiguous name across sections | Re-run with an explicit section label. |
| Truncated or omitted output | Token budget too small | Add narrower `--match=TEXT` terms or re-run with a larger `MAX_TOKENS` value. |

## Security Notes

- The skill accepts only manual page names, not arbitrary file paths.
- The script rejects slash-based input to avoid `man` local-file mode.
- The `man` and `awk` subprocesses run with a filtered environment (`env -i`) so caller-supplied `MANOPT`, `MANPAGER`, or `PAGER` values do not alter behavior; `--match=TEXT` values are passed as literal data, never evaluated as regexes or shell code.
- See `SKILL.md` for the trusted-tool and execution boundaries; environment filtering does not confine installed tools or their cache behavior.
