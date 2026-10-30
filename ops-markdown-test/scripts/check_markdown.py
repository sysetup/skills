"""Read-only, deliberately partial checks against one finalized Markdown standard."""

import argparse
import hashlib
import json
import os
from pathlib import PurePosixPath
import re
import stat
import sys


STANDARD_SHA256 = "61991c4fdd665c8a903f31ff466ab3b28c523160a4ca3f872a80c152add62123"
MAX_FILES, MAX_BYTES, MAX_LINES, MAX_LINE, MAX_FINDINGS = 32, 1048576, 20000, 65536, 200
UNASSESSED = ["M03", "M05", "M07", "M08", "M09", "M10", "context-dependent parts of M01/M02/M04/M06"]
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+|$)")
CONTAINER = re.compile(r"^ {0,3}(?:>|[-+*](?:[ \t]|$)|[0-9]{1,9}[.)](?:[ \t]|$))")
THEMATIC = re.compile(r"^ {0,3}(?:\*[ \t]*){3,}$|^ {0,3}(?:-[ \t]*){3,}$|^ {0,3}(?:_[ \t]*){3,}$")


def finding(file, line, category, rule, explanation, correction):
    return dict(file=file, line=line, column=1 if line else None, category=category,
                rule=rule, explanation=explanation, correction=correction)


def relative_path(value):
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError("Use an explicit relative path without parent traversal.")
    if path.suffix.lower() not in (".md", ".markdown"):
        raise ValueError("Input must have a .md or .markdown suffix.")
    return path


class ReadScope:
    """Own the root descriptor; every opened child stays beneath that descriptor."""

    def __init__(self, root):
        self.root = root
        self.fd = None

    def __enter__(self):
        self.fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        return self

    def __exit__(self, *unused):
        os.close(self.fd)

    def read(self, value):
        parts = relative_path(value).parts
        directory = os.dup(self.fd)
        try:
            for part in parts[:-1]:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                dir_fd=directory)
                os.close(directory)
                directory = child
            descriptor = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                 dir_fd=directory)
            with os.fdopen(descriptor, "rb") as stream:
                if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                    raise ValueError("Input must be a regular file.")
                data = stream.read(MAX_BYTES + 1)
                if len(data) > MAX_BYTES:
                    raise ValueError("Input exceeds the 1 MiB read limit.")
                return data
        finally:
            os.close(directory)


def scan(file, data, new=False):
    """Mask literals first; classify ambiguous layout before asserting prose rules."""
    findings = []

    def add(line, category, rule, explanation, correction):
        if len(findings) <= MAX_FINDINGS:
            findings.append(finding(file, line, category, rule, explanation, correction))

    text = data.decode("utf-8-sig")
    if "\x00" in text:
        raise ValueError("NUL bytes are unsupported.")
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if lines[-1] == "":
        lines.pop()
    if len(lines) > MAX_LINES or any(len(line) > MAX_LINE for line in lines):
        raise ValueError("Input exceeds the line count or line length limit.")
    if b"\r" in data:
        add(1, "violation" if new else "exception", "M01", "Non-LF line endings found.",
            "Use LF for new documents; confirm existing representation requirements before conversion.")
    if not data.endswith(b"\n"):
        add(len(lines) or 1, "violation" if new else "exception", "M01", "No final LF newline.",
            "Add a final LF for new documents; preserve an existing required representation.")

    visible = [True] * len(lines)
    start = 0
    if lines and lines[0] in ("---", "+++"):
        terminators = ("---", "...") if lines[0] == "---" else ("+++",)
        end = next((i for i in range(1, len(lines)) if lines[i] in terminators), None)
        if end is None:
            add(1, "review", "M09", "Frontmatter boundary is unresolved; remaining layout unassessed.",
                "Confirm the frontmatter dialect and closing boundary manually.")
            return findings
        visible[:end + 1] = [False] * (end + 1)
        start = end + 1
        add(1, "exception", "M09", "Frontmatter retained as literal metadata.", "Preserve its document-specific syntax.")

    # Collect fence findings provisionally: containers can invalidate this simple parse.
    fences = []
    i = start
    while i < len(lines):
        marker = FENCE.match(lines[i])
        if marker:
            delimiter, info = marker.groups()
            end = i + 1
            while end < len(lines):
                close = FENCE.match(lines[end])
                if close and close[1][0] == delimiter[0] and len(close[1]) >= len(delimiter) and not close[2].strip():
                    break
                end += 1
            visible[i:min(end + 1, len(lines))] = [False] * (min(end + 1, len(lines)) - i)
            if delimiter[0] == "`" and "`" in info:
                fences.append((i + 1, "review", "M06", "Ambiguous backtick fence info string.", "Inspect the literal boundary manually."))
            elif not info.strip():
                fences.append((i + 1, "violation" if new else "exception", "M06", "Fence has no language label.", "Use a known language or text for new examples; preserve existing literals."))
            if end == len(lines):
                fences.append((i + 1, "review", "M06", "Fence extends to EOF; remaining content is protected.", "Confirm intended literal extent; an EOF-terminated fence is legal GFM."))
            i = end + 1
        else:
            i += 1

    complex_line = next((i for i in range(start, len(lines)) if visible[i] and lines[i].strip()
                         and (CONTAINER.match(lines[i]) or "<" in lines[i]
                              or lines[i].startswith((" ", "\t")))), None)
    if complex_line is not None:
        add(complex_line + 1, "review", "M09", "Containers, HTML, or indentation require manual structural assessment for this document.",
            "Review M02-M10 with the applicable dialect; nested literals and lazy continuations are not parsed.")
        return findings
    for note in fences:
        add(*note)

    paragraph = []
    previous_level = 0

    def flush():
        if not paragraph:
            return
        first = paragraph[0][0]
        content = [line for _, line in paragraph]
        if len(content) > 1 and any(":::" in line or any(char in line for char in "`[]*_\\${}") for line in content):
            hard_break = any(line.endswith("  ") or (len(line) - len(line.rstrip("\\"))) % 2 for line in content[:-1])
            if hard_break:
                add(first, "exception", "M02", "Intentional rendered-break markers retained.", "Preserve meaningful source breaks and inspect inline semantics.")
            else:
                add(first, "review", "M02", "Inline or extension constructs make paragraph boundaries uncertain.", "Review inline spans and paragraph intent without flattening constructs.")
        elif any("|" in line for line in content):
            add(first, "review", "M07", "Table-like content is not parsed.", "Review cells, escaped pipes, header and delimiter rows manually.")
        elif any(line.endswith("  ") for line in content[:-1]):
            add(first, "exception", "M02", "Intentional rendered-break markers retained.", "Preserve meaningful source breaks.")
        elif len(content) > 1:
            add(first, "violation", "M02", "Plain top-level prose spans multiple source lines.", "Confirm one paragraph, then join incidental wrapping without changing words.")
        paragraph.clear()

    for index, line in enumerate(lines):
        if not visible[index] or not line.strip():
            flush()
            continue
        heading = HEADING.match(line)
        if heading:
            flush()
            level = len(heading[1])
            if previous_level and level > previous_level + 1:
                add(index + 1, "violation" if new else "exception", "M04", "ATX hierarchy descends more than one level.",
                    "Use a coherent new hierarchy; preserve existing levels unless restructuring is authorized.")
            previous_level = level
        elif re.fullmatch(r"(?:=+|-+)[ \t]*", line) and paragraph:
            paragraph.clear()
            previous_level = 0
            add(index + 1, "review", "M04", "Possible setext heading requires contextual assessment.", "Use ATX for new headings; preserve established structures when required.")
        elif THEMATIC.fullmatch(line):
            flush()
        else:
            paragraph.append((index + 1, line))
    flush()
    if len(findings) > MAX_FINDINGS:
        return findings[:MAX_FINDINGS] + [finding(file, None, "error", "limit", "Finding limit reached; scan output is partial.", "Assess smaller explicit files or complete manual review.")]
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        "Read-only; partial coverage only. Exit: 0 no automated issue, 1 violations, "
        "2 input/standard/limit error, 3 local manual review needed. "
        "Limits: 32 files, 1 MiB each, 20000 lines, 65536 chars/line, 200 findings/file."))
    parser.add_argument("--root", required=True, help="Explicit authorized assessment root")
    parser.add_argument("--standard", required=True, help="Exact finalized standard; root-relative Markdown path")
    parser.add_argument("--new", action="store_true", help="Apply new-document M01/M04/M06 conventions to all inputs")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("files", nargs="+", help="Explicit root-relative .md/.markdown paths; no recursion")
    args = parser.parse_args(argv)
    findings = []
    digest = None
    attempted = 0
    context_file, context_rule = "<inputs>", "input"
    try:
        if len(args.files) > MAX_FILES:
            raise ValueError("At most 32 document inputs are allowed.")
        context_file, context_rule = args.root, "scope"
        with ReadScope(args.root) as scope:
            context_file, context_rule = args.standard, "standard"
            standard = scope.read(args.standard)
            digest = hashlib.sha256(standard).hexdigest()
            if digest != STANDARD_SHA256:
                raise ValueError("Standard digest mismatch; reconcile the rule mapping before assessment.")
            seen = set()
            for file in args.files:
                attempted += 1
                try:
                    path = relative_path(file)
                    if path in seen:
                        raise ValueError("Duplicate input path is not allowed.")
                    seen.add(path)
                    findings.extend(scan(file, scope.read(file), args.new))
                except (OSError, ValueError) as error:
                    if isinstance(error, UnicodeError):
                        reason = "Input encoding is not supported; UTF-8 is required for automated assessment."
                    else:
                        reason = "Cannot read input within the selected root." if isinstance(error, OSError) else str(error)
                    findings.append(finding(file, None, "error", "input", reason, "Confirm scope, file availability, limits and UTF-8 encoding."))
    except (OSError, ValueError) as error:
        reason = "Cannot access the selected root or standard." if isinstance(error, OSError) else str(error)
        findings.append(finding(context_file, None, "error", context_rule, reason, "Supply authorized inputs and the exact finalized standard."))
    counts = {category: sum(row["category"] == category for row in findings)
              for category in ("violation", "exception", "review", "error")}
    status = 2 if counts["error"] else 1 if counts["violation"] else 3 if counts["review"] else 0
    report = dict(coverage="partial", unassessed=UNASSESSED, standard_sha256=digest,
                  documents_attempted=attempted, counts=counts, findings=findings, exit_status=status)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=True, indent=2))
    else:
        for row in findings:
            location = json.dumps(row["file"], ensure_ascii=True) + (f":{row['line']}:{row['column']}" if row["line"] else "")
            print(f"{location}: {row['category']} {row['rule']}: {row['explanation']} {row['correction']}")
        print(f"Partial coverage; counts={counts}; exit={status}. Full standard requires manual review.")
    return status


if __name__ == "__main__":
    sys.exit(main())
