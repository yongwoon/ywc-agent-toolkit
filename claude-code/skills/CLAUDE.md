# Skills Directory — Project Instructions

## Writing Rules

- `README.md` — written in Korean
- `README.[LOCALE].md` — written in the corresponding locale language
- All other files — written in English

## Language Policy for Localized Documentation

When writing or updating localized documentation (README files), follow the language policy for the target locale below. All non-README file bodies must be written entirely in English regardless of locale. Skill frontmatter `description` trigger phrases are the narrow exception: keep Korean/Japanese trigger examples when they are required for activation quality.

### Korean (`README.md`)

- Write prose in Korean
- Preserve English for all technical terms — do not transliterate into Hangul

| Correct | Incorrect |
|---|---|
| Database 연결 설정 | 데이터베이스 연결 설정 |
| API Endpoint 구현 | API 엔드포인트 구현 |
| Cache Directory 관리 | 캐시 디렉토리 관리 |
| Backend Service Logic | 백엔드 서비스 로직 |

### Japanese (`README.ja.md`)

- Write prose in Japanese
- Preserve English for all technical terms — do not transliterate into Katakana

| Correct | Incorrect |
|---|---|
| Database connection 設定 | データベースコネクション設定 |
| API Endpoint 実装 | API エンドポイント実装 |
| Cache Directory 管理 | キャッシュディレクトリ管理 |
| Backend Service Logic | バックエンドサービスロジック |

## Technical Terms (Keep in English)

The following terms must remain in English across all locales:

- **Infrastructure**: API, Backend, Frontend, Database, Cache, Service, Repository
- **Architecture**: Application, Component, Module, Framework, Library
- **Communication**: Request, Response, Schema, Model, Controller
- **Workflow**: Test, Debug, Deploy, Build, Configuration
- **Runtime**: Docker, Container, Server, Client, Router, Middleware
- **AI/LLM**: Agent, Prompt, Token, Context, Skill, Subagent

## Authoring or Restructuring `ywc-*` Skills

When creating a new `ywc-*` skill or modifying an existing skill's structure
(frontmatter, body sections, references), **invoke `ywc-skill-author` first**.

`ywc-skill-author` encodes the canonical rules derived from the 18 production
`ywc-*` skills:

- Frontmatter format (description must start with `(ywc) Use when...` and end
  with `Do not use for ...` anti-triggers; multilingual triggers required)
- Body structure (`**Announce at start:**` line, `## Rationalization Defense`
  table with ≥5 domain-specific Excuse / Reality pairs)
- Filesystem (full README locale set: `.md`, `.en.md`, `.ja.md`, `.ko.md`;
  long sections >30 lines extracted to `references/`)
- Anti-patterns (workflow-summary descriptions, stub code, `@` cross-references,
  vague language without thresholds)

For ad-hoc minor edits (typo fix, link correction), follow the existing skill's
patterns in the same directory without invoking the meta-skill.

For details, see `ywc-skill-author/SKILL.md` and the four reference documents
under `ywc-skill-author/references/`.

## Bot Review Polling Parameters

Skills that integrate with automated PR review bots (CodeRabbit, Codex Review,
Claude Review) must use the canonical polling procedure defined in
`references/pr-bot-polling.md`. Do not inline or approximate this logic in a
SKILL.md body.

Key parameters (canonical source is the reference file — do not hardcode these
values in skill bodies):

- **Initial wait**: 60 seconds after CI passes before the first poll (bots begin
  analysis only after CI completes)
- **Polling window**: 300 seconds (10 attempts × 30 s)
- **Merge condition**: `BOT_COUNT == 0` after the full window → proceed; `BOT_COUNT > 0` → invoke `ywc-handle-pr-reviews`

Skills must reference the file with an explicit `> **Action required**: Read
[references/pr-bot-polling.md]` directive, not a bare hyperlink, so the LLM
actually reads the canonical parameters rather than inferring them.

**Execution shape (enforced in the reference file)**: The polling loop must run
as a **single Bash call** using the `until` pattern — never split into per-iteration
calls. `sleep N && gh pr view` as a standalone call is blocked by Claude Code's
PreToolUse hook. The initial 60-second wait is embedded inside the loop's first
iteration (not a leading standalone `sleep 60`) to avoid the "long leading sleep"
block.

## PR Conflict & Merge-Readiness Resolution

Skills that create, update, or merge a PR (`ywc-create-pr`, `ywc-handle-pr-reviews`,
`ywc-finish-branch`, `ywc-parallel-executor`) must use the canonical conflict
procedure defined in `references/pr-conflict-resolution.md`. Do not inline or
approximate this logic in a SKILL.md body — reference it with an explicit
`> **Action required**: Read [references/pr-conflict-resolution.md]` directive
the same way `pr-bot-polling.md` is referenced.

The reference codifies two facts that are easy to miss:

- **CI status and merge-readiness are independent gates.** A PR can pass CI and
  still be `CONFLICTING` against the base if the base advanced. Always check
  `gh pr view --json mergeable,mergeStateStatus` before declaring a PR done or
  calling `gh pr merge`.
- **Resolve a PR-vs-base conflict by merging the base INTO the feature branch,
  never by rebasing.** Rebasing rewrites commit SHAs and orphans existing PR
  review threads; merging (`git merge --no-ff origin/<base>`) preserves both.

Real textual conflicts are a 1-attempt, surface-to-user (`BLOCKED`) situation —
never auto-resolve, never force-push, never `git merge --abort`. A merely-behind
branch is auto-updated and CI re-verified (up to 2 cycles, matching the CI
fix-loop budget).

## Skill Invocation Syntax

Skills in `tools/claude-code/skills/` are Claude Code skills. Use `/skill-name` (slash command) syntax in all documentation and examples — never `$skill-name`, which is the Codex CLI format.

| Correct (Claude Code) | Incorrect (Codex) |
|---|---|
| `/ywc-commit` | `Use $ywc-commit to ...` |
| `/ywc-create-pr` | `Use $ywc-create-pr to ...` |
| `/ywc-finish-branch` | `Use $ywc-finish-branch to ...` |

Skills are also auto-triggered by natural language phrases listed in each skill's `description` frontmatter field.

## Calling `ywc-create-pr` from Other Skills

Skills that delegate PR creation to `ywc-create-pr` must pass `--title` explicitly
when they have a pre-constructed title (e.g., the `[task-id] description` format
in `ywc-finish-branch`). Without `--title`, `ywc-create-pr` generates its own title
from `git log` and the caller's intended prefix is silently discarded.

Required arguments when delegating:

```
ywc-create-pr --title "<pre-constructed title>" --lang <lang> --base-branch <branch>
```

Do not rely on `ywc-create-pr`'s internal title generation when the calling skill
owns the title format.

**Skipping post-CI check**: Pass `--skip-post-ci-check` when the calling skill
handles remote CI verification and bot review independently (e.g., `ywc-finish-branch`
runs its own Step 4 CI check after PR creation). Without this flag, `ywc-create-pr`
runs Step 8 (Remote CI & Bot Review Check) automatically, which would double-check
CI and bots that the caller will already cover.

**Skipping ubiquitous-language update**: Pass `--skip-ubiquitous-update` when the
calling skill has already invoked `ywc-ubiquitous-language --mode update` (e.g.,
`ywc-finish-branch` Step 1.5). `ywc-create-pr`'s Step 0.5 will then no-op,
preventing the same incremental update from running twice in one PR creation flow.

## Calling `ywc-commit` from Other Skills

`ywc-commit` runs `ywc-ubiquitous-language --mode update` in its own Step 0.5
when `docs/ubiquitous-language.md` exists. Skills that delegate commits to
`ywc-commit` and have already performed the UL update upstream must pass
`--skip-ubiquitous-update` to prevent double invocation. This is the same
propagation pattern used between `ywc-finish-branch` → `ywc-create-pr`.

Required form when delegating from a skill that already ran the UL update:

```
ywc-commit --skip-ubiquitous-update
```

Canonical propagation chains:

- `ywc-finish-branch` (Step 1.5 runs UL update) → `ywc-create-pr` (`--skip-ubiquitous-update`) → `ywc-commit` (`--skip-ubiquitous-update`)
- `ywc-create-pr` (Step 0.5 runs UL update) → `ywc-commit` (`--skip-ubiquitous-update`)
- Direct user invocation of `/ywc-commit` → Step 0.5 runs UL update itself, no flag needed

The flag must be forwarded explicitly in every delegation. Inferring it from
context is unsafe because the call site may not know whether the upstream
caller performed the update — explicit propagation makes the contract auditable.

## Subagent Return Payload Contract and Structured Surface-to-User

Skills that dispatch subagents via the Task tool (fan-out skills:
`ywc-code-gen`, `ywc-impl-review`, `ywc-parallel-executor`,
`ywc-sequential-executor`, `ywc-spec-validate`, `ywc-task-generator`) follow
two contracts defined in `references/subagent-status-actions.md`:

**Return payload (§3.5)** — every subagent prompt must include a directive
constraining the return to: `Status | 1-line summary | artifact paths |
(Concerns ≤ 10 lines | Blocker ≤ 5 lines | Missing-context bullets)`.
Generated code, full findings, full diffs, restated prompts, and
chain-of-thought go to files; only paths come back. Without this contract,
3+ verbose returns per fan-out phase saturate the orchestrator's main
context within one or two waves.

**Structured surface-to-user (§4 step 4)** — when BLOCKED Triage routes to
"Plan problem", the orchestrator surfaces with three required elements
(attempted triage steps + verbatim blocker + proposed default action), not
as a bare halt. Generic "halted, awaiting input" surfaces are a regression.

New fan-out skills must link `references/subagent-status-actions.md` and
inject the §3.5 directive verbatim into each subagent prompt.

## Bundled Execution Scripts

Several `ywc-*` skills ship bundled scripts for deterministic or repetitive
operations. Scripts execute without loading their body into LLM context — use
them instead of inlining equivalent logic in SKILL.md bodies.

| Script | Skill | Purpose |
|---|---|---|
| `scripts/poll-pr-reviews.sh <pr>` | shared | Bot-polling loop; exit 0 = bots found, exit 1 = no bots |
| `ywc-create-pr/scripts/scan-secrets.sh --staged \| --committed <base>` | ywc-create-pr | 3-phase secret scan; exit 0 = clean, exit 1 = found |
| `ywc-finish-branch/scripts/build-pr-title.py <task> [--format parts\|title]` | ywc-finish-branch | task-name → TASK_NUMBER + SLUG_EN; 4 regex patterns incl. flexible N-M and single-prefix fallbacks |
| `ywc-sequential-executor/scripts/verify-transition.sh <base> <task> [dir]` | ywc-sequential-executor | 4-condition pre-transition check; exit 0 = PASS |
| `ywc-worktrees/scripts/cleanup-worktree.sh [--root <path>] [--branch <branch>] [--force] <task>` | ywc-worktrees | Worktree cleanup + safe local branch delete; exit 0 = PASS (moved from ywc-parallel-executor in Sprint 22) |
| `ywc-worktrees/scripts/audit-worktrees.sh [--root <path>] [--prune] [--expect <tasks>]` | ywc-worktrees | Pre-flight/wave-end worktree audit; exit 0 = clean, exit 1 = findings (moved from ywc-parallel-executor in Sprint 22) |
| `ywc-docker-isolate/scripts/setup-docker-ports.sh --task-name <t> --worktree-path <dir> [--compose-file <f>] [--port-vars V1,V2]` | ywc-docker-isolate | Derive deterministic per-worktree Docker host-port block + write worktree-local env-file/`.ywc-docker-ports`; exit 0 = isolated/no-op, 1 = hardcoded/squatter/corrupt |
| `ywc-docker-isolate/scripts/teardown-docker.sh (--task-name <t> \| --project-name <p>) --worktree-path <dir> [--keep-volumes]` | ywc-docker-isolate | Tear down only this worktree's stack (`down --volumes` default), delete persist on success; exit 0 = ok, 1 = LEAKED/SANITIZE_ERROR |
| `ywc-docker-isolate/scripts/audit-docker-stacks.sh --expect <t1,t2,...> [--prune]` | ywc-docker-isolate | Report residual `ywc-<task>` stacks via stdout non-empty; exit ALWAYS 0; `--prune` tears them down |
| `ywc-handle-pr-reviews/scripts/fetch-unresolved-comments.sh <repo> <pr>` | ywc-handle-pr-reviews | Paginated comment fetch + thread filtering; exit 0 = JSON array |
| `ywc-release-pr-list/scripts/fetch-pr-metadata.sh <pr> [<pr> ...]` | ywc-release-pr-list | Batch PR metadata (author, title, summary, state); NDJSON output |
| `ywc-merge-dependabot/scripts/group-by-ecosystem.py <pr> [<pr> ...]` | ywc-merge-dependabot | Classify Dependabot PRs by lockfile ecosystem (npm / github-actions / python / go / cargo / maven / gradle / docker / mixed); JSON output; powers parallel-auto mode grouping |
| `ywc-merge-dependabot/scripts/detect-major-bump.py --title <t> \| (stdin)` | ywc-merge-dependabot | Deterministic "leftmost non-zero segment" semver major-bump gate; NDJSON output; `major_bump: true\|false\|null` (null = undecidable, LLM falls back) |
| `ywc-release-pr-list/scripts/extract-merged-prs.sh [--exclude <pr>]` | ywc-release-pr-list | Pure-text extraction of merged PR numbers from commit headlines (2 anchored patterns only); dedup + ascending sort; no network |
| `ywc-confidence-gate/scripts/score-gate.py --scope N --architecture N --evidence N --reuse N --root-cause N` | ywc-confidence-gate | Weighted aggregate + band (PROCEED/REVIEW/STOP) + single-dim ≤50 override; JSON output |

All paths are relative to the repository root. When authoring a new `ywc-*`
skill that needs deterministic parsing or a bounded wait loop, add a script
to `<skill>/scripts/` and reference it with a one-line Bash invocation in the
SKILL.md body rather than describing the logic inline.

## HTML Output Mode

Nine review and report skills (`ywc-impl-review`, `ywc-security-audit`,
`ywc-spec-validate`, `ywc-tech-research`, `ywc-incident-postmortem`,
`ywc-product-review`, `ywc-ui-ux-review`, `ywc-gen-testcase`,
`ywc-design-renew`) support an opt-in `--format html` flag that emits a
self-contained HTML report instead of Markdown. The canonical convention — single-file rule, severity color
tokens, document structure, and the embedded `Copy as Markdown` surface — is
defined in `references/html-output.md`.

Rules for skills that adopt this mode:

- The default must stay `markdown`. HTML output costs 2–4× the output tokens,
  so it is opt-in, not a new default.
- Do not inline the HTML skeleton or conventions in a SKILL.md body — link
  `references/html-output.md` with a one-line pointer, the same way
  `pr-bot-polling.md` is referenced.
- `references/html-output.md` is a top-level shared reference. The skill roots
  are maintained independently (no auto-sync); if the codex bundle needs the
  same convention, copy it to `tools/codex-skill/skills/references/` by hand.
- Never apply HTML output to version-controlled canonical documents
  (`docs/specification/`, `tasks/`, CHANGELOG, the ubiquitous-language
  glossary) — HTML diff noise outweighs the benefit. Those skills do not
  expose `--format`.

When authoring a new review or report skill whose output a human reads to
make a decision, add the `--format` flag and the `html-output.md` pointer
following the eight skills above.

## Shared Schema Guide (DB invariants)

Database schema design, review, and migration guidance is centralized in the
top-level shared reference set `references/schema/`. It is the single source of
truth for any skill that plans, generates, executes, or reviews a schema change
— do not re-state schema invariants inline in a SKILL.md body.

- **`references/schema/core.md`** — stack-agnostic. Part A (design principles:
  naming, normalization, expand→migrate→contract evolution, reversibility,
  indexing), Part B (eight mechanical invariants that fail deterministically when
  omitted), Part C (the review checklist). This is the entry point; read it first.
- **`references/schema/<stack>.md`** — per-stack syntax for Part B's eight
  invariants plus stack-specific traps. Current stacks: `prisma.md`, `sql-ddl.md`
  (raw Postgres DDL), `drizzle.md`, `typeorm.md`.

Five skills point here at their schema touchpoints: `ywc-plan` (Data Model draft
+ Step 4b.5 Pass C), `ywc-task-generator` (Database Migration Separation),
`ywc-sequential-executor` (Step 3 schema-aware implementation), `ywc-code-gen`
(Backend subagent dispatch), and `ywc-impl-review` (Architecture subagent). Each
uses an inline `[../references/schema/core.md]` pointer that names "read core,
then the stack file matching the project".

**Adding a new stack** is the whole maintenance contract: create one
`references/schema/<stack>.md`, translate Part B's eight invariants into that
stack's syntax, link it in the `core.md` table, and stop. Do not duplicate Part A
— link back to it. Principles change in one place (`core.md`); only syntax files
grow. This split is what keeps the guide maintainable and extensible.

As with the other top-level shared references, the skill roots are maintained
independently — the codex bundle keeps its own schema guidance and is not
auto-synced; port deliberately if a shared change is wanted there.

## Codex-skill: Maintained Independently

`tools/codex-skill/skills/` and `tools/claude-code/skills/` are **no longer
auto-synced**. The former `sync-skills.sh` pre-commit hook and the
`tools/pi-skills` root were removed; each root is now edited independently. When
a change applies to both runtimes, apply it to each root deliberately — nothing
propagates edits automatically, and there is no obligation to mirror a
claude-code edit into codex-skill.

Several codex-skill files carry intentional, runtime-specific divergence from
their claude-code counterparts. They are listed here for awareness when a shared
change is ported by hand:

- **`ywc-onboard-repo`** — codex variant emits **AGENTS.md** (Codex CLI
  convention) instead of CLAUDE.md, including `references/agents-md-starter.md`
  (renamed from `claude-md-starter.md`) and `agents/openai.yaml`.
- **`ywc-release-pr-list`** — codex variant resolves bundled scripts from
  `${CODEX_HOME:-$HOME/.codex}/skills/...` instead of the source tree, so the
  installed Codex copy works outside this repository.
- **`ywc-code-gen` / `ywc-parallel-executor` / `ywc-sequential-executor` /
  `ywc-agentic`** — claude-code variants carry named `subagent_type` dispatch
  (`ywc-backend-coder` / `ywc-frontend-coder` / `ywc-qa-engineer`) and Status
  Routing tables that resolve only against the claude-code agent catalog at
  `tools/claude-code/agents/`. The codex variants keep generic worker prose.
  The codex `ywc-code-gen` layer-role references also use `*-generation.md`
  filenames where claude-code uses `*-agent.md`.
- **`ywc-impl-review`** — both carry the 5-aspect shape (architecture / design /
  devex / security / QA); claude-code uses model-explicit Task-tool dispatch,
  codex uses Codex worker/advisor terminology without `model:` fields.
- **`ywc-spec-validate`** — shared 4-dimension model + Step 3.5
  (Precedent-Completeness Re-grounding) obligation; codex uses Codex terminology
  (`AGENTS.md`, `$`-prefixed commands, `rg`-first search) without `model:` fields.

The claude-code agent catalog at `tools/claude-code/agents/` is claude-code only
— Codex CLI has no equivalent named-dispatch agent catalog.
