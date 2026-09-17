# yw-000044-010-docs-fix-readonly-agent-return-contract

## Purpose
Seven read-only Claude Code agents (`tools:` omits `Write`) instruct the caller, in three separate places in each agent's own body, to "write analysis to a file under the caller's artifact directory" — an action the agent cannot perform. This task rewrites all three contradicting sites in each of the 7 agents to instruct an inline, bounded return instead, closing the self-contradiction that leaves the agent with no terminal move (the "read-only reviewer agent stall" defect class from PR #234 of the sibling `develop-with-llm` project).

## Scope
- In each of the 7 read-only agent files, rewrite exactly 3 sites per file (Success Criteria bullet, Return Contract paragraph, Anti-patterns table row) to reference the inline-return contract, per the exact replacement wording in Spec FR-1.
- Agents: `ywc-architect`, `ywc-go-reviewer`, `ywc-performance-engineer`, `ywc-python-reviewer`, `ywc-root-cause-analyst`, `ywc-security-engineer`, `ywc-typescript-reviewer`.
- Preserve each site's existing agent-specific noun phrase (e.g. "trade-off matrix", "goroutine-theory", "findings dump") — only the write-to-file clause changes.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260917-readonly-agent-inline-return.md` FR-1, AC1, Scope, Existing Constraints Touched (row 2)

### Summary
Each of the 7 agent files has 3 sites (Success Criteria bullet, Return Contract paragraph, Anti-patterns row) that currently instruct writing full analysis to a file, contradicting the fact that these agents hold no `Write` tool. Replace each site with wording that returns the payload inline, bounded, per the read-only review-worker exception at `subagent-status-actions.md` §3.5 (added by `yw-000044-020`, but not a build dependency for this task — the pointer text is written now regardless of whether §3.5 already resolves). Line numbers in the spec are approximate; re-`grep` each file immediately before editing rather than trusting fixed numbers, since edits earlier in the same file shift later line numbers.

### Out of Scope (from spec)
- Codex mirror (`codex/agents/*.toml`) — already correct, not touched
- `plugins/ywc-agent-toolkit` — no `agents/` directory to touch
- Any change to `tools:` grants
- The `§3.5` pointer line itself (`> §3.5. Do not restate the generic format inline.`, immediately below each `## Return Contract` heading) — already correct, not one of the 3 contradicting sites, left unchanged

## Criticality
`normal` — this task only edits agent prompt-body prose describing return-payload behavior; no auth, payment, secret-handling, or PII-adjacent code is touched.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `yw-000044-030-test-add-readonly-return-contract-validator` — needs this task's fixed tree to (a) verify `bash scripts/validate.sh` exits 0 against a tree that already carries the inline-return qualifier, and (b) reintroduce the bad phrase into one already-fixed file to prove the new validator rule catches the regression (AC3)

## Key Files
- `claude-code/agents/ywc-architect.md` — 3 sites (~lines 80-82, 119-121, 132)
- `claude-code/agents/ywc-go-reviewer.md` — 3 sites (~lines 185-186, 231, 246)
- `claude-code/agents/ywc-performance-engineer.md` — 3 sites (~lines 194-195, 230, 246)
- `claude-code/agents/ywc-python-reviewer.md` — 3 sites (~lines 169, 214-215, 229)
- `claude-code/agents/ywc-root-cause-analyst.md` — 3 sites (~lines 113, 141-142, 157)
- `claude-code/agents/ywc-security-engineer.md` — 3 sites (~lines 90, 141, 153)
- `claude-code/agents/ywc-typescript-reviewer.md` — 3 sites (~lines 128, 170-171, 185)

## Notes
- Verified during task generation (2026-09-17): all 7 files' 3 sites exist at line numbers within ±1 of the spec's table, confirming the spec is accurate as of this generation. Re-grep before each edit anyway.
- Replacement wording (adapt only the agent-specific noun phrase already present at each site):
  - **Success Criteria bullet**: `... stays under 300 words; supporting analysis returns inline, bounded, per the read-only review-worker exception (§3.5) — never to a file.`
  - **Return Contract paragraph**: `Full analysis (<agent-specific list>) returns inline, bounded, per the read-only review-worker exception in [claude-code/skills/references/subagent-status-actions.md](../skills/references/subagent-status-actions.md) §3.5; only status, 1-line summary, verdict/findings, and severity counts return.`
  - **Anti-patterns row** (`Avoid` column): `Return the bounded inline payload per §3.5 — never write to a file; this agent holds no Write tool.`
- This task does not require `yw-000044-020` to land first — the §3.5 pointer text is unchanged by this task (it already says "§3.5" verbatim in all 7 files) and will simply resolve once `yw-000044-020` adds the heading.

## Parallel Execution Metadata

### Ownership
- `claude-code/agents/ywc-architect.md`
- `claude-code/agents/ywc-go-reviewer.md`
- `claude-code/agents/ywc-performance-engineer.md`
- `claude-code/agents/ywc-python-reviewer.md`
- `claude-code/agents/ywc-root-cause-analyst.md`
- `claude-code/agents/ywc-security-engineer.md`
- `claude-code/agents/ywc-typescript-reviewer.md`

### Owned Interface
- (None — no public interface owned; this task only edits prompt prose)

### Shared Surfaces
- (None identified — each of the 7 files is exclusively owned by this task; `yw-000044-020` and `yw-000044-030` touch different files entirely)

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `grep -rn "goes to a file\|Write the .* to a file\|file under the.*artifact directory" claude-code/agents/ywc-architect.md claude-code/agents/ywc-go-reviewer.md claude-code/agents/ywc-performance-engineer.md claude-code/agents/ywc-python-reviewer.md claude-code/agents/ywc-root-cause-analyst.md claude-code/agents/ywc-security-engineer.md claude-code/agents/ywc-typescript-reviewer.md` — must return zero matches (AC1)
- `bash scripts/validate.sh` — must still exit 0 (no frontmatter/structure regression introduced by the prose edits)

## Out of Scope
- Editing any agent other than the 7 named above
- Editing the `§3.5` pointer line itself
- Adding the `§3.5` heading to `subagent-status-actions.md` (handled by `yw-000044-020`)
- Any validator change (handled by `yw-000044-030`)
