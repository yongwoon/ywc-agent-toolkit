# task: 000044-020-docs-infra-shared-references

## Prerequisites
- [ ] (없음)

## Allowed Edit Scope
공유 reference 디렉터리(providers/iac-tools/lenses)와 `codex/skills/references/` 만.

## Stop Conditions
- 공유 refs가 CC 설치 시 실제로 배포되지 않는 구조로 판명되면(각 스킬 독립 복사) 중단하고 (a)복제/(b)공유 결정을 사용자에게 보고.

## Implementation Steps
- [ ] `claude-code/skills/references/` 및 `codex/skills/references/` 기존 구조 확인 후 저장 위치 확정
- [ ] `references/providers/aws.md` — VPC·IAM·S3·RDS·ECS/EKS·Lambda를 Terraform aws provider 관점으로 기술
- [ ] `references/providers/gcp.md` — VPC·IAM·GCS·CloudSQL·GKE·CloudRun (Terraform google provider)
- [ ] `references/providers/azure.md` — VNet·RBAC·Storage·SQL·AKS·Functions (Terraform azurerm provider)
- [ ] `references/providers/k8s.md` — RBAC·NetworkPolicy·resource limits·probes (Terraform kubernetes/helm provider)
- [ ] `references/iac-tools/terraform.md` — validate/plan 워크플로, state·secret 외부화 가드
- [ ] `references/lenses/security.md` — 오구성 taxonomy(공개 버킷·개방 SG·IAM 와일드카드·state 시크릿)
- [ ] `references/lenses/cost.md` — right-sizing·예약/스팟·미사용·데이터 전송
- [ ] `references/lenses/reliability.md` — SPOF·다중 AZ/리전·백업/복구·헬스체크·오토스케일

## Task Verify
- [ ] `for f in references/providers/aws.md references/providers/gcp.md references/providers/azure.md references/providers/k8s.md references/iac-tools/terraform.md references/lenses/security.md references/lenses/cost.md references/lenses/reliability.md; do test -f "$f" || echo MISSING "$f"; done`

## Verification
- [ ] `bash scripts/validate.sh` exit 0
- [ ] markdownlint 통과
