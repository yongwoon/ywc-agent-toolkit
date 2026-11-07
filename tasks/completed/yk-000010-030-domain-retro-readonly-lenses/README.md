# yk-000010-030-domain-retro-readonly-lenses

## Purpose
`ywc-retro` dispatches its three lenses and the synthesizer as `general-purpose` subagents, which hold Bash/WebFetch/MCP while reading an untrusted session transcript (yk-000005-050 deferred Medium). Confinement is prose-only.

## Scope
- Read `claude-code/skills/ywc-retro/SKILL.md` Steps 3-4 and the four prompt files first. Lenses need to read the transcript and write one output file; nothing else.
- Preferred fix (no new agent): dispatch each lens/synthesizer with a tool set limited to read-only tools, or — if the Agent tool cannot restrict tools for `general-purpose` — have each lens return its full output as its final message and let the orchestrator write `<run>/<lens>.md` itself, so the subagent needs no Write/Bash. Pick the option the current Agent tool supports, and record the choice as a Ruling.
- Do not add a new custom agent unless both options above are impossible; if you must, stop and report first (it changes the agent counts in `CLAUDE.md` and READMEs).
- Extend `claude-code/skills/ywc-retro/tests/test_retro_safety.py` with a check that SKILL.md no longer dispatches `general-purpose` for the lenses/synthesizer (or that it names the read-only path you chose). RED before the change.
- Mirror the change in `codex/skills/ywc-retro/` only where the Codex skill has the same dispatch; let the pre-commit hook regenerate `plugins/ywc-agent-toolkit`.

## Spec Reference

### Primary Sources
- Deferred findings in the Completion Reports of yk-000004..yk-000009 runs on `feature/improvement-20261106` (rulings ledger: yk-000004-020, yk-000005-040, yk-000005-050, yk-000006-010, yk-000009-010).
- `docs/review-learnings.md` (repository review rules)

### Summary
Follow-up items deferred by earlier runs on `feature/improvement-20261106`. Each Scope bullet names the file and the expected end state.

### Out of Scope (from findings)
- Anything not in Scope; other Phase 000010 tasks' items.

## Criticality
critical — secret detection, remote-controlled values reaching shell/gh, or remote branch deletion.

## Dependencies

### Depends On
- (None)

### Depended By
- `yk-000010-060-test-reviewer-trigger-coverage`

## Key Files
- `claude-code/skills/ywc-retro/**`
- `codex/skills/ywc-retro/**`
- `plugins/ywc-agent-toolkit/skills/ywc-retro/**` (generated)
- `plugins/ywc-agent-toolkit/README.md` (generated)

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `claude-code/skills/ywc-retro/**`
- `codex/skills/ywc-retro/**`
- `plugins/ywc-agent-toolkit/skills/ywc-retro/**` (generated)
- `plugins/ywc-agent-toolkit/README.md` (generated)
- `claude-code/agents/ywc-retro-lens.md` (user-approved widening)
- `claude-code/agents/README*.md` (user-approved widening)
- `CLAUDE.md` (agent count only; user-approved widening)
- `README*.md` (root; agent count/list lines only; user-approved widening)

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- `../references/subagent-status-actions.md` §3.5 return directive (read only)

### Conflicts With
- (None)

### Parallelizable After
- (None)

### Task Verify
- `python3 claude-code/skills/ywc-retro/tests/test_retro_safety.py`
- `[ "$(grep -c 'general-purpose' claude-code/skills/ywc-retro/SKILL.md | tr -d ' ')" = 0 ]`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000010 Wave 1 tasks do NOT commit the baseline file; yk-000010-060 stages it last
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-retro/SKILL.md`

## Out of Scope
Anything not listed in Scope. Codex files only where Ownership names them.
