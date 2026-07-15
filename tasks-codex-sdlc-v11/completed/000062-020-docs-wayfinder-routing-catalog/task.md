# 000062-020-docs-wayfinder-routing-catalog — Implementation Checklist

## Prerequisites

- [ ] `000062-010` map/ticket contract is merged.

## Allowed Edit Scope

- [ ] stated routing sections and `codex/skills/README.md` only.

## Stop Conditions

- [ ] routing makes Wayfinder a default implementation or ordinary planning replacement이면 중단한다.
- [ ] task-generator argument/preview text가 필요하면 `000062-030/040` ownership으로 넘긴다.

## Implementation Steps

- [ ] adjacent skills에 Wayfinder activation/anti-trigger와 local handoff를 추가한다.
  - Related AC/FR: AC1, AC2, FR-5.
- [ ] research/plan/spec consumers가 persisted artifact와 unsaved conversational research를 구분하도록 routing pointer를 쓴다.
  - Related AC/FR: AC6, Amendment E.
- [ ] catalog discoverability 및 routing fixture를 업데이트한다.
  - Related AC/FR: AC7.

## Task Verify

- [ ] `rg -n "ywc-wayfinder" codex/skills/{ywc-plan,ywc-brainstorm,ywc-tech-research,ywc-agentic,ywc-spec-ready,ywc-task-generator}/SKILL.md codex/skills/README.md`
  - Expected Passing Signal: activation boundary and catalog entry are present.
  - Pre-change Failing Evidence / Exception: Wayfinder did not exist.
  - Contract/Test Evidence: fixture runner output.
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
  - Expected Passing Signal: routing fixture passes.
  - Pre-change Failing Evidence / Exception: N/A.
  - Contract/Test Evidence: JSON contract check.

## Verification

- [ ] changed skill validators and `bash scripts/validate.sh` pass.
