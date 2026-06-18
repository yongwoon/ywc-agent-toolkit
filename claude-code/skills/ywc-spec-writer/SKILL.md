---
name: ywc-spec-writer
version: 1.3.1
description: (ywc) Use when creating or updating a project specification (사양서) in docs/specification/, including task-range and PR-based incremental updates. Triggers: "spec 작성", "사양서 작성", "사양서 업데이트", "task 로 사양서 갱신", "PR 로 사양서 갱신", "여러 PR 로 사양서 갱신", "specification 작성", "프로젝트 사양", "전체 사양서", "write spec", "generate specification", "update spec from task range", "update spec from PRs", "project spec", "仕様書作成", "仕様書更新", "タスク範囲から仕様書更新", "PRから仕様書更新", "スペック作成", "ywc-spec-writer". Do not use for spec quality review (use ywc-spec-validate), task decomposition from a finalized spec (use ywc-task-generator), or pre-implementation planning without a spec intent (use ywc-plan).
category: spec
phase: planning
requires: []
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
| "Language not specified — I'll default to English" | Default is Korean (`ko`) unless the project's CLAUDE.md or `--lang` flag says otherwise. |
| "`--setup-hook` is optional — I'll just describe the hook approach" | `--setup-hook` must produce a working script at `tools/scripts/spec-update-hook.sh` and install it. Documentation alone does not fulfill the step. |
| "Multiple PRs share files — I'll skip deduplication" | Always dedupe the union file list before invoking section detection. Without dedup, the same diff is fed to the LLM multiple times and bloats context. |
| "Open PR diff will change soon — recording the HEAD SHA in README index is unnecessary" | Always record `headRefOid` (and PR numbers) in the README index entry. Without it, a future reader cannot reproduce or audit which PR snapshot drove the update. |
| "The task range or PR set touched >4 sections — I'll patch them all anyway" | Stop and propose `--update` (Full Refresh) explicitly. Spec changes at that scope are coherent only when written holistically; patching pieces creates internal drift. |
| "Range spans phase boundary — I'll silently combine them" | Phase boundaries are hard gates in `ywc-task-generator`. When a range crosses phases, the README index entry must list every resolved task ID so the audit trail survives. |
| "Spec is for business stakeholders, so keeping NFR numbers vague is fine" | Spec must be **dual-audience**: readable by business stakeholders AND decomposable by `ywc-task-generator`. NFR with placeholder values like "数秒以内" / "X seconds" fail downstream `ywc-spec-validate` and force a Re-plan iteration. Always extract concrete numbers from `*.constants.ts`, `*config*.ts`, migrations, or record them under Open Questions with rationale. |
| "Project has many models — I'll lump them into category groups" | Every model in `prisma/schema.prisma` (or equivalent ORM/DB schema) MUST appear by name in `03-data.md`. Lumping ≥3 sibling entities is permitted only as a `### <Family>` heading with an explicit inline list of all member names. Silent omission produces Code Compatibility Critical findings downstream. |
| "Token-efficiency rule says 'no open-ended exploration' — constants files are off-limits" | The "no open-ended exploration" rule has explicit **exceptions** documented in [references/full-gen-workflow.md](references/full-gen-workflow.md) §Exceptions: constants files, primary schema, feature directory listings, and auth guard / middleware definitions. These supply the concrete numbers and enumeration boundaries that `ywc-spec-validate` checks for. Skipping them produces vague NFRs and lumped entities. |
| "UL is for code-level naming, spec uses business language so it's OK" | `docs/ubiquitous-language.md` is the **canonical vocabulary for the entire project**, not just code. Synonyms-to-Avoid violations (e.g., using "Tenant Admin" when UL canonical is "Admin" with "Tenant Admin" listed as a synonym to avoid) propagate through every downstream artifact: tasks generated by `ywc-task-generator`, code authored by `ywc-backend-coder` / `ywc-frontend-coder`, and PR titles created by `ywc-create-pr`. Skipping the UL cross-check at spec-write time turns a 5-minute grep into a multi-PR rename refactor downstream. Always run the avoid-list extraction grep before drafting `01-overview.md`. |
| "Inline backticks are not code blocks, so a Prisma snippet in them is OK" | Inline backticks containing executable syntax (`@default(...)`, `dbgenerated(...)`, `WHERE x = $1`, decorators) are exactly the case `ywc-spec-validate` flags as a Code Compatibility Warning — the spec then drifts when the underlying ORM / SQL changes. Field-reference identifiers (`tenantId`, `BeaconSite.samplingState`) are fine; **expressions** are not. The mechanical test: "if I copy this backtick content into a `.prisma` / `.sql` file, would it parse?" If yes, paraphrase into plain prose. |

**Violating the letter of these rules is violating the spirit.** A spec containing code, written in the wrong language, or auto-generated without explicit intent does not serve its readers. A spec that cannot pass `ywc-spec-validate` at the REVIEW band (Gate ≥ 70) does not serve its **pipeline** — fix the gaps at write time, not at validate time.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--full` | flag | `--full` | Generate complete spec from scratch. Requires user confirmation. Uses best available model. |
| `--update` | flag | `--update` | Regenerate all existing spec sections. |
| `--from-task` | `--from-task <path>` | `--from-task tasks/000002-010-api-user/` | Update spec from a single ywc-task-generator task directory. |
| `--from-tasks` | `--from-tasks <id-or-pattern> [<id-or-pattern> ...]` | `--from-tasks 000002-010..000003-020` | Update spec from a range, glob, or multi-id set of task directories. Patterns: single ID prefix, `START..END` range, shell glob, or multi-value list. Active and completed tasks both resolve. |
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
- `CLAUDE.md` — language policy, domain conventions
- `docs/ubiquitous-language.md` (if exists) — canonical terms; use these verbatim in spec text

**For `--full` and `--update` only**, also read:
- Project directory structure (top 2 levels of `src/`, `app/`, or equivalent)
- `docs/ywc-plans/` — existing feature plans
- Key structural files: schema, API route index, main domain directories

### Step 3: Language Setup

If `--lang` is not specified, check the project's CLAUDE.md for a declared primary documentation language. If not found there either, use Korean (`ko`) as the default. Ask the user only when they explicitly ask to choose a language or the project guidance conflicts.

> "사양서를 어떤 언어로 작성할까요? / Which language should the spec be written in? / 仕様書をどの言語で作成しますか？"
> 1. 한국어 (ko) — 기본값
> 2. English (en)
> 3. 日本語 (ja)

When asking, wait for the user's answer before proceeding.

For locale-specific writing rules (formality level, term policy), see [references/language-policy.md](references/language-policy.md).

### Step 4: Prepare Spec Directory

If `docs/specification/` does not exist, run:

```bash
bash claude-code/skills/ywc-spec-writer/scripts/init-spec-structure.sh <lang> "<ProjectName>"
```

This creates the 7-section skeleton without any LLM calls. For the full section layout and writing templates, see [references/spec-structure.md](references/spec-structure.md).

### Step 5: Determine Affected Sections

For incremental modes, identify which spec sections need updating before writing. Run the appropriate branch then **union** every detected section across sources.

**Commit-based**

```bash
git diff <ref>^..<ref> --name-only \
  | bash claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh
```

**Task-based (single task)** — read the task `README.md` for its `category` field and apply the mapping in [references/section-mapping.md](references/section-mapping.md).

**Task Range / Multi-task** — resolve task IDs, then read each task's `README.md` for its `category` field:

```bash
# Resolve range / glob / multi-id to absolute task directory paths
bash claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh \
  000002-010..000003-020

# For each resolved path: read README.md → category → look up in section-mapping.md
# Then UNION every resulting section list.
```

**PR-based (single or multiple PRs)** — fetch the changed-file union, then feed it into `detect-affected-sections.sh`:

```bash
bash claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh 42 43 51 \
  | bash claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh
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
- When the source (task / PR / commit / design note) admits two readings that change the spec's meaning, record **both** under `## Open Questions` rather than silently picking one. A spec writer transcribes decided intent; it does not decide it. The silent pick is invisible until implementation contradicts the spec.
- Write for a **dual audience**: business stakeholder (must be readable without engineering knowledge) AND `ywc-task-generator` (must be decomposable into concrete tasks). Vague prose serves neither — concrete numbers serve both.
- Features use the user story format: "As a [user], I want [action] so that [benefit]"
- Data and flows use plain-language descriptions
- Section file size cap, scaled to project size:
  - Default: ≤ 400 lines per section file
  - When project has **>50 entities** (Prisma models / equivalent ORM models) OR **>20 features** (top-level feature directories): cap raises to ≤ 800 lines per section file
  - `03-data.md` may exceed the section cap by up to 30 lines per entity beyond 50 entities (e.g., 82 entities → cap = 400 + 30×32 = 1,360 lines), so enumeration is not artificially blocked by the cap

**Additional non-negotiable rules for `--full` and `--update` modes** (these modes claim to produce a complete spec, so they bear the full burden):

- Every NFR in `06-requirements.md` MUST include ≥1 quantitative target (latency, throughput, retention period, concurrency, etc.). If the project does not yet have a target, list it under an `## Open Questions` section with the reason, do NOT leave it as a placeholder like "X seconds" or vague prose like "数秒以内".
- Every model in the project's primary schema (`prisma/schema.prisma`, `*/migrations/*.sql`, `*/models/`, or `*/entities/`) MUST appear by name in `03-data.md`. Sibling entities sharing a prefix MAY be grouped under one `### <Family>` heading, but each member name MUST appear in the inline list under that heading.
- When the project has **≥3 distinct actor roles** (Operator/Admin/Owner/etc.), `02-features.md` or `06-requirements.md` MUST include a Role × Action matrix.
- When the project has **long-lived high-volume data** (audit logs, time-series analytics, event streams), `06-requirements.md` MUST include a Data Lifecycle subsection covering retention period per entity, sampling strategy, and aggregation timing.
- Constants and config files (`*.constants.ts`, `*config*.ts`, `*.config.json`, `**/config/*.yaml`) MUST be referenced in spec under "Existing Constraints Touched" or an equivalent subsection. The concrete numbers in these files (plan limits, retry counts, retention periods, fee rates, timeouts) are the source of truth for the NFR section.
- **Ubiquitous Language cross-check**: When `docs/ubiquitous-language.md` exists, extract its `Synonyms to Avoid` column (see one-liner in [references/full-gen-workflow.md](references/full-gen-workflow.md) §Exceptions) **before drafting `01-overview.md`**. Every role / entity / domain concept name introduced anywhere in the spec MUST be **absent** from that avoid-list. Names found in the avoid-list MUST either:
  - be **replaced with the canonical term** from the same UL row (e.g., "Tenant Admin" → restructure as "Operator (Billing scope)" if Operator is the canonical), or
  - be **proposed as a new canonical term in `§Open Questions`** for the next UL update (e.g., add row "Tenant Owner" if a third tier truly exists beyond Operator + Admin).
  Silently introducing avoid-list synonyms is the most common Consistency Warning at `ywc-spec-validate` time, and it propagates to every downstream artifact (tasks, code, PR titles) — fix at write time, not at validate time.
- **No ORM / SQL / schema syntax in any section** — the "no code" rule applies cross-section, not only to `03-data.md`. Even **inline backtick mentions** of Prisma directives (`@default`, `@relation`, `@@index`, `dbgenerated(...)`), SQL fragments (`SELECT`, `WHERE`, `CREATE TABLE`), or ORM-specific configuration (TypeORM decorators, SQLAlchemy column definitions) count as code and MUST be paraphrased into plain language. Examples:
  - ✗ `tenantId String @default(dbgenerated("current_setting('app.tenant_id'::text)"))` を設定
  - ✓ `tenantId` 列に PostgreSQL session variable `app.tenant_id` の現在値を default として bind し、RLS で他テナント行を遮断
  - ✗ `WHERE tenant_id = $1 AND status = 'ACTIVE'`
  - ✓ クエリは tenant ID と active status の 2 条件で絞り込む
  Identifier names (e.g., `tenantId`, `BeaconSite.samplingState`) in inline backticks are permitted because they are field references, not syntax — the test is "would this paste into `schema.prisma` / `*.sql` / decorator code and execute?". If yes, paraphrase.

For per-section writing templates, see [references/spec-structure.md](references/spec-structure.md).

For **Full Generation**, follow the detailed analysis steps in [references/full-gen-workflow.md](references/full-gen-workflow.md). Use **claude-opus-4-7** or the best available model.

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

See [references/hook-setup.md](references/hook-setup.md) for the full installation procedure. The hook creates a `.spec-update-pending` marker on commits with significant code changes, keeping Claude API calls out of the git hook itself.

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
  Model: claude-opus-4-7
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

**Pipeline alignment (for `--full` / `--update` only)** — the next pipeline stage is `ywc-spec-validate`, so the writer must self-check against the validator's rubric before declaring done:

- [ ] Every NFR in `06-requirements.md` has ≥1 quantitative target (no `X seconds` / `Y users` placeholders, no vague prose like "数秒以内")
- [ ] Every model in the project's primary schema appears by name in `03-data.md` (lumping permitted only as `### <Family>` heading with explicit inline member list)
- [ ] Role × Action matrix exists in `02-features.md` or `06-requirements.md` when the project has ≥3 actor roles
- [ ] Data Lifecycle subsection exists in `06-requirements.md` when the project has audit / analytics / time-series data
- [ ] Constants files (`*.constants.ts`, `*config*.ts`, etc.) referenced under "Existing Constraints Touched" or an equivalent subsection with `file:line`-style citation
- [ ] **Ubiquitous Language cross-check passed** — when `docs/ubiquitous-language.md` exists, every role / entity / concept name in the spec was verified **absent** from the `Synonyms to Avoid` column via the grep one-liner in `references/full-gen-workflow.md` §Exceptions. Any found synonym was either replaced with the canonical term OR proposed as a new canonical term in `§Open Questions`. (Skip when UL doc absent.)
- [ ] **No ORM / SQL / schema syntax leak** — every section (not only `03-data.md`) verified free of Prisma directives (`@default`, `@relation`, `@@index`, `dbgenerated(...)`), SQL fragments (`SELECT`, `WHERE`, `CREATE TABLE`, etc.), and ORM-specific decorator / column-definition syntax. Inline backticks containing such syntax MUST be paraphrased into plain prose. Field-reference identifiers (`tenantId`, `BeaconSite.samplingState`) remain permitted.
- [ ] Spec is expected to pass `ywc-spec-validate` at Gate ≥ 70 (REVIEW band) for downstream hand-off; `--full` mode aims for Gate ≥ 90 (PROCEED band)

## Common Mistakes

- **Reading nothing before writing** — always read existing spec and CLAUDE.md first to avoid overwriting valid content or misusing domain terminology.
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
