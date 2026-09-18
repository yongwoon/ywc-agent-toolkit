# yw-000044-030-test-add-readonly-return-contract-validator

## Purpose
Add a mechanical CI check to `scripts/validate.sh` that fails validation if any Claude Code agent whose `tools:` list omits `Write` lacks the inline-return qualifier inside its own `## Return Contract` section — so the contradiction fixed in `yw-000044-010` cannot silently regress, and so a future 8th read-only agent is caught automatically without a per-agent allowlist.

## Scope
- Add a new bash function `check_agent_readonly_return_contract()` (or equivalent name) to `scripts/validate.sh`.
- Call it from `check_cc_agents()` right after the existing `check_agent_file "$file"` call (`scripts/validate.sh:757`), with the same `$file` argument.
- Logic: skip agents whose `tools:` frontmatter is absent/malformed or contains `Write` (word-boundary match); for the rest, extract the `## Return Contract` section body and require a match for an inline-return qualifier regex; emit `ERROR: ...` and increment `ERRORS` if absent.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260917-readonly-agent-inline-return.md` FR-3, AC3, AC4, Edge Cases (all 3 bullets)

### Summary
`check_cc_agents()` (`scripts/validate.sh:741-760`) already loops every `claude-code/agents/ywc-*.md` file and calls `check_agent_file "$file"` per file — this task hooks a new check into that same per-file loop, requiring no new loop. The new check must scope its regex search specifically to the `## Return Contract` section (extracted from that heading to the next `^## ` heading or EOF), not the whole file body, so a stray mention elsewhere (e.g. in Success Criteria or Boundaries) does not produce a false pass — this mirrors PR #234's own Rule 8 fix in the sibling project after an initial whole-body search let mismatched files through. This task depends on `yw-000044-010` because AC3 requires verifying `bash scripts/validate.sh` exits 0 against the already-fixed tree, and requires reintroducing the bad phrase into one already-fixed agent's `## Return Contract` section to prove the regression check fires.

### Out of Scope (from spec)
- Validating `tools:` shape itself (malformed `tools:` frontmatter is a pre-existing gap in `check_agent_file`, not this rule's job)
- A standalone Python validator script — this project's convention is bash checks inside `scripts/validate.sh`
- Any change to the 7 agent files' body text (handled by `yw-000044-010`) or `subagent-status-actions.md` (handled by `yw-000044-020`)

## Criticality
`normal` — this task only extends a CI text-matching script; no auth, payment, secret-handling, or PII-adjacent code is touched.

## Dependencies

### Depends On
- `yw-000044-010-docs-fix-readonly-agent-return-contract` — provides the already-fixed tree needed to (a) confirm `bash scripts/validate.sh` exits 0 for the agents section post-fix (AC3 positive case), and (b) reintroduce the bad phrase into one fixed agent's `## Return Contract` section to prove the new check catches the regression (AC3 negative case)

### Depended By
- (None — leaf task)

## Key Files
- `scripts/validate.sh` — new `check_agent_readonly_return_contract()` function; one new call site inside `check_cc_agents()` at line 757

## Notes
- The spec's FR-3 step 3 references "the same extraction idiom used for other section-scoped checks already in this file, e.g. `check_codex_agent_file`'s field checks". Verified during task generation that `check_codex_agent_file` (`scripts/validate.sh:542-589`) actually only does flat `grep -q "^${field} ="` frontmatter-field checks, not a heading-to-heading section extraction. No existing section-extraction idiom exists in this file yet; implement a straightforward `awk`/`sed` range extraction (from the `## Return Contract` heading line to the next line matching `^## ` or EOF) rather than searching for a nonexistent precedent.
- `Write`-substring guard: match `tools:` list contents on a word boundary so `Rewrite`/`WriteXyz` (unlikely today, but possible in a future agent name/tool) never falsely counts as holding `Write`. A regex like `\bWrite\b` (or comma/bracket-delimited token match against the `[A-Za-z, ]` list) satisfies this.
- Qualifier regex suggestion from the spec: `returns? inline|read-only review-worker exception` — case-sensitivity and exact wording should match what `yw-000044-010` actually wrote (re-read one of the 7 fixed files' `## Return Contract` paragraph before finalizing the regex).
- AC4 requires the new check to **not** fire for the 6 write-capable agents (`ywc-backend-coder`, `ywc-cloud-engineer`, `ywc-doc-writer`, `ywc-frontend-coder`, `ywc-qa-engineer`, `ywc-refactor-cleaner`) — all confirmed to carry `Write` in their `tools:` list as of task generation.

## Parallel Execution Metadata

### Ownership
- `scripts/validate.sh`

### Owned Interface
- (None — no public interface owned; this is a CI script internal function)

### Shared Surfaces
- `check_cc_agents()` dispatch loop in `scripts/validate.sh` (extended with one new call, not restructured)

### Conflicts With
- (None identified — `yw-000044-010` and `yw-000044-020` do not touch `scripts/validate.sh`)

### Parallelizable After
- `yw-000044-010-docs-fix-readonly-agent-return-contract`

### Task Verify
- `bash scripts/validate.sh` exits 0 against the fixed tree (AC3 positive case)
- Manually reintroduce the phrase "goes to a file under the caller's artifact directory" inside one read-only agent's `## Return Contract` section, re-run `bash scripts/validate.sh`, confirm it exits non-zero with an `ERROR` message naming that file, then revert the manual edit (AC3 negative case — do not leave this test edit committed)
- `bash scripts/validate.sh` still passes for the 6 write-capable agents with no new errors attributable to this check (AC4)

## Out of Scope
- Any change to the 7 read-only agents' body text (handled by `yw-000044-010`)
- Any change to `subagent-status-actions.md` (handled by `yw-000044-020`)
- Inventing `tools:` frontmatter shape validation beyond the word-boundary `Write` check this rule needs
