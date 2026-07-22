"""Manual-only paired ablation aggregation with conservative retirement evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

VALID_STATUSES = {"PASS", "FAIL", "SKIPPED_UNAVAILABLE", "ERROR", "INCONCLUSIVE"}


@dataclass(frozen=True)
class Trial:
    run_id: str
    arm: str
    case_id: str
    model: str
    cli_version: str | None
    attempt: int
    status: str
    cost: float | None

    def key(self) -> tuple[str, str, str | None, int]:
        return self.case_id, self.model, self.cli_version, self.attempt


def aggregate(trials: Iterable[Trial], *, human_approved: bool) -> dict[str, object]:
    rows = list(trials)
    for trial in rows:
        if trial.arm not in {"with", "without"} or trial.status not in VALID_STATUSES:
            raise ValueError("invalid ablation trial")
        if trial.cost is not None and trial.cost < 0:
            raise ValueError("cost must be non-negative")
    pairs: dict[tuple[str, str, str | None, int], dict[str, Trial]] = {}
    for trial in rows:
        slot = pairs.setdefault(trial.key(), {})
        if trial.arm in slot:
            raise ValueError("duplicate arm for paired trial")
        slot[trial.arm] = trial
    paired = [pair for pair in pairs.values() if set(pair) == {"with", "without"}]
    complete_cost = bool(paired) and all(pair[arm].cost is not None for pair in paired for arm in ("with", "without"))
    additional_without_failures = sum(pair["without"].status != "PASS" and pair["with"].status == "PASS" for pair in paired)
    candidate = len(paired) >= 6 and complete_cost and additional_without_failures <= 1 and human_approved
    return {"decision": "CANDIDATE_FOR_REVIEW" if candidate else "INCONCLUSIVE",
            "paired_trials": len(paired), "complete_cost": complete_cost,
            "additional_without_failures": additional_without_failures,
            "human_approved": human_approved,
            "with_passes": sum(pair["with"].status == "PASS" for pair in paired),
            "without_passes": sum(pair["without"].status == "PASS" for pair in paired)}
