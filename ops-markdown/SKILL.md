---
name: ops-markdown
description: Create and edit Markdown files. Use whenever writing or modifying .md files, including README files, documentation, and SKILL.md files, or removing fixed-width paragraph wrapping.
---

# Markdown prose formatting

## Formatting rules

- Keep each prose paragraph on one physical line in the stored file. Use blank lines to separate paragraphs. Editor visual wrapping is acceptable because it does not insert stored newlines.
- Do not insert line breaks to enforce a character or column limit. Width conventions for Bash or commit messages do not establish Markdown prose limits. Configure any formatter used for this task to preserve prose lines; avoid automatic hard wrapping.
- Preserve structural and intentional line breaks in headings, list items, tables, code blocks, block quotes, and deliberate rendered breaks. Keep list markers, nesting, quote prefixes, and code indentation intact; do not flatten multiline structures to satisfy the prose rule.
- Separate headings and lists from surrounding content with blank lines. Preserve the target document's Markdown dialect, links, inline markup, and fenced or indented code semantics.

## Procedure

1. For an existing file, inspect its source and applicable project instructions before editing. Identify paragraph boundaries and meaningful line breaks; adjacent lines do not necessarily belong to the same paragraph.
2. For a new file, organize the requested content with appropriate headings, paragraphs, lists, and code blocks, then apply the formatting rules above.
3. For edits, apply the rules to new and affected prose. Join incidental fixed-width wrapping within a paragraph without changing its wording or boundaries; make content changes only as requested.
4. Keep unrelated content unchanged. Reformat entire documents or repositories only when that scope is authorized.
5. Follow higher-priority instructions. Resolve remaining conflicts with explicit artifact requirements before the dependent edit; any requested exception must have an authorized scope and reason.

## Verification

Inspect the source and, for edits, the diff rather than relying on rendered appearance. Confirm that each affected prose paragraph occupies one physical line unless it contains an intentional rendered break. Check paragraph separation and verify that lists, quotes, tables, links, and code retain their intended meaning. No external reference, formatter, or additional dependency is required. Report the changed files, checks actually performed, and any unresolved conflict.
