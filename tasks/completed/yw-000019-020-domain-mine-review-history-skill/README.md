# yw-000019-020-domain-mine-review-history-skill

## Purpose
Create the discoverable Codex `ywc-mine-review-history` skill that safely mines a bounded window of merged-PR bot comments into confirmation-gated review-memory proposals.

## Scope
Create the Codex skill contract, executable bulk-fetch helper, UI metadata, and required localized README files. Document exact CLI selection semantics, anchored bot allowlist, NDJSON output, GraphQL/thread and later-fix evidence boundary, classification, recurrence, project-local handoff, shared-catalog proposal-only behavior, and dry-run confirmation flow.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#fr1--skill-metadata-and-localized-documentation`
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#fr2--hardened-bulk-fetch-helper`
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#fr3--classification-routing-and-confirmation`
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#module-boundaries`

### Summary
The new skill is a producer: it reads a confirmed bounded merged-PR scope, emits only allowlisted bot-comment NDJSON from the helper, obtains resolution and later-fix evidence, clusters only distinct PR recurrence, and presents a complete changeset before any write. Project-local writes delegate to `ywc-review-learnings --source mining`; shared catalog entries remain maintainer proposals.

### Out of Scope (from spec)
- Mining-source consumer contract — handled by `yw-000019-010-domain-review-learnings-mining-contract`.
- Behavioral fixtures and hermetic helper tests — handled by `yw-000019-030-test-mine-review-history-contract`.
- Runtime writes to project learnings or shared catalog.
- Custom-agent changes, new dependencies, Claude Code port, and upstream/release changes.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000019-010-domain-review-learnings-mining-contract` — provides the exact confirmation-gated `mining` handoff boundary.

### Depended By
- `yw-000019-030-test-mine-review-history-contract` — verifies the CLI/helper and classification contracts.
- `yw-000020-010-docs-codex-catalog-distribution` — catalogs and syncs the completed source skill.

## Key Files
- `codex/skills/ywc-mine-review-history/SKILL.md`
- `codex/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh`
- `codex/skills/ywc-mine-review-history/agents/openai.yaml`
- `codex/skills/ywc-mine-review-history/README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`

## Notes
The helper stdout is intentionally insufficient for resolution/reply inference. Keep all owner boundaries explicit and preserve executable mode. Do not edit `plugins/ywc-agent-toolkit/skills/` directly.

## Hardening Evidence
### Test Feedback Path
- RED-first target: `codex/skills/ywc-mine-review-history/scripts/test_fetch_bulk_review_comments.sh` — created by `yw-000019-030` before behavior is considered complete.
- Existing coverage: `bash -n` plus the repository validation mirror.

### Interface Contract
- Contract: bulk helper positional CLI and NDJSON stdout
- Owner task: `yw-000019-020-domain-mine-review-history-skill`
- Canonical signature: `fetch-bulk-review-comments.sh <owner/repo> --limit <N> [--since <YYYY-MM-DD>]` → one JSON object per eligible comment with `pr,id,path,line,body,in_reply_to_id`
- Consumers: `yw-000019-030-test-mine-review-history-contract`, Codex user, new skill workflow
- Implementation opacity: consumers use the documented grammar and fields without relying on helper internals.
- Mismatch action: `NEEDS_CONTEXT`
- Inputs: resolved repository, positive limit, optional ISO UTC date
- Outputs: NDJSON records; diagnostics plus nonzero final status on per-PR API failures
- Error model: usage/validation exit 2 before `gh`; missing tools or API failures are nonzero
- Impacted tests: hermetic helper test and JSON/schema checks

### Critical Surface Review
- Review requirement: `ywc-impl-review` or manual full implementation review — retryable external API calls and duplicate-sensitive proposal routing.

### Data Integrity Hardening
- Trigger surface: retryable command/API; duplicate-sensitive side effect
- Atomic / locking strategy: no runtime durable write; confirmation gate and delegated owner serialize writes
- Transaction boundary: changeset presentation through confirmed owner handoff
- Idempotency guard: distinct-PR recurrence and catalog duplicate check before proposal
- Required tests: API failure injection, duplicate-PR recurrence, confirmation-before-write

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-mine-review-history/**`

### Shared Surfaces
- Bulk-helper NDJSON contract
- `ywc-review-learnings --source mining` handoff

### Conflicts With
- `yw-000019-010-domain-review-learnings-mining-contract` — sequential contract handoff.
- `yw-000019-030-test-mine-review-history-contract` — test task consumes this contract and must not redefine it.

### Parallelizable After
- `yw-000019-010-domain-review-learnings-mining-contract`

### Task Verify
- `bash -n codex/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh`
- `rg -n "--repo|--limit|--since|--min-recurrence|--dry-run|in_reply_to_id|github-actions|confirmation" codex/skills/ywc-mine-review-history`

## Out of Scope
- Eval fixtures, helper mock harness, catalog rows, root README counts, and generated package sync.
