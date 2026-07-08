# 000044-020-docs-infra-shared-references

## Purpose
4개 인프라 스킬이 공유 참조하는 reference 문서를 저작한다: 프로바이더 4종(AWS/GCP/Azure/K8s, Terraform provider 관점), Terraform 도구 가이드, 3-lens(security/cost/reliability).

## Scope
- `references/providers/{aws,gcp,azure,k8s}.md`
- `references/iac-tools/terraform.md`
- `references/lenses/{security,cost,reliability}.md`
(저장 위치는 아래 Notes의 결정에 따른다.)

## Spec Reference
### Primary Sources
- `docs/ywc-plans/infra-skill-suite-design.md` §1 (공유 프로바이더 reference 아키텍처), §7 (Terraform 단일 고정, 4-provider)
### Summary
프로바이더 차이를 SKILL.md에 넣지 않고 Progressive Disclosure(Pattern 2)로 분리. 각 프로바이더 파일은 Terraform provider 관점으로 기술한다.
### Out of Scope (from spec)
CDK/Pulumi/CFN/Bicep/Helm reference는 저작하지 않음(§7 Terraform 단일 고정).

## Criticality
normal

## Dependencies
- **Depends On**: (None)
- **Depended By**: `000045-020`, `000045-030`, `000045-040`, `000045-050` (모든 스킬이 링크), `000045-010` (lens taxonomy 공유)

## Key Files
- `references/providers/aws.md`, `gcp.md`, `azure.md`, `k8s.md`
- `references/iac-tools/terraform.md`
- `references/lenses/security.md`, `cost.md`, `reliability.md`

## Notes
- **저장 위치 결정 필요**: CC 스킬은 설치 시 각 스킬 디렉터리를 독립 복사한다. 공유 refs를 (a) 각 스킬 `references/`에 복제할지, (b) `claude-code/skills/references/` + `codex/skills/references/`(validate.sh가 존재를 강제) 공유 위치에 둘지 결정하고 Implementation Steps에서 확정한다. 기본안: 공유 위치 저작 후 각 스킬에서 링크.

## Out of Scope
- SKILL.md 저작 — 각 스킬 태스크.

## Parallel Execution Metadata
- **Ownership**: `references/providers/**`, `references/iac-tools/terraform.md`, `references/lenses/**` (또는 확정된 공유 경로)
- **Shared Surfaces**: `codex/skills/references/` (validate.sh 강제 대상)
- **Conflicts With**: (None identified)
- **Parallelizable After**: (batch baseline)
- **Task Verify**: `test -f references/iac-tools/terraform.md && bash scripts/validate.sh`
