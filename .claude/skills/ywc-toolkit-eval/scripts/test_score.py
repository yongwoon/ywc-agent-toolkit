#!/usr/bin/env python3
"""Unit tests for the mechanical scorer (score.py).

Protects the rubric<->implementation alignment for the logic landed in task
000009-010 (FR2/FR3/FR4/FR6/FR10) so future edits cannot silently drift the
scorer away from references/skill-rubric.md and references/agent-rubric.md.

Stdlib only (`unittest`), matching score.py's no-dependency convention. Run with:

  python3 -m unittest discover -s .claude/skills/ywc-toolkit-eval/scripts -p 'test_score.py'
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

# Import the sibling score module regardless of the caller's CWD.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import score  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "score.py"

# A shared, high-overlap description body so two synthetic siblings collide on
# the word-trigram Jaccard threshold (FR6 tests vary only the anti-trigger tail).
SHARED = (
    "Use when reviewing code for type system depth and async correctness and "
    "idiomatic patterns and concurrency safety and error handling and framework "
    "conventions and performance characteristics and review discipline"
)


class A5HeuristicTest(unittest.TestCase):
    """FR3 — A5 model-tier band derives from role keywords in the NAME."""

    def test_expected_tier_from_name(self) -> None:
        self.assertEqual(score.expected_model_tier("ywc-architect"), "opus")
        self.assertEqual(score.expected_model_tier("ywc-root-cause-analyst"), "opus")
        self.assertEqual(score.expected_model_tier("ywc-doc-writer"), "haiku")
        self.assertEqual(score.expected_model_tier("ywc-backend-coder"), "sonnet")
        self.assertEqual(score.expected_model_tier("ywc-security-engineer"), "sonnet")

    def test_bands_for_current_catalog_roles(self) -> None:
        # Well-matched current-catalog pairings all score 5 (Amendment A1).
        self.assertEqual(score.a5_model_band("ywc-architect", "opus"), 5)
        self.assertEqual(score.a5_model_band("ywc-security-engineer", "sonnet"), 5)
        self.assertEqual(score.a5_model_band("ywc-doc-writer", "haiku"), 5)

    def test_bands_discriminate_mismatches(self) -> None:
        # Opus on a mechanical (Haiku-expected) role -> over-provisioned -> 3.
        self.assertEqual(score.a5_model_band("ywc-mechanical-lister", "opus"), 3)
        # Haiku on an architecture (Opus-expected) role -> under-provisioned -> 2.
        self.assertEqual(score.a5_model_band("ywc-architecture-judge", "haiku"), 2)

    def test_no_model_is_zero(self) -> None:
        self.assertEqual(score.a5_model_band("ywc-backend-coder", ""), 0)


class A7RowCountTest(unittest.TestCase):
    """FR4 — A7 counts Rationalization Defense DATA rows (>= 5)."""

    @staticmethod
    def _body(data_rows: int) -> str:
        rows = "\n".join(f"| excuse{i} | reality{i} |" for i in range(data_rows))
        return (
            "# Skill\n\n## Rationalization Defense\n\n"
            "| Excuse | Reality |\n|---|---|\n" + rows + "\n\n## Next Section\n"
        )

    def test_four_rows_fails_gate(self) -> None:
        rows = score._rationalization_data_rows(self._body(4))
        self.assertEqual(rows, 4)
        self.assertFalse(rows >= 5)  # A7 gate (same threshold score_skill applies)

    def test_five_rows_passes_gate(self) -> None:
        rows = score._rationalization_data_rows(self._body(5))
        self.assertEqual(rows, 5)
        self.assertTrue(rows >= 5)  # A7 gate (same threshold score_skill applies)

    def test_absent_section_is_zero(self) -> None:
        self.assertEqual(score._rationalization_data_rows("# Skill\n\nNo defense.\n"), 0)


class CollisionClauseTest(unittest.TestCase):
    """FR6 — collision suppressed only when the sibling is named in a
    'Do not use for' clause, not when merely mentioned cooperatively."""

    def test_excluded_helper(self) -> None:
        self.assertTrue(score._excluded_in_anti_trigger(
            "Use when X. Do not use for Y tasks (use ywc-sibling).", "ywc-sibling"))
        self.assertFalse(score._excluded_in_anti_trigger(
            "Works alongside ywc-sibling during handoff.", "ywc-sibling"))

    def test_collision_suppressed_in_anti_trigger(self) -> None:
        items = [
            {"name": "ywc-aaa-reviewer",
             "description": SHARED + " Do not use for ywc-bbb-reviewer work."},
            {"name": "ywc-bbb-reviewer",
             "description": SHARED + " for the bbb language."},
        ]
        self.assertEqual(score.find_collisions(items), {})

    def test_collision_suppressed_when_anti_trigger_on_other_side(self) -> None:
        # Exercises the right-hand operand of find_collisions' `or`: the
        # anti-trigger names the sibling only in the SECOND item's description.
        items = [
            {"name": "ywc-aaa-reviewer",
             "description": SHARED + " for the aaa language."},
            {"name": "ywc-bbb-reviewer",
             "description": SHARED + " Do not use for ywc-aaa-reviewer work."},
        ]
        self.assertEqual(score.find_collisions(items), {})

    def test_collision_retained_when_only_cooperative(self) -> None:
        items = [
            {"name": "ywc-aaa-reviewer",
             "description": SHARED + " Works alongside ywc-bbb-reviewer in handoff."},
            {"name": "ywc-bbb-reviewer",
             "description": SHARED + " for the bbb language."},
        ]
        out = score.find_collisions(items)
        self.assertIn("ywc-aaa-reviewer", out)
        self.assertIn("ywc-bbb-reviewer", out)


class SiblingPointerTest(unittest.TestCase):
    """FR10 — 'use ywc-<name>' resolves against skill dirs OR agent files.

    The real-resolution cases discover a live agent/skill name at runtime instead
    of hard-coding one, so renaming any single catalog entry cannot flip these
    tests red without an actual FR10 regression.
    """

    @staticmethod
    def _a_real_agent() -> str | None:
        for root in score.AGENT_ROOTS:
            files = sorted((score.REPO_ROOT / root).glob("ywc-*.md"))
            if files:
                return files[0].stem
        return None

    @staticmethod
    def _a_real_skill() -> str | None:
        for root in score.SKILL_ROOTS:
            d = score.REPO_ROOT / root
            if d.is_dir():
                for sk in sorted(d.iterdir()):
                    if (sk / "SKILL.md").exists():
                        return sk.name
        return None

    def test_real_agent_pointer_not_flagged(self) -> None:
        agent = self._a_real_agent()
        if agent is None:
            self.skipTest("no agent catalog present")
        self.assertEqual(
            score._unresolved_sibling_pointers(f"for design, use {agent} here"), [])

    def test_real_skill_pointer_not_flagged(self) -> None:
        skill = self._a_real_skill()
        if skill is None:
            self.skipTest("no skill catalog present")
        self.assertEqual(
            score._unresolved_sibling_pointers(f"to proceed, use {skill} instead"), [])

    def test_unknown_pointer_flagged(self) -> None:
        self.assertEqual(
            score._unresolved_sibling_pointers("use ywc-nonexistent-zzz here"),
            ["ywc-nonexistent-zzz"])


class CiItemGuardTest(unittest.TestCase):
    """FR2 — '--ci' combined with '--item' exits non-zero and writes no baseline."""

    def test_ci_with_item_rejected_and_baseline_untouched(self) -> None:
        baseline = score.HISTORY_MECH
        before = baseline.read_bytes() if baseline.exists() else None
        self.assertIsNotNone(
            before, "committed baseline must exist for the byte-equality check to be load-bearing")
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--ci", "--item", "ywc-commit"],
            capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("cannot be combined", proc.stderr)
        after = baseline.read_bytes() if baseline.exists() else None
        self.assertEqual(before, after)


class FrontmatterAndStructureTest(unittest.TestCase):
    """Guards the three false-positive fixes: quoted-scalar parsing (A2),
    kanji-only Japanese (A4), and flexible anti-trigger phrasing (A3)."""

    def test_double_quoted_scalar_is_unquoted(self) -> None:
        fm = score.parse_yaml_lite(
            'name: ywc-x\ndescription: "(ywc) Use when \\"foo\\" happens. Do not use for bar."')
        self.assertTrue(fm["description"].startswith("(ywc) Use when"))
        self.assertIn('"foo"', fm["description"])  # escaped quotes restored

    def test_single_quoted_scalar_is_unquoted(self) -> None:
        fm = score.parse_yaml_lite("name: ywc-x\ndescription: '(ywc) Use when it''s time'")
        self.assertEqual(fm["description"], "(ywc) Use when it's time")

    def test_folded_scalar_unaffected(self) -> None:
        fm = score.parse_yaml_lite("name: ywc-x\ndescription: >-\n  (ywc) Use when a thing\n  spans lines")
        self.assertEqual(fm["description"], "(ywc) Use when a thing spans lines")

    def test_kanji_only_japanese_counts_for_a4(self) -> None:
        # "자율 실행" (Hangul) + "自律実行" (kanji-only, no kana) is bilingual.
        self.assertTrue(score.HANGUL.search("자율 실행 自律実行"))
        self.assertTrue(score.JAPANESE.search("自律実行"))
        self.assertFalse(score.KANA.search("自律実行"))  # documents why KANA alone failed

    def test_anti_trigger_accepts_during(self) -> None:
        import re
        self.assertTrue(re.search(r"Do not use (?:for|during|when|in)\b",
                                  "Do not use during active feature work, or for X."))


if __name__ == "__main__":
    unittest.main()
