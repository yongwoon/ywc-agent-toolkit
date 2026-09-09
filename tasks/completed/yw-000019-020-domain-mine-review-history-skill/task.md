# yw-000019-020-domain-mine-review-history-skill — Implementation Checklist

## Prerequisites
- [ ] `yw-000019-010-domain-review-learnings-mining-contract` is completed and merged.
- [ ] The `--source mining` handoff contract matches README.md.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-mine-review-history/**`.
- [ ] Do not edit `plugins/ywc-agent-toolkit/skills/**` or catalog/root README files.

## Stop Conditions
- [ ] Stop if the helper requires a new runtime dependency or service.
- [ ] Stop if durable writes, shared-catalog mutation, or custom-agent edits become necessary.
- [ ] Stop if the helper contract differs from the README Interface Contract.

## Hardening Gate
- [ ] Classify as new behavior with retryable external API and duplicate-sensitive routing surfaces.
- [ ] Record the RED-first helper-test target owned by `yw-000019-030` before implementation.
- [ ] Preserve the helper interface contract exactly; return `NEEDS_CONTEXT` on mismatch.
- [ ] Apply the retry/API and duplicate-sensitive Data Integrity fields from README.
- [ ] Require full implementation review before `DONE`.

## Implementation Steps
- [ ] Create `codex/skills/ywc-mine-review-history/SKILL.md` with Codex-only frontmatter, activation/anti-trigger boundaries, five arguments, rationale defenses, and seven-step scope/fetch/classify/cluster/route/confirm/report workflow.
- [ ] Implement `scripts/fetch-bulk-review-comments.sh` with portable Bash, usage/unknown-flag handling, positive-integer and ISO-date validation, pre-`gh` exit 2 validation, tool checks, repository-scoped merged-PR selection, anchored case-insensitive bot allowlist, explicit `gh api` error propagation, and exact six-field NDJSON.
- [ ] Document GraphQL pagination, exact later-commit patch-hunk overlap, conservative evidence drops, distinct-PR recurrence, catalog duplicate lookup, confirmation-before-write, and `--dry-run` behavior.
- [ ] Add `agents/openai.yaml` and the four required Tier 1 README locales, keeping wording aligned with the source skill and English task language policy.

## Task Verify
- [ ] `bash -n codex/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh`
- [ ] `rg -n -- "--repo|--limit|--since|--min-recurrence|--dry-run|in_reply_to_id|github-actions|confirmation|GraphQL|distinct PR" codex/skills/ywc-mine-review-history`
- [ ] `git diff --summary -- codex/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh` confirms executable mode.

## Verification
- [ ] lint: `bash -n codex/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh`
- [ ] typecheck: N/A — no typed application source
- [ ] tests: delegated to `yw-000019-030-test-mine-review-history-contract`
- [ ] build: N/A — source package is validated by repository scripts

## Implementation Notes (optional)
