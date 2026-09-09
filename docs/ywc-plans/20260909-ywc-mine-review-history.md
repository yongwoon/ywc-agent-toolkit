# ywc-mine-review-history (Claude Code skill port)

> Status: Draft
> Scale: Medium
> Created: 2026-09-09
> Author: Claude Code (ywc-plan)
> Spec Reference: develop-with-llm PR #226 (https://github.com/yongwoon/develop-with-llm/pull/226) — port target, not binding on this repo's architecture

## Global Constraints

- Every `claude-code/skills/<name>/` directory must contain `SKILL.md` with `name:`/`description:` frontmatter (name matching the directory) and `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md` — enforced by `scripts/validate.sh` (`check_skill_dir`, `check_readme_set`) and CI's `validate.yml`. (`CLAUDE.md` "Skill Authoring Rules", `scripts/validate.sh:8-51`)
- `description:` frontmatter must include trigger phrases and explicit "Do not use for…" anti-triggers to avoid false activation against sibling skills. (`CLAUDE.md` "Skill Authoring Rules")
- Skill names follow `ywc-<kebab-case>`. Keep `SKILL.md` under ~500 lines; extract long procedures to `references/`. (`CLAUDE.md`)
- Do not reference other skills with `@skill-name` (force-load); reference by name only. (`CLAUDE.md`)
- New shell scripts must pass shellcheck (CI `validate.yml` runs shellcheck on `scripts/`) — apply the same discipline to skill-local scripts even though `scripts/validate.sh`'s shellcheck pass targets the top-level `scripts/` directory only; `ywc-create-pr/scripts/*.sh` is the in-repo precedent for style (`set -uo pipefail` or `set -euo pipefail`, usage comment header, explicit exit codes).
- CI's `markdownlint` workflow lints skill README files; new README files must pass with zero errors.
- Commit messages follow `<type>: <description>` (types: `feat`, `fix`, `docs`, `i18n`, `ci`, `chore`) and end with the attribution block mandated for this session (`Co-Authored-By: Claude Sonnet 5 …`, `Claude-Session: …`).

## Purpose

`develop-with-llm` PR #226 added `ywc-mine-review-history`, a skill that batch-mines bot review comments (CodeRabbit / Codex Review) across many already-merged PRs, clusters them into recurring defect classes, and routes classes that recur across `--min-recurrence` (default 3) distinct PRs into durable review memory. This repo's Claude Code skill set has two existing capture paths — `ywc-review-learnings --mode update --source pr` (single PR, on demand) and `ywc-incident-postmortem` (single incident) — but no path for a **batch/retrospective sweep** of PRs that predate either skill's adoption. That sweep is the actual value PR #226 adds, and it is currently missing here.

## Scope

- New skill directory `claude-code/skills/ywc-mine-review-history/` with `SKILL.md`, `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`, `scripts/fetch-bulk-review-comments.sh`.
- The skill fetches bot review comments across N merged PRs (by count and/or date-range window), reusing the `gh api --paginate "repos/{owner}/{repo}/pulls/<PR>/comments"` query shape already documented in `claude-code/skills/ywc-review-learnings/references/capture-sources.md` `--source pr` section — iterated across PRs instead of one, and with the broader bot-login regex decided below (see the Bot-login allowlist item), not the narrower one `capture-sources.md` currently uses.
- Classification (accept vs dismiss) reuses the same resolved-thread / dismissal-reply signal already defined in `capture-sources.md`'s `--source pr` section — this skill does not invent a new classification rule, it applies the existing one at batch scale.
- Defect-class clustering: group classified comments by defect class (same free-text clustering judgment already used elsewhere in this skill family — no controlled vocabulary exists to automate this, consistent with `ywc-impl-review/SKILL.md:178`'s documented limitation for within-run occurrence counting).
- Recurrence gate: a defect class is promoted only when it recurs across `--min-recurrence` (default 3, CLI-overridable) **distinct PRs** — single-PR-only classes are reported but not promoted.
- Promotion target: **`ywc-review-learnings --mode update --source pr`** only (project-local `docs/review-learnings.md`, via the existing confirmation-gated write path). No new cross-project catalog write path is introduced (see Out of Scope).
- `fetch-bulk-review-comments.sh` is ported from the upstream PR's CodeRabbit-review-fixed revision (commit `93129bd89756fad8e4fa17000e9d8e54325280fb` in `develop-with-llm`), which already fixed: `--limit`/`--since` input validation, separating `gh api` from `jq --arg` piping, anchoring the bot-login allowlist, and propagating `gh api` failures instead of swallowing them with `|| true`.
- `claude-code/skills/ywc-review-learnings/SKILL.md` and `references/capture-sources.md` gain a short cross-reference noting that `ywc-mine-review-history` is the batch/retrospective entry point that feeds `--source pr`, alongside the existing single-PR convenience path — this is a documentation-only edit, not a new `--source` value.
- **Bot-login allowlist**: `fetch-bulk-review-comments.sh` adopts the broader regex already used by the shared executor infra — `coderabbitai|coderabbit|codex|claude|anthropic|github-actions` (from `claude-code/skills/scripts/poll-pr-reviews.sh`) — rather than the narrower `coderabbitai|chatgpt-codex|github-actions` regex in `ywc-review-learnings/references/capture-sources.md`. A batch/retrospective sweep is exactly the case where under-detecting a bot login (missing Claude Review or Codex-only comments the executor path already recognizes) silently shrinks the mined evidence set; the broader allowlist trades a small false-positive risk (an unrelated `github-actions` comment) for not missing true bot comments, and false positives are already absorbed by the accept/dismiss classification step (an uncategorizable comment simply gets skipped, not miscounted). The regex is kept **inline in the new script**, not extracted into a shared constant — three of the four existing sites (`capture-sources.md`, `poll-pr-reviews.sh`, `fetch-nitpick-comments.sh`) already keep their own inline copy with no shared import today, so introducing a shared-constant file now would be a new abstraction this port doesn't need (YAGNI); a future cross-cutting cleanup that unifies all four is a separate, explicitly out-of-scope follow-up (see Out of Scope).

## Out of Scope

- **Cross-project `recurring-defects.md` append infrastructure** (the `source: mining` provenance line, the append-only-sink schema, `ywc-impl-review` Step 7 / `ywc-incident-postmortem` Step 6.5 parity). This repo's `claude-code/skills/ywc-impl-review/references/recurring-defects.md` is explicitly documented as read-only today (`ywc-impl-review/SKILL.md:111`: "No mode ever writes to `docs/review-learnings.md` or `references/recurring-defects.md`"). Building that sink is a separate, materially larger architectural change (new provenance schema, new write gate, changes to two other skills' Step 6/7 flows) that PR #226's own scope only extended, it did not originate — introducing it here as a side effect of this port would silently expand this change's blast radius. Tracked as a candidate follow-up, not built now.
- Porting to `codex/skills/` (Codex variant). The user's request scoped this port to "claude code skills, agents" only.
- Any change to `claude-code/agents/`. The upstream PR made no agent changes (its commits touch zero `agents/` paths), and no agent-level capability is needed for this skill (it is a data-fetch + classify + delegate flow entirely within skill-authored steps).
- A new `--source mining` value on `ywc-review-learnings`. The existing `--source pr` classification rule is reused verbatim at batch scale; inventing a parallel enum value for the same rule would be a distinction without a behavioral difference (YAGNI).
- Any change to a `docs/llm-studies/research/`-equivalent tree — this repo has no such research-doc tree; the upstream `ai-slop-registry.md` research document is out of scope for this port (it documents terminology/reasoning for a repo-tree structure this project doesn't have).
- Modifying `scripts/install.sh` or `scripts/validate.sh` — the existing glob-driven skill discovery already picks up any new `claude-code/skills/<name>/` directory without a code change (verified: `scripts/validate.sh` iterates skill directories generically via `is_skill_dir`/`check_skill_dir`, not an explicit allowlist).

## Existing Constraints Touched

| Existing artifact | Behavior (verified by reading the file) | New code's interaction |
|---|---|---|
| `claude-code/skills/ywc-review-learnings/references/capture-sources.md` (`## --source pr` section) | Defines the `gh api --paginate "repos/{owner}/{repo}/pulls/<PR>/comments"` query filtered to `coderabbitai\|chatgpt-codex\|github-actions` logins, and the resolved-thread / dismissal-reply accept-vs-dismiss classification rule | Reuse the query shape and the classification rule verbatim, generalized to iterate over a PR list instead of a single `<PR>` — the login filter itself is widened per the Bot-login allowlist decision in Scope, not reused verbatim |
| `claude-code/skills/ywc-review-learnings/SKILL.md` (confirmation-gated write) | Every `--mode update` write requires the user-confirmation CHANGESET before touching `docs/review-learnings.md`; there is no non-interactive bypass for `docs/review-learnings.md` writes | New skill's promoted candidates go through this exact same confirmation gate — the new skill never writes `docs/review-learnings.md` directly, it only invokes `ywc-review-learnings --mode update --source pr` |
| `claude-code/skills/ywc-impl-review/SKILL.md:111` | "No mode ever writes to `docs/review-learnings.md` or `references/recurring-defects.md`" — states `recurring-defects.md` is read-only under the current architecture | New skill does not write `recurring-defects.md`; this line remains accurate after the port and needs no edit |
| `scripts/validate.sh` (`check_skill_dir`, `check_readme_set`) | Generic per-directory checks: `SKILL.md` exists with `name:`/`description:` matching dirname; all four README locale files exist | New skill directory must satisfy both checks with no script change required |
| `.github/workflows/markdownlint.yml` glob covering skill READMEs | Lints skill README files | New skill's 4 README files must be markdownlint-clean before merge |
| `claude-code/skills/scripts/poll-pr-reviews.sh` + `claude-code/skills/references/pr-bot-polling.md` | Shared bot-detection infra used by `ywc-sequential-executor`/`ywc-parallel-executor` pre-merge; queries both `gh pr view --json reviews,comments` and `gh api .../pulls/<n>/comments`, matched against bot regex `coderabbitai\|coderabbit\|codex\|claude\|anthropic\|github-actions` | `fetch-bulk-review-comments.sh` reuses this broader regex for its own line-anchored `gh api` fetch (see Scope) — it does not call `poll-pr-reviews.sh` itself, since that script answers "did any bot post" for one open PR pre-merge, a different question from "fetch all bot comments across N merged PRs" |
| `claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-nitpick-comments.sh` | CodeRabbit-only fetch (`gh pr view --json reviews` scoped to `coderabbitai` review bodies), parses Nitpick pseudo-comments via a Python helper, per single PR | Not reused directly (different bot scope and a different comment shape — full review bodies vs line-anchored comments); named here only to complete the precedent-site enumeration, no interaction |

## Acceptance Criteria

- [ ] **AC1 — Skill structure passes validation**: When `bash scripts/validate.sh` is run after adding `claude-code/skills/ywc-mine-review-history/`, the script reports 0 errors for the new directory (name/frontmatter match, all 4 README locales present).
- [ ] **AC2 — Script is syntactically valid and shellcheck-clean**: When `bash -n claude-code/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh` is run, it exits `0`; when `shellcheck claude-code/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh` is run, it reports no errors (warnings triaged, not silently suppressed).
- [ ] **AC3 — Markdown lint clean**: When `npx markdownlint-cli2@0.22.1 "claude-code/skills/ywc-mine-review-history/README*.md"` is run, it reports 0 errors.
- [ ] **AC4 — Recurrence gate is documented and testable by inspection**: `SKILL.md` states the default `--min-recurrence` value (3) and that a defect class below this distinct-PR count is reported but not promoted — observable by reading the step where the gate is applied and confirming it names the CLI flag, the default, and the "distinct PR" unit (not distinct comment).
- [ ] **AC5 — No unauthorized write path introduced**: `grep -rn "review-learnings.md\|recurring-defects.md" claude-code/skills/ywc-mine-review-history/SKILL.md` shows the skill only *invokes* `ywc-review-learnings --mode update --source pr` (a skill delegation, not a direct file write) — no direct `Write`/`Edit` instruction targets either file from within this skill.
- [ ] **AC6 — Description frontmatter carries anti-triggers**: `ywc-mine-review-history/SKILL.md`'s `description:` field distinguishes itself from `ywc-review-learnings` (single-PR/on-demand) and `ywc-incident-postmortem` (single-incident), matching this repo's existing anti-trigger convention (e.g. `ywc-handle-pr-reviews`/`ywc-create-pr` descriptions) — observable by reading the frontmatter and confirming a "Do not use for…" clause naming both sibling skills.
- [ ] **AC7 — Cross-reference added, no behavior change to `ywc-review-learnings`**: `claude-code/skills/ywc-review-learnings/SKILL.md` and `references/capture-sources.md` mention `ywc-mine-review-history` as the batch entry point; `git diff` on these two files shows no change to the `--source` enum, the classification rule, or the confirmation-gate logic — only an added cross-reference sentence.

## Functional Requirements

### FR-1: Scope selection

The skill accepts a bounded scope for the sweep: either `--limit <n>` (most-recent N merged PRs) or `--since <date>` (merged-after date), matching the validated-input pattern already fixed upstream in `fetch-bulk-review-comments.sh`. At least one bound is required — an unbounded "scan everything" default is not offered (avoids an accidental full-history `gh api` sweep on a large repo).

### FR-2: Batch fetch

`scripts/fetch-bulk-review-comments.sh` iterates the selected merged PRs and fetches bot review comments per PR using the same `gh api --paginate` query shape as `ywc-review-learnings`'s `--source pr` path (with the broader bot-login regex from the Bot-login allowlist decision in Scope), emitting NDJSON (one line per comment, tagged with its source PR number) to stdout or a file.

### FR-3: Accept/dismiss classification

For each fetched comment, classify as `DO` (resolved thread + fix landed in a later commit), `FALSE-POSITIVE` (reply states not applicable / wrong), or skip (open, no resolution, no reply) — identical rule to `capture-sources.md`'s existing `--source pr` classification table, applied per comment across the whole NDJSON stream rather than a single PR's comments.

### FR-4: Defect-class clustering and recurrence count

Cluster classified comments into defect classes (judgment-based, no controlled vocabulary — same limitation `ywc-impl-review/SKILL.md:178` already documents for a different counting context) and count **distinct PRs** exhibiting each class (not raw comment count — two comments in the same PR count once toward recurrence).

### FR-5: Recurrence-gated promotion

Classes meeting or exceeding `--min-recurrence` (default 3) are surfaced as promotion candidates and offered to `ywc-review-learnings --mode update --source pr` with the aggregated evidence (list of contributing PR numbers, one representative comment body per PR) as context. Classes below the threshold are listed in the skill's own report output only — never silently dropped, and never auto-promoted without the existing `ywc-review-learnings` confirmation gate.

### FR-6: Report surface

The skill's own output (independent of anything promoted) states: PRs scanned (count + date range), comments fetched, comments classified `DO`/`FALSE-POSITIVE`/skipped, defect classes found, and which classes met vs missed the recurrence threshold — auditability parity with `ywc-impl-review`'s existing "Learning candidates" report block (`SKILL.md:178`), which is never omitted even when a section is empty (`(none)`).

## Quality Gate Contract

N/A — this repository has no CRAP/mutation quality-gate tooling; skill correctness is validated by `scripts/validate.sh`, shellcheck, `bash -n`, and markdownlint per the Acceptance Criteria above.

## Module Boundaries

N/A — a single self-contained skill directory; the only cross-skill interaction (delegating to `ywc-review-learnings`) is a documented skill invocation, not a code-level API surface.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Performance | The batch fetch must respect a caller-supplied bound (`--limit` or `--since`); no default unbounded scan (see FR-1) — protects against excessive `gh api` calls / rate-limit exhaustion on large repos. |
| Security | The bot-login allowlist regex must be anchored (`^(coderabbitai\|coderabbit\|codex\|claude\|anthropic\|github-actions)$`-equivalent, not a bare substring match) — carried over from the upstream fix in commit `93129bd`, which explicitly anchored this to prevent a crafted login from matching loosely; the anchoring discipline applies regardless of which regex value is used (see Scope's Bot-login allowlist decision). |
| Reliability | `gh api` failures must propagate (non-zero exit), not be swallowed with `|| true` — carried over from the same upstream fix. |
| Auditability | The report surface (FR-6) is never omitted, matching the existing `(none)`-not-omitted convention in `ywc-impl-review/SKILL.md:178`. |

## Critical Surfaces

N/A — no auth, payment, PII, or secret-handling surface. The skill reads public/repo-scoped PR review-comment metadata via `gh api` (already-authenticated CLI context) and writes only through the existing confirmation-gated `ywc-review-learnings` path.

## Data Model

N/A — no persistent schema. Output is transient NDJSON (fetch stage) and a promotion candidate list consumed interactively by `ywc-review-learnings`; the only durable artifact is `docs/review-learnings.md`, whose format `ywc-review-learnings` already owns and this port does not change.

## API Contract

N/A — no HTTP surface. The only external interface is the `gh` CLI (already a dependency of `ywc-review-learnings --source pr` and `ywc-create-pr`) and the skill's own CLI-style flags (`--limit`, `--since`, `--min-recurrence`) documented in `SKILL.md`.

## Edge Cases

- **Zero merged PRs in the selected window** → report `PRs scanned: 0`, no classes, no promotion candidates (not an error).
- **A PR has bot comments but no human reply/resolution on any of them** → all comments classified "skip" for that PR; the PR still counts toward `PRs scanned` but contributes no classified evidence.
- **A defect class recurs across exactly `--min-recurrence` PRs (boundary)** → promoted (inclusive: `count >= --min-recurrence`, matching the upstream default's own "3 or more" framing).
- **The same defect class was already captured as an active learning in `docs/review-learnings.md`** → `ywc-review-learnings`'s own existing dedupe/skip behavior for already-captured learnings applies unchanged (`capture-sources.md` `--source review` step 4's "skip a finding that is already captured" principle carries over structurally); this skill does not re-implement that check.
- **`gh` is unauthenticated or rate-limited mid-sweep** → the fetch script propagates the `gh api` failure (NFR: Reliability) rather than silently returning partial/empty results as if the window were genuinely empty.

## Open Questions

N/A — none identified. The one architectural fork (cross-project catalog vs. project-local-only routing) is resolved in Scope/Out of Scope above based on this repo's current `recurring-defects.md` being read-only; revisit only if a future request explicitly asks to build the append-only sink.

## Skill-Authoring Precedent

- `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh` and `detect-ci-commands.sh` are the in-repo precedent for skill-local script style (`#!/usr/bin/env bash`, usage header comment, `set -uo pipefail` or `set -euo pipefail`, explicit numbered exit codes) — `fetch-bulk-review-comments.sh` should match this style rather than introducing a new one.

## Amendment Log

### Iteration 1 — 2026-09-09

**Driven by**: DONE_WITH_CONCERNS, gate 91/100 (PROCEED band, Critical present), 1/1/1 findings
**Signatures**: `completeness:precedent-site-coverage-omits-two-bot-fetch-sites`, `consistency:bot-login-regex-not-reconciled-across-sites`

> Resolved the Critical by enumerating all 3 pre-existing bot-comment-fetch sites (not just 1) and deciding the new script adopts the broader shared regex from `poll-pr-reviews.sh` rather than the narrower `capture-sources.md` one, kept inline per existing per-site convention (no new shared-constant abstraction). The duplicate-claim sweep then reconciled every other place in the document that had asserted "reuses the exact/same query as `capture-sources.md`" verbatim, since that claim was only true for the query *shape*, not the login regex, after this decision.

| Section edited | What changed | Why |
|---|---|---|
| `## Scope` | Added a "Bot-login allowlist" bullet deciding the new script uses the broader `poll-pr-reviews.sh` regex, kept inline (not a shared constant), with rationale | Critical: precedent-site coverage gap; Warning: regex-sharing decision was unstated |
| `## Existing Constraints Touched` | Added 2 rows: `claude-code/skills/scripts/poll-pr-reviews.sh` + `references/pr-bot-polling.md`, and `claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-nitpick-comments.sh`; reworded the `capture-sources.md` row's "New code's interaction" cell from "Reuse verbatim" to "Reuse the query shape... verbatim, the login filter itself is widened" | Critical: these 2 sites were omitted from the precedent-site enumeration entirely |
| `## Scope` (bullet: skill fetches bot review comments) | Changed "reusing the exact `gh api` bot-login query pattern" to "reusing the query shape... with the broader bot-login regex decided below" | n/a — additive clarification, but corrects an implied claim ("exact"/"same") the Bot-login allowlist decision now contradicts |
| `## Existing Constraints Touched` (`capture-sources.md` row) | "Reuse verbatim" → "Reuse the query shape... verbatim... not reused verbatim" for the login filter | Duplicate-claim sweep: same fact as the Scope bullet edit, restated here |
| `## Functional Requirements` (FR-2) | "using the same `gh api --paginate` query as `ywc-review-learnings`'s `--source pr` path" → "using the same... query shape... (with the broader bot-login regex...)" | Duplicate-claim sweep: FR-2 restated the pre-amendment "same query" claim |
| `## Non-Functional Requirements` (Security row) | Anchored-regex example updated from the narrow `^(coderabbitai|chatgpt-codex|github-actions)$` to the broader `^(coderabbitai|coderabbit|codex|claude|anthropic|github-actions)$`, with a note that anchoring discipline applies regardless of which regex value is used | Duplicate-claim sweep: this row cited the old regex value as its worked example |
