# 000004-030-test-trigger-fixture-coverage — Implementation Checklist

## Prerequisites
- [ ] Confirm this is a root task and no predecessor task is required
- [ ] Read `docs/ywc-plans/codex-toolkit-eval-improvements.md`
- [ ] Read `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md`

## Allowed Edit Scope
- [ ] Stay within `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json`
- [ ] Edit `trigger-eval-method.md` only if fixture convention and reference text are inconsistent

## Stop Conditions
- [ ] Stop if the existing JSON schema is unclear or incompatible with the intended case shape
- [ ] Stop if a collision case cannot name the expected skill/agent and the excluded sibling clearly
- [ ] Stop if fixture additions become a broad rewrite rather than coverage expansion

## Implementation Steps

- [ ] **Inventory evaluated items**
  - [ ] List all 39 Codex skills from `codex/skills/*`
  - [ ] List all 7 Codex agents from `codex/agents/*.toml`
  - [ ] Compare them against existing `trigger-cases.json`

- [ ] **Add positive coverage**
  - [ ] Add at least one realistic positive case for every missing Codex skill
  - [ ] Add at least one realistic positive case for every missing Codex agent
  - [ ] Use stable, deterministic case ids

- [ ] **Add collision coverage**
  - [ ] Add cases for plan/spec/task sibling group
  - [ ] Add cases for commit/create-pr/handle-pr/release-pr-list sibling group
  - [ ] Add cases for impl-review/security-audit/ui-ux-review/product-review sibling group
  - [ ] Add cases for language reviewer agents
  - [ ] Add cases for architect/performance/security/root-cause advisor agents

- [ ] **Validate JSON and coverage**
  - [ ] Run JSON syntax validation
  - [ ] Count cases and confirm each evaluated item has positive coverage
  - [ ] Preserve existing cases unless clearly incorrect

## Task Verify
- [ ] `python3 -m json.tool tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json >/dev/null`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] JSON syntax validation passes
- [ ] repository validation passes (`bash scripts/validate.sh`)
- [ ] no evaluator baseline update is performed
