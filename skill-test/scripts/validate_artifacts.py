#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Stages 2-4: validate canonical evaluation-loop artifacts.

grading.json must use expectations[]{text, passed, evidence} exactly (the
viewer depends on these field names). timing.json must capture total_tokens
and duration_ms. benchmark.json follows the aggregate_benchmark.py contract.
"""

from __future__ import annotations

import sys
from pathlib import Path

from _common import (
    EXIT_OK,
    FAIL,
    PASS,
    SCHEMAS_DIR,
    WARNING,
    build_cli,
    die,
    load_json,
    parse_or_usage,
    resolve_reports_dir,
    save_stage,
    stage_result,
    validate_schema,
)

FORBIDDEN_EXPECTATION_KEYS = ("name", "met", "details")


def _load(path_text: str) -> tuple[Path, dict]:
    path = Path(path_text).expanduser()
    data = load_json(path, default=None)
    if data is None:
        die(f"File not found or unreadable JSON: {path}")
    return path, data


def _result(stage: str, findings: list[dict], **extra) -> dict:
    status = FAIL if any(row["severity"] == FAIL for row in findings) else PASS
    return stage_result(stage, status, findings, **extra)


def validate_grading(path_text: str) -> dict:
    path, data = _load(path_text)
    schema = load_json(SCHEMAS_DIR / "grading.schema.json")
    findings = [
        {
            "id": "G001",
            "severity": FAIL,
            "message": f"grading.json violates canonical schema: {error}",
            "location": str(path),
            "evidence": "Canonical shape: expectations[]{text, passed, evidence} (+ summary, timing)",
        }
        for error in validate_schema(data, schema)
    ]
    expectations = data.get("expectations")
    if isinstance(expectations, list):
        for index, item in enumerate(expectations):
            if not isinstance(item, dict):
                continue
            wrong = sorted(set(item) & set(FORBIDDEN_EXPECTATION_KEYS))
            if wrong:
                findings.append(
                    {
                        "id": "G002",
                        "severity": FAIL,
                        "message": f"expectations[{index}] uses forbidden field(s) {wrong}; must be text/passed/evidence",
                        "location": str(path),
                        "evidence": "Artifact reporting groups and renders these exact field names",
                    }
                )
    return _result("grading", findings, path=str(path.resolve()))


def validate_timing(path_text: str) -> dict:
    path, data = _load(path_text)
    schema = load_json(SCHEMAS_DIR / "timing.schema.json")
    findings = [
        {
            "id": "T001",
            "severity": FAIL,
            "message": f"timing.json violates canonical schema: {error}",
            "location": str(path),
            "evidence": "Capture total_tokens and duration_ms from the task notification immediately; they are not recoverable later",
        }
        for error in validate_schema(data, schema)
    ]
    return _result("timing", findings, path=str(path.resolve()))


def validate_metadata(path_text: str) -> dict:
    path, data = _load(path_text)
    schema = load_json(SCHEMAS_DIR / "eval-metadata.schema.json")
    findings = [
        {
            "id": "M001",
            "severity": FAIL,
            "message": f"eval_metadata.json violates canonical schema: {error}",
            "location": str(path),
            "evidence": "Canonical shape: eval_id, eval_name, prompt, assertions (may be empty while drafting)",
        }
        for error in validate_schema(data, schema)
    ]
    return _result("runs", findings, path=str(path.resolve()))


def validate_benchmark(path_text: str) -> dict:
    path, data = _load(path_text)
    schema = load_json(SCHEMAS_DIR / "benchmark.schema.json")
    findings = [
        {
            "id": "B001",
            "severity": FAIL,
            "message": f"benchmark.json violates canonical schema: {error}",
            "location": str(path),
            "evidence": "Generate it with scripts/aggregate_benchmark.py rather than writing it by hand",
        }
        for error in validate_schema(data, schema)
    ]
    runs = data.get("runs") if isinstance(data, dict) else None
    if isinstance(runs, list) and runs:
        with_skill = [r for r in runs if r.get("configuration") == "with_skill"]
        baseline = [
            r
            for r in runs
            if r.get("configuration") in {"without_skill", "old_skill"}
        ]
        if not with_skill or not baseline:
            findings.append(
                {
                    "id": "B002",
                    "severity": FAIL,
                    "message": "benchmark runs must include with_skill plus a baseline (without_skill or old_skill)",
                    "location": str(path),
                    "evidence": f"configurations found: {sorted({str(r.get('configuration')) for r in runs})}",
                }
            )
    return _result("benchmark", findings, path=str(path.resolve()))


def validate_iteration(path_text: str) -> dict:
    path = Path(path_text).expanduser()
    if not path.is_dir():
        die(f"Iteration directory not found: {path}")
    findings: list[dict] = []
    eval_dirs = sorted(
        d for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")
    )
    if not eval_dirs:
        findings.append(
            {
                "id": "R001",
                "severity": FAIL,
                "message": "no eval directories under the iteration directory",
                "location": str(path),
                "evidence": "Expected iteration-N/<eval-name>/ directories with with_skill/ and baseline runs",
            }
        )
    checked = 0
    for eval_dir in eval_dirs:
        checked += 1
        if not (eval_dir / "eval_metadata.json").is_file():
            findings.append(
                {
                    "id": "R002",
                    "severity": FAIL,
                    "message": f"missing eval_metadata.json in {eval_dir.name}",
                    "location": str(eval_dir),
                    "evidence": "Each test case directory needs eval_metadata.json",
                }
            )
        if not (eval_dir / "with_skill" / "outputs").is_dir():
            findings.append(
                {
                    "id": "R003",
                    "severity": FAIL,
                    "message": f"missing with_skill/outputs in {eval_dir.name}",
                    "location": str(eval_dir),
                    "evidence": "Canonical layout: <eval>/with_skill/outputs/",
                }
            )
        baselines = [
            d
            for d in ("without_skill", "old_skill")
            if (eval_dir / d / "outputs").is_dir()
        ]
        if not baselines:
            findings.append(
                {
                    "id": "R004",
                    "severity": FAIL,
                    "message": f"missing baseline (without_skill/ or old_skill/) in {eval_dir.name}",
                    "location": str(eval_dir),
                        "evidence": "The evaluation loop launches with-skill AND baseline runs in the same turn",
                }
            )
        for run_dir in ("with_skill", "without_skill", "old_skill"):
            run_path = eval_dir / run_dir
            if run_path.is_dir() and not (run_path / "grading.json").is_file():
                findings.append(
                    {
                        "id": "R005",
                        "severity": WARNING,
                        "message": f"grading.json pending in {eval_dir.name}/{run_dir}",
                        "location": str(run_path),
                        "evidence": "Grade each run once its outputs are complete",
                    }
                )
    return _result("runs", findings, path=str(path.resolve()), eval_dirs=checked)


def main(argv: list[str] | None = None) -> int:
    parser = build_cli(
        "validate_artifacts.py",
        "Stages 2-4: validate canonical evaluation-loop artifacts.",
        epilog=(
            "SUBCOMMANDS\n"
            "  grading GRADING_JSON      expectations[]{text, passed, evidence} contract\n"
            "  timing TIMING_JSON        total_tokens / duration_ms contract\n"
            "  metadata METADATA_JSON    eval_metadata.json contract\n"
            "  benchmark BENCHMARK_JSON  aggregate_benchmark.py output contract\n"
            "  iteration ITERATION_DIR   run-directory layout contract\n"
            "\n"
            "EXIT STATUS\n"
            "  0  PASS (warnings allowed)\n"
            "  1  FAIL or missing input\n"
            "  2  usage error\n"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for label, func in (
        ("grading", validate_grading),
        ("timing", validate_timing),
        ("metadata", validate_metadata),
        ("benchmark", validate_benchmark),
        ("iteration", validate_iteration),
    ):
        child = sub.add_parser(label, help=f"validate {label} artifact")
        child.add_argument("path", metavar="PATH")
        child.set_defaults(func=func)

    args = parse_or_usage(parser, argv)
    result = args.func(args.path)
    reports_dir = resolve_reports_dir(args.reports_dir)
    result_path = save_stage(reports_dir, result)
    for row in result["findings"]:
        if row["severity"] == FAIL:
            print(f"FAIL {row['id']}: {row['message']}", file=sys.stderr)
    print(f"{result['stage']}: {result['status']} -> {result_path}")
    return EXIT_OK if result["status"] == PASS else 1


if __name__ == "__main__":
    sys.exit(main())
