from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from inventory_gate import enumerate_skills


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


if __name__ == "__main__":
    unittest.main()
