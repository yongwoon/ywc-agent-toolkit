# yw-000065-020-domain-impact-security-evidence

## Purpose

Localized PR Impact and security testcase evidence for Stage 3 of the selected Codex issue #69 port.

## Scope

- Generate concise optional Impact from existing evidence
- Derive deduplicated negative-path scenarios
- Verify Impact applicability and scenario reuse

## Spec Reference

### Primary Sources

- [docs/ywc-plans/20261016-codex-issue69-selective-port.md#functional-requirements](../../docs/ywc-plans/20261016-codex-issue69-selective-port.md#functional-requirements)
- [docs/ywc-plans/20261016-codex-issue69-selective-port.md#acceptance-criteria](../../docs/ywc-plans/20261016-codex-issue69-selective-port.md#acceptance-criteria)
- [docs/ywc-plans/20261016-codex-issue69-selective-port.md#verification](../../docs/ywc-plans/20261016-codex-issue69-selective-port.md#verification)
- [docs/ywc-plans/20261016-codex-issue69-selective-port.md#failure-modes](../../docs/ywc-plans/20261016-codex-issue69-selective-port.md#failure-modes)
- [docs/ywc-plans/20261016-codex-issue69-selective-port.md#global-constraints](../../docs/ywc-plans/20261016-codex-issue69-selective-port.md#global-constraints)

### Summary

The approved plan selectively adapts upstream intent to existing Codex contracts. This task delivers localized pr impact and security testcase evidence and covers AC-8, FR-7, AC-10, FR-9, FM-8, FM-9. Static assertions and fixtures establish contract evidence; they cannot stand in for live observations. Trust the source plan and flag drift if this summary disagrees.

### Out of Scope (from spec)

Other deliverables belong to their named owner tasks in [the dependency graph](../dependency-graph.md#batch-27--codex-issue-69-selective-port). Claude Code, upstream release/history imports, new dependencies/DB changes, executor state or planner/ready Result schema expansion, screenshots, unrelated optimizations, and release metadata are excluded by the plan. Implementation and delivery require a subsequent execution request; generation alone authorizes neither.

## Criticality

`critical` — Conservative inference: security/approval/selection authority is touched by this contract; require full review. This is task metadata, not a new CLI criticality flag.

## Dependencies

### Depends On

- [yw-000065-010-domain-bounded-suggestion-policy](../yw-000065-010-domain-bounded-suggestion-policy/README.md)

The predecessor supplies the finalized contract and synchronized, validated baseline. First task: revision `614096d3` with current repository rules. Stage 2 requires all Stage 1 outputs accepted; Stage 3 requires all Stage 2 outputs accepted. Acceptance means regression evidence and review are accepted, not authority to publish.

### Depended By

- [yw-000065-030-domain-sdk-review-evidence](../yw-000065-030-domain-sdk-review-evidence/README.md)

The successor consumes this task's tested source and installed/package-compatible contracts.

## Acceptance Criteria and Verification Mapping

- `AC-8` — implement its bounded portion in this task; verify via `task.md`, `test.md`, `tests/codex_issue69_contract_test.py` and fixtures `tests/fixtures/codex-issue69/impact-security-evidence/` (E1).
- `FR-7` — implement its bounded portion in this task; verify via `task.md`, `test.md`, `tests/codex_issue69_contract_test.py` and fixtures `tests/fixtures/codex-issue69/impact-security-evidence/` (E1).
- `AC-10` — implement its bounded portion in this task; verify via `task.md`, `test.md`, `tests/codex_issue69_contract_test.py` and fixtures `tests/fixtures/codex-issue69/impact-security-evidence/` (E1).
- `FR-9` — implement its bounded portion in this task; verify via `task.md`, `test.md`, `tests/codex_issue69_contract_test.py` and fixtures `tests/fixtures/codex-issue69/impact-security-evidence/` (E1).
- `FM-8` — implement its bounded portion in this task; verify via `task.md`, `test.md`, `tests/codex_issue69_contract_test.py` and fixtures `tests/fixtures/codex-issue69/impact-security-evidence/` (E1).
- `FM-9` — implement its bounded portion in this task; verify via `task.md`, `test.md`, `tests/codex_issue69_contract_test.py` and fixtures `tests/fixtures/codex-issue69/impact-security-evidence/` (E1).

AC-10/FR-9 packaging and FM-8/FM-9 apply to every task. AC-5/FR-4 and AC-9/FR-8 are distributed requirements; this task alone does not close another owner's portion. Full requirement ownership is in the graph. Final stage review must have no unresolved Critical/High findings.

## Key Files

- `codex/skills/ywc-create-pr/SKILL.md`
- `codex/skills/ywc-create-pr/evals/evals.json`
- `codex/skills/ywc-gen-testcase/SKILL.md`
- `codex/skills/ywc-gen-testcase/evals/evals.json`
- `tests/fixtures/codex-issue69/impact-security-evidence/**` and `tests/codex_issue69_contract_test.py` — focused source/fixture evidence.

## Notes

- Mode: `llm`; language: `en`; initials: `yw`. Invocation normalized from `$ywc-task-generator docs/ywc-plans/20261016-codex-issue69-selective-port.md --mode --llm --lang en` to `--mode llm --lang en`; interactive preview shown, no separate approval wait under the invoked skill. `--approve-preview` not supplied and no persisted preview approval is claimed.
- Size forecast: up to 16 source/locale paths, 16 generated copies and 3 test/wiring scopes; ~650 authored changed LOC plus duplicate generated content. Update only behavior-relevant locale/eval content; existing matching files need no gratuitous changes. Reassess if authored scope exceeds ~1,200 LOC.
- Stage packaging is source-first via `bash scripts/sync-codex-plugin.sh`; each task must leave its own source/package parity valid. Review generated deltas and stop if synchronization includes unrelated unmerged work.
- The shared harness grows incrementally: task 63-010 creates/wires it; later tasks add only their completed requirements. No new runtime dependency, network call or LLM invocation belongs in offline validation.

## Hardening Evidence

### Test Feedback Path

RED-first target: `tests/codex_issue69_contract_test.py` with this task's `tests/fixtures/codex-issue69/impact-security-evidence/` scenarios, plus existing `scripts/run-codex-skill-contract-evals.sh`. Record the failing assertion before contract edits, or name an existing-coverage/docs-only exception and its replacement verification. Record baseline revision/context and measured evidence; otherwise explicitly state `not measured` and the gap.

### Interface Contract

This task changes prose workflow contracts defined in the spec Module Boundaries and FR sections. Canonical callable signature: N/A — the spec declares responsibilities/behavior, not a function signature; no Owned Interface Contract is synthesized. Consumers trust the declared behavior and do not infer internal signatures. Record actual name/input/output/error evidence before edits; an owner/consumer mismatch returns NEEDS_CONTEXT.

### Critical Surface Review

Full `ywc-impl-review` or manual full implementation review is required before DONE.

### Data Integrity Hardening

- Trigger surface: N/A — documentation/test contract and generated-copy edits; no runtime shared-state write or state-schema change.
- Atomic / locking strategy: N/A for application state. Serialize shared test/harness and plugin synchronization edits through this task DAG.
- Transaction boundary: N/A — no application transaction.
- Idempotency guard: N/A — preserve existing monitoring/preview guards; introduce no side effects.
- Required tests: N/A for data writes; relevant contract failure/duplicate-event/approval cases remain mandatory in `test.md`.

## Architecture Contract Consumer Handoff

- contract_state: N/A — no architecture contract.
- enforcement_verdict: N/A.

## Parallel Execution Metadata

### Ownership

Only these paths and this task's named contract portions may be edited. Locale and eval changes are limited to this task's behavior. Plugin paths are generated output only.

- `codex/skills/ywc-create-pr/README.en.md`
- `codex/skills/ywc-create-pr/README.es.md`
- `codex/skills/ywc-create-pr/README.ja.md`
- `codex/skills/ywc-create-pr/README.ko.md`
- `codex/skills/ywc-create-pr/README.md`
- `codex/skills/ywc-create-pr/README.zh.md`
- `codex/skills/ywc-create-pr/SKILL.md`
- `codex/skills/ywc-create-pr/evals/evals.json`
- `codex/skills/ywc-gen-testcase/README.en.md`
- `codex/skills/ywc-gen-testcase/README.es.md`
- `codex/skills/ywc-gen-testcase/README.ja.md`
- `codex/skills/ywc-gen-testcase/README.ko.md`
- `codex/skills/ywc-gen-testcase/README.md`
- `codex/skills/ywc-gen-testcase/README.zh.md`
- `codex/skills/ywc-gen-testcase/SKILL.md`
- `codex/skills/ywc-gen-testcase/evals/evals.json`
- `plugins/ywc-agent-toolkit/skills/ywc-create-pr/README.en.md`
- `plugins/ywc-agent-toolkit/skills/ywc-create-pr/README.es.md`
- `plugins/ywc-agent-toolkit/skills/ywc-create-pr/README.ja.md`
- `plugins/ywc-agent-toolkit/skills/ywc-create-pr/README.ko.md`
- `plugins/ywc-agent-toolkit/skills/ywc-create-pr/README.md`
- `plugins/ywc-agent-toolkit/skills/ywc-create-pr/README.zh.md`
- `plugins/ywc-agent-toolkit/skills/ywc-create-pr/SKILL.md`
- `plugins/ywc-agent-toolkit/skills/ywc-create-pr/evals/evals.json`
- `plugins/ywc-agent-toolkit/skills/ywc-gen-testcase/README.en.md`
- `plugins/ywc-agent-toolkit/skills/ywc-gen-testcase/README.es.md`
- `plugins/ywc-agent-toolkit/skills/ywc-gen-testcase/README.ja.md`
- `plugins/ywc-agent-toolkit/skills/ywc-gen-testcase/README.ko.md`
- `plugins/ywc-agent-toolkit/skills/ywc-gen-testcase/README.md`
- `plugins/ywc-agent-toolkit/skills/ywc-gen-testcase/README.zh.md`
- `plugins/ywc-agent-toolkit/skills/ywc-gen-testcase/SKILL.md`
- `plugins/ywc-agent-toolkit/skills/ywc-gen-testcase/evals/evals.json`
- `scripts/run-codex-skill-contract-evals.sh`
- `tests/codex_issue69_contract_test.py`
- `tests/fixtures/codex-issue69/impact-security-evidence/**`

### Shared Surfaces

`tests/codex_issue69_contract_test.py`, `scripts/run-codex-skill-contract-evals.sh`, source/generated synchronization, and shared spec/preview/review contracts. `scripts/validate.sh` wiring is owned only by 63-010. Concurrent Claude task `yw-000058-010-docs-named-agent-release` may edit that validator; rebase and serialize its edits, with no functional dependency on Claude work.

### Conflicts With

- `yw-000063-010-domain-event-monitoring` — shared harness, policy or generated synchronization; never run concurrently.
- `yw-000063-020-domain-spec-review-availability` — shared harness, policy or generated synchronization; never run concurrently.
- `yw-000064-010-domain-conditional-omission-lenses` — shared harness, policy or generated synchronization; never run concurrently.
- `yw-000064-020-domain-spec-failure-evidence` — shared harness, policy or generated synchronization; never run concurrently.
- `yw-000064-030-domain-task-coverage-gate` — shared harness, policy or generated synchronization; never run concurrently.
- `yw-000065-010-domain-bounded-suggestion-policy` — shared harness, policy or generated synchronization; never run concurrently.
- `yw-000065-030-domain-sdk-review-evidence` — shared harness, policy or generated synchronization; never run concurrently.
- `yw-000065-040-domain-trigger-selection-evidence` — shared harness, policy or generated synchronization; never run concurrently.
- `yw-000058-010-docs-named-agent-release` — shared harness, policy or generated synchronization; never run concurrently.

### Parallelizable After

- [yw-000065-010-domain-bounded-suggestion-policy](../yw-000065-010-domain-bounded-suggestion-policy/README.md)

No concurrent ready peer in this batch. Refresh the merged baseline before edits; acceptance gates and any external shared-validator conflict must be resolved first.

### Task Verify

Run trusted commands from the repository root. The focused runner is created by 63-010 before its verification. Run source synchronization before package validation.

- `python3 tests/codex_issue69_contract_test.py`
- `bash scripts/run-codex-skill-contract-evals.sh`
- `bash scripts/check-codex-skill-descriptions.sh`
- `bash scripts/check-codex-agent-evals.sh`
- `bash scripts/validate.sh`
- `bash scripts/install.sh --list --codex`

## Out of Scope

No edits outside Ownership, no task execution during generation, no new dependencies or DB/state migration, no Claude Code changes, and no publishing. Later task requirements must remain with their owners; do not preemptively widen the common harness to demand unimplemented later behavior.
