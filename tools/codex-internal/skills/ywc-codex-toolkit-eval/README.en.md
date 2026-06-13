# ywc-codex-toolkit-eval

Internal maintenance skill for evaluating this repository's Codex `ywc-*` skills and Codex custom agents. It gathers structural evidence with `inventory_gate.py`, scores deterministic mechanical axes with `score.py`, then uses a 0-4 rubric judgment pass for final grades and a prioritized backlog.

This skill is not distributed. Keep it only under `tools/codex-internal/skills/ywc-codex-toolkit-eval/`; never package it under `codex/skills/` or `.codex-plugin/skills/`.

## Usage

```bash
$ywc-codex-toolkit-eval --mode full --target all
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --format markdown
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --ci
```

## Outputs

- `docs/skill-agent-eval/codex/reports/` — Codex evaluation reports
- `docs/skill-agent-eval/codex/scoreboard.md` — rolling scoreboard
- `evals/history.mechanical.json` — reviewed mechanical baseline

## Related Skills

- `ywc-skill-author` — source of Codex skill authoring rules
- `.claude/skills/ywc-toolkit-eval` — separate evaluator for Claude Code skills and agents
