#!/usr/bin/env python3
"""Unit tests for the v2 fixture validator and the verifier registry.

Guards the two contracts every later task in this batch builds on
(000067-010): the v2 case shape (AC3), the closed `expected_checks`
whitelist (AC4), and `fixture_root` boundary sealing (AC5).

The central invariant under test is that a fixture is *data*, never a
command: no fixture string may reach a verifier's argv, and no path may
resolve outside `fixture_root`. Without that, running the evaluation is
arbitrary code execution.

Stdlib only (`unittest`), matching score.py's no-dependency convention. Run with:

  python3 .claude/skills/ywc-toolkit-eval/scripts/test_fixture_schema.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Import the sibling modules regardless of the caller's CWD.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fixture_schema  # noqa: E402
import verifier_registry  # noqa: E402


def _valid_case(**overrides) -> dict:
    """A minimal well-formed v2 case; overrides let each test bend one field."""
    case = {
        "schema": 2,
        "id": "sample-happy-1",
        "prompt": "이 스킬로 작업을 실행해줘",
        "language": "ko",
        "category": "happy_path",
        "should_trigger": True,
        "expected_checks": [{"type": "stdout_regex", "pattern": "DONE"}],
    }
    case.update(overrides)
    return case


class V2RequiredFieldsTest(unittest.TestCase):
    """AC3 — a v2 case carries exactly the six required fields."""

    def test_valid_case_has_no_errors(self) -> None:
        self.assertEqual(fixture_schema.validate_case(_valid_case()), [])

    def test_each_missing_required_field_is_reported(self) -> None:
        for field in fixture_schema.REQUIRED_FIELDS:
            case = _valid_case()
            del case[field]
            errors = fixture_schema.validate_case(case)
            self.assertTrue(
                any(field in e for e in errors),
                f"missing {field!r} was not reported: {errors}")

    def test_should_trigger_must_be_boolean(self) -> None:
        errors = fixture_schema.validate_case(_valid_case(should_trigger="yes"))
        self.assertTrue(any("should_trigger" in e for e in errors))

    def test_language_must_be_non_empty_string(self) -> None:
        self.assertTrue(fixture_schema.validate_case(_valid_case(language="")))


class V2CategoryTest(unittest.TestCase):
    """AC3 — `category` is exactly one of the three declared values."""

    def test_all_declared_categories_pass(self) -> None:
        for category in ("happy_path", "negative", "boundary"):
            self.assertEqual(
                fixture_schema.validate_case(_valid_case(category=category)), [],
                f"{category!r} should be accepted")

    def test_unsupported_category_is_rejected(self) -> None:
        errors = fixture_schema.validate_case(_valid_case(category="edge_case"))
        self.assertTrue(any("category" in e for e in errors))


class CheckWhitelistTest(unittest.TestCase):
    """AC4 — `expected_checks` accepts only the six whitelisted types."""

    def test_every_whitelisted_type_is_accepted(self) -> None:
        for check_type in fixture_schema.CHECK_TYPES:
            check = {"type": check_type}
            if check_type == "verifier":
                check["verifier_id"] = next(iter(verifier_registry.verifier_ids()))
            self.assertEqual(
                fixture_schema.validate_case(_valid_case(expected_checks=[check])), [],
                f"{check_type!r} should be accepted")

    def test_unknown_check_type_is_rejected(self) -> None:
        errors = fixture_schema.validate_case(
            _valid_case(expected_checks=[{"type": "shell_exec"}]))
        self.assertTrue(any("shell_exec" in e for e in errors))

    def test_empty_expected_checks_is_rejected(self) -> None:
        self.assertTrue(fixture_schema.validate_case(_valid_case(expected_checks=[])))

    def test_free_form_command_keys_are_rejected(self) -> None:
        # The whole point of the whitelist: a fixture must not be able to name
        # a command, an interpreter, or an executable path anywhere.
        for key in ("command", "argv", "shell", "exec", "executable", "cmd", "script"):
            errors = fixture_schema.validate_case(
                _valid_case(expected_checks=[{"type": "stdout_regex", key: "/bin/sh"}]))
            self.assertTrue(
                any(key in e for e in errors),
                f"free-form {key!r} was not rejected: {errors}")

    def test_verifier_check_requires_registered_id(self) -> None:
        errors = fixture_schema.validate_case(
            _valid_case(expected_checks=[{"type": "verifier", "verifier_id": "rm -rf /"}]))
        self.assertTrue(any("verifier_id" in e for e in errors))

    def test_verifier_check_without_id_is_rejected(self) -> None:
        self.assertTrue(fixture_schema.validate_case(
            _valid_case(expected_checks=[{"type": "verifier"}])))


class V1CompatibilityTest(unittest.TestCase):
    """v1 fixtures stay readable — this task must not break existing datasets."""

    def test_v1_case_passes_read_only(self) -> None:
        v1 = {"id": "agentic-pos-1", "prompt": "자율 실행", "expected": "ywc-agentic",
              "kind": "positive"}
        self.assertEqual(fixture_schema.validate_case(v1), [])

    def test_v1_is_not_v2(self) -> None:
        self.assertFalse(fixture_schema.is_v2({"schema": 1}))
        self.assertFalse(fixture_schema.is_v2({}))
        self.assertTrue(fixture_schema.is_v2({"schema": 2}))

    def test_shipped_v1_datasets_still_validate(self) -> None:
        evals_dir = Path(__file__).resolve().parents[1] / "evals"
        cases = json.loads(
            (evals_dir / "trigger-cases.json").read_text(encoding="utf-8"))["cases"]
        for case in cases:
            self.assertEqual(fixture_schema.validate_case(case), [],
                             f"v1 trigger case {case.get('id')!r} regressed")


class ManifestBoundaryTest(unittest.TestCase):
    """AC5 — every declared path resolves inside `fixture_root`."""

    def _root(self, tmp: str) -> Path:
        root = Path(tmp) / "fixtures"
        (root / "case").mkdir(parents=True)
        (root / "case" / "input.txt").write_text("x", encoding="utf-8")
        return root

    def test_relative_paths_inside_root_are_normalized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            manifest = fixture_schema.normalize_manifest(
                _valid_case(fixture_files=["case/input.txt"],
                            output_paths=["case/out.json"],
                            target_skill="ywc-toolkit-eval"),
                root)
            self.assertEqual(manifest["target_skill"], "ywc-toolkit-eval")
            self.assertEqual(manifest["fixture_root"], str(root.resolve()))
            for key in ("fixture_files", "output_paths"):
                for resolved in manifest[key]:
                    self.assertTrue(resolved.startswith(str(root.resolve())))

    def test_parent_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            with self.assertRaises(fixture_schema.ManifestError):
                fixture_schema.normalize_manifest(
                    _valid_case(fixture_files=["../escape.txt"]), root)

    def test_absolute_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            with self.assertRaises(fixture_schema.ManifestError):
                fixture_schema.normalize_manifest(
                    _valid_case(fixture_files=["/etc/passwd"]), root)

    def test_symlink_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            outside = Path(tmp) / "outside.txt"
            outside.write_text("secret", encoding="utf-8")
            os.symlink(outside, root / "case" / "link.txt")
            with self.assertRaises(fixture_schema.ManifestError):
                fixture_schema.normalize_manifest(
                    _valid_case(fixture_files=["case/link.txt"]), root)

    def test_undeclared_output_path_is_not_invented(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            manifest = fixture_schema.normalize_manifest(_valid_case(), root)
            self.assertEqual(manifest["output_paths"], [])
            self.assertEqual(manifest["fixture_files"], [])

    def test_invalid_case_cannot_produce_a_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            with self.assertRaises(fixture_schema.ManifestError):
                fixture_schema.normalize_manifest(_valid_case(category="nope"), root)

    def test_verifier_ids_must_be_registered(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            with self.assertRaises(fixture_schema.ManifestError):
                fixture_schema.normalize_manifest(
                    _valid_case(verifier_ids=["bash -c whoami"]), root)


class VerifierRegistryTest(unittest.TestCase):
    """AC4 — the evaluator owns argv; a fixture can only name a registry id."""

    def test_resolve_returns_the_declared_contract(self) -> None:
        for verifier_id in verifier_registry.verifier_ids():
            entry = verifier_registry.resolve(verifier_id)
            for field in ("argv", "cwd", "timeout", "env_allowlist", "expected_exit"):
                self.assertIn(field, entry, f"{verifier_id} missing {field}")
            self.assertIsInstance(entry["argv"], list)
            self.assertTrue(entry["argv"], f"{verifier_id} has an empty argv")

    def test_unknown_id_raises(self) -> None:
        with self.assertRaises(verifier_registry.UnknownVerifier):
            verifier_registry.resolve("no-such-verifier")

    def test_resolve_returns_a_copy_so_callers_cannot_mutate_the_registry(self) -> None:
        verifier_id = next(iter(verifier_registry.verifier_ids()))
        entry = verifier_registry.resolve(verifier_id)
        entry["argv"].append("--injected")
        entry["timeout"] = 99999
        fresh = verifier_registry.resolve(verifier_id)
        self.assertNotIn("--injected", fresh["argv"])
        self.assertNotEqual(fresh["timeout"], 99999)

    def test_no_entry_invokes_a_shell_interpreter(self) -> None:
        shells = {"sh", "bash", "zsh", "dash", "fish", "cmd", "cmd.exe",
                  "powershell", "pwsh", "env", "eval", "xargs"}
        for verifier_id in verifier_registry.verifier_ids():
            argv = verifier_registry.resolve(verifier_id)["argv"]
            program = Path(argv[0]).name
            self.assertNotIn(program, shells,
                             f"{verifier_id} shells out via {program!r}")
            self.assertNotIn("-c", argv[:2],
                             f"{verifier_id} passes an inline command string")

    def test_env_allowlist_excludes_credentials(self) -> None:
        banned = {"ANTHROPIC_API_KEY", "GITHUB_TOKEN", "GH_TOKEN", "AWS_SECRET_ACCESS_KEY"}
        for verifier_id in verifier_registry.verifier_ids():
            allowed = set(verifier_registry.resolve(verifier_id)["env_allowlist"])
            self.assertEqual(allowed & banned, set(),
                             f"{verifier_id} inherits credentials")

    def test_argv_is_constant_and_never_carries_fixture_text(self) -> None:
        # The proof that a fixture string cannot reach argv: resolution takes
        # only an id, so there is no channel for fixture content to travel.
        hostile = "sample-happy-1; rm -rf /"
        with self.assertRaises(verifier_registry.UnknownVerifier):
            verifier_registry.resolve(hostile)
        for verifier_id in verifier_registry.verifier_ids():
            first = verifier_registry.resolve(verifier_id)["argv"]
            second = verifier_registry.resolve(verifier_id)["argv"]
            self.assertEqual(first, second)
            self.assertNotIn(hostile, first)


class ShippedFixturesTest(unittest.TestCase):
    """The representative v2 fixtures shipped with this task must be valid."""

    def test_bundled_v2_fixtures_validate(self) -> None:
        fixture_root = Path(__file__).resolve().parents[1] / "evals" / "fixtures"
        files = sorted(fixture_root.glob("*.json"))
        self.assertTrue(files, "no v2 fixtures found under evals/fixtures/")
        categories = set()
        for path in files:
            case = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(fixture_schema.is_v2(case), f"{path.name} is not schema 2")
            self.assertEqual(fixture_schema.validate_case(case), [],
                             f"{path.name} failed validation")
            fixture_schema.normalize_manifest(case, fixture_root)
            categories.add(case["category"])
        self.assertIn("happy_path", categories)
        self.assertIn("negative", categories)


if __name__ == "__main__":
    unittest.main()
