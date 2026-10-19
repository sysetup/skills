---
name: standards-javascript
description: Enforce JavaScript standards for authoring/refactoring/reviewing `*.js` and JavaScript snippets in docs; optional Prettier/ESLint verification; stop on config conflicts.
license: MIT
metadata:
  author: "SYSETUP.COM CarlosHRG"
  short-description: JavaScript standards.
  version: "1.0.0"
---

## 1. Skill Specification
*Defines the capabilities, requirements, and boundaries of this skill.*

### 1.1 Objective
*   **Purpose**: `Create, update, refactor, or review JavaScript code while enforcing every rule in the authoritative standard "references/standards/javascript-standards.md" (formatting, naming, structure, JS rules, security, and documentation).`
*   **Context**: Used when `any change request involves writing/editing JavaScript source (*.js) and/or embedding JavaScript code examples in documentation; file deletion policies are out of scope`.

### 1.2 Interface (Contract)
**Inputs (Parameters)**
| Name | Type | Description | Validation Rule |
| :--- | :--- | :--- | :--- |
| `repo_root` | `DIR` | `Target repository root (default: current working directory)` | `MUST_EXIST_DIR` |
| `operation` | `STRING` | `One of: create, update, refactor, review (read-only audit)` | `^(create|update|refactor|review)$` |
| `targets` | `LIST<PATH>` | `Files to create/modify/review (JS and/or docs)` | `NO_TRAVERSAL (".."), RELATIVE_TO repo_root` |
| `allow_config_create` | `BOOL` | `Allow creating missing ESLint/Prettier config files (default: false)` | `TRUE/FALSE` |
| `allow_config_modify` | `BOOL` | `Allow modifying existing configs if they conflict (default: false; must be explicitly approved)` | `TRUE/FALSE` |
| `verify_tools` | `BOOL` | `Final verification with Prettier/ESLint (default: true; no auto-install)` | `TRUE/FALSE` |

**Defaults and validation semantics (normative)**
*   `repo_root`: defaults to `.`.
*   `targets`: must be explicitly provided and must be non-empty; do not guess or expand scope implicitly.
*   `allow_config_create=false`, `allow_config_modify=false`, `verify_tools=true` unless explicitly set.
*   `MUST_EXIST_DIR`: path exists and is a directory.
*   `NO_TRAVERSAL ("..")`: reject any path containing `..` segments; reject absolute paths.
*   `RELATIVE_TO repo_root`: each target must resolve under `repo_root` after normalization.

**Outputs (Deliverables)**
*   **Primary Artifact**: `Updated JavaScript code and/or documentation snippets aligned to the JavaScript code conventions`.
*   **Success Signal**: `All rules in "references/standards/javascript-standards.md" are satisfied. If verify_tools==true and tools are installed, Prettier/ESLint verification passes; otherwise, report missing tools and mark tool-based verification as skipped.`

### 1.3 Requirements
*   **Permissions**: User must hold `REPO_WRITE_ACCESS` (no root required).
*   **Dependencies**:
    *   System: `Debian (stable) + bash`.
    *   Tools (verification; required by the standard): `prettier`, `eslint`.
*   **OpenAPI**: `N/A` (this skill does not define or expose an HTTP API).

---

## 2. Operational Workflow
*The standardized process for executing this skill. This workflow must be followed linearly.*

### Phase 0: Initialization (Pre-Flight)
*Objective: Ensure scope, safety, and tooling readiness before changing code.*

1.  **Load the authoritative standard**
    *   Reference: `references/standards/javascript-standards.md`
    *   Rule: This skill must not skip any rule in that document. If a rule cannot be proven by tooling, enforce it by review checklist.

2.  **Scope the change**
    *   Identify `targets` and classify each as:
        *   `JS_SOURCE`: `*.js`
        *   `DOC`: any doc containing JS snippets (e.g., `*.md`)
    *   For `DOC`, treat embedded JS snippets as first-class code: formatting, naming, and security rules still apply.

3.  **Safety interlock: config changes**
    *   If ESLint/Prettier config files exist and conflict with the standard:
        *   If `allow_config_modify != true`: stop and request explicit confirmation before modifying.
        *   If approved: modify only the minimum necessary keys to comply.
    *   Treat these as "existing config" (do not create duplicates without approval):
        *   ESLint: `.eslintrc.*`, `eslint.config.*`, `package.json` (`eslintConfig`)
        *   Prettier: `.prettierrc.*`, `prettier.config.*`, `package.json` (`prettier`)

4.  **Tooling presence check (no auto-install)**
    *   Only if `verify_tools == true`:
        *   Detect binaries (prefer local project binaries over global):
            *   Prettier: `./node_modules/.bin/prettier` else `prettier`
            *   ESLint: `./node_modules/.bin/eslint` else `eslint`
        *   If the resolved binary is repo-local (e.g., `./node_modules/.bin/*`), require explicit confirmation that the repository is trusted before executing.
        *   If missing, report that tools are not installed and skip tool-based verification (see **Exception Handling**).
    *   Do not auto-install, do not run `npx`, and do not fetch dependencies over the network.

5.  **Config creation (when missing)**
    *   If `allow_config_create == true` and configs are missing:
        *   Create Prettier config from `assets/templates/prettierrc.json` as `.prettierrc.json` in `repo_root`.
        *   Create ESLint config from `assets/templates/eslintrc.cjs` as `.eslintrc.cjs` in `repo_root` (extends `airbnb-base` then `prettier` to disable formatting-rule conflicts).
    *   If `allow_config_create != true`, do not create configs; report that verification may be incomplete.

### Phase 1: Execution (Authoring / Refactor)
*Objective: Make the requested code change while enforcing every standard rule during authoring.*

For each `JS_SOURCE` change:
1.  **Formatting & naming (author-time)**
    *   4 spaces, semicolons, single quotes, trailing commas where supported.
    *   Naming: camelCase variables/functions, PascalCase classes, UPPER_SNAKE constants, kebab-case filenames.

2.  **Structure & modules**
    *   One module per file; classes in their own files.
    *   Prefer ES modules (`import`/`export`) over CommonJS.
    *   Order code blocks: imports → constants → functions → exports.
    *   Avoid globals; pass dependencies explicitly.

3.  **JavaScript rules**
    *   `const` by default; `let` only when reassignment is required; never `var`.
    *   Strict equality (`===`, `!==`).
    *   1TBS braces; spaces around operators and after commas.
    *   Arrow functions for callbacks; avoid arrows for methods relying on `this`.
    *   Prefer `async`/`await`; use template literals for interpolation.
    *   Avoid implicit type coercion; use explicit conversions.
    *   Avoid `eval` / `new Function`.
    *   Multi-line objects: one property per line.

4.  **Security & safety**
    *   Validate and sanitize all external input.
    *   Do not insert untrusted HTML via `innerHTML`; use `textContent` or a trusted sanitizer.

5.  **Documentation**
    *   JSDoc blocks for public functions and complex logic; avoid trailing inline comments.

For each `DOC` change:
* Ensure any JS snippet follows the same formatting/security rules (especially input validation and avoiding unsafe `innerHTML` patterns).

### Phase 2: Verification (Quality Control)
*Objective: Prove compliance independently of implementation.*

1.  **Rule-by-rule checklist**
    *   Re-check every rule in `references/standards/javascript-standards.md` against modified/added JS and JS doc snippets.
    *   If a rule is not tool-checkable, record it as a reviewed item (do not omit).

2.  **Mandatory checklist (do not skip)**
    *   Scope: all changed `*.js` comply; all JS doc snippets comply.
    *   Normative alignment: if Airbnb/other guides conflict, follow the standard.
    *   Prettier config matches the standard example (`useTabs=false`, `tabWidth=4`, `semi=true`, `singleQuote=true`, `trailingComma="es5"`, `bracketSpacing=true`).
    *   ESLint uses Airbnb base and disables formatting conflicts with Prettier (extend `prettier` last or equivalent).
    *   Formatting: 4-space indentation, semicolons, single quotes, trailing commas where supported, spaces around operators/after commas, 1TBS braces.
    *   Naming: camelCase variables/functions, PascalCase classes, UPPER_SNAKE constants, kebab-case filenames.
    *   Structure: one module per file; classes in own files; ES modules; ordered blocks; no globals.
    *   JS rules: `const`/`let` (no `var`), `===`/`!==`, async/await, safe arrow usage, explicit conversions, no `eval`/`new Function`, multi-line objects one property per line.
    *   Security: validate/sanitize external input; avoid unsafe `innerHTML`.
    *   Documentation: JSDoc for public/complex logic; minimal line comments; no trailing inline comments.
    *   Testing: add/update unit tests where business logic exists.
    *   Editor (recommended): VS Code with ESLint, Prettier, Better Comments.

3.  **Prettier (if available)**
    *   Run from `repo_root` on `JS_SOURCE` targets only: `prettier --check <targets...>`
    *   Expect: exit code `0`.

4.  **ESLint (if available)**
    *   Run from `repo_root` on `JS_SOURCE` targets only: `eslint <targets...>`
    *   Expect: exit code `0`.

5.  **Testing (when business logic exists)**
    *   Ensure unit tests exist/updated where business logic is introduced or changed.

### Phase 3: Finalization
*Objective: Produce an auditable completion report.*

1.  **Report**
    *   List changed files.
    *   State whether configs were created/changed (and whether approval was required).
    *   Include Prettier/ESLint commands executed and exit codes (or missing-tool status).
2.  **Cleanup**
    *   Remove any temporary files created during verification (if any).

---

## 3. Exception Handling (Circuit Breakers)
*Protocols for when the workflow deviates from the happy path.*

| Trigger Event | Severity | Response Protocol |
| :--- | :--- | :--- |
| `prettier not found` | `MEDIUM` | **Stop verification** and report manual install commands. Continue authoring checklist-only. |
| `eslint not found` | `MEDIUM` | **Stop verification** and report manual install commands. Continue authoring checklist-only. |
| `Existing config conflicts with standard` | `HIGH` | **Abort** until `allow_config_modify == true` is explicitly approved. |
| `prettier/eslint exit != 0` | `HIGH` | **Fix** code/config issues; re-run checks; if unresolved, report exact failures. |

### Manual install guidance (do not auto-install)
* Provide the following commands (as applicable to the target repository):*
* Install tools (project-local dev dependencies) matching this skill’s templates:
  * `npm install --save-dev prettier eslint eslint-config-airbnb-base eslint-plugin-import eslint-config-prettier`
* Verify using local binaries:
  * `./node_modules/.bin/prettier --check <targets...>`
  * `./node_modules/.bin/eslint <targets...>`

### Rollback Procedure
*Execute immediately if **Abort** is triggered.*
1.  **Stop**: Do not modify existing ESLint/Prettier configs without explicit approval.
2.  **Revert**: If this skill created new config files and rollback is requested, remove the newly created `.prettierrc.json` and/or `.eslintrc.cjs`.
3.  **Verify**: Confirm the repository is back to the pre-change config state.

---

## 4. Security & Compliance
*   **Data Privacy**: Do not introduce secrets in code or docs; use environment variables or a secret manager (by reference) and redact logs/examples.
*   **Tool Execution**: Only run Prettier/ESLint when `verify_tools == true`; treat repo-local `./node_modules/.bin/*` as trusted code and do not execute it in untrusted repositories.
*   **Audit Trail**: Record checks executed (e.g., `prettier --check <targets...>`, `eslint <targets...>`) and outcomes in the final report.
*   **Least Privilege**: Do not require root; do not instruct global installs as a default.

---

## 5. Usage Examples
*Examples are illustrative; adapt parameters to the task while keeping the workflow deterministic.*

*   **Create a new JS module**
    *   `operation=create`
    *   `targets=["src/user-service.js"]`
    *   `allow_config_create=true`, `allow_config_modify=false`, `verify_tools=true`
*   **Refactor and update docs**
    *   `operation=refactor`
    *   `targets=["src/user-service.js","docs/api.md"]`
    *   `allow_config_create=true`, `allow_config_modify=false`, `verify_tools=true`
*   **Review-only audit (no changes)**
    *   `operation=review`
    *   `targets=["src/user-service.js"]`
    *   `verify_tools=true`
