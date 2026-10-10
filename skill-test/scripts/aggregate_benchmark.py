#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Aggregate completed evaluation-loop artifacts into benchmark files.

Reads grading.json and timing.json artifacts from an iteration directory and
writes benchmark.json plus benchmark.md. The script validates the input layout
and never launches a target skill.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from _common import EXIT_OK, die, load_json, write_text_file


CONFIG_ORDER = ("with_skill", "without_skill", "old_skill")
BASELINE_ORDER = ("without_skill", "old_skill")


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _required_json(path: Path) -> dict:
    if not path.is_file():
        die(f"Required file not found: {path}")
    data = load_json(path, default=None)
    if not isinstance(data, dict):
        die(f"Expected a JSON object in {path}")
    return data


def _number(value: Any, default: float = 0.0) -> float:
    return value if _is_number(value) else default


def _integer(value: Any, default: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        return default
    return value


def _grading_run_dirs(config_dir: Path) -> list[tuple[int, Path]]:
    """Return graded runs in canonical single-run and repeated-run layouts."""
    runs: list[tuple[int, Path]] = []
    for run_dir in sorted(config_dir.glob("run-*")):
        if not run_dir.is_dir() or not (run_dir / "grading.json").is_file():
            continue
        try:
            run_number = int(run_dir.name.split("-", 1)[1])
        except (IndexError, ValueError):
            continue
        runs.append((run_number, run_dir))
    if (config_dir / "grading.json").is_file():
        runs.append((1, config_dir))
    return runs


def _run_result(eval_id: int, run_number: int, run_dir: Path) -> dict:
    grading = _required_json(run_dir / "grading.json")
    summary = grading.get("summary") if isinstance(grading.get("summary"), dict) else {}
    nested_timing = (
        grading.get("timing") if isinstance(grading.get("timing"), dict) else {}
    )
    metrics = (
        grading.get("execution_metrics")
        if isinstance(grading.get("execution_metrics"), dict)
        else {}
    )

    timing: dict = {}
    timing_path = run_dir / "timing.json"
    if timing_path.is_file():
        timing = _required_json(timing_path)

    time_seconds = _number(nested_timing.get("total_duration_seconds"))
    if time_seconds == 0:
        time_seconds = _number(timing.get("total_duration_seconds"))
    if time_seconds == 0 and _is_number(timing.get("duration_ms")):
        time_seconds = float(timing["duration_ms"]) / 1000

    tokens = timing.get("total_tokens")
    if not isinstance(tokens, int) or isinstance(tokens, bool):
        tokens = _integer(metrics.get("output_chars"))

    expectations = grading.get("expectations")
    if not isinstance(expectations, list):
        expectations = []

    notes_summary = (
        grading.get("user_notes_summary")
        if isinstance(grading.get("user_notes_summary"), dict)
        else {}
    )
    notes = []
    for key in ("uncertainties", "needs_review", "workarounds"):
        values = notes_summary.get(key)
        if isinstance(values, list):
            notes.extend(str(value) for value in values)

    return {
        "eval_id": eval_id,
        "run_number": run_number,
        "pass_rate": _number(summary.get("pass_rate")),
        "passed": _integer(summary.get("passed")),
        "failed": _integer(summary.get("failed")),
        "total": _integer(summary.get("total")),
        "time_seconds": time_seconds,
        "tokens": tokens,
        "tool_calls": _integer(metrics.get("total_tool_calls")),
        "errors": _integer(metrics.get("errors_encountered")),
        "expectations": expectations,
        "notes": notes,
    }


def load_run_results(iteration_dir: Path) -> dict[str, list[dict]]:
    """Load graded results while preserving canonical configuration order."""
    if not iteration_dir.is_dir():
        die(f"Iteration directory not found: {iteration_dir}")

    search_dir = iteration_dir / "runs" if (iteration_dir / "runs").is_dir() else iteration_dir
    eval_dirs = sorted(path for path in search_dir.iterdir() if path.is_dir())
    if not eval_dirs:
        die(f"No eval directories found under {search_dir}")

    loaded: dict[str, list[dict]] = {}
    for fallback_id, eval_dir in enumerate(eval_dirs):
        metadata = _required_json(eval_dir / "eval_metadata.json")
        eval_id = metadata.get("eval_id", fallback_id)
        if isinstance(eval_id, bool) or not isinstance(eval_id, int):
            eval_id = fallback_id

        for config in CONFIG_ORDER:
            config_dir = eval_dir / config
            if not config_dir.is_dir():
                continue
            for run_number, run_dir in _grading_run_dirs(config_dir):
                loaded.setdefault(config, []).append(
                    _run_result(eval_id, run_number, run_dir)
                )

    if not loaded:
        die(f"No graded runs found under {search_dir}")
    if "with_skill" not in loaded or not any(config in loaded for config in BASELINE_ORDER):
        die("Benchmark input needs with_skill runs plus a without_skill or old_skill baseline")
    return loaded


def calculate_stats(values: list[float]) -> dict[str, float]:
    """Return mean, sample standard deviation, minimum, and maximum."""
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}
    mean = sum(values) / len(values)
    stddev = (
        math.sqrt(sum((value - mean) ** 2 for value in values) / (len(values) - 1))
        if len(values) > 1
        else 0.0
    )
    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def aggregate_results(results: dict[str, list[dict]]) -> dict[str, Any]:
    """Calculate per-configuration statistics and the primary-baseline delta."""
    run_summary: dict[str, Any] = {}
    for config, runs in results.items():
        run_summary[config] = {
            "pass_rate": calculate_stats([float(run["pass_rate"]) for run in runs]),
            "time_seconds": calculate_stats([float(run["time_seconds"]) for run in runs]),
            "tokens": calculate_stats([float(run["tokens"]) for run in runs]),
        }

    baseline = next((config for config in BASELINE_ORDER if config in run_summary), None)
    if "with_skill" not in run_summary or baseline is None:
        return run_summary

    primary = run_summary["with_skill"]
    comparison = run_summary[baseline]
    delta_pass_rate = (
        primary["pass_rate"]["mean"] - comparison["pass_rate"]["mean"]
    )
    delta_time = (
        primary["time_seconds"]["mean"] - comparison["time_seconds"]["mean"]
    )
    delta_tokens = primary["tokens"]["mean"] - comparison["tokens"]["mean"]
    run_summary["delta"] = {
        "pass_rate": f"{delta_pass_rate:+.2f}",
        "time_seconds": f"{delta_time:+.1f}",
        "tokens": f"{delta_tokens:+.0f}",
    }
    return run_summary


def generate_benchmark(
    iteration_dir: Path, skill_name: str, skill_path: str = ""
) -> dict[str, Any]:
    """Build the complete benchmark object from an iteration directory."""
    results = load_run_results(iteration_dir)
    runs = [
        {
            "eval_id": result["eval_id"],
            "configuration": config,
            "run_number": result["run_number"],
            "result": {
                key: result[key]
                for key in (
                    "pass_rate",
                    "passed",
                    "failed",
                    "total",
                    "time_seconds",
                    "tokens",
                    "tool_calls",
                    "errors",
                )
            },
            "expectations": result["expectations"],
            "notes": result["notes"],
        }
        for config in CONFIG_ORDER
        for result in results.get(config, [])
    ]
    eval_ids = sorted(
        {
            int(result["eval_id"])
            for runs in results.values()
            for result in runs
        }
    )

    return {
        "metadata": {
            "skill_name": skill_name,
            "skill_path": skill_path or str(iteration_dir),
            "executor_model": "<model-name>",
            "analyzer_model": "<model-name>",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "evals_run": eval_ids,
            "runs_per_configuration": max(len(rows) for rows in results.values()),
        },
        "runs": runs,
        "run_summary": aggregate_results(results),
        "notes": [],
    }


def generate_markdown(benchmark: dict[str, Any]) -> str:
    """Render a compact benchmark summary suitable for review."""
    metadata = benchmark["metadata"]
    summary = benchmark["run_summary"]
    baseline = next((config for config in BASELINE_ORDER if config in summary), None)
    delta = summary.get("delta", {})
    primary = summary.get("with_skill", {})
    comparison = summary.get(baseline, {}) if baseline else {}

    def metric(name: str, scale: float = 1.0, suffix: str = "") -> str:
        left = primary.get(name, {}).get("mean", 0) * scale
        right = comparison.get(name, {}).get("mean", 0) * scale
        change = delta.get(name, "—")
        label = name.replace("_", " ").title()
        return (
            f"| {label} | {left:g}{suffix} | {right:g}{suffix} "
            f"| {change}{suffix} |"
        )

    return "\n".join(
        [
            f"# Skill Benchmark: {metadata['skill_name']}",
            "",
            f"**Date:** {metadata['timestamp']}",
            f"**Evals:** {', '.join(str(value) for value in metadata['evals_run'])}",
            "",
            f"| Metric | With Skill | {baseline or 'Baseline'} | Delta |",
            "|---|---:|---:|---:|",
            metric("pass_rate", 100, "%"),
            metric("time_seconds", 1, "s"),
            metric("tokens"),
            "",
        ]
    )


def write_benchmark(benchmark: dict[str, Any], output: Path) -> tuple[Path, Path]:
    """Write the JSON and Markdown benchmark outputs."""
    if output.exists() and output.is_dir():
        die(f"Output path is a directory: {output}")
    markdown_path = output.with_suffix(".md")
    write_text_file(output, json.dumps(benchmark, indent=2, ensure_ascii=False) + "\n")
    write_text_file(markdown_path, generate_markdown(benchmark))
    return output, markdown_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="aggregate_benchmark.py",
        description="Aggregate grading and timing artifacts into benchmark.json and benchmark.md.",
        epilog=(
            "EXIT STATUS\n"
            "  0  benchmark generated\n"
            "  1  missing or invalid artifact\n"
            "  2  usage error\n"
        ),
    )
    parser.add_argument("iteration_dir", metavar="ITERATION_DIR", type=Path)
    parser.add_argument("--skill-name", required=True, help="Name of the evaluated skill")
    parser.add_argument("--skill-path", default="", help="Optional path of the evaluated skill")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="benchmark.json path (default: ITERATION_DIR/benchmark.json)",
    )
    args = parser.parse_args(argv)

    benchmark = generate_benchmark(
        args.iteration_dir.expanduser(), args.skill_name, args.skill_path
    )
    output = args.output or args.iteration_dir.expanduser() / "benchmark.json"
    json_path, markdown_path = write_benchmark(benchmark, output)
    print(f"Generated: {json_path}")
    print(f"Generated: {markdown_path}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
