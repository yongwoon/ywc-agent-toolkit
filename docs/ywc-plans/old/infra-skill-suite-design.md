# 인프라 스킬 스위트 설계 블루프린트 (ywc-agent-toolkit)

> 대상: AWS · GCP · Azure · Kubernetes/Helm
> 구성: 스킬 4종 + 신규 워커 에이전트 1종 + 기존 에이전트 2종 확장
> 원칙: 앱 라이프사이클 미러링, 스킬=WHAT/오케스트레이션 · 에이전트=HOW/워커, 프로바이더 차이는 Progressive Disclosure로 references/ 분리

---

## 0. Taxonomy 배치

| 신규 스킬 | category | phase | 대응 앱 스킬 |
|---|---|---|---|
| `ywc-infra-design` | spec | planning | ywc-project-scaffold / ywc-tech-research |
| `ywc-iac-author` | implement | implementation | ywc-code-gen |
| `ywc-infra-review` | review | quality | ywc-impl-review / ywc-security-audit |
| `ywc-infra-optimize` | maintenance | cleanup | ywc-refactor-clean |

신규 에이전트: `ywc-cloud-engineer` (read-write 워커, backend-coder의 인프라 판)
확장 에이전트: `ywc-security-engineer`(IaC 오구성 refs), `ywc-performance-engineer`(FinOps refs)

---

## 1. 공유 프로바이더 reference 아키텍처

각 스킬은 프로바이더 세부를 SKILL.md에 넣지 않고 아래를 공유 참조한다.

```
references/providers/
  aws.md      # Terraform/CDK/CFN, VPC·IAM·S3·RDS·ECS/EKS·Lambda, Well-Architected 매핑
  gcp.md      # Terraform/Deployment Manager, VPC·IAM·GCS·CloudSQL·GKE·CloudRun
  azure.md    # Bicep/Terraform, VNet·RBAC·Storage·SQL·AKS·Functions
  k8s.md      # manifests·Helm·Kustomize, RBAC·NetworkPolicy·resource limits·probes
references/iac-tools/
  terraform.md   # §7 확정: Terraform 단일 고정. 타 도구 reference는 저작하지 않음.
references/lenses/
  security.md      # 오구성 taxonomy (공개 버킷·개방 SG·IAM 와일드카드·state 시크릿)
  cost.md          # right-sizing·예약/스팟·미사용 리소스·데이터 전송 비용
  reliability.md   # SPOF·다중 AZ/리전·백업/복구·헬스체크·오토스케일
```

> 스킬은 프로바이더 선택 후 해당 파일 1개만 로드한다 (Pattern 2).

---

## 2. 스킬별 상세 설계

> **Codex 미러 주의**: 아래 frontmatter 예시의 `category`/`phase`/`requires`/`advisor_budget`는 **Claude Code 전용**이다. Codex `SKILL.md`는 `name`+`description`만 허용하며, 나머지 필드가 있으면 `validate.sh`가 실패한다. Codex 미러 저작 시 해당 필드를 제거한다.

### 2.1 `ywc-infra-design` — 설계

**frontmatter**
```yaml
name: ywc-infra-design
description: >-
  (ywc) Use when designing cloud/infrastructure architecture before writing IaC:
  service selection, network topology, IAM/identity boundaries, data stores,
  scaling & availability strategy, cost estimate, and trade-off records for
  AWS/GCP/Azure/Kubernetes. Produces an infra design doc consumed by ywc-iac-author.
  Triggers: "인프라 설계", "클라우드 아키텍처", "aws 구성 설계", "네트워크 토폴로지",
  "infra design", "cloud architecture", "design the infrastructure",
  "インフラ設計", "クラウド構成", "ywc-infra-design".
  Do not use for: writing the actual IaC code (use ywc-iac-author), source-code
  folder layout (use ywc-project-scaffold), library/tech comparison only
  (use ywc-tech-research — it feeds this skill), reviewing existing infra
  (use ywc-infra-review), or local worktree docker port issues (ywc-docker-isolate).
category: spec
phase: planning
requires: []
advisor_budget: 2
```

**body 구조**
1. 요구 수집: 워크로드 특성·트래픽·데이터·규제·예산·RTO/RPO
2. 프로바이더 선정 (미정 시 `ywc-tech-research` 위임)
3. 토폴로지 설계: 네트워크·컴퓨트·스토리지·IAM 경계
4. 신뢰성/비용/보안 3-lens 사전 점검 (`references/lenses/*`)
5. trade-off 기록 (ADR 형식)
6. **산출**: `infra-design.md` (ywc-iac-author 입력 계약)

**dispatch**: `ywc-tech-research`(프로바이더 비교), 필요 시 `ywc-cloud-engineer`(토폴로지 실현 가능성 자문, read-only 모드)

---

### 2.2 `ywc-iac-author` — 실장

**frontmatter**
```yaml
name: ywc-iac-author
description: >-
  (ywc) Use when authoring or modifying Infrastructure-as-Code from a design:
  Terraform/Pulumi/CDK/CloudFormation/Bicep modules and Kubernetes/Helm manifests
  for AWS/GCP/Azure/K8s, including validate/plan and a blast-radius summary.
  Triggers: "IaC 작성", "terraform 작성", "인프라 코드", "k8s 매니페스트",
  "helm 차트 작성", "write terraform", "author IaC", "provision infrastructure",
  "IaC を書いて", "ywc-iac-author".
  Do not use for: application server/business logic (use ywc-backend-coder),
  designing the topology first (use ywc-infra-design), reviewing IaC quality
  (use ywc-infra-review), cost/right-sizing remediation (use ywc-infra-optimize),
  or local worktree docker port collisions (ywc-docker-isolate — dev-only, not prod infra).
category: implement
phase: implementation
requires: []
advisor_budget: 1
```

**body 구조**
1. 설계 입력 로드 (infra-design.md) 또는 인라인 의도 파악
2. IaC 도구 선정 → `references/iac-tools/*` 로드
3. `ywc-cloud-engineer`로 fan-out (모듈 단위)
4. 검증: `validate` / `plan` / `synth` (에이전트 Bash)
5. **diff·blast radius 요약** (생성/변경/삭제 리소스, 파괴적 변경 강조)
6. 상태(state) 취급 주의·시크릿 외부화 가드

**dispatch**: `ywc-cloud-engineer`(작성), 완료 후 `ywc-infra-review` 권유

---

### 2.3 `ywc-infra-review` — 리뷰 (개선 진단)

**frontmatter**
```yaml
name: ywc-infra-review
description: >-
  (ywc) Use when reviewing IaC / cloud configuration for misconfiguration,
  least-privilege, cost, and reliability before applying — security groups,
  IAM/RBAC, public exposure, secrets in state, SPOF, missing backups, resource
  limits. Fans out to security/cost/reliability lenses across AWS/GCP/Azure/K8s.
  Triggers: "인프라 리뷰", "IaC 리뷰", "terraform 검토", "보안 그룹 점검",
  "iam 과권한", "infra review", "review my terraform", "IaC review",
  "インフラレビュー", "ywc-infra-review".
  Do not use for: app-code auth/injection review (use ywc-security-audit),
  writing IaC (use ywc-iac-author), executing cost/drift remediation
  (use ywc-infra-optimize), or general app code review (use ywc-impl-review).
category: review
phase: quality
requires: []
advisor_budget: 3
```

**body 구조 (3-lens fan-out)**
- Security lens → `ywc-security-engineer` + `references/lenses/security.md`
- Cost lens → `ywc-performance-engineer` + `references/lenses/cost.md`
- Reliability lens → `ywc-cloud-engineer`(review 모드) + `references/lenses/reliability.md`
- severity-rated 취합 → CRITICAL/HIGH는 apply 차단 권고

---

### 2.4 `ywc-infra-optimize` — 개선 (실행)

**frontmatter**
```yaml
name: ywc-infra-optimize
description: >-
  (ywc) Use when improving existing infrastructure: cost right-sizing, removing
  unused resources, reserved/spot adoption, drift detection & remediation, and
  reliability hardening for AWS/GCP/Azure/K8s — the safe change-loop equivalent of
  refactor-clean for infra. Triggers: "인프라 개선", "비용 최적화", "right-sizing",
  "drift 점검", "미사용 리소스 정리", "cost optimization", "optimize infrastructure",
  "terraform drift", "インフラ最適化", "ywc-infra-optimize".
  Do not use for: greenfield design (use ywc-infra-design), first-time IaC authoring
  (use ywc-iac-author), pre-apply review only (use ywc-infra-review), or app-code
  performance (use ywc-performance-engineer directly for code hotspots).
category: maintenance
phase: cleanup
requires: []
advisor_budget: 2
```

**body 구조**
1. 현황 수집: `plan`(drift), 비용 리포트, 사용률
2. 개선 후보 분류: SAFE / CAUTION / DANGER (refactor-clean의 Iron Law 차용)
3. SAFE 항목만 `ywc-cloud-engineer`로 변경 → per-item plan 확인 → 단일 커밋
4. CAUTION/DANGER는 별도 에스컬레이션

---

## 3. 신규 에이전트 `ywc-cloud-engineer`

```
name: ywc-cloud-engineer
role: read-write IaC 워커 (backend-coder의 인프라 판) + review 모드
tools: Read, Write, Edit, Bash, Grep, Glob
```

**Mission**: IaC(Terraform 단일 — §7 확정) 작성·수정, `terraform validate` / `terraform plan` 검증, 신뢰성 렌즈 리뷰. (K8s/Helm 리소스도 Terraform `kubernetes`/`helm` provider로 기술.)

**Do not use for**: 앱 서버 로직(backend-coder), 아키텍처 판단(architect), 앱 보안 정적분석(security-engineer), 인프라 토폴로지 초기 설계 결정(infra-design 스킬이 소유).

**출력 계약 (Codex 규약 일치)**: `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` + 변경 리소스 요약 + `Next action:`

### 기존 에이전트 확장
- `ywc-security-engineer` ← `references/iac-security.md` (오구성 taxonomy) 추가, description에 IaC 트리거 보강
- `ywc-performance-engineer` ← `references/finops.md` (right-sizing·예약/스팟·데이터 전송 비용) 추가

---

## 4. Dispatch 그래프

```
ywc-infra-design ──(infra-design.md)──▶ ywc-iac-author ──▶ ywc-cloud-engineer
       │                                      │
       └─(provider 비교) ywc-tech-research     ▼
                                        ywc-infra-review ──▶ security-engineer / performance-engineer / cloud-engineer
                                              │
                                              ▼
                                        ywc-infra-optimize ──▶ ywc-cloud-engineer
```

---

## 5. Anti-trigger 통합 매트릭스

| 스킬 | 배제 대상 | 사유 |
|---|---|---|
| infra-design | iac-author, project-scaffold, tech-research, docker-isolate | 설계 vs 실장/폴더/비교/로컬포트 |
| iac-author | backend-coder, infra-design, infra-review, optimize, docker-isolate | 인프라코드 vs 앱코드/설계/리뷰/개선/로컬 |
| infra-review | security-audit, impl-review, iac-author, optimize | 인프라오구성 vs 앱보안/앱리뷰/작성/실행 |
| infra-optimize | infra-design, iac-author, infra-review, performance-engineer | 개선실행 vs 설계/작성/진단/앱성능 |

> `ywc-docker-isolate`는 로컬 worktree 포트 충돌 전용 — 모든 신규 스킬이 "prod 인프라 아님"을 명시 배제.

---

## 6. 롤아웃 체크리스트 (스킬당)

각 신규 스킬은 다음을 충족해야 CI 통과:
- [ ] `claude-code/skills/<name>/SKILL.md` (name+description frontmatter)
- [ ] `README.md` `README.en.md` `README.ja.md` `README.ko.md` (Tier1 필수)
- [ ] `references/` 프로바이더 4종 + lens 파일
- [ ] Codex 미러: `codex/skills/<name>/` + `agents/openai.yaml` (frontmatter는 **name+description만** — `validate.sh:88`이 `category|phase|requires|advisor_budget|allowed tools` 존재 시 실패)
- [ ] Codex 플러그인 동기화: `bash scripts/sync-codex-plugin.sh` 실행 → `plugins/ywc-agent-toolkit/skills/` 미러 + `.codex-plugin/plugin.json` 갱신 (pre-commit 훅이 자동 수행하나 로컬 `validate.sh`의 `check_codex_plugin_manifest` 게이트 대비)
- [ ] 에이전트: `claude-code/agents/ywc-cloud-engineer.md` + `codex/agents/ywc-cloud-engineer.toml`
- [ ] 스킬은 `install.sh`가 `skills/*/` 자동 탐색 → 별도 등록 편집 불필요
- [ ] `bash scripts/validate.sh` exit 0, markdownlint 통과

**권장 저작 순서**: cloud-engineer 에이전트 → iac-author → infra-design → infra-review → infra-optimize
(워커 먼저 세워야 나머지 스킬이 dispatch 가능)

---

## 7. 결정 사항 (확정)
- **IaC 기본 도구**: **Terraform 단일 고정.** 모든 프로바이더를 Terraform으로 통일한다. `references/iac-tools/`는 `terraform.md` 1개만 저작하고, `ywc-cloud-engineer`의 검증 체인은 `terraform validate` / `terraform plan`으로 단순화한다. (CDK/Pulumi/CFN/Bicep/Helm reference는 저작하지 않는다 — 향후 필요 시 별도 확장.)
- **infra-review 배치**: **독립 스킬 유지.** `ywc-infra-review`를 독립 스킬로 저작하며 `ywc-security-audit`에 흡수하지 않는다. 스킬 4종 구성을 확정한다.
- **프로바이더 reference 범위**: **AWS·GCP·Azure·K8s/Helm 4종 동시.** `references/providers/` 4파일을 동시 저작한다. (단, 각 파일은 Terraform provider 관점으로 기술한다 — 위 IaC 도구 결정과 정합.)

## 8. Iteration 1 Amendments (spec-ready 수렴 로그)
> `ywc-spec-validate` 1회차(DONE_WITH_CONCERNS, Critical 2 / Warning 3)에 대한 보정.
- **C1 해소**: infra-review 독립 스킬 확정 → §0/§2.3/§4/§5 유효, 스킬 4종 유지.
- **C2 해소**: Terraform 단일 고정 → §1 `references/iac-tools/`를 `terraform.md` 단일로 축소, §3 cloud-engineer 검증 체인 `terraform validate/plan`으로 확정.
- **W1 해소**: §6 체크리스트에 Codex 플러그인 동기화 사이트 추가(아래 반영).
- **W2 해소**: §2 frontmatter 예시에 Codex strip 주석 추가(아래 반영).
- **W3 해소**: Decision 3(프로바이더 범위)을 §7에서 확정 처리(4종 동시).
