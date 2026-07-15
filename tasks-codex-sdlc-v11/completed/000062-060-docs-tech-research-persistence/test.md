# 000062-060-docs-tech-research-persistence — Test Scenarios

## Scenario 1 — New Persisted Report

- Given a valid repository-relative Markdown `--output`
- When `ywc-tech-research` is run with that path
- Then the contract documents a persisted report with evidence, inference, and provenance fields

## Scenario 2 — Overwrite Requires Confirmation

- Given an existing output file
- When overwrite flags are incomplete or confirmation is missing
- Then the skill blocks the write and explains the required confirmation path

## Scenario 3 — Non-Interactive Safe Overwrite

- Given an existing output file and fully matched non-interactive overwrite flags
- When the caller re-runs with the same approved intent
- Then the contract allows overwrite and preserves provenance requirements

## Scenario 4 — Unsafe Path Rejected

- Given an absolute path, parent-directory escape, symlink escape, or non-Markdown extension
- When the caller requests persistence
- Then the contract rejects the path before any write semantics are described

## Scenario 5 — Consumer Handoff

- Given a persisted research artifact
- When plan/spec-ready/task-generator/wayfinder mention downstream usage
- Then each skill references the same overwrite and provenance expectations
