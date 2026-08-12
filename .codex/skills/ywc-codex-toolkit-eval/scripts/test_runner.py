from __future__ import annotations

import sys
import os
import json
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from codex_adapter import AdapterResult, FakeAdapter
import runner
from runner import run_case
from verifier_registry import VerifierEntry, VerifierMode


class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        (self.root / "codex/skills/demo").mkdir(parents=True)
        (self.root / "codex/skills/demo/SKILL.md").write_text("---\nname: demo\ndescription: demo\n---\n")
        self.fixtures = self.root / "fixtures"; (self.fixtures / "case").mkdir(parents=True)
        (self.fixtures / "case/input.txt").write_text("input")

    def tearDown(self): self.temp.cleanup()

    def payload(self, outputs=None):
        return {"schema": 2, "id": "case", "prompt": "go", "language": "en", "category": "happy_path", "should_trigger": True, "expected_checks": [], "workspace": {"fixture_root": "case", "target_skill": "demo", "skill_dependencies": [], "fixture_files": ["input.txt"], "output_paths": outputs or ["result.txt"], "evidence_packet": {}, "verifier_ids": []}}

    def run_live(self, payload, adapter):
        return run_case(payload, fixture_root=self.fixtures, repo_root=self.root, adapter=adapter,
                        credential_provider="injected_ci_secret", credential_material=("CODEX_API_KEY", "test-only-secret"))

    def test_no_provider_is_not_pass(self):
        result = run_case(self.payload(), fixture_root=self.fixtures, repo_root=self.root, adapter=FakeAdapter())
        self.assertEqual("SKIPPED_UNAVAILABLE", result["status"])

    def test_undeclared_write_fails(self):
        result = self.run_live(self.payload(), FakeAdapter(lambda request: (request.workspace / "escape.txt").write_text("x")))
        self.assertEqual("FAIL", result["status"]); self.assertIn("escape.txt", result["diff"])

    def test_declared_write_and_consecutive_attempts_are_isolated(self):
        seen = []
        def write(request):
            seen.append((request.run_id, request.workspace, request.codex_home))
            self.assertFalse((request.workspace / "sentinel").exists())
            (request.workspace / "result.txt").write_text(request.run_id)
        adapter = FakeAdapter(write)
        first = self.run_live(self.payload(), adapter)
        second = self.run_live(self.payload(), adapter)
        self.assertEqual("PASS", first["status"]); self.assertEqual("PASS", second["status"])
        self.assertNotEqual(seen[0][0], seen[1][0]); self.assertNotEqual(seen[0][1], seen[1][1]); self.assertNotEqual(seen[0][2], seen[1][2])
        self.assertFalse(seen[0][1].exists()); self.assertFalse(seen[1][2].exists())

    def test_stale_fixture_symlink_is_rejected(self):
        (self.fixtures / "outside").write_text("secret")
        (self.fixtures / "case/input.txt").unlink(); (self.fixtures / "case/input.txt").symlink_to(self.fixtures / "outside")
        result = self.run_live(self.payload(), FakeAdapter())
        self.assertEqual("FAIL", result["status"])

    def test_timeout_and_output_symlink_fail(self):
        timeout = self.run_live(self.payload(), FakeAdapter(result=AdapterResult("ERROR", error="timeout")))
        self.assertEqual("ERROR", timeout["status"])
        redirect = self.run_live(self.payload(), FakeAdapter(lambda request: (request.workspace / "result.txt").symlink_to(self.fixtures / "outside")))
        self.assertEqual("FAIL", redirect["status"]); self.assertEqual("workspace symlink redirect", redirect["error"])

    def test_credential_is_ephemeral_and_not_label_only(self):
        adapter = FakeAdapter()
        result = self.run_live(self.payload(), adapter)
        self.assertEqual("PASS", result["status"])
        self.assertEqual({"CODEX_API_KEY": "test-only-secret"}, dict(adapter.requests[0].credential_environment))
        missing = run_case(self.payload(), fixture_root=self.fixtures, repo_root=self.root, adapter=FakeAdapter(), credential_provider="injected_ci_secret")
        self.assertEqual("ERROR", missing["status"]); self.assertNotIn("test-only-secret", str(missing))

    def test_readonly_verifier_detects_unlisted_source_mutation(self):
        self.payload()["workspace"]["verifier_ids"]
        payload = self.payload(); payload["workspace"]["verifier_ids"] = ["bundle.validate"]
        original = runner.get_verifier
        runner.get_verifier = lambda _: VerifierEntry("bundle.validate", VerifierMode.SOURCE_CHECKOUT_READONLY, ("python3", "-c", "from pathlib import Path; Path('unlisted.txt').write_text('changed')"), ".", 10, (), 0)
        try:
            result = self.run_live(payload, FakeAdapter())
        finally:
            runner.get_verifier = original
        self.assertEqual("FAIL", result["status"]); self.assertEqual("readonly verifier mutated source checkout", result["error"])

    def test_content_snapshot_detects_restored_metadata(self):
        input_path = self.fixtures / "case/input.txt"; original = input_path.stat()
        def rewrite(request):
            path = request.workspace / "input.txt"; path.write_text("other"); os.utime(path, ns=(original.st_atime_ns, original.st_mtime_ns))
        result = self.run_live(self.payload(), FakeAdapter(rewrite))
        self.assertEqual("FAIL", result["status"]); self.assertIn("input.txt", result["diff"])

    def test_expected_checks_are_enforced(self):
        def write(request):
            (request.workspace / "result.json").write_text('{"status":"DONE"}')
        payload = self.payload(outputs=["result.json"])
        payload["expected_checks"] = [
            {"type": "file_exists", "path": "result.json"},
            {"type": "json_path_equals", "path": "result.json", "json_path": "$.status", "expected_value": "DONE"},
        ]
        result = self.run_live(payload, FakeAdapter(write))
        self.assertEqual("PASS", result["status"])
        payload["expected_checks"][1]["expected_value"] = "BLOCKED"
        result = self.run_live(payload, FakeAdapter(write))
        self.assertEqual("FAIL", result["status"])
        self.assertIn("json_path_equals", result["error"])

    def test_architecture_fixture_manifests_validate_in_isolation(self):
        fixture_root = Path(__file__).parents[1] / "evals" / "fixtures"
        repo_root = Path(__file__).parents[4]
        def write_evidence(request):
            evidence = {
                "Validate": "evidence/validation.json",
                "Reject": "evidence/rejection.json",
                "With": "evidence/fallback.json",
            }[request.prompt.split(" ")[0]]
            source = json.loads((request.workspace / "input.json").read_text(encoding="utf-8"))
            manifest = request.workspace / "architecture-invariants.json"
            if manifest.exists():
                contract = json.loads(manifest.read_text(encoding="utf-8"))
                status = "NEEDS_CONTEXT" if "verifier" in contract or not contract.get("components") else "DONE"
            else:
                status = source["expected"]
            path = request.workspace / evidence
            path.parent.mkdir()
            path.write_text(json.dumps({"status": status}, ensure_ascii=False))
        original_verifiers = runner._run_verifiers
        runner._run_verifiers = lambda *_args: None
        try:
            for relative in ("ywc-architecture-invariants/valid/fixture.json", "ywc-architecture-invariants/unsafe/fixture.json", "ywc-architecture-invariants/no-manifest/fixture.json"):
                payload = json.loads((fixture_root / relative).read_text(encoding="utf-8"))
                result = run_case(payload, fixture_root=fixture_root, repo_root=repo_root, adapter=FakeAdapter(write_evidence), credential_provider="injected_ci_secret", credential_material=("CODEX_API_KEY", "test-only-secret"))
                self.assertEqual("PASS", result["status"], f"{relative}: {result}")
        finally:
            runner._run_verifiers = original_verifiers


if __name__ == "__main__":
    unittest.main()
