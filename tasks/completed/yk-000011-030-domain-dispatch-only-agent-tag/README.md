# yk-000011-030-domain-dispatch-only-agent-tag

## Purpose
Replace the prose regex `DISPATCH_ONLY_RE` in the trigger-coverage exemption with an explicit `tags: [dispatch-only]` frontmatter marker on the four dispatch-only Claude Code agents.

## Scope
- Implement `docs/ywc-plans/20261107-p1-hardening-before-main-pr.md` **FR-5** exactly: add `tags: [dispatch-only]` to `claude-code/agents/ywc-go-reviewer.md`, `ywc-python-reviewer.md`, `ywc-typescript-reviewer.md`, `ywc-retro-lens.md` (no other agent).
- Tests first in `.claude/skills/ywc-toolkit-eval/scripts/test_score.py` (RED): every AC6 case (untagged description with the phrase is not exempt; tag with <2 collisions is insufficient; `[dispatch-only-x]`, `[non-dispatch-only]`, `[Dispatch-Only]`, `[dispatch_only]`, `[language-reviewer] # not dispatch-only` not exempt; `[dispatch-only, language-reviewer]`, `["dispatch-only"]` and the block-list form exempt; a block list whose first line is `# dispatch-only (disabled)` not exempt). Rewrite `test_score.py:676-689` to set `tags`.
- In `.claude/skills/ywc-toolkit-eval/scripts/score.py`: derive dispatch-only from the `tags` value per FR-5; delete `DISPATCH_ONLY_RE`; keep the slash-only rule; update the comment block (~:362-375). No YAML library.
- Keep `test_shipped_catalog_has_no_unexplained_gap` green with the same 8-item exemption map and the single `ywc-mine-review-history` gap.
- Document the tag in `claude-code/agents/CLAUDE.md` optional-keys table (`tags` row): `dispatch-only` marks an agent no user-typed prompt can select; it waives only the trigger-coverage positives floor.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261107-p1-hardening-before-main-pr.md` — FR-5 (normative), AC5, AC6, Existing Constraints Touched, Failure Modes
- `docs/ywc-plans/20261107-p1-hardening-before-main-pr.review-5.md` — residual Warnings folded into Scope
- `docs/review-learnings.md`

### Summary
Spec FR-5 defines the exact token rule (cut at the first comment `#`, split on brackets/commas/whitespace, strip quotes, exact case-sensitive `dispatch-only`), and AC6 lists the positive and negative tag forms the tests must cover.

### Out of Scope (from spec)
- P2-a (hook enforcement), P2-b (scan-secrets residual gaps), P2-c (real prompts for `ywc-mine-review-history`), P2-d (Codex `ywc-worktrees` C2 form); porting `wait-dependabot-rebase.sh`; the release gate (FR-6, post-run step).

## Criticality
normal — Spec Critical Surfaces marks T3 (eval scorer and agent tags) `normal`.

## Dependencies

### Depends On
- (None)

### Depended By
- (None — the post-run release gate (FR-6) runs after all P1 tasks)

## Key Files
- `claude-code/agents/ywc-go-reviewer.md` (frontmatter only)
- `claude-code/agents/ywc-python-reviewer.md` (frontmatter only)
- `claude-code/agents/ywc-typescript-reviewer.md` (frontmatter only)
- `claude-code/agents/ywc-retro-lens.md` (frontmatter only)
- `claude-code/agents/CLAUDE.md` (tags row only)
- `.claude/skills/ywc-toolkit-eval/scripts/score.py`
- `.claude/skills/ywc-toolkit-eval/scripts/test_score.py`

## Notes
- Line numbers come from the spec; re-locate each before editing. If a premise no longer matches the file, stop and report.

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default

### Ownership
- `claude-code/agents/ywc-go-reviewer.md` (frontmatter only)
- `claude-code/agents/ywc-python-reviewer.md` (frontmatter only)
- `claude-code/agents/ywc-typescript-reviewer.md` (frontmatter only)
- `claude-code/agents/ywc-retro-lens.md` (frontmatter only)
- `claude-code/agents/CLAUDE.md` (tags row only)
- `.claude/skills/ywc-toolkit-eval/scripts/score.py`
- `.claude/skills/ywc-toolkit-eval/scripts/test_score.py`

### Owned Interface
- `apply_coverage_exemption(cov, fm)` — dispatch-only now derived from `fm['tags']`

### Shared Surfaces
- `score.py --ci` coverage report format (unchanged)

### Conflicts With
- (None identified)

### Parallelizable After
- (None)

### Task Verify
- `[ "$(grep -l '^tags:.*dispatch-only' claude-code/agents/*.md | wc -l | tr -d ' ')" = 4 ]`
- `[ "$(grep -c DISPATCH_ONLY_RE .claude/skills/ywc-toolkit-eval/scripts/score.py | tr -d ' ')" = 0 ]`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci 2>&1 | grep -q '1 items below minimum'`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Wave 1 tasks do NOT commit the baseline; yk-000012-010 stages it last

## Out of Scope
Anything not listed in Scope.
