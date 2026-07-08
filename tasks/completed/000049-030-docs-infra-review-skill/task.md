# 000049-030-docs-infra-review-skill — Implementation Checklist

## Prerequisites

- [ ] `000047-010-infra-cloud-engineer-specialist` is completed.
- [ ] `000047-020-infra-agent-lens-extensions` is completed.
- [ ] `000048-010-docs-infra-reference-core` is completed.
- [ ] `000048-020-docs-infra-provider-packs` is completed.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-infra-review/**` 안에서만 수정합니다.
- [ ] specialist agent names나 wording이 잘못되었다고 느껴져도 agent files는 여기서 수정하지 않습니다.

## Stop Conditions

- [ ] review skill이 직접 findings를 생성하는 대신 specialist dispatch 없이 독자적으로 모든 렌즈를 흡수해야 한다면 중단합니다.
- [ ] reliability lens가 security/performance agent 중 하나에 흡수되어야 한다면 중단합니다.
- [ ] CRITICAL/HIGH apply-blocking policy를 spec과 다르게 완화해야만 한다면 중단합니다.

## Hardening Gate

- [ ] Classify this task: docs-only / skill-definition maintenance on critical routing surface.
- [ ] Named exception: runtime code 없음. validator, grep witnesses, reviewer diff inspection으로 대체합니다.
- [ ] Interface contract: explicit dispatch to `ywc-security-engineer`, `ywc-performance-engineer`, `ywc-cloud-engineer`; conservative escalation policy.
- [ ] Critical surface: specialist names, severity policy, anti-trigger wording require manual review.

## Implementation Steps

- [ ] `SKILL.md`의 review workflow를 작성합니다.
  - [ ] security/cost/reliability lens fan-out과 bounded evidence packet expectations를 적습니다.
  - [ ] CRITICAL/HIGH findings 시 apply 차단 권고를 명시합니다.
  - [ ] Related AC/FR: `AC1`, `AC2`, `AC3`, `AC8`, `FR-1`, `FR-6`
  - [ ] Contract / Behavior Change: Codex session이 installable infra review skill을 사용하게 됩니다.
  - [ ] Verification Command / Evidence: `rg -n 'ywc-security-engineer|ywc-performance-engineer|ywc-cloud-engineer|CRITICAL|HIGH|Do not use for' codex/skills/ywc-infra-review/SKILL.md`
- [ ] Shared references와 anti-trigger matrix를 연결합니다.
  - [ ] core lenses와 provider docs를 body에 링크하고 `ywc-docker-isolate` 비대상 조건을 적습니다.
  - [ ] authoring/optimization/design sibling skill boundary를 분리합니다.
  - [ ] Related AC/FR: `AC4`, `AC8`, `FR-2`, `FR-6`
  - [ ] Contract / Behavior Change: skill routing ambiguity가 줄어듭니다.
  - [ ] Verification Command / Evidence: `rg -n '../references/infra|ywc-docker-isolate|ywc-iac-author|ywc-infra-optimize|ywc-infra-design' codex/skills/ywc-infra-review/SKILL.md`
- [ ] UI metadata와 Tier 1 README set를 작성합니다.
  - [ ] `agents/openai.yaml`를 채우고 README 4종에서 purpose, when-to-use, related skills 구조를 정렬합니다.
  - [ ] zh/es 문서가 생성되지 않았는지 확인합니다.
  - [ ] Related AC/FR: `AC2`, `AC9`, `FR-5`
  - [ ] Contract / Behavior Change: installable user-facing docs와 metadata가 완성됩니다.
  - [ ] Verification Command / Evidence: `for f in README.md README.en.md README.ja.md README.ko.md; do test -f codex/skills/ywc-infra-review/$f; done`
- [ ] Targeted validation을 실행합니다.
  - [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-infra-review`
  - [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`
  - [ ] Related AC/FR: `AC12`, `FR-7`
  - [ ] Contract / Behavior Change: Codex-only boundary와 skill structure correctness를 early-check합니다.
  - [ ] Verification Command / Evidence: validator output

## Task Verify

- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-infra-review`
  - Expected Passing Signal: skill-local validation passes
  - Pre-change Failing Evidence / Exception: directory absent before task
  - Contract/Test Evidence: validator output
- [ ] `rg -n 'ywc-security-engineer|ywc-performance-engineer|ywc-cloud-engineer|CRITICAL|HIGH' codex/skills/ywc-infra-review/SKILL.md`
  - Expected Passing Signal: dispatch names and escalation policy are present
  - Pre-change Failing Evidence / Exception: file absent before task
  - Contract/Test Evidence: grep witness
- [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`
  - Expected Passing Signal: no output, exit 0
  - Pre-change Failing Evidence / Exception: unrelated user changes under `claude-code/**` must be called out, not reverted
  - Contract/Test Evidence: scope guard

## Verification

- [ ] edited paths stay within `codex/skills/ywc-infra-review/**`
- [ ] no specialist agent files are modified here
