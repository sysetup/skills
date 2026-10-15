#!/usr/bin/env bash
# ==============================================================================
# man_page_lookup.sh - Query installed man pages as sanitized plain text.
#
# License: MIT
# Part of: ops-man
# SPDX-License-Identifier: MIT
#
# Read-only CLI that validates inputs, sanitizes the man(1) execution
# environment, requires explicit dependencies, and returns deterministic exit
# codes for agent workflows.
# ==============================================================================

set -Eeuo pipefail
IFS=$'\n\t'

readonly SCRIPT_NAME="man_page_lookup.sh"
readonly SCRIPT_VERSION="1.2.1"
readonly DEFAULT_MAX_TOKENS=6000
readonly CHARS_PER_TOKEN=4
readonly MAX_COMMAND_LENGTH=128
readonly MAX_SECTION_LENGTH=32
readonly COMMAND_REGEX='^[-A-Za-z0-9._:@+]+$'
readonly SECTION_REGEX='^(0|[A-Za-z0-9][A-Za-z0-9._-]{0,31})$'
readonly EXIT_OK=0
readonly EXIT_USAGE=2
readonly EXIT_MISSING_DEPENDENCY=3
readonly EXIT_NOT_FOUND=4
readonly SAFE_LOCALE="C"
readonly SAFE_PATH_FALLBACK="/usr/bin:/bin:/usr/sbin:/sbin"

# Purpose: Print a formatted error diagnostic and terminate.
# Inputs:
#   $1: error message string
#   $2: numeric exit code (default: 1)
# Outputs:
#   stderr: single-line ERROR diagnostic
# Exit codes:
#   Exits with $2
# Side effects:
#   Terminates the current process.
die() {
  local message="$1"
  local exit_code="${2:-1}"

  printf 'ERROR: %s\n' "${message}" >&2
  exit "${exit_code}"
}

# Purpose: Print GNU-style runtime help text.
# Inputs: none
# Outputs:
#   stdout: usage, options, exit status, and examples
# Exit codes: 0
# Side effects: none
print_help() {
  cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS]... COMMAND [SECTION] [MAX_TOKENS]

Look up installed man pages as sanitized plain text for agent workflows.

MAX_TOKENS is a decimal integer from 100 to 100000, without leading zeros.

Options:
  -h, --help      Show this help and exit.
  -V, --version   Print version and exit.

Exit status:
  0  Success.
  2  Usage or validation error.
  3  Missing dependency (man or col).
  4  No manual entry found.

Examples:
  bash ${SCRIPT_NAME} ls
  bash ${SCRIPT_NAME} open 2
  bash ${SCRIPT_NAME} printf 3posix 8000
EOF
}

# Purpose: Print tool version string.
# Inputs: none
# Outputs:
#   stdout: script name and version
# Exit codes: 0
# Side effects: none
print_version() {
  printf '%s %s\n' "${SCRIPT_NAME}" "${SCRIPT_VERSION}"
}

# Purpose: Print usage text to stderr on invalid invocation.
# Inputs: none
# Outputs:
#   stderr: help text
# Exit codes: 0
# Side effects: none
print_usage_error() {
  print_help >&2
}

# Purpose: Normalize allowlisted long options (--help, --version) to short flags.
# Inputs:
#   $1: nameref array for normalized output
#   $@: original CLI arguments
# Outputs: none (populates nameref array)
# Exit codes: 0
# Side effects: none
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

# Purpose: Verify a required host command is available on PATH.
# Inputs:
#   $1: binary name
#   $2: remediation install hint
# Outputs:
#   stderr: error message if missing
# Exit codes:
#   0 if present; exits EXIT_MISSING_DEPENDENCY (3) if missing
# Side effects: none
require_cmd() {
  local command_name="$1"
  local install_hint="$2"

  if ! command -v "${command_name}" >/dev/null 2>&1; then
    die \
      "Required command '${command_name}' is not installed. ${install_hint}" \
      "${EXIT_MISSING_DEPENDENCY}"
  fi
}

# Purpose: Validate the requested manual page command name against security rules.
# Inputs:
#   $1: command name string
# Outputs:
#   stderr: diagnostic on validation failure
# Exit codes:
#   0 if valid; exits EXIT_USAGE (2) if invalid
# Side effects: none
validate_command_name() {
  local command_name="$1"

  if [[ -z "${command_name}" ]]; then
    die "Command name cannot be empty." "${EXIT_USAGE}"
  fi

  if ((${#command_name} > MAX_COMMAND_LENGTH)); then
    die \
      "Command name exceeds maximum length of ${MAX_COMMAND_LENGTH} characters." \
      "${EXIT_USAGE}"
  fi

  if [[ "${command_name}" == -* ]]; then
    die "Command name must not start with '-'." "${EXIT_USAGE}"
  fi

  if [[ "${command_name}" == *"/"* ]]; then
    die "Command name must not contain slashes." "${EXIT_USAGE}"
  fi

  if [[ "${command_name}" == *".."* ]]; then
    die "Command name must not contain '..'." "${EXIT_USAGE}"
  fi

  if [[ ! "${command_name}" =~ ${COMMAND_REGEX} ]]; then
    die \
      "Invalid command name. Allowed: letters, numbers, dots, hyphens, underscores, colons, at-signs, and plus-signs." \
      "${EXIT_USAGE}"
  fi
}

# Purpose: Validate the manual section identifier.
# Inputs:
#   $1: section label string
# Outputs:
#   stderr: diagnostic on validation failure
# Exit codes:
#   0 if valid; exits EXIT_USAGE (2) if invalid
# Side effects: none
validate_section() {
  local section="$1"

  if [[ ! "${section}" =~ ${SECTION_REGEX} ]]; then
    die \
      "Invalid section '${section}'. Allowed: 0, numeric sections, or labels like 3posix." \
      "${EXIT_USAGE}"
  fi

  if ((${#section} > MAX_SECTION_LENGTH)); then
    die \
      "Section exceeds maximum length of ${MAX_SECTION_LENGTH} characters." \
      "${EXIT_USAGE}"
  fi
}

# Purpose: Validate the approximate token budget parameter.
# Inputs:
#   $1: integer token budget
# Outputs:
#   stderr: diagnostic on validation failure
# Exit codes:
#   0 if valid; exits EXIT_USAGE (2) if invalid
# Side effects: none
validate_max_tokens() {
  local max_tokens="$1"

  # Match the bounded decimal range before any arithmetic can overflow.
  if [[ ! "${max_tokens}" =~ ^([1-9][0-9]{2,4}|100000)$ ]]; then
    die "max_tokens must be 100 to 100000 in decimal, without leading zeros." \
      "${EXIT_USAGE}"
  fi
}

# Purpose: Construct a minimal, sanitized PATH string for man and col.
# Inputs:
#   $1: absolute path to man binary
#   $2: absolute path to col binary
# Outputs:
#   stdout: colon-delimited PATH string
# Exit codes: 0
# Side effects: none
build_sanitized_path() {
  local man_path="$1"
  local col_path="$2"
  local man_dir="${man_path%/*}"
  local col_dir="${col_path%/*}"

  if [[ "${man_dir}" == "${col_dir}" ]]; then
    printf '%s:%s\n' "${man_dir}" "${SAFE_PATH_FALLBACK}"
    return 0
  fi

  printf '%s:%s:%s\n' "${man_dir}" "${col_dir}" "${SAFE_PATH_FALLBACK}"
}

# Purpose: Execute man(1) in an isolated environment and strip overstrikes via col(1).
# Inputs:
#   $1: absolute path to man
#   $2: absolute path to col
#   $3: validated command name
#   $4: validated section label
# Outputs:
#   stdout: plain-text rendered manual page
# Exit codes:
#   0 on non-empty render; 1 if manual entry is missing or empty
# Side effects: spawns isolated read-only subprocesses (env -i man | col -bx)
fetch_man_page() {
  local man_bin="$1"
  local col_bin="$2"
  local command_name="$3"
  local section="$4"
  local sanitized_path
  local man_output
  local -a man_args=("--")

  if [[ "${section}" != "0" ]]; then
    man_args+=("${section}")
  fi
  man_args+=("${command_name}")

  sanitized_path="$(build_sanitized_path "${man_bin}" "${col_bin}")"

  if ! man_output="$(
    env -i \
      PATH="${sanitized_path}" \
      LC_ALL="${SAFE_LOCALE}" \
      LANG="${SAFE_LOCALE}" \
      LANGUAGE="${SAFE_LOCALE}" \
      TERM="dumb" \
      MANWIDTH="80" \
      "${man_bin}" "${man_args[@]}" 2>/dev/null \
      | "${col_bin}" -bx 2>/dev/null
  )"; then
    return 1
  fi

  if [[ -z "${man_output//[[:space:]]/}" ]]; then
    return 1
  fi

  printf '%s\n' "${man_output}"
}

# Purpose: Truncate rendered manual text to an approximate token limit.
# Inputs:
#   $1: full manual text
#   $2: max token budget
# Outputs:
#   stdout: full or truncated manual text with notice
# Exit codes: 0
# Side effects: none
truncate_output() {
  local text="$1"
  local max_tokens="$2"
  local max_chars=$((max_tokens * CHARS_PER_TOKEN))
  local text_length=${#text}
  local truncated

  if ((text_length <= max_chars)); then
    printf '%s\n' "${text}"
    return 0
  fi

  truncated="${text:0:max_chars}"
  truncated="${truncated%$'\n'*}"

  printf '%s\n' "${truncated}"
  printf '\n[... OUTPUT TRUNCATED at ~%d tokens (%d/%d chars). Request a specific section with:\n' \
    "${max_tokens}" "${max_chars}" "${text_length}"
  printf '  bash man_page_lookup.sh <command> <section> <higher_limit>\n'
  printf '  or ask about a specific flag/option to get targeted information.]\n'
}

# Purpose: Parse CLI options, validate inputs, and run the manual lookup.
# Inputs:
#   $@: CLI arguments
# Outputs:
#   stdout: manual text, help, or version
#   stderr: error diagnostics on failure
# Exit codes:
#   0 success, 2 usage error, 3 missing dependency, 4 manual not found
# Side effects: none
main() {
  local -a argv=()
  local option
  local command_name
  local section
  local max_tokens
  local man_bin
  local col_bin
  local raw_output

  # Reject leading-dash command names that are not allowlisted flags (-h, -V, --help, --version, --)
  if [[ "${#}" -ge 1 ]]; then
    case "$1" in
      -h | --help | -V | --version | --) ;;
      -*)
        die "Command name must not start with '-'." "${EXIT_USAGE}"
        ;;
    esac
  fi

  normalize_argv argv "$@"
  if [ "${#argv[@]}" -gt 0 ]; then
    set -- "${argv[@]}"
  else
    set --
  fi

  OPTIND=1
  while getopts ":hV" option; do
    case "${option}" in
      h)
        print_help
        exit "${EXIT_OK}"
        ;;
      V)
        print_version
        exit "${EXIT_OK}"
        ;;
      \?)
        die "Unknown option: -${OPTARG}" "${EXIT_USAGE}"
        ;;
    esac
  done
  shift $((OPTIND - 1))

  if [[ "${#}" -ge 1 && "$1" == "--" ]]; then
    shift
  fi

  command_name="${1:-}"
  section="${2-0}"
  max_tokens="${3-${DEFAULT_MAX_TOKENS}}"

  if [[ -z "${command_name}" ]]; then
    print_usage_error
    exit "${EXIT_USAGE}"
  fi

  if [[ "${#}" -gt 3 ]]; then
    die "Too many positional arguments." "${EXIT_USAGE}"
  fi

  validate_command_name "${command_name}"
  validate_section "${section}"
  validate_max_tokens "${max_tokens}"

  require_cmd "man" "Package: man-db. Installation requires user authorization."
  require_cmd "col" "Package: bsdextrautils. Installation requires user authorization."

  man_bin="$(command -v man)"
  col_bin="$(command -v col)"

  if ! raw_output="$(fetch_man_page "${man_bin}" "${col_bin}" "${command_name}" "${section}")"; then
    if [[ "${section}" == "0" ]]; then
      die "No man page found for '${command_name}'." "${EXIT_NOT_FOUND}"
    fi

    die \
      "No man page found for '${command_name}' in section ${section}." \
      "${EXIT_NOT_FOUND}"
  fi

  truncate_output "${raw_output}" "${max_tokens}"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi

# NAME
# man_page_lookup.sh - Query installed man pages as sanitized plain text
#
# SYNOPSIS
# man_page_lookup.sh [OPTIONS]... COMMAND [SECTION] [MAX_TOKENS]
#
# DESCRIPTION
# Look up an installed manual page using an isolated environment, strip
# overstrike formatting with col(1), and truncate the output to an approximate
# token budget suitable for AI agent workflows.
#
# OPTIONS
# -h, --help
#   Show help and exit 0.
# -V, --version
#   Print version and exit 0.
#
# EXIT STATUS
# 0  success
# 2  usage or validation error
# 3  missing dependency (man or col)
# 4  no manual entry found
#
# EXAMPLES
# bash man_page_lookup.sh ls
# bash man_page_lookup.sh open 2
# bash man_page_lookup.sh printf 3posix 8000
#
# SEE ALSO
# man(1), col(1)
