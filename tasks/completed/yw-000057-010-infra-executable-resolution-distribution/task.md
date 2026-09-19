# Implementation Task

## Prerequisites

- [ ] Focused resolver regression and complement validation pass.
- [ ] `scripts/check-codex-agent-evals.sh` passes with no agent changes.

## Allowed Edit Scope

Run the synchronization workflow and modify only generated files under `plugins/ywc-agent-toolkit/skills/` as produced by the repository sync script. Do not hand-edit generated output or agent TOML.

## Stop Conditions

- Stop if synchronization produces stale or divergent generated output.
- Stop if either resolver loses required executable/readable mode in source, temporary install, or plugin output.
- Stop if validation requires changing agent definitions or adding a dependency.

## Hardening Gate

- RED-first evidence: predecessor regression and complement checks must be green before synchronization.
- Public surface: verify source and generated resolver interfaces remain identical.
- Data Integrity: N/A.
- Critical surface: review generated diff and confirm no unapproved agent or Claude changes.

## Implementation Steps

- [ ] Run `bash scripts/sync-codex-plugin.sh` from the source-authoritative tree.
  - [ ] Inspect the generated diff for only expected Codex resolver/caller/reference changes.
- [ ] Install the Codex bundle into a temporary `CODEX_HOME` and verify both resolver files retain source-compatible modes.
- [ ] Verify the corresponding files under `plugins/ywc-agent-toolkit/skills/` have the required modes and synchronized content.
- [ ] Run agent evaluation and full repository validation; report any stale generated output or unexpected agent changes.

## Task Verify

- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] Temporary `CODEX_HOME` install mode/content check for both resolver files
- [ ] `bash scripts/check-codex-agent-evals.sh`
- [ ] `bash scripts/validate.sh`

## Verification

- [ ] `git diff --check`
- [ ] Confirm `git diff -- codex/agents` is empty.
- [ ] Confirm a second sync produces no unexpected source/plugin drift.

