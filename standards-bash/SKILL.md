---
name: standards-bash
description: "Enterprise Bash standards + workflow; auto-trigger on Bash domain shift, multi-step Bash work, Bash refactoring, or system events requiring Bash automation expertise. Keywords: bash, shell scripting, bash refactor, shellcheck, shfmt, getopts."
metadata:
  short-description: Bash standards.
license: MIT
---

## 1. Skill Specification
*Defines the capabilities, requirements, and boundaries of this skill.*

### 1.1 Objective
*   **Purpose**: Apply the repository’s **MANDATORY** Bash rules, regulations, specifications, and standards (normative requirements) to produce secure, maintainable, auditable Bash code and reviews.
*   **Normative source (MANDATORY)**: `references/standards-bash.md` (this skill-local document is the authoritative standard for this skill; compliance is required and deviations must be explicitly justified and approved).
*   **Context (automatic activation)**: Use this skill whenever any of the following is true (even if the user does not request it explicitly):
    *   **Domain shift**: The conversation moves into specialized Bash/programming concerns where a generalist context is insufficient.
    *   **Task complexity**: The request requires a multi-step Bash workflow (state tracking, executions, verifications, creations) or Bash-specific constraints.
    *   **Role simulation**: The user asks the agent to “act as” / simulate a Bash specialist for a prolonged period.
    *   **System event response**: A concrete system event requires Bash automation expertise (triage, hardening, or corrective scripting).

### 1.2 Interface (Contract)
**Inputs (Parameters)**
| Name | Type | Description | Validation Rule |
| :--- | :--- | :--- | :--- |
| `request` | `STRING` | Desired Bash outcome (new script, refactor, review, bugfix) and constraints. | Non-empty; must not include secrets/PII; clarify OS/target environment if relevant. |
| `repo_paths` | `FILE/LIST` | Target files/dirs inside the repository scope. | Relative paths only; must stay within the current repo; reject `..` traversal and absolute paths. |
| `needs_root` | `BOOL` | Whether the produced script is intended to require root privileges at runtime. | `true`/`false`; default `false` unless explicitly required. |

**Outputs (Deliverables)**
*   **Primary Artifact**: Bash code/doc changes compliant with the **MANDATORY** normative standard in `references/standards-bash.md`, with verification evidence (lint/format/tests as applicable).
*   **Success Signal**: `shellcheck` clean, `shfmt` idempotent, and any relevant tests pass; zero-argument behavior is safe (usage/help only).

### 1.3 Requirements
*   **Permissions**: Least privilege by default; require root only when the functionality truly demands it.
*   **Dependencies**:
    *   System: Debian (stable) with GNU userland; GNU Bash.
    *   Tools: `shellcheck` (required), `shfmt` (required), `git` (required); `bats` (recommended when tests exist).

### 1.4 Path resolution (Deterministic)
*Defines how to resolve skill-local file paths (references, scripts, assets) for this skill.*

*   **Rule**: Resolve `SKILL_ROOT` as the directory containing this `SKILL.md`. Treat `REFERENCES_DIR="${SKILL_ROOT}/references"`, `SCRIPTS_DIR="${SKILL_ROOT}/scripts"`, and `ASSETS_DIR="${SKILL_ROOT}/assets"` as skill-local roots (do not assume the process `cwd`).
*   **Constraint**: Treat any `references/...`, `scripts/...`, `assets/...` paths in this document as relative to `SKILL_ROOT`. Do not hardcode machine-specific absolute paths (e.g., `$HOME/...`) for skill-local resources.
*   **Example derivation**:
    ```bash
    SKILL_MD_PATH="/abs/path/to/standards-bash/SKILL.md"
    SKILL_ROOT="$(cd -- "$(dirname -- "$SKILL_MD_PATH")" && pwd -P)"
    REFERENCES_DIR="${SKILL_ROOT}/references"
    SCRIPTS_DIR="${SKILL_ROOT}/scripts"
    ASSETS_DIR="${SKILL_ROOT}/assets"
    ```

---

## 2. Operational Workflow
*The standardized process for executing this skill. Follow this workflow linearly.*

### Phase 0: Initialization (Pre-Flight)
*Objective: Ensure safety and readiness before any changes.*

1.  **Scope gate**:
    *   Action: Operate only within the repository working directory and its subdirectories.
2.  **Load the normative standard**:
    *   Action: Treat `references/standards-bash.md` as the **MANDATORY** authoritative rules/regulations/specifications/standards for Bash style and safety in this skill.
3.  **Risk/correctness pass (mini threat model)**:
    *   Identify trust boundaries: CLI args, environment variables, file inputs, network inputs, and privilege boundaries.
    *   Decide whether `needs_root=true` is truly required; default to `false`.
4.  **Define acceptance criteria**:
    *   Standards conformance: changes satisfy all applicable requirements in `references/standards-bash.md`.
    *   Lint: `shellcheck` on all modified/added `.sh` files.
    *   Format: verify with `shfmt -i 2 -ci -bn -d` (no diff); apply with `shfmt -i 2 -ci -bn -w` only when ready to accept changes.
    *   Tests: run existing tests when present (e.g., `bats`) for impacted behaviors.
5.  **Zero-argument and privilege gating constraints**:
    *   Zero-arg invocation must not perform actions; it must print usage/help (except root-gated tools below).
    *   If `needs_root=true`: implement **root-first gating** (check `EUID` immediately; if not root, print `Unauthorized` and exit; do not show help/capabilities when unauthorized).
    *   Note: root-first gating reduces UX/discoverability by design; rationale is minimizing capability disclosure across privilege boundaries.

### Phase 1: Execution (The Core Maneuver)
*Objective: Implement the smallest safe change that meets the request.*

**Step 1.1: Apply Bash safety and structure**
*   Action:
    *   Use safe defaults (`set -Eeuo pipefail` and `IFS=$'\n\t'`), strict quoting, arrays over word-splitting, and avoid `eval`.
    *   Use a `main()` entrypoint with a guard (`[[ "${BASH_SOURCE[0]}" == "$0" ]]`) for libraries.
    *   Validate all externally influenced inputs (args/env/file content) with allowlists and fail fast on first error.
    *   Prefer deterministic exit codes (e.g., invalid input vs missing dependency).

**Step 1.2: Enforce safe CLI behavior**
*   Action:
    *   Implement `-h`/`--help` and document usage and examples.
    *   Language standard: All CLI help outputs (-h/--help), usage guides, parameter descriptions, error banners, and interactive prompts must be written in English by default.
    *   Zero-arg: usage only (no side effects).
    *   If `needs_root=true`: enforce root-first gating before parsing args/help to avoid leaking capabilities to unauthorized users.

**Step 1.3: Safe filesystem and networking patterns (when applicable)**
*   Action:
    *   Temp files: use `mktemp`; cleanup with `trap`.
    *   Writes: use atomic writes when replacing files (write → fsync where feasible → rename).
    *   Networking: explicit timeouts/retries; TLS verification on; avoid silent fallbacks.

### Phase 2: Verification (Quality Control)
*Objective: Prove the change is correct, formatted, and safe.*

1.  **Lint**
    *   Run: `shellcheck <touched-script>.sh` (or repo batch lint when appropriate).
    *   Expect: zero findings, or explicitly justified suppressions with a narrow scope and rationale.
2.  **Format**
    *   Run (non-mutating check): `shfmt -i 2 -ci -bn -d <touched-script>.sh` and review the diff.
    *   Apply (mutating): `shfmt -i 2 -ci -bn -w <touched-script>.sh` when ready to accept changes.
    *   Expect: after applying, `shfmt -d` output is empty (idempotent formatting).
3.  **Behavioral checks**
    *   Validate: `--help` output and zero-arg behavior.
    *   If `needs_root=true`: validate unauthorized behavior (`Unauthorized` + exit) and authorized behavior (usage/help allowed).
4.  **Tests (if present)**
    *   Run the narrowest relevant tests first; expand only as needed.

### Phase 3: Finalization
*Objective: Deliver an auditable change with a clear handoff.*

1.  **Documentation**: Update or add concise usage/examples and failure modes for any new/changed script behavior.
2.  **Change hygiene**: Keep diffs small, single-responsibility, and reviewable.
3.  **Record**: Provide validation commands and outcomes (lint/format/tests) for reproducibility.

---

## 3. Exception Handling (Circuit Breakers)
*Protocols for when the workflow deviates from the happy path.*

| Trigger Event | Severity | Response Protocol |
| :--- | :--- | :--- |
| `INPUT_AMBIGUOUS` | `MEDIUM` | **Stop** and ask clarifying questions; do not guess behavior or invent interfaces. |
| `MISSING_DEPENDENCY` | `HIGH` | **Abort** with a clear dependency list and install guidance (no unsafe curl-pipe installs). |
| `SHELLCHECK_FAIL` | `HIGH` | **Fix** findings; only suppress narrowly with justification when unavoidable. |
| `PRIVILEGE_BOUNDARY_UNCLEAR` | `HIGH` | **Default to non-root**; require explicit confirmation before designing a root-required tool. |
| `DESTRUCTIVE_OPERATION_REQUESTED` | `CRITICAL` | **Require explicit user confirmation**, add dry-run, and implement state detection/idempotency first. |

### Rollback Procedure
*Execute immediately if **Abort** is triggered after partial changes.*

1.  **Stop**: Ensure no processes are left running and no temp files remain (cleanup via `trap` where used).
2.  **Undo**: Manually revert the working tree changes for the files touched by this task (avoid history rewriting).
3.  **Verify**: Re-run Phase 2 checks to confirm the repo returns to the pre-change baseline.

---

## 4. Security & Compliance
*   **Data Privacy**: Do not request/store/paste secrets or PII; redact sensitive values from logs and examples; use placeholders.
*   **Auditability**: Prefer small patches; deterministic commands; explicit exit codes; clear failure messages without leaking sensitive details.
*   **Least Privilege**: Avoid root by default; when root is required, enforce root-first gating and minimize privileged surface area.
*   **Safe defaults**: Zero-arg must be non-destructive; no silent network bypasses; deny-by-default where possible.
