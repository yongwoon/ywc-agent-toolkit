# 000005-010-test-evaluation-report-refresh — Implementation Checklist

## Prerequisites
- [ ] `000004-010-refactor-skill-s5-contracts` 완료(merge) 확인
- [ ] `000004-020-refactor-agent-integration-status` 완료(merge) 확인
- [ ] `000004-030-test-trigger-fixture-coverage` 완료(merge) 확인

## Allowed Edit Scope
- [ ] Edit only `docs/skill-agent-eval/codex/**`
- [ ] If source skill, agent, or fixture changes are still required, stop and return to the predecessor task

## Stop Conditions
- [ ] Stop if any FR-1 target skill remains below S5 3
- [ ] Stop if `ywc-root-cause-analyst` or `ywc-security-engineer` remains below A7 3
- [ ] Stop if inventory warnings remain for `ywc-performance-engineer` or `ywc-root-cause-analyst`
- [ ] Stop if `bash scripts/validate.sh` fails

## Implementation Steps

- [ ] **Run evaluator checks**
  - [ ] Run `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json`
  - [ ] Run `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --format markdown --target all`
  - [ ] Run `bash scripts/validate.sh`

- [ ] **Analyze acceptance criteria**
  - [ ] Confirm no structural gate failures
  - [ ] Confirm no target agent shared Status line warnings
  - [ ] Confirm all FR-1 target skills have S5 >= 3
  - [ ] Confirm `ywc-root-cause-analyst` and `ywc-security-engineer` have A7 >= 3
  - [ ] Confirm trigger fixture expansion is documented as complete or note residual reference-ideal gap

- [ ] **Write post-change report**
  - [ ] Create a new dated report under `docs/skill-agent-eval/codex/`
  - [ ] Preserve `docs/skill-agent-eval/codex/2026-06-13-full-sweep.md` as pre-change evidence
  - [ ] Include command outputs summarized enough for review
  - [ ] Include any remaining warnings or judgment-pass limitations

- [ ] **Update scoreboard**
  - [ ] Update `docs/skill-agent-eval/codex/scoreboard.md` with post-improvement scores
  - [ ] Cross-check scoreboard against the new report

## Task Verify
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json`
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --format markdown --target all`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] inventory gate passes with target warnings cleared
- [ ] mechanical score output satisfies S5/A7 acceptance criteria
- [ ] repository validation passes (`bash scripts/validate.sh`)
