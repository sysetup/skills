# Code conventions for CSS in **Sysetup**.

These conventions define mandatory standards for CSS across Sysetup. They prioritize consistency, readability, and long-term maintainability.

---

## 1. Purpose and Scope
- Applies to all CSS files (*.css).
- New and modified files must comply.

## 2. Normative Alignment
- CSS specifications are defined by the W3C CSS Snapshot.
- Style baseline: Google HTML/CSS Style Guide.
- This document is authoritative for Sysetup; where external guides conflict, follow this standard.

## 3. Tooling (Optional)
### 3.1 Linting (Optional)
- If available in the project toolchain, run Stylelint with the project configuration.
- Example command:
```bash
stylelint "src/**/*.css"
```

### 3.2 Formatting (Optional)
- If available in the project toolchain, run Prettier. When used, prefer formatter output over manual formatting.
- Example command:
```bash
prettier --write "src/**/*.css"
```

### 3.3 Editor (Recommended)
- Visual Studio Code with Stylelint and Prettier extensions.

## 4. Formatting (Rationale)
- Indentation: 4 spaces; no tabs (Prettier: `tabWidth: 4`, `useTabs: false`).
- One declaration per line; trailing semicolon required.
- Lowercase hex colors.
- Group declarations by type: Positioning, Box Model, Color, Text, Other.
- Rationale: consistent diffs and predictable scanning during reviews.

## 5. Naming (Rationale)
- Class, id, and custom property names: kebab-case.
- Use meaningful, semantic names; avoid abbreviations.
- Rationale: predictable naming improves reuse and auditability.

## 6. Structure and Organization
- Order selectors by type: element, id, class.
- Keep related rules together; group by component or module.
- Place utilities in a dedicated section or file.

## 7. CSS Rules
- Avoid `!important` except for documented legacy overrides.
- Prefer CSS custom properties for shared values.
- Keep selector specificity low and consistent.
- Use shorthand properties only when they improve clarity.

**Property Grouping Example**

```css
.selector {
    /* Positioning */
    position: absolute;
    z-index: 10;
    top: 0;
    right: 0;

    /* Display and Box Model */
    display: inline-block;
    overflow: hidden;
    box-sizing: border-box;
    width: 100px;
    height: 100px;
    padding: 10px;
    border: 10px solid #333;
    margin: 10px;

    /* Color */
    background: #000;
    color: #fff;

    /* Text */
    font-family: sans-serif;
    font-size: 16px;
    line-height: 1.4;
    text-align: right;

    /* Other */
    cursor: pointer;
}
```

## 8. Security and Safety (Rationale)
- Avoid inline styles for untrusted content; keep CSS in static files.
- Avoid `@import` from untrusted sources.
- Rationale: reduce injection risk and improve caching.

## 9. Documentation and Comments
- Use block comments for section headers and non-obvious rules.

## 10. Testing and Verification
- If tooling is used (e.g., Stylelint/Prettier): it should pass cleanly with the project configuration.
- Validate CSS in CI as part of the build pipeline.

## 11. Appendix A: References
- W3C CSS Snapshot - https://www.w3.org/TR/css-2025/ (Accessed 2026-01-15)
- Google HTML/CSS Style Guide - https://google.github.io/styleguide/htmlcssguide.html (Accessed 2026-01-15)
- Stylelint - https://stylelint.io/ (Accessed 2026-01-15)
- Prettier - https://prettier.io/docs/configuration (Accessed 2026-01-15)
