#!/usr/bin/env python3
"""Unit tests for paired with/without ablation and the retirement gate.

Guards the contracts of 000068-020: paired trials (AC10), the retirement
evidence bar and human-approval gate (AC11), fixture survival (AC12), and
mixed-status aggregation (AC18).

Two properties matter most here and both are about refusing to conclude:

* A pair where either arm errored is not evidence. It is dropped, and if
  fewer than the full trial count survive, the whole suite is `INCONCLUSIVE`
  rather than a smaller sample quietly reported as a result.
* Nothing in this module can retire a skill. The strongest verdict reachable
  from data alone is `CANDIDATE_FOR_REVIEW`; retirement requires a human
  approval argument, and the tests assert there is no path around it.

Every test uses `FakeAdapter` — real ablation costs ~$6.50 per case
(6 trials x 2 arms x $0.54), so the suite must never dispatch.

Stdlib only (`unittest`), matching score.py's no-dependency convention. Run with:

  python3 .claude/skills/ywc-toolkit-eval/scripts/test_ablation.py
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ablation  # noqa: E402
import claude_adapter  # noqa: E402


def _case(**overrides) -> dict:
    case = {
        "schema": 2,
        "id": "ablation-sample",
        "prompt": "커밋 메시지를 작성해줘",
        "language": "ko",
        "category": "happy_path",
        "should_trigger": True,
        "target_skill": "ywc-commit",
        "expected_checks": [{"type": "stdout_regex", "pattern": "DONE"}],
    }
    case.update(overrides)
    return case


class ArmAsymmetryTest(unittest.TestCase):
    """The without-arm must be a fair comparison, not a short circuit."""

    def test_with_arm_uses_the_slash_invocation(self) -> None:
        argv = claude_adapter.build_argv("ywc-commit", "커밋해줘", disable_skills=False)
        self.assertTrue(any(a.startswith("/ywc-commit ") for a in argv))

    def test_without_arm_sends_natural_language_not_a_slash_call(self) -> None:
        # Measured in the spike: "/name ..." plus --disable-slash-commands is an
        # unknown command, returns in milliseconds and costs $0. That is not a
        # weaker arm, it is no arm at all — the comparison would be vacuous.
        argv = claude_adapter.build_argv("ywc-commit", "커밋해줘", disable_skills=True)
        self.assertIn("--disable-slash-commands", argv)
        self.assertFalse(any(a.startswith("/ywc-commit ") for a in argv))
        self.assertIn("커밋해줘", argv)

    def test_the_two_arms_actually_dispatch_differently(self) -> None:
        # Asserts the dispatch itself, not the strings the record reports. An
        # earlier version recorded a tidy prompt_without while dispatching both
        # arms with skills enabled — the pass counts looked fine and measured
        # nothing. The manipulation has to be observable at the call boundary.
        adapter = claude_adapter.FakeAdapter(result="DONE")
        ablation.run_pair(_case(), 0, adapter=adapter)
        flags = [call["disable_skills"] for call in adapter.calls]
        self.assertEqual(flags, [False, True],
                         "expected with-arm enabled then without-arm disabled")

    def test_both_arms_send_the_identical_prompt(self) -> None:
        prompt = "동일한 프롬프트"
        pair = ablation.run_pair(_case(prompt=prompt), 0,
                                 adapter=claude_adapter.FakeAdapter(result="DONE"))
        self.assertEqual(pair["prompt_with"], f"/{_case()['target_skill']} {prompt}")
        self.assertEqual(pair["prompt_without"], prompt)


class PairedAggregationTest(unittest.TestCase):
    """AC18 — a pair is evidence only when both arms produced a verdict."""

    def test_six_clean_pairs_are_all_valid(self) -> None:
        suite = ablation.run_suite(
            _case(), adapter=claude_adapter.FakeAdapter(result="DONE"))
        self.assertEqual(suite["trials"], ablation.DEFAULT_TRIALS)
        self.assertEqual(suite["paired_valid"], ablation.DEFAULT_TRIALS)

    def test_errored_pair_is_dropped_not_counted_as_failure(self) -> None:
        suite = ablation.run_suite(_case(),
                                   adapter=claude_adapter.FakeAdapter(result="DONE"),
                                   error_trials={1, 4})
        self.assertEqual(suite["paired_valid"], 4)

    def test_fewer_than_full_pairs_is_inconclusive(self) -> None:
        # The RED case from the task: 2 of 6 pairs error, so the sample is
        # incomplete and must not be reported as a measurement.
        suite = ablation.run_suite(_case(),
                                   adapter=claude_adapter.FakeAdapter(result="DONE"),
                                   error_trials={2, 5})
        self.assertEqual(suite["verdict"], "INCONCLUSIVE")
        self.assertLess(suite["paired_valid"], ablation.DEFAULT_TRIALS)

    def test_unavailable_arm_also_invalidates_the_pair(self) -> None:
        suite = ablation.run_suite(_case(),
                                   adapter=claude_adapter.FakeAdapter(result="DONE"),
                                   unavailable_trials={0})
        self.assertLess(suite["paired_valid"], ablation.DEFAULT_TRIALS)
        self.assertEqual(suite["verdict"], "INCONCLUSIVE")


class RetirementEvidenceTest(unittest.TestCase):
    """AC11 — the evidence bar for even *proposing* retirement."""

    def _verdict(self, with_passes: int, without_passes: int, **over) -> str:
        kwargs = {"paired_valid": ablation.DEFAULT_TRIALS,
                  "trials": ablation.DEFAULT_TRIALS,
                  "cost_usd": 6.48, "loaded_skill_count": 243}
        kwargs.update(over)
        return ablation.classify(with_passes=with_passes,
                                 without_passes=without_passes, **kwargs)

    def test_without_arm_matching_with_arm_is_a_candidate(self) -> None:
        # The skill added nothing measurable, so it is worth a human look.
        self.assertEqual(self._verdict(6, 6), "CANDIDATE_FOR_REVIEW")

    def test_one_extra_failure_without_the_skill_is_still_a_candidate(self) -> None:
        self.assertEqual(self._verdict(6, 5), "CANDIDATE_FOR_REVIEW")

    def test_two_extra_failures_without_the_skill_means_retain(self) -> None:
        # The skill demonstrably helps; nothing to review.
        self.assertEqual(self._verdict(6, 4), "RETAIN")

    def test_missing_cost_evidence_blocks_the_candidate_verdict(self) -> None:
        self.assertEqual(self._verdict(6, 6, cost_usd=None), "INCONCLUSIVE")

    def test_missing_loaded_skill_count_blocks_the_candidate_verdict(self) -> None:
        # AC2": the report must disclose how many skills were loaded, because
        # a sibling could have contributed to the with-arm. Without that
        # disclosure the attribution claim is not supportable.
        self.assertEqual(self._verdict(6, 6, loaded_skill_count=None), "INCONCLUSIVE")

    def test_a_with_arm_that_never_passed_is_inconclusive(self) -> None:
        # 0 vs 0 satisfies the "no worse without it" arithmetic, but it means
        # the case never worked at all. That is a broken fixture, not evidence
        # the skill is redundant, and it must not feed a retirement decision.
        self.assertEqual(self._verdict(0, 0), "INCONCLUSIVE")

    def test_incomplete_pairs_beat_any_pass_pattern(self) -> None:
        self.assertEqual(self._verdict(6, 6, paired_valid=5), "INCONCLUSIVE")


class HumanApprovalGateTest(unittest.TestCase):
    """AC11 / AC12 — code cannot retire a skill, and fixtures survive."""

    def _candidate(self) -> dict:
        return ablation.run_suite(
            _case(), adapter=claude_adapter.FakeAdapter(result="DONE"),
            loaded_skill_count=243)

    def test_suite_alone_never_reports_retired(self) -> None:
        suite = self._candidate()
        self.assertEqual(suite["verdict"], "CANDIDATE_FOR_REVIEW")
        self.assertFalse(suite["retired"])

    def test_retire_requires_explicit_approval(self) -> None:
        suite = self._candidate()
        with self.assertRaises(ablation.ApprovalRequired):
            ablation.retire(suite, approved_by=None)
        with self.assertRaises(ablation.ApprovalRequired):
            ablation.retire(suite, approved_by="   ")

    def test_retire_refuses_a_non_candidate_even_with_approval(self) -> None:
        # Approval is necessary, not sufficient — a human cannot rubber-stamp
        # a verdict the evidence never reached.
        suite = ablation.run_suite(_case(),
                                   adapter=claude_adapter.FakeAdapter(result="DONE"),
                                   error_trials={0}, loaded_skill_count=243)
        self.assertEqual(suite["verdict"], "INCONCLUSIVE")
        with self.assertRaises(ablation.ApprovalRequired):
            ablation.retire(suite, approved_by="yongwoon")

    def test_approved_candidate_retires_and_keeps_the_fixture(self) -> None:
        retired = ablation.retire(self._candidate(), approved_by="yongwoon")
        self.assertTrue(retired["retired"])
        self.assertEqual(retired["approved_by"], "yongwoon")
        # AC12 — the case stays for regression watch, flagged rather than deleted.
        self.assertTrue(retired["fixture_retained"])

    def test_retire_does_not_mutate_the_original_suite(self) -> None:
        suite = self._candidate()
        ablation.retire(suite, approved_by="yongwoon")
        self.assertFalse(suite["retired"])


class CostDisclosureTest(unittest.TestCase):
    """NFR1" — the operator sees the bill before it is incurred."""

    def test_estimate_covers_both_arms_of_every_trial(self) -> None:
        self.assertAlmostEqual(
            ablation.estimate_cost(cases=2, trials=6),
            2 * 6 * 2 * ablation.COST_PER_DISPATCH_USD, places=4)

    def test_one_case_costs_about_six_and_a_half_dollars(self) -> None:
        self.assertAlmostEqual(ablation.estimate_cost(cases=1, trials=6), 6.48, places=2)

    def test_suite_reports_cost_and_loaded_skill_count(self) -> None:
        suite = ablation.run_suite(_case(),
                                   adapter=claude_adapter.FakeAdapter(result="DONE"),
                                   loaded_skill_count=243)
        self.assertGreater(suite["cost_usd"], 0)
        self.assertEqual(suite["loaded_skill_count"], 243)

    def test_report_states_the_attribution_limit(self) -> None:
        report = ablation.format_report(
            ablation.run_suite(_case(),
                               adapter=claude_adapter.FakeAdapter(result="DONE"),
                               loaded_skill_count=243))
        self.assertIn("243", report)
        self.assertIn("CANDIDATE_FOR_REVIEW", report)


if __name__ == "__main__":
    unittest.main()
