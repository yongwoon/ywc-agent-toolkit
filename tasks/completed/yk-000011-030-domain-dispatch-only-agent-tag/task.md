# yk-000011-030-domain-dispatch-only-agent-tag — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/agents/ywc-go-reviewer.md` (frontmatter only)
  - `claude-code/agents/ywc-python-reviewer.md` (frontmatter only)
  - `claude-code/agents/ywc-typescript-reviewer.md` (frontmatter only)
  - `claude-code/agents/ywc-retro-lens.md` (frontmatter only)
  - `claude-code/agents/CLAUDE.md` (tags row only)
  - `.claude/skills/ywc-toolkit-eval/scripts/score.py`
  - `.claude/skills/ywc-toolkit-eval/scripts/test_score.py`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a spec premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] Implement `docs/ywc-plans/20261107-p1-hardening-before-main-pr.md` **FR-5** exactly: add `tags: [dispatch-only]` to `claude-code/agents/ywc-go-reviewer.md`, `ywc-python-reviewer.md`, `ywc-typescript-reviewer.md`, `ywc-retro-lens.md` (no other agent).
- [ ] Tests first in `.claude/skills/ywc-toolkit-eval/scripts/test_score.py` (RED): every AC6 case (untagged description with the phrase is not exempt; tag with <2 collisions is insufficient; `[dispatch-only-x]`, `[non-dispatch-only]`, `[Dispatch-Only]`, `[dispatch_only]`, `[language-reviewer] # not dispatch-only` not exempt; `[dispatch-only, language-reviewer]`, `["dispatch-only"]` and the block-list form exempt; a block list whose first line is `# dispatch-only (disabled)` not exempt). Rewrite `test_score.py:676-689` to set `tags`.
- [ ] In `.claude/skills/ywc-toolkit-eval/scripts/score.py`: derive dispatch-only from the `tags` value per FR-5; delete `DISPATCH_ONLY_RE`; keep the slash-only rule; update the comment block (~:362-375). No YAML library.
- [ ] Keep `test_shipped_catalog_has_no_unexplained_gap` green with the same 8-item exemption map and the single `ywc-mine-review-history` gap.
- [ ] Document the tag in `claude-code/agents/CLAUDE.md` optional-keys table (`tags` row): `dispatch-only` marks an agent no user-typed prompt can select; it waives only the trigger-coverage positives floor.
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: AC5, AC6 (FR-5)

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `[ "$(grep -l '^tags:.*dispatch-only' claude-code/agents/*.md | wc -l | tr -d ' ')" = 4 ]`
- [ ] `[ "$(grep -c DISPATCH_ONLY_RE .claude/skills/ywc-toolkit-eval/scripts/score.py | tr -d ' ')" = 0 ]`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci 2>&1 | grep -q '1 items below minimum'`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Wave 1 tasks do NOT commit the baseline; yk-000012-010 stages it last

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
