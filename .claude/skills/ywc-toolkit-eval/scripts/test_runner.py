#!/usr/bin/env python3
"""Unit tests for the isolated evaluation runner and the dispatch adapter.

Guards the contracts of 000067-020: workspace isolation (AC5), the status
enum (AC6), and artifact hygiene (AC13).

Scope of the isolation claim, stated plainly because overclaiming it is the
failure mode the spec warns about: this is **best-effort** isolation. The
workspace is a fresh temporary directory per run, which keeps one case's
writes away from the next case and away from the repository. It does **not**
make the run unobservable to the host filesystem, and nothing here should be
read as claiming container- or VM-grade containment. Route N1 gave up catalog
isolation; workspace isolation is what remains, and it is what lets a
file-writing skill be evaluated at all.

Every test uses `FakeAdapter` — the suite must run with no `claude` CLI
present and must never spend money.

Stdlib only (`unittest`), matching score.py's no-dependency convention. Run with:

  python3 .claude/skills/ywc-toolkit-eval/scripts/test_runner.py
"""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

# Import the sibling modules regardless of the caller's CWD.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import claude_adapter  # noqa: E402
import runner  # noqa: E402


def _case(**overrides) -> dict:
    """A minimal well-formed v2 case the runner can execute."""
    case = {
        "schema": 2,
        "id": "runner-sample",
        "prompt": "샘플 프롬프트",
        "language": "ko",
        "category": "happy_path",
        "should_trigger": True,
        "target_skill": "ywc-toolkit-eval",
        "expected_checks": [{"type": "stdout_regex", "pattern": "DONE"}],
    }
    case.update(overrides)
    return case


class WorkspaceLifecycleTest(unittest.TestCase):
    """A run gets its own directory, and the directory goes away afterwards."""

    def test_make_workspace_is_unique_per_run_id(self) -> None:
        made = [runner.make_workspace(runner.new_run_id()) for _ in range(5)]
        try:
            self.assertEqual(len({str(p) for p in made}), 5)
            for path in made:
                self.assertTrue(path.is_dir())
        finally:
            for path in made:
                runner.cleanup(path)

    def test_run_ids_do_not_collide(self) -> None:
        ids = {runner.new_run_id() for _ in range(1000)}
        self.assertEqual(len(ids), 1000)

    def test_cleanup_removes_the_workspace(self) -> None:
        ws = runner.make_workspace(runner.new_run_id())
        (ws / "artifact.txt").write_text("x", encoding="utf-8")
        runner.cleanup(ws)
        self.assertFalse(ws.exists())

    def test_cleanup_can_retain_a_failed_workspace(self) -> None:
        ws = runner.make_workspace(runner.new_run_id())
        try:
            runner.cleanup(ws, keep_on_fail=True, failed=True)
            self.assertTrue(ws.exists(), "failed workspace should be retained")
        finally:
            runner.cleanup(ws)

    def test_successful_workspace_is_removed_even_when_retention_is_on(self) -> None:
        # Retention is for failures only — a passing run leaves nothing behind.
        ws = runner.make_workspace(runner.new_run_id())
        runner.cleanup(ws, keep_on_fail=True, failed=False)
        self.assertFalse(ws.exists())


class SnapshotDiffTest(unittest.TestCase):
    """Undeclared writes are the thing the snapshot exists to catch."""

    def _ws(self) -> Path:
        ws = runner.make_workspace(runner.new_run_id())
        (ws / "declared.txt").write_text("before", encoding="utf-8")
        return ws

    def test_no_change_yields_no_diff(self) -> None:
        ws = self._ws()
        try:
            before = runner.snapshot(ws)
            self.assertEqual(runner.diff_snapshot(before, runner.snapshot(ws), []), [])
        finally:
            runner.cleanup(ws)

    def test_undeclared_addition_is_reported(self) -> None:
        ws = self._ws()
        try:
            before = runner.snapshot(ws)
            (ws / "sneaky.txt").write_text("new", encoding="utf-8")
            diff = runner.diff_snapshot(before, runner.snapshot(ws), [])
            self.assertTrue(any("sneaky.txt" in d for d in diff))
        finally:
            runner.cleanup(ws)

    def test_undeclared_modification_is_reported(self) -> None:
        ws = self._ws()
        try:
            before = runner.snapshot(ws)
            (ws / "declared.txt").write_text("after", encoding="utf-8")
            diff = runner.diff_snapshot(before, runner.snapshot(ws), [])
            self.assertTrue(any("declared.txt" in d for d in diff))
        finally:
            runner.cleanup(ws)

    def test_undeclared_deletion_is_reported(self) -> None:
        ws = self._ws()
        try:
            before = runner.snapshot(ws)
            (ws / "declared.txt").unlink()
            diff = runner.diff_snapshot(before, runner.snapshot(ws), [])
            self.assertTrue(any("declared.txt" in d for d in diff))
        finally:
            runner.cleanup(ws)

    def test_declared_output_path_is_allowed(self) -> None:
        ws = self._ws()
        try:
            before = runner.snapshot(ws)
            (ws / "out.json").write_text("{}", encoding="utf-8")
            diff = runner.diff_snapshot(before, runner.snapshot(ws), ["out.json"])
            self.assertEqual(diff, [])
        finally:
            runner.cleanup(ws)

    def test_declared_nested_output_allows_its_parent_directories(self) -> None:
        ws = self._ws()
        try:
            before = runner.snapshot(ws)
            (ws / "sub").mkdir()
            (ws / "sub" / "out.json").write_text("{}", encoding="utf-8")
            diff = runner.diff_snapshot(
                before, runner.snapshot(ws), ["sub/out.json"])
            self.assertEqual(diff, [])
        finally:
            runner.cleanup(ws)

    def test_allowed_path_does_not_license_a_same_named_file_elsewhere(self) -> None:
        # Declaring `out.json` must not silently permit `sub/out.json` — a
        # different file the case never declared.
        ws = self._ws()
        try:
            before = runner.snapshot(ws)
            (ws / "sub").mkdir()
            (ws / "sub" / "out.json").write_text("{}", encoding="utf-8")
            diff = runner.diff_snapshot(before, runner.snapshot(ws), ["out.json"])
            self.assertTrue(any("sub/out.json" in d for d in diff),
                            f"basename collision slipped through: {diff}")
        finally:
            runner.cleanup(ws)

    def test_symlink_retarget_is_reported(self) -> None:
        ws = self._ws()
        try:
            (ws / "link").symlink_to(ws / "declared.txt")
            before = runner.snapshot(ws)
            (ws / "link").unlink()
            (ws / "other.txt").write_text("o", encoding="utf-8")
            (ws / "link").symlink_to(ws / "other.txt")
            diff = runner.diff_snapshot(before, runner.snapshot(ws), ["other.txt"])
            self.assertTrue(any("link" in d for d in diff),
                            f"symlink retarget not caught: {diff}")
        finally:
            runner.cleanup(ws)

    def test_symlink_escaping_the_workspace_is_reported(self) -> None:
        ws = self._ws()
        try:
            before = runner.snapshot(ws)
            (ws / "escape").symlink_to(Path(os.sep) / "etc" / "passwd")
            diff = runner.diff_snapshot(before, runner.snapshot(ws), [])
            self.assertTrue(any("escape" in d for d in diff))
        finally:
            runner.cleanup(ws)


class RunCaseStatusTest(unittest.TestCase):
    """AC6 — every run returns exactly one status from the enum."""

    def test_passing_case_is_pass(self) -> None:
        adapter = claude_adapter.FakeAdapter(result="DONE — all good")
        record = runner.run_case(_case(), adapter=adapter)
        self.assertEqual(record["status"], "PASS")

    def test_failed_check_is_fail(self) -> None:
        adapter = claude_adapter.FakeAdapter(result="nothing matched here")
        record = runner.run_case(_case(), adapter=adapter)
        self.assertEqual(record["status"], "FAIL")

    def test_adapter_error_is_error(self) -> None:
        adapter = claude_adapter.FakeAdapter(is_error=True, result="boom")
        self.assertEqual(runner.run_case(_case(), adapter=adapter)["status"], "ERROR")

    def test_missing_adapter_is_skipped_unavailable(self) -> None:
        adapter = claude_adapter.FakeAdapter(unavailable=True)
        record = runner.run_case(_case(), adapter=adapter)
        self.assertEqual(record["status"], "SKIPPED_UNAVAILABLE")

    def test_timeout_is_error_and_cleans_up(self) -> None:
        adapter = claude_adapter.FakeAdapter(timeout=True)
        record = runner.run_case(_case(), adapter=adapter)
        self.assertEqual(record["status"], "ERROR")
        self.assertFalse(Path(record["workspace"]).exists(),
                         "timed-out workspace must still be cleaned up")

    def test_invalid_case_is_error_not_a_crash(self) -> None:
        record = runner.run_case(_case(category="bogus"),
                                 adapter=claude_adapter.FakeAdapter(result="DONE"))
        self.assertEqual(record["status"], "ERROR")

    def test_every_status_is_in_the_enum(self) -> None:
        for adapter in (claude_adapter.FakeAdapter(result="DONE"),
                        claude_adapter.FakeAdapter(result="no"),
                        claude_adapter.FakeAdapter(is_error=True),
                        claude_adapter.FakeAdapter(unavailable=True),
                        claude_adapter.FakeAdapter(timeout=True)):
            self.assertIn(runner.run_case(_case(), adapter=adapter)["status"],
                          runner.STATUSES)

    def test_undeclared_write_fails_the_case(self) -> None:
        # The destructive-skill scenario: the dispatch writes somewhere it
        # never declared. Deterministic checks may pass; the case must not.
        adapter = claude_adapter.FakeAdapter(result="DONE", writes={"stray.txt": "x"})
        record = runner.run_case(_case(), adapter=adapter)
        self.assertEqual(record["status"], "FAIL")
        self.assertTrue(any("stray.txt" in c for c in record["undeclared_changes"]))

    def test_parent_escape_write_fails_the_case(self) -> None:
        # The regression that matters most: a dispatch writing `../x` leaves
        # the work directory entirely. Snapshotting only the work directory
        # made this invisible and the case reported PASS.
        adapter = claude_adapter.FakeAdapter(
            result="DONE", writes={"../escaped.txt": "x"})
        record = runner.run_case(_case(), adapter=adapter)
        self.assertEqual(record["status"], "FAIL")
        self.assertTrue(any("escaped.txt" in c for c in record["undeclared_changes"]),
                        f"parent escape not caught: {record['undeclared_changes']}")

    def test_escape_beyond_the_containment_root_is_a_known_best_effort_limit(self) -> None:
        # Documents the boundary rather than overclaiming it. One level up is
        # caught; two levels leaves the watched root and is NOT caught. Only an
        # OS-level sandbox could close this, which route N1 does not have — so
        # the honest grade stays `best-effort`, and this test exists so nobody
        # reads the containment guarantee as total.
        adapter = claude_adapter.FakeAdapter(
            result="DONE", writes={"../../beyond-root.txt": "x"})
        record = runner.run_case(_case(), adapter=adapter)
        self.assertEqual(record["status"], "PASS",
                         "if this now FAILs, containment improved — update the docstring")
        stray = Path(record["workspace"]).parents[1] / "beyond-root.txt"
        stray.unlink(missing_ok=True)

    def test_escaped_write_is_cleaned_up_with_the_run(self) -> None:
        adapter = claude_adapter.FakeAdapter(
            result="DONE", writes={"../escaped.txt": "x"})
        record = runner.run_case(_case(), adapter=adapter)
        root = runner.containment_root(record["workspace"])
        self.assertFalse(root.exists(), "containment root outlived the run")

    def test_declared_output_write_still_passes(self) -> None:
        adapter = claude_adapter.FakeAdapter(result="DONE", writes={"out.json": "{}"})
        record = runner.run_case(_case(output_paths=["out.json"]), adapter=adapter)
        self.assertEqual(record["status"], "PASS", record.get("undeclared_changes"))


class RecordShapeTest(unittest.TestCase):
    """The record is the contract 000068-010 / -020 / 000069-010 consume."""

    def test_record_carries_the_declared_fields(self) -> None:
        record = runner.run_case(_case(), adapter=claude_adapter.FakeAdapter(result="DONE"))
        for field in ("run_id", "case_id", "attempt", "status", "duration_ms",
                      "activation_observability", "undeclared_changes"):
            self.assertIn(field, record)

    def test_activation_observability_is_always_unavailable(self) -> None:
        # Measured, not assumed: the spike found no activation signal in the
        # --output-format json payload, so outcome is the only evidence.
        record = runner.run_case(_case(), adapter=claude_adapter.FakeAdapter(result="DONE"))
        self.assertEqual(record["activation_observability"], "unavailable")

    def test_record_is_json_serializable(self) -> None:
        record = runner.run_case(_case(), adapter=claude_adapter.FakeAdapter(result="DONE"))
        json.loads(json.dumps(record))

    def test_record_redacts_credential_shaped_values(self) -> None:
        leak = "token sk-ant-oat01-AAAABBBBCCCC and ghp_0123456789abcdefghij"
        record = runner.run_case(_case(expected_checks=[{"type": "stdout_regex",
                                                         "pattern": "token"}]),
                                 adapter=claude_adapter.FakeAdapter(result=leak))
        blob = json.dumps(record)
        self.assertNotIn("sk-ant-oat01-AAAABBBBCCCC", blob)
        self.assertNotIn("ghp_0123456789abcdefghij", blob)


class ConsecutiveRunIsolationTest(unittest.TestCase):
    """Best-effort isolation: run N's leftovers are not visible to run N+1."""

    def test_second_run_does_not_see_the_first_runs_workspace(self) -> None:
        first = runner.run_case(
            _case(id="iso-1", output_paths=["out.json"]),
            adapter=claude_adapter.FakeAdapter(result="DONE", writes={"out.json": "1"}))
        second = runner.run_case(
            _case(id="iso-2"),
            adapter=claude_adapter.FakeAdapter(result="DONE"))

        self.assertNotEqual(first["workspace"], second["workspace"])
        self.assertFalse(Path(first["workspace"]).exists())
        self.assertEqual(second["undeclared_changes"], [],
                         "run 2 saw residue from run 1")

    def test_repository_is_untouched_by_a_run(self) -> None:
        repo_root = Path(__file__).resolve().parents[4]
        before = sorted(p.name for p in repo_root.iterdir())
        runner.run_case(_case(), adapter=claude_adapter.FakeAdapter(
            result="DONE", writes={"stray.txt": "x"}))
        self.assertEqual(sorted(p.name for p in repo_root.iterdir()), before)


class AdapterTest(unittest.TestCase):
    """The real adapter builds an argv; it never builds a shell string."""

    def test_dispatch_argv_is_a_list_with_the_slash_invocation(self) -> None:
        argv = claude_adapter.build_argv("ywc-toolkit-eval", "점수 매겨줘")
        self.assertIsInstance(argv, list)
        self.assertEqual(argv[0], "claude")
        self.assertIn("-p", argv)
        self.assertIn("--output-format", argv)
        self.assertIn("json", argv)
        self.assertTrue(any(a.startswith("/ywc-toolkit-eval ") for a in argv))

    def test_disable_skills_only_appears_for_the_without_arm(self) -> None:
        with_arm = claude_adapter.build_argv("s", "p", disable_skills=False)
        without_arm = claude_adapter.build_argv("s", "p", disable_skills=True)
        self.assertNotIn("--disable-slash-commands", with_arm)
        self.assertIn("--disable-slash-commands", without_arm)

    def test_without_arm_uses_the_bare_prompt_not_the_slash_form(self) -> None:
        # --disable-slash-commands turns every skill off, so sending "/name …"
        # would just be an unresolvable string; the arm must send the natural
        # language prompt on its own for the comparison to mean anything.
        without_arm = claude_adapter.build_argv("s", "prompt text", disable_skills=True)
        self.assertIn("prompt text", without_arm)
        self.assertFalse(any(a.startswith("/s ") for a in without_arm))

    def test_prompt_is_never_interpolated_into_a_shell_string(self) -> None:
        hostile = 'p"; touch /tmp/pwned; echo "'
        argv = claude_adapter.build_argv("s", hostile)
        self.assertTrue(any(hostile in a for a in argv),
                        "prompt should travel as one argv element, unescaped")
        self.assertNotIn("sh", [Path(a).name for a in argv])

    def test_cost_estimate_is_reported_before_dispatching(self) -> None:
        estimate = runner.estimate_cost(dispatches=12)
        self.assertAlmostEqual(estimate, 12 * runner.COST_PER_DISPATCH_USD, places=4)


if __name__ == "__main__":
    unittest.main()
