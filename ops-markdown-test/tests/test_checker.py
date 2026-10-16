"""Acceptance and regression tests; assessed files remain read-only."""

import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch


PACKAGE = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE / "scripts/check_markdown.py"
FIXTURES = PACKAGE / "fixtures"
SPEC = importlib.util.spec_from_file_location("checker", SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class ScannerTests(unittest.TestCase):
    def scan(self, text, new=False):
        return checker.scan("sample.md", text.encode("utf-8"), new)

    def test_plain_wrap_reports_exact_location(self):
        rows = self.scan("# Guide\n\nRead this\nwrapped paragraph.\n")
        self.assertEqual([(r["line"], r["rule"], r["category"]) for r in rows], [(3, "M02", "violation")])

    def test_unicode_and_long_paragraph_not_truncated(self):
        text = "# Guide\n\n" + "café inventory " * 2000 + "\n"
        self.assertEqual(self.scan(text, new=True), [])
        self.assertGreater(len(text), 80)

    def test_file_representation_depends_on_operation(self):
        for new, category in ((True, "violation"), (False, "exception")):
            with self.subTest(new=new):
                rows = checker.scan("sample.md", b"# Sample\r\n\r\nText", new)
                self.assertEqual([r["category"] for r in rows], [category, category])
        self.assertEqual(checker.scan("empty.md", b"", True)[0]["category"], "violation")

    def test_existing_hierarchy_is_preserved(self):
        text = "## Fragment\n\n#### Detail\n"
        self.assertEqual(self.scan(text)[0]["category"], "exception")
        self.assertEqual(self.scan(text, True)[0]["category"], "violation")
        self.assertEqual(self.scan("### Fragment\n", True), [])

    def test_fences_preserve_hash_comments_and_delimiter_lengths(self):
        text = "````bash\n# comment\nplain\nwrapped\n```\n# literal\n````\n\nFine.\n"
        self.assertEqual(self.scan(text, True), [])
        self.assertEqual(self.scan("~~~text\n## literal\na\nb\n~~~\n", True), [])

    def test_html_in_fenced_examples_is_literal(self):
        html = "<h1>Title</h1>\n<strong>Strong</strong>\n"
        for delimiter, label in (("```", "html"), ("~~~", "html"), ("````", "text")):
            for new in (False, True):
                with self.subTest(delimiter=delimiter, label=label, new=new):
                    text = f"{delimiter}{label}\n{html}{delimiter}\n"
                    self.assertEqual(self.scan(text, new), [])

    def test_raw_html_requires_review_instead_of_automatic_rejection(self):
        cases = ("<h1>Title</h1>\n", "<strong>Strong</strong>\n",
                 "<details>\n<summary>Details</summary>\n\nBody.\n</details>\n")
        for text in cases:
            for new in (False, True):
                with self.subTest(text=text, new=new):
                    rows = self.scan(text, new)
                    self.assertEqual([(r["category"], r["rule"]) for r in rows],
                                     [("review", "M09")])
        self.assertEqual(self.scan("# Title\n\n**Strong**\n", True), [])

    def test_existing_unlabeled_fence_is_exception(self):
        text = "```\nliteral\n```\n"
        self.assertEqual(self.scan(text)[0]["category"], "exception")
        self.assertEqual(self.scan(text, True)[0]["category"], "violation")

    def test_eof_fence_requests_review_not_syntax_error(self):
        rows = self.scan("```text\n# literal\na\nb\n")
        self.assertEqual([(r["category"], r["rule"]) for r in rows], [("review", "M06")])

    def test_frontmatter_protected_and_unclosed_boundary_reported(self):
        text = "---\ntitle: Sample\nwrapped:\n  - value\n---\n\nPlain prose.\n"
        rows = self.scan(text)
        self.assertEqual([r["category"] for r in rows], ["exception"])
        self.assertEqual(self.scan("---\n# metadata\na\nb\n")[0]["category"], "review")

    def test_containers_and_lazy_literals_never_get_prose_violations(self):
        cases = ["- Parent\n  - Nested\n    continued\n", "> quoted\nlazy continuation\n",
                 "- ```text\n\n# literal\na\nb\n```\n", "    # indented\n    a\n    b\n",
                 "> - Nested\n>   ```text\n>   a\n>   b\n>   ```\n"]
        for text in cases:
            with self.subTest(text=text):
                rows = self.scan(text, True)
                self.assertEqual({r["category"] for r in rows}, {"review"})

    def test_escaped_table_pipes_inline_spans_and_html_need_review(self):
        cases = ["| Field | Value |\n| --- | --- |\n| x | `a\\|b` |\n",
                 "Use `a\nb` here.\n", "<div>\na\n\nb\n</div>\n",
                 "[label]: destination\n  continued title\n"]
        for text in cases:
            with self.subTest(text=text):
                self.assertFalse(any(r["category"] == "violation" for r in self.scan(text)))
                self.assertTrue(any(r["category"] == "review" for r in self.scan(text)))

    def test_hard_break_forms_and_plain_colon(self):
        for text in ("First  \nsecond\n", "First\\\nsecond\n"):
            self.assertEqual(self.scan(text)[0]["category"], "exception")
        self.assertEqual(self.scan("Status: available.\n"), [])

    def test_setext_multiline_title_is_not_prose_violation(self):
        for text in ("A multiline\ntitle\n===\n", "Title\n=== \t\n", "# A\n\nB\n---\n\n### C\n"):
            with self.subTest(text=text):
                rows = self.scan(text, True)
                self.assertEqual([(r["category"], r["rule"]) for r in rows], [("review", "M04")])

    def test_limits_and_unsupported_inputs(self):
        for data in (b"\xff", b"a\x00b", b"a" * (checker.MAX_LINE + 1), b"x\n" * (checker.MAX_LINES + 1)):
            with self.subTest(length=len(data)):
                with self.assertRaises(ValueError):
                    checker.scan("sample.md", data)
        rows = self.scan("a\nb\n\n" * (checker.MAX_FINDINGS + 2))
        self.assertEqual(len(rows), checker.MAX_FINDINGS + 1)
        self.assertEqual(rows[-1]["category"], "error")

    def test_path_validation(self):
        for value in ("/guide.md", "../guide.md", "nested/../../guide.md", ".", "guide.txt"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    checker.relative_path(value)

    def test_bounded_reads_and_non_directory_components(self):
        with checker.ReadScope(str(PACKAGE)) as scope:
            with patch.object(checker, "MAX_BYTES", 16):
                with self.assertRaisesRegex(ValueError, "read limit"):
                    scope.read("SKILL.md")
            with self.assertRaises(NotADirectoryError):
                scope.read("SKILL.md/child.md")

    def test_author_edit_changes_only_incidental_wrap(self):
        before = (FIXTURES / "wrapped.md").read_bytes()
        after = (FIXTURES / "edited.md").read_bytes()
        self.assertEqual(after, before.replace(b"`status` value\nbefore", b"`status` value before"))
        self.assertIn(b"line  \nsecond", after)
        self.assertIn(b"# Keep this comment", after)
        self.assertFalse(any(r["category"] == "violation" for r in checker.scan("edited.md", after)))


@unittest.skipUnless(os.environ.get("OPS_MARKDOWN_STANDARD"), "Supply the exact standard through OPS_MARKDOWN_STANDARD")
class CLITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.standard = Path(os.environ["OPS_MARKDOWN_STANDARD"]).absolute()
        cls.root = Path(os.path.commonpath([PACKAGE, cls.standard.parent]))
        cls.standard_arg = str(cls.standard.relative_to(cls.root))
        cls.fixture_prefix = FIXTURES.relative_to(cls.root)

    def cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), *args], text=True,
                              capture_output=True, timeout=10, check=False)

    def check(self, name, *options):
        return self.cli("--root", str(self.root), "--standard", self.standard_arg,
                        *options, "--", str(self.fixture_prefix / name))

    def test_help_and_zero_arguments(self):
        help_result = self.cli("--help")
        self.assertEqual(help_result.returncode, 0)
        self.assertIn("--standard", help_result.stdout)
        empty = self.cli()
        self.assertEqual(empty.returncode, 2)
        self.assertIn("usage:", empty.stderr)

    def test_all_exit_statuses_and_json_contract(self):
        cases = [("edited.md", 0), ("review.md", 1), ("absent.md", 2), ("created.md", 3)]
        for name, status in cases:
            with self.subTest(name=name):
                result = self.check(name, "--format", "json")
                self.assertEqual(result.returncode, status, result.stderr + result.stdout)
                report = json.loads(result.stdout)
                self.assertEqual(report["exit_status"], status)
                self.assertEqual(report["coverage"], "partial")
                self.assertTrue(report["unassessed"])
                self.assertIn("M10", report["unassessed"])
                for row in report["findings"]:
                    self.assertEqual(set(row), {"file", "line", "column", "category", "rule", "explanation", "correction"})

    def test_review_and_entire_cli_leave_inputs_unchanged(self):
        paths = [self.standard, *sorted(FIXTURES.glob("*.md"))]
        before = [hashlib.sha256(p.read_bytes()).digest() for p in paths]
        first = self.check("review.md", "--format", "json")
        second = self.check("review.md", "--format", "json")
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, [hashlib.sha256(p.read_bytes()).digest() for p in paths])
        human = self.check("review.md").stdout
        self.assertIn(":3:1: violation M02", human)

    def test_wrong_standard_stops_before_documents(self):
        result = self.cli("--root", str(self.root), "--standard", str(self.fixture_prefix / "edited.md"),
                          "--format", "json", "--", str(self.fixture_prefix / "review.md"))
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["documents_attempted"], 0)

    def test_invalid_duplicate_and_unavailable_root(self):
        for paths in (("../outside.md",), ("/outside.md",), ("guide.md", "guide.md"), ("x.md",) * 33):
            result = self.cli("--root", str(self.root), "--standard", self.standard_arg, *paths)
            self.assertEqual(result.returncode, 2)
        result = self.cli("--root", str(self.root / "absent"), "--standard", "standard.md", "guide.md")
        self.assertEqual(result.returncode, 2)

    def test_input_errors_preserve_other_results_and_do_not_echo_contents(self):
        standard = self.standard.read_bytes()
        with patch.object(checker.ReadScope, "read", side_effect=[standard, b"\xff", b"plain\nwrapped\n"]):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = checker.main(["--root", str(self.root), "--standard", self.standard_arg,
                                       "--format", "json", "bad.md", "good.md"])
        report = json.loads(output.getvalue())
        self.assertEqual(status, 2)
        self.assertEqual(report["counts"]["violation"], 1)
        self.assertEqual(report["counts"]["error"], 1)

    def test_bad_path_identifies_input_and_preserves_valid_peer(self):
        good = str(self.fixture_prefix / "review.md")
        result = self.cli("--root", str(self.root), "--standard", self.standard_arg,
                          "--format", "json", "--", good, "bad.txt")
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["documents_attempted"], 2)
        self.assertEqual(report["counts"]["violation"], 1)
        error = next(row for row in report["findings"] if row["category"] == "error")
        self.assertEqual((error["file"], error["rule"]), ("bad.txt", "input"))


if __name__ == "__main__":
    unittest.main()
