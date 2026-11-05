# yk-000005-040-domain-merge-dependabot-workflow

## Purpose
Bring the `ywc-merge-dependabot` scripts and workflow safeguards up to the upstream final state with validated base-branch handling (AC13b).

Spec item: B4 (#341, #345) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- Port from the snapshot `ywc-merge-dependabot/scripts/`: `poll-merge-queue.py` (`chunk_deadline`), `wait-dependabot-rebase.sh`, `detect-dockerfile-from.sh`, `detect-major-bump.py`, and `test_merge_dependabot_scripts.py` (stdlib only, `gh`/`sleep` stubs, no network). Keep mode 755 and call via `bash`/`python3`. Python ≥3.10 syntax is required (`from __future__ import annotations` is allowed).
- SKILL.md: validate `baseRefName` with `^[A-Za-z0-9._/-]+$`, no leading `-`, no `..`, `git check-ref-format --branch` before it enters a shell variable or `gh api repos/{owner}/{repo}/branches/$base/…`; failures → 'cannot confirm', excluded from the `--auto` queue and handled sequentially (snapshot `:81-89`), quoted variables only.
- Require a required status check on the base branch before any `--auto` (none → no `--auto`); separate CI failed / pending (pending only in the parallel-auto queue); Dockerfile `FROM` detection limited to Dockerfile hunks; one `@dependabot rebase` comment on conflict; polling chunks (`chunk_deadline` 540 s, `gh` timeout 20 s, clamped sleep, stalled only after the overall deadline); major bumps always skipped; replace `/path/to/…` (`SKILL.md:118,121`) with the B1 convention.
- Register the three new scripts as rows in the Bundled Execution Scripts table (`claude-code/skills/CLAUDE.md:361` already lists `detect-major-bump.py`) and register the test in `scripts/validate.sh` `check_cc_support_dirs`; both new `.sh` files must be shellcheck-clean.
- Update the four Tier 1 READMEs (required-check gate, polling, major skip, rebase comment — 1–2 sentences).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 12 (B4), AC13b, Critical Surfaces, Failure Modes 'merge-dependabot required check'
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-merge-dependabot` — upstream scripts, test and SKILL.md (T0 snapshot)

### Summary
Only `group-by-ecosystem.py` exists locally. The base branch name comes from the remote and must be treated as hostile input, and `--auto` on a branch without required checks merges instantly. The scripts bring polling, rebase and Dockerfile/major-bump detection.

### Out of Scope (from spec)
- Docker gate semantics beyond the Dockerfile `FROM` detection
- Codex counterpart
- `ywc-performance-engineer` FinOps contract

## Criticality
critical — Spec Critical Surface: remote-controlled `baseRefName` enters shell and `gh api` paths and drives `--auto` merge decisions.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream scripts and SKILL.md
- `yk-000005-030-refactor-skill-script-paths` — serializes the shared-file chain (B3 → B2 → B4) and `history.mechanical.json`; B3 already edited `ywc-merge-dependabot/SKILL.md`/README

### Depended By
- `yk-000005-050-domain-handoff-retro-skills` — needs the output of this task

## Key Files
- `claude-code/skills/ywc-merge-dependabot/scripts/*` — 4 scripts + 1 test
- `claude-code/skills/ywc-merge-dependabot/SKILL.md` — safeguards, paths
- `claude-code/skills/ywc-merge-dependabot/README*.md` — behavior sentences
- `claude-code/skills/CLAUDE.md` — Bundled Execution Scripts rows
- `scripts/validate.sh` — test registration
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — baseline

## Notes
- `python3` here is 3.14.0; the 3.10 requirement matters for older environments.
- `SKILL.md` ~293 lines → ~336 after this task; fine.

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `claude-code/skills/ywc-merge-dependabot/**`
- `claude-code/skills/CLAUDE.md` (scripts table rows)
- `scripts/validate.sh`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- `scripts/validate.sh` `check_cc_support_dirs` (A8c → B4)
- Bundled Execution Scripts table

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`
- `yk-000005-030-refactor-skill-script-paths`

### Task Verify
- `python3 claude-code/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py`
- `for f in poll-merge-queue.py wait-dependabot-rebase.sh detect-dockerfile-from.sh detect-major-bump.py test_merge_dependabot_scripts.py; do test -x claude-code/skills/ywc-merge-dependabot/scripts/$f || exit 1; done`
- `grep -q 'chunk_deadline' claude-code/skills/ywc-merge-dependabot/scripts/poll-merge-queue.py`
- `for k in required_status_checks baseRefName check-ref-format; do grep -q "$k" claude-code/skills/ywc-merge-dependabot/SKILL.md || exit 1; done`
- `[ "$(grep -c -- '/path/to/' claude-code/skills/ywc-merge-dependabot/SKILL.md | tr -d ' ')" = 0 ]`
- `shellcheck claude-code/skills/ywc-merge-dependabot/scripts/wait-dependabot-rebase.sh claude-code/skills/ywc-merge-dependabot/scripts/detect-dockerfile-from.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-merge-dependabot/SKILL.md`

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
