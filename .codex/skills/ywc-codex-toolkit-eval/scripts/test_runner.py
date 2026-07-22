from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from codex_adapter import AdapterResult, FakeAdapter
from runner import run_case


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

    def test_no_provider_is_not_pass(self):
        result = run_case(self.payload(), fixture_root=self.fixtures, repo_root=self.root, adapter=FakeAdapter())
        self.assertEqual("SKIPPED_UNAVAILABLE", result["status"])

    def test_undeclared_write_fails(self):
        result = run_case(self.payload(), fixture_root=self.fixtures, repo_root=self.root, credential_provider="injected_ci_secret", adapter=FakeAdapter(lambda request: (request.workspace / "escape.txt").write_text("x")))
        self.assertEqual("FAIL", result["status"]); self.assertIn("escape.txt", result["diff"])

    def test_declared_write_and_consecutive_attempts_are_isolated(self):
        seen = []
        def write(request):
            seen.append((request.run_id, request.workspace, request.codex_home))
            self.assertFalse((request.workspace / "sentinel").exists())
            (request.workspace / "result.txt").write_text(request.run_id)
        adapter = FakeAdapter(write)
        first = run_case(self.payload(), fixture_root=self.fixtures, repo_root=self.root, adapter=adapter, credential_provider="ephemeral_session_material")
        second = run_case(self.payload(), fixture_root=self.fixtures, repo_root=self.root, adapter=adapter, credential_provider="ephemeral_session_material")
        self.assertEqual("PASS", first["status"]); self.assertEqual("PASS", second["status"])
        self.assertNotEqual(seen[0][0], seen[1][0]); self.assertNotEqual(seen[0][1], seen[1][1]); self.assertNotEqual(seen[0][2], seen[1][2])
        self.assertFalse(seen[0][1].exists()); self.assertFalse(seen[1][2].exists())

    def test_stale_fixture_symlink_is_rejected(self):
        (self.fixtures / "outside").write_text("secret")
        (self.fixtures / "case/input.txt").unlink(); (self.fixtures / "case/input.txt").symlink_to(self.fixtures / "outside")
        result = run_case(self.payload(), fixture_root=self.fixtures, repo_root=self.root, adapter=FakeAdapter(), credential_provider="injected_ci_secret")
        self.assertEqual("FAIL", result["status"])

    def test_timeout_and_output_symlink_fail(self):
        timeout = run_case(self.payload(), fixture_root=self.fixtures, repo_root=self.root, credential_provider="injected_ci_secret", adapter=FakeAdapter(result=AdapterResult("ERROR", error="timeout")))
        self.assertEqual("ERROR", timeout["status"])
        redirect = run_case(self.payload(), fixture_root=self.fixtures, repo_root=self.root, credential_provider="injected_ci_secret", adapter=FakeAdapter(lambda request: (request.workspace / "result.txt").symlink_to(self.fixtures / "outside")))
        self.assertEqual("FAIL", redirect["status"]); self.assertEqual("workspace symlink redirect", redirect["error"])
