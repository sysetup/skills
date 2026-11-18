#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Regression and schema-equivalence tests for validate-question-set.py."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import unittest

import jsonschema

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
VALIDATOR_PATH = SCRIPT_DIR / "validate-question-set.py"
SCHEMA_PATH = SCRIPT_DIR.parent / "schemas" / "question-set.schema.json"
EXAMPLE_PATH = SCRIPT_DIR.parent / "assets" / "question-set.example.json"


def _load_validator_module() -> object:
    """Load validate-question-set.py as a module for unit checks."""
    spec = importlib.util.spec_from_file_location(
        "validate_question_set", VALIDATOR_PATH
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["validate_question_set"] = module
    spec.loader.exec_module(module)
    return module


def _single_select_with_preview(preview: str) -> dict[str, object]:
    """Build a single-select question set with a given preview string."""
    return {
        "questions": [
            {
                "id": "choice-one",
                "text": "Pick one option?",
                "kind": "single-select",
                "required": True,
                "options": [
                    {
                        "label": "First (Recommended)",
                        "description": "Use first choice.",
                        "preview": preview,
                    },
                    {
                        "label": "Second",
                        "description": "Use second choice.",
                    },
                ],
                "default": "First (Recommended)",
            }
        ]
    }


def _free_text_with_default(default: str) -> dict[str, object]:
    """Build a free-text question set with zero options and given default."""
    return {
        "questions": [
            {
                "id": "free-one",
                "text": "Provide target label?",
                "kind": "free-text",
                "required": False,
                "options": [],
                "default": default,
            }
        ]
    }


class ValidateQuestionSetTests(unittest.TestCase):
    """Verify boundary limits and JSON Schema equivalence."""

    validator = _load_validator_module()
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    draft7 = jsonschema.Draft7Validator(schema)

    def _assert_equivalent(self, payload: dict[str, object], valid: bool) -> None:
        """Assert both validator script and Draft-7 schema agree."""
        schema_errors = list(self.draft7.iter_errors(payload))
        script_errors = self.validator.validate_data(payload)
        if valid:
            self.assertEqual(schema_errors, [])
            self.assertEqual(script_errors, [])
        else:
            self.assertTrue(schema_errors)
            self.assertTrue(script_errors)

    def test_example_fixture_passes_both(self) -> None:
        """Example payload passes both schema and validator script."""
        payload = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
        self._assert_equivalent(payload, valid=True)

    def test_preview_length_boundaries(self) -> None:
        """Preview allows 4000 chars and rejects 4001 chars."""
        self._assert_equivalent(_single_select_with_preview("x" * 4000), valid=True)
        self._assert_equivalent(_single_select_with_preview("x" * 4001), valid=False)

    def test_free_text_default_length_boundaries(self) -> None:
        """Free-text default allows 80 chars and rejects 81 chars."""
        self._assert_equivalent(_free_text_with_default("d" * 80), valid=True)
        self._assert_equivalent(_free_text_with_default("d" * 81), valid=False)


if __name__ == "__main__":
    unittest.main()
