# Code conventions for JavaScript in **Sysetup**.

These conventions define mandatory standards for JavaScript. They prioritize correctness, security, and maintainability.

---

## 1. Purpose and Scope
- Applies to all JavaScript source files (*.js).
- New and modified files must comply.

## 2. Normative Alignment
- Primary language reference: ECMA-262 (ECMAScript).
- Style baseline: Airbnb JavaScript Style Guide.
- This document is authoritative for Sysetup; where external guides conflict, follow this standard.

## 3. Tooling Requirements
### 3.1 Linting (Required)
- ESLint is required for code-quality rules.
- Use the Airbnb base configuration.
- If ESLint formatting rules conflict with Prettier, disable the conflicting rules in ESLint.
 - Command:
```bash
eslint .
```

### 3.2 Formatting (Required)
- Prettier is required for formatting; do not hand-format against formatter output.
 - Command:
```bash
prettier --check .
```

### 3.3 Editor (Recommended)
- Visual Studio Code with ESLint, Prettier, and Better Comments.

**Prettier configuration (example)**
```json
{
    "useTabs": false,
    "tabWidth": 4,
    "semi": true,
    "singleQuote": true,
    "trailingComma": "es5",
    "bracketSpacing": true
}
```

**ESLint configuration (example for .eslintrc.cjs)**
```javascript
module.exports = {
    env: {
        browser: true,
        es2021: true,
        node: true
    },
    extends: ["airbnb-base"]
}
```

## 4. Formatting (Rationale)
- Indentation: 4 spaces; no tabs (Prettier: `tabWidth: 4`, `useTabs: false`).
- Semicolons are required.
- Use single quotes for JavaScript strings.
- Use trailing commas where supported.
- Rationale: consistent formatting reduces review friction and formatter conflicts.

## 5. Naming (Rationale)
- Variables and functions: camelCase.
- Classes and constructors: PascalCase.
- Constants: UPPER_SNAKE.
- Filenames: kebab-case.
- Rationale: consistent naming improves readability and searchability.

**Naming Table**

| Element         | Convention   | Example                 |
| --------------- | ------------ | ----------------------- |
| Constant        | UPPER_SNAKE  | `const MAX_RETRY = 5;`  |
| Variable        | camelCase    | `let configFile = '…';` |
| Function        | camelCase    | `validateInput()`       |
| Class/constructor | PascalCase | `class UserService {}`  |
| Module filename | kebab-case   | `user-service.js`       |

## 6. Structure and Organization
- One module per file; classes live in their own files.
- Prefer ES modules (`import` / `export`) over CommonJS.
- Order code blocks: imports, constants, functions, exports.
- Avoid global variables; pass dependencies explicitly.

## 7. JavaScript Rules
- Use `const` by default, `let` only when reassignment is required; never use `var`.
- Use strict equality (`===`, `!==`).
- Use 1TBS brace style; opening brace on the same line.
- Use spaces around operators and after commas.
- Prefer arrow functions for callbacks; do not use arrows for methods that rely on `this`.
- Prefer `async`/`await` over raw Promise chains.
- Use template literals for interpolation.
- Avoid implicit type coercion; use explicit conversions.
- Avoid `eval` and `new Function`.
- Put each object property on its own line when objects span multiple lines.

## 8. Security and Safety (Rationale)
- Validate and sanitize all external input.
- Do not insert untrusted content via `innerHTML`; use `textContent` or a trusted sanitizer.
- Rationale: reduce injection risk and unsafe runtime behavior.

## 9. Documentation and Comments
- Use JSDoc block comments for public functions and complex logic.
- Use line comments sparingly; avoid trailing inline comments after code.

**JSDoc example**
```javascript
/**
 *
 * !Alert.
 * ?Questions.
 * *Important.
 * TODO: Things.
 * Description: Things.
 * @function nameFunction This functions does x1 and x2 things.
 * @param {array|number|string|boolean|int|float|*} myParam This parameter does x1 and/or x2 things.
 *
 * Tag order if apply.
 * Tags available should be declared in the following order:
 *
 * @action
 * @global
 * @typedef
 * @constant
 * @let
 * @var
 * @name
 * @namespace
 * @constructor
 * @callback
 * @event
 * @function
 * @augments
 * @lends
 * @type
 * @prop
 * @param
 * @return
 * @throws
 * @fires
 * @listens
 * @ingroup
 * @deprecated
 * @see
 * @ignor
 * @condition
 * @return {type} Return value description.
 *
 */
```

## 10. Testing and Verification
- ESLint must pass; Prettier checks must pass.
- Unit tests are required where business logic exists.

## 11. Appendix A: References
- ECMA-262 (ECMAScript) - https://tc39.es/ecma262/2023/multipage/ (Accessed 2026-01-15)
- Airbnb JavaScript Style Guide - https://github.com/airbnb/javascript (Accessed 2026-01-15)
- ESLint - https://eslint.org/ (Accessed 2026-01-15)
- Prettier - https://prettier.io/docs/configuration (Accessed 2026-01-15)
