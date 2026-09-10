# yw-000032-020-domain-task-quality-gate-packet — Implementation Checklist

## Prerequisites
- [ ] `yw-000031-010-docs-quality-gate-contract` is completed and merged.
- [ ] `yw-000032-010-domain-plan-scaffold-quality-declaration` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-task-generator/**`.

## Stop Conditions
- [ ] Stop if a packet field cannot be sourced from the declaration or canonical reference.
- [ ] Stop if a template would emit raw commands, transcripts, full diffs, or placeholder values.

## Hardening Gate
- [ ] Classify as cross-task metadata behavior.
- [ ] Add eval evidence before changing packet rules.
- [ ] Treat the packet as a public interface and return `NEEDS_CONTEXT` for mismatches.
- [ ] Data Integrity Hardening: N/A.

## Implementation Steps
- [ ] Add the conditional Quality Gate Contract section to `references/README.md.template` with state, ownership, IDs/digests, thresholds, evidence paths, and attempt cap.
- [ ] Add the matching bounded-worker handoff checklist to `references/task.md.template` and preserve omission when no contract exists.
- [ ] Update `SKILL.md` metadata and validation rules to mirror the architecture-packet conditional pattern without executing a verifier.
- [ ] Add eval cases proving no placeholder packet, no raw command text, exact Ownership propagation, and exact N/A omission.

## Task Verify
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `rg -n "BEGIN CONDITIONAL SECTION: Quality Gate|approved.*digest|sanitized.*evidence|N/A — no quality gate contract|raw command" codex/skills/ywc-task-generator`

## Verification
- [ ] Contract evals pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] Typecheck/build: N/A — Markdown/eval-only changes.
