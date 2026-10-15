#!/bin/bash
# Check package consistency without executing bundled scripts.
# SPDX-License-Identifier: MIT
# Part of: ops-tools; read-only maintenance diagnostic.
set -euo pipefail

print_help() {
  printf '%s\n' \
    'Usage: load-skill.sh [OPTIONS]... SKILL_NAME' \
    'Check the ops-tools package identity, resources, and Bash syntax.' \
    'Options:' \
    '  -h, --help      Show help and exit.' \
    '  -V, --version   Print version and exit.' \
    'Exit status: 0 success; 1 package error; 2 usage error.' \
    'Example: bash load-skill.sh ops-tools'
}

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit "$2"
}

# Shallow identity/resource check; full YAML validation is a separate check.
main() {
  local root line name='' closed=0 path
  (($#)) || {
    print_help >&2
    return 2
  }
  case "$1" in
    -h | --help)
      print_help
      return 0
      ;;
    -V | --version)
      printf '%s\n' 'load-skill.sh 2.0.0'
      return 0
      ;;
    --) shift ;;
    -*) fail 'unknown option' 2 ;;
  esac
  if (($# != 1)) || [[ "$1" != ops-tools ]]; then
    fail 'exactly one skill name, ops-tools, is required' 2
  fi
  root=$(cd -- "${BASH_SOURCE[0]%/*}/.." && pwd -P) || return 1
  [[ "${root##*/}" == ops-tools ]] || fail 'package directory mismatch' 1
  [[ -f "$root/SKILL.md" && -r "$root/SKILL.md" ]] \
    || fail 'SKILL.md is not readable' 1
  {
    IFS= read -r line || fail 'empty SKILL.md' 1
    [[ "$line" == --- ]] || fail 'missing frontmatter' 1
    while IFS= read -r line; do
      [[ "$line" != --- ]] || {
        closed=1
        break
      }
      [[ "$line" != 'name: '* ]] || name="${line#name: }"
    done
  } <"$root/SKILL.md"
  [[ "$name" == ops-tools && "$closed" == 1 ]] \
    || fail 'invalid package identity or unclosed frontmatter' 1
  for path in references/tool-selection.md references/safety.md \
    references/output-contract.md assets/tool-catalog.txt \
    scripts/discover-host-tools.sh scripts/load-skill.sh; do
    [[ -f "$root/$path" && -r "$root/$path" ]] \
      || fail "missing or unreadable resource: $path" 1
  done
  for path in scripts/load-skill.sh scripts/discover-host-tools.sh; do
    "$BASH" -n "$root/$path" || fail 'invalid Bash syntax' 1
  done
  printf '%s\n' 'OK: loaded ops-tools'
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
