---
name: ywc-spec-writer
description: (ywc) Use when creating or updating a project specification (사양서) in docs/specification/. Triggers: "spec 작성", "사양서 작성", "사양서 업데이트", "specification 작성", "프로젝트 사양", "전체 사양서", "write spec", "generate specification", "update spec", "project spec", "仕様書作成", "仕様書更新", "スペック作成", "ywc-spec-writer". Do not use for spec quality review (use ywc-spec-validate), task decomposition from a finalized spec (use ywc-task-generator), or pre-implementation planning without a spec intent (use ywc-plan).
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

**Violating the letter of these rules is violating the spirit.** A spec containing code, written in the wrong language, or auto-generated without explicit intent does not serve its readers.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--full` | flag | `--full` | Generate complete spec from scratch. Requires user confirmation. Uses best available model. |
| `--update` | flag | `--update` | Regenerate all existing spec sections. |
| `--from-task` | `--from-task <path>` | `--from-task tasks/000002-010-api-user/` | Update spec from a ywc-task-generator task directory. |
| `--from-commit` | `--from-commit <ref>` | `--from-commit HEAD` | Update spec based on diff of a specific commit. |
| `--setup-hook` | flag | `--setup-hook` | Install git hook for automatic spec-update tracking. |
| `--lang` | `--lang ko\|ja\|en` | `--lang ja` | Output language. Default: `ko`. |

## Workflow

### Step 1: Determine Mode

| Mode | Trigger | Notes |
|------|---------|-------|
| **Full Generation** | `--full` | Requires user confirmation. Uses best model. |
| **Full Refresh** | `--update` | Regenerates all existing sections. |
| **Task-based Update** | `--from-task <path>` | Maps task category to affected sections. |
| **Commit-based Update** | `--from-commit <ref>` | Analyzes git diff to determine affected sections. |
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

If `--lang` is not specified, check the project's CLAUDE.md for a declared primary documentation language. If not found there either, **ask the user**:

> "사양서를 어떤 언어로 작성할까요? / Which language should the spec be written in? / 仕様書をどの言語で作成しますか？"
> 1. 한국어 (ko) — 기본값
> 2. English (en)
> 3. 日本語 (ja)

Wait for the user's answer before proceeding. Do not assume Korean silently — the question must appear in the conversation.

For locale-specific writing rules (formality level, term policy), see [references/language-policy.md](references/language-policy.md).

### Step 4: Prepare Spec Directory

If `docs/specification/` does not exist, run:

```bash
bash codex/skills/ywc-spec-writer/scripts/init-spec-structure.sh <lang> "<ProjectName>"
```

This creates the 7-section skeleton without any LLM calls. For the full section layout and writing templates, see [references/spec-structure.md](references/spec-structure.md).

### Step 5: Determine Affected Sections

For **commit-based** and **task-based** modes, identify which spec sections need updating before writing:

```bash
# Commit-based
git diff <ref>^..<ref> --name-only | bash codex/skills/ywc-spec-writer/scripts/detect-affected-sections.sh

# Task-based: read task README.md for category field, then apply mapping
```

For the category-to-section and file-pattern-to-section mapping tables, see [references/section-mapping.md](references/section-mapping.md).

### Step 6: Write or Update Spec Content

**Non-negotiable writing rules for all modes:**
- Zero program code in any spec output
- Write for a business stakeholder, not a developer
- Features use the user story format: "As a [user], I want [action] so that [benefit]"
- Data and flows use plain-language descriptions
- Keep each section file ≤ 400 lines

For per-section writing templates, see [references/spec-structure.md](references/spec-structure.md).

For **Full Generation**, follow the detailed analysis steps in [references/full-gen-workflow.md](references/full-gen-workflow.md). Use **claude-opus-4-7** or the best available model.

### Step 7: Update README Index

After every write, update `docs/specification/README.md`:
- Set `**Last updated**` to today's date
- Append: `| YYYY-MM-DD | <section(s)> | <one-line summary> |`

### Step 8: Hook Setup (if `--setup-hook`)

See [references/hook-setup.md](references/hook-setup.md) for the full installation procedure. The hook creates a `.spec-update-pending` marker on commits with significant code changes, keeping Claude API calls out of the git hook itself.

## Output Format

```text
✅ Spec updated: docs/specification/
  Modified: 02-features.md, 03-data.md
  Unchanged: 01-overview.md, 04-interfaces.md, 05-user-flows.md, 06-requirements.md, 07-glossary.md
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
- [ ] All written sections have substantive content (no "To be written" placeholder remaining)
- [ ] Technical terms kept in English per language policy (not transliterated)

## Common Mistakes

- **Reading nothing before writing** — always read existing spec and CLAUDE.md first to avoid overwriting valid content or misusing domain terminology.
- **Including code in spec output** — even a one-line variable name breaks non-developer readability. Replace with flow descriptions or plain-language attribute lists.
- **Running full generation without `--full`** — unexpected long-running model calls surprise users. The explicit flag is the contract.

## Integration

- **Upstream**: `ywc-plan` (generates feature specs), `ywc-task-generator` (produces task docs for `--from-task`)
- **Downstream**: `ywc-spec-validate` (validates the written spec before task decomposition)
- **Pairs with**: `ywc-ubiquitous-language` (align spec vocabulary with canonical domain terms)
