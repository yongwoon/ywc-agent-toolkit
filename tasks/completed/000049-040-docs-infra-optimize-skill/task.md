# 000049-040-docs-infra-optimize-skill — Implementation Checklist

## Prerequisites

- [ ] `000047-010-infra-cloud-engineer-specialist` is completed.
- [ ] `000048-010-docs-infra-reference-core` is completed.
- [ ] `000048-020-docs-infra-provider-packs` is completed.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-infra-optimize/**` 안에서만 수정합니다.
- [ ] review skill이나 agent files 수정이 필요해지면 중단합니다.

## Stop Conditions

- [ ] optimization skill이 direct apply or execution worker처럼 서술되어야 한다면 중단합니다.
- [ ] SAFE / CAUTION / DANGER taxonomy 없이도 spec intent가 전달된다고 판단되면 중단합니다.
- [ ] review vs optimize 경계가 명확히 나뉘지 않으면 중단합니다.

## Hardening Gate

- [ ] Classify this task: docs-only / skill-definition maintenance.
- [ ] Named exception: runtime code 없음. validator와 grep witnesses로 대체합니다.
- [ ] Interface contract: conservative optimization planning skill with explicit SAFE/CAUTION/DANGER classification.
- [ ] Critical surface: severity taxonomy and handoff boundaries require manual review.

## Implementation Steps

- [ ] `SKILL.md`의 optimization workflow를 작성합니다.
  - [ ] drift, right-sizing, unused resources, reliability hardening planning과 SAFE / CAUTION / DANGER 분류를 명시합니다.
  - [ ] `ywc-cloud-engineer` advisory path와 `ywc-infra-review` re-check recommendation을 포함합니다.
  - [ ] Related AC/FR: `AC1`, `AC2`, `AC3`, `AC8`, `FR-1`, `FR-6`
  - [ ] Contract / Behavior Change: Codex session이 installable infra optimization skill을 사용하게 됩니다.
  - [ ] Verification Command / Evidence: `rg -n 'SAFE|CAUTION|DANGER|ywc-cloud-engineer|ywc-infra-review|Do not use for' codex/skills/ywc-infra-optimize/SKILL.md`
- [ ] Shared reference links와 anti-trigger matrix를 정리합니다.
  - [ ] core lens docs와 provider docs를 body에 링크하고 `ywc-docker-isolate` 비대상 조건을 적습니다.
  - [ ] design/author/review sibling skill 경계를 분리합니다.
  - [ ] Related AC/FR: `AC4`, `AC8`, `FR-2`, `FR-6`
  - [ ] Contract / Behavior Change: unsafe expectation 없이 optimization skill positioning이 명확해집니다.
  - [ ] Verification Command / Evidence: `rg -n '../references/infra|ywc-docker-isolate|ywc-iac-author|ywc-infra-review|ywc-infra-design' codex/skills/ywc-infra-optimize/SKILL.md`
- [ ] UI metadata와 Tier 1 README set를 작성합니다.
  - [ ] `agents/openai.yaml`를 채우고 README 4종에서 purpose, when-to-use, related skills 구조를 정렬합니다.
  - [ ] zh/es 문서가 생성되지 않았는지 확인합니다.
  - [ ] Related AC/FR: `AC2`, `AC9`, `FR-5`
  - [ ] Contract / Behavior Change: installable user-facing docs와 metadata가 완성됩니다.
  - [ ] Verification Command / Evidence: `for f in README.md README.en.md README.ja.md README.ko.md; do test -f codex/skills/ywc-infra-optimize/$f; done`
- [ ] Targeted validation을 실행합니다.
  - [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-infra-optimize`
  - [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`
  - [ ] Related AC/FR: `AC12`, `FR-7`
  - [ ] Contract / Behavior Change: Codex-only boundary와 skill structure correctness를 early-check합니다.
  - [ ] Verification Command / Evidence: validator output

## Task Verify

- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-infra-optimize`
  - Expected Passing Signal: skill-local validation passes
  - Pre-change Failing Evidence / Exception: directory absent before task
  - Contract/Test Evidence: validator output
- [ ] `rg -n 'SAFE|CAUTION|DANGER|ywc-cloud-engineer|ywc-infra-review' codex/skills/ywc-infra-optimize/SKILL.md`
  - Expected Passing Signal: optimization taxonomy and handoff names are present
  - Pre-change Failing Evidence / Exception: file absent before task
  - Contract/Test Evidence: grep witness
- [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`
  - Expected Passing Signal: no output, exit 0
  - Pre-change Failing Evidence / Exception: unrelated user changes under `claude-code/**` must be called out, not reverted
  - Contract/Test Evidence: scope guard

## Verification

- [ ] edited paths stay within `codex/skills/ywc-infra-optimize/**`
- [ ] no review or agent files are modified here
