#!/usr/bin/env bats

setup() {
  script="${BATS_TEST_DIRNAME}/../scripts/man_page_lookup.sh"
}

@test "help succeeds and zero arguments fail safely" {
  run bash "${script}" --help
  [ "${status}" -eq 0 ]
  [[ "${output}" == Usage:* ]]
  run bash "${script}"
  [ "${status}" -eq 2 ]
}

@test "budgets outside the declared range are rejected" {
  for budget in 0 99 100001 18446744073709551716; do
    run bash "${script}" ls 1 "${budget}"
    [ "${status}" -eq 2 ]
    [[ "${output}" == ERROR:* ]]
  done
}

@test "leading zeros are rejected without octal evaluation" {
  for budget in 0100 0800 000144; do
    run bash "${script}" ls 1 "${budget}"
    [ "${status}" -eq 2 ]
    [[ "${output}" == ERROR:* ]]
    [[ "${output}" != *"error token"* ]]
  done
}

@test "empty and nondecimal budgets are rejected" {
  for budget in '' -1 1.5 1e3 '100+1' ' 100'; do
    run bash "${script}" ls 1 "${budget}"
    [ "${status}" -eq 2 ]
  done
}

@test "an explicit empty section is rejected" {
  run bash "${script}" ls '' 100
  [ "${status}" -eq 2 ]
}

@test "paths and shell syntax cannot become manual names" {
  for name in /etc/passwd a..b 'ls;true'; do
    run bash "${script}" "${name}"
    [ "${status}" -eq 2 ]
  done
}

@test "ordinary lookup accepts both budget boundaries and defaults" {
  command -v man >/dev/null || skip "man is unavailable"
  command -v col >/dev/null || skip "col is unavailable"
  for budget in 100 99999 100000; do
    run bash "${script}" ls 1 "${budget}"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"LS(1)"* ]]
  done
  run bash "${script}" ls
  [ "${status}" -eq 0 ]
}

@test "missing manual returns four without a section fallback" {
  command -v man >/dev/null || skip "man is unavailable"
  command -v col >/dev/null || skip "col is unavailable"
  run bash "${script}" ls unavailable-section-4821 100
  [ "${status}" -eq 4 ]
  [[ "${output}" == *"in section unavailable-section-4821"* ]]
}

@test "caller man options and pagers do not alter a lookup" {
  command -v man >/dev/null || skip "man is unavailable"
  command -v col >/dev/null || skip "col is unavailable"
  run env MANOPT=--version MANPAGER=false PAGER=false \
    bash "${script}" ls 1 100
  [ "${status}" -eq 0 ]
  [[ "${output}" == *"LS(1)"* ]]
}

@test "absolute script path works outside the skill directory" {
  command -v man >/dev/null || skip "man is unavailable"
  command -v col >/dev/null || skip "col is unavailable"
  run bash -c 'cd / && bash "$1" ls 1 100' bash "${script}"
  [ "${status}" -eq 0 ]
  [[ "${output}" == *"LS(1)"* ]]
}

@test "missing dependencies return three with a named diagnostic" {
  for dependency in man col; do
    run bash -c '
      missing=$2
      source "$1"
      command() {
        if [[ "$1" == -v && "$2" == "${missing}" ]]; then
          return 1
        fi
        builtin command "$@"
      }
      main ls
    ' bash "${script}" "${dependency}"
    [ "${status}" -eq 3 ]
    [[ "${output}" == *"Required command '${dependency}' is not installed."* ]]
  done
}

@test "version succeeds and unknown options and extra operands fail" {
  run bash "${script}" --version
  [ "${status}" -eq 0 ]
  [[ "${output}" == man_page_lookup.sh* ]]
  run bash "${script}" --unsupported
  [ "${status}" -eq 2 ]
  run bash "${script}" ls 1 100 extra
  [ "${status}" -eq 2 ]
}
