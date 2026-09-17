# yw-000045-010-docs-readonly-inline-contract-source

## Purpose
Establish one explicit local inline/no-artifact return contract for the eight read-only Codex reviewer/advisor agents and align the shared status reference with that boundary.

## Scope
- Add the exact qualifier from FR-3 to the eight named read-only agent TOMLs.
- Update the shared `subagent-status-actions.md` exception without changing canonical statuses or Phase 1 limits.
- Preserve the two `workspace-write` worker contracts and all domain-specific Output sections.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260917-codex-readonly-agent-inline-contract.md#fr-1-explicit-read-only-agent-qualifier` — local agent contract.
- `docs/ywc-plans/20260917-codex-readonly-agent-inline-contract.md#fr-2-shared-read-only-routing-exception` — shared routing exception.

### Summary
The eight read-only agents must state in their own `developer_instructions` that they cannot create artifacts, must return bounded findings/advice inline, and must not promise or await an artifact file. The shared status reference must name this exception while retaining existing status fields and finding limits. The two write-enabled workers remain unchanged.

### Out of Scope (from spec)
- Validator logic — handled by `yw-000046-020-infra-readonly-contract-validator`.
- Installed-agent smoke coverage — handled by `yw-000046-030-test-installed-readonly-contract`.
- Generated marketplace synchronization — handled by `yw-000047-040-infra-readonly-contract-distribution`.
- Claude agents, new agents, model/tool/sandbox changes, release files, and upstream PR changes.

## Criticality
normal

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `yw-000046-020-infra-readonly-contract-validator` — validates the exact qualifier in read-only agent instructions.
- `yw-000046-030-test-installed-readonly-contract` — checks the installed copies retain the source contract.
- `yw-000047-040-infra-readonly-contract-distribution` — synchronizes the generated package after source edits and validation.

## Key Files
- `codex/agents/ywc-architect.toml` — add local qualifier.
- `codex/agents/ywc-cloud-engineer.toml` — add local qualifier.
- `codex/agents/ywc-go-reviewer.toml` — add local qualifier.
- `codex/agents/ywc-performance-engineer.toml` — add local qualifier.
- `codex/agents/ywc-python-reviewer.toml` — add local qualifier.
- `codex/agents/ywc-root-cause-analyst.toml` — add local qualifier.
- `codex/agents/ywc-security-engineer.toml` — add local qualifier.
- `codex/agents/ywc-typescript-reviewer.toml` — add local qualifier.
- `codex/skills/references/subagent-status-actions.md` — clarify named read-only exception.

## Notes
Use the exact canonical qualifier defined in FR-3. Keep each agent's existing domain-specific Output contract and do not add the qualifier to `ywc-complexity-cleaner.toml` or `ywc-test-hardener.toml`.

## Hardening Evidence

### Test Feedback Path
- Named exception: docs/contract-only change; downstream validator and installation smoke test provide mechanical verification.

### Interface Contract
- Contract: read-only inline/no-artifact return contract.
- Owner task: `yw-000045-010-docs-readonly-inline-contract-source`.
- Canonical signature: bounded caller evidence → inline `Status`, concise findings/advice, and conditional `Concerns`, `Blocker`, or `Missing context`; no artifact path required.
- Consumers: `yw-000046-020-infra-readonly-contract-validator`, `yw-000046-030-test-installed-readonly-contract`, orchestrating Codex skills.
- Implementation opacity: consumers rely on this wording and must not invent a second Output schema.
- Mismatch action: return `NEEDS_CONTEXT` if the named agent set, qualifier, or status fields conflict with the spec.

### Data Integrity Hardening
- Trigger: N/A — documentation-only contract change; no mutable state or side effect.

### Critical Surface Review
- N/A — not a critical surface under the spec's criticality rules.

## Out of Scope
No validator, test-script, generated-package, or runtime behavior changes.

## Parallel Execution Metadata
- **Ownership:** The eight named read-only TOMLs and `codex/skills/references/subagent-status-actions.md` only.
- **Shared Surfaces:** Read-only agent return contract; source reference consumed by the generated marketplace mirror.
- **Conflicts With:** `(None identified)`.
- **Parallelizable After:** Repository baseline before this batch; no predecessor task.
- **Task Verify:** `rg -n "Read-only inline/no-artifact contract" codex/agents/ywc-*.toml`; `rg -n "read-only reviewer/advisor|Artifacts:" codex/skills/references/subagent-status-actions.md`.

