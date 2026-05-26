# Repository Guidelines

## Project Structure & Module Organization

This repository is a portable skill bundle for Claude Code and Codex.

Codex skills live under `codex/skills/` in a flat `codex/skills/<skill-name>/` structure.
Each skill keeps its main instructions in `SKILL.md`, with optional supporting material in `references/`.
Codex custom agents live under `codex/agents/` as one TOML file per agent.
Shared bundle metadata sits at the root: `README.md`, `CHANGELOG.md`, `VERSION`.
Installation logic lives in `scripts/install.sh`.

## Build, Test, and Development Commands

- `bash scripts/install.sh --codex`: copies every skill under `codex/skills/` into `${CODEX_HOME:-~/.codex}/skills` and every custom agent under `codex/agents/` into `${CODEX_HOME:-~/.codex}/agents`
- `bash scripts/install.sh --codex --skip-agents`: installs only the bundled Codex skills (skip agents)
- `bash scripts/install.sh --codex-agents`: installs only the bundled Codex custom agents
- `bash scripts/install.sh --codex ywc-task-generator ywc-tech-research`: installs only the specified skills (does not touch agents)
- `bash scripts/install.sh --list --codex`: list all available Codex skills
- `bash scripts/install.sh --list --codex-agents`: list all available Codex custom agents
- `find codex/skills codex/agents -maxdepth 3 -type f`: quick check that the bundle contains the expected files
- `git diff --stat`: review scope before committing documentation or skill changes

There is no project build pipeline or package manager in this repository.
Development is primarily editing Markdown and shell scripts.

## Coding Style & Naming Conventions

Use concise, instructional Markdown with short sections and concrete examples.
Keep directory names lowercase with hyphens, matching installed skill names such as `ywc-tech-research`.
Keep shell scripts portable Bash with `set -euo pipefail`.

Bundle-level documentation aimed at repository users should be written in Korean unless there is a specific reason to use English.
