#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate and render a logical question-set JSON file.

Read-only. Does not modify the skill tree or the input file.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

SCRIPT_NAME = "validate-question-set.py"
SCRIPT_VERSION = "2.0.0"
EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 2
MAX_BYTES = 1_048_576
KINDS = ("single-select", "multi-select", "confirm", "free-text")
ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
SECRET_RE = re.compile(
    r"(?:provide|paste|enter|send|give)\s.{0,60}"
    r"(?:password|passwd|api[\s_-]*key|secret|private[\s_-]*key|\btoken\b)"
    r"|(?:password|api[\s_-]*key|secret|private[\s_-]*key)\s*[:=]\s*\S+",
    re.IGNORECASE,
)
HELP_TEXT = f"""Usage: {SCRIPT_NAME} [OPTIONS]... COMMAND [--root DIR] FILE

Validate logical question-set JSON or render a textual questionnaire.
The agent adapts questions to native tools using their live contracts.

Commands:
  validate FILE          Validate FILE and print OK or NO_QUESTIONS.
  render-fallback FILE   Print the textual fallback questionnaire.

Options:
  -h, --help             Show this help and exit.
  -V, --version          Print version and exit.
  --root DIR             Check resolved containment (stable directories).
                         Applies to the selected command, not a sandbox.

Exit status:
  0  Validation or render succeeded.
  1  Invalid input, missing file, or policy failure.
  2  Usage error.

Examples:
  {SCRIPT_NAME} validate ../assets/question-set.example.json
  {SCRIPT_NAME} render-fallback ../assets/question-set.example.json
"""


def eprint(message: str) -> None:
    """Write a diagnostic line to stderr.

    Arguments:
      message: text to print
    Outputs: one line on stderr
    Returns: None
    """
    print(message, file=sys.stderr)


def fail(message: str, code: int = EXIT_FAIL) -> int:
    """Print FAIL: message and return an exit code.

    Arguments:
      message: diagnostic
      code: process exit status
    Outputs: FAIL line on stderr
    Returns: code
    """
    eprint(f"FAIL: {message}")
    return code


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate JSON keys before constructing an object."""
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("duplicate JSON keys")
    return result


def load_question_set(
    path: Path, root: Path | None = None
) -> tuple[dict[str, Any] | None, int]:
    """Read and parse a question-set JSON file.

    Arguments:
      path: explicitly authorized input JSON path
      root: optional containment root; parent directories must remain stable
    Outputs: FAIL diagnostics on stderr on error
    Returns: (data, exit_code). data is None on failure.
    """
    try:
        path = path.expanduser().resolve(strict=True)
        if root is not None:
            root = root.expanduser().resolve(strict=True)
            if not root.is_dir() or not path.is_relative_to(root):
                return None, fail("path is outside the selected root")
        flags = os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW
        with os.fdopen(os.open(path, flags), "rb") as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                return None, fail("input must be a regular file")
            raw = source.read(MAX_BYTES + 1)
    except FileNotFoundError:
        return None, fail(f"file not found: {path}")
    except PermissionError:
        return None, fail(f"permission denied: {path}")
    except IsADirectoryError:
        return None, fail(f"not a file: {path}")
    except (OSError, RuntimeError, ValueError) as exc:
        return None, fail(f"cannot read input: {exc}")
    if len(raw) > MAX_BYTES:
        return None, fail(f"input exceeds {MAX_BYTES} bytes")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, fail("file is not valid UTF-8")
    try:
        data = json.loads(text, object_pairs_hook=unique_object)
    except (ValueError, RecursionError) as exc:
        return None, fail(f"invalid JSON: {exc}")
    if not isinstance(data, dict):
        return None, fail("question set must be a JSON object")
    return data, EXIT_OK


def option_label(option: Any, index: int, errors: list[str]) -> str:
    """Return a validated option label, recording errors.

    Arguments:
      option: option object
      index: 1-based option index
      errors: accumulator
    Outputs: none
    Returns: label string (may be empty on error)
    """
    if not isinstance(option, dict):
        errors.append(f"option {index} must be an object")
        return ""
    label = option.get("label")
    description = option.get("description")
    if not isinstance(label, str) or not label.strip():
        errors.append(f"option {index} needs a non-empty label")
        label = ""
    elif len(label) > 80:
        errors.append(f"option {index} label exceeds 80 characters")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"option {index} needs a non-empty description")
    elif len(description) > 300:
        errors.append(f"option {index} description exceeds 300 characters")
    preview = option.get("preview", None)
    if preview is not None and not isinstance(preview, str):
        errors.append(f"option {index} preview must be a string or null")
    extra = set(option) - {"label", "description", "preview"}
    if extra:
        errors.append(f"option {index} has unknown fields: {sorted(extra)}")
    return label


def validate_question(item: Any, index: int, seen_ids: set[str]) -> list[str]:
    """Validate one logical question object.

    Arguments:
      item: question mapping
      index: 1-based question index
      seen_ids: ids already used
    Outputs: none
    Returns: list of error strings (empty means valid)
    """
    prefix = f"questions[{index}]"
    errors: list[str] = []
    if not isinstance(item, dict):
        return [f"{prefix} must be an object"]
    qid = item.get("id")
    text = item.get("text")
    kind = item.get("kind")
    required = item.get("required")
    header = item.get("header")
    options = item.get("options")
    default = item.get("default")
    if not isinstance(qid, str) or not ID_RE.match(qid) or len(qid) > 64:
        errors.append(f"{prefix}.id must be a kebab-case slug of 1-64 chars")
    elif qid in seen_ids:
        errors.append(f"{prefix}.id {qid!r} is duplicated")
    else:
        seen_ids.add(qid)
    if not isinstance(text, str) or not text.strip():
        errors.append(f"{prefix}.text must be a non-empty string")
    else:
        if len(text) > 500:
            errors.append(f"{prefix}.text exceeds 500 characters")
        if SECRET_RE.search(text):
            errors.append(f"{prefix}.text requests a secret; use a placeholder")
    if not isinstance(kind, str) or kind not in KINDS:
        errors.append(f"{prefix}.kind must be one of: {', '.join(KINDS)}")
        return errors
    if not isinstance(required, bool):
        errors.append(f"{prefix}.required must be a boolean")
    if header is not None and (not isinstance(header, str) or not header.strip()):
        errors.append(f"{prefix}.header must be a non-empty string")
    if not isinstance(options, list):
        errors.append(f"{prefix}.options must be an array")
        options = []
    labels: list[str] = []
    for opt_index, option in enumerate(options, start=1):
        labels.append(option_label(option, opt_index, errors))
    if len(labels) != len(set(labels)):
        errors.append(f"{prefix}.options contains duplicate labels")
    if kind in {"single-select", "multi-select"} and len(options) < 2:
        errors.append(f"{prefix} {kind} needs at least two options")
    if kind == "confirm" and len(options) != 2:
        errors.append(f"{prefix} confirm needs exactly two options")
    if not isinstance(default, str) or not default.strip():
        errors.append(f"{prefix}.default must be a non-empty string")
    elif labels and default not in labels:
        errors.append(f"{prefix}.default must match an option label")
    if labels and "(Recommended)" not in labels[0]:
        errors.append(f"{prefix} first option label must include (Recommended)")
    extra = set(item) - {
        "id",
        "header",
        "text",
        "kind",
        "required",
        "options",
        "default",
        "rationale",
    }
    if extra:
        errors.append(f"{prefix} has unknown fields: {sorted(extra)}")
    rationale = item.get("rationale")
    if rationale is not None and not isinstance(rationale, str):
        errors.append(f"{prefix}.rationale must be a string")
    elif isinstance(rationale, str) and len(rationale) > 300:
        errors.append(f"{prefix}.rationale exceeds 300 characters")
    return errors


def validate_data(data: dict[str, Any]) -> list[str]:
    """Return all validation errors for a parsed question set.

    Arguments:
      data: parsed JSON object
    Outputs: none
    Returns: error strings
    """
    extra = set(data) - {"questions"}
    errors: list[str] = []
    if extra:
        errors.append(f"unknown top-level fields: {sorted(extra)}")
    questions = data.get("questions")
    if not isinstance(questions, list):
        errors.append("questions must be an array")
        return errors
    seen_ids: set[str] = set()
    for index, item in enumerate(questions, start=1):
        errors.extend(validate_question(item, index, seen_ids))
    return errors


def render_fallback(data: dict[str, Any]) -> str:
    """Render the textual fallback questionnaire.

    Arguments:
      data: validated question set
    Outputs: none
    Returns: markdown string
    """
    required: list[str] = []
    optional: list[str] = []
    number = 1
    for item in data["questions"]:
        option_bits = []
        for index, option in enumerate(item["options"]):
            letter = chr(ord("A") + index)
            option_bits.append(f"[{letter}] {option['label']}")
        options_line = " | ".join(option_bits) if option_bits else "(free-text)"
        block = (
            f"{number}. [{item['text']}]\n"
            f"   - Kind: {item['kind']}\n"
            f"   - Options: {options_line}\n"
            f"   - Default: [{item['default']}]"
        )
        if item["required"]:
            required.append(block)
        else:
            optional.append(block)
        number += 1
    parts = [
        "Clarification needed before I start.",
        "",
        "Native interactive questions are unavailable in this session",
        "(missing | disabled | non-interactive), so this is the text fallback.",
        "",
        "### Required",
    ]
    if required:
        parts.extend(required)
    else:
        parts.append("(none)")
    parts.extend(["", "### Optional"])
    if optional:
        parts.extend(optional)
    else:
        parts.append("(none)")
    parts.extend(
        [
            "",
            "Reply with answers; defaults apply only to optional questions.",
            "",
        ]
    )
    return "\n".join(parts)


def cmd_validate(path: Path, root: Path | None = None) -> int:
    """Validate FILE and print OK or NO_QUESTIONS.

    Arguments:
      path: question-set JSON
    Outputs: OK/NO_QUESTIONS on stdout, FAIL on stderr
    Returns: exit code
    """
    data, code = load_question_set(path, root)
    if data is None:
        return code
    errors = validate_data(data)
    if errors:
        return fail("; ".join(errors))
    questions = data.get("questions") or []
    if not questions:
        print("NO_QUESTIONS: proceed")
        return EXIT_OK
    print(f"OK: {len(questions)} question(s) valid")
    return EXIT_OK


def cmd_render_fallback(path: Path, root: Path | None = None) -> int:
    """Print the textual fallback questionnaire.

    Arguments:
      path: question-set JSON
    Outputs: markdown on stdout, FAIL on stderr
    Returns: exit code
    """
    data, code = load_question_set(path, root)
    if data is None:
        return code
    errors = validate_data(data)
    if errors:
        return fail("; ".join(errors))
    questions = data.get("questions") or []
    if not questions:
        print("NO_QUESTIONS: proceed")
        return EXIT_OK
    sys.stdout.write(render_fallback(data))
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    """Build the GNU-style argument parser.

    Arguments: none
    Outputs: none
    Returns: parser
    """
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        add_help=False,
        description=(
            "Validate logical question-set JSON or render a textual questionnaire."
        ),
    )
    parser.add_argument(
        "-h",
        "--help",
        action="store_true",
        help="Show this help and exit.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Print version and exit.",
    )
    sub = parser.add_subparsers(dest="command")
    for name in ("validate", "render-fallback"):
        cmd = sub.add_parser(name, add_help=False)
        cmd.add_argument("file", metavar="FILE")
        cmd.add_argument("--root", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint.

    Arguments:
      argv: argument list without the program name
    Outputs: help, version, OK/FAIL, or rendered artifacts
    Returns: exit code
    Side effects: reads FILE; no writes
    """
    if argv is None:
        argv = sys.argv[1:]
    parser = build_parser()
    if not argv:
        sys.stderr.write(HELP_TEXT)
        return EXIT_USAGE
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return EXIT_USAGE if code not in (0, None) else EXIT_OK
    if args.help:
        sys.stdout.write(HELP_TEXT)
        return EXIT_OK
    if args.version:
        print(f"{SCRIPT_NAME} {SCRIPT_VERSION}")
        return EXIT_OK
    if not args.command:
        sys.stderr.write(HELP_TEXT)
        return EXIT_USAGE
    path = Path(args.file)
    if args.command == "validate":
        return cmd_validate(path, args.root)
    if args.command == "render-fallback":
        return cmd_render_fallback(path, args.root)
    return fail(f"unknown command {args.command}", EXIT_USAGE)


if __name__ == "__main__":
    sys.exit(main())

# NAME
# validate-question-set.py - validate and render a logical question set
#
# SYNOPSIS
# validate-question-set.py [OPTIONS]... COMMAND [--root DIR] FILE
#
# DESCRIPTION
# Reads a UTF-8 JSON logical question set (max 1048576 bytes) and either
# validates it or renders a textual questionnaire. Optional --root checks
# resolved containment in stable directories; runtime controls enforce access.
# Empty questions arrays print NO_QUESTIONS: proceed and exit 0.
#
# OPTIONS
# -h, --help     Print help and exit 0.
# -V, --version  Print version and exit 0.
# --root DIR     Check resolved containment within DIR.
#
# EXIT STATUS
# 0 success
# 1 invalid input, missing file, or policy failure
# 2 usage error
#
# EXAMPLES
# validate-question-set.py validate ../assets/question-set.example.json
# validate-question-set.py render-fallback ../assets/question-set.example.json
#
# SEE ALSO
# load-skill.sh, python3(1)
