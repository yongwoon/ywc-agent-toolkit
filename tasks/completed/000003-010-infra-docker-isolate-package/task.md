# 000003-010-infra-docker-isolate-package - Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] Source PR #110 Codex package files are available for comparison.
- [ ] No existing `codex/skills/ywc-docker-isolate/` directory exists, or any existing partial directory is intentionally from this task.

## Allowed Edit Scope

- [ ] Stay within `codex/skills/ywc-docker-isolate/**`.
- [ ] If executor integration, catalog, `.codex-plugin`, or release metadata edits are needed, stop and report before proceeding.

## Stop Conditions

- [ ] Stop if the source package requires a behavior decision not covered by `docs/ywc-plans/codex-pr110-120-129-port.md`.
- [ ] Stop if copied frontmatter contains Claude-only fields such as `version`, `category`, or `requires`.
- [ ] Stop if any script requires a runtime path that cannot be expressed as skill-call form, `codex/skills/...`, or installed `${CODEX_HOME}` path.

## Implementation Steps

- [ ] Create the new Codex skill package.
  - [ ] Add `codex/skills/ywc-docker-isolate/SKILL.md` with only `name:` and `description:` frontmatter.
  - [ ] Add `README.md`, `README.en.md`, `README.ja.md`, and `README.ko.md`.
  - [ ] Add `agents/openai.yaml` following existing Codex skill metadata style.
- [ ] Port Docker isolation reference material.
  - [ ] Add `references/port-allocation.md`.
  - [ ] Add `references/preconditions.md`.
  - [ ] Rewrite any source-only `tools/codex-skill/skills/...` examples.
- [ ] Port shell scripts.
  - [ ] Add `scripts/_lib.sh`.
  - [ ] Add `scripts/audit-docker-stacks.sh`.
  - [ ] Add `scripts/setup-docker-ports.sh`.
  - [ ] Add `scripts/teardown-docker.sh`.
- [ ] Preserve executable behavior.
  - [ ] Mark executable scripts with executable bits.
  - [ ] Keep shell syntax portable Bash with `set -euo pipefail` where source scripts use it.
  - [ ] Verify macOS-compatible assumptions are preserved from the source PR.
- [ ] Remove source-path leakage.
  - [ ] Prefer `ywc-docker-isolate --mode ...` examples in `SKILL.md`.
  - [ ] Use `codex/skills/ywc-docker-isolate/...` only for source-tree verification commands.
  - [ ] Use `${CODEX_HOME:-$HOME/.codex}/skills/ywc-docker-isolate/...` only for installed-runtime examples.

## Task Verify

- [ ] `find codex/skills/ywc-docker-isolate -maxdepth 3 -type f | sort`
- [ ] `bash -n codex/skills/ywc-docker-isolate/scripts/*.sh`
- [ ] `find codex/skills/ywc-docker-isolate/scripts -type f -perm -111 | sort`
- [ ] `rg -n 'tools/codex-skill|requires:|version:|category:' codex/skills/ywc-docker-isolate && exit 1 || true`

## Verification

- [ ] Local structural validation still passes after this task's source edits: `bash scripts/validate.sh`
- [ ] `git diff --check`
