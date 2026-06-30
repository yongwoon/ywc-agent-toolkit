# ywc-codex-toolkit-eval

Local maintenance skill for evaluating this repository's Codex `ywc-*` skills and Codex custom agents. It gathers structural evidence with `inventory_gate.py`, scores deterministic mechanical axes with `score.py`, then uses a 0-4 rubric judgment pass for final grades and a prioritized backlog.

This skill is not distributed. Keep it only under `.codex/skills/ywc-codex-toolkit-eval/`; never package it under `codex/skills/` or `.codex-plugin/skills/`.

## Usage

```bash
$ywc-codex-toolkit-eval --target all
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format markdown
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --ci
```

## Outputs

- `docs/skill-agent-eval/codex/` — Codex evaluation reports
- `docs/skill-agent-eval/codex/scoreboard.md` — rolling scoreboard
- `evals/history.mechanical.json` — reviewed mechanical baseline

## Related Skills

- `ywc-skill-author` — source of Codex skill authoring rules
- `.claude/skills/ywc-toolkit-eval` — separate evaluator for Claude Code skills and agents
