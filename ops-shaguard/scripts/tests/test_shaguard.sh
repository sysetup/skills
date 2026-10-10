#!/bin/bash
# Behavioral tests for shaguard. Uses only Bash and common Linux utilities.

set -Eeuo pipefail
IFS=$'\n\t'
LC_ALL=C
export LC_ALL

TEST_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_DIR="$(cd -- "${TEST_DIR}/.." && pwd -P)"
readonly TEST_DIR PROJECT_DIR
readonly -a SUT=(bash "${PROJECT_DIR}/bin/shaguard")

pass_count=0
fail_count=0
sandbox=""

cleanup() {
  if [[ -n "$sandbox" && -d "$sandbox" ]]; then
    rm -rf -- "$sandbox"
  fi
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

pass() {
  printf 'PASS: %s\n' "$1"
  pass_count=$((pass_count + 1))
}

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  fail_count=$((fail_count + 1))
}

assert_status() {
  local name="$1"
  local expected="$2"
  shift 2
  local status=0

  "$@" >/dev/null 2>&1 || status=$?
  if [[ "$status" -eq "$expected" ]]; then
    pass "$name"
  else
    fail "${name} (expected ${expected}, got ${status})"
  fi
}

run_tests() {
  local expected
  local manifest
  local output

  sandbox="$(mktemp -d "${TMPDIR:-/tmp}/shaguard-test.XXXXXX")"
  mkdir -p -- "$sandbox/tree/sub"
  printf 'alpha\n' >"$sandbox/tree/a.txt"
  printf 'beta\n' >"$sandbox/tree/sub/b.txt"
  printf 'ignore\n' >"$sandbox/tree/skip.tmp"
  printf 'slash\n' >"$sandbox/tree/back\\slash"
  printf 'newline\n' >"$sandbox/tree/"$'line\nbreak'

  assert_status "zero arguments are safe" 0 "${SUT[@]}"
  assert_status "selftest passes" 0 "${SUT[@]}" selftest
  assert_status "help help succeeds" 0 "${SUT[@]}" help help
  output="$("${SUT[@]}" help help 2>/dev/null)" || output=""
  if [[ "$output" == "Usage: shaguard help [COMMAND]" ]]; then
    pass "help help prints its usage"
  else
    fail "help help prints its usage"
  fi

  expected="$(sha256sum -- "$sandbox/tree/a.txt")"
  expected="${expected:0:64}"
  output="$("${SUT[@]}" hash "$sandbox/tree/a.txt")"
  if [[ "$output" == "$expected"* ]]; then
    pass "hash emits the expected digest"
  else
    fail "hash emits the expected digest"
  fi

  assert_status "compare accepts a matching digest" 0 \
    "${SUT[@]}" compare "$expected" "$sandbox/tree/a.txt"
  assert_status "compare rejects a wrong digest" 4 \
    "${SUT[@]}" compare \
    "0000000000000000000000000000000000000000000000000000000000000000" \
    "$sandbox/tree/a.txt"

  manifest="$sandbox/tree/SHA256SUMS"
  assert_status "manifest generation succeeds" 0 \
    "${SUT[@]}" manifest -x '*.tmp' "$sandbox/tree"

  if [[ -f "$manifest" ]] && ! grep -q 'skip.tmp' "$manifest"; then
    pass "manifest exclusion works"
  else
    fail "manifest exclusion works"
  fi

  assert_status "manifest verifies with escaped filenames" 0 \
    "${SUT[@]}" verify "$manifest"

  printf 'changed\n' >"$sandbox/tree/sub/b.txt"
  assert_status "content modification is detected" 4 \
    "${SUT[@]}" verify -q "$manifest"
  printf 'beta\n' >"$sandbox/tree/sub/b.txt"

  printf '%064d  ../escape\n' 0 >"$sandbox/bad-traversal"
  assert_status "parent traversal is rejected" 6 \
    "${SUT[@]}" verify -r "$sandbox/tree" "$sandbox/bad-traversal"

  mkdir -p -- "$sandbox/outside"
  printf 'outside\n' >"$sandbox/outside/secret"
  ln -s -- "$sandbox/outside" "$sandbox/tree/link"
  expected="$(sha256sum -- "$sandbox/outside/secret")"
  expected="${expected:0:64}"
  printf '%s  link/secret\n' "$expected" >"$sandbox/bad-symlink"
  assert_status "symlink traversal is rejected" 6 \
    "${SUT[@]}" verify -r "$sandbox/tree" "$sandbox/bad-symlink"

  rm -f -- "$sandbox/tree/dry-manifest"
  assert_status "dry run succeeds" 0 \
    "${SUT[@]}" manifest -n -o "$sandbox/tree/dry-manifest" "$sandbox/tree"
  if [[ ! -e "$sandbox/tree/dry-manifest" ]]; then
    pass "dry run writes nothing"
  else
    fail "dry run writes nothing"
  fi

  assert_status "existing manifest requires force" 2 \
    "${SUT[@]}" manifest "$sandbox/tree"
  assert_status "force replaces manifest" 0 \
    "${SUT[@]}" manifest -f -x '*.tmp' "$sandbox/tree"

  printf '\nTests passed: %d\n' "$pass_count"
  printf 'Tests failed: %d\n' "$fail_count"

  ((fail_count == 0))
}

run_tests
