# Repository Guidelines

## Project Structure & Module Organization

This repository distributes `ywc-*` skills for Claude Code and Codex. Claude Code skills live in `claude-code/skills/<skill-name>/`; Codex skills live in `codex/skills/<skill-name>/`. Each skill requires `SKILL.md` plus localized README files: `README.md`, `README.en.md`, `README.ja.md`, and `README.ko.md`. Codex skills also require `agents/openai.yaml`. Claude Code custom agents live in `claude-code/agents/<agent-name>.md` (one Markdown file per agent). Codex custom agents live in `codex/agents/<agent-name>.toml` (one TOML per agent). Shared Codex material belongs in `codex/skills/references/` or `codex/skills/scripts/`. Root files such as `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `VERSION`, `plugin.json`, and `translations.json` describe distribution metadata and release state.

## Build, Test, and Development Commands

- `bash scripts/install.sh --list`: list all installable skills and verify the install script can scan the repository.
- `bash scripts/install.sh --cc ywc-plan`: install one Claude Code skill into `${CLAUDE_SKILLS_DIR:-~/.claude/skills}` for local testing.
- `bash scripts/install.sh --codex ywc-plan`: install one Codex skill into `${CODEX_HOME:-~/.codex}/skills`.
- `bash scripts/install.sh --cc-agents`: install Claude Code custom agents into `${CLAUDE_AGENTS_DIR:-~/.claude/agents}`.
- `bash scripts/install.sh --codex-agents`: install Codex custom agents into `${CODEX_HOME:-~/.codex}/agents`.
- `bash scripts/install.sh --all`: install both Claude Code and Codex bundles (skills + agents).
- `bash scripts/validate.sh`: run the local validation mirror for CI structure checks.
- `bash scripts/translate.sh --dry-run`: preview Tier 2 translation regeneration without API calls.

## Coding Style & Naming Conventions

Use portable Bash for scripts with `set -euo pipefail`. Keep skill names and directories in kebab case, for example `ywc-tech-research`. `SKILL.md` frontmatter must include `name:` and `description:`. Codex `SKILL.md` frontmatter must contain only those two fields; do not copy Claude-only fields such as `version`, `category`, or `requires`. Keep Markdown concise, instructional, and example-driven.

## Testing Guidelines

There is no package test runner. Treat `bash scripts/validate.sh` as the required pre-PR test. For install changes, also run targeted install/list commands. New or changed skills should be checked for required README locale files, matching `name:` frontmatter, and Codex `agents/openai.yaml` metadata.

## Commit & Pull Request Guidelines

Follow Conventional Commit style used in history: `feat:`, `fix:`, `docs:`, `i18n:`, `ci:`, or `chore:`. Example: `docs: update skill authoring guide`. PRs should explain the change, link the related issue when available, and pass CI checks for validation, shellcheck, markdownlint, and translation warnings.

## Security & Configuration Tips

Do not commit secrets or local install artifacts. Use `CLAUDE_SKILLS_DIR` and `CODEX_HOME` to test installs in temporary directories before touching real user skill folders.
