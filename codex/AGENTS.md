# Repository Guidelines

## Project Structure & Module Organization

This repository is a portable skill bundle for Claude Code and Codex.

Codex skills live under `codex/skills/` in a flat `codex/skills/<skill-name>/` structure.
Each skill keeps its main instructions in `SKILL.md`, with optional supporting material in `references/`.
Codex custom agents live under `codex/agents/` as one TOML file per agent.
Shared bundle metadata sits at the root: `README.md`, `CHANGELOG.md`, `VERSION`.
Installation logic lives in `scripts/install.sh`.
For Codex skills, `codex/skills/` is the source of truth. The marketplace package under `plugins/ywc-agent-toolkit/skills/` is generated from it by `bash scripts/sync-codex-plugin.sh`; do not edit the generated package first.

## Build, Test, and Development Commands

- `bash scripts/install.sh --codex`: `codex/skills/`의 모든 스킬을 `${CODEX_HOME:-~/.codex}/skills`로, `codex/agents/`의 모든 custom agent를 `${CODEX_HOME:-~/.codex}/agents`로 복사합니다.
- `bash scripts/install.sh --codex --skip-agents`: 번들된 Codex 스킬만 설치하고 agents는 건드리지 않습니다.
- `bash scripts/install.sh --codex-agents`: 번들된 Codex custom agents만 설치합니다.
- `bash scripts/install.sh --codex ywc-task-generator ywc-tech-research`: 지정한 스킬만 설치하고 agents는 건드리지 않습니다.
- `bash scripts/install.sh --list --codex`: 설치 가능한 모든 Codex 스킬을 나열합니다.
- `bash scripts/install.sh --list --codex-agents`: 설치 가능한 모든 Codex custom agents를 나열합니다.
- `bash scripts/install-git-hooks.sh`: `codex/skills/` 변경 commit 시 marketplace package sync와 validation이 자동 실행되도록 repo Git hook을 설치합니다.
- `bash scripts/sync-codex-plugin.sh`: `codex/skills/` 변경 사항을 Codex marketplace package인 `plugins/ywc-agent-toolkit/skills/`로 동기화합니다.
- `bash scripts/validate.sh`: source install 구조와 marketplace package가 모두 최신인지 검증합니다.
- `find codex/skills codex/agents -maxdepth 3 -type f`: 번들에 필요한 파일이 포함되어 있는지 빠르게 확인합니다.
- `git diff --stat`: review scope before committing documentation or skill changes

There is no project build pipeline or package manager in this repository.
Development is primarily editing Markdown and shell scripts.

## Coding Style & Naming Conventions

Use concise, instructional Markdown with short sections and concrete examples.
Keep directory names lowercase with hyphens, matching installed skill names such as `ywc-tech-research`.
Keep shell scripts portable Bash with `set -euo pipefail`.

Bundle-level documentation aimed at repository users should be written in Korean unless there is a specific reason to use English.
