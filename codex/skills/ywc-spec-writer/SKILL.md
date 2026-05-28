---
name: ywc-spec-writer
description: (ywc) Use when creating or updating a project specification (사양서) in docs/specification/, including task-range and PR-based incremental updates. Triggers: "spec 작성", "사양서 작성", "사양서 업데이트", "task 로 사양서 갱신", "PR 로 사양서 갱신", "여러 PR 로 사양서 갱신", "specification 작성", "프로젝트 사양", "전체 사양서", "write spec", "generate specification", "update spec from task range", "update spec from PRs", "project spec", "仕様書作成", "仕様書更新", "タスク範囲から仕様書更新", "PRから仕様書更新", "スペック作成", "ywc-spec-writer". Do not use for spec quality review (use ywc-spec-validate), task decomposition from a finalized spec (use ywc-task-generator), or pre-implementation planning without a spec intent (use ywc-plan).
---

# ywc-spec-writer

**Announce at start:** "I'm using the ywc-spec-writer skill to create or update the project specification in docs/specification/."

Writes and maintains the `docs/specification/` directory. Produces human-readable markdown describing the project's goals, features, data model, user flows, and non-functional requirements — with **no program code**. Intended audience: developers and non-developers alike. Supports Korean, Japanese, and English output.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "This is a minor change — I'll update inline without reading existing spec files" | Always read existing spec files before writing. Editing without reading overwrites valid content silently. |
| "A code snippet would make this feature clearer" | Zero program code in any spec output. Non-developer audience cannot parse code. Use user stories and flow descriptions instead. |
| "User seems to want a full spec — I'll generate it without `--full` to save time" | Full generation requires the explicit `--full` flag AND user confirmation. Never auto-generate the full spec from an incremental run. |
| "The commit changed several files — I'll update the entire spec to be safe" | Update only sections mapped to the changed domain. Use `scripts/detect-affected-sections.sh` to determine scope precisely. |
| "Language not specified — I'll default to English" | Default is Korean (`ko`) unless project guidance files (`AGENTS.md`, `CODEX.md`, `CLAUDE.md`) or `--lang` say otherwise. |
| "`--setup-hook` is optional — I'll just describe the hook approach" | `--setup-hook` must produce a working script at `tools/scripts/spec-update-hook.sh` and install it. Documentation alone does not fulfill the step. |
| "Multiple PRs share files — I'll skip deduplication" | Always dedupe the union file list before invoking section detection. Without dedup, the same diff is fed to the LLM multiple times and bloats context. |
| "Open PR diff will change soon — recording the HEAD SHA in README index is unnecessary" | Always record `headRefOid` (and PR numbers) in the README index entry. Without it, a future reader cannot reproduce or audit which PR snapshot drove the update. |
| "The task range or PR set touched >4 sections — I'll patch them all anyway" | Stop and propose `--update` (Full Refresh) explicitly. Spec changes at that scope are coherent only when written holistically; patching pieces creates internal drift. |
| "Range spans phase boundary — I'll silently combine them" | Phase boundaries are hard gates in `ywc-task-generator`. When a range crosses phases, the README index entry must list every resolved task ID so the audit trail survives. |

**Violating the letter of these rules is violating the spirit.** A spec containing code, written in the wrong language, or auto-generated without explicit intent does not serve its readers.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--full` | flag | `--full` | Generate complete spec from scratch. Requires user confirmation. Uses best available model. |
| `--update` | flag | `--update` | Regenerate all existing spec sections. |
| `--from-task` | `--from-task <path>` | `--from-task tasks/000002-010-api-user/` | Update spec from a single ywc-task-generator task directory. |
| `--from-tasks` | `--from-tasks <id-or-pattern> [<id-or-pattern> ...]` | `--from-tasks 000002-010..000003-020` | Update spec from a range, glob, or multi-id set of task directories. Patterns: single ID prefix, `START..END` range, quoted shell glob, or multi-value list. Active and completed tasks both resolve. |
| `--from-commit` | `--from-commit <ref>` | `--from-commit HEAD` | Update spec based on diff of a specific commit. |
| `--from-pr` | `--from-pr <num>` | `--from-pr 42` | Update spec from a single pull request's diff. Requires `gh` CLI auth. |
| `--from-prs` | `--from-prs <num> [<num> ...]` | `--from-prs 42 43 51` | Update spec from the union diff of multiple PRs. Each PR fetched via `gh pr diff`; duplicate files are coalesced. |
| `--setup-hook` | flag | `--setup-hook` | Install git hook for automatic spec-update tracking. |
| `--lang` | `--lang ko\|ja\|en` | `--lang ja` | Output language. Default: `ko`. |

## Workflow

### Step 1: Determine Mode

| Mode | Trigger | Notes |
|------|---------|-------|
| **Full Generation** | `--full` | Requires user confirmation. Uses best model. |
| **Full Refresh** | `--update` | Regenerates all existing sections. |
| **Task-based Update** | `--from-task <path>` | Maps a single task's category to affected sections. |
| **Task Range Update** | `--from-tasks <id-or-pattern> ...` | Resolves IDs / ranges / globs via `scripts/resolve-task-paths.sh`; unions each task's category mapping. |
| **Commit-based Update** | `--from-commit <ref>` | Analyzes git diff to determine affected sections. |
| **PR-based Update** | `--from-pr <num>` / `--from-prs <num> ...` | Fetches changed files via `scripts/collect-files-from-prs.sh` (gh CLI); unions across PRs; uses PR title + body as narrative context. |
| **Auto** | No flags | Reads last commit diff; runs commit-based update. |

### Step 2: Collect Context

**Always read before writing:**
- `docs/specification/README.md` — current spec state (if exists)
- `AGENTS.md`, `CODEX.md`, `CLAUDE.md` — language policy, domain conventions (read whichever exist, nearest file first)
- `docs/ubiquitous-language.md` (if exists) — canonical terms; use these verbatim in spec text

**For `--full` and `--update` only**, also read:
- Project directory structure (top 2 levels of `src/`, `app/`, or equivalent)
- `docs/ywc-plans/` — existing feature plans
- Key structural files: schema, API route index, main domain directories

### Step 3: Language Setup

If `--lang` is not specified, check project guidance files (`AGENTS.md`, `CODEX.md`, `CLAUDE.md`) for a declared primary documentation language. If not found there either, use Korean (`ko`) as the default. Ask the user only when they explicitly ask to choose a language or project guidance conflicts.

> "사양서를 어떤 언어로 작성할까요? / Which language should the spec be written in? / 仕様書をどの言語で作成しますか？"
> 1. 한국어 (ko) — 기본값
> 2. English (en)
> 3. 日本語 (ja)

When asking, wait for the user's answer before proceeding.

For locale-specific writing rules (formality level, term policy), see [references/language-policy.md](references/language-policy.md).

### Step 4: Prepare Spec Directory

If `docs/specification/` does not exist, run:

```bash
bash codex/skills/ywc-spec-writer/scripts/init-spec-structure.sh <lang> "<ProjectName>"
```

This creates the 7-section skeleton without any LLM calls. For the full section layout and writing templates, see [references/spec-structure.md](references/spec-structure.md).

### Step 5: Determine Affected Sections

For incremental modes, identify which spec sections need updating before writing. Run the appropriate branch then **union** every detected section across sources.

**Commit-based**

```bash
git diff <ref>^..<ref> --name-only \
  | bash codex/skills/ywc-spec-writer/scripts/detect-affected-sections.sh
```

**Task-based (single task)** — read the task `README.md` for its `category` field and apply the mapping in [references/section-mapping.md](references/section-mapping.md).

**Task Range / Multi-task** — resolve task IDs, then read each task's `README.md` for its `category` field:

```bash
# Resolve range / glob / multi-id to absolute task directory paths
bash codex/skills/ywc-spec-writer/scripts/resolve-task-paths.sh \
  000002-010..000003-020

# Quote glob patterns so the user's shell does not expand or reject them first.
bash codex/skills/ywc-spec-writer/scripts/resolve-task-paths.sh \
  '000002-*'

# For each resolved path: read README.md → category → look up in section-mapping.md
# Then UNION every resulting section list.
```

**PR-based (single or multiple PRs)** — fetch the changed-file union, then feed it into `detect-affected-sections.sh`:

```bash
bash codex/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh 42 43 51 \
  | bash codex/skills/ywc-spec-writer/scripts/detect-affected-sections.sh
```

Additionally, for `--from-pr` / `--from-prs`, fetch each PR's title + body as narrative context:

```bash
gh pr view <num> --json number,title,body,headRefOid
```

Use the PR's `title` + `body` to inform spec wording (the "why") and record `headRefOid` in the README change log entry for reproducibility.

**Safety threshold** — if the unioned section count exceeds **4**, stop and propose `--update` (Full Refresh) to the user. Patching that many sections piecemeal produces internal drift; see [references/section-mapping.md](references/section-mapping.md) §"When Many Sections Are Affected".

### Step 6: Write or Update Spec Content

**Non-negotiable writing rules for all modes:**
- Zero program code in any spec output
- Write for a business stakeholder, not a developer
- Features use the user story format: "As a [user], I want [action] so that [benefit]"
- Data and flows use plain-language descriptions
- Keep each section file ≤ 400 lines

For per-section writing templates, see [references/spec-structure.md](references/spec-structure.md).

For **Full Generation**, follow the detailed analysis steps in [references/full-gen-workflow.md](references/full-gen-workflow.md). Use the most capable available reasoning model.

### Step 7: Update README Index

After every write, update `docs/specification/README.md`:
- Set `**Last updated**` to today's date
- Append a row in this format: `| YYYY-MM-DD | <section(s)> | <source> | <one-line summary> |`

The `<source>` column captures provenance so future readers can trace the spec change back to its driver:

| Mode | `<source>` example |
|------|--------------------|
| Full Generation / Refresh | `--full` or `--update` |
| Commit-based | `commit <short-sha>` |
| Task-based (single) | `task 000002-010-api-user` |
| Task Range / Multi | `tasks 000002-010..000003-020 (3 tasks)` — list every resolved ID inline or in a sub-bullet when >5 |
| PR-based (single) | `PR #42 @ <headRefOid-short>` |
| PR-based (multi) | `PRs #42, #43, #51 @ <headRefOid-short each>` |

### Step 8: Hook Setup (if `--setup-hook`)

See [references/hook-setup.md](references/hook-setup.md) for the full installation procedure. The hook creates a `.spec-update-pending` marker on commits with significant code changes, keeping LLM calls out of the git hook itself.

## Output Format

```text
✅ Spec updated: docs/specification/
  Modified: 02-features.md, 03-data.md
  Unchanged: 01-overview.md, 04-interfaces.md, 05-user-flows.md, 06-requirements.md, 07-glossary.md
  Index updated: docs/specification/README.md
```

For Task Range / Multi:

```text
✅ Spec updated: docs/specification/
  Source: tasks 000002-010..000003-020 (4 tasks)
    - 000002-010-api-user
    - 000002-020-api-auth
    - 000003-010-domain-billing
    - 000003-020-domain-invoice
  Modified: 02-features.md, 03-data.md, 04-interfaces.md
  Index updated: docs/specification/README.md
```

For PR-based (single or multi):

```text
✅ Spec updated: docs/specification/
  Source: PRs #42 @ a1b2c3d, #43 @ e4f5g6h
  Modified: 02-features.md, 04-interfaces.md
  Index updated: docs/specification/README.md
```

For Full Generation / Full Refresh:

```text
✅ Spec generated: docs/specification/
  Created: README.md, 01-overview.md, 02-features.md, 03-data.md,
           04-interfaces.md, 05-user-flows.md, 06-requirements.md, 07-glossary.md
  Model: most capable available reasoning model
  Language: Korean (ko)
```

## Validation

Before declaring the skill's task complete:

- [ ] Zero program code in any generated spec file
- [ ] Language matches `--lang` option or default `ko`
- [ ] For incremental modes: only affected sections updated
- [ ] `docs/specification/README.md` change log updated with today's date
- [ ] Change log row includes the `<source>` column (mode + identifier per Step 7 table)
- [ ] For Task Range / Multi: every resolved task ID is listed (inline or sub-bullet)
- [ ] For PR-based: every PR number and its `headRefOid` short SHA recorded
- [ ] If unioned affected sections > 4: user explicitly confirmed continuing with incremental update instead of switching to `--update`
- [ ] All written sections have substantive content (no "To be written" placeholder remaining)
- [ ] Technical terms kept in English per language policy (not transliterated)

## Common Mistakes

- **Reading nothing before writing** — always read the existing spec and project guidance files first to avoid overwriting valid content or misusing domain terminology.
- **Including code in spec output** — even a one-line variable name breaks non-developer readability. Replace with flow descriptions or plain-language attribute lists.
- **Running full generation without `--full`** — unexpected long-running model calls surprise users. The explicit flag is the contract.
- **Skipping PR HEAD SHA capture** — for `--from-pr` / `--from-prs`, an open PR's diff can shift the next day. Without `headRefOid` in the change log, the spec update becomes un-reproducible.
- **Silently merging cross-phase task ranges** — when `--from-tasks` spans a phase boundary, list every resolved task ID in the change log. Combining them without enumeration hides the boundary crossing from audit.
- **Forgetting PR narrative context** — `gh pr diff` alone gives mechanical file changes; the PR title and body carry the "why". Spec writing without the narrative produces description-of-what instead of statement-of-intent text.

## Integration

- **Upstream**: `ywc-plan` (generates feature specs), `ywc-task-generator` (produces task docs for `--from-task` / `--from-tasks`), `ywc-create-pr` (produces PR artifacts consumed by `--from-pr` / `--from-prs`)
- **Downstream**: `ywc-spec-validate` (validates the written spec before task decomposition)
- **Pairs with**: `ywc-ubiquitous-language` (align spec vocabulary with canonical domain terms)
- **External dependency**: `gh` CLI must be installed and authenticated for `--from-pr` / `--from-prs`
