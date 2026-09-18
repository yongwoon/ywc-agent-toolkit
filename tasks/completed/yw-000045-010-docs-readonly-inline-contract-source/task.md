# yw-000045-010-docs-readonly-inline-contract-source — Implementation Checklist

## Prerequisites
- [ ] Confirm the eight read-only agents and two `workspace-write` workers match the spec inventory.

## Allowed Edit Scope
- [ ] Edit only the eight named read-only TOMLs and `codex/skills/references/subagent-status-actions.md`.
- [ ] Stop and report before editing validator, tests, generated package files, or worker TOMLs.

## Stop Conditions
- [ ] Stop if an agent's existing Output contract conflicts with the exact qualifier.
- [ ] Stop if the shared reference would need a second competing Output schema.
- [ ] Stop if either workspace-write worker would need modification.

## Hardening Gate
- [ ] Classify as documentation/contract-only behavior specification.
- [ ] Use the canonical qualifier from FR-3 verbatim; downstream validator and installer tests are the replacement evidence.
- [ ] Record the read-only return interface contract before changing prose.
- [ ] Data Integrity Hardening: N/A — no mutable state, transaction, retry, or duplicate-sensitive side effect.
- [ ] Critical review: N/A — not a critical surface.

## Implementation Steps
- [ ] Insert the exact qualifier into the `developer_instructions` value of the eight named read-only TOMLs, preserving each existing domain-specific Output section and redaction guidance.
  - Confirm `sandbox_mode = "read-only"` remains unchanged in each file.
  - Confirm no qualifier is added to `ywc-complexity-cleaner.toml` or `ywc-test-hardener.toml`.
- [ ] Update `codex/skills/references/subagent-status-actions.md` to name the read-only reviewer/advisor exception and state that `Artifacts:` is omitted unless a write-enabled caller separately produced an artifact.
  - Preserve `Status`, `Summary`, `Concerns`, `Blocker`, and `Missing context` semantics.
  - Preserve the existing Phase 1 target/finding/advisor-candidate limits.
- [ ] Review the diff for wording drift, accidental Claude-side edits, and changes outside Ownership.

## Task Verify
- [ ] `rg -l 'Read-only inline/no-artifact contract: You have no write capability\. Return bounded findings/advice inline; do not promise or wait for an artifact file\. Omit Artifacts: unless a write-enabled caller separately produced an artifact\.' codex/agents/ywc-*.toml | wc -l` returns `8`.
- [ ] `grep -q '^sandbox_mode = "workspace-write"$' codex/agents/ywc-complexity-cleaner.toml && grep -q '^sandbox_mode = "workspace-write"$' codex/agents/ywc-test-hardener.toml`.
- [ ] `git diff --check`.

## Verification
- [ ] Repository has no project lint, typecheck, unit-test, integration-test, or build command; use the task-specific checks above.

