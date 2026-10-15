#!/usr/bin/env bats
# Observable contracts for the local diagnostics; no host mutations.

setup() {
  bats_require_minimum_version 1.5.0
  tools_root="$BATS_TEST_DIRNAME/.."
}

@test "diagnostic help succeeds before target inspection" {
  for script in load-skill.sh discover-host-tools.sh; do
    run bash "$tools_root/scripts/$script" --help
    [ "$status" -eq 0 ]
    [[ "$output" == *Usage:* ]]
  done
}

@test "zero arguments and unknown options fail safely" {
  for script in load-skill.sh discover-host-tools.sh; do
    run bash "$tools_root/scripts/$script"
    [ "$status" -eq 2 ]
    run bash "$tools_root/scripts/$script" --unknown
    [ "$status" -eq 2 ]
  done
}

@test "package check succeeds without external runtimes" {
  run env PATH= /bin/bash "$tools_root/scripts/load-skill.sh" ops-tools
  [ "$status" -eq 0 ]
  [ "$output" = "OK: loaded ops-tools" ]
}

@test "package identity and empty end-of-options are rejected" {
  run bash "$tools_root/scripts/load-skill.sh" wrong-name
  [ "$status" -eq 2 ]
  run bash "$tools_root/scripts/load-skill.sh" --
  [ "$status" -eq 2 ]
}

@test "named inventory records present and missing external tools" {
  run bash "$tools_root/scripts/discover-host-tools.sh" bash ops-tools-unavailable-demo
  [ "$status" -eq 0 ]
  [[ "$output" == *$'AVAILABLE\tbash\t'* ]]
  [[ "$output" == *$'MISSING\tops-tools-unavailable-demo'* ]]
  [[ "$output" == *$'SUMMARY\tavailable=1\tmissing=1\ttotal=2'* ]]
}

@test "duplicate input preserves first-occurrence order" {
  run bash "$tools_root/scripts/discover-host-tools.sh" bash bash ops-tools-unavailable-demo
  [ "$status" -eq 0 ]
  [[ "$output" == *total=2 ]]
  [[ "${lines[0]}" == $'AVAILABLE\tbash\t'* ]]
  [[ "${lines[1]}" == $'MISSING\tops-tools-unavailable-demo' ]]
}

@test "builtin-only names are not external executables" {
  run bash "$tools_root/scripts/discover-host-tools.sh" mapfile
  [ "$status" -eq 0 ]
  [[ "$output" == $'MISSING\tmapfile'* ]]
}

@test "invalid names never publish a partial inventory" {
  run --separate-stderr bash "$tools_root/scripts/discover-host-tools.sh" bash ../invalid
  [ "$status" -eq 2 ]
  [ -z "$output" ]
  [[ "$stderr" == FAIL:* ]]
}

@test "empty and comment operands fail rather than being ignored" {
  run bash "$tools_root/scripts/discover-host-tools.sh" bash ""
  [ "$status" -eq 2 ]
  run bash "$tools_root/scripts/discover-host-tools.sh" bash "#not-a-name"
  [ "$status" -eq 2 ]
}

@test "catalog mode is explicit and cannot mix with names" {
  run bash "$tools_root/scripts/discover-host-tools.sh" --all
  [ "$status" -eq 0 ]
  [[ "$output" == *SUMMARY* ]]
  run bash "$tools_root/scripts/discover-host-tools.sh" --all bash
  [ "$status" -eq 2 ]
}

@test "missing catalog values and inaccessible catalogs are diagnosed" {
  run bash "$tools_root/scripts/discover-host-tools.sh" --catalog
  [ "$status" -eq 2 ]
  run bash "$tools_root/scripts/discover-host-tools.sh" --catalog "$BATS_TEST_DIRNAME/absent-catalog"
  [ "$status" -eq 1 ]
}

@test "retired file-output options fail without writes" {
  run bash "$tools_root/scripts/discover-host-tools.sh" --output ignored-output
  [ "$status" -eq 2 ]
  [ ! -e ignored-output ]
}

@test "repeat probes have stable records for unchanged PATH" {
  run bash "$tools_root/scripts/discover-host-tools.sh" bash ops-tools-unavailable-demo
  [ "$status" -eq 0 ]
  first="$output"
  run bash "$tools_root/scripts/discover-host-tools.sh" bash ops-tools-unavailable-demo
  [ "$status" -eq 0 ]
  [ "$output" = "$first" ]
}
