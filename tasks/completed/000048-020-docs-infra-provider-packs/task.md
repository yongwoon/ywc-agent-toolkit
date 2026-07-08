# 000048-020-docs-infra-provider-packs — Implementation Checklist

## Prerequisites

- [ ] `000048-010-docs-infra-reference-core` is completed.

## Allowed Edit Scope

- [ ] `codex/skills/references/infra/providers/aws.md`
- [ ] `codex/skills/references/infra/providers/gcp.md`
- [ ] `codex/skills/references/infra/providers/azure.md`
- [ ] `codex/skills/references/infra/providers/k8s.md`
- [ ] core reference files 수정이 필요해지면 중단하고 이전 task로 되돌립니다.

## Stop Conditions

- [ ] provider 문서가 Terraform provider 범위를 넘어 Helm general guide나 multi-tool guide로 확장되면 중단합니다.
- [ ] 하나 이상의 provider가 동일 template 복붙으로만 채워져 real differentiation이 없으면 중단합니다.
- [ ] link path를 맞추기 위해 skill directories까지 건드려야 한다면 중단합니다.

## Hardening Gate

- [ ] Classify this task: docs-only shared-contract authoring with mid-plan validation spot-check.
- [ ] Named exception: runtime code 없음. file checks, grep witnesses, validator spot-check로 대체합니다.
- [ ] Interface contract: provider docs live under `codex/skills/references/infra/providers/**` and are linked by downstream skills.
- [ ] Critical surface: Terraform-only provider framing must remain intact.

## Implementation Steps

- [ ] Provider directory와 file paths를 spec과 일치시킵니다.
  - [ ] `aws.md`, `gcp.md`, `azure.md`, `k8s.md` 경로를 정확히 맞춥니다.
  - [ ] Related AC/FR: `AC4`, `FR-2`
  - [ ] Contract / Behavior Change: downstream skills가 stable provider links를 사용합니다.
  - [ ] Verification Command / Evidence: `find codex/skills/references/infra/providers -maxdepth 1 -type f | sort`
- [ ] AWS/GCP/Azure provider docs를 작성합니다.
  - [ ] account/project/subscription boundaries, IAM/network/state considerations, common Terraform module cautions를 provider별로 구분해 적습니다.
  - [ ] Related AC/FR: `AC4`, `AC5`, `FR-2`
  - [ ] Contract / Behavior Change: design/author/review skills가 provider-specific reference를 읽고 ambiguity를 줄입니다.
  - [ ] Verification Command / Evidence: `rg -n 'AWS|GCP|Azure|IAM|VPC|network|subscription|project' codex/skills/references/infra/providers`
- [ ] Kubernetes provider doc를 작성하고 mid-plan validation을 수행합니다.
  - [ ] Terraform provider 관점의 cluster, namespace, RBAC, ingress/service boundary, rollout caution을 정리합니다.
  - [ ] `bash scripts/validate.sh`를 한 번 실행해 shared reference path와 bundle 구조가 깨지지 않았는지 spot-check합니다.
  - [ ] Related AC/FR: `AC4`, `AC5`, `FR-2`, `FR-7`
  - [ ] Contract / Behavior Change: downstream skill authoring 전에 shared reference layer의 structural drift를 조기에 발견합니다.
  - [ ] Verification Command / Evidence: `bash scripts/validate.sh`

## Task Verify

- [ ] `for f in codex/skills/references/infra/providers/aws.md codex/skills/references/infra/providers/gcp.md codex/skills/references/infra/providers/azure.md codex/skills/references/infra/providers/k8s.md; do test -f "$f"; done`
  - Expected Passing Signal: all provider files exist
  - Pre-change Failing Evidence / Exception: new files absent before task
  - Contract/Test Evidence: file-existence witness
- [ ] `rg -n 'Terraform|provider|IAM|network|state|module|cluster|RBAC' codex/skills/references/infra/providers`
  - Expected Passing Signal: provider docs contain expected provider-specific vocabulary
  - Pre-change Failing Evidence / Exception: directory absent or empty before task
  - Contract/Test Evidence: grep witness
- [ ] `bash scripts/validate.sh`
  - Expected Passing Signal: exit 0 or only unrelated pre-existing failures explicitly identified
  - Pre-change Failing Evidence / Exception: repository-level gate may include unrelated pending work
  - Contract/Test Evidence: mid-plan structural validation

## Verification

- [ ] edited paths stay inside `codex/skills/references/infra/providers/**`
- [ ] no skill-local copies of provider docs are created
