import json
import tempfile
import unittest
from pathlib import Path

from ablation import Trial, aggregate
from results import ArtifactStore, ResultRecord, VALID_STATUSES


class ResultsTest(unittest.TestCase):
    def record(self, run_id="run-1", status="PASS"):
        return ResultRecord.from_runner_result({"run_id": run_id, "status": status,
            "final_output": "token=super-secret", "command": ["codex", "exec"],
            "cli_version": "1.0"}, profile="mocked", case_id="case", attempt=1,
            duration_seconds=0.1, target_skill="ywc-plan", dependencies=[])

    def test_record_is_redacted_and_has_only_valid_status(self):
        record = self.record()
        payload = record.to_dict()
        self.assertEqual(payload["status"], "PASS")
        self.assertNotIn("final_output", payload)
        self.assertNotIn("super-secret", json.dumps(payload))
        self.assertEqual(VALID_STATUSES, {"PASS", "FAIL", "SKIPPED_UNAVAILABLE", "ERROR", "INCONCLUSIVE"})

    def test_duplicate_run_id_is_rejected_and_summary_is_atomic(self):
        with tempfile.TemporaryDirectory() as temporary:
            store = ArtifactStore(Path(temporary))
            store.write_result(self.record())
            with self.assertRaises(ValueError):
                store.write_result(self.record())
            self.assertEqual(json.loads((Path(temporary) / "run-1" / "summary.json").read_text())["run_id"], "run-1")

    def test_oversized_failed_workspace_is_not_retained(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"; workspace.mkdir()
            (workspace / "large.log").write_bytes(b"x" * 1025)
            store = ArtifactStore(root / "runs", max_artifact_bytes=1024)
            with self.assertRaises(ValueError):
                store.retain_failed_workspace("run-1", workspace, retain=True)

    def test_retained_artifacts_are_redacted_and_pruned_repeatably(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); workspace = root / "workspace"; workspace.mkdir()
            (workspace / "trace.txt").write_text("API_KEY=abc123\nnormal")
            store = ArtifactStore(root / "runs")
            store.write_result(self.record(status="FAIL"))
            artifact = store.retain_failed_workspace("run-1", workspace, retain=True)
            self.assertNotIn("abc123", (artifact / "trace.txt").read_text())
            self.assertEqual(store.prune_expired(now=10**10), ["run-1"])
            self.assertEqual(store.prune_expired(now=10**10), [])


class AblationTest(unittest.TestCase):
    def trials(self, missing_cost=False):
        rows = []
        for number in range(6):
            common = dict(case_id="case", model="model", cli_version="1", attempt=number, run_id=f"with-{number}")
            rows.append(Trial(arm="with", status="PASS", cost=1.0, **common))
            rows.append(Trial(arm="without", status="PASS", cost=None if missing_cost and number == 0 else 0.5,
                run_id=f"without-{number}", case_id="case", model="model", cli_version="1", attempt=number))
        return rows

    def test_six_complete_pairs_need_human_approval_for_candidate(self):
        self.assertEqual(aggregate(self.trials(), human_approved=False)["decision"], "INCONCLUSIVE")
        self.assertEqual(aggregate(self.trials(), human_approved=True)["decision"], "CANDIDATE_FOR_REVIEW")

    def test_incomplete_cost_is_inconclusive(self):
        self.assertEqual(aggregate(self.trials(missing_cost=True), human_approved=True)["decision"], "INCONCLUSIVE")


if __name__ == "__main__":
    unittest.main()
