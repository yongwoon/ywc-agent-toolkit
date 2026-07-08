# 000049-020-docs-infra-design-skill — Implementation Checklist

## Prerequisites

- [ ] `000048-010-docs-infra-reference-core` is completed.
- [ ] `000048-020-docs-infra-provider-packs` is completed.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-infra-design/**` 안에서만 수정합니다.
- [ ] provider/core references나 agent files 수정이 필요해지면 중단합니다.

## Stop Conditions

- [ ] design skill이 Terraform code authoring까지 포함해야 한다면 중단합니다.
- [ ] `ywc-architect`와의 경계가 불명확해 irreversible verdict를 skill이 직접 내려야 한다면 중단합니다.
- [ ] Tier 1 README 구조를 맞추기 위해 README locale meaning drift가 생기면 중단합니다.

## Hardening Gate

- [ ] Classify this task: docs-only / skill-definition maintenance.
- [ ] Named exception: runtime code 없음. validator와 grep witnesses로 대체합니다.
- [ ] Interface contract: required skill file set, clear anti-trigger matrix, relative shared-reference links.
- [ ] Critical surface: design-vs-authoring-vs-architect routing boundary requires review.

## Implementation Steps

- [ ] `SKILL.md`를 작성합니다.
  - [ ] design triggers, anti-triggers, provider Progressive Disclosure, topology/trade-off output expectations을 넣습니다.
  - [ ] `ywc-iac-author`로 authoring handoff, `ywc-architect`로 irreversible architecture verdict handoff를 구분합니다.
  - [ ] Related AC/FR: `AC1`, `AC2`, `AC3`, `AC8`, `FR-1`, `FR-6`
  - [ ] Contract / Behavior Change: Codex session이 design-specific infra skill을 사용하게 됩니다.
  - [ ] Verification Command / Evidence: `rg -n 'ywc-iac-author|ywc-architect|Do not use for|ywc-docker-isolate' codex/skills/ywc-infra-design/SKILL.md`
- [ ] UI metadata와 shared reference links를 작성합니다.
  - [ ] `agents/openai.yaml`의 세 필드를 채우고 provider/core reference paths를 body에서 링크합니다.
  - [ ] Related AC/FR: `AC2`, `AC4`, `FR-2`, `FR-5`
  - [ ] Contract / Behavior Change: installable Codex surface와 stable relative links가 제공됩니다.
  - [ ] Verification Command / Evidence: `test -f codex/skills/ywc-infra-design/agents/openai.yaml`
- [ ] Tier 1 README set를 작성하고 검증합니다.
  - [ ] `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`의 purpose, usage timing, related skills sections를 정렬합니다.
  - [ ] zh/es 문서가 생성되지 않았는지 확인합니다.
  - [ ] Related AC/FR: `AC2`, `AC9`, `FR-5`
  - [ ] Contract / Behavior Change: locale docs가 동일한 구조와 의미를 유지합니다.
  - [ ] Verification Command / Evidence: `for f in README.md README.en.md README.ja.md README.ko.md; do test -f codex/skills/ywc-infra-design/$f; done`
- [ ] Targeted validation을 실행합니다.
  - [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-infra-design`
  - [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`
  - [ ] Related AC/FR: `AC12`, `FR-7`
  - [ ] Contract / Behavior Change: Codex-only boundary와 skill structure correctness를 early-check합니다.
  - [ ] Verification Command / Evidence: validator output

## Task Verify

- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-infra-design`
  - Expected Passing Signal: skill-local validation passes
  - Pre-change Failing Evidence / Exception: directory absent before task
  - Contract/Test Evidence: validator output
- [ ] `for f in SKILL.md agents/openai.yaml README.md README.en.md README.ja.md README.ko.md; do test -f codex/skills/ywc-infra-design/$f; done`
  - Expected Passing Signal: all required files exist
  - Pre-change Failing Evidence / Exception: new directory absent before task
  - Contract/Test Evidence: file-existence witness
- [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`
  - Expected Passing Signal: no output, exit 0
  - Pre-change Failing Evidence / Exception: unrelated user changes under `claude-code/**` must be called out, not reverted
  - Contract/Test Evidence: scope guard

## Verification

- [ ] edited paths stay within `codex/skills/ywc-infra-design/**`
- [ ] no provider or agent files are changed here
