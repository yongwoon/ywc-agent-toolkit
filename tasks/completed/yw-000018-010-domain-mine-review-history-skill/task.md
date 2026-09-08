# yw-000018-010-domain-mine-review-history-skill — Implementation Checklist

## Prerequisites
- [ ] (None — root task)

## Allowed Edit Scope
- [ ] Stay within `claude-code/skills/ywc-mine-review-history/**`
- [ ] If a change to `ywc-review-learnings` files seems needed, stop — that belongs to `yw-000018-020-docs-review-learnings-cross-reference`

## Stop Conditions
- [ ] Stop if `claude-code/skills/ywc-mine-review-history/` already exists with unrelated content (should not — verified absent at task-generation time)
- [ ] Stop if the promotion path would require any direct `Write`/`Edit` to `docs/review-learnings.md` or `references/recurring-defects.md` (must go through `ywc-review-learnings --mode update --source pr` only)
- [ ] Stop if implementing FR2 would require importing a new library/dependency beyond `gh`, `jq`, and bash builtins (library introduction is a separate task category, not this one)

## Implementation Steps

- [ ] **Scaffold the skill directory**
  - [ ] Create `claude-code/skills/ywc-mine-review-history/` and `claude-code/skills/ywc-mine-review-history/scripts/`
  - [ ] Confirm the directory name exactly matches the `name:` frontmatter value that will be written into `SKILL.md` (required by `scripts/validate.sh`'s `check_skill_dir`)

- [ ] **Write `SKILL.md`**
  - [ ] Frontmatter: `name: ywc-mine-review-history`; `description:` starting `(ywc) Use when...` with trigger phrases for a batch/retrospective PR review-comment sweep, ending with an explicit "Do not use for…" clause naming `ywc-review-learnings` (single-PR/on-demand) and `ywc-incident-postmortem` (single-incident) — per AC6
  - [ ] Body opens with an `**Announce at start:**` line and includes a `## Rationalization Defense` table with ≥5 domain-specific Excuse/Reality rows (per `ywc-skill-author` convention referenced in `claude-code/skills/CLAUDE.md`)
  - [ ] Document FR1: `--limit <n>` / `--since <date>`, at least one required, no unbounded default
  - [ ] Document FR2: batch fetch reusing the `capture-sources.md` `--source pr` query shape, iterated per PR, with the broader bot-login regex (see Notes) — emitting NDJSON tagged by source PR number
  - [ ] Document FR3: per-comment classification into `DO` / `FALSE-POSITIVE` / skip, identical rule to `capture-sources.md`'s `--source pr` table
  - [ ] Document FR4: defect-class clustering (judgment-based) and recurrence counted by **distinct PRs**, not raw comment count
  - [ ] Document FR5: `--min-recurrence` (default 3, CLI-overridable), inclusive threshold (`count >= --min-recurrence`), promoted classes offered to `ywc-review-learnings --mode update --source pr` with aggregated evidence (contributing PR numbers + one representative comment per PR); below-threshold classes reported only, never auto-promoted — state this explicitly enough to satisfy AC4 (names the flag, the default, and the "distinct PR" unit)
  - [ ] Document FR6: report surface (PRs scanned + date range, comments fetched, comments classified by outcome, defect classes found, which met vs. missed the recurrence threshold) — never omitted, `(none)` when empty
  - [ ] State explicitly that promotion is a skill invocation (`ywc-review-learnings --mode update --source pr`), never a direct file write — satisfies AC5

- [ ] **Write `scripts/fetch-bulk-review-comments.sh`**
  - [ ] Port from `develop-with-llm` commit `93129bd89756fad8e4fa17000e9d8e54325280fb`: validate `--limit`/`--since` inputs, separate `gh api` from `jq --arg` piping, anchor the bot-login regex, propagate `gh api` failures (no `|| true`)
  - [ ] Use the broader inline regex `coderabbitai|coderabbit|codex|claude|anthropic|github-actions`, anchored, per the Bot-login allowlist decision (Notes)
  - [ ] Match `scan-secrets.sh`/`detect-ci-commands.sh` style: `#!/usr/bin/env bash`, usage header comment, `set -uo pipefail` or `set -euo pipefail`, explicit numbered exit codes
  - [ ] Emit NDJSON (one line per comment, tagged with its source PR number) to stdout

- [ ] **Write the 4 README locale files**
  - [ ] `README.md` — Korean prose, English technical terms preserved
  - [ ] `README.en.md` — English
  - [ ] `README.ja.md` — Japanese prose, English technical terms preserved
  - [ ] `README.ko.md` — Korean (per this repo's existing Tier-1 locale set convention: `.md` and `.ko.md` both exist)
  - [ ] Each summarizes purpose, usage flags (`--limit`, `--since`, `--min-recurrence`), and the promotion relationship to `ywc-review-learnings`

## Task Verify
- [ ] `bash scripts/validate.sh` — 0 errors for the new directory
- [ ] `bash -n claude-code/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh` — exits 0
- [ ] `shellcheck claude-code/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh` — no errors (triage warnings, do not silently suppress)
- [ ] `npx markdownlint-cli2@0.22.1 "claude-code/skills/ywc-mine-review-history/README*.md"` — 0 errors
- [ ] `grep -rn "review-learnings.md\|recurring-defects.md" claude-code/skills/ywc-mine-review-history/SKILL.md` — only a skill-delegation reference, no direct write instruction

## Verification
- [ ] `bash scripts/validate.sh` passes (repo has no separate lint/typecheck/build step for skill-only changes)
- [ ] `shellcheck claude-code/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh` passes
- [ ] `npx markdownlint-cli2@0.22.1 "claude-code/skills/ywc-mine-review-history/README*.md"` passes

## Implementation Notes
(grows during execution — none yet)
