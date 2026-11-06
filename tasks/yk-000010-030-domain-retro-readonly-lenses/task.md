# yk-000010-030-domain-retro-readonly-lenses — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-retro/**`
  - `codex/skills/ywc-retro/**`
  - `plugins/ywc-agent-toolkit/skills/ywc-retro/**` (generated)
  - `plugins/ywc-agent-toolkit/README.md` (generated)
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] Read `claude-code/skills/ywc-retro/SKILL.md` Steps 3-4 and the four prompt files first. Lenses need to read the transcript and write one output file; nothing else.
- [ ] Preferred fix (no new agent): dispatch each lens/synthesizer with a tool set limited to read-only tools, or — if the Agent tool cannot restrict tools for `general-purpose` — have each lens return its full output as its final message and let the orchestrator write `<run>/<lens>.md` itself, so the subagent needs no Write/Bash. Pick the option the current Agent tool supports, and record the choice as a Ruling.
- [ ] Do not add a new custom agent unless both options above are impossible; if you must, stop and report first (it changes the agent counts in `CLAUDE.md` and READMEs).
- [ ] Extend `claude-code/skills/ywc-retro/tests/test_retro_safety.py` with a check that SKILL.md no longer dispatches `general-purpose` for the lenses/synthesizer (or that it names the read-only path you chose). RED before the change.
- [ ] Mirror the change in `codex/skills/ywc-retro/` only where the Codex skill has the same dispatch; let the pre-commit hook regenerate `plugins/ywc-agent-toolkit`.
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `python3 claude-code/skills/ywc-retro/tests/test_retro_safety.py`
- [ ] `[ "$(grep -c 'general-purpose' claude-code/skills/ywc-retro/SKILL.md | tr -d ' ')" = 0 ]`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000010 Wave 1 tasks do NOT commit the baseline file; yk-000010-060 stages it last
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-retro/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
