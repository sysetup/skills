# Canonical contract (preflight)

Source of truth: this file and the local `schemas/` directory. This file maps
each canonical requirement to its preflight check and states the severity
policy.

## Fail-only-on-canon policy

`preflight.py` FAILs only when a canonical requirement is broken. Everything
else is `WARNING` or `ADVICE`. Consequences:

- A generated skill passes preflight unless it truly violates the canon
  (broken name/description, dangling bundled reference, or a security
  violation).
- Extra frontmatter fields (`version`, `license`, `allowed-tools`,
  `metadata`, ...) are tolerated with no penalty: the canon requires only
  `name` and `description`, plus optional string `compatibility`.
- Body length is advisory: the canon's "under 500 lines" is explicitly
  approximate ("feel free to go longer if needed").
- Skills without `evals/`, `scripts/`, `references/`, or `assets/` pass:
  those resources are optional and are created by the loop when needed.

## Check map

| ID | Severity | Canon requirement |
|----|----------|-------------------|
| P001 | FAIL | Valid YAML frontmatter between `---` delimiters |
| P002 | FAIL | `name`: kebab-case, max 64 chars |
| P003 | FAIL | `description`: non-empty, max 1024 chars |
| P004 | FAIL | Referenced bundled files exist (`scripts/`, `references/`, `assets/`, bundled siblings) |
| P005 | FAIL | Principle of Lack of Surprise: no secrets, destructive commands, pipe-to-shell, exfiltration, or jailbreak instructions |
| P101 | ADVICE | SKILL.md body ideally under 500 lines |
| P102 | ADVICE | Description carries WHEN/trigger context (undertriggering is the canonical failure mode) |
| P103 | WARNING | Reference files over 300 lines need a table of contents |
| P105 | ADVICE | `compatibility`, when present, should be a string |
| P106 | ADVICE | Files under `references/` are pointed to from SKILL.md with load guidance |

## Bundled-resource declarations (P004)

A relative Markdown link in resource guidance declares a bundled resource;
directory and file-extension names do not restrict this requirement. This
includes inline links, images, and explicit or collapsed reference-style
links with a defined destination. Resolve the destination relative to the
target `SKILL.md`, including `./` and bundled sibling paths using `../`.
Strip the anchor fragment and decode URL-encoded path characters before
checking existence. Pure `#section` links are internal links; preflight
does not validate anchors. URLs with a scheme, protocol-relative URLs, and
absolute paths do not declare files bundled relative to the skill.

P004 checks actual bundled-resource declarations, not every path mentioned
in documentation. Fenced examples (backticks or tildes), inline code that
quotes Markdown link syntax, and explicitly titled example/sample or
generated/expected output sections are illustrative. An immediately
preceding `Example:`, `For example,`, `Output:`, or instruction such as
`Generate`, `Save the report to`, or `Write the output to` marks an example
or future output rather than a required input. Section context ends at the
next heading of equal or higher level. Nearby words elsewhere in the prose
do not exempt a required link. Unused link definitions are not declarations.

Existing supported bare paths under `scripts/`, `references/`, `assets/`,
`agents/`, `eval-viewer/`, `schemas/`, `templates/`, and `fixtures/` remain
checked, including paths in inline code and supported sibling forms.
Arbitrary bare prose paths and the full Markdown grammar are not inferred:
use a supported link form for resources outside those bare-path forms.
Natural-language intent beyond the explicit contexts above remains
ambiguous; preflight does not introduce additional failure rules for it.

## Documentation-context rule

The security scan skips fenced/inline code and matches surrounded by
documentation hints (a checklist that names a dangerous command is not an
instruction to run it). See `security-preflight.md`.
