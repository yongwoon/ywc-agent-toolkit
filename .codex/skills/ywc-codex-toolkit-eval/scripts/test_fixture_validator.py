#!/usr/bin/env python3
"""Security-boundary tests for V1/V2 evaluator fixture validation."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fixture_validator import FixtureValidationError, validate_fixture
from verifier_registry import VERIFIER_REGISTRY, VerifierMode


def v2_fixture() -> dict:
    return {
        "schema": 2,
        "id": "safe-case",
        "prompt": "Validate the selected skill.",
        "language": "en",
        "category": "boundary",
        "should_trigger": False,
        "expected_checks": [{"type": "verifier", "verifier_id": "bundle.validate"}],
        "workspace": {
            "fixture_root": "safe",
            "target_skill": "ywc-plan",
            "skill_dependencies": [],
            "fixture_files": ["input.txt"],
            "output_paths": ["result.json"],
            "evidence_packet": {"request": "safe"},
            "verifier_ids": ["bundle.validate"],
        },
    }


class FixtureValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "safe").mkdir()
        (self.root / "safe" / "input.txt").write_text("input\n", encoding="utf-8")

    def test_v1_is_normalized_without_mutating_source(self) -> None:
        source = {"skill_name": "legacy", "evals": [{"id": 1, "prompt": "legacy"}]}
        normalized = validate_fixture(source, fixture_root=self.root)
        self.assertEqual(normalized["schema"], 1)
        self.assertEqual(normalized["v1_remaining"], 1)
        self.assertEqual(source["evals"][0]["id"], 1)

    def test_valid_v2_manifest_and_registry_verifier_pass(self) -> None:
        normalized = validate_fixture(v2_fixture(), fixture_root=self.root)
        self.assertEqual(normalized["schema"], 2)
        self.assertEqual(normalized["v1_remaining"], 0)

    def test_rejects_arbitrary_commands_and_path_escapes(self) -> None:
        for field, value in (("command", "sh -c id"), ("executable", "/bin/sh")):
            payload = v2_fixture()
            payload["expected_checks"][0][field] = value
            with self.assertRaisesRegex(FixtureValidationError, "not permitted"):
                validate_fixture(payload, fixture_root=self.root)
        payload = v2_fixture()
        payload["workspace"]["command"] = "id"
        with self.assertRaisesRegex(FixtureValidationError, "not permitted"):
            validate_fixture(payload, fixture_root=self.root)
        payload = v2_fixture()
        payload["workspace"]["fixture_files"] = ["../secret"]
        with self.assertRaisesRegex(FixtureValidationError, "relative path"):
            validate_fixture(payload, fixture_root=self.root)
        payload = v2_fixture()
        payload["expected_checks"] = [{"type": "file_exists", "path": "/tmp/escape"}]
        with self.assertRaisesRegex(FixtureValidationError, "relative path"):
            validate_fixture(payload, fixture_root=self.root)

    def test_rejects_symlink_escaping_fixture_root(self) -> None:
        outside = self.root / "outside.txt"
        outside.write_text("nope\n", encoding="utf-8")
        (self.root / "safe" / "escape").symlink_to(outside)
        payload = v2_fixture()
        payload["workspace"]["fixture_files"] = ["escape"]
        with self.assertRaisesRegex(FixtureValidationError, "escapes fixture root"):
            validate_fixture(payload, fixture_root=self.root)

    def test_rejects_v1_v2_ambiguity_unknown_dependency_and_bad_category(self) -> None:
        payload = v2_fixture()
        payload["evals"] = []
        with self.assertRaisesRegex(FixtureValidationError, "ambiguous"):
            validate_fixture(payload, fixture_root=self.root)
        payload = v2_fixture()
        payload["workspace"]["skill_dependencies"] = ["unknown"]
        with self.assertRaisesRegex(FixtureValidationError, "unknown dependency"):
            validate_fixture(payload, fixture_root=self.root, available_skills={"ywc-plan"})
        payload = v2_fixture()
        with self.assertRaisesRegex(FixtureValidationError, "unknown target skill"):
            validate_fixture(payload, fixture_root=self.root, available_skills={"other"})
        payload = v2_fixture()
        payload["category"] = "other"
        with self.assertRaisesRegex(FixtureValidationError, "category"):
            validate_fixture(payload, fixture_root=self.root)

    def test_registry_is_fixed_and_bundle_validation_is_checkout_readonly(self) -> None:
        entry = VERIFIER_REGISTRY["bundle.validate"]
        self.assertEqual(entry.mode, VerifierMode.SOURCE_CHECKOUT_READONLY)
        self.assertEqual(entry.argv, ("bash", "scripts/validate.sh"))
        self.assertTrue(entry.readonly_roots)

    def test_validates_v2_agent_fixture_without_allowing_commands(self) -> None:
        payload = {
            "schema": 2,
            "fixtures": [{
                "id": "agent-boundary",
                "agent": "ywc-reviewer",
                "input": {"prompt": "Review safely."},
                "evidence_packet": {"summary": "bounded"},
                "expected_status": "DONE",
                "expected_signals": ["bounded"],
                "forbidden_signals": ["shell"],
                "output_path": "outputs/result.md",
            }],
        }
        normalized = validate_fixture(payload, fixture_root=self.root)
        self.assertEqual(normalized["schema"], 2)
        payload["fixtures"][0]["command"] = "id"
        with self.assertRaisesRegex(FixtureValidationError, "not permitted"):
            validate_fixture(payload, fixture_root=self.root)


if __name__ == "__main__":
    unittest.main()
