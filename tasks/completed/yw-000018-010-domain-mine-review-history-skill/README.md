# yw-000018-010-domain-mine-review-history-skill

## Purpose
Create the new `ywc-mine-review-history` Claude Code skill: a batch/retrospective sweep that mines bot review comments (CodeRabbit / Codex Review / Claude Review) across N already-merged PRs, clusters them into recurring defect classes, and routes classes recurring across `--min-recurrence` distinct PRs into `ywc-review-learnings --mode update --source pr`. This closes the gap identified from `develop-with-llm` PR #226: neither `ywc-review-learnings --mode update --source pr` (single PR, on demand) nor `ywc-incident-postmortem` (single incident) covers a batch sweep of PRs that predate either skill's adoption.

## Scope
- New directory `claude-code/skills/ywc-mine-review-history/` containing `SKILL.md`, `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`, `scripts/fetch-bulk-review-comments.sh`.
- `SKILL.md` documents: scope selection (`--limit`/`--since`, at least one required), batch fetch, accept/dismiss classification (reusing the existing `--source pr` rule), defect-class clustering with distinct-PR recurrence counting, the `--min-recurrence` (default 3) gated promotion, and the report surface (PRs scanned, comments fetched/classified, defect classes found vs. promoted).
- `scripts/fetch-bulk-review-comments.sh` is ported from `develop-with-llm` commit `93129bd89756fad8e4fa17000e9d8e54325280fb`, adapted to this repo's bot-login allowlist decision (see Notes).
- This task does **not** touch `ywc-review-learnings` itself — the cross-reference edit is a separate task (`yw-000018-020-docs-review-learnings-cross-reference`).

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260909-ywc-mine-review-history.md#scope` — skill directory contents, bot-login allowlist decision, promotion target
- `docs/ywc-plans/20260909-ywc-mine-review-history.md#functional-requirements` — FR1 (scope selection), FR2 (batch fetch), FR3 (classification), FR4 (clustering/recurrence), FR5 (gated promotion), FR6 (report surface)
- `docs/ywc-plans/20260909-ywc-mine-review-history.md#acceptance-criteria` — AC1-AC6 (this task's scope; AC7 belongs to the sibling cross-reference task)
- `docs/ywc-plans/20260909-ywc-mine-review-history.md#non-functional-requirements` — anchored bot-login regex, `gh api` failure propagation, auditability of the report surface
- `docs/ywc-plans/20260909-ywc-mine-review-history.md#skill-authoring-precedent` — script style precedent (`scan-secrets.sh`, `detect-ci-commands.sh`)
- `claude-code/skills/ywc-review-learnings/references/capture-sources.md#--source-pr-bot-comment-harvest` — the `gh api --paginate` query shape and accept/dismiss classification table this skill reuses (query shape only — the login filter is widened, see Notes)
- `claude-code/skills/CLAUDE.md` — README locale language policy and `ywc-skill-author` authoring conventions (description frontmatter, Rationalization Defense table)

### Summary
This task ports a batch-mining capability from an external PR into this repo as a net-new, self-contained skill directory. The skill's classification rule and query shape are reused verbatim from `ywc-review-learnings`'s existing `--source pr` path, generalized to iterate over a PR list; the bot-login regex is deliberately widened per the spec's Scope decision (see Notes). The only write path is delegation to `ywc-review-learnings --mode update --source pr` — this skill never writes `docs/review-learnings.md` or `references/recurring-defects.md` directly (AC5).

### Out of Scope (from spec)
- Cross-project `recurring-defects.md` append infrastructure — explicitly out of scope in the spec (that reference stays read-only).
- Porting to `codex/skills/` — out of scope per the user's original request.
- Any change to `claude-code/agents/` — upstream made no agent changes.
- A new `--source mining` value on `ywc-review-learnings` — the existing `--source pr` rule is reused verbatim.
- The cross-reference edit to `ywc-review-learnings`'s own files — handled by `yw-000018-020-docs-review-learnings-cross-reference`.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `yw-000018-020-docs-review-learnings-cross-reference` — needs this skill's final directory name/path to exist before adding a cross-reference sentence to it.

## Key Files
- `claude-code/skills/ywc-mine-review-history/SKILL.md` — created
- `claude-code/skills/ywc-mine-review-history/README.md` — created (Korean)
- `claude-code/skills/ywc-mine-review-history/README.en.md` — created
- `claude-code/skills/ywc-mine-review-history/README.ja.md` — created
- `claude-code/skills/ywc-mine-review-history/README.ko.md` — created
- `claude-code/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh` — created

## Notes
- **Bot-login allowlist**: use the broader regex already used by the shared executor infra (`claude-code/skills/scripts/poll-pr-reviews.sh:25`) — `coderabbitai|coderabbit|codex|claude|anthropic|github-actions` — rather than the narrower `coderabbitai|chatgpt-codex|github-actions` in `capture-sources.md`. Keep the regex **inline in the new script**, not extracted into a shared constant (per spec's YAGNI rationale — three of four existing sites already keep their own inline copy).
- Anchor the regex (`^(coderabbitai|coderabbit|codex|claude|anthropic|github-actions)$`-equivalent), not a bare substring match — carried over from the upstream fix in commit `93129bd`.
- `gh api` failures must propagate (non-zero exit), never swallowed with `|| true`.
- `--limit`/`--since`: at least one bound is required; no unbounded default scan.
- Follow `ywc-create-pr/scripts/scan-secrets.sh` and `detect-ci-commands.sh` style: `#!/usr/bin/env bash`, usage header comment, `set -uo pipefail` or `set -euo pipefail`, explicit numbered exit codes.
- `SKILL.md` description frontmatter must include `(ywc) Use when...` trigger phrases and an explicit "Do not use for…" clause distinguishing this skill from `ywc-review-learnings` (single-PR/on-demand) and `ywc-incident-postmortem` (single-incident) — see `ywc-handle-pr-reviews`/`ywc-create-pr` for the existing anti-trigger convention. Invoke `ywc-skill-author` conventions (Announce-at-start line, Rationalization Defense table with ≥5 domain-specific rows) per `claude-code/skills/CLAUDE.md`.
- No `test.md` for this task — this is a skill/library-introduction-shaped task with no UI, no external service call outside `gh` (already a dependency elsewhere), and verification is by inspection/shellcheck/validate.sh per the AC list, matching the "library introduction tasks... via Verification" omission rule.

## Out of Scope
- Editing `ywc-review-learnings/SKILL.md` or `references/capture-sources.md` — that is `yw-000018-020-docs-review-learnings-cross-reference`'s exclusive Ownership.
- Any `codex/skills/` port.
- Building the `recurring-defects.md` append-only sink.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-mine-review-history/**`

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `bash scripts/validate.sh`
- `bash -n claude-code/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh`
- `shellcheck claude-code/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh`
- `npx markdownlint-cli2@0.22.1 "claude-code/skills/ywc-mine-review-history/README*.md"`
- `grep -rn "review-learnings.md\|recurring-defects.md" claude-code/skills/ywc-mine-review-history/SKILL.md` (must show only a skill-invocation reference, never a direct Write/Edit instruction)
