#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Shared CLI, I/O, schema-validation, and stage-result helpers (skill-test 2.0.0).

The canonical contract lives in this skill's references/ and schemas/
directories. Scripts never execute the target skill.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

VERSION = "2.0.0"
SKILL_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"
REFERENCES_DIR = SKILL_ROOT / "references"
TEMPLATES_DIR = SKILL_ROOT / "templates"
SCHEMAS_DIR = SKILL_ROOT / "schemas"

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2

PASS = "PASS"
FAIL = "FAIL"
WARNING = "WARNING"
ADVICE = "ADVICE"

# Stage result filename map. Order defines the canonical loop order.
STAGE_FILES = {
    "preflight": "preflight.json",
    "evals": "evals.json",
    "runs": "runs.json",
    "grading": "grading.json",
    "timing": "timing.json",
    "benchmark": "benchmark.json",
}


def eprint(*args: Any) -> None:
    """Write a diagnostic line to stderr."""
    print(*args, file=sys.stderr)


def die(message: str, code: int = EXIT_ERROR) -> None:
    """Print a single-line diagnostic prefixed by severity, then exit."""
    prefix = "FAIL:" if code == EXIT_ERROR else "Usage error:"
    eprint(f"{prefix} {message}")
    raise SystemExit(code)


def require_yaml():
    """Import PyYAML or exit with an install hint."""
    try:
        import yaml  # type: ignore
    except ImportError:
        die("Missing dependency: PyYAML. Install with: python3 -m pip install pyyaml")
    return yaml


def resolve_reports_dir(value: str | Path | None) -> Path:
    """Resolve --reports-dir, defaulting to ./reports under the process cwd."""
    if value is None or str(value).strip() == "":
        return Path.cwd() / "reports"
    return Path(value).expanduser().resolve()


def ensure_dir(path: Path) -> Path:
    """Create a directory (and parents) if missing."""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        die(f"Cannot create directory {path}: {exc}")
    return path


def load_json(path: Path, default: Any = None) -> Any:
    """Load JSON. Missing file returns default (or {} when omitted)."""
    if default is None:
        default = {}
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        die(f"Cannot read JSON {path}: {exc}")


def save_json(path: Path, obj: Any) -> None:
    """Write pretty UTF-8 JSON."""
    ensure_dir(path.parent)
    try:
        path.write_text(
            json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    except OSError as exc:
        die(f"Cannot write {path}: {exc}")


def read_text(path: Path) -> str:
    """Read a UTF-8 text file or exit with a useful error."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        die(f"Cannot read {path}: {exc}")


def write_text_file(path: Path, text: str) -> None:
    """Write UTF-8 text after ensuring the parent directory exists."""
    ensure_dir(path.parent)
    try:
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        die(f"Cannot write {path}: {exc}")


def build_cli(
    prog: str, description: str, epilog: str = ""
) -> argparse.ArgumentParser:
    """Build the common CLI parser shared by every stage script."""
    parser = argparse.ArgumentParser(
        prog=prog,
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--reports-dir",
        metavar="DIR",
        help="Directory for stage results (default: ./reports under cwd)",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"{prog} {VERSION}"
    )
    return parser


def parse_or_usage(
    parser: argparse.ArgumentParser, argv: list[str] | None
) -> argparse.Namespace:
    """Parse args. Missing required arguments and empty argv exit 2."""
    return parser.parse_args(argv)


_TYPE_MAP: dict[str, Any] = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "integer": int,
    "number": (int, float),
}


def validate_schema(instance: Any, schema: dict, path: str = "$") -> list[str]:
    """Validate the JSON-Schema subset used by this skill's schemas/.

    Supported keywords: type, enum, pattern, minLength, maxLength, required,
    properties, items. Unsupported keywords are ignored rather than guessed.
    """
    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type:
        python_type = _TYPE_MAP.get(expected_type)
        if python_type is None:
            errors.append(f"{path}: unsupported schema type {expected_type!r}")
        elif isinstance(instance, bool) and expected_type in {"integer", "number"}:
            errors.append(f"{path}: expected {expected_type}, got bool")
        elif not isinstance(instance, python_type):
            errors.append(
                f"{path}: expected {expected_type}, got {type(instance).__name__}"
            )
            return errors
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in allowed values {schema['enum']}")
    if isinstance(instance, str):
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: {instance!r} does not match {schema['pattern']!r}")
        if "minLength" in schema and len(instance) < int(schema["minLength"]):
            errors.append(f"{path}: shorter than {schema['minLength']} chars")
        if "maxLength" in schema and len(instance) > int(schema["maxLength"]):
            errors.append(f"{path}: longer than {schema['maxLength']} chars ({len(instance)})")
    if (
        isinstance(instance, (int, float))
        and not isinstance(instance, bool)
        and "minimum" in schema
        and instance < schema["minimum"]
    ):
        errors.append(f"{path}: below minimum {schema['minimum']}")
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing required key {key!r}")
        properties = schema.get("properties", {})
        for key, value in instance.items():
            if key in properties:
                errors.extend(validate_schema(value, properties[key], f"{path}.{key}"))
    if isinstance(instance, list) and "items" in schema:
        for index, item in enumerate(instance):
            errors.extend(validate_schema(item, schema["items"], f"{path}[{index}]"))
    return errors


def finding(
    fid: str, severity: str, message: str, location: str = "", evidence: str = ""
) -> dict:
    """Build one finding row."""
    return {
        "id": fid,
        "severity": severity,
        "message": message,
        "location": location,
        "evidence": evidence,
    }


def stage_result(stage: str, status: str, findings: list[dict], **extra: Any) -> dict:
    """Build one stage result envelope."""
    return {
        "stage": stage,
        "status": status,
        "auditor_version": VERSION,
        "findings": findings,
        **extra,
    }


def save_stage(reports_dir: Path, result: dict) -> Path:
    """Persist a stage result under its canonical filename."""
    stage = str(result.get("stage") or "")
    if stage not in STAGE_FILES:
        die(f"Unknown stage {stage!r}; expected one of {sorted(STAGE_FILES)}")
    path = Path(reports_dir) / STAGE_FILES[stage]
    save_json(path, result)
    return path
