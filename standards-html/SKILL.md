---
name: standards-html
description: "Enforce HTML standards when authoring/refactoring/reviewing *.html (keywords: html, *.html, a11y, accessibility, prettier, vnu) using the canonical ruleset in `references/html-standards.md`."
metadata:
  author: "SYSETUP.COM CarlosHRG"
  short-description: HTML standards
license: MIT
---

## 1. Skill Specification
*Defines the capabilities, requirements, and boundaries of this skill.*

### 1.1 Objective
*   **Purpose**: Ensure all generated/modified HTML complies with the canonical standard at `references/html-standards.md`.
*   **Context**: Used when authoring, refactoring, or reviewing HTML (`*.html`) in this repository/workspace, especially under the automatic activation conditions in §1.5.

### 1.2 Interface (Contract)
**Inputs (Parameters)**
| Name | Type | Description | Validation Rule |
| :--- | :--- | :--- | :--- |
| `paths` | `STRING` | Space-separated repo-relative file/dir paths to process (no whitespace in any path token). | Must not be absolute; must not contain `..`; must not contain whitespace; after `realpath -P`, must remain within `WORKSPACE_ROOT`; files must be `*.html`. |
| `intent` | `ENUM` | Operation mode. | Must be one of: `author`, `refactor`, `review`. |

**Outputs (Deliverables)**
*   **Primary Artifact**: HTML changes that conform to `references/html-standards.md`.
*   **Success Signal**: No standard violations remain; when tooling is available, Nu HTML Checker reports zero errors and formatting matches Prettier.

### 1.3 Requirements
*   **Permissions**: No elevated privileges required. Operate only within the current workspace.
*   **Dependencies**:
    *   Canonical standard (required): `references/html-standards.md`.
    *   Tooling (required by the standard when available in your toolchain): Prettier; Nu HTML Checker.

### 1.4 Path resolution (Deterministic)
*Defines how to resolve skill-local file paths (references, scripts, assets) for this skill.*

*   **Rule**: Resolve `SKILL_ROOT` as the directory containing this `SKILL.md`. Treat `REFERENCES_DIR="${SKILL_ROOT}/references"`, `SCRIPTS_DIR="${SKILL_ROOT}/scripts"`, and `ASSETS_DIR="${SKILL_ROOT}/assets"` as skill-local roots (do not assume the process `cwd`).
*   **Constraint**: Treat any `references/...`, `scripts/...`, `assets/...` paths in this document as relative to `SKILL_ROOT`. Do not hardcode machine-specific absolute paths (e.g., `$HOME/...`) for skill-local resources.
*   **Workspace boundary**: Define `WORKSPACE_ROOT` as the workspace root for `paths` (prefer an environment/harness-provided root; else, if in a Git repo, use `git rev-parse --show-toplevel`; else use `pwd -P`). Resolve each candidate target with `realpath -P` and abort if it does not remain within `WORKSPACE_ROOT` (symlink escape prevention).
*   **Example derivation**:
    ```bash
    SKILL_MD_PATH="/abs/path/to/standards-html/SKILL.md"
    SKILL_ROOT="$(cd -- "$(dirname -- "$SKILL_MD_PATH")" && pwd -P)"
    REFERENCES_DIR="${SKILL_ROOT}/references"
    SCRIPTS_DIR="${SKILL_ROOT}/scripts"
    ASSETS_DIR="${SKILL_ROOT}/assets"
    ```

### 1.5 Automatic activation (Mandatory)
This skill must be activated automatically (even if the user does not request it explicitly) when any of the following conditions are met:

1.  **Domain shift**: The conversation moves into a specialized Hypertext Markup Language (HTML) domain where generic guidance is insufficient.
2.  **Task complexity**: The request requires a multi-step workflow needing a dedicated HTML specialist to track state/flow/execution/verification/constraints.
3.  **Role simulation**: The user asks to “act as” or “simulate” a sustained HTML-specialist role for a prolonged period.
4.  **Event response**: A specific system event requires an HTML specialist response.

---

## 2. Operational Workflow
*The standardized process for executing this skill. This workflow must be followed linearly.*

### Phase 0: Initialization (Pre-Flight)
*Objective: Ensure safety and readiness before action.*

1.  **Path resolution**:
    *   Action: Resolve `SKILL_ROOT` and derived dirs per §1.4 (never assume the process `cwd`).
2.  **Load canonical rules**:
    *   Requirement: `${REFERENCES_DIR}/html-standards.md` must exist and is authoritative for this skill.
3.  **Scope gate (deny-by-default)**:
    *   Action: Ensure `paths` are workspace-local, contain no traversal (`..`), contain no whitespace, and target only `*.html`.
    *   Action: Resolve each path via `realpath -P` (from `WORKSPACE_ROOT`) and abort if any resolved target is outside `WORKSPACE_ROOT` (symlink escape).
4.  **Tooling check (best-effort, no network)**:
    *   Prettier (if present): `npx --no-install prettier -v` or `prettier -v`
    *   Nu HTML Checker (if present): `vnu --version` or `java -version` (for `vnu.jar` workflows)
    *   If tooling is unavailable: proceed with standards-based review, but do not claim full tooling verification.

### Phase 1: Execution (The Core Maneuver)
*Objective: Apply the standard to author/refactor/review HTML.*

**Step 1.1: Apply the canonical standard**
*   **Action**: Use `${REFERENCES_DIR}/html-standards.md` as a checklist. Do not invent additional rules; if external sources conflict, follow the canonical standard.
*   **Minimum requirements** (non-exhaustive; see canonical standard for full rules):
    *   Use `<!doctype html>` and a complete document structure with `<html lang="...">`.
    *   Prefer semantic elements; ensure valid nesting/hierarchy.
    *   Accessibility: `alt` on images; labels for form controls.
    *   Naming: `id`/`class` are kebab-case; `id` is unique; prefer `data-*` for JS hooks.
    *   Avoid inline styles and inline event handlers.
    *   Security: never inject untrusted HTML; use `rel="noopener"` (and `noreferrer` when needed) with `target="_blank"`.

**Step 1.2: Formatting (if toolchain is available)**
*   **Action**: Format with Prettier (required by the standard when available).
*   **Example**:
    ```bash
    npx --no-install prettier --write --log-level warn -- "*.html"
    ```

**Step 1.3: Validation (if toolchain is available)**
*   **Action**: Validate markup with Nu HTML Checker (required by the standard when available).
*   **Example** (binary on PATH):
    ```bash
    vnu --errors-only -- "*.html"
    ```
*   **Example** (`vnu.jar` via env var):
    ```bash
    java -jar "${VNU_JAR:?set VNU_JAR to the vnu.jar path}" --errors-only -- "*.html"
    ```

### Phase 2: Verification (Quality Control)
*Objective: Prove the output conforms to the canonical standard.*

1.  **Standards check**:
    *   Verify against `${REFERENCES_DIR}/html-standards.md` with special attention to semantics, accessibility, and security rules.
2.  **Tooling confirmation (when available)**:
    *   Ensure Prettier produces no further changes.
    *   Ensure Nu HTML Checker reports zero errors.

### Phase 3: Finalization
*Objective: Return a clear, auditable outcome.*

1.  **Report**:
    *   Summarize which files were changed and what standard sections were applied.
    *   Explicitly state whether Prettier and Nu HTML Checker were run (and on what targets).
2.  **Cleanup**:
    *   Remove any temporary files created by the workflow.

---

## 3. Exception Handling (Circuit Breakers)
*Protocols for when the workflow deviates from the happy path.*

| Trigger Event | Severity | Response Protocol |
| :--- | :--- | :--- |
| `MISSING_CANONICAL_STANDARD` | `HIGH` | **Abort**: `${REFERENCES_DIR}/html-standards.md` is required; do not proceed without it. |
| `OUT_OF_SCOPE_PATH` | `HIGH` | **Abort**: Reject absolute paths, traversal, and non-`*.html` targets. |
| `PATH_ESCAPES_WORKSPACE` | `HIGH` | **Abort**: Reject any path that resolves (via `realpath -P`) outside `WORKSPACE_ROOT` (including symlink escape). |
| `TOOLING_UNAVAILABLE` | `MEDIUM` | **Warn**: Continue standards-based review; do not claim tooling verification. Ask the user to provide/enable the toolchain. |
| `VALIDATION_ERRORS` | `HIGH` | **Fix**: Correct markup/accessibility/security issues, then re-run validation where available. |

### Rollback Procedure
1.  **Principle**: Prefer a follow-up, reviewed change that restores the prior state; do not rewrite history.
2.  **Action**: Record the rollback intent and rationale in your change-control/PR workflow, then apply the minimal revert via standard VCS practices.

---

## 4. Security & Compliance
*   **No secrets / PII**: Do not embed credentials, tokens, or sensitive identifiers in HTML (including comments).
*   **XSS risk**: Treat any user-controlled content as untrusted; sanitize/encode before rendering; do not “string-build” HTML from untrusted input.
*   **Tab-nabbing**: Use `rel="noopener"` (and `noreferrer` when needed) with `target="_blank"`.
*   **Least privilege**: This skill does not require root; do not request elevated privileges.
*   **No network by default**: Do not fetch toolchains/config at runtime; only use repository-provided or user-approved tooling.

---

## 5. References (Skill-Local)
*   Canonical standard: `references/html-standards.md`
