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

    def run_score(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repo-root", str(self.repo), *args],
            text=True,
            capture_output=True,
            check=False,
        )

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
        nested = self.repo / "tools" / "codex-internal" / "skills" / "eval" / "scripts"
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


if __name__ == "__main__":
    unittest.main()
