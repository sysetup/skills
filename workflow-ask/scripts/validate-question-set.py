#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate and render a logical question-set JSON file.

Read-only. Does not modify the skill tree or the input file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCRIPT_NAME = "validate-question-set.py"
SCRIPT_VERSION = "1.1.0"
EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 2
MAX_BYTES = 1_048_576
KINDS = ("single-select", "multi-select", "confirm", "free-text")
CODEX_MAX_QUESTIONS = 3
CODEX_HEADER_MAX_CHARS = 12
ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
SECRET_RE = re.compile(
    r"(?:provide|paste|enter|send|give)\s.{0,60}"
    r"(?:password|passwd|api[\s_-]*key|secret|private[\s_-]*key|\btoken\b)"
    r"|(?:password|api[\s_-]*key|secret|private[\s_-]*key)\s*[:=]\s*\S+",
    re.IGNORECASE,
)
RESTRICTED_PREFIX = Path("")
HELP_TEXT = f"""Usage: {SCRIPT_NAME} [OPTIONS]... COMMAND [FILE]

Validate a logical question-set JSON file, or render it to a native
Grok or Codex native payload, or the textual fallback questionnaire.

Commands:
  validate FILE          Validate FILE and print OK or NO_QUESTIONS.
  render-native [--target TARGET] FILE
                         Print the native Grok (default) or Codex payload JSON.
  render-fallback FILE   Print the textual fallback questionnaire.

Options:
  -h, --help             Show this help and exit.
  -V, --version          Print version and exit.

Exit status:
  0  Validation or render succeeded.
  1  Invalid input, missing file, or policy failure.
  2  Usage error.

Examples:
  {SCRIPT_NAME} validate ../assets/question-set.example.json
  {SCRIPT_NAME} render-native ../assets/question-set.example.json
  {SCRIPT_NAME} render-native --target codex ../assets/question-set.example.json
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


def restricted_path(path: Path) -> bool:
    """True if path is inside the host restricted security domain.

    Arguments:
      path: resolved filesystem path
    Outputs: none
    Returns: bool
    """
    try:
        path.relative_to(RESTRICTED_PREFIX)
        return True
    except ValueError:
        return False


def load_question_set(path: Path) -> tuple[dict[str, Any] | None, int]:
    """Read and parse a question-set JSON file.

    Arguments:
      path: input JSON path
    Outputs: FAIL diagnostics on stderr on error
    Returns: (data, exit_code). data is None on failure.
    """
    if restricted_path(path):
        return None, fail("path is outside the authorized security domain")
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return None, fail(f"file not found: {path}")
    except PermissionError:
        return None, fail(f"permission denied: {path}")
    except IsADirectoryError:
        return None, fail(f"not a file: {path}")
    except OSError as exc:
        return None, fail(f"cannot read {path}: {exc}")
    if len(raw) > MAX_BYTES:
        return None, fail(
            f"input too large ({len(raw)} bytes); max is {MAX_BYTES}"
        )
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, fail("file is not valid UTF-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
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
    if kind not in KINDS:
        errors.append(
            f"{prefix}.kind must be one of: {', '.join(KINDS)}"
        )
    if not isinstance(required, bool):
        errors.append(f"{prefix}.required must be a boolean")
    if header is not None and (
        not isinstance(header, str)
        or not header.strip()
        or len(header) > CODEX_HEADER_MAX_CHARS
    ):
        errors.append(
            f"{prefix}.header must be a non-empty string of at most "
            f"{CODEX_HEADER_MAX_CHARS} characters"
        )
    if not isinstance(options, list):
        errors.append(f"{prefix}.options must be an array")
        options = []
    labels: list[str] = []
    for opt_index, option in enumerate(options, start=1):
        labels.append(option_label(option, opt_index, errors))
    if kind in {"single-select", "multi-select"} and len(options) < 2:
        errors.append(f"{prefix} {kind} needs at least two options")
    if kind == "confirm" and len(options) != 2:
        errors.append(f"{prefix} confirm needs exactly two options")
    if not isinstance(default, str) or not default.strip():
        errors.append(f"{prefix}.default must be a non-empty string")
    elif labels and default not in labels:
        errors.append(f"{prefix}.default must match an option label")
    if labels and "(Recommended)" not in labels[0]:
        errors.append(
            f"{prefix} first option label must include (Recommended)"
        )
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


def render_grok_native(data: dict[str, Any]) -> dict[str, Any]:
    """Map a logical set onto the Grok ask_user_question payload.

    Arguments:
      data: validated question set
    Outputs: none
    Returns: payload dict
    """
    payload_questions: list[dict[str, Any]] = []
    for item in data["questions"]:
        kind = item["kind"]
        options = []
        for option in item["options"]:
            entry: dict[str, Any] = {
                "label": option["label"],
                "description": option["description"],
            }
            preview = option.get("preview")
            if isinstance(preview, str) and preview and kind == "single-select":
                entry["preview"] = preview
            options.append(entry)
        if kind == "free-text" and not options:
            options.append(
                {
                    "label": "Use recommended default (Recommended)",
                    "description": item["default"],
                }
            )
        payload_questions.append(
            {
                "question": item["text"],
                "options": options,
                "multi_select": kind == "multi-select",
            }
        )
    return {"questions": payload_questions}


def render_codex_native(data: dict[str, Any]) -> dict[str, Any]:
    """Map a logical set onto the Codex request_user_input payload.

    Arguments:
      data: validated question set
    Outputs: none
    Returns: payload dict
    Raises:
      ValueError: when Codex cannot preserve the logical set's semantics.
    """
    questions = data["questions"]
    if len(questions) > CODEX_MAX_QUESTIONS:
        raise ValueError(
            f"Codex request_user_input accepts at most "
            f"{CODEX_MAX_QUESTIONS} questions per call"
        )

    payload_questions: list[dict[str, Any]] = []
    for item in questions:
        if item["kind"] == "multi-select":
            raise ValueError(
                "Codex request_user_input has no multi-select field; "
                "use the textual fallback to preserve multi-select semantics"
            )

        options = [
            {
                "label": option["label"],
                "description": option["description"],
            }
            for option in item["options"]
        ]
        if item["kind"] == "free-text" and not options:
            options.append(
                {
                    "label": "Use recommended default (Recommended)",
                    "description": item["default"],
                }
            )

        header = item.get("header")
        if header is None:
            header = item["id"].replace("-", "_")
        payload_questions.append(
            {
                "id": item["id"].replace("-", "_"),
                "header": header,
                "question": item["text"],
                "options": options,
            }
        )
    return {"questions": payload_questions}


def render_native(data: dict[str, Any], target: str) -> dict[str, Any]:
    """Dispatch a logical set to the selected native payload renderer.

    Arguments:
      data: validated question set
      target: native target name
    Outputs: none
    Returns: payload dict
    Raises:
      ValueError: when the target cannot represent the logical set.
    """
    if target == "codex":
        return render_codex_native(data)
    return render_grok_native(data)


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
            'If you want me to proceed with the defaults, reply: "use defaults".',
            "",
        ]
    )
    return "\n".join(parts)


def cmd_validate(path: Path) -> int:
    """Validate FILE and print OK or NO_QUESTIONS.

    Arguments:
      path: question-set JSON
    Outputs: OK/NO_QUESTIONS on stdout, FAIL on stderr
    Returns: exit code
    """
    data, code = load_question_set(path)
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


def cmd_render_native(path: Path, target: str) -> int:
    """Print the selected native payload JSON.

    Arguments:
      path: question-set JSON
      target: native target name
    Outputs: JSON on stdout, FAIL on stderr
    Returns: exit code
    """
    data, code = load_question_set(path)
    if data is None:
        return code
    errors = validate_data(data)
    if errors:
        return fail("; ".join(errors))
    questions = data.get("questions") or []
    if not questions:
        print("NO_QUESTIONS: proceed")
        return EXIT_OK
    try:
        payload = render_native(data, target)
    except ValueError as exc:
        return fail(str(exc))
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return EXIT_OK


def cmd_render_fallback(path: Path) -> int:
    """Print the textual fallback questionnaire.

    Arguments:
      path: question-set JSON
    Outputs: markdown on stdout, FAIL on stderr
    Returns: exit code
    """
    data, code = load_question_set(path)
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
            "Validate a logical question-set JSON file, or render it to a "
            "native Grok or Codex payload, or the textual fallback "
            "questionnaire."
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
    for name in ("validate", "render-native", "render-fallback"):
        cmd = sub.add_parser(name, add_help=False)
        cmd.add_argument("file", metavar="FILE")
        if name == "render-native":
            cmd.add_argument(
                "--target",
                choices=("grok", "codex"),
                default="grok",
                help="Native payload target (default: grok).",
            )
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
    path = Path(args.file).expanduser()
    try:
        path = path.resolve()
    except OSError as exc:
        return fail(f"cannot resolve {args.file}: {exc}")
    if args.command == "validate":
        return cmd_validate(path)
    if args.command == "render-native":
        return cmd_render_native(path, args.target)
    if args.command == "render-fallback":
        return cmd_render_fallback(path)
    return fail(f"unknown command {args.command}", EXIT_USAGE)


if __name__ == "__main__":
    sys.exit(main())

# NAME
# validate-question-set.py - validate and render a logical question set
#
# SYNOPSIS
# validate-question-set.py [OPTIONS]... COMMAND [FILE]
#
# DESCRIPTION
# Reads a UTF-8 JSON logical question set (max 1048576 bytes) and either
# validates it or renders a native Grok or Codex payload, or the textual
# fallback questionnaire from references/question-channel.md.
# Empty questions arrays print NO_QUESTIONS: proceed and exit 0.
#
# OPTIONS
# -h, --help     Print help and exit 0.
# -V, --version  Print version and exit 0.
#
# EXIT STATUS
# 0 success
# 1 invalid input, missing file, or policy failure
# 2 usage error
#
# EXAMPLES
# validate-question-set.py validate ../assets/question-set.example.json
# validate-question-set.py render-native ../assets/question-set.example.json
# validate-question-set.py render-native --target codex ../assets/question-set.example.json
#
# SEE ALSO
# load-skill.sh, python3(1)
