# Contributing to ywc-agent-toolkit

Thank you for your interest in contributing! This guide explains how to submit bug reports, skill improvements, new skills, and translations.

## Table of Contents

- [How to contribute](#how-to-contribute)
- [Development setup](#development-setup)
- [Skill authoring rules](#skill-authoring-rules)
- [Translations](#translations)
- [Commit message conventions](#commit-message-conventions)
- [Pull request process](#pull-request-process)
- [CI requirements](#ci-requirements)

---

## How to contribute

| Contribution type | How |
|-------------------|-----|
| Bug report | Open an [issue](../../issues/new?template=bug_report.md) |
| Skill improvement | Open an issue or submit a PR |
| New skill | Open a [new skill issue](../../issues/new?template=new_skill.md) first, then PR |
| Translation | Open a [translation issue](../../issues/new?template=translation.md) or submit a PR directly |

---

## Development setup

```bash
# Fork and clone your fork
git clone https://github.com/<your-username>/ywc-agent-toolkit.git
cd ywc-agent-toolkit

# Create a feature branch
git checkout -b feat/your-skill-name

# Test the install script locally
bash scripts/install.sh --list
bash scripts/install.sh --cc ywc-plan   # install a single skill for testing
bash scripts/install.sh --codex ywc-plan
```

---

## Skill authoring rules

### Directory structure

```
claude-code/skills/<skill-name>/
├── SKILL.md          # required — skill definition
├── README.md         # required — English usage guide
├── README.ja.md      # optional — Japanese
├── README.ko.md      # optional — Korean
├── README.zh.md      # optional — Chinese
├── README.es.md      # optional — Spanish
└── references/       # optional — reference documents loaded by the skill

codex/skills/<skill-name>/
├── SKILL.md          # required — Codex-compatible skill definition
├── README.md         # required — Korean usage guide
├── README.en.md      # required — English canonical source
├── README.ja.md      # required — Japanese
├── README.ko.md      # required — Korean
├── agents/
│   └── openai.yaml   # required — Codex UI metadata
└── references/       # optional — reference documents loaded by the skill
```

### SKILL.md frontmatter (required fields)

```yaml
---
name: ywc-your-skill-name
description: >
  One or two sentences describing WHEN this skill activates and WHAT it does.
  Include trigger phrases so the tool can match user intent.
---
```

Codex `SKILL.md` frontmatter must contain only `name` and `description`.
Claude Code skills may include extra metadata such as `version`, `category`,
`phase`, or `requires`, but those fields must not be copied into Codex skills.

### Naming conventions

- Skill directory: `ywc-<kebab-case>` for distributed Claude Code and Codex skills
- Follow the patterns in [ywc-skill-author](claude-code/skills/ywc-skill-author/SKILL.md)

### Before submitting a new skill PR

- [ ] `SKILL.md` has `name:` and `description:` frontmatter
- [ ] `README.md`, `README.en.md`, `README.ja.md`, and `README.ko.md` are included
- [ ] Codex skills include `agents/openai.yaml`
- [ ] Codex `SKILL.md` frontmatter has no Claude-only metadata fields
- [ ] The skill is general-purpose (not specific to a single project)
- [ ] `bash scripts/install.sh --list` still works after your change

---

## Translations

Translations are very welcome and are labeled `good first issue`.

### Language tiers

Languages are organized into two tiers. The tier list is the single source of truth in [`translations.json`](translations.json).

| Tier | Languages | How maintained |
|------|-----------|---------------|
| **Tier 1** | `en` (canonical), `ja`, `ko` | Manually written and reviewed |
| **Tier 2** | `es`, `zh` | AI-generated via `scripts/translate.sh`, community review welcome |

Tier 2 files include an auto-generation notice at the top:

```html
<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->
```

### How to add a Tier 1 translation

1. Find a `README.md` that has not yet been translated into your language
2. Create `README.<lang>.md` in the same directory
3. Translate the full content from `README.md`
4. Submit a PR with the label `i18n:<lang>`

### How to regenerate Tier 2 translations

Tier 2 files (es, zh) can be regenerated automatically using `scripts/translate.sh`.

**Requirements**: `ANTHROPIC_API_KEY`, `jq`, `curl`

```bash
# Regenerate all Tier 2 translations
ANTHROPIC_API_KEY=sk-... bash scripts/translate.sh

# Regenerate a single language
ANTHROPIC_API_KEY=sk-... bash scripts/translate.sh --lang es

# Regenerate a single skill
ANTHROPIC_API_KEY=sk-... bash scripts/translate.sh --skill ywc-plan

# Regenerate Codex skills only
ANTHROPIC_API_KEY=sk-... bash scripts/translate.sh --codex

# Preview what would be generated (no API calls)
bash scripts/translate.sh --dry-run
```

### How to add a new language

1. Add the language code to `translations.json` under `tier1.codes` (manual) or `tier2.codes` (AI-generated) and to the `all` array
2. For Tier 1: create `README.<lang>.md` files manually
3. For Tier 2: run `bash scripts/translate.sh --lang <code>`
4. Update the tier table above in this file

### Translation sync

When an English source (`README.md`) changes, CI posts an informational warning on PRs that update English without also updating translations. The comment distinguishes Tier 1 (manual update recommended) from Tier 2 (run the script). You are not required to update all languages in a single PR — the warning is informational only.

---

## Commit message conventions

```
<type>: <short description>

[optional body]
```

| Type | Use for |
|------|---------|
| `feat` | New skill or feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `i18n` | Translation |
| `ci` | CI/CD changes |
| `chore` | Maintenance (scripts, config) |

Examples:

```
feat: add ywc-api-design skill
fix: install.sh prune not working on partial install
i18n: add Japanese translation for ywc-plan README
```

---

## Pull request process

1. Ensure CI passes (skill validation, shellcheck, markdownlint)
2. Fill in the PR template completely
3. Link the related issue if one exists
4. A maintainer will review and merge

**Note**: Only the maintainer (@yongwoon) can merge PRs and create releases.

---

## CI requirements

All PRs must pass:

| Check | What it verifies |
|-------|-----------------|
| `validate` | Every skill has required frontmatter, README locale files, and Codex `agents/openai.yaml` metadata |
| `shellcheck` | `scripts/install.sh` has no shell script errors |
| `markdownlint` | README files pass basic Markdown formatting rules |

The translation check posts an **informational warning** only — it does not block merging.
