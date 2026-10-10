#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Aggregate stage results into the final skill-test report.

Reads whatever stage JSONs exist under --reports-dir and emits report.md +
report.json. Overall verdict: READY FOR EVAL LOOP when every recorded stage
passes, otherwise BLOCKED: <first failing stage>. There are no L-levels.
"""

from __future__ import annotations

import sys
from pathlib import Path

from _common import (
    EXIT_OK,
    EXIT_USAGE,
    FAIL,
    PASS,
    STAGE_FILES,
    TEMPLATES_DIR,
    WARNING,
    build_cli,
    die,
    load_json,
    parse_or_usage,
    read_text,
    resolve_reports_dir,
    save_json,
    write_text_file,
)


def aggregate(reports_dir: Path, skill_name: str) -> dict:
    """Load stage results in canonical loop order."""
    stages = []
    for stage, filename in STAGE_FILES.items():
        path = reports_dir / filename
        if path.is_file():
            stages.append(load_json(path))
    if not stages:
        die(f"No stage results found under {reports_dir}; run pipeline stages first")
    failing = [s["stage"] for s in stages if s.get("status") == FAIL]
    overall = (
        f"BLOCKED: {failing[0]} stage failed"
        if failing
        else "READY FOR EVAL LOOP"
    )
    return {
        "skill_name": skill_name,
        "overall": overall,
        "stages": stages,
    }


def render_markdown(report: dict, template: str) -> str:
    """Fill templates/report-template.md placeholders."""
    stage_rows = []
    for stage in report["stages"]:
        counts = {level: 0 for level in (FAIL, WARNING, "ADVICE")}
        for row in stage.get("findings", []):
            if row.get("severity") in counts:
                counts[row["severity"]] += 1
        stage_rows.append(
            f"| {stage['stage']} | {stage['status']} | {counts[FAIL]} | "
            f"{counts[WARNING]} | {counts['ADVICE']} |"
        )
    findings_lines = []
    for stage in report["stages"]:
        for row in stage.get("findings", []):
            if row.get("severity") == FAIL:
                findings_lines.append(
                    f"- **{stage['stage']} / {row['id']}**: {row['message']} "
                    f"({row.get('location', '')})"
                )
    next_step = (
        "Fix the first failing stage, then rerun it and this report."
        if report["overall"].startswith("BLOCKED")
        else "Continue the evaluation loop: launch/finish runs, grade, benchmark, review, improve."
    )
    text = template
    for placeholder, value in (
        ("__SKILL_NAME__", report["skill_name"] or "unknown-skill"),
        ("__OVERALL__", report["overall"]),
        ("__STAGE_TABLE__", "\n".join(stage_rows) or "| — | — | — | — | — |"),
        ("__FAILING_FINDINGS__", "\n".join(findings_lines) or "- None."),
        ("__NEXT_STEP__", next_step),
    ):
        text = text.replace(placeholder, value)
    return text


def main(argv: list[str] | None = None) -> int:
    parser = build_cli(
        "report.py",
        "Aggregate stage results into report.md and report.json (no L-levels).",
        epilog=(
            "EXIT STATUS\n"
            "  0  READY FOR EVAL LOOP\n"
            "  1  BLOCKED (a recorded stage failed) or nothing to aggregate\n"
            "  2  usage error\n"
        ),
    )
    parser.add_argument(
        "--skill-name", default=None, help="Skill name for the report header"
    )
    args = parse_or_usage(parser, argv)
    if argv is not None and not argv:
        parser.print_help(sys.stderr)
        raise SystemExit(EXIT_USAGE)
    reports_dir = resolve_reports_dir(args.reports_dir)
    report = aggregate(reports_dir, args.skill_name or "")
    if not report["skill_name"]:
        preflight = next(
            (s for s in report["stages"] if s["stage"] == "preflight"), None
        )
        report["skill_name"] = (
            (preflight or {}).get("skill", {}).get("name") or "unknown-skill"
        )
    save_json(reports_dir / "report.json", report)
    template = read_text(TEMPLATES_DIR / "report-template.md")
    write_text_file(reports_dir / "report.md", render_markdown(report, template))
    print(f"Overall: {report['overall']}")
    print(f"Artifacts generated in {reports_dir}/ - See report.md")
    return EXIT_OK if not report["overall"].startswith("BLOCKED") else 1


if __name__ == "__main__":
    sys.exit(main())
