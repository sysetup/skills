---
name: standards-css
description: "Enforce CSS conventions via references/css-standards.md. Use for *.css changes, CSS lint/format, naming (kebab-case), selector specificity/!important, @import safety, theming/layout regressions, or when invoked as $standards-css."
metadata:
  short-description: CSS standards.
license: MIT
---

## 1. Skill Specification
*Defines the capabilities, requirements, and boundaries of this skill.*

### 1.1 Objective
*   **Purpose**: Provide a deterministic, security-conscious workflow for authoring, reviewing, and validating CSS changes according to this repository’s CSS standard.
*   **Context**: Used when CSS expertise is required and a generalist approach is insufficient.

**Auto-activation triggers (mandatory)**
This skill must be activated automatically when any of the following is true:
1. **Domain shift**: The conversation moves into specialized CSS/styling or CSS-adjacent markup/programming decisions where generic guidance is insufficient.
2. **Task complexity**: The request requires a multi-step CSS workflow (e.g., design → implement → lint/format → verify → iterate) that benefits from a dedicated, stateful CSS specialist.
3. **Role simulation**: The user asks to “act as” / “simulate” a CSS specialist for an extended period.
4. **Event response**: A concrete system event requires CSS expertise (e.g., theming regressions, layout breakages, critical UI visibility/accessibility issues caused by CSS).

**Activation keywords (non-exhaustive)**
Trigger this skill when the user mentions any of:
- `$standards-css`
- `standards-css` / `css standards`
- `stylelint`
- `prettier`
- `lint css` / `format css`
- `kebab-case` / `selector specificity` / `!important` / `@import`

### 1.2 Interface (Contract)
**Inputs (Parameters)**
| Name | Type | Description | Validation Rule |
| :--- | :--- | :--- | :--- |
| `mode` | `STRING` | Operation mode: `audit`, `fix`, or `guide`. | Must be one of: `audit`, `fix`, `guide`. |
| `targets` | `STRING` | Whitespace-separated CSS file paths or glob patterns to operate on. | Required for `audit`/`fix`; must not contain `..`; must not start with `/`; must target `*.css` only. |

**Outputs (Deliverables)**
*   **Primary Artifact**: CSS changes (if `fix`), plus a concise validation report aligned to the repository’s CSS standard.
*   **Success Signal**: Changes conform to `CSS_STANDARD_MD`; if optional tooling (e.g., Prettier/Stylelint) is used, it completes with exit code `0`, or explicit failure reasons with safe next steps.

### 1.3 Requirements
*   **Permissions**: Non-root user with write access to the working tree; do not require `sudo`.
*   **Skill license**: MIT (SPDX: `MIT`).
*   **Normative standard**: `references/css-standards.md` is the authoritative CSS standard for this skill.
*   **Dependencies** (optional, not auto-installed):
    *   Tools: `stylelint` and/or `prettier` available via the project toolchain or `PATH` (if used).
    *   Environment: GNU userland on Debian (or compatible).
*   **Documentation verification (Context7)** (optional): Use Context7 when necessary or if the user requests it, especially when inconsistencies are observed and/or official documentation verification is required (CSS specs, Stylelint, Prettier).

### 1.4 Path resolution (Deterministic)
*Defines how to resolve skill-local file paths (references, scripts, assets) for this skill.*

*   **Rule**: Resolve `SKILL_ROOT` as the directory containing this `SKILL.md`. Treat `REFERENCES_DIR="${SKILL_ROOT}/references"`, `SCRIPTS_DIR="${SKILL_ROOT}/scripts"`, and `ASSETS_DIR="${SKILL_ROOT}/assets"` as skill-local roots (do not assume the process `cwd`).
*   **Standard location**: Resolve the bundled standard as `CSS_STANDARD_MD="${REFERENCES_DIR}/css-standards.md"`.
*   **Example derivation**:
    ```bash
    SKILL_MD_PATH="/abs/path/to/standards-css/SKILL.md"
    SKILL_ROOT="$(cd -- "$(dirname -- "$SKILL_MD_PATH")" && pwd -P)"
    REFERENCES_DIR="${SKILL_ROOT}/references"
    SCRIPTS_DIR="${SKILL_ROOT}/scripts"
    ASSETS_DIR="${SKILL_ROOT}/assets"

    CSS_STANDARD_MD="${REFERENCES_DIR}/css-standards.md"
    ```

---

## 2. Operational Workflow
*The standardized process for executing this skill. Follow this workflow linearly.*

### Primary Checklist (Authoritative)
*Use this checklist as the primary standard for reviews. If any item is unclear, consult `CSS_STANDARD_MD` directly.*

- [ ] Tooling (optional): run Prettier + Stylelint (do not auto-install).
- [ ] Formatting: 4 spaces (no tabs); one declaration per line; trailing semicolons; lowercase hex; group declarations (Positioning, Box Model, Color, Text, Other).
- [ ] Naming: class/id/custom properties use kebab-case; semantic names; avoid abbreviations.
- [ ] Structure: order selectors element → id → class; keep related rules together; isolate utilities in a dedicated file/section.
- [ ] CSS rules: avoid `!important` (except documented legacy overrides); prefer CSS custom properties; keep specificity low/consistent; use shorthand only when it improves clarity.
- [ ] Security: avoid inline styles for untrusted content; avoid `@import` from untrusted sources.
- [ ] Comments: use block comments for section headers and non-obvious rules.
- [ ] Verification: diff stays minimal and request-aligned; if tooling is used, it exits with code `0`; validate in CI where available.

### Phase 0: Initialization (Pre-Flight)
*Objective: Ensure safety and readiness before action.*

1.  **Path resolution**:
    *   Resolve `SKILL_ROOT` and `CSS_STANDARD_MD` per §1.4 (never assume the process `cwd`).
2.  **Standard availability**:
    *   Verify `CSS_STANDARD_MD` exists and is readable. If missing: abort and ask the user to provide the correct standard file path.
    *   Do not attempt to read/compare standards outside `SKILL_ROOT` unless the user explicitly provides the path and confirms it is in-scope.
3.  **Safety interlock (consultative)**:
    *   Before changing any file, outline the minimal proposed change set (files, intent, commands to run) and wait for user approval.
4.  **Input validation**:
    *   Reject `targets` that include traversal (`..`), absolute paths, or non-CSS targets.
    *   If `mode=guide`, `targets` may be empty; otherwise it must be non-empty.

### Phase 1: Execution (The Core Maneuver)
*Objective: Apply the repo standard to the requested CSS work.*

**Step 1.1: Optional formatting (Prettier)**
*   **Action**: Format the target CSS consistently. Prefer formatter output over manual formatting.
*   **Command/Action**:
    ```bash
    TARGETS="<targets>" # e.g. "src/**/*.css"
    prettier --write "$TARGETS"
    ```
*   **Constraint**: Do not introduce behavioral changes during formatting-only passes.

**Step 1.2: Optional lint (Stylelint)**
*   **Action**: Lint the target CSS against the standard configuration.
*   **Command/Action**:
    ```bash
    TARGETS="<targets>" # e.g. "src/**/*.css"
    stylelint "$TARGETS"
    ```
*   **Note**: If the project uses a different invocation (e.g., via a package manager script), use that, but do not install dependencies automatically.

**Step 1.3: Standard compliance review**
*   **Action**: Verify the change adheres to `CSS_STANDARD_MD`, including naming, structure, selector specificity, and safety rules.
*   **Observation**: Call out any intentional deviations explicitly (with rationale) and request confirmation.

### Phase 2: Verification (Quality Control)
*Objective: Prove the skill was executed correctly.*

1.  **Tool exit codes**:
    *   If tooling is used: ensure exit code is `0`, or capture and summarize the errors without leaking sensitive data.
2.  **Diff sanity**:
    *   Confirm the diff is minimal and consistent with the request (no unrelated refactors).
3.  **Safety check**:
    *   Verify no new external `@import` from untrusted sources is introduced.

### Phase 3: Finalization
*Objective: Produce an auditable handoff.*

1.  **Report**: Provide a compact report: changed files, commands run, and pass/fail status.
2.  **Handoff**: Suggest next validation steps in the consuming project (CI lint/format, UI smoke check).

---

## 3. Exception Handling (Circuit Breakers)
*Protocols for when the workflow deviates from the happy path.*

| Trigger Event | Severity | Response Protocol |
| :--- | :--- | :--- |
| `MISSING_CSS_STANDARD_MD` | `HIGH` | **Abort**: Ask the user to confirm the correct location of `CSS_STANDARD_MD` (default: `references/css-standards.md`). |
| `INVALID_TARGETS` | `MEDIUM` | **Abort**: Explain which validation rule failed; request corrected `targets`. |
| `MISSING_TOOLING` (`stylelint`/`prettier`) | `MEDIUM` | **Pause**: Ask whether to proceed in `guide` mode (no file writes), or provide the project’s pinned tool invocation. |
| `LINT_OR_FORMAT_FAILURE` | `LOW` | **Iterate**: Fix the reported issues (minimal changes), then re-run verification. |

### Rollback Procedure
1.  **Stop**: Do not apply further changes.
2.  **Contain**: Clearly identify which files were modified and why.
3.  **User-driven revert**: Ask the user to perform their preferred VCS rollback (this skill does not execute destructive/reversion commands).

---

## 4. Security & Compliance
*   **Data Privacy**: Do not add secrets/PII into CSS, comments, or file names. Treat UI strings/URLs as potentially sensitive.
*   **Audit Trail**: Keep changes reviewable (small diffs, explicit rationale for deviations, deterministic commands).
*   **Least Privilege**: Do not use `sudo` or root-only operations for CSS work.
*   **Supply-chain safety**: Avoid `@import` from untrusted sources; do not fetch remote dependencies as part of this skill.
