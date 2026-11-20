#!/bin/bash
# ==============================================================================
# man_page_lookup.sh - Query installed man pages as sanitized plain text.
#
# License: MIT
# Part of: ops-man
# SPDX-License-Identifier: MIT
#
# Read-only CLI that validates inputs, sanitizes the man(1) execution
# environment, supports literal focused excerpt retrieval with --match=TEXT,
# requires explicit dependencies, and returns deterministic exit codes for
# agent workflows.
# ==============================================================================

set -euo pipefail
IFS=$'\n\t'

readonly SCRIPT_NAME='man_page_lookup.sh'
readonly SCRIPT_VERSION='1.3.0'
readonly DEFAULT_MAX_TOKENS=6000
readonly CHARS_PER_TOKEN=4
readonly MAX_COMMAND_LENGTH=128
readonly MAX_SECTION_LENGTH=32
readonly MAX_MATCH_LENGTH=256
readonly MAX_MATCH_TERMS=32
readonly COMMAND_REGEX='^[-A-Za-z0-9._:@+]+$'
readonly SECTION_REGEX='^(0|[A-Za-z0-9][A-Za-z0-9._-]{0,31})$'
readonly EXIT_OK=0
readonly EXIT_NO_MATCH=1
readonly EXIT_USAGE=2
readonly EXIT_MISSING_DEPENDENCY=3
readonly EXIT_NOT_FOUND=4
readonly SAFE_LOCALE='C'
readonly SAFE_PATH_FALLBACK='/usr/bin:/bin:/usr/sbin:/sbin'

MAN_SANITIZED_PATH=''
MAN_PAGE_TEXT=''

# Purpose: Print a formatted error diagnostic and terminate.
# Inputs:
#   $1: error message string
#   $2: numeric exit code (default: 1)
# Outputs:
#   stderr: single-line ERROR diagnostic
# Exit codes:
#   Exits with $2
# Globals: none
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
# Globals: SCRIPT_NAME, DEFAULT_MAX_TOKENS, MAX_MATCH_TERMS
# Side effects: none
print_help() {
  cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS]... COMMAND [SECTION] [MAX_TOKENS]

Look up installed man pages as sanitized plain text for agent workflows.

MAX_TOKENS is a decimal integer from 100 to 100000, without leading zeros
(default: ${DEFAULT_MAX_TOKENS}).

Options:
  --match=TEXT    Return focused excerpts containing literal TEXT (repeatable,
                  up to ${MAX_MATCH_TERMS} unique terms, before positional arguments).
                  Prefers complete option, directive, or entry definitions and
                  pertinent cross-references; falls back to a bounded context
                  window when structure is ambiguous. Budget applies after
                  selection.
  -h, --help      Show this help and exit.
  -V, --version   Print version and exit.
  --              End option parsing.

Exit status:
  0  Success.
  1  No matching excerpt found for --match=TEXT.
  2  Usage or validation error.
  3  Missing dependency (man, col, or awk for --match).
  4  No manual entry found.

Examples:
  bash ${SCRIPT_NAME} ls
  bash ${SCRIPT_NAME} open 2
  bash ${SCRIPT_NAME} printf 3posix 8000
  bash ${SCRIPT_NAME} --match=--color ls 1
  bash ${SCRIPT_NAME} --match=GuestExecStatus --match=guest-exec-status qemu-ga-ref 7
EOF
}

# Purpose: Print tool version string.
# Inputs: none
# Outputs:
#   stdout: script name and version
# Exit codes: 0
# Globals: SCRIPT_NAME, SCRIPT_VERSION
# Side effects: none
print_version() {
  printf '%s %s\n' "${SCRIPT_NAME}" "${SCRIPT_VERSION}"
}

# Purpose: Print usage text to stderr on invalid invocation.
# Inputs: none
# Outputs:
#   stderr: help text
# Exit codes: 0
# Globals: none
# Side effects: none
print_usage_error() {
  print_help >&2
}

# Purpose: Verify a required host command is available on PATH.
# Inputs:
#   $1: binary name
#   $2: remediation install hint
# Outputs:
#   stderr: error message if missing
# Exit codes:
#   0 if present; exits EXIT_MISSING_DEPENDENCY (3) if missing
# Globals: EXIT_MISSING_DEPENDENCY
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

# Purpose: Validate one literal --match=TEXT argument.
# Inputs:
#   $1: literal match term
# Outputs:
#   stderr: diagnostic on validation failure
# Exit codes:
#   0 if valid; exits EXIT_USAGE (2) if invalid
# Globals: MAX_MATCH_LENGTH, EXIT_USAGE
# Side effects: none
validate_match_term() {
  local term="$1"

  if [[ -z "${term}" ]]; then
    die 'Match term cannot be empty.' "${EXIT_USAGE}"
  fi

  if [[ "${term}" == *$'\n'* || "${term}" == *$'\r'* ]]; then
    die 'Match term must be a single line without CR or LF.' "${EXIT_USAGE}"
  fi

  if (( ${#term} > MAX_MATCH_LENGTH )); then
    die \
      "Match term exceeds maximum length of ${MAX_MATCH_LENGTH} characters." \
      "${EXIT_USAGE}"
  fi
}

# Purpose: Validate the requested manual page command name against security rules.
# Inputs:
#   $1: command name string
# Outputs:
#   stderr: diagnostic on validation failure
# Exit codes:
#   0 if valid; exits EXIT_USAGE (2) if invalid
# Globals: MAX_COMMAND_LENGTH, COMMAND_REGEX, EXIT_USAGE
# Side effects: none
validate_command_name() {
  local command_name="$1"

  if [[ -z "${command_name}" ]]; then
    die 'Command name cannot be empty.' "${EXIT_USAGE}"
  fi

  if (( ${#command_name} > MAX_COMMAND_LENGTH )); then
    die \
      "Command name exceeds maximum length of ${MAX_COMMAND_LENGTH} characters." \
      "${EXIT_USAGE}"
  fi

  if [[ "${command_name}" == -* ]]; then
    die "Command name must not start with '-'." "${EXIT_USAGE}"
  fi

  if [[ "${command_name}" == *'/'* ]]; then
    die 'Command name must not contain slashes.' "${EXIT_USAGE}"
  fi

  if [[ "${command_name}" == *'..'* ]]; then
    die "Command name must not contain '..'." "${EXIT_USAGE}"
  fi

  if [[ ! "${command_name}" =~ ${COMMAND_REGEX} ]]; then
    die \
      'Invalid command name. Allowed: letters, numbers, dots, hyphens, underscores, colons, at-signs, and plus-signs.' \
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
# Globals: SECTION_REGEX, MAX_SECTION_LENGTH, EXIT_USAGE
# Side effects: none
validate_section() {
  local section="$1"

  if [[ ! "${section}" =~ ${SECTION_REGEX} ]]; then
    die \
      "Invalid section '${section}'. Allowed: 0, numeric sections, or labels like 3posix." \
      "${EXIT_USAGE}"
  fi

  if (( ${#section} > MAX_SECTION_LENGTH )); then
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
# Globals: EXIT_USAGE
# Side effects: none
validate_max_tokens() {
  local max_tokens="$1"

  # Match the bounded decimal range before any arithmetic can overflow.
  if [[ ! "${max_tokens}" =~ ^([1-9][0-9]{2,4}|100000)$ ]]; then
    die 'max_tokens must be 100 to 100000 in decimal, without leading zeros.' \
      "${EXIT_USAGE}"
  fi
}

# Purpose: Construct a minimal, sanitized PATH string for required tool paths.
# Inputs:
#   $@: absolute paths to required binaries
# Outputs: none (writes MAN_SANITIZED_PATH)
# Exit codes: 0
# Globals: SAFE_PATH_FALLBACK, MAN_SANITIZED_PATH
# Side effects: none
build_sanitized_path() {
  local bin_path
  local bin_dir
  local result="${SAFE_PATH_FALLBACK}"

  for bin_path in "$@"; do
    bin_dir="${bin_path%/*}"
    if [[ ":${result}:" != *":${bin_dir}:"* ]]; then
      result="${bin_dir}:${result}"
    fi
  done

  MAN_SANITIZED_PATH="${result}"
}

# Purpose: Execute man(1) once in an isolated environment and strip overstrikes.
# Inputs:
#   $1: absolute path to man
#   $2: absolute path to col
#   $3: validated command name
#   $4: validated section label
# Outputs: none (writes MAN_PAGE_TEXT; stderr on missing page)
# Exit codes:
#   0 on non-empty render; exits EXIT_NOT_FOUND (4) if absent or empty
# Globals: MAN_SANITIZED_PATH, MAN_PAGE_TEXT, SAFE_LOCALE, EXIT_NOT_FOUND
# Side effects: spawns isolated read-only subprocesses (env -i man | col -bx)
fetch_man_page() {
  local man_bin="$1"
  local col_bin="$2"
  local command_name="$3"
  local section="$4"
  local man_output=''
  local -a man_args=(--)

  if [[ "${section}" != 0 ]]; then
    man_args+=("${section}")
  fi
  man_args+=("${command_name}")

  build_sanitized_path "${man_bin}" "${col_bin}"

  if ! man_output="$(
    env -i \
      PATH="${MAN_SANITIZED_PATH}" \
      LC_ALL="${SAFE_LOCALE}" \
      LANG="${SAFE_LOCALE}" \
      LANGUAGE="${SAFE_LOCALE}" \
      TERM='dumb' \
      "${man_bin}" "${man_args[@]}" 2>/dev/null \
      | "${col_bin}" -bx 2>/dev/null
  )"; then
    man_output=''
  fi

  if [[ -z "${man_output//[[:space:]]/}" ]]; then
    if [[ "${section}" == 0 ]]; then
      die "No man page found for '${command_name}'." "${EXIT_NOT_FOUND}"
    fi
    die \
      "No man page found for '${command_name}' in section ${section}." \
      "${EXIT_NOT_FOUND}"
  fi

  MAN_PAGE_TEXT="${man_output}"
}

# Purpose: Truncate rendered manual text to an approximate token limit.
# Inputs:
#   $1: full manual text
#   $2: max token budget
# Outputs:
#   stdout: full or truncated manual text with notice
# Exit codes: 0
# Globals: CHARS_PER_TOKEN, SCRIPT_NAME
# Side effects: none
truncate_output() {
  local text="$1"
  local max_tokens="$2"
  local max_chars=$(( max_tokens * CHARS_PER_TOKEN ))
  local text_length="${#text}"
  local truncated

  if (( text_length <= max_chars )); then
    printf '%s\n' "${text}"
    return 0
  fi

  truncated="${text:0:max_chars}"
  truncated="${truncated%$'\n'*}"

  printf '%s\n' "${truncated}"
  printf '\n[... OUTPUT TRUNCATED at ~%d tokens (%d/%d chars). Request a specific section or match with:\n' \
    "${max_tokens}" "${max_chars}" "${text_length}"
  printf '  bash %s <command> <section> <higher_limit>\n' "${SCRIPT_NAME}"
  printf '  bash %s --match=<term> <command> [section]]\n' "${SCRIPT_NAME}"
}

# Purpose: Extract and budget-pack literal matching excerpts from rendered text.
# Inputs:
#   $1: absolute path to awk
#   $2: validated command name
#   $3: validated section label
#   $4: validated max token budget
#   $5..: deduplicated literal match terms
# Outputs:
#   stdout: matching verbatim excerpts and omission/missing notices
#   stderr: diagnostic on no match or extractor failure
# Exit codes:
#   0 on match; exits EXIT_NO_MATCH (1) if no excerpt matched;
#   exits EXIT_NOT_FOUND (4) on unexpected extractor failure
# Globals: MAN_PAGE_TEXT, MAN_SANITIZED_PATH, CHARS_PER_TOKEN, SAFE_LOCALE,
#          EXIT_NO_MATCH, EXIT_NOT_FOUND
# Side effects: spawns isolated read-only awk subprocess
extract_matching_excerpts() {
  local awk_bin="$1"
  local command_name="$2"
  local section="$3"
  local max_tokens="$4"
  shift 4
  local -a terms=("$@")
  local max_chars=$(( max_tokens * CHARS_PER_TOKEN ))
  local awk_program=''
  local awk_status=0
  local missing_list=''
  local term

  IFS= read -r -d '' awk_program <<'AWK' || true
function trim_str(s) {
  sub(/^[ \t]+/, "", s)
  sub(/[ \t]+$/, "", s)
  return s
}

function compact_label(s) {
  s = trim_str(s)
  gsub(/[ \t]+/, " ", s)
  if (length(s) > 64) {
    s = substr(s, 1, 61) "..."
  }
  return s
}

function is_boundary_match(text, term,    rest, pos, offset, tlen, pre, post) {
  tlen = length(term)
  rest = text
  offset = 0
  while ((pos = index(rest, term)) > 0) {
    pre = (offset + pos == 1) ? "" : substr(text, offset + pos - 1, 1)
    post = (offset + pos + tlen > length(text)) ? "" : substr(text, offset + pos + tlen, 1)
    if (pre !~ /[A-Za-z0-9_-]/ && post !~ /[A-Za-z0-9_-]/) {
      return 1
    }
    offset += pos
    rest = substr(rest, pos + 1)
  }
  return 0
}

function split_tag_part(s,    p) {
  if (match(s, /   +/)) {
    p = RSTART
    return substr(s, 1, p - 1)
  }
  return s
}

function has_inline_gap(s) {
  return (match(s, /^[^ \t][^ \t]*([ \t][^ \t]+)?   +[^ \t]/) > 0)
}

function can_stack_header(s) {
  if (s ~ /\.$/) {
    return 0
  }
  if (match(s, /   +/)) {
    return 0
  }
  return 1
}

function add_candidate(s, e, tier, kind, sec, ctx, lbl, tidx) {
  cand_count++
  c_start[cand_count] = s
  c_end[cand_count] = e
  c_tier[cand_count] = tier
  c_kind[cand_count] = kind
  c_sec[cand_count] = sec
  c_ctx[cand_count] = ctx
  c_lbl[cand_count] = lbl
  c_term[cand_count] = tidx
}

function format_excerpt_header(m,    kind_name, loc) {
  if (m_kind[m] == 1) {
    kind_name = "definition"
  } else if (m_kind[m] == 2) {
    kind_name = "cross-reference"
  } else {
    kind_name = "context window"
  }
  loc = m_sec[m]
  if (m_ctx[m] != "" && m_ctx[m] != loc) {
    loc = (loc != "" ? loc " > " m_ctx[m] : m_ctx[m])
  }
  if (loc != "") {
    return "--- [" kind_name " | " loc " | lines " m_start[m] "-" m_end[m] "] ---"
  }
  return "--- [" kind_name " | lines " m_start[m] "-" m_end[m] "] ---"
}

function excerpt_body_len(s, e,    i, total) {
  total = 0
  for (i = s; i <= e; i++) {
    total += length(line[i]) + 1
  }
  return total
}

NR == 1 {
  max_tokens = $0 + 0
  next
}
NR == 2 {
  max_chars = $0 + 0
  next
}
NR == 3 {
  term_count = $0 + 0
  next
}
NR <= 3 + term_count {
  terms[NR - 3] = $0
  next
}
{
  n_lines++
  line[n_lines] = $0
}

END {
  COMPACT_ENTRY_LIMIT = 24
  SHORT_SECTION_LIMIT = 30
  MAX_PARA_LINES = 16
  CONTEXT_RADIUS = 4

  first_nb = 0
  last_nb = 0
  for (i = 1; i <= n_lines; i++) {
    if (line[i] ~ /^[ \t]*$/) {
      is_blank[i] = 1
      indent[i] = -1
      trimmed[i] = ""
    } else {
      is_blank[i] = 0
      match(line[i], /^[ \t]*/)
      indent[i] = RLENGTH
      trimmed[i] = trim_str(line[i])
      if (first_nb == 0) {
        first_nb = i
      }
      last_nb = i
    }
    is_chrome[i] = 0
  }

  if (first_nb > 0 && indent[first_nb] == 0 && match(line[first_nb], /   +/)) {
    is_chrome[first_nb] = 1
  }
  if (last_nb > first_nb && indent[last_nb] == 0 && match(line[last_nb], /   +/)) {
    is_chrome[last_nb] = 1
  }
  page_header = (first_nb > 0 && is_chrome[first_nb]) ? line[first_nb] : ""

  # Identify top-level sections (column 0, non-chrome).
  cur_sec = ""
  cur_sec_line = 0
  for (i = 1; i <= n_lines; i++) {
    if (!is_blank[i] && !is_chrome[i] && indent[i] == 0) {
      cur_sec = compact_label(trimmed[i])
      cur_sec_line = i
      is_sec_hdr[i] = 1
    } else {
      is_sec_hdr[i] = 0
    }
    sec_name[i] = cur_sec
    sec_hdr_line[i] = cur_sec_line
  }

  for (i = 1; i <= n_lines; i++) {
    if (is_sec_hdr[i]) {
      se = i
      for (j = i + 1; j <= n_lines; j++) {
        if (is_chrome[j]) {
          break
        }
        if (is_sec_hdr[j]) {
          break
        }
        if (!is_blank[j]) {
          se = j
        }
      }
      sec_end[i] = se
    }
  }

  # Identify hanging-indent, blank-headed, and inline-tagged entries.
  num_entries = 0
  for (i = 1; i <= n_lines; i++) {
    if (is_blank[i] || is_chrome[i] || indent[i] == 0 || hdr_owner[i] > 0) {
      continue
    }
    ind = indent[i]

    # Subcase A: direct hanging indent, allowing up to 4 stacked alias lines.
    he = i
    while (he + 1 <= n_lines && !is_blank[he + 1] && !is_chrome[he + 1] \
           && indent[he + 1] == ind && (he - i) < 3 && can_stack_header(trimmed[he])) {
      he++
    }
    nx = he + 1
    if (nx <= n_lines && !is_blank[nx] && !is_chrome[nx] && indent[nx] > ind) {
      e_end = nx
      for (j = nx + 1; j <= n_lines; j++) {
        if (is_chrome[j]) {
          break
        }
        if (is_blank[j]) {
          continue
        }
        if (indent[j] <= ind) {
          break
        }
        e_end = j
      }
      num_entries++
      ent_start[num_entries] = i
      ent_hdr_end[num_entries] = he
      ent_end[num_entries] = e_end
      ent_ind[num_entries] = ind
      ent_form[num_entries] = 1
      for (k = i; k <= he; k++) {
        hdr_owner[k] = num_entries
      }
      continue
    }

    # Subcase B: single-line header + single blank line + deeper-indented body.
    prev_diff = (i == 1 || is_blank[i - 1] || is_chrome[i - 1] || indent[i - 1] != ind)
    if (prev_diff && i + 2 <= n_lines && is_blank[i + 1] && !is_blank[i + 2] \
        && !is_chrome[i + 2] && indent[i + 2] > ind \
        && trimmed[i] !~ /[.:]$/ && !match(trimmed[i], /   +/)) {
      e_end = i + 2
      for (j = i + 3; j <= n_lines; j++) {
        if (is_chrome[j]) {
          break
        }
        if (is_blank[j]) {
          continue
        }
        if (indent[j] <= ind) {
          break
        }
        e_end = j
      }
      num_entries++
      ent_start[num_entries] = i
      ent_hdr_end[num_entries] = i
      ent_end[num_entries] = e_end
      ent_ind[num_entries] = ind
      ent_form[num_entries] = 2
      hdr_owner[i] = num_entries
      continue
    }

    # Subcase C: single-line inline tagged entry (short tag + 3+ spaces + desc).
    next_sep = (i == n_lines || is_blank[i + 1] || is_chrome[i + 1] \
                || indent[i + 1] != ind || has_inline_gap(trimmed[i + 1]))
    prev_ok = (prev_diff || (i > 1 && hdr_owner[i - 1] > 0 && ent_form[hdr_owner[i - 1]] == 3))
    if (prev_ok && next_sep && has_inline_gap(trimmed[i])) {
      num_entries++
      ent_start[num_entries] = i
      ent_hdr_end[num_entries] = i
      ent_end[num_entries] = i
      ent_ind[num_entries] = ind
      ent_form[num_entries] = 3
      hdr_owner[i] = num_entries
    }
  }

  # Scan all lines for literal hits and classify each hit structurally.
  cand_count = 0
  for (t = 1; t <= term_count; t++) {
    term_matched[t] = 0
    term_has_def[t] = 0
  }

  for (i = 1; i <= n_lines; i++) {
    if (is_blank[i]) {
      continue
    }
    for (t = 1; t <= term_count; t++) {
      if (index(line[i], terms[t]) == 0) {
        continue
      }
      term_matched[t] = 1

      # 1. Section heading hit.
      if (is_sec_hdr[i]) {
        se = sec_end[i]
        is_bnd = is_boundary_match(trimmed[i], terms[t])
        if (se - i + 1 <= SHORT_SECTION_LIMIT) {
          term_has_def[t] = 1
          add_candidate(i, se, (is_bnd ? 1 : 2), 1, sec_name[i], "", compact_label(trimmed[i]), t)
        } else {
          we = (i + 12 < se) ? i + 12 : se
          add_candidate(i, we, 2, 3, sec_name[i], "", compact_label(trimmed[i]), t)
        }
        continue
      }

      # 2. Entry header hit (tag portion vs inline description tail).
      e_id = hdr_owner[i] + 0
      if (e_id > 0) {
        tag_part = split_tag_part(trimmed[i])
        if (index(tag_part, terms[t]) > 0) {
          is_bnd = is_boundary_match(tag_part, terms[t])
          term_has_def[t] = 1
          lbl = compact_label(split_tag_part(trimmed[ent_start[e_id]]))
          add_candidate(ent_start[e_id], ent_end[e_id], (is_bnd ? 1 : 2), 1, sec_name[i], "", lbl, t)
        } else {
          # Hit appeared only in the inline description after the tag gap.
          lbl = compact_label(split_tag_part(trimmed[ent_start[e_id]]))
          if (ent_end[e_id] - ent_start[e_id] + 1 <= COMPACT_ENTRY_LIMIT) {
            add_candidate(ent_start[e_id], ent_end[e_id], 3, 2, sec_name[i], "", lbl, t)
          } else {
            ws = ent_start[e_id]
            we = (i + CONTEXT_RADIUS < ent_end[e_id]) ? i + CONTEXT_RADIUS : ent_end[e_id]
            add_candidate(ws, we, 4, 3, sec_name[i], lbl, lbl, t)
          }
        }
        continue
      }

      # 3. Enclosing definition entry hit (body / cross-reference).
      best_compact = 0
      outer_enclosing = 0
      tight_enclosing = 0
      for (e = 1; e <= num_entries; e++) {
        if (ent_start[e] < i && i <= ent_end[e]) {
          if (outer_enclosing == 0) {
            outer_enclosing = e
          }
          tight_enclosing = e
          if (best_compact == 0 && (ent_end[e] - ent_start[e] + 1) <= COMPACT_ENTRY_LIMIT) {
            best_compact = e
          }
        }
      }

      if (best_compact > 0) {
        lbl = compact_label(split_tag_part(trimmed[ent_start[best_compact]]))
        ctx = ""
        if (outer_enclosing > 0 && outer_enclosing != best_compact) {
          ctx = compact_label(split_tag_part(trimmed[ent_start[outer_enclosing]]))
        }
        add_candidate(ent_start[best_compact], ent_end[best_compact], 3, 2, sec_name[i], ctx, lbl, t)
        continue
      }

      if (outer_enclosing > 0) {
        # Inside a large entry (> COMPACT_ENTRY_LIMIT): extract matching paragraph or window.
        parent_lbl = compact_label(split_tag_part(trimmed[ent_start[outer_enclosing]]))
        lo_bound = ent_start[tight_enclosing]
        hi_bound = ent_end[tight_enclosing]
        ps = i
        while (ps > lo_bound && !is_blank[ps - 1] && indent[ps - 1] == indent[i]) {
          ps--
        }
        pe = i
        while (pe < hi_bound && !is_blank[pe + 1] && indent[pe + 1] == indent[i]) {
          pe++
        }
        if (pe - ps + 1 <= MAX_PARA_LINES) {
          add_candidate(ps, pe, 3, 2, sec_name[i], parent_lbl, parent_lbl, t)
        } else {
          ws = (i - CONTEXT_RADIUS > ps) ? i - CONTEXT_RADIUS : ps
          we = (i + CONTEXT_RADIUS < pe) ? i + CONTEXT_RADIUS : pe
          add_candidate(ws, we, 4, 3, sec_name[i], parent_lbl, parent_lbl, t)
        }
        continue
      }

      # 4. Standalone prose paragraph vs ambiguous structure.
      sec_lo = (sec_hdr_line[i] > 0) ? sec_hdr_line[i] + 1 : 1
      sec_hi = (sec_hdr_line[i] > 0) ? sec_end[sec_hdr_line[i]] : n_lines
      if (is_chrome[i] || indent[i] == 0) {
        ws = (i - CONTEXT_RADIUS > 1) ? i - CONTEXT_RADIUS : 1
        we = (i + CONTEXT_RADIUS < n_lines) ? i + CONTEXT_RADIUS : n_lines
        if (!is_chrome[i]) {
          if (ws < sec_lo) {
            ws = sec_lo
          }
          if (we > sec_hi) {
            we = sec_hi
          }
        }
        add_candidate(ws, we, 4, 3, sec_name[i], "", compact_label(trimmed[i]), t)
        continue
      }

      ps = i
      while (ps > sec_lo && !is_blank[ps - 1] && !is_chrome[ps - 1] \
             && indent[ps - 1] == indent[i]) {
        ps--
      }
      pe = i
      while (pe < sec_hi && !is_blank[pe + 1] && !is_chrome[pe + 1] \
             && indent[pe + 1] == indent[i]) {
        pe++
      }
      clean_top = (ps == sec_lo || is_blank[ps - 1] || is_sec_hdr[ps - 1])
      clean_bot = (pe == sec_hi || is_blank[pe + 1] || is_sec_hdr[pe + 1])

      if (clean_top && clean_bot && (pe - ps + 1) <= MAX_PARA_LINES) {
        # Defer kind (cross-reference vs context window) via kind=20 sentinel.
        add_candidate(ps, pe, 3, 20, sec_name[i], "", compact_label(trimmed[ps]), t)
      } else {
        ws = (i - CONTEXT_RADIUS > sec_lo) ? i - CONTEXT_RADIUS : sec_lo
        we = (i + CONTEXT_RADIUS < sec_hi) ? i + CONTEXT_RADIUS : sec_hi
        while (ws < i && is_blank[ws]) {
          ws++
        }
        while (we > i && is_blank[we]) {
          we--
        }
        add_candidate(ws, we, 4, 3, sec_name[i], "", compact_label(trimmed[i]), t)
      }
    }
  }

  if (cand_count == 0) {
    exit 1
  }

  # Resolve deferred standalone paragraph kind: cross-reference if term has a definition, else context window.
  for (c = 1; c <= cand_count; c++) {
    if (c_kind[c] == 20) {
      if (term_has_def[c_term[c]]) {
        c_kind[c] = 2
      } else {
        c_kind[c] = 3
        c_tier[c] = 4
      }
    }
  }

  # Sort raw candidates by (start ASC, end DESC) via insertion sort.
  for (c = 1; c <= cand_count; c++) {
    order[c] = c
  }
  for (i = 2; i <= cand_count; i++) {
    key = order[i]
    j = i - 1
    while (j >= 1 && (c_start[order[j]] > c_start[key] \
                      || (c_start[order[j]] == c_start[key] && c_end[order[j]] < c_end[key]))) {
      order[j + 1] = order[j]
      j--
    }
    order[j + 1] = key
  }

  # Merge overlapping excerpts (and immediately contiguous context windows).
  m_count = 0
  for (idx = 1; idx <= cand_count; idx++) {
    c = order[idx]
    can_merge = 0
    if (m_count > 0) {
      if (c_start[c] <= m_end[m_count]) {
        can_merge = 1
      } else if (c_start[c] == m_end[m_count] + 1 && m_kind[m_count] == 3 && c_kind[c] == 3) {
        can_merge = 1
      }
    }
    if (can_merge) {
      if (c_end[c] > m_end[m_count]) {
        m_end[m_count] = c_end[c]
      }
      if (c_tier[c] < m_tier[m_count] \
          || (c_tier[c] == m_tier[m_count] && c_kind[c] < m_kind[m_count])) {
        m_tier[m_count] = c_tier[c]
        m_kind[m_count] = c_kind[c]
        m_sec[m_count] = c_sec[c]
        m_ctx[m_count] = c_ctx[c]
        m_lbl[m_count] = c_lbl[c]
      } else if (c_kind[c] < m_kind[m_count]) {
        m_kind[m_count] = c_kind[c]
      }
      t = c_term[c]
      key_mt = m_count SUBSEP t
      if (!(key_mt in m_term_tier) || c_tier[c] < m_term_tier[key_mt]) {
        m_term_tier[key_mt] = c_tier[c]
      }
    } else {
      m_count++
      m_start[m_count] = c_start[c]
      m_end[m_count] = c_end[c]
      m_tier[m_count] = c_tier[c]
      m_kind[m_count] = c_kind[c]
      m_sec[m_count] = c_sec[c]
      m_ctx[m_count] = c_ctx[c]
      m_lbl[m_count] = c_lbl[c]
      m_term_tier[m_count SUBSEP c_term[c]] = c_tier[c]
    }
  }

  # Compute exact formatted character cost for each merged excerpt.
  for (m = 1; m <= m_count; m++) {
    m_hdr[m] = format_excerpt_header(m)
    m_cost[m] = length(m_hdr[m]) + 1 + excerpt_body_len(m_start[m], m_end[m]) + 1
  }

  # Build priority queue: pass 1 guarantees top excerpt per matched term;
  # pass 2 ranks remaining excerpts by (tier ASC, start ASC).
  q_count = 0
  for (t = 1; t <= term_count; t++) {
    if (!term_matched[t]) {
      continue
    }
    best_m = 0
    best_t = 999
    for (m = 1; m <= m_count; m++) {
      key_mt = m SUBSEP t
      if (key_mt in m_term_tier) {
        if (m_term_tier[key_mt] < best_t \
            || (m_term_tier[key_mt] == best_t && (best_m == 0 || m_start[m] < m_start[best_m]))) {
          best_t = m_term_tier[key_mt]
          best_m = m
        }
      }
    }
    if (best_m > 0 && !in_queue[best_m]) {
      q_count++
      queue[q_count] = best_m
      in_queue[best_m] = 1
    }
  }

  rem_count = 0
  for (m = 1; m <= m_count; m++) {
    if (!in_queue[m]) {
      rem_count++
      rem[rem_count] = m
    }
  }
  for (i = 2; i <= rem_count; i++) {
    key = rem[i]
    j = i - 1
    while (j >= 1 && (m_tier[rem[j]] > m_tier[key] \
                      || (m_tier[rem[j]] == m_tier[key] && m_start[rem[j]] > m_start[key]))) {
      rem[j + 1] = rem[j]
      j--
    }
    rem[j + 1] = key
  }
  for (i = 1; i <= rem_count; i++) {
    q_count++
    queue[q_count] = rem[i]
  }

  # Pack excerpts into max_chars budget in priority order.
  used_chars = 0
  emit_page_header = 0
  if (page_header != "" && length(page_header) + 2 <= max_chars / 2) {
    emit_page_header = 1
    used_chars = length(page_header) + 2
  }

  sel_count = 0
  omit_count = 0
  truncate_first = 0
  for (q = 1; q <= q_count; q++) {
    m = queue[q]
    if (sel_count == 0 && used_chars + m_cost[m] > max_chars) {
      sel_count++
      selected[sel_count] = m
      truncate_first = 1
      used_chars = max_chars
    } else if (used_chars + m_cost[m] <= max_chars) {
      sel_count++
      selected[sel_count] = m
      used_chars += m_cost[m]
    } else {
      omit_count++
      omitted[omit_count] = m
    }
  }

  # Sort selected excerpts in ascending document line order.
  for (i = 2; i <= sel_count; i++) {
    key = selected[i]
    j = i - 1
    while (j >= 1 && m_start[selected[j]] > m_start[key]) {
      selected[j + 1] = selected[j]
      j--
    }
    selected[j + 1] = key
  }

  # Emit page header and verbatim selected excerpts.
  if (emit_page_header) {
    print page_header
    print ""
  }

  trunc_emitted = 0
  trunc_total = 0
  for (s_idx = 1; s_idx <= sel_count; s_idx++) {
    m = selected[s_idx]
    if (s_idx > 1) {
      print ""
    }
    print m_hdr[m]
    if (truncate_first && sel_count == 1) {
      avail = max_chars - (emit_page_header ? length(page_header) + 2 : 0) - length(m_hdr[m]) - 1
      if (avail < 1) {
        avail = 1
      }
      emitted = 0
      trunc_total = excerpt_body_len(m_start[m], m_end[m])
      for (i = m_start[m]; i <= m_end[m]; i++) {
        line_cost = length(line[i]) + 1
        if (i > m_start[m] && emitted + line_cost > avail) {
          break
        }
        print line[i]
        emitted += line_cost
      }
      trunc_emitted = emitted
    } else {
      for (i = m_start[m]; i <= m_end[m]; i++) {
        print line[i]
      }
    }
  }

  # Explicit notices for truncation, omitted excerpts, and missing terms.
  if (truncate_first) {
    printf "\n[... EXCERPT TRUNCATED at ~%d tokens (%d/%d chars of selected excerpt). Re-run with a larger MAX_TOKENS budget.]\n", \
      max_tokens, trunc_emitted, trunc_total
  }

  if (omit_count > 0) {
    # Sort omitted excerpts in document order for readable reporting.
    for (i = 2; i <= omit_count; i++) {
      key = omitted[i]
      j = i - 1
      while (j >= 1 && m_start[omitted[j]] > m_start[key]) {
        omitted[j + 1] = omitted[j]
        j--
      }
      omitted[j + 1] = key
    }
    omit_summary = ""
    shown = (omit_count <= 5) ? omit_count : 5
    for (i = 1; i <= shown; i++) {
      m = omitted[i]
      item = m_lbl[m] " (lines " m_start[m] "-" m_end[m] ")"
      omit_summary = (omit_summary == "" ? item : omit_summary ", " item)
    }
    if (omit_count > shown) {
      omit_summary = omit_summary ", +" (omit_count - shown) " more"
    }
    printf "\n[... OMITTED EXCERPTS: %d matching excerpt(s) omitted due to ~%d token budget (%d chars): %s. Re-run with a larger MAX_TOKENS budget.]\n", \
      omit_count, max_tokens, max_chars, omit_summary
  }

  miss_str = ""
  for (t = 1; t <= term_count; t++) {
    if (!term_matched[t]) {
      miss_str = (miss_str == "" ? terms[t] : miss_str ", " terms[t])
    }
  }
  if (miss_str != "") {
    printf "\n[... MISSING MATCH TERMS (not found in rendered page): %s]\n", miss_str
  }
}
AWK

  build_sanitized_path "${awk_bin}"

  {
    printf '%d\n%d\n%d\n' "${max_tokens}" "${max_chars}" "${#terms[@]}"
    printf '%s\n' "${terms[@]}"
    printf '%s\n' "${MAN_PAGE_TEXT}"
  } \
    | env -i \
      PATH="${MAN_SANITIZED_PATH}" \
      LC_ALL="${SAFE_LOCALE}" \
      LANG="${SAFE_LOCALE}" \
      LANGUAGE="${SAFE_LOCALE}" \
      "${awk_bin}" -- "${awk_program}" \
    || awk_status="$?"

  if (( awk_status == 0 )); then
    return 0
  fi

  if (( awk_status == 1 )); then
    for term in "${terms[@]}"; do
      if [[ -z "${missing_list}" ]]; then
        missing_list="${term}"
      else
        missing_list="${missing_list}, ${term}"
      fi
    done
    if [[ "${section}" == 0 ]]; then
      die \
        "No matching excerpt found in '${command_name}' for: ${missing_list}" \
        "${EXIT_NO_MATCH}"
    fi
    die \
      "No matching excerpt found in '${command_name}' (section ${section}) for: ${missing_list}" \
      "${EXIT_NO_MATCH}"
  fi

  die "Failed to extract excerpts from '${command_name}'." "${EXIT_NOT_FOUND}"
}

# Purpose: Parse CLI options, validate inputs, and run the manual lookup.
# Inputs:
#   $@: CLI arguments
# Outputs:
#   stdout: manual text, focused excerpts, help, or version
#   stderr: error diagnostics on failure
# Exit codes:
#   0 success, 1 no match for --match, 2 usage error,
#   3 missing dependency, 4 manual not found
# Globals: DEFAULT_MAX_TOKENS, MAX_MATCH_TERMS, EXIT_OK, EXIT_USAGE,
#          MAN_PAGE_TEXT
# Side effects: none
main() {
  local show_help=0
  local show_version=0
  local match_value=''
  local existing_term=''
  local duplicate=0
  local command_name=''
  local section=''
  local max_tokens=''
  local man_bin=''
  local col_bin=''
  local awk_bin=''
  local -a match_terms=()

  while (( $# > 0 )); do
    case "$1" in
      -h | --help)
        show_help=1
        shift
        ;;
      -V | --version)
        show_version=1
        shift
        ;;
      --match=*)
        match_value="${1#*=}"
        validate_match_term "${match_value}"
        duplicate=0
        for existing_term in "${match_terms[@]}"; do
          if [[ "${existing_term}" == "${match_value}" ]]; then
            duplicate=1
            break
          fi
        done
        if (( !duplicate )); then
          if (( ${#match_terms[@]} >= MAX_MATCH_TERMS )); then
            die \
              "Too many unique --match terms (maximum: ${MAX_MATCH_TERMS})." \
              "${EXIT_USAGE}"
          fi
          match_terms+=("${match_value}")
        fi
        shift
        ;;
      --match)
        die "Option '--match' requires '=TEXT'." "${EXIT_USAGE}"
        ;;
      --)
        shift
        break
        ;;
      -*)
        die "Unknown option: $1" "${EXIT_USAGE}"
        ;;
      *)
        break
        ;;
    esac
  done

  if (( show_help && show_version )); then
    die 'Options --help and --version cannot be combined.' "${EXIT_USAGE}"
  fi

  if (( $# > 3 )); then
    die 'Too many positional arguments.' "${EXIT_USAGE}"
  fi

  if (( show_help )); then
    print_help
    exit "${EXIT_OK}"
  fi

  if (( show_version )); then
    print_version
    exit "${EXIT_OK}"
  fi

  if (( $# == 0 )); then
    print_usage_error
    exit "${EXIT_USAGE}"
  fi

  command_name="$1"
  section="${2-0}"
  max_tokens="${3-${DEFAULT_MAX_TOKENS}}"

  validate_command_name "${command_name}"
  validate_section "${section}"
  validate_max_tokens "${max_tokens}"

  require_cmd 'man' 'Package: man-db. Installation requires user authorization.'
  require_cmd 'col' 'Package: bsdextrautils. Installation requires user authorization.'
  if (( ${#match_terms[@]} > 0 )); then
    require_cmd 'awk' 'Package: mawk or gawk. Installation requires user authorization.'
  fi

  man_bin="$(command -v 'man')"
  col_bin="$(command -v 'col')"
  if (( ${#match_terms[@]} > 0 )); then
    awk_bin="$(command -v 'awk')"
  fi

  fetch_man_page "${man_bin}" "${col_bin}" "${command_name}" "${section}"

  if (( ${#match_terms[@]} > 0 )); then
    extract_matching_excerpts \
      "${awk_bin}" \
      "${command_name}" \
      "${section}" \
      "${max_tokens}" \
      "${match_terms[@]}"
  else
    truncate_output "${MAN_PAGE_TEXT}" "${max_tokens}"
  fi
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
# Look up an installed manual page once using an isolated environment, strip
# overstrike formatting with col(1), optionally extract literal matching
# definitions, cross-references, or bounded context windows with --match=TEXT,
# and apply the approximate token budget after selection.
#
# OPTIONS
# --match=TEXT
#   Extract excerpts containing literal TEXT (repeatable, before positional
#   arguments). Regex metacharacters and leading hyphens are treated as plain
#   text.
# -h, --help
#   Show help and exit 0.
# -V, --version
#   Print version and exit 0.
# --
#   End option parsing.
#
# EXIT STATUS
# 0  success
# 1  no matching excerpt found for --match=TEXT
# 2  usage or validation error
# 3  missing dependency (man, col, or awk for --match)
# 4  no manual entry found
#
# EXAMPLES
# bash man_page_lookup.sh ls
# bash man_page_lookup.sh open 2
# bash man_page_lookup.sh printf 3posix 8000
# bash man_page_lookup.sh --match=--color ls 1
# bash man_page_lookup.sh --match=GuestExecStatus --match=guest-exec-status qemu-ga-ref 7
#
# SEE ALSO
# man(1), col(1), awk(1)
