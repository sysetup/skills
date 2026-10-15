#!/bin/bash
# Probe explicit external command names without executing them.
# SPDX-License-Identifier: MIT
# Part of: ops-tools; read-only stdout diagnostics.
set -euo pipefail

print_help() {
  printf '%s\n' \
    'Usage: discover-host-tools.sh [OPTIONS]... [NAME]...' \
    'Probe named external commands on PATH without executing them.' \
    'Options:' \
    '  -h, --help          Show help and exit.' \
    '  -V, --version       Print version and exit.' \
    '  -a, --all           Probe the bundled catalog.' \
    '  -c, --catalog FILE  Probe an explicit catalog instead of names.' \
    'Exit status: 0 success; 1 runtime error; 2 usage or input error.' \
    'Examples:' \
    '  bash discover-host-tools.sh git rg' \
    '  bash discover-host-tools.sh --all'
}

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit "$2"
}

# Validate the complete input, then probe PATH and print TSV records.
main() {
  local catalog='' root name found line available=0 missing=0
  local -a names=() records=()
  local -A seen=()
  local LC_ALL=C
  (($#)) || {
    print_help >&2
    return 2
  }
  while (($#)); do
    case "$1" in
      -h | --help)
        print_help
        return 0
        ;;
      -V | --version)
        printf '%s\n' 'discover-host-tools.sh 2.0.0'
        return 0
        ;;
      -a | --all)
        [[ -z "$catalog" ]] || fail 'catalog already selected' 2
        root=$(cd -- "${BASH_SOURCE[0]%/*}/.." && pwd -P) || return 1
        catalog="$root/assets/tool-catalog.txt"
        shift
        ;;
      -c | --catalog)
        if (($# < 2)) || [[ -z "$2" || "$2" == -* ]]; then
          fail '--catalog requires a file' 2
        fi
        [[ -z "$catalog" ]] || fail 'catalog already selected' 2
        catalog=$2
        shift 2
        ;;
      --)
        shift
        names+=("$@")
        break
        ;;
      -*) fail 'unknown option' 2 ;;
      *)
        names+=("$1")
        shift
        ;;
    esac
  done
  if [[ -n "$catalog" ]]; then
    (("${#names[@]}" == 0)) || fail 'catalog and names cannot be combined' 2
    [[ -f "$catalog" && -r "$catalog" ]] || fail 'catalog is not readable' 1
    mapfile -t names <"$catalog" || fail 'cannot read catalog' 1
    local -a entries=()
    for name in "${names[@]}"; do
      [[ -z "$name" || "$name" == \#* ]] || entries+=("$name")
    done
    names=("${entries[@]}")
  fi
  for name in "${names[@]}"; do
    [[ "$name" =~ ^[A-Za-z0-9][A-Za-z0-9._+-]*$ ]] \
      || fail 'invalid command name' 2
    [[ -z "${seen[$name]+present}" ]] || continue
    seen[$name]=1
    if found=$(type -P -- "$name"); then
      [[ "$found" != *[[:cntrl:]]* ]] \
        || fail 'executable locator contains control characters' 1
      records+=("AVAILABLE"$'\t'"$name"$'\t'"$found")
      available=$((available + 1))
    else
      records+=("MISSING"$'\t'"$name")
      missing=$((missing + 1))
    fi
  done
  (("${#records[@]}" > 0)) || fail 'no command names supplied' 2
  for line in "${records[@]}"; do printf '%s\n' "$line"; done
  printf 'SUMMARY\tavailable=%d\tmissing=%d\ttotal=%d\n' \
    "$available" "$missing" "${#records[@]}"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
