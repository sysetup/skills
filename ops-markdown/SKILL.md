---
name: ops-markdown
description: Create, edit, normalize, and review Markdown formatting. Use whenever a user or another agent assigns work on .md or .markdown files, including README files, technical guides and Markdown agent instructions.
---

# Markdown formatting

Apply the standard below within the requested scope. It governs formatting; the document owner governs subject matter, factual correctness, and operational policy.

## Workflow

1. Establish the files, embedding context, and requested operation: create, edit, normalize, or review. A review is read-only unless corrections are requested; whole-document or repository normalization requires that scope.
2. Read the source and applicable project instructions before editing. Identify paragraphs, container boundaries, literal regions, dialect requirements, and meaningful whitespace. Adjacent source lines need not belong to one paragraph.
3. Resolve material instruction conflicts before the affected edit. Record scoped exceptions with their authority and reason; preserve uncertain content and report the issue while continuing independent work.
4. Create or edit through the runtime's authorized patch mechanism. For ordinary edits, format only new and affected content; preserve unrelated bytes where practical.
5. Inspect the resulting source and diff. Check affected paragraph boundaries, block structure, inline markup, links, and literal content against this standard.
6. Report changed or reviewed files, actual manual checks, actionable locations, and unresolved formatting issues or exceptions. Do not claim automated verification from visual inspection.

## Local standard

The identifiers below name this standard's rules. Use GitHub Flavored Markdown (GFM) by default, preserving an existing document's required dialect and embedding context. House conventions supplement syntax; they do not redefine it.

### M01 — File representation

Create documents as UTF-8 with LF line endings and a final newline. Preserve required encodings or line endings in existing artifacts unless conversion is authorized. Treat such requirements as explicit exceptions, not incidental cleanup.

### M02 — Prose paragraphs

Store each prose paragraph on one physical line and separate paragraphs with blank lines. This is a house convention: GFM permits ordinary source newlines inside paragraphs. Editor visual wrapping is acceptable; fixed-column hard wrapping and prose truncation are not.

Join incidental wrapped lines only after identifying the same paragraph and preserving its wording, inline markup, and boundaries. Structural breaks, multiline inline constructs, and deliberate rendered breaks are preservation exceptions; two trailing spaces or a terminal backslash can encode a rendered break.

### M03 — Block boundaries

Separate headings, lists, and other blocks clearly, normally with blank lines around blocks. Preserve list tightness, nesting, and continuation semantics; do not insert blank lines mechanically between list items or flatten quotes and containers.

### M04 — Headings

Use ATX headings for new headings with a space after the marker and a coherent hierarchy; normally descend one level at a time. Preserve established heading levels and structures in existing documents unless restructuring is requested. Do not force a standalone title onto an embedded fragment.

### M05 — Lists

Use consistent markers within each list and align nested content with its parent item's content. Preserve ordered-list starting values, task markers, nesting, tightness, and intentional continuations. Keep structural source line breaks rather than joining list items as prose.

### M06 — Literal examples

Prefer fenced examples for new code, using a known language label or `text` for unclassified text. Choose a fence longer than conflicting delimiter runs in its content. Preserve existing fenced and indented code, comments beginning with `#`, diagrams, and significant literal whitespace. Format the surrounding Markdown without interpreting or executing embedded content.

### M07 — Tables

Use legible GFM tables with a header and delimiter row. Keep source cells readable without requiring equal column widths. Preserve cell content and alignment; escape literal cell pipes, including pipes inside inline code, where GFM requires it. Keep complex or dialect-specific tables intact when their interpretation is uncertain.

### M08 — Links and images

Use meaningful link labels and image alternatives appropriate to their context. Preserve destinations, URLs, reference definitions, escapes, inline markup, and existing citations unless a requested change covers them. Empty image alternatives may be intentional for decorative images; retain that exception when appropriate.

### M09 — Preservation and scope

Preserve wording, content boundaries, intentional line breaks, frontmatter, HTML, inline constructs, and dialect semantics unless changing them is explicitly in scope. Avoid blanket whitespace cleanup because literal whitespace and rendered breaks carry meaning.

Keep document-specific requirements and explicit scoped exceptions visible. Formatting does not authorize content changes, link removal, subject-matter assessment, installation, or execution of examples. Do not impose runbook sections, version-control procedures, or skill-authoring policy as Markdown syntax.

### M10 — Native Markdown and HTML fallback

Use native syntax of the document's required Markdown dialect whenever it can express the required structure and meaning. Do not substitute raw HTML for equivalent Markdown headings, paragraphs, emphasis, lists, links, images, tables, or code blocks. Use raw HTML only as a last resort when the required feature has no native Markdown equivalent and the target renderer supports it; record the necessity as a scoped exception.

This rule applies to HTML used as document markup. HTML displayed as literal code inside fenced blocks (including `html` fences), indented code blocks, or inline code is exempt; preserve it under M06. Under M09, report redundant existing HTML and recommend its Markdown equivalent without rewriting it unless that conversion is explicitly in scope.

## Manual completion check

For creation, inspect the whole new artifact; for edits, inspect affected source and the diff; for review, report findings without writing. Confirm no prose was truncated or wrapped to a fixed width and that protected structures retain their meaning.

This package contains instructions only and works independently. Basic manual inspection completes its workflow; automated checking, checker development, formal tests, and machine-readable audits belong to separately requested verification work.
