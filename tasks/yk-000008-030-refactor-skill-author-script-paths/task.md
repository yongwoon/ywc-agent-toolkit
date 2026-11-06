# yk-000008-030-refactor-skill-author-script-paths — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-skill-author/SKILL.md`
  - `claude-code/skills/ywc-skill-author/references/**`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] `claude-code/skills/ywc-skill-author/SKILL.md` (~line 194): `bash "${CLAUDE_SKILL_DIR}/scripts/audit-skills.sh" ...`.
- [ ] `claude-code/skills/ywc-skill-author/references/audit-workflow.md` (~line 12): `bash "<skill-base-dir>/scripts/audit-skills.sh" ...` plus the defining sentence from `claude-code/skills/CLAUDE.md` Skill-local script paths (b).
- [ ] Sweep `claude-code/skills/*/SKILL.md` and `claude-code/skills/*/references/*.md` for any other `bash scripts/<name>` where `<name>` is a skill-local script (not `scripts/validate.sh` / `scripts/install.sh` at the repo root); fix each in the owning file only if it is listed in Ownership, otherwise list it in Implementation Notes.
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `[ "$(grep -c 'bash scripts/audit-skills.sh' claude-code/skills/ywc-skill-author/SKILL.md claude-code/skills/ywc-skill-author/references/audit-workflow.md | awk -F: '{s+=$2} END{print s}')" = 0 ]`
- [ ] `grep -qF '${CLAUDE_SKILL_DIR}/scripts/audit-skills.sh' claude-code/skills/ywc-skill-author/SKILL.md`
- [ ] `grep -qF '<skill-base-dir>/scripts/audit-skills.sh' claude-code/skills/ywc-skill-author/references/audit-workflow.md`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000008 parallel tasks do NOT commit the baseline file; yk-000008-040 stages it last
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-skill-author/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
- Sweep (`bash +"?scripts/` over `claude-code/skills/*/SKILL.md` and `references/*.md`): the only hits were the two Scope lines in `ywc-skill-author`; both fixed (SKILL.md -> `${CLAUDE_SKILL_DIR}`, audit-workflow.md -> `<skill-base-dir>` plus the defining sentence). No other skill's `bash scripts/<name>` found.
- Not edited (outside Scope, same defect class, prose mentions without `bash`): `ywc-skill-author/SKILL.md` lines ~214 (`scripts/enumerate-rd-rows.sh`), ~227 and ~268 (`scripts/build-variant.sh`, `scripts/enumerate-rd-rows.sh`) still use bare repo-relative skill-local paths; `claude-code/skills/CLAUDE.md` says the rule covers prose too. Candidate for a follow-up.
