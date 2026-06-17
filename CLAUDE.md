# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

A skill and agent distribution toolkit for **Claude Code** (38 skills, 12 agents) and **Codex** (37 skills, 7 custom agents). Skills are installed locally via `scripts/install.sh` and activate inside the respective AI tool by matching user intent from `description:` frontmatter.

## Key Commands

```bash
# Install full bundles
bash scripts/install.sh --cc          # Claude Code → ~/.claude/skills/
bash scripts/install.sh --codex       # Codex → ~/.codex/skills/
bash scripts/install.sh --all         # both

# Install specific skills only
bash scripts/install.sh --cc ywc-plan ywc-commit

# Install custom agents only
bash scripts/install.sh --cc-agents
bash scripts/install.sh --codex-agents

# List available items
bash scripts/install.sh --list
bash scripts/install.sh --list --cc
bash scripts/install.sh --list --cc-agents
bash scripts/install.sh --list --codex-agents

# Validate skill structure locally (mirrors CI)
bash scripts/validate.sh

# Install repository Git hooks for Codex package sync/validation
bash scripts/install-git-hooks.sh
```

Override install paths via environment variables:
- `CLAUDE_SKILLS_DIR` — Claude Code install path (default: `~/.claude/skills`)
- `CLAUDE_AGENTS_DIR` — Claude Code agent install path (default: `~/.claude/agents`)
- `CODEX_HOME` — Codex home path (default: `~/.codex`)

## Repository Structure

```
claude-code/skills/<skill-name>/   # one directory per skill
  SKILL.md                         # required — frontmatter + skill body
  README.md                        # required — Korean default usage guide
  README.en.md                     # required — English source for generated translations
  README.ja.md / README.ko.md      # required Tier 1 translations
  references/                      # optional — long reference docs extracted from SKILL.md
codex/skills/<skill-name>/         # one directory per Codex skill
  SKILL.md                         # required — Codex-compatible frontmatter + skill body
  README.md / README.en.md         # required Korean default + English source
  README.ja.md / README.ko.md      # required Tier 1 translations
  agents/openai.yaml               # required — Codex UI metadata
  references/                      # optional — long reference docs extracted from SKILL.md
claude-code/agents/                # Claude Code custom agents, one ywc-*.md per agent
codex/agents/                      # Codex custom agents, one ywc-*.toml per agent
codex/skills/references/           # shared Codex reference docs linked by multiple skills
codex/skills/scripts/              # shared Codex helper scripts installed with skills
scripts/
  install.sh                       # install/prune/list entry point
  install-git-hooks.sh             # sets core.hooksPath to .githooks
  validate.sh                      # local CI mirror
.githooks/
  pre-commit                       # syncs plugins/ywc-agent-toolkit when codex/skills changes
  pre-push                         # blocks stale Codex generated package before push
.github/workflows/
  validate.yml                     # skill structure + shellcheck + dry-run
  markdownlint.yml                 # README*.md lint
  release-please.yml               # creates/updates Release PRs and GitHub Releases
  translation-check.yml            # informational warning, does not block merge
```

Codex skills mostly mirror the Claude Code `ywc-*` skill set, with Codex-specific additions where useful. Codex `SKILL.md` frontmatter must keep only `name` and `description`.

Codex custom agents are read-only TOML definitions. Their output contract uses `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` plus concise findings and a `Next action:` when the caller needs to apply or inspect something.

## Skill Authoring Rules

Every skill directory must contain:
1. `SKILL.md` with `name:` and `description:` YAML frontmatter
2. `README.md`, `README.en.md`, `README.ja.md`, and `README.ko.md`
3. Codex skills must also contain `agents/openai.yaml`

The `description:` field drives activation — it must include trigger phrases users will type AND explicit "Do not use for..." anti-triggers to prevent false matches against sibling skills.

Skill names follow `ywc-<kebab-case>` for all distributed skills. Keep SKILL.md under ~500 lines; extract long sections to `references/`.

Do not reference other skills with `@skill-name` (force-load) — it consumes excessive context. Reference by skill name only.

## CI Checks (all PRs must pass)

| Workflow | What it checks |
|----------|---------------|
| `validate` | Each skill has required frontmatter and README locale files; Codex skills also have `agents/openai.yaml` and no Claude-only frontmatter; shellcheck on `scripts/`; `--list` dry run |
| `markdownlint` | Root, skill, and contributing README files pass MD formatting with project-specific rule disables |
| `translation-check` | Informational only — warns if root or skill `README.md` changes without matching translation updates |

## Release Process

Releases are managed by Release Please on pushes to `main`. It creates or updates a Release PR that bumps `.release-please-manifest.json` and prepends `CHANGELOG.md`. Merging that PR creates the git tag and GitHub Release.

## Commit Conventions

```
feat: add ywc-api-design skill
fix: install.sh prune not working on partial install
i18n: add Japanese translation for ywc-plan README
ci: add shellcheck to validate workflow
chore: update .gitignore
```

Types: `feat`, `fix`, `docs`, `i18n`, `ci`, `chore`
