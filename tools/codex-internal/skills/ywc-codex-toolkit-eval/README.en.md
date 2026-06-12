# ywc-codex-toolkit-eval

Internal Codex-only quality evaluation skill for this repository's Codex `ywc-*` skills and Codex custom agents. It scores the catalog on a 0-5 rubric, creates scorecards and improvement backlogs, and drives an evaluate -> improve -> re-evaluate cycle.

This skill is not distributed. Keep it under `tools/codex-internal/skills/ywc-codex-toolkit-eval/`; it must not appear under `codex/skills/` or `.codex-plugin/skills/`.

## Usage

```bash
$ywc-codex-toolkit-eval --mode full --target all
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --format markdown
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --ci
```

## Output

- `evals/scorecard.md` — per Codex skill/agent scores plus a prioritized backlog.
- `evals/history.json` — append-only trend history.

## Related Skills

- `ywc-skill-author` — source of the structural authoring rules.
- `.claude/skills/ywc-toolkit-eval` — separate evaluation skill for Claude Code skills and agents.
