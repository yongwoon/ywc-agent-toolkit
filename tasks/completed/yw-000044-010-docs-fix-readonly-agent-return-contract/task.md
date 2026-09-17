# yw-000044-010-docs-fix-readonly-agent-return-contract — Implementation Checklist

## Prerequisites
- [ ] None — this is a root task.

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md` — the 7 named agent `.md` files only
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if any of the 7 files' 3 expected sites cannot be located by grep (the file has drifted from the spec's description)
- [ ] Stop if a site's surrounding structure (heading name, table shape) differs enough that the replacement wording would not fit grammatically — report and ask rather than force a bad edit
- [ ] Stop if an edit would require touching the Codex mirror or `plugins/ywc-agent-toolkit` (out of scope per spec)

## Implementation Steps
- [ ] For each of the 7 files, re-`grep -n "goes to a file\|Write the .* to a file\|file under the.*artifact directory"` immediately before editing that file, to get current (not spec-cached) line numbers
- [ ] `claude-code/agents/ywc-architect.md`: rewrite the Success Criteria bullet, Return Contract paragraph, and Anti-patterns row per the replacement wording in README.md Notes
- [ ] `claude-code/agents/ywc-go-reviewer.md`: same 3-site rewrite, preserving the "escape-analysis"/goroutine-specific noun phrases
- [ ] `claude-code/agents/ywc-performance-engineer.md`: same 3-site rewrite, preserving the "bundle-analyzer treemap"/query-plan noun phrases
- [ ] `claude-code/agents/ywc-python-reviewer.md`: same 3-site rewrite, preserving the "type-theory"/asyncio noun phrases
- [ ] `claude-code/agents/ywc-root-cause-analyst.md`: same 3-site rewrite, preserving the "architecture-vs-fix verdict reasoning" noun phrase
- [ ] `claude-code/agents/ywc-security-engineer.md`: same 3-site rewrite, preserving the "findings dump" noun phrase
- [ ] `claude-code/agents/ywc-typescript-reviewer.md`: same 3-site rewrite, preserving the "type-theory lecture" noun phrase

## Task Verify
- [ ] `grep -rn "goes to a file\|Write the .* to a file\|file under the.*artifact directory" claude-code/agents/ywc-architect.md claude-code/agents/ywc-go-reviewer.md claude-code/agents/ywc-performance-engineer.md claude-code/agents/ywc-python-reviewer.md claude-code/agents/ywc-root-cause-analyst.md claude-code/agents/ywc-security-engineer.md claude-code/agents/ywc-typescript-reviewer.md` returns zero matches (AC1)
- [ ] `grep -c "§3.5" claude-code/agents/ywc-architect.md` (and the other 6 files) still shows at least 2 occurrences per file (the existing pointer line plus the new Return Contract paragraph reference) — confirms the rewrite did not accidentally delete the pointer

## Verification
- [ ] `bash scripts/validate.sh` exits 0 (this repo's sole CI-mirroring check; no separate lint/typecheck/test/build commands apply to prompt-body Markdown edits)

## Implementation Notes (optional)
