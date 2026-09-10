# yw-000035-050-refactor-cleaner-boundary-note — Implementation Checklist

## Prerequisites
- [ ] None — root task.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `claude-code/agents/ywc-refactor-cleaner.md` only.
- [ ] Do NOT edit `claude-code/agents/ywc-qa-engineer.md`.

## Stop Conditions
- [ ] Stop if the target sentence already exists in the file.
- [ ] Stop if `## Boundaries` heading cannot be found (confirmed at line 38 as of spec authoring — re-verify).

## Implementation Steps
- [ ] Locate the `## Boundaries` section in `claude-code/agents/ywc-refactor-cleaner.md` (currently states SAFE-tier dead-code deletion only).
- [ ] Add exactly one sentence: "May also perform read-only complexity measurement (e.g. CRAP-gate greps via Bash) and report findings; deletion authority remains SAFE-tier only."
- [ ] Do not modify any other section of this file (Mission, Success Criteria, Return Contract) and do not touch `ywc-qa-engineer.md`.

## Task Verify
- [ ] `grep -q "May also perform read-only complexity measurement" claude-code/agents/ywc-refactor-cleaner.md`
- [ ] `git diff --name-only` shows exactly one file changed: `claude-code/agents/ywc-refactor-cleaner.md`

## Verification
- [ ] `bash scripts/validate.sh` exits 0
- [ ] No lint/typecheck/build/test toolchain applies to this repository.
