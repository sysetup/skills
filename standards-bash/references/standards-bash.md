# Bash code conventions (Google-aligned)

This document defines Bash conventions for this repository. It is **aligned with the Google Shell Style Guide** and prioritizes security, maintainability, and operational safety.

---

## 1. Purpose and Scope
- Applies to all Bash scripts (`*.sh`) and executable shell utilities.
- For **new code**, follow this standard (Google-aligned) by default.
- For **existing files**, prefer consistency with the surrounding style, but do not introduce new violations (especially around quoting, safety, and error handling).

## 2. Normative Alignment
- **Upstream style baseline**: Google Shell Style Guide (see Appendix A).
- **Primary language reference**: GNU Bash Reference Manual.
- This document is the repository’s **operational standard** (deterministic and offline-friendly) and is intended to remain aligned with Google’s guidance.
- If a conflict with upstream is discovered, do **not** change repository behavior based on upstream drift alone; instead, update this document (and any tooling/config) via review so the standard stays reproducible.
- Prioritize: security, robustness, clarity, minimal viable code, and auditability.


## 3. Tooling Requirements
### 3.1 Editor (Recommended)
- Visual Studio Code with ShellCheck, Bash IDE, and Better Comments.

### 3.2 Linting (Required)
- ShellCheck must pass before every commit.
- Commands:
  - `shellcheck script.sh`
  - `find . -name "*.sh" -exec shellcheck {} +`

### 3.3 Formatting (Required)
- Use `shfmt` configured to **closely resemble Google’s style**.
- Commands:
- Check (no writes; preferred for verification/CI):
```bash
shfmt -i 2 -ci -bn -d script.sh
```
- Apply (writes file):
```bash
shfmt -i 2 -ci -bn -w script.sh
```

### 3.4 Testing (Recommended)
- Use bats for unit tests where feasible.

## 4. Formatting (Rationale)
- Indentation: 2 spaces, no tabs.
- Use tabs only for `<<-` heredocs (if needed).
- Maximum line length: 80 characters.
- Line endings: LF.
- One command per line; wrap long commands with `\` and indent continuations.
- Rationale: consistent diffs and deterministic tool output.

## 5. Naming (Rationale)
- Functions: lower_case_with_underscores.
- Variables: lower_case_with_underscores (prefer `local` inside functions).
- Constants and environment variables: UPPER_CASE_WITH_UNDERSCORES (declare constants with `readonly`).
- Filenames: lower_case_with_underscores.
- Rationale: predictable identifiers reduce cognitive load in audits.

**Naming Table**

| Element         | Convention   | Example                |
| --------------- | ------------ | ---------------------- |
| Constant        | UPPER_SNAKE  | `readonly MAX_RETRY=5` |
| Env var         | UPPER_SNAKE  | `export APP_ENV="prod"` |
| Variable        | snake_case   | `log_dir="$HOME/.local/state/mytool"` |
| Local variable  | snake_case   | `local retry_count=0` |
| Function        | snake_case   | `validate_input()` |
| Filename        | snake_case   | `install_tools.sh` |

- Avoid collisions: prefix exported env vars, constants, and unavoidable globals by project/module as scope grows (e.g., `MYTOOL_LOG_LEVEL="info"`).

## 6. Structure and Organization
- Declare globals at the top; prefer `readonly` for constants.
- Use a `main()` entrypoint and guard:
```bash
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
```
- Standard project layout:
```text
project/
├── bin/
├── lib/
├── config/
├── logs/
└── tests/
```
- Versioning: use Semantic Versioning and maintain `CHANGELOG.md`.

## 7. Bash Language Rules
- Shebang (executables): use `#!/bin/bash`.
- Do not use SUID/SGID shell scripts.
- File types:
  - Executables: prefer **no extension**; if using an extension, use `.sh`.
  - Libraries: must use `.sh` and must not be executable.
- Recommended safety defaults (security hardening):
```bash
set -Eeuo pipefail
IFS=$'\n\t'
```
- Assignment: no spaces around `=` (e.g., `var=value`, never `var = value`).
- Use `[[ ... ]]` for tests; always quote variables (`"$var"`).
- Use braces for concatenation/parameter expansion to avoid ambiguity (e.g., `"${var}suffix"`).
- Parameter expansion for safe defaults/validation (especially with `set -u`):
  - Default if unset/empty: `value="${VAR:-default}"`
  - Require non-empty (fail fast): `: "${VAR:?VAR is required}"`
  - Assign default if unset/empty: `: "${CACHE_DIR:="$HOME/.cache/mytool"}"`
- Use `$(...)` for command substitution; avoid backticks.
- Avoid `eval`, untrusted `source`, and `ls | while read` loops.
- If indirection is required, prefer Bash *namerefs* (Bash 4.3+):
```bash
set_var() {
  local -n ref="$1"
  ref="$2"
}
```
- Prefer arrays for lists; avoid word splitting.
- Arrays: iterate with `"${arr[@]}"` to preserve elements; avoid `"${arr[*]}"` except in tightly controlled cases.
- Special variables: always quote positional args (`"$1"`, `"$2"`), use `"$#"` for argc, prefer `"$@"` and avoid `"$*"`.
- Scope: declare variables inside functions as `local` unless a global is explicitly intended.
- CLI parsing: use `getopts` for flags; zero-arg should print usage.
- Language standard: All CLI messages, options descriptions, usage guides, error banners, and comments must be in English by default.
- Dependency checks:
```bash
command -v curl >/dev/null 2>&1 || {
  printf '%s\n' "Error: curl not installed." >&2
  exit 2
}
```
- Paths: avoid unanchored relative paths; anchor to script directory:
```bash
readonly BASE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
source "${BASE_DIR}/../lib/colors.sh"
```
- Error handling and exit codes:
```bash
exit 1  # general error
exit 2  # dependency missing
exit 3  # invalid input
```
```bash
abort() {
  printf '%s\n' "$1" >&2
  exit "${2:-1}"
}
```
- Logging (optional, non-sensitive):
- Prefer user-writable locations by default; use `/var/log/...` only for root-only tools that explicitly require system-wide logs.
- Use restrictive permissions (e.g., `umask 077`) and avoid logging secrets/PII.
```bash
umask 077
log_dir="${XDG_STATE_HOME:-"$HOME/.local/state"}/myscript"
mkdir -p -- "$log_dir"
log_file="${log_dir}/myscript.log"
printf '%s [INFO] %s\n' "$(date +%F_%T)" "message" >> "$log_file"
```

### Zero-Argument Safety:
- **Default to Help:** No script, binary, or module may execute actions simply by being called.
- If a user runs a tool without arguments, it must output a clear **Usage Guide** and list available parameters.
- If the tool has complex functionality, explicitly suggest using the `--help` or `-h` flag.

## 8. Security and Safety (Rationale)
- Validate all inputs with allowlists; fail fast on invalid data.
- Do not store secrets in scripts; use environment variables or external config with 0600 permissions.
- Require explicit confirmation before privileged actions; check UID when root is required.
- Use `mktemp` for temp files and atomic writes (write -> fsync -> rename).
- Use `trap` for cleanup and deterministic exits.

## 9. Documentation and Comments
- File header: include a short summary of purpose at top-of-file.
- Better Comments tags (when apply):
```bash
#* Description: {description_here}
#? Question: {questions_here}
#! Alert: {alerts_here}
#TODO: {todo_items_here}
```
- Function header comment (preferred):
```bash
# Does a thing.
# Globals:
#   FOO
# Arguments:
#   $1: input path
# Returns:
#   0 on success, non-zero on error
do_a_thing() {
  ...
}
```

## 10. Testing and Verification
- Support dry-run mode when feasible.
- Tests live under `tests/`; use bats where possible.
- Example:
```bash
@test "function does X" {
  run function_name arg1
  [ "$status" -eq 0 ]
}
```

## 11. Appendix A: References
- Google Shell Style Guide - https://google.github.io/styleguide/shellguide.html (Accessed 2026-01-18)
- GNU Bash Reference Manual - https://www.gnu.org/software/bash/manual/ (Accessed 2026-01-18)
- ShellCheck - https://github.com/koalaman/shellcheck (Accessed 2026-01-18)
- shfmt (mvdan/sh) - https://github.com/mvdan/sh (Accessed 2026-01-18)
