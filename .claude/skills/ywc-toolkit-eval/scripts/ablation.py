#!/usr/bin/env python3
"""Paired with/without ablation — the only attribution route N1 supports.

Because route N1 abandoned catalog isolation, every dispatch loads the whole
installed catalog. A single passing run therefore proves nothing about *this*
skill: the outcome could have come from any of the loaded siblings, or from
the base model. The only defensible claim is a difference between two arms:

* **with-arm** — `/<skill> <prompt>`. The explicit call guarantees the target
  skill runs.
* **without-arm** — the *same natural-language prompt* plus
  `--disable-slash-commands`, which turns every skill off.

So what is measured is "do this skill's instructions beat the model's default
behavior", which is exactly the ablation the evaluation guide asks for.

The without-arm must never be built as a slash call. The spike measured it:
`/name ...` with `--disable-slash-commands` is an unknown command that returns
in milliseconds for $0. That is not a weaker arm, it is no arm, and the
comparison silently becomes vacuous.

**Residual limit, disclosed in every report:** a sibling skill can still
contribute during the with-arm. The explicit call reduces that risk but cannot
remove it, so the report records how many skills were loaded and the verdict
refuses to reach `CANDIDATE_FOR_REVIEW` without that number.

Stdlib only, matching score.py's no-dependency convention.

  python3 .claude/skills/ywc-toolkit-eval/scripts/ablation.py --case <id> --suite expensive
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import claude_adapter  # noqa: E402
import runner  # noqa: E402

DEFAULT_TRIALS = 6
COST_PER_DISPATCH_USD = runner.COST_PER_DISPATCH_USD
ARMS_PER_TRIAL = 2

VERDICTS = ("RETAIN", "CANDIDATE_FOR_REVIEW", "INCONCLUSIVE")

# A pair only counts when both arms produced a real verdict. These statuses
# mean the trial did not happen, which is different from having failed.
NON_EVIDENCE_STATUSES = frozenset({"ERROR", "SKIPPED_UNAVAILABLE", "INCONCLUSIVE"})

# AC11: the without-arm may fail at most this much more often than the
# with-arm before the skill counts as demonstrably earning its place.
MAX_EXTRA_FAILURES_FOR_CANDIDATE = 1


class ApprovalRequired(PermissionError):
    """Raised when retirement is attempted without a human approver."""


class _WithoutArm:
    """Adapter proxy that forces `disable_skills=True` on every dispatch.

    `runner.run_case` owns the workspace, snapshotting, and scoring, and it
    calls `adapter.dispatch(...)` without a `disable_skills` argument — it has
    no notion of arms. Rather than reach into the runner (which this task does
    not own), the without-arm wraps its adapter so the flag is applied at the
    only place both arms differ.

    Without this the two arms dispatch identically and every verdict measures
    nothing, while still reporting confident-looking pass counts.
    """

    def __init__(self, inner) -> None:
        self._inner = inner

    def dispatch(self, skill: str, prompt: str, cwd, disable_skills: bool = False,
                 timeout: int = claude_adapter.DEFAULT_TIMEOUT_SECONDS) -> dict:
        return self._inner.dispatch(skill, prompt, cwd, disable_skills=True,
                                    timeout=timeout)


def estimate_cost(cases: int, trials: int = DEFAULT_TRIALS) -> float:
    """Projected spend for a full ablation, both arms of every trial."""
    return cases * trials * ARMS_PER_TRIAL * COST_PER_DISPATCH_USD


def announce_cost(cases: int, trials: int = DEFAULT_TRIALS, stream=sys.stderr) -> None:
    """Print the bill before incurring it, so the operator can abort."""
    dispatches = cases * trials * ARMS_PER_TRIAL
    print(f"[ablation] {cases} case(s) x {trials} trials x {ARMS_PER_TRIAL} arms "
          f"= {dispatches} dispatches - estimated cost: "
          f"${estimate_cost(cases, trials):.2f}", file=stream)
    print("[ablation] this dispatches for real money; Ctrl-C now to abort.",
          file=stream)


def run_pair(case: dict, trial_idx: int, adapter=None,
             force_error: bool = False, force_unavailable: bool = False) -> dict:
    """Run one with/without pair and report whether it counts as evidence."""
    prompt = case.get("prompt", "")
    skill = case.get("target_skill", "")

    with_adapter = adapter
    if force_error:
        with_adapter = claude_adapter.FakeAdapter(is_error=True, result="injected")

    # The without-arm is the same adapter with skills disabled — that flag is
    # the entire experimental manipulation.
    without_adapter = _WithoutArm(
        claude_adapter.FakeAdapter(unavailable=True) if force_unavailable else adapter)

    with_record = runner.run_case(case, adapter=with_adapter, attempt=trial_idx + 1)
    without_record = runner.run_case(case, adapter=without_adapter,
                                     attempt=trial_idx + 1)

    counted = (with_record["status"] not in NON_EVIDENCE_STATUSES
               and without_record["status"] not in NON_EVIDENCE_STATUSES)

    return {
        "trial": trial_idx,
        "prompt_with": f"/{skill} {prompt}",
        "prompt_without": prompt,
        "with_status": with_record["status"],
        "without_status": without_record["status"],
        "counted": counted,
    }


def classify(with_passes: int, without_passes: int, paired_valid: int,
             trials: int, cost_usd: float | None,
             loaded_skill_count: int | None) -> str:
    """Decide the verdict from the aggregated evidence (AC11 / AC18).

    Every guard here fails toward `INCONCLUSIVE`. Proposing a skill for
    retirement on a partial sample, or without the cost and catalog-size
    disclosures that qualify the claim, would be an unsupported conclusion —
    and this verdict is the input to an irreversible decision.
    """
    if paired_valid < trials:
        return "INCONCLUSIVE"
    if cost_usd is None or loaded_skill_count is None:
        return "INCONCLUSIVE"
    if with_passes == 0:
        # The with-arm never passed, so the case never exercised the skill —
        # a broken fixture, not a useless skill. Reporting "the without-arm
        # did just as badly" as retirement evidence would be an artifact of a
        # test that measured nothing.
        return "INCONCLUSIVE"

    extra_failures_without = with_passes - without_passes
    if extra_failures_without <= MAX_EXTRA_FAILURES_FOR_CANDIDATE:
        return "CANDIDATE_FOR_REVIEW"
    return "RETAIN"


def run_suite(case: dict, trials: int = DEFAULT_TRIALS, adapter=None,
              error_trials: set[int] | None = None,
              unavailable_trials: set[int] | None = None,
              loaded_skill_count: int | None = None) -> dict:
    """Run `trials` paired trials for one case and aggregate them.

    `error_trials` / `unavailable_trials` inject failures so the aggregation
    rules can be exercised without dispatching.
    """
    error_trials = error_trials or set()
    unavailable_trials = unavailable_trials or set()

    pairs = [run_pair(case, i, adapter=adapter,
                      force_error=i in error_trials,
                      force_unavailable=i in unavailable_trials)
             for i in range(trials)]

    counted = [p for p in pairs if p["counted"]]
    with_passes = sum(1 for p in counted if p["with_status"] == "PASS")
    without_passes = sum(1 for p in counted if p["without_status"] == "PASS")
    cost = estimate_cost(cases=1, trials=trials)

    return {
        "case_id": case.get("id", "<no id>"),
        "trials": trials,
        "paired_valid": len(counted),
        "with_passes": with_passes,
        "without_passes": without_passes,
        "difference": with_passes - without_passes,
        "verdict": classify(with_passes=with_passes, without_passes=without_passes,
                            paired_valid=len(counted), trials=trials,
                            cost_usd=cost, loaded_skill_count=loaded_skill_count),
        "retired": False,
        "approved_by": None,
        "fixture_retained": True,
        "cost_usd": cost,
        "loaded_skill_count": loaded_skill_count,
        "pairs": pairs,
    }


def retire(suite: dict, approved_by: str | None) -> dict:
    """Mark a reviewed candidate as retired. Requires a named human.

    Two guards, both deliberate. Approval is **necessary**: no data pattern
    retires a skill on its own. Approval is also **not sufficient**: a verdict
    the evidence never reached cannot be rubber-stamped into existence.

    Returns a new record; the input is left untouched so a failed or repeated
    call cannot half-apply.
    """
    if not approved_by or not approved_by.strip():
        raise ApprovalRequired(
            f"retiring {suite.get('case_id')!r} requires a named human approver; "
            "ablation evidence alone never retires a skill (AC11)")
    if suite.get("verdict") != "CANDIDATE_FOR_REVIEW":
        raise ApprovalRequired(
            f"{suite.get('case_id')!r} is {suite.get('verdict')!r}, not "
            "CANDIDATE_FOR_REVIEW; approval cannot substitute for evidence")

    retired = dict(suite)
    retired["retired"] = True
    retired["approved_by"] = approved_by.strip()
    # AC12 — the case survives as a regression watch, flagged not deleted.
    retired["fixture_retained"] = True
    return retired


def format_report(suite: dict) -> str:
    """Human-readable summary, including the limits of what it can claim."""
    loaded = suite.get("loaded_skill_count")
    loaded_text = str(loaded) if loaded is not None else "NOT RECORDED"
    lines = [
        f"# Ablation — {suite['case_id']}",
        "",
        f"- verdict: **{suite['verdict']}**",
        f"- paired trials: {suite['paired_valid']}/{suite['trials']} valid",
        f"- with-arm passes:    {suite['with_passes']}",
        f"- without-arm passes: {suite['without_passes']}",
        f"- difference: {suite['difference']}",
        f"- estimated cost: ${suite['cost_usd']:.2f}",
        f"- skills loaded during the run: {loaded_text}",
        "",
        "## Attribution limit",
        "",
        f"Route N1 does not isolate the catalog, so all {loaded_text} installed "
        "skills were loaded in both arms. The explicit `/name` call guarantees "
        "the target skill ran, but a sibling may still have contributed to the "
        "with-arm result. This report claims only the difference between the "
        "two arms, never that the target skill alone produced the outcome.",
    ]
    if suite["verdict"] == "CANDIDATE_FOR_REVIEW":
        lines += ["", "Retirement requires human approval; this verdict is a "
                      "proposal, not a decision."]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--case", required=True, help="fixture id to ablate")
    parser.add_argument("--suite", choices=("expensive",), required=True,
                        help="explicit opt-in; ablation dispatches for real money")
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    parser.add_argument("--adapter", choices=("claude", "fake"), default="fake")
    parser.add_argument("--loaded-skill-count", type=int, default=None,
                        help="skills loaded during the run; required for a verdict")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)

    case = runner.load_case(args.case)
    if args.adapter == "claude":
        announce_cost(cases=1, trials=args.trials)
        adapter = claude_adapter
    else:
        adapter = claude_adapter.FakeAdapter(result="DONE")

    suite = run_suite(case, trials=args.trials, adapter=adapter,
                      loaded_skill_count=args.loaded_skill_count)
    print(json.dumps(suite, ensure_ascii=False, indent=2)
          if args.format == "json" else format_report(suite))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
