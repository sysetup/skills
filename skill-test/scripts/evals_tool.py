#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Stage 1: evals/evals.json init, validation, and canonical workspace scaffolding.

Shapes come from the local schemas/ directory. evals[].expectations is the
canonical expectations field; drafting prose may say "assertions," but the
schema defines expectations.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from _common import (
    EXIT_OK,
    FAIL,
    PASS,
    SCHEMAS_DIR,
    TEMPLATES_DIR,
    WARNING,
    build_cli,
    die,
    load_json,
    parse_or_usage,
    read_text,
    require_yaml,
    resolve_reports_dir,
    save_json,
    save_stage,
    stage_result,
    validate_schema,
)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
EVAL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BASELINE_DIRS = {"without": "without_skill", "old": "old_skill"}


def _skill_name(skill_dir: Path) -> str:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        die(f"SKILL.md not found: {skill_md}")
    yaml = require_yaml()
    match = FRONTMATTER_RE.match(read_text(skill_md))
    if not match:
        die(f"No YAML frontmatter in {skill_md}")
    try:
        loaded = yaml.safe_load(match.group(1))
    except Exception as exc:
        die(f"Invalid YAML frontmatter in {skill_md}: {exc}")
    name = (loaded or {}).get("name") if isinstance(loaded, dict) else None
    if not isinstance(name, str) or not name.strip():
        die(f"frontmatter name missing in {skill_md}")
    return name.strip()


def validate_evals(path: Path) -> dict:
    """Validate evals/evals.json against the canonical schema."""
    data = load_json(path, default=None)
    if data is None:
        die(f"File not found or unreadable JSON: {path}")
    schema = load_json(SCHEMAS_DIR / "evals.schema.json")
    findings: list[dict] = []
    errors = validate_schema(data, schema)
    for error in errors:
        findings.append(
            {
                "id": "E001",
                "severity": FAIL,
                "message": f"evals.json violates canonical schema: {error}",
                "location": str(path),
                "evidence": "Canonical shape: skill_name + evals[]{id, prompt, expected_output, files?, expectations?}",
            }
        )
    evals = data.get("evals") if isinstance(data, dict) else None
    if isinstance(evals, list):
        ids = [row.get("id") for row in evals if isinstance(row, dict)]
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        if duplicates:
            findings.append(
                {
                    "id": "E002",
                    "severity": FAIL,
                    "message": f"duplicate eval ids: {duplicates}",
                    "location": str(path),
                    "evidence": "evals[].id must be a unique integer identifier",
                }
            )
        if not evals:
            findings.append(
                {
                    "id": "E003",
                    "severity": WARNING,
                    "message": "evals list is empty (draft state)",
                    "location": str(path),
                    "evidence": "Add 2-3 realistic test prompts per the evaluation loop",
                }
            )
        if data.get("skill_name") and isinstance(data.get("skill_name"), str):
            skill_md = path.resolve().parent.parent / "SKILL.md"
            if skill_md.is_file():
                declared = _skill_name(skill_md.parent)
                if declared != data["skill_name"]:
                    findings.append(
                        {
                            "id": "E004",
                            "severity": FAIL,
                            "message": f"skill_name {data['skill_name']!r} does not match frontmatter name {declared!r}",
                            "location": str(path),
                            "evidence": "skill_name must match the skill's frontmatter name",
                        }
                    )
    status = FAIL if any(row["severity"] == FAIL for row in findings) else PASS
    return stage_result(
        "evals",
        status,
        findings,
        path=str(path.resolve()),
        eval_count=len(evals) if isinstance(evals, list) else 0,
    )


def cmd_init(args: argparse.Namespace) -> int:
    skill_dir = Path(args.skill_dir).expanduser().resolve()
    name = _skill_name(skill_dir)
    evals_path = skill_dir / "evals" / "evals.json"
    if evals_path.exists():
        die(f"already exists; refusing to overwrite: {evals_path}")
    template = load_json(TEMPLATES_DIR / "evals-template.json")
    template["skill_name"] = name
    save_json(evals_path, template)
    print(f"Initialized {evals_path} (skill_name={name}); add 2-3 realistic prompts")
    return EXIT_OK


def cmd_validate(args: argparse.Namespace) -> int:
    result = validate_evals(Path(args.eval_json).expanduser())
    reports_dir = resolve_reports_dir(args.reports_dir)
    result_path = save_stage(reports_dir, result)
    for row in result["findings"]:
        if row["severity"] == FAIL:
            print(f"FAIL {row['id']}: {row['message']}", file=sys.stderr)
    print(f"Evals: {result['status']} ({result['eval_count']} evals) -> {result_path}")
    return EXIT_OK if result["status"] == PASS else 1


def cmd_scaffold(args: argparse.Namespace) -> int:
    skill_dir = Path(args.skill_dir).expanduser().resolve()
    name = _skill_name(skill_dir)
    if not EVAL_NAME_RE.match(args.name):
        die(f"--name must be a descriptive kebab-case slug, got {args.name!r}")
    evals_path = skill_dir / "evals" / "evals.json"
    prompt = args.prompt
    if evals_path.is_file():
        data = load_json(evals_path, default={})
        for row in data.get("evals", []):
            if row.get("id") == args.eval_id:
                if prompt and prompt != row.get("prompt"):
                    die("--prompt disagrees with evals.json entry; fix one of them")
                prompt = row.get("prompt")
                break
    if not prompt:
        die("no --prompt and no matching evals.json entry; provide --prompt or add the eval first")

    baseline_dir = BASELINE_DIRS[args.baseline]
    workspace = skill_dir.parent / f"{name}-workspace"
    eval_dir = workspace / f"iteration-{args.iteration}" / args.name
    for run_dir in ("with_skill", baseline_dir):
        (eval_dir / run_dir / "outputs").mkdir(parents=True, exist_ok=True)
    metadata = {
        "eval_id": args.eval_id,
        "eval_name": args.name,
        "prompt": prompt,
        "assertions": [],
    }
    metadata_path = eval_dir / "eval_metadata.json"
    if metadata_path.exists():
        existing = load_json(metadata_path, default={})
        if existing != metadata:
            die(f"exists with different content; refusing to overwrite: {metadata_path}")
    else:
        save_json(metadata_path, metadata)
    print(f"Scaffolded {eval_dir} (with_skill + {baseline_dir})")
    print(f"Metadata: {metadata_path}")
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    parser = build_cli(
        "evals_tool.py",
        "Stage 1: canonical evals/evals.json init, validation, and workspace scaffolding.",
        epilog=(
            "SUBCOMMANDS\n"
            "  init SKILL_DIR                         create evals/evals.json from the template\n"
            "  validate EVALS_JSON                    validate against schemas/evals.schema.json\n"
            "  scaffold SKILL_DIR --eval-id N --name SLUG [--iteration N]\n"
            "                                         [--baseline without|old] [--prompt TEXT]\n"
            "\n"
            "EXIT STATUS\n"
            "  0  ok\n"
            "  1  validation FAIL, missing input, or refuse-to-overwrite\n"
            "  2  usage error\n"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create evals/evals.json if absent")
    p_init.add_argument("skill_dir", metavar="SKILL_DIR")
    p_init.set_defaults(func=cmd_init)

    p_validate = sub.add_parser("validate", help="validate an evals.json file")
    p_validate.add_argument("eval_json", metavar="EVALS_JSON")
    p_validate.set_defaults(func=cmd_validate)

    p_scaffold = sub.add_parser("scaffold", help="create the canonical run workspace")
    p_scaffold.add_argument("skill_dir", metavar="SKILL_DIR")
    p_scaffold.add_argument("--eval-id", type=int, required=True)
    p_scaffold.add_argument("--name", required=True, help="descriptive kebab-case slug")
    p_scaffold.add_argument("--iteration", type=int, default=1)
    p_scaffold.add_argument("--baseline", choices=sorted(BASELINE_DIRS), default="without")
    p_scaffold.add_argument("--prompt", default=None)
    p_scaffold.set_defaults(func=cmd_scaffold)

    args = parse_or_usage(parser, argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
