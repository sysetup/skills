#!/usr/bin/env python3
"""Validate the systems-engineering skill layout, frontmatter, and references."""

from __future__ import annotations

import argparse
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None
from pathlib import Path

SKILL_NAME = "systems-engineering"
MAX_NAME = 64
MAX_DESC = 1024
MAX_SKILL_LINES = 500
REQUIRED_TEMPLATES = (
    "business-needs-and-requirements-template.md",
    "configuration-baselines-template.md",
    "context-diagram-template.md",
    "conops-template.md",
    "design-review-checklist-template.md",
    "ffbd-template.md",
    "fmea-template.md",
    "evidence-register-template.md",
    "standards-applicability-template.md",
    "icd-template.md",
    "requirements-breakdown-structure-template.md",
    "risk-register-template.md",
    "semp-outline-template.md",
    "stakeholder-requirements-specification-template.md",
    "sysml-model-template.md",
    "system-requirements-specification-template.md",
    "traceability-matrix-template.md",
    "trade-off-analysis-matrix-template.md",
    "vv-plan-template.md",
    "work-breakdown-structure-template.md",
)
REQUIRED_REFERENCES = (
    "01-systems-fundamentals.md",
    "02-se-discipline-framework.md",
    "03-needs-requirements.md",
    "04-requirements-engineering.md",
    "05-conceptual-design.md",
    "06-preliminary-detailed.md",
    "07-construction-utilization.md",
    "08-se-management.md",
    "09-standards-glossary.md",
    "10-decision-frameworks.md",
    "11-mbse-interfaces-vv.md",
    "12-evidence-and-assurance.md",
)
REQUIRED_TRIGGERS = (
    "FMEA",
    "ICD",
    "SysML",
    "V-model",
    "ConOps",
    "Pugh",
    "Do not use when",
)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
TEMPLATE_TICK_RE = re.compile(r"`([a-z0-9-]+-template\.md)`")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate systems-engineering skill structure and references."
    )
    parser.add_argument(
        "-r",
        "--root",
        default=str(Path(__file__).resolve().parent.parent),
        help="Skill root directory. Default: parent of this script.",
    )
    return parser.parse_args()


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("SKILL.md is missing YAML frontmatter")
    if yaml is None:
        raise ValueError("PyYAML 6.x is required for YAML validation")

    class UniqueLoader(yaml.SafeLoader):
        def construct_mapping(self, node, deep=False):
            result = {}
            for key_node, value_node in node.value:
                key = self.construct_object(key_node, deep=deep)
                if not isinstance(key, str):
                    raise ValueError("frontmatter keys must be strings")
                if key in result:
                    raise ValueError(f"duplicate frontmatter key: {key}")
                result[key] = self.construct_object(value_node, deep=deep)
            return result

    try:
        data = yaml.load(match.group(1), Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise ValueError("invalid YAML frontmatter") from exc
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    allowed = {
        "name",
        "description",
        "license",
        "compatibility",
        "metadata",
        "allowed-tools",
    }
    if set(data) - allowed:
        raise ValueError("unsupported frontmatter fields")
    for key in allowed - {"metadata"}:
        if key in data and (not isinstance(data[key], str) or not data[key].strip()):
            raise ValueError(f"{key} must be a nonempty string")
    if len(data.get("compatibility", "")) > 500:
        raise ValueError("compatibility exceeds 500 characters")
    metadata = data.get("metadata")
    if not isinstance(metadata, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in metadata.items()
    ):
        raise ValueError("metadata must be a string-to-string mapping")
    if not re.fullmatch(
        r"[1-9][0-9]*\.[0-9]+(?:\.[0-9]+)?", metadata.get("version", "")
    ):
        raise ValueError("metadata.version must be a version string starting at 1.0")
    return data


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []
    skill = root / "SKILL.md"
    if not skill.is_file():
        print(f"ERROR: missing {skill}", file=sys.stderr)
        return 1
    if root.name != SKILL_NAME:
        fail(errors, f"directory name {root.name!r} does not match {SKILL_NAME!r}")
    text = skill.read_text(encoding="utf-8")
    lines = text.count("\n") + (0 if text.endswith("\n") else 1)
    if lines > MAX_SKILL_LINES:
        fail(errors, f"SKILL.md has {lines} lines; cap is {MAX_SKILL_LINES}")
    try:
        fm = parse_frontmatter(text)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    name = fm.get("name", "")
    description = fm.get("description", "")
    if name != SKILL_NAME:
        fail(errors, f"frontmatter name {name!r} != {SKILL_NAME!r}")
    if not NAME_RE.fullmatch(name) or len(name) > MAX_NAME:
        fail(errors, f"invalid skill name {name!r}")
    if not description:
        fail(errors, "description is empty")
    elif len(description) > MAX_DESC:
        fail(errors, f"description is {len(description)} chars; cap is {MAX_DESC}")
    body = FRONTMATTER_RE.sub("", text, count=1)
    if not body.lstrip().startswith(f"# {SKILL_NAME}\n"):
        fail(errors, "H1 must match the skill name")
    required_sections = (
        "Execution Workflow",
        "Output Contract",
        "Completion Verification",
    )
    positions = [body.find(f"\n## {heading}\n") for heading in required_sections]
    if min(positions) < 0 or positions != sorted(positions):
        fail(errors, "required local skeleton sections are missing or out of order")
    required_extras = (
        "scripts/engineering_checks.py",
        "scripts/validate-artifacts.py",
    )
    for extra in required_extras:
        if not (root / extra).is_file():
            fail(errors, f"missing {extra}")
    agent_path = root / "agents/openai.yaml"
    if agent_path.is_file():
        agent = agent_path.read_text(encoding="utf-8")
        for field in ("display_name", "short_description"):
            if not re.search(rf"^  {field}: [\"']?[^\s\"']", agent, re.M):
                fail(errors, f"agents/openai.yaml missing {field}")
        if not re.search(
            r"^  allow_implicit_invocation: (?:true|false)\s*$", agent, re.M
        ):
            fail(errors, "implicit invocation policy must be an explicit boolean")
        if re.search(r"^  products:", agent, re.M):
            fail(
                errors,
                "unsupported cross-host products metadata; use host-specific packaging separately",
            )
    for member in root.rglob("*"):
        if member.is_symlink():
            fail(errors, f"symlink in package: {member.relative_to(root)}")
        if member.name == "__pycache__" or member.suffix == ".pyc":
            fail(
                errors, f"generated Python cache in package: {member.relative_to(root)}"
            )
    for doc in root.rglob("*.md"):
        try:
            content = doc.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            fail(errors, f"unreadable Markdown {doc}: {exc}")
            continue
        for link in MD_LINK_RE.findall(content):
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            local = link.split("#", 1)[0]
            target = (doc.parent / local).resolve()
            if root != target and root not in target.parents:
                fail(errors, f"link escapes root in {doc.relative_to(root)}: {link}")
            elif not target.exists():
                fail(errors, f"broken link in {doc.relative_to(root)}: {link}")
    for trigger in REQUIRED_TRIGGERS:
        if trigger not in text:
            fail(errors, f"SKILL.md missing required trigger or section {trigger!r}")
    refs_dir = root / "references"
    templates_dir = root / "assets" / "templates"
    for ref in REQUIRED_REFERENCES:
        path = refs_dir / ref
        if not path.is_file():
            fail(errors, f"missing reference {path.relative_to(root)}")
    for template in REQUIRED_TEMPLATES:
        path = templates_dir / template
        if not path.is_file():
            fail(errors, f"missing template {path.relative_to(root)}")
    for link in MD_LINK_RE.findall(text):
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = (root / link).resolve()
        if root not in target.parents and target != root:
            fail(errors, f"link escapes skill root: {link}")
        elif not target.exists():
            fail(errors, f"broken markdown link {link}")
    for template in TEMPLATE_TICK_RE.findall(text):
        if not (templates_dir / template).is_file():
            fail(errors, f"SKILL.md lists missing template {template}")
    listed_refs = set(re.findall(r"references/([0-9]{2}-[a-z0-9-]+\.md)", text))
    for ref in REQUIRED_REFERENCES:
        if ref not in listed_refs:
            fail(errors, f"SKILL.md does not navigate to {ref}")
    if errors:
        print("VALIDATION FAILED")
        for item in errors:
            print(f"- {item}")
        return 1
    print("VALIDATION PASSED (package structure, not engineering or agent behavior)")
    print(f"root: {root}")
    print(f"name: {name}")
    print(f"description_chars: {len(description)}")
    print(f"skill_md_lines: {lines}")
    print(f"references: {len(REQUIRED_REFERENCES)}")
    print(f"templates: {len(REQUIRED_TEMPLATES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
