"""RED-first contract tests for the offline evaluator CI boundary."""

from __future__ import annotations

import json
import os
import tempfile
import time
import unittest
from pathlib import Path

from results import ArtifactStore, ResultRecord
from workflow_contract import check_upload_root, live_available, status_exit


class WorkflowContractTest(unittest.TestCase):
    def record(self, run_id: str, status: str) -> ResultRecord:
        return ResultRecord.from_runner_result({"run_id": run_id, "status": status}, profile="mocked", case_id="case", attempt=1, duration_seconds=0, target_skill="demo", dependencies=[])

    def test_status_exit_contract_and_manual_only_inconclusive(self):
        self.assertEqual(0, status_exit("PASS", suite="mocked"))
        self.assertEqual(1, status_exit("FAIL", suite="mocked"))
        self.assertEqual(2, status_exit("ERROR", suite="mocked"))
        self.assertEqual(3, status_exit("SKIPPED_UNAVAILABLE", suite="live"))
        self.assertEqual(2, status_exit("INCONCLUSIVE", suite="mocked"))
        self.assertEqual(0, status_exit("INCONCLUSIVE", suite="ablation", manual_ablation=True))

    def test_live_gate_needs_explicit_provider_and_egress_policy(self):
        self.assertFalse(live_available({}))
        self.assertFalse(live_available({"EVAL_CREDENTIAL_PROVIDER": "configured"}))
        self.assertTrue(live_available({"EVAL_CREDENTIAL_PROVIDER": "configured", "EVAL_API_EGRESS_POLICY": "allow"}))

    def test_cap_and_sensitive_paths_fail_before_upload(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "report.md").write_text("safe")
            check_upload_root(root)
            (root / "secret").mkdir()
            (root / "secret" / "trace.txt").write_text("no")
            with self.assertRaisesRegex(ValueError, "sensitive"):
                check_upload_root(root)
            (root / "secret").rename(root / "removed")
            (root / "report.md").write_text("API_KEY=should-not-upload")
            with self.assertRaisesRegex(ValueError, "secret-like artifact content"):
                check_upload_root(root)
            (root / "report.md").write_text("safe")
            (root / "large.log").write_text("x" * (10 * 1024 * 1024 + 1))
            with self.assertRaisesRegex(ValueError, "10 MB"):
                check_upload_root(root)

    def test_cleanup_only_removes_stale_failed_runs_under_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "runs"; store = ArtifactStore(root)
            for run_id, status in (("old-fail", "FAIL"), ("old-pass", "PASS"), ("new-error", "ERROR")):
                store.write_result(self.record(run_id, status))
            old = time.time() - 8 * 24 * 60 * 60
            os.utime(root / "old-fail", (old, old)); os.utime(root / "old-pass", (old, old))
            self.assertEqual(["old-fail"], store.prune_expired())
            self.assertTrue((root / "old-pass").is_dir())
            self.assertTrue((root / "new-error").is_dir())

    def test_workflow_keeps_pr_path_offline_and_orders_protections_before_upload(self):
        workflow = Path(__file__).parents[4] / ".github/workflows/codex-skill-evals.yml"
        text = workflow.read_text(encoding="utf-8")
        self.assertIn("pull_request:", text)
        self.assertIn("--adapter fake", text)
        self.assertNotIn("--adapter codex", text)
        self.assertLess(text.index("--check-upload-root"), text.index("actions/upload-artifact"))
        self.assertIn("SKIPPED_UNAVAILABLE", text)


if __name__ == "__main__":
    unittest.main()
