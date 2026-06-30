#!/usr/bin/env python3
"""Tests for the Codex mechanical scorer."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("score.py")
AGENT_SMOKE_SCRIPT = Path(__file__).with_name("agent_smoke.py")
EVAL_ROOT = SCRIPT.parent.parent / "evals"


class ScoreScriptTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self._write_skill("ywc-example")
        self._write_agent("ywc-reviewer")

    def _write_skill(self, name: str, *, with_openai_yaml: bool = True) -> None:
        skill = self.repo / "codex" / "skills" / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"""---
name: {name}
description: >-
  Use when evaluating Codex score output. Do not use for Claude Code skill evaluation.
---

# {name}

**Announce at start:** "I'm using {name}."

## Workflow

1. Inspect the Codex skill.
2. Produce a bounded scorecard.

## Output Format

```text
Status: PASS
```

## Validation

- [ ] Scorecard was produced.

## Rationalization Defense

| Excuse | Reality |
|---|---|
| "Structure is enough" | Quality still needs scoring. |
| "No baseline is fine" | Trends need a baseline. |
| "Claude and Codex are the same" | Runtime surfaces differ. |
| "Partial means final" | Judgment axes remain pending. |
| "CI should rewrite history" | CI should compare only. |
""",
            encoding="utf-8",
        )
        for readme in ("README.md", "README.en.md", "README.ja.md", "README.ko.md"):
            (skill / readme).write_text(f"# {name}\n", encoding="utf-8")
        if with_openai_yaml:
            (skill / "agents").mkdir()
            (skill / "agents" / "openai.yaml").write_text(
                'interface:\n  display_name: "Example"\n  short_description: "Example"\n  default_prompt: "Run example."\n',
                encoding="utf-8",
            )

    def _write_agent(self, name: str) -> None:
        agents = self.repo / "codex" / "agents"
        agents.mkdir(parents=True)
        (agents / f"{name}.toml").write_text(
            f'''name = "{name}"
description = "Use for bounded Codex review."
model = "gpt-5.4"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
developer_instructions = """
Mission: Review the supplied packet.
Boundaries: Do not edit files.
Output: Start with Status: <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>.
"""
''',
            encoding="utf-8",
        )

    def _write_agent_smoke_case(
        self,
        *,
        fixture_id: str = "reviewer-happy-path",
        agent: str = "ywc-reviewer",
        output_path: str = "evals/agent-smoke-output/ywc-reviewer/happy.md",
        expected_status: str = "DONE",
        expected_signals: list[str] | None = None,
        forbidden_signals: list[str] | None = None,
        output_text: str | None = None,
    ) -> tuple[Path, Path]:
        evaluator = self.repo / ".codex" / "skills" / "ywc-codex-toolkit-eval"
        fixtures = evaluator / "evals" / "agent-smoke-fixtures.json"
        outputs = evaluator / "evals" / "agent-smoke-output"
        fixtures.parent.mkdir(parents=True)
        signals = expected_signals if expected_signals is not None else ["bounded review"]
        forbidden = forbidden_signals if forbidden_signals is not None else ["edit files"]
        payload = {
            "schema": 1,
            "fixtures": [
                {
                    "id": fixture_id,
                    "agent": agent,
                    "output_path": output_path,
                    "intent": "Validate bounded reviewer behavior.",
                    "evidence_packet": {"summary": "Small static packet."},
                    "expected_status": expected_status,
                    "expected_signals": signals,
                    "forbidden_signals": forbidden,
                }
            ],
        }
        fixtures.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        if output_text is not None:
            output_file = evaluator / output_path
            output_file.parent.mkdir(parents=True)
            output_file.write_text(output_text, encoding="utf-8")
        return fixtures, outputs

    def run_agent_smoke(self, fixtures: Path, outputs: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(AGENT_SMOKE_SCRIPT),
                "--fixtures",
                str(fixtures),
                "--outputs",
                str(outputs),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def run_score(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repo-root", str(self.repo), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def trigger_coverage(self) -> tuple[dict[str, dict[str, int]], list[dict[str, int | str]]]:
        cases = json.loads((EVAL_ROOT / "trigger-cases.json").read_text(encoding="utf-8"))["cases"]
        counts: dict[str, dict[str, int]] = {}
        for case in cases:
            expected = case.get("expected")
            if isinstance(expected, str):
                counts.setdefault(expected, {"positive": 0, "impostor": 0})
                if case.get("kind") == "positive":
                    counts[expected]["positive"] += 1
            impostor = case.get("impostor")
            if isinstance(impostor, str):
                counts.setdefault(impostor, {"positive": 0, "impostor": 0})
                counts[impostor]["impostor"] += 1
        undercovered = [
            {
                "item": item,
                "positive": coverage["positive"],
                "impostor": coverage["impostor"],
            }
            for item, coverage in sorted(counts.items())
            if coverage["positive"] < 3 or coverage["impostor"] < 2
        ]
        return counts, undercovered

    def test_json_marks_judgment_axes_as_partial(self) -> None:
        proc = self.run_score("--target", "all", "--format", "json")

        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        skill = payload["roots"]["codex/skills"][0]
        agent = payload["roots"]["codex/agents"][0]

        self.assertEqual(payload["mode"], "mechanical")
        self.assertIsNone(skill["axes"]["S1"])
        self.assertIsInstance(skill["axes"]["S2"], int)
        self.assertIsNone(agent["axes"]["A1"])
        self.assertIsInstance(agent["axes"]["A2"], int)
        self.assertIsNone(skill["final_total"])
        self.assertGreater(skill["mechanical_points"], 0)

    def test_mode_mechanical_matches_default_shape(self) -> None:
        default_proc = self.run_score("--target", "codex/skills", "--format", "json")
        explicit_proc = self.run_score(
            "--mode", "mechanical", "--target", "codex/skills", "--format", "json"
        )

        self.assertEqual(default_proc.returncode, 0, default_proc.stderr)
        self.assertEqual(explicit_proc.returncode, 0, explicit_proc.stderr)
        default_payload = json.loads(default_proc.stdout)
        explicit_payload = json.loads(explicit_proc.stdout)
        self.assertEqual(default_payload["mode"], "mechanical")
        self.assertEqual(explicit_payload["mode"], "mechanical")
        self.assertEqual(
            [item["path"] for item in default_payload["roots"]["codex/skills"]],
            [item["path"] for item in explicit_payload["roots"]["codex/skills"]],
        )

    def test_unsupported_judge_mode_fails_clearly(self) -> None:
        proc = self.run_score("--mode", "judge", "--target", "codex/skills")

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("score.py only supports --mode mechanical", proc.stderr)
        self.assertIn("judge", proc.stderr)

    def test_missing_item_fails_with_item_and_target(self) -> None:
        proc = self.run_score(
            "--target", "codex/skills", "--item", "no-such-skill", "--format", "markdown"
        )

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("no-such-skill", proc.stderr)
        self.assertIn("codex/skills", proc.stderr)

    def test_targeted_item_returns_one_skill(self) -> None:
        proc = self.run_score(
            "--target", "codex/skills", "--item", "ywc-example", "--format", "json"
        )

        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual([item["name"] for item in payload["roots"]["codex/skills"]], ["ywc-example"])

    def test_trigger_fixture_covers_internal_evaluator(self) -> None:
        counts, undercovered = self.trigger_coverage()
        target = counts["ywc-codex-toolkit-eval"]

        self.assertIsInstance(undercovered, list)
        self.assertGreaterEqual(target["positive"], 3, undercovered)
        self.assertGreaterEqual(target["impostor"], 2, undercovered)

    def test_ci_detects_regression_without_rewriting_history(self) -> None:
        history = self.repo / "history.mechanical.json"
        history.write_text(
            json.dumps(
                {
                    "schema": 1,
                    "items": {
                        "codex/skills/ywc-example": {"S2": 4},
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        skill_dir = self.repo / "codex" / "skills" / "ywc-example"
        (skill_dir / "agents" / "openai.yaml").unlink()
        before = history.read_text(encoding="utf-8")

        proc = self.run_score("--ci", "--history-file", str(history))

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("MECHANICAL REGRESSION", proc.stdout)
        self.assertEqual(history.read_text(encoding="utf-8"), before)

    def test_update_baseline_writes_history(self) -> None:
        history = self.repo / "history.mechanical.json"

        proc = self.run_score("--update-baseline", "--history-file", str(history))

        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(history.read_text(encoding="utf-8"))
        self.assertIn("codex/skills/ywc-example", payload["items"])
        self.assertIn("codex/agents/ywc-reviewer.toml", payload["items"])

    def test_repo_root_can_be_discovered_from_nested_path(self) -> None:
        nested = self.repo / ".codex" / "skills" / "eval" / "scripts"
        nested.mkdir(parents=True)

        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo-root", str(nested), "--format", "json"],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["repo_root"], str(self.repo.resolve()))
        self.assertEqual(len(payload["roots"]["codex/skills"]), 1)

    def test_runtime_fit_does_not_treat_codex_paths_as_slash_commands(self) -> None:
        skill_md = self.repo / "codex" / "skills" / "ywc-example" / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8")
            + "\nRefer to codex/skills/ywc-plan for adjacent planning behavior.\n",
            encoding="utf-8",
        )

        proc = self.run_score("--target", "codex/skills", "--format", "json")

        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        skill = payload["roots"]["codex/skills"][0]
        self.assertEqual(skill["axes"]["S7"], 4)

    def test_agent_output_contract_requires_done_with_concerns(self) -> None:
        agent = self.repo / "codex" / "agents" / "ywc-reviewer.toml"
        agent.write_text(
            agent.read_text(encoding="utf-8").replace("DONE_WITH_CONCERNS | ", ""),
            encoding="utf-8",
        )

        proc = self.run_score("--target", "codex/agents", "--format", "json")

        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        scored_agent = payload["roots"]["codex/agents"][0]
        self.assertLess(scored_agent["axes"]["A6"], 4)

    def test_repo_root_missing_fails_instead_of_scoring_empty_repo(self) -> None:
        empty_dir = tempfile.TemporaryDirectory()
        self.addCleanup(empty_dir.cleanup)
        empty = Path(empty_dir.name)

        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo-root", str(empty), "--format", "json"],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("could not locate repository root", proc.stderr)

    def test_agent_smoke_passes_with_expected_status_and_signals(self) -> None:
        fixtures, outputs = self._write_agent_smoke_case(
            output_text="Fixture: reviewer-happy-path\nStatus: DONE\nbounded review\n"
        )

        proc = self.run_agent_smoke(fixtures, outputs)

        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("PASS reviewer-happy-path", proc.stdout)

    def test_agent_smoke_fails_on_missing_output(self) -> None:
        fixtures, outputs = self._write_agent_smoke_case()

        proc = self.run_agent_smoke(fixtures, outputs)

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("missing output", proc.stdout)

    def test_agent_smoke_fails_on_missing_expected_signal(self) -> None:
        fixtures, outputs = self._write_agent_smoke_case(output_text="Status: DONE\n")

        proc = self.run_agent_smoke(fixtures, outputs)

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("missing expected signal", proc.stdout)

    def test_agent_smoke_fails_on_forbidden_signal(self) -> None:
        fixtures, outputs = self._write_agent_smoke_case(
            output_text="Status: DONE\nbounded review\nedit files\n"
        )

        proc = self.run_agent_smoke(fixtures, outputs)

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("forbidden signal present", proc.stdout)

    def test_agent_smoke_fails_on_unknown_agent(self) -> None:
        fixtures, outputs = self._write_agent_smoke_case(
            agent="no-such-agent",
            output_text="Status: DONE\nbounded review\n",
        )

        proc = self.run_agent_smoke(fixtures, outputs)

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("unknown agent", proc.stdout)

    def test_agent_smoke_fails_on_duplicate_fixture_id(self) -> None:
        fixtures, outputs = self._write_agent_smoke_case(
            output_text="Status: DONE\nbounded review\n"
        )
        payload = json.loads(fixtures.read_text(encoding="utf-8"))
        payload["fixtures"].append(dict(payload["fixtures"][0]))
        fixtures.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        proc = self.run_agent_smoke(fixtures, outputs)

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("duplicate fixture id", proc.stdout)


if __name__ == "__main__":
    unittest.main()
