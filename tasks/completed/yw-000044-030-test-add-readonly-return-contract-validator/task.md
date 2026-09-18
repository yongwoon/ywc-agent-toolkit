# yw-000044-030-test-add-readonly-return-contract-validator — Implementation Checklist

## Prerequisites
- [ ] `yw-000044-010-docs-fix-readonly-agent-return-contract` is completed (merged) — this task's AC3 verification requires the already-fixed tree

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md` — `scripts/validate.sh` only
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if `yw-000044-010` is not actually merged (its fixed tree is a prerequisite for AC3's positive-case test)
- [ ] Stop if `check_cc_agents()` or `check_agent_file()`'s shape has changed enough that "call right after the existing `check_agent_file` call" is ambiguous
- [ ] Stop if extending the check would require inventing `tools:` frontmatter shape validation beyond a word-boundary `Write` match

## Implementation Steps
- [ ] Re-`grep -n "check_cc_agents\|check_agent_file "` `scripts/validate.sh` to confirm current line numbers before editing
- [ ] Add `check_agent_readonly_return_contract()`: read the `tools:` frontmatter line via `sed -n 's/^tools:[[:space:]]*//p' "$file" | head -n1`; skip if absent or not a `[...]`-shaped list
- [ ] Add the `Write` word-boundary skip: if the `tools:` list contains `Write` as a whole token (not a substring of `Rewrite`/`WriteXyz`), skip — the rule only applies to read-only agents
- [ ] Add the `## Return Contract` section extraction: from that heading line to the next line matching `^## ` or EOF, using `awk` or `sed` (no existing section-extraction idiom to copy in this file — see README Notes)
- [ ] Within the extracted section only, `grep -Eq` for the qualifier regex `returns? inline|read-only review-worker exception` (confirm exact wording against one of the 7 files `yw-000044-010` fixed); on no match, `echo "ERROR: agents/<base>.md is a read-only agent (no Write tool) but its Return Contract section does not carry the inline-return qualifier"` and increment `ERRORS`
- [ ] Wire the call: add `check_agent_readonly_return_contract "$file"` inside `check_cc_agents()`'s existing loop, immediately after `check_agent_file "$file"`

## Task Verify
- [ ] `bash scripts/validate.sh` exits 0 against the fixed tree
- [ ] Temporarily reintroduce "goes to a file under the caller's artifact directory" into one read-only agent's `## Return Contract` section, re-run `bash scripts/validate.sh`, confirm non-zero exit with an `ERROR` line naming that file, then revert the temporary edit before finishing
- [ ] `bash scripts/validate.sh` shows no new errors for the 6 write-capable agents (`ywc-backend-coder`, `ywc-cloud-engineer`, `ywc-doc-writer`, `ywc-frontend-coder`, `ywc-qa-engineer`, `ywc-refactor-cleaner`)

## Verification
- [ ] `bash scripts/validate.sh` exits 0 (this repo's sole CI-mirroring check for this change; no separate lint/typecheck/build applies to a bash script edit)

## Implementation Notes (optional)
