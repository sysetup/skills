# Code conventions for HTML.

These conventions define mandatory standards for HTML. They prioritize validity, accessibility, and consistency.

---

## 1. Purpose and Scope
- Applies to all HTML files (*.html).
- New and modified files must comply.

## 2. Normative Alignment
- HTML is defined by the WHATWG HTML Living Standard.
- Style baseline: Google HTML/CSS Style Guide.
- This document is authoritative; where external guides conflict, follow this standard.

## 3. Tooling Requirements
### 3.1 Validation (Required)
- Validate markup with the Nu HTML Checker.

### 3.2 Formatting (Required)
- Prettier for formatting; do not hand-format against formatter output.

### 3.3 Editor (Recommended)
- Visual Studio Code with HTML, Prettier, and accessibility tooling.

## 4. Formatting (Rationale)
- Indentation: 4 spaces; no tabs (Prettier: `tabWidth: 4`, `useTabs: false`).
- Lowercase tag and attribute names.
- Double quotes for attribute values.
- One element per line for nested structures; wrap long attribute lists onto multiple lines.
- Rationale: predictable structure improves readability and diff quality.

## 5. Naming (Rationale)
- `id` and `class` values must use kebab-case.
- `id` is unique per document; use `class` for shared styling/behavior.
- Use `data-*` attributes for JS hooks; avoid styling based on data attributes.
- Rationale: consistent naming supports searchability and maintainable selectors.

## 6. Structure and Organization
- Use the HTML5 doctype and a complete document structure:
```html
<!doctype html>
<html lang="en">
    <head>...</head>
    <body>...</body>
</html>
```
- Place scripts at the end of `body` or use `defer`.
- Keep CSS in external stylesheets; avoid inline styles.

## 7. Markup Rules
- Prefer semantic elements (`header`, `main`, `section`, `nav`, `footer`).
- Provide `alt` for images and labels for form controls.
- Avoid inline event handlers (`onclick`, `onload`).
- Ensure proper nesting and valid hierarchy.

## 8. Security and Safety (Rationale)
- Do not inject untrusted HTML; sanitize and encode user content.
- Use `rel="noopener"` (and `noreferrer` when needed) with `target="_blank"`.
- Rationale: reduce XSS risk and prevent tab-nabbing.

## 9. Documentation and Comments
- Use HTML comments to separate major sections.
- Do not leave commented-out code in production templates.

## 10. Testing and Verification
- Validate with Nu HTML Checker.
- Run Prettier as part of CI formatting checks.

## 11. Appendix A: References
- WHATWG HTML Living Standard - https://html.spec.whatwg.org/multipage/ (Accessed 2026-01-15)
- Google HTML/CSS Style Guide - https://google.github.io/styleguide/htmlcssguide.html (Accessed 2026-01-15)
- Nu HTML Checker - https://validator.github.io/validator/ (Accessed 2026-01-15)
- Prettier - https://prettier.io/docs/configuration (Accessed 2026-01-15)
