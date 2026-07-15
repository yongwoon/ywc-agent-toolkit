# Codex Skill SDLC v1.1 Release Validation

## Scope

- Release candidate: `1.28.0`
- Branch: `feature/000063-010-infra-codex-release-evidence`
- Task: `000063-010-infra-codex-release-evidence`
- Evidence date: `2026-07-15`

The primary plan file referenced by the task is not present in this repository snapshot. This evidence uses the merged Phase `000061` and `000062` task artifacts plus the executed release commands below as the auditable source of truth.

## Validation Matrix

| Command | Timestamp (UTC) | Exit | Evidence | Notes |
|---|---|---:|---|---|
| `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-agentic` | `2026-07-15T11:27:53Z` | 0 | `PASS: ywc-agentic (290 lines)` | Focused author-validator check for a Phase `000062` skill that gained the preview approval flow contract. |
| `bash scripts/run-codex-skill-contract-evals.sh` | `2026-07-15T11:27:53Z` | 0 | `PASS: Codex skill contract evals are structurally valid.` | Confirms the merged routing, preview, agentic, and persistence eval fixtures all remain valid together. |
| `bash scripts/install.sh --list` | `2026-07-15T11:27:54Z` | 0 | Enumerated installable Claude Code skills/agents and Codex skills/agents without metadata errors. | Confirms packaging metadata remains discoverable before release. |
| `tmpdir="$(mktemp -d)" && CODEX_HOME="$tmpdir" bash scripts/install.sh --codex ywc-plan` | `2026-07-15T11:27:54Z` | 0 | Installed `references/`, `scripts/`, and `ywc-plan` into a temporary Codex home and cleaned it up via `trap`. | Verifies the release artifact installs without touching the real user environment. |
| `bash scripts/sync-codex-plugin.sh` | `2026-07-15T11:27:55Z` | 0 | Synced `.codex-plugin/plugin.json` and `codex/skills` into `plugins/ywc-agent-toolkit/`. | Confirms plugin packaging remains generated from source, not manually edited. |
| `bash scripts/validate.sh` | `2026-07-15T11:28:01Z` | 0 | `All checks passed.` | Repository-wide gate covering Codex/Claude assets, plugin package validation, release version parity, install dry run, and the toolkit evaluator regression gate. |
| `git diff -- codex/skills plugins/ywc-agent-toolkit/skills` | `2026-07-15T11:28:14Z` | 0 | No residual source-vs-plugin skill diff remained after the sync. | Final parity spot-check for the generated Codex plugin skill tree. |

## Source And Plugin Parity

- Source of truth remains `codex/skills/` and `.codex-plugin/plugin.json`.
- `scripts/sync-codex-plugin.sh` completed without error and refreshed the generated package from source.
- `bash scripts/validate.sh` passed after the sync, so manifest parity, executable mode parity, and release version parity all held at the repository gate.
- Manual edits under `plugins/ywc-agent-toolkit/skills/` were not used. Generated plugin changes were produced only by the sync script.

## Release Metadata

- `VERSION` advanced to `1.28.0`.
- `.release-please-manifest.json`, `plugin.json`, `.claude-plugin/plugin.json`, and `.codex-plugin/plugin.json` were aligned to `1.28.0`.
- `CHANGELOG.md` now contains the `1.28.0` release entry summarizing the Codex SDLC v1.1 contract work and this release-evidence closeout.

## Follow-up

- If the missing upstream plan document is restored later, add a backlink from that plan to this evidence file instead of replacing this command log.
