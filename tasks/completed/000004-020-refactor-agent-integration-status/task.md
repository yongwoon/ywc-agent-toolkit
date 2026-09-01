# 000004-020-refactor-agent-integration-status — Implementation Checklist

## Prerequisites
- [ ] Confirm this is a root task and no predecessor task is required
- [ ] Read `docs/ywc-plans/codex-toolkit-eval-improvements.md`

## Allowed Edit Scope
- [ ] Edit only the four files listed in `README.md` Ownership
- [ ] If another skill is a better caller, stop and update task scope before editing it

## Stop Conditions
- [ ] Stop if the agent reference would be only decorative and not tied to a real workflow step
- [ ] Stop if adding the Status line weakens existing `NEEDS_CONTEXT` or `BLOCKED` semantics
- [ ] Stop if A7 remains 1 after adding the references

## Implementation Steps

- [ ] **Add root-cause caller reference**
  - [ ] In `codex/skills/ywc-debug-rootcause/SKILL.md`, add concise optional delegation guidance for `ywc-root-cause-analyst`
  - [ ] Specify when to call it: bounded hypothesis/root-cause review after evidence collection
  - [ ] Specify payload: symptom, timeline, evidence, rejected hypotheses, and current candidate cause
  - [ ] Specify expected output status: `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT`

- [ ] **Add security caller reference**
  - [ ] In `codex/skills/ywc-security-audit/SKILL.md`, add concise optional delegation guidance for `ywc-security-engineer`
  - [ ] Specify when to call it: bounded OWASP/security advisor review when delegation is available
  - [ ] Specify payload: trust boundaries, authz/authn flows, external inputs, and suspected risks
  - [ ] Specify expected output status

- [ ] **Normalize agent status output**
  - [ ] Add exact phrase `Status: <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>` to `codex/agents/ywc-performance-engineer.toml`
  - [ ] Add exact phrase `Status: <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>` to `codex/agents/ywc-root-cause-analyst.toml`
  - [ ] Preserve each agent's role-specific guidance around non-DONE statuses

## Task Verify
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json`
- [ ] Confirm no warnings remain for `ywc-performance-engineer` or `ywc-root-cause-analyst`
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --format markdown --target all`
- [ ] Confirm `ywc-root-cause-analyst` and `ywc-security-engineer` show A7 >= 3
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] validation passes (`bash scripts/validate.sh`)
- [ ] inventory gate output has no shared Status line warning for the target agents
- [ ] mechanical score output shows target A7 improvement
