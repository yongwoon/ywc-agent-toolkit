# 000049-010-docs-iac-author-skill — Implementation Checklist

## Prerequisites

- [ ] `000047-010-infra-cloud-engineer-specialist` is completed.
- [ ] `000048-010-docs-infra-reference-core` is completed.
- [ ] `000048-020-docs-infra-provider-packs` is completed.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-iac-author/**` 안에서만 수정합니다.
- [ ] shared references나 agent files 수정이 필요해지면 중단합니다.

## Stop Conditions

- [ ] `SKILL.md` frontmatter에 `name`, `description` 외 필드가 필요해 보이면 중단합니다.
- [ ] Tier 1 README만으로는 spec scope를 충족할 수 없다고 판단되면 중단합니다.
- [ ] Terraform-only authoring boundary 없이 multi-IaC wording이 필요해지면 중단합니다.

## Hardening Gate

- [ ] Classify this task: docs-only / skill-definition maintenance.
- [ ] Named exception: runtime code 없음. skill validator와 structure checks로 대체합니다.
- [ ] Interface contract: required file set, valid frontmatter, relative shared-reference links, clear dispatch boundary.
- [ ] Critical surface: sibling skill overlap and anti-trigger wording require review.

## Implementation Steps

- [ ] Skill instruction surface를 작성합니다.
  - [ ] `SKILL.md` frontmatter에 `name`, `description`만 두고 triggers, anti-triggers, Terraform-only workflow를 본문에 작성합니다.
  - [ ] `ywc-cloud-engineer` advisory fan-out과 `ywc-infra-review` handoff recommendation을 포함합니다.
  - [ ] Related AC/FR: `AC1`, `AC2`, `AC3`, `AC5`, `AC8`, `FR-1`, `FR-5`, `FR-6`
  - [ ] Contract / Behavior Change: Codex session이 installable IaC authoring skill을 사용할 수 있습니다.
  - [ ] Verification Command / Evidence: `rg -n 'Terraform|ywc-cloud-engineer|ywc-infra-review|Do not use for|ywc-docker-isolate' codex/skills/ywc-iac-author/SKILL.md`
- [ ] Shared reference links와 UI metadata를 작성합니다.
  - [ ] `agents/openai.yaml`에 `display_name`, `short_description`, `default_prompt`를 채웁니다.
  - [ ] `../references/infra/iac/terraform.md`와 provider docs를 body에서 참조합니다.
  - [ ] Related AC/FR: `AC2`, `AC4`, `AC5`, `FR-2`, `FR-5`
  - [ ] Contract / Behavior Change: validator-required metadata와 reference path contract가 충족됩니다.
  - [ ] Verification Command / Evidence: `test -f codex/skills/ywc-iac-author/agents/openai.yaml`
- [ ] Tier 1 README set를 완성합니다.
  - [ ] `README.en.md`를 source로 삼아 `README.md`, `README.ja.md`, `README.ko.md`의 목적/사용 시점/related skill 구조를 맞춥니다.
  - [ ] zh/es 문서가 생성되지 않았는지 확인합니다.
  - [ ] Related AC/FR: `AC2`, `AC9`, `FR-5`
  - [ ] Contract / Behavior Change: user-facing docs가 locale set 요구사항을 만족합니다.
  - [ ] Verification Command / Evidence: `for f in README.md README.en.md README.ja.md README.ko.md; do test -f codex/skills/ywc-iac-author/$f; done`
- [ ] Targeted validation을 실행합니다.
  - [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-iac-author`
  - [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`
  - [ ] Related AC/FR: `AC12`, `FR-7`
  - [ ] Contract / Behavior Change: Codex-only boundary와 skill structure correctness를 early-check합니다.
  - [ ] Verification Command / Evidence: validator output

## Task Verify

- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-iac-author`
  - Expected Passing Signal: skill-local validation passes
  - Pre-change Failing Evidence / Exception: directory absent before task
  - Contract/Test Evidence: validator output
- [ ] `for f in SKILL.md agents/openai.yaml README.md README.en.md README.ja.md README.ko.md; do test -f codex/skills/ywc-iac-author/$f; done`
  - Expected Passing Signal: all required files exist
  - Pre-change Failing Evidence / Exception: new directory absent before task
  - Contract/Test Evidence: file-existence witness
- [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`
  - Expected Passing Signal: no output, exit 0
  - Pre-change Failing Evidence / Exception: unrelated user changes under `claude-code/**` must be called out, not reverted
  - Contract/Test Evidence: scope guard

## Verification

- [ ] edited paths stay within `codex/skills/ywc-iac-author/**`
- [ ] no zh/es README files are created in v1
