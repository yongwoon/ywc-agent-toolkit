# Codex Package

The Codex bundle contains **54 skills** and **10 custom agents**.

Skills are sourced from codex/skills; each skill directory contains its SKILL.md, localized README files, and metadata. Evaluation files are included where maintained. Agent definitions are sourced from codex/agents.

## Install

    bash scripts/install.sh --codex
    bash scripts/install.sh --codex-agents

To install selected skills:

    bash scripts/install.sh --codex ywc-handoff ywc-retro ywc-mission

Set CODEX_HOME to use a temporary or non-default installation directory. The marketplace bundle under plugins/ywc-agent-toolkit is generated from codex/skills with bash scripts/sync-codex-plugin.sh.

## Skill Catalog

- [ywc-agentic](skills/ywc-agentic/README.md)
- [ywc-architecture-invariants](skills/ywc-architecture-invariants/README.md)
- [ywc-auth-implement](skills/ywc-auth-implement/README.md)
- [ywc-brainstorm](skills/ywc-brainstorm/README.md)
- [ywc-changelog-release-notes](skills/ywc-changelog-release-notes/README.md)
- [ywc-code-gen](skills/ywc-code-gen/README.md)
- [ywc-commit](skills/ywc-commit/README.md)
- [ywc-confidence-gate](skills/ywc-confidence-gate/README.md)
- [ywc-create-pr](skills/ywc-create-pr/README.md)
- [ywc-debug-rootcause](skills/ywc-debug-rootcause/README.md)
- [ywc-design-renew](skills/ywc-design-renew/README.md)
- [ywc-docker-isolate](skills/ywc-docker-isolate/README.md)
- [ywc-e2e-test-strategy](skills/ywc-e2e-test-strategy/README.md)
- [ywc-finish-branch](skills/ywc-finish-branch/README.md)
- [ywc-gen-testcase](skills/ywc-gen-testcase/README.md)
- [ywc-handle-pr-reviews](skills/ywc-handle-pr-reviews/README.md)
- [ywc-handoff](skills/ywc-handoff/README.md)
- [ywc-iac-author](skills/ywc-iac-author/README.md)
- [ywc-impl-review](skills/ywc-impl-review/README.md)
- [ywc-implement](skills/ywc-implement/README.md)
- [ywc-incident-postmortem](skills/ywc-incident-postmortem/README.md)
- [ywc-infra-design](skills/ywc-infra-design/README.md)
- [ywc-infra-optimize](skills/ywc-infra-optimize/README.md)
- [ywc-infra-review](skills/ywc-infra-review/README.md)
- [ywc-merge-dependabot](skills/ywc-merge-dependabot/README.md)
- [ywc-mine-review-history](skills/ywc-mine-review-history/README.md)
- [ywc-mission](skills/ywc-mission/README.md)
- [ywc-onboard-repo](skills/ywc-onboard-repo/README.md)
- [ywc-parallel-executor](skills/ywc-parallel-executor/README.md)
- [ywc-plan](skills/ywc-plan/README.md)
- [ywc-product-review](skills/ywc-product-review/README.md)
- [ywc-project-docs](skills/ywc-project-docs/README.md)
- [ywc-project-scaffold](skills/ywc-project-scaffold/README.md)
- [ywc-receive-review](skills/ywc-receive-review/README.md)
- [ywc-refactor-clean](skills/ywc-refactor-clean/README.md)
- [ywc-release-pr-list](skills/ywc-release-pr-list/README.md)
- [ywc-retro](skills/ywc-retro/README.md)
- [ywc-review-learnings](skills/ywc-review-learnings/README.md)
- [ywc-security-audit](skills/ywc-security-audit/README.md)
- [ywc-sequential-executor](skills/ywc-sequential-executor/README.md)
- [ywc-setup](skills/ywc-setup/README.md)
- [ywc-skill-author](skills/ywc-skill-author/README.md)
- [ywc-spec-ready](skills/ywc-spec-ready/README.md)
- [ywc-spec-validate](skills/ywc-spec-validate/README.md)
- [ywc-spec-writer](skills/ywc-spec-writer/README.md)
- [ywc-task-generator](skills/ywc-task-generator/README.md)
- [ywc-tdd-ritual](skills/ywc-tdd-ritual/README.md)
- [ywc-team-assemble](skills/ywc-team-assemble/README.md)
- [ywc-tech-research](skills/ywc-tech-research/README.md)
- [ywc-ubiquitous-language](skills/ywc-ubiquitous-language/README.md)
- [ywc-ui-ux-review](skills/ywc-ui-ux-review/README.md)
- [ywc-verify-done](skills/ywc-verify-done/README.md)
- [ywc-wayfinder](skills/ywc-wayfinder/README.md)
- [ywc-worktrees](skills/ywc-worktrees/README.md)

## Custom Agents

- [ywc-architect](agents/ywc-architect.toml)
- [ywc-cloud-engineer](agents/ywc-cloud-engineer.toml)
- [ywc-complexity-cleaner](agents/ywc-complexity-cleaner.toml)
- [ywc-go-reviewer](agents/ywc-go-reviewer.toml)
- [ywc-performance-engineer](agents/ywc-performance-engineer.toml)
- [ywc-python-reviewer](agents/ywc-python-reviewer.toml)
- [ywc-root-cause-analyst](agents/ywc-root-cause-analyst.toml)
- [ywc-security-engineer](agents/ywc-security-engineer.toml)
- [ywc-test-hardener](agents/ywc-test-hardener.toml)
- [ywc-typescript-reviewer](agents/ywc-typescript-reviewer.toml)
