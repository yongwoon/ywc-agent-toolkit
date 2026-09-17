# yw-000043-020-docs-document-gate-ledger-escalation

## Purpose
Document the newly-ported Executable Gate Ledger (from `yw-000043-010`) as an optional escalation inside `ywc-verify-done`'s own SKILL.md and Korean README, so the calling LLM discovers the mechanism, understands it is strictly optional (Steps 1–6 remain the unchanged default path), and sees the shell-execution security warning before ever pointing `gate-check.py` at a ledger it did not author.

## Scope
- Add one `## Optional Escalation: Executable Gate Ledger` section to `claude-code/skills/ywc-verify-done/SKILL.md`, inserted after `### Step 6: On failure, classify and route` and before `## Integration`.
- Append the two upstream **Common Mistakes** bullets ("Trusting an absence check without a positive control", "Copying a supplied number into the claim instead of recomputing it") to the existing `## Common Mistakes` section.
- Add one row for `references/gate-ledger.md` to the existing `## References` table in SKILL.md.
- Add one Korean paragraph section (`## Optional: Executable Gate Ledger`) to `claude-code/skills/ywc-verify-done/README.md`, positioned after `## 무엇을 하나요` and before `## 언제 trigger 되나요`.
- Per FR-7: invoke `ywc-skill-author` before finalizing the SKILL.md edit, per `claude-code/skills/CLAUDE.md`'s "Authoring or Restructuring `ywc-*` Skills" rule (this edit adds a new body section and a new `references/` file — not an ad-hoc minor edit that would qualify for the exemption).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260917-verify-done-gate-ledger-port.md` — FR-2, FR-3, FR-4 (References row only), FR-6, FR-7, Existing Constraints Touched table, AC8
- Upstream source (read directly, sibling checkout `/Users/yongwoon.kim/Desktop/yongwoon/source/private/develop-with-llm`): the equivalent `## Optional Escalation: Executable Gate Ledger` SKILL.md section, Common Mistakes bullets, and README paragraph in `tools/claude-code/skills/ywc-verify-done/SKILL.md` and `README.md`
- `claude-code/skills/ywc-verify-done/SKILL.md` (this repo's current file — confirmed structurally identical Step 1–6 shape to upstream's pre-port version)
- `claude-code/skills/CLAUDE.md` §"Authoring or Restructuring `ywc-*` Skills" (governs the FR-7 process requirement)

### Summary
This task is a documentation-only change confined to `ywc-verify-done`'s own SKILL.md and README.md. It must preserve upstream's explicit framing that the ledger is optional and that Steps 1–6 remain unchanged, name the three invocation modes with this repo's path (`claude-code/skills/ywc-verify-done/scripts/gate-check.py`, established by `yw-000043-010`), and repeat the shell-execution security warning rather than only linking to `references/gate-ledger.md` once. The SKILL.md edit must go through `ywc-skill-author` per this repo's own skill-authoring discipline rule (FR-7), since it is more than an ad-hoc minor edit.

### Out of Scope (from spec)
- `gate-check.py`, `test_gate_check.py`, `references/gate-ledger.md` content — handled by `yw-000043-010-infra-port-gate-ledger-script`
- The existing 5-step prose Gate Function, Forbidden Vocabulary table, Rationalization Defense table, and Claim Classification table — strictly unchanged
- Localized README variants (`README.en.md`, `README.ja.md`, `README.ko.md`) and Tier 2 (`README.zh.md`, `README.es.md`) — the escalation summary is added only to the Korean-default `README.md`, matching this repo's precedent for small ports
- `codex/skills/ywc-verify-done/` and `plugins/ywc-agent-toolkit/skills/ywc-verify-done/` — out of scope for the whole spec

## Criticality
`normal` — this task only edits skill documentation/instruction prose; it repeats (does not introduce) the security warning about the ported script's shell execution. The underlying critical surface belongs to `yw-000043-010`'s `gate-check.py`, not to this task's Ownership.

## Dependencies

### Depends On
- `yw-000043-010-infra-port-gate-ledger-script` — provides `references/gate-ledger.md` (this task's new References table row points at it, and the SKILL.md section's format-spec pointer must reference an existing file) and the confirmed script path/CLI invocation modes this task documents

### Depended By
- (None — leaf task)

## Key Files
- `claude-code/skills/ywc-verify-done/SKILL.md` — new `## Optional Escalation` section, two new Common Mistakes bullets, one new References row
- `claude-code/skills/ywc-verify-done/README.md` — one new Korean section

## Notes
- Do not touch the Claim Classification table — the spec explicitly notes upstream's own current SKILL.md has since drifted further (a `detect-bot-presence.sh` mention this repo doesn't have) from an unrelated later change; this port does not follow that drift.
- The `## Optional Escalation` section's insertion point is between end of Step 6 (after line ~145) and `## Integration` (line ~146) in this repo's current file — confirmed by direct read during spec authoring; re-confirm the exact line numbers before editing since `yw-000043-010` does not touch SKILL.md and line numbers should be stable, but always re-read the file first.
- The References table's new row is the second row, after `verification-block-examples.md` and before the two `../references/` shared-file rows — matching upstream's row ordering.
- README.md's Korean section must use Korean prose with English technical terms preserved (no transliteration), per `claude-code/skills/CLAUDE.md` §"Writing Rules" — this differs from SKILL.md, which is English-only.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-verify-done/SKILL.md`
- `claude-code/skills/ywc-verify-done/README.md`

### Owned Interface
- (None — no public interface owned; this task only adds prose/documentation)

### Shared Surfaces
- (None identified — both files are exclusively owned by the `ywc-verify-done` skill directory)

### Conflicts With
- (None identified)

### Parallelizable After
- `yw-000043-010-infra-port-gate-ledger-script`

### Task Verify
- `bash scripts/validate.sh` (AC8 — no new errors for `ywc-verify-done`, `Skill is valid!` or equivalent zero-`ERROR` output)
- `grep -n "gate-ledger.md" claude-code/skills/ywc-verify-done/SKILL.md` (confirms the new References row exists)
- `grep -n "Optional Escalation" claude-code/skills/ywc-verify-done/SKILL.md` (confirms the new section exists)

## Out of Scope
- Any change to `gate-check.py`, `test_gate_check.py`, or `references/gate-ledger.md` content (owned by `yw-000043-010`)
- Any change to the existing 5-step prose Gate Function, Forbidden Vocabulary table, Rationalization Defense table, or Claim Classification table
- Translating the new README section into `README.en.md`, `README.ja.md`, or `README.ko.md`
