from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from inventory_gate import enumerate_skills, fixture_diagnostics, lint_skill


class InventoryGateTest(unittest.TestCase):
    def test_only_immediate_directories_with_skill_md_are_enumerated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "codex" / "skills" / "ywc-real"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# real\n", encoding="utf-8")
            (root / "codex" / "skills" / "references").mkdir()
            nested = root / "codex" / "skills" / "scripts" / "nested"
            nested.mkdir(parents=True)
            (nested / "SKILL.md").write_text("# excluded\n", encoding="utf-8")

            self.assertEqual([item["name"] for item in enumerate_skills(root)], ["ywc-real"])

    def test_fixture_diagnostics_rejects_unknown_v2_skill_references(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "codex" / "skills" / "ywc-known"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# known\n", encoding="utf-8")
            fixtures = root / ".codex" / "skills" / "ywc-codex-toolkit-eval" / "evals" / "fixtures" / "safe"
            fixtures.mkdir(parents=True)
            (fixtures / "input.txt").write_text("input\n", encoding="utf-8")
            manifest = {
                "schema": 2,
                "id": "unknown-target",
                "prompt": "Check it.",
                "language": "en",
                "category": "boundary",
                "should_trigger": False,
                "expected_checks": [{"type": "file_exists", "path": "input.txt"}],
                "workspace": {
                    "fixture_root": "safe",
                    "target_skill": "unknown-skill",
                    "skill_dependencies": [],
                    "fixture_files": ["input.txt"],
                    "output_paths": [],
                    "evidence_packet": {},
                    "verifier_ids": [],
                },
            }
            evals = fixtures.parents[1] / "evals.json"
            evals.write_text(json.dumps(manifest), encoding="utf-8")

            diagnostics = fixture_diagnostics(root)

            self.assertFalse(diagnostics[0]["passed"])
            self.assertIn("unknown target skill", diagnostics[0]["error"])

            manifest["workspace"]["target_skill"] = "ywc-known"
            manifest["workspace"]["skill_dependencies"] = ["missing-dependency"]
            evals.write_text(json.dumps(manifest), encoding="utf-8")
            diagnostics = fixture_diagnostics(root)
            self.assertFalse(diagnostics[0]["passed"])
            self.assertIn("unknown dependency", diagnostics[0]["error"])

    def test_lint_suppression_requires_a_nonempty_reason(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_md = Path(tmp) / "SKILL.md"
            skill_md.write_text(
                "eval-lint: suppress=SKILL-L002 reason=\nrepeat\nrepeat\n",
                encoding="utf-8",
            )

            warnings = lint_skill(skill_md)

            self.assertFalse(warnings[0]["suppressed"])

            skill_md.write_text(
                "eval-lint: suppress=SKILL-L002 reason=legacy compatibility\nrepeat\nrepeat\n",
                encoding="utf-8",
            )
            self.assertTrue(lint_skill(skill_md)[0]["suppressed"])


if __name__ == "__main__":
    unittest.main()
