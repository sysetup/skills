import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_frontmatter(text: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    data: dict = {}
    current_key = None
    current_list: list[str] | None = None
    folded: list[str] | None = None
    for raw_line in match.group(1).splitlines():
        if current_list is not None and raw_line.startswith("  - "):
            current_list.append(raw_line[4:].strip().strip('"'))
            continue
        if folded is not None and raw_line.startswith("  "):
            folded.append(raw_line.strip())
            continue
        current_list = None
        folded = None
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_key = key
        if value in {">", ">-"}:
            folded = []
            data[key] = folded
            continue
        if value == "":
            current_list = []
            data[key] = current_list
            continue
        data[key] = value.strip('"')
    if current_key and isinstance(data.get(current_key), list) and data[current_key] and isinstance(data[current_key][0], str) and current_key == "description":
        pass
    for key, value in list(data.items()):
        if isinstance(value, list) and key == "description":
            data[key] = " ".join(value)
        elif isinstance(value, list) and key != "allowed-tools" and not value:
            data[key] = {}
    return data


class SkillDocumentationTests(unittest.TestCase):
    def test_skill_authority_precedence_matches_source_authority(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("4. Scripts under `scripts/`", skill_text)
        self.assertIn("5. Templates under `assets/templates/`", skill_text)

    def test_templates_require_explicit_assumptions_where_outputs_are_non_trivial(self) -> None:
        change_request = (ROOT / "assets/templates/change-request.md").read_text(encoding="utf-8")
        test_matrix = (ROOT / "assets/templates/network-test-matrix.md").read_text(encoding="utf-8")
        ops_plan = (ROOT / "assets/templates/operations-maintenance-plan.md").read_text(encoding="utf-8")

        self.assertIn("## 4. Assumptions", change_request)
        self.assertIn("## 2. Assumptions", test_matrix)
        self.assertIn("## 2. Assumptions", ops_plan)

    def test_openai_yaml_exists_for_machine_readable_skill_metadata(self) -> None:
        openai_yaml = ROOT / "agents/openai.yaml"
        self.assertTrue(openai_yaml.exists(), "agents/openai.yaml should exist")

    def test_python_cache_is_not_shipped(self) -> None:
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("__pycache__/", gitignore)
        self.assertIn("*.py[cod]", gitignore)

    def test_frontmatter_declares_version_and_allowed_tools(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        self.assertEqual(frontmatter.get("name"), "networking")
        self.assertRegex(str(frontmatter.get("version")), r"^\d+\.\d+\.\d+$")
        self.assertEqual(frontmatter.get("allowed-tools"), ["read", "write", "python", "bash"])
        description = " ".join(str(frontmatter.get("description") or "").split())
        self.assertGreaterEqual(len(description), 20)
        self.assertLessEqual(len(description), 300)

    def test_no_pdf_exists_in_skill_tree(self) -> None:
        pdfs = [path for path in ROOT.rglob("*.pdf") if ".git" not in path.parts]
        self.assertEqual(pdfs, [])

    def test_declared_relative_files_exist(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        refs = set(
            re.findall(
                r"(?:scripts|references|assets)/[A-Za-z0-9._/-]+\.(?:md|py|sh)",
                text,
            )
        )
        self.assertGreater(len(refs), 10)
        missing = [rel for rel in sorted(refs) if not (ROOT / rel).is_file()]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
