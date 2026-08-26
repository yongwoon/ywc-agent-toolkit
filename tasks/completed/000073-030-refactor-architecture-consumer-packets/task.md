# 000073-030-refactor-architecture-consumer-packets — Implementation Checklist

## Prerequisites
- [ ] `000073-010-domain-architecture-invariants-contract` is completed and merged.

## Allowed Edit Scope
- [ ] Modify only the four listed consumer/agent surfaces and their focused eval metadata.
- [ ] Use the shared helper; do not copy schema or verdict evaluation logic into a consumer.

## Stop Conditions
- [ ] Stop if a consumer needs broad repository scanning to derive changed paths.
- [ ] Stop if raw evidence contents, command text, or transcript data would enter a packet.
- [ ] Stop if no-manifest fallback would change existing behavior.

## Hardening Gate
- RED-first evidence: add or update routing fixtures for manifest/evidence pairing before changing dispatch text.
- Public contract: document the exact forwarded packet and architect output fields.
- Data Integrity Hardening: N/A — no persistence/schema change.
- Critical review: inspect all dispatch boundaries for raw evidence leakage and fabricated violations.

## Implementation Steps
- [ ] Add paired `--manifest` and `--architecture-evidence` handling to `ywc-code-gen`, `ywc-task-generator`, and `ywc-impl-review`, deriving changed paths only from each existing bounded file list.
  - Related AC/FR: AC4, AC5 / Iteration 2 D
  - Contract / Behavior Change: valid paired inputs produce a sanitized invariant packet; absent inputs preserve current flow.
  - Verification Command / Evidence: targeted eval cases for positive, missing, and invalid evidence.
- [ ] Route `contract_state`, affected component/rule IDs, evidence artifact path, and aggregate verdict from the shared helper without forwarding evidence contents.
  - Related AC/FR: AC3, AC5, AC7 / Iteration 2 C–D
  - Contract / Behavior Change: `VIOLATED` uses the normal finding/error channel; `NEEDS_CONTEXT` stops before dispatch.
  - Verification Command / Evidence: packet-shape grep/eval and bounded-dispatch review.
- [ ] Update `codex/skills/ywc-task-generator/SKILL.md` metadata/checklist rules to record component ownership, affected rules, and verifier requirement without reimplementing verifier logic.
  - Related AC/FR: AC5 / FR-4
  - Contract / Behavior Change: generated task metadata can carry architecture ownership context safely.
  - Verification Command / Evidence: task-generator contract evals pass.
- [ ] Update `codex/agents/ywc-architect.toml` to emit `Status`, `Invariant Verdict`, `Rules`, `Evidence`, and `Next action` within 300 words and to preserve `N/A — no architecture contract`.
  - Related AC/FR: AC6 / Iteration 2 E
  - Contract / Behavior Change: architect consumes a bounded packet and never audits independently.
  - Verification Command / Evidence: architect status/verdict fixture cases pass.

## Task Verify
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
  - Expected Passing Signal: all affected skill eval inventories pass shape and required routing tokens.
  - Pre-change Failing Evidence / Exception: RED routing fixtures must cover paired-input and no-evidence behavior.
  - Contract/Test Evidence: bounded packet and architect output assertions.
- [ ] `bash scripts/validate.sh`
  - Expected Passing Signal: repository validation exits 0 after source-only changes.
  - Pre-change Failing Evidence / Exception: N/A — validation is the integration gate.
  - Contract/Test Evidence: metadata, descriptions, and package source checks pass.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — Markdown/TOML/JSON contract changes)
- [ ] unit tests pass (consumer eval fixtures)
- [ ] integration tests pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] app builds without error (N/A — generated package is handled by `000074-010`)
