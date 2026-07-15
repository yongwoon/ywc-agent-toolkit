# 000063-010-infra-codex-release-evidence — Test Scenarios

## Scenario 1 — Validation Matrix Complete

- Given all source task contracts are merged
- When the release task is executed
- Then every required validator/install/sync command is recorded with status and evidence

## Scenario 2 — Plugin Parity

- Given updated source skills
- When the Codex plugin sync runs
- Then generated plugin files match source intent without manual plugin-only edits

## Scenario 3 — Temporary Install Safety

- Given a temporary `CODEX_HOME`
- When a targeted Codex install command is executed
- Then the package installs successfully and does not touch the real user environment

## Scenario 4 — Release Gate Enforcement

- Given an unresolved Phase 000062 contract
- When someone attempts to complete release evidence
- Then the task blocks and sends the work back to the owning earlier task
