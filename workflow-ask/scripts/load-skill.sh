#!/bin/bash
# load-skill.sh - Verify the workflow-ask package is loadable.
#
# License: MIT
# Part of: workflow-ask
#
# Read-only. Does not modify the skill tree.
# SPDX-License-Identifier: MIT

set -Eeuo pipefail
IFS=$'\n\t'

readonly SCRIPT_NAME="load-skill.sh"
readonly SCRIPT_VERSION="1.1.0"
readonly EXIT_OK=0
readonly EXIT_FAIL=1
readonly EXIT_USAGE=2
readonly EXPECTED_NAME="workflow-ask"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
SKILL_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd -P)"
readonly SCRIPT_DIR SKILL_ROOT

# Print GNU-style help to stdout.
# Globals: SCRIPT_NAME
# Arguments: none
# Outputs: help text on stdout
# Returns: none
print_help() {
  cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS]... SKILL_NAME

Verify this skill package can be loaded. SKILL_NAME must equal the
frontmatter name (${EXPECTED_NAME}). Analogous to
skills.load_skill({"skill_name": "${EXPECTED_NAME}"}).

Options:
  -h, --help      Show this help and exit.
  -V, --version   Print version and exit.

Exit status:
  0  Package is loadable.
  1  Package failed validation.
  2  Usage error.

Examples:
  ${SCRIPT_NAME} ${EXPECTED_NAME}
EOF
}

# Print version to stdout.
# Globals: SCRIPT_NAME, SCRIPT_VERSION
# Arguments: none
# Outputs: version line on stdout
# Returns: none
print_version() {
  printf '%s %s\n' "${SCRIPT_NAME}" "${SCRIPT_VERSION}"
}

# Abort with a usage error.
# Globals: none
# Arguments: $* diagnostic
# Outputs: FAIL line and help on stderr
# Returns: exits EXIT_USAGE
die_usage() {
  printf 'FAIL: %s\n' "$*" >&2
  print_help >&2
  exit "${EXIT_USAGE}"
}

# Abort with a load failure.
# Globals: none
# Arguments: $* diagnostic
# Outputs: FAIL line on stderr
# Returns: exits EXIT_FAIL
die_fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit "${EXIT_FAIL}"
}

# Map allowlisted long options to short flags.
# Globals: none
# Arguments: $1 nameref, remaining original argv
# Outputs: none
# Returns: 0
normalize_argv() {
  local -n _out=$1
  shift
  local seen_dd=0
  _out=()
  while [ "${#}" -gt 0 ]; do
    if [ "${seen_dd}" -eq 1 ]; then
      _out+=("$1")
      shift
      continue
    fi
    case "$1" in
      --)
        seen_dd=1
        _out+=("$1")
        ;;
      --help)
        _out+=(-h)
        ;;
      --version)
        _out+=(-V)
        ;;
      *)
        _out+=("$1")
        ;;
    esac
    shift
  done
}

# Validate SKILL.md frontmatter and required files.
# Globals: SKILL_ROOT, SCRIPT_DIR, EXPECTED_NAME
# Arguments: $1 expected skill name
# Outputs: OK line on stdout
# Returns: EXIT_OK / EXIT_FAIL
validate_package() {
  local want_name=$1
  local skill_md="${SKILL_ROOT}/SKILL.md"
  local validator="${SCRIPT_DIR}/validate-question-set.py"
  local example="${SKILL_ROOT}/assets/question-set.example.json"
  local schema="${SKILL_ROOT}/schemas/question-set.schema.json"
  local channel="${SKILL_ROOT}/references/question-channel.md"
  local parsed

  [ "${want_name}" = "${EXPECTED_NAME}" ] \
    || die_fail "requested '${want_name}' but this package is ${EXPECTED_NAME}"
  [ -f "${skill_md}" ] || die_fail "missing SKILL.md"
  [ -f "${channel}" ] || die_fail "missing references/question-channel.md"
  [ -f "${example}" ] || die_fail "missing assets/question-set.example.json"
  [ -f "${schema}" ] || die_fail "missing schemas/question-set.schema.json"
  [ -f "${validator}" ] || die_fail "missing scripts/validate-question-set.py"
  [ -x "${validator}" ] \
    || die_fail "scripts/validate-question-set.py is not executable"

  command -v python3 >/dev/null 2>&1 \
    || die_fail "python3 is required to parse SKILL.md"

  parsed="$(
    python3 - "${skill_md}" "${want_name}" "${SKILL_ROOT}" <<'PY'
import sys
from pathlib import Path

skill_md, want_name, skill_root = sys.argv[1], sys.argv[2], sys.argv[3]
text = Path(skill_md).read_text(encoding="utf-8")
if not text.startswith("---"):
    print("FAIL: SKILL.md missing YAML frontmatter", file=sys.stderr)
    sys.exit(1)
end = text.find("\n---", 3)
if end < 0:
    print("FAIL: SKILL.md frontmatter not closed", file=sys.stderr)
    sys.exit(1)
try:
    import yaml
except ImportError:
    print("FAIL: PyYAML is required to parse SKILL.md", file=sys.stderr)
    sys.exit(1)
data = yaml.safe_load(text[4:end])
if not isinstance(data, dict):
    print("FAIL: SKILL.md frontmatter is not a mapping", file=sys.stderr)
    sys.exit(1)
name = data.get("name")
desc = data.get("description")
if not isinstance(name, str) or not name:
    print("FAIL: name is required", file=sys.stderr)
    sys.exit(1)
if name != want_name:
    print(
        f"FAIL: requested '{want_name}' but SKILL.md name is '{name}'",
        file=sys.stderr,
    )
    sys.exit(1)
dir_name = Path(skill_root).name
if name != dir_name:
    print(
        f"FAIL: name '{name}' does not match directory '{dir_name}'",
        file=sys.stderr,
    )
    sys.exit(1)
if not all(c.islower() or c.isdigit() or c == "-" for c in name):
    print(
        "FAIL: name must be lowercase alphanumeric plus hyphens",
        file=sys.stderr,
    )
    sys.exit(1)
if name.startswith("-") or name.endswith("-") or "--" in name:
    print("FAIL: invalid name hyphens", file=sys.stderr)
    sys.exit(1)
if len(name) > 64:
    print("FAIL: name exceeds 64 characters", file=sys.stderr)
    sys.exit(1)
if not isinstance(desc, str) or not desc.strip():
    print("FAIL: description is required", file=sys.stderr)
    sys.exit(1)
collapsed = " ".join(desc.split())
if len(collapsed) > 1024:
    print("FAIL: description exceeds 1024 characters", file=sys.stderr)
    sys.exit(1)
tools = data.get("allowed-tools")
if not isinstance(tools, list) or not tools:
    print("FAIL: allowed-tools must be a non-empty array", file=sys.stderr)
    sys.exit(1)
version = data.get("version") or ""
if not isinstance(version, str):
    version = str(version)
meta = data.get("metadata") or {}
if isinstance(meta, dict) and not version:
    version = str(meta.get("version") or "")
print(f"{name}\t{version}")
PY
  )" || exit "${EXIT_FAIL}"

  if ! python3 "${validator}" validate "${example}" >/dev/null; then
    die_fail "assets/question-set.example.json failed validate-question-set.py"
  fi

  local loaded_name loaded_version
  loaded_name="${parsed%%$'\t'*}"
  loaded_version="${parsed#*$'\t'}"

  printf 'OK: loaded %s' "${loaded_name}"
  if [ -n "${loaded_version}" ]; then
    printf ' v%s' "${loaded_version}"
  fi
  printf ' from %s\n' "${SKILL_ROOT}"
}

# Parse argv and load the package.
# Globals: SCRIPT_NAME
# Arguments: CLI argv
# Outputs: OK or FAIL diagnostics
# Returns: EXIT_OK / EXIT_FAIL / EXIT_USAGE
main() {
  local -a argv=()
  local opt

  normalize_argv argv "$@"
  if [ "${#argv[@]}" -gt 0 ]; then
    set -- "${argv[@]}"
  else
    set --
  fi

  while getopts ':hV' opt; do
    case "${opt}" in
      h)
        print_help
        exit "${EXIT_OK}"
        ;;
      V)
        print_version
        exit "${EXIT_OK}"
        ;;
      :)
        die_usage "option -${OPTARG} requires an argument"
        ;;
      \?)
        die_usage "unknown option -${OPTARG}"
        ;;
    esac
  done
  shift $((OPTIND - 1))

  if [ "${#}" -ge 1 ] && [ "$1" = "--" ]; then
    shift
  fi

  [ "${#}" -eq 1 ] || die_usage "exactly one SKILL_NAME is required"
  validate_package "$1"
  exit "${EXIT_OK}"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi

# NAME
# load-skill.sh - verify the workflow-ask package is loadable
#
# SYNOPSIS
# load-skill.sh [OPTIONS]... SKILL_NAME
#
# DESCRIPTION
# Parses SKILL.md frontmatter, checks required files, and validates
# assets/question-set.example.json. SKILL_NAME must match the
# frontmatter name and the parent directory.
#
# OPTIONS
# -h, --help     Print help and exit 0.
# -V, --version  Print version and exit 0.
#
# EXIT STATUS
# 0 success
# 1 package failed validation
# 2 usage error
#
# EXAMPLES
# load-skill.sh workflow-ask
#
# SEE ALSO
# validate-question-set.py, python3(1)
