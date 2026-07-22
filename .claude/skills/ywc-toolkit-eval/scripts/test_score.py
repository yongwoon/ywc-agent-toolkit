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


class A3ToolBandTest(unittest.TestCase):
    """A3 — a bounded mutating grant on an implementer role is minimal-for-role."""

    def test_star_grant_is_one_any_role(self) -> None:
        self.assertEqual(score.a3_tool_band("*", False), 1)
        self.assertEqual(score.a3_tool_band("*", True), 1)

    def test_readonly_role_holding_mutating_is_three(self) -> None:
        self.assertEqual(score.a3_tool_band("Read, Grep, Edit", True), 3)

    def test_readonly_role_without_mutating_is_five(self) -> None:
        self.assertEqual(score.a3_tool_band("Read, Grep, Glob, WebFetch", True), 5)

    def test_implementer_bounded_mutating_is_five(self) -> None:
        # a coder legitimately needs Write/Edit/Bash — minimal-for-role, not an
        # over-grant, so it must not be capped at 4 the way it once was.
        self.assertEqual(
            score.a3_tool_band("Read, Write, Edit, Bash, Grep, Glob", False), 5)


class S5LocaleTest(unittest.TestCase):
    """S5 — es/zh are optional; their absence must not deduct."""

    def _mk_skill(self, tmp: str, locales: tuple) -> Path:
        d = Path(tmp) / "ywc-sample"
        d.mkdir()
        (d / "SKILL.md").write_text(
            "---\nname: ywc-sample\n"
            "description: (ywc) Use when sampling. Do not use for others. 한국어 日本語\n"
            "---\n\n**Announce at start:** x\n\nbody\n", encoding="utf-8")
        for loc in locales:
            (d / loc).write_text("content", encoding="utf-8")
        return d

    def test_missing_es_zh_is_still_five(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            d = self._mk_skill(tmp, tuple(score.REQUIRED_LOCALES))
            r = score.score_skill(d, {}, {})
            self.assertEqual(r["axes"]["S5"], 5)
            self.assertEqual(r["signals"]["missing_optional_locales"],
                             ["README.es.md", "README.zh.md"])

    def test_missing_required_locale_is_zero(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            d = self._mk_skill(tmp, ("README.md", "README.en.md", "README.ja.md"))
            r = score.score_skill(d, {}, {})
            self.assertEqual(r["axes"]["S5"], 0)


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


class ReadonlyRoleTest(unittest.TestCase):
    """A3 — an implementer that mentions reviewing must not be scored read-only."""

    @staticmethod
    def _readonly(name: str, role_text: str) -> bool:
        """Mirror score_agent()'s classification on an isolated role statement."""
        import re
        head = re.split(r"—|--", role_text)[0]
        return bool(
            (score.READONLY_HINT.search(name) or score.READONLY_HINT.search(role_text))
            and not score.IMPL_ROLE_HINT.search(head)
        )

    def test_implementer_mentioning_review_is_not_readonly(self) -> None:
        """The ywc-cloud-engineer regression: authors Terraform, reviews its own change."""
        role = ("Use when implementing or modifying Infrastructure-as-Code — Terraform "
                "modules and resources, including terraform plan verification and a "
                "reliability-lens review of the change. ")
        self.assertFalse(self._readonly("ywc-cloud-engineer", role))
        self.assertEqual(score.a3_tool_band("Read, Write, Edit, Bash", False), 5)

    def test_genuine_reviewer_stays_readonly(self) -> None:
        role = "Use when reviewing Go code for goroutine lifecycle — leak detection. "
        self.assertTrue(self._readonly("ywc-go-reviewer", role))

    def test_readonly_holding_mutating_tool_is_still_banded_three(self) -> None:
        """The veto must not disarm the real least-privilege check."""
        self.assertEqual(score.a3_tool_band("Read, Grep, Write", True), 3)

    def test_veto_reads_only_the_opening_clause(self) -> None:
        """A negation or routing note after the em-dash must not clear a reviewer.

        Mirrors ywc-performance-engineer, whose role statement declares itself
        read-only and then mentions writing verbs only to route them elsewhere.
        """
        role = ("Use when analyzing performance characteristics — read-only; the agent "
                "recommends but does NOT execute the fix; fixes go to ywc-backend-coder. ")
        self.assertTrue(self._readonly("ywc-performance-engineer", role))


class ProseLintTest(unittest.TestCase):
    """Prose lint — advisory signal only; must never move an axis."""

    def test_noop_and_nondirective_are_flagged(self) -> None:
        r = score._prose_lint(
            "Always write clean code.\n"
            "Follow best practices.\n"
            "가독성 좋게 작성해라.\n"
            "This is recommended.\n")
        self.assertEqual([h["line"] for h in r["noop_lines"]], [1, 2, 3])
        self.assertEqual([h["line"] for h in r["nondirective_lines"]], [4])

    def test_concrete_anchor_is_not_flagged(self) -> None:
        """A phrase carrying a real anchor is actionable, not an empty exhortation."""
        r = score._prose_lint(
            "Using `ripgrep` is recommended.\n"          # backtick identifier
            "Reading src/main.py is recommended.\n"      # path
            "Read the file; this is recommended.\n")     # tool name
        self.assertEqual(r["noop_lines"], [])
        self.assertEqual(r["nondirective_lines"], [])

    def test_quoting_contexts_are_not_flagged(self) -> None:
        """Rationalization Defense rows quote excuses verbatim — must not fire."""
        r = score._prose_lint(
            "# Follow best practices\n"                  # heading
            "| excuse | write clean code |\n"            # table row
            "> quoted: follow best practices\n"          # blockquote
            "```\n"
            "write clean code\n"                         # fenced code
            "```\n")
        self.assertEqual(r["noop_lines"], [])
        self.assertEqual(r["nondirective_lines"], [])

    def test_line_numbers_are_file_based(self) -> None:
        text = "---\nname: ywc-x\n---\n\nAlways write clean code.\n"
        _, body = score.split_frontmatter(text)
        r = score._prose_lint(body, score._body_line_offset(text, body))
        self.assertEqual(r["noop_lines"][0]["line"], 5)
        self.assertEqual(text.splitlines()[4], "Always write clean code.")

    def test_prose_lint_never_moves_an_axis(self) -> None:
        """Poisoning the lint output must leave every axis byte-identical."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "ywc-sample"
            d.mkdir()
            (d / "SKILL.md").write_text(
                "---\nname: ywc-sample\n"
                "description: (ywc) Use when sampling. Do not use for others. 한국어 日本語\n"
                "---\n\n**Announce at start:** x\n\nAlways write clean code.\n",
                encoding="utf-8")
            for loc in score.REQUIRED_LOCALES:
                (d / loc).write_text("content", encoding="utf-8")

            baseline = score.score_skill(d, {}, {})["axes"]
            original = score._prose_lint
            try:
                score._prose_lint = lambda *a, **k: {
                    "noop_lines": [{"line": 1, "text": "x", "phrase": "y"}] * 99,
                    "nondirective_lines": [{"line": 2, "text": "z", "phrase": "w"}] * 99,
                }
                poisoned = score.score_skill(d, {}, {})
            finally:
                score._prose_lint = original

            self.assertEqual(poisoned["axes"], baseline)
            self.assertEqual(len(poisoned["signals"]["prose_lint"]["noop_lines"]), 99)


SKILL_WEIGHTS = {"S1": 30, "S2": 15, "S3": 20, "S4": 10, "S5": 15, "S6": 10}


class S3ReliabilityBandTest(unittest.TestCase):
    """S3 becomes an observed reliability, not a reading of the body."""

    def test_perfect_reliability_is_five(self) -> None:
        self.assertEqual(score.reliability_band(6, 6), 5)

    def test_total_failure_is_zero(self) -> None:
        self.assertEqual(score.reliability_band(0, 6), 0)

    def test_bands_are_monotonic_in_passes(self) -> None:
        bands = [score.reliability_band(p, 6) for p in range(7)]
        self.assertEqual(bands, sorted(bands))

    def test_zero_trials_is_unmeasured_not_zero(self) -> None:
        # No evidence and evidence-of-failure are different findings; collapsing
        # them would let a missing fixture read as a broken skill.
        self.assertEqual(score.reliability_band(0, 0), score.UNMEASURED)

    def test_band_four_is_unreachable_at_six_trials(self) -> None:
        # AC9 wants the unreachable bands named rather than assumed away.
        # 5/6 = 0.833 falls to band 3 and 6/6 = 1.0 jumps to band 5.
        self.assertEqual(score.unreachable_bands(6), [4])

    def test_more_trials_close_the_gap(self) -> None:
        self.assertEqual(score.unreachable_bands(10), [])


class HistoryRowHonestyTest(unittest.TestCase):
    """An unmeasured axis must not be laundered into a smaller total."""

    def _measured(self, **over) -> dict:
        axes = {"S1": 5, "S2": 5, "S3": 4, "S4": 5, "S5": 5, "S6": 4}
        axes.update(over)
        return axes

    def test_measured_item_gets_a_total(self) -> None:
        self.assertEqual(score.item_total(self._measured(), SKILL_WEIGHTS), 94)

    def test_unmeasured_axis_yields_no_total(self) -> None:
        self.assertIsNone(
            score.item_total(self._measured(S3=score.UNMEASURED), SKILL_WEIGHTS))

    def test_skipped_judgment_axis_also_yields_no_total(self) -> None:
        self.assertIsNone(score.item_total(self._measured(S3=None), SKILL_WEIGHTS))

    def test_unmeasured_axes_are_named(self) -> None:
        axes = self._measured(S1=score.UNMEASURED, S3=None)
        self.assertEqual(score.unmeasured_axes(axes), ["S1", "S3"])

    def test_unmeasured_item_is_null_and_excluded_from_statistics(self) -> None:
        row = score.build_history_row({
            "ywc-sample-a": {"axes": self._measured(), "s3_source": "runner"},
            "ywc-sample-b": {"axes": self._measured(S3=score.UNMEASURED)},
        }, SKILL_WEIGHTS)

        self.assertIsNone(row["items"]["ywc-sample-b"])
        self.assertEqual(row["unmeasured"], ["ywc-sample-b"])
        self.assertEqual(row["count"], 2)
        self.assertEqual(row["measured"], 1)
        # The mean is over measured items only — averaging in a null, or
        # treating it as zero, would both misreport the catalog.
        self.assertEqual(row["mean_total"], 94.0)

    def test_below_threshold_ignores_unmeasured_items(self) -> None:
        row = score.build_history_row({
            "weak": {"axes": {"S1": 2, "S2": 2, "S3": 2, "S4": 2, "S5": 2, "S6": 2}},
            "unknown": {"axes": self._measured(S3=score.UNMEASURED)},
        }, SKILL_WEIGHTS)
        self.assertEqual(row["below_threshold"], 1)

    def test_all_unmeasured_reports_no_mean_rather_than_zero(self) -> None:
        row = score.build_history_row({
            "a": {"axes": self._measured(S3=score.UNMEASURED)},
        }, SKILL_WEIGHTS)
        self.assertIsNone(row["mean_total"])
        self.assertEqual(row["below_threshold"], 0)

    def test_s3_source_is_recorded_and_validated(self) -> None:
        # A 4 measured by the runner and a 4 inferred from reading the body are
        # different claims; the row has to say which one it is.
        row = score.build_history_row({
            "a": {"axes": self._measured(), "s3_source": "runner"},
            "b": {"axes": self._measured(), "s3_source": "read-only"},
        }, SKILL_WEIGHTS)
        self.assertEqual(row["s3_source"], {"a": "runner", "b": "read-only"})

        with self.assertRaises(ValueError):
            score.build_history_row(
                {"c": {"axes": self._measured(), "s3_source": "vibes"}}, SKILL_WEIGHTS)


class S3DoesNotReachTheCiBaselineTest(unittest.TestCase):
    """AC7 — the CI gate stays a pure function of the mechanical tier."""

    def test_axes_s3_is_none_for_every_skill(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "ywc-sample"
            d.mkdir()
            (d / "SKILL.md").write_text(
                "---\nname: ywc-sample\n"
                "description: (ywc) Use when sampling. Do not use for others. 한국어 日本語\n"
                "---\n\n**Announce at start:** x\n", encoding="utf-8")
            for loc in score.REQUIRED_LOCALES:
                (d / loc).write_text("content", encoding="utf-8")
            self.assertIsNone(score.score_skill(d, {}, {})["axes"]["S3"])

    def test_judgment_axes_never_enter_the_real_baseline(self) -> None:
        # The invariant that actually protects `--ci`: judgment axes stay
        # `None` in `score_skill`, so `flatten_mech` never stores them and the
        # baseline cannot move with an LLM's mood.
        #
        # Note what this does NOT claim: `flatten_mech` filters `None` only, so
        # it would happily store a *number* someone wired into `axes.S3`. The
        # guarantee lives upstream, which is why the assertion is made against
        # real scored output rather than a hand-built dict.
        baseline = score.flatten_mech(score.evaluate(".claude/skills"))
        self.assertTrue(baseline, "no items scored — the assertion would be vacuous")
        for key, axes in baseline.items():
            for judgment_axis in ("S3", "S6"):
                self.assertNotIn(judgment_axis, axes,
                                 f"{key}: {judgment_axis} reached the CI baseline")

    def test_runner_reliability_is_not_wired_into_axes(self) -> None:
        # reliability_band() produces real S3 values, and they must stay out of
        # the mechanical result entirely — scorecard and backlog only.
        import tempfile
        self.assertEqual(score.reliability_band(6, 6), 5)
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "ywc-sample"
            d.mkdir()
            (d / "SKILL.md").write_text(
                "---\nname: ywc-sample\n"
                "description: (ywc) Use when sampling. Do not use for others. 한국어 日本語\n"
                "---\n\n**Announce at start:** x\n", encoding="utf-8")
            for loc in score.REQUIRED_LOCALES:
                (d / loc).write_text("content", encoding="utf-8")
            flat = score.flatten_mech({"r": [score.score_skill(d, {}, {})]})
            self.assertNotIn("S3", next(iter(flat.values())))


if __name__ == "__main__":
    unittest.main()
