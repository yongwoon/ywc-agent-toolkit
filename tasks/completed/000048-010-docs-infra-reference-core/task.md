# 000048-010-docs-infra-reference-core — Implementation Checklist

## Prerequisites

- [ ] `000047-010-infra-cloud-engineer-specialist` is completed.
- [ ] `000047-020-infra-agent-lens-extensions` is completed.

## Allowed Edit Scope

- [ ] `codex/skills/references/infra/iac/terraform.md`
- [ ] `codex/skills/references/infra/lenses/security.md`
- [ ] `codex/skills/references/infra/lenses/cost.md`
- [ ] `codex/skills/references/infra/lenses/reliability.md`
- [ ] provider docs나 skill directories로 범위가 번지면 중단합니다.

## Stop Conditions

- [ ] Terraform-only 전략을 유지할 수 없다고 판단되면 중단합니다.
- [ ] lens taxonomy가 agent wording과 충돌하면 중단합니다.
- [ ] provider-specific detail이 core reference에 반드시 들어가야 한다면 중단합니다.

## Hardening Gate

- [ ] Classify this task: docs-only shared-contract authoring.
- [ ] Named exception: runtime code 없음. reference path validation과 diff review로 대체합니다.
- [ ] Interface contract: stable shared reference paths under `codex/skills/references/infra/**`.
- [ ] Critical surface: Terraform-only boundary and lens vocabulary require manual review.

## Implementation Steps

- [ ] Infra reference directory skeleton을 고정합니다.
  - [ ] `codex/skills/references/infra/iac/`와 `codex/skills/references/infra/lenses/` 아래 파일 경로를 spec 이름과 정확히 일치시킵니다.
  - [ ] Related AC/FR: `AC4`, `FR-2`
  - [ ] Contract / Behavior Change: downstream SKILL.md가 stable relative path를 링크할 수 있습니다.
  - [ ] Verification Command / Evidence: `find codex/skills/references/infra -maxdepth 3 -type f | sort`
- [ ] `iac/terraform.md`를 작성합니다.
  - [ ] Terraform-only strategy, provider coverage, `terraform validate`, `terraform plan`, blast-radius summary expectations을 적습니다.
  - [ ] Related AC/FR: `AC4`, `AC5`, `FR-2`
  - [ ] Contract / Behavior Change: `ywc-iac-author`와 related skills가 공통 IaC baseline을 참조합니다.
  - [ ] Verification Command / Evidence: `rg -n 'Terraform only|terraform validate|terraform plan|blast-radius' codex/skills/references/infra/iac/terraform.md`
- [ ] Lens 문서 세 개를 작성합니다.
  - [ ] `security.md`에 public exposure, IAM/RBAC over-privilege, secrets/state 관점을 적습니다.
  - [ ] `cost.md`에 right-sizing, reserved/spot, idle resources, transfer cost 관점을 적습니다.
  - [ ] `reliability.md`에 availability, rollback, failure domain, dependency blast radius 관점을 적습니다.
  - [ ] Related AC/FR: `AC4`, `FR-2`
  - [ ] Contract / Behavior Change: review/optimize skills가 공통 lens taxonomy를 공유합니다.
  - [ ] Verification Command / Evidence: `rg -n 'public|IAM|RBAC|state|right-sizing|reserved|spot|idle|transfer|rollback|blast radius' codex/skills/references/infra/lenses`

## Task Verify

- [ ] `for f in codex/skills/references/infra/iac/terraform.md codex/skills/references/infra/lenses/security.md codex/skills/references/infra/lenses/cost.md codex/skills/references/infra/lenses/reliability.md; do test -f \"$f\"; done`
  - Expected Passing Signal: all core reference files exist
  - Pre-change Failing Evidence / Exception: new files absent before task
  - Contract/Test Evidence: file-existence witness
- [ ] `rg -n 'Terraform|terraform validate|terraform plan|security|cost|reliability' codex/skills/references/infra`
  - Expected Passing Signal: expected vocabulary appears in the new docs
  - Pre-change Failing Evidence / Exception: directory absent or empty before task
  - Contract/Test Evidence: grep witness
- [ ] `bash scripts/validate.sh`
  - Expected Passing Signal: exit 0 or only unrelated pre-existing failures explicitly identified
  - Pre-change Failing Evidence / Exception: repository-level gate may include unrelated pending work
  - Contract/Test Evidence: reference-path validation

## Verification

- [ ] core reference files are the only edited paths under `codex/skills/references/infra/**`
- [ ] no provider docs or skill docs are authored in this task
