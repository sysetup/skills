#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Stage 0: Canonical preflight for one SKILL.md (fail-only-on-canon).

FAIL is reserved for explicit canonical requirements: valid name and
description, existing bundled references, and the Lack-of-Surprise security
floor. Everything else is WARNING or ADVICE. See references/canonical-contract.md.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

from _common import (
    ADVICE,
    EXIT_OK,
    FAIL,
    PASS,
    SCHEMAS_DIR,
    WARNING,
    build_cli,
    die,
    load_json,
    parse_or_usage,
    read_text,
    require_yaml,
    resolve_reports_dir,
    save_stage,
    stage_result,
    validate_schema,
)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
BUNDLED_REF_RE = re.compile(
    r"(?<![A-Za-z0-9._/:-])(?:\.\./[A-Za-z0-9._\-]+/)?(?:\./)?"
    r"(?:scripts|references|assets|agents|eval-viewer|schemas|templates|fixtures)"
    r"/[A-Za-z0-9._\-/]+\.(?:py|md|html|json|sh|svg|txt|yaml|yml|png|jpg|jpeg|ttf|otf)"
)
LOCAL_LINK_RE = re.compile(
    r'!?\[[^\]\n]*\]\(\s*(?:<(?P<angle>[^>\n]+)>|'
    r'(?P<plain>[^\s()]+(?:\([^\s()]*\)[^\s()]*)*))'
    r'(?:\s+(?:"[^"\n]*"|\x27[^\x27\n]*\x27))?\s*\)'
)
REFERENCE_LINK_RE = re.compile(r"!?\[([^\]\n]+)\]\[([^\]\n]*)\]")
LINK_DEFINITION_RE = re.compile(
    r"^ {0,3}\[([^\]\n]+)\]:\s*(?:<([^>\n]+)>|([^\s]+))", re.MULTILINE
)
EXTERNAL_REF_RE = re.compile(r"(?:[A-Za-z][A-Za-z0-9+.-]*:|//)[^\s<>`]+")
NON_RESOURCE_PREFIX_RE = re.compile(
    r"(?:\b(?:example|sample|illustration|e\.g\.|output|generated output)\s*:\s*|"
    r"\bfor example[, :]\s*|"
    r"\b(?:write|save|create|generate|export)\s+"
    r"(?:(?:the|a|an|new|generated|output|report|file|results?)\s+)*"
    r"(?:(?:to|as|at|in|under|into)\s+)?)$",
    re.IGNORECASE,
)
WHEN_HINT_RE = re.compile(
    r"\b(use (?:this |it )?(?:when|whenever)|when (?:the )?user|whenever|"
    r"for (?:creating|editing|reviewing|testing|auditing)|trigger(?:s|ing)?)\b",
    re.IGNORECASE,
)

# Patterns match dangerous ACTIONS in prose. Code fences and documented
# prohibitions are filtered out (a checklist that names a dangerous command
# is not an instruction to run it).
SECURITY_PATTERNS = {
    "SECRET": (
        r"(api[_-]?key|apikey|secret|password|\btoken\b)\s*[:=]\s*[^\s]+",
        "Possible hardcoded secret or credential request",
    ),
    "BYPASS": (
        r"\b(ignore (all )?(your |my )?(previous |prior )?instructions|"
        r"jailbreak|bypass (the )?(system|safety|guard))\b",
        "Bypass / jailbreak instruction detected",
    ),
    "DESTRUCTIVE": (
        r"\brm\s+-[a-zA-Z]*rf\b|\bsudo\s+rm\b|\bmkfs(?:\.\w+)?\b|:\(\)\s*\{",
        "Destructive command detected",
    ),
    "PIPE_TO_SHELL": (
        r"\b(curl|wget)\b[^\n]{0,120}\|\s*(ba)?sh\b",
        "curl|sh / wget|sh pattern detected",
    ),
    "EXFIL": (
        r"\b(send|post|upload|exfiltrat\w*)\b[^\n]{0,120}\bhttps?://",
        "Possible data exfiltration to an external URL",
    ),
}
DOC_HINTS = (
    "detect",
    "check",
    "scan",
    "pattern",
    "blocker",
    "forbidden",
    "must fail",
    "fail if",
    "never",
    "do not",
    "don't",
    "must not",
    "not execute",
    "checklist",
    "anti-pattern",
    "if found",
    "without verification",
    "security",
    "prohibition",
    "must refuse",
    "should refuse",
    "does not execute",
    "treat a documented",
)


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _resource_prose(text: str) -> str:
    """Mask fenced examples and explicitly illustrative/output sections in place."""
    lines: list[str] = []
    fence = ""
    excluded_heading = 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})([^\n]*)", line)
        in_fence = bool(fence or marker)
        if marker:
            delimiter, tail = marker.groups()
            if not fence:
                fence = delimiter
            elif (
                delimiter[0] == fence[0]
                and len(delimiter) >= len(fence)
                and not tail.strip()
            ):
                fence = ""
        if not in_fence:
            heading = re.match(r"^ {0,3}(#{1,6})\s+(.+)", line)
            if heading:
                level = len(heading[1])
                if excluded_heading and level <= excluded_heading:
                    excluded_heading = 0
                if not excluded_heading and re.match(
                    r"(?:examples?|samples?|illustrations?|(?:generated |expected )?outputs?)\b",
                    heading[2],
                    re.IGNORECASE,
                ):
                    excluded_heading = level
        if in_fence or excluded_heading:
            line = re.sub(r"[^\n]", " ", line)
        lines.append(line)
    return "".join(lines)


def _bundled_references(text: str) -> dict[str, int]:
    """Return declared local paths and their first source offset, excluding examples."""
    prose = _resource_prose(text)
    references: dict[str, int] = {}
    # Inline code may hold a real bare resource path, but quoted link syntax
    # is an illustration rather than an active Markdown link.
    inline_code = list(re.finditer(r"(`+).*?\1", prose))
    links = list(LOCAL_LINK_RE.finditer(prose))
    definitions = list(LINK_DEFINITION_RE.finditer(prose))
    reference_links = list(REFERENCE_LINK_RE.finditer(prose))
    excluded = [(match.start(), match.end()) for match in links]
    excluded.extend(
        (match.start(), match.end()) for match in definitions + reference_links
    )
    excluded.extend(
        (match.start(), match.end()) for match in EXTERNAL_REF_RE.finditer(prose)
    )

    def is_output_or_example(index: int) -> bool:
        line_start = prose.rfind("\n", 0, index) + 1
        prefix = prose[line_start:index].rstrip("`")
        return bool(NON_RESOURCE_PREFIX_RE.search(prefix))

    def reference_key(label: str) -> str:
        return " ".join(label.split()).casefold()

    destinations = {
        reference_key(match[1]): match[2] or match[3] for match in definitions
    }
    declared_links = [(match, match["angle"] or match["plain"]) for match in links]
    for match in reference_links:
        destination = destinations.get(reference_key(match[2] or match[1]))
        if destination:
            declared_links.append((match, destination))

    for match, destination in declared_links:
        if any(code.start() <= match.start() < code.end() for code in inline_code):
            continue
        # Schemes, protocol-relative URLs, absolute paths and pure fragments
        # do not declare a file bundled relative to this SKILL.md.
        if destination.startswith(("#", "/")) or re.match(
            r"^[A-Za-z][A-Za-z0-9+.-]*:", destination
        ):
            continue
        if is_output_or_example(match.start()):
            continue
        relative = unquote(destination.split("#", 1)[0])
        if relative:
            references[relative] = min(
                references.get(relative, match.start()), match.start()
            )

    for match in BUNDLED_REF_RE.finditer(prose):
        if any(start <= match.start() < end for start, end in excluded):
            continue
        if is_output_or_example(match.start()):
            continue
        relative = match.group(0)
        references[relative] = min(references.get(relative, match.start()), match.start())
    return references


def _code_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for match in re.finditer(r"```.*?```", text, flags=re.DOTALL):
        ranges.append((match.start(), match.end()))
    for match in re.finditer(r"`[^`\n]*`", text):
        if not any(start <= match.start() < end for start, end in ranges):
            ranges.append((match.start(), match.end()))
    return ranges


def _is_documentation(text: str, start: int, end: int) -> bool:
    window = text[max(0, start - 180) : min(len(text), end + 180)].lower()
    return any(hint in window for hint in DOC_HINTS)


def _has_toc(ref_text: str) -> bool:
    head = ref_text[:6000]
    if re.search(r"table of contents", head, re.IGNORECASE):
        return True
    anchors = re.findall(r"\[[^\]]+\]\(#[^)]+\)", ref_text[:8000])
    return len(anchors) >= 5


def parse_frontmatter(path: Path) -> dict:
    """Parse SKILL.md into frontmatter + body. YAML failure is a canon FAIL."""
    yaml = require_yaml()
    text = read_text(path)
    result: dict = {
        "path": str(path.resolve()),
        "skill_root": str(path.resolve().parent),
        "raw": text,
        "body": "",
        "frontmatter": {},
        "parse_error": None,
    }
    match = FRONTMATTER_RE.match(text)
    if not match:
        result["parse_error"] = "No YAML frontmatter found between --- delimiters"
        result["body"] = text
        return result
    result["body"] = text[match.end():]
    try:
        loaded = yaml.safe_load(match.group(1))
    except Exception as exc:  # yaml.YAMLError and variants
        result["parse_error"] = f"Invalid YAML frontmatter: {exc}"
        return result
    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        result["parse_error"] = "YAML frontmatter is not a mapping"
        return result
    result["frontmatter"] = loaded
    return result


def preflight(path: Path) -> dict:
    """Run all canonical checks and return a stage result envelope."""
    parsed = parse_frontmatter(path)
    text = parsed["raw"]
    body = parsed["body"]
    frontmatter = parsed["frontmatter"]
    skill_root = Path(parsed["skill_root"])
    findings: list[dict] = []

    if parsed["parse_error"]:
        findings.append(
            {
                "id": "P001",
                "severity": FAIL,
                "message": parsed["parse_error"],
                "location": f"{path}:1:1",
                "evidence": "The canonical contract requires YAML frontmatter with name and description",
            }
        )
        return stage_result(
            "preflight",
            FAIL,
            findings,
            skill={
                "path": str(path),
                "name": None,
                "body_lines": body.count("\n") + 1,
                "description_chars": 0,
                "anatomy_dirs": [],
                "referenced_bundled_files": [],
            },
        )

    schema = load_json(SCHEMAS_DIR / "skill-frontmatter.schema.json")
    schema_errors = validate_schema(frontmatter, schema)
    for error in schema_errors:
        findings.append(
            {
                "id": "P002" if "'name'" in error or ".name" in error else "P003",
                "severity": FAIL,
                "message": f"Canonical frontmatter: {error}",
                "location": f"{path}:frontmatter",
                "evidence": "A skill name must be kebab-case (max 64 chars) and its description non-empty (max 1024 chars)",
            }
        )

    if "compatibility" in frontmatter and not isinstance(
        frontmatter["compatibility"], str
    ):
        findings.append(
            {
                "id": "P105",
                "severity": ADVICE,
                "message": "compatibility should be a string when present",
                "location": f"{path}:frontmatter:compatibility",
                "evidence": "Optional canonical field; a wrong type usually means a YAML quoting mistake",
            }
        )

    # Local resource links are independent of directory and extension names;
    # preserve the previously supported bare-path forms as well.
    resource_locations = _bundled_references(text)
    referenced = sorted(resource_locations)
    for relative in referenced:
        target = (skill_root / relative).resolve()
        if not target.exists():
            findings.append(
                {
                    "id": "P004",
                    "severity": FAIL,
                    "message": f"Referenced bundled file does not exist: {relative}",
                    "location": f"{path}:{_line_of(text, resource_locations[relative])}",
                    "evidence": "A dangling reference breaks the skill at invocation time",
                }
            )

    # Security floor: Principle of Lack of Surprise.
    ranges = _code_ranges(text)
    for label, (pattern, message) in SECURITY_PATTERNS.items():
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            if any(start <= match.start() < end for start, end in ranges):
                continue
            if _is_documentation(text, match.start(), match.end()):
                continue
            findings.append(
                {
                    "id": "P005",
                    "severity": FAIL,
                    "message": f"[{label}] {message}",
                    "location": f"{path}:{_line_of(text, match.start())}",
                    "evidence": match.group(0),
                }
            )

    # Body length: the canonical ideal is under 500 lines, explicitly approximate.
    body_lines = body.count("\n") + 1
    if body_lines > 500:
        findings.append(
            {
                "id": "P101",
                "severity": ADVICE,
                "message": f"SKILL.md body is {body_lines} lines; canonical ideal is under 500",
                "location": f"{path}:body",
                "evidence": "Consider moving detail into references/ with explicit load guidance",
            }
        )

    description = frontmatter.get("description")
    if isinstance(description, str) and description and not WHEN_HINT_RE.search(
        description
    ):
        findings.append(
            {
                "id": "P102",
                "severity": ADVICE,
                "message": "description has no WHEN/trigger signal; all when-to-use info belongs in the description",
                "location": f"{path}:frontmatter:description",
                "evidence": "Undertriggering is the canonical failure mode; add explicit 'use when...' contexts",
            }
        )

    # Reference guidance: >300-line references need a TOC; files under
    # references/ should be pointed to from SKILL.md.
    references_dir = skill_root / "references"
    if references_dir.is_dir():
        for ref_file in sorted(references_dir.rglob("*")):
            if not ref_file.is_file():
                continue
            try:
                ref_text = ref_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if ref_file.suffix.lower() == ".md":
                if ref_text.count("\n") + 1 > 300 and not _has_toc(ref_text):
                    findings.append(
                        {
                            "id": "P103",
                            "severity": WARNING,
                            "message": f"reference {ref_file.name} exceeds 300 lines without a table of contents",
                            "location": str(ref_file),
                            "evidence": "Reference files over 300 lines require a table of contents",
                        }
                    )
                rel = ref_file.relative_to(skill_root).as_posix()
                if ref_file.name not in body and ref_file.stem not in body:
                    findings.append(
                        {
                            "id": "P106",
                            "severity": ADVICE,
                            "message": f"reference {rel} is never mentioned in SKILL.md (orphan)",
                            "location": str(ref_file),
                            "evidence": "Reference files must be pointed to with guidance on when to read them",
                        }
                    )

    anatomy = [
        d for d in ("scripts", "references", "assets") if (skill_root / d).is_dir()
    ]
    status = FAIL if any(row["severity"] == FAIL for row in findings) else PASS
    description_chars = len(description) if isinstance(description, str) else 0
    return stage_result(
        "preflight",
        status,
        findings,
        skill={
            "path": str(path.resolve()),
            "name": frontmatter.get("name"),
            "body_lines": body_lines,
            "description_chars": description_chars,
            "anatomy_dirs": anatomy,
            "referenced_bundled_files": referenced,
        },
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_cli(
        "preflight.py",
        "Stage 0: validate one SKILL.md against the canonical contract.",
        epilog=(
            "EXIT STATUS\n"
            "  0  PASS (warnings/advice allowed)\n"
            "  1  FAIL (canonical violation) or unreadable target\n"
            "  2  usage error\n"
            "\n"
            "Writes preflight.json under --reports-dir.\n"
            "Fail-only-on-canon: see references/canonical-contract.md."
        ),
    )
    parser.add_argument(
        "skill_md", metavar="SKILL_MD", help="Path to the target SKILL.md"
    )
    args = parse_or_usage(parser, argv)
    target = Path(args.skill_md).expanduser()
    if not target.is_file():
        die(f"File not found: {target}")
    result = preflight(target)
    reports_dir = resolve_reports_dir(args.reports_dir)
    result_path = save_stage(reports_dir, result)
    for row in result["findings"]:
        if row["severity"] == FAIL:
            print(
                f"FAIL {row['id']}: {row['message']} ({row['location']})",
                file=sys.stderr,
            )
    print(
        f"Preflight: {result['status']} "
        f"({len(result['findings'])} findings) -> {result_path}"
    )
    return EXIT_OK if result["status"] == PASS else 1


if __name__ == "__main__":
    sys.exit(main())
