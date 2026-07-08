# ywc-infra-design

Cloud/Infrastructure Architecture 를 설계하는 Skill 입니다. IaC 를 한 줄이라도 작성하기 전에 Requirements Gathering, Provider 선택, Network/Compute/Storage/IAM Topology 설계, Reliability/Cost/Security 3-lens Pre-check 를 거쳐 모든 주요 Trade-off 를 ADR(Architecture Decision Record) 형식으로 기록하고, `ywc-iac-author` 가 로드하는 Input Contract 인 `infra-design.md` 를 산출합니다. 본 Skill 은 IaC 를 직접 작성하지 않습니다 — 본 toolkit 에서 **Terraform 은 유일하게 고정된 IaC Tool** 이며, 실제 `.tf` 작성은 `ywc-iac-author` 의 역할입니다.

## Localized Versions

- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)

## 사용 시나리오

- 사용자가 "인프라 설계", "클라우드 아키텍처", "aws 구성 설계", "네트워크 토폴로지", "infra design", "cloud architecture", "design the infrastructure" 라고 말할 때
- 새로운 Feature/Service 를 위해 Infrastructure 를 처음부터 설계해야 할 때
- Provider 가 아직 결정되지 않아 비교가 필요한 경우 (`ywc-tech-research` 로 delegate)
- 기존 `infra-design.md` 없이 바로 `ywc-iac-author` 로 넘어가려는 상황을 방지하고 싶을 때

## 사용 방법

```bash
$ywc-infra-design --provider aws
```

또는 자연어로:

> "이 Service 를 위한 Infrastructure 설계해줘"
> "payments-api 의 클라우드 아키텍처 설계해줘"

## 입력

- (선택) `--provider <aws|gcp|azure|k8s>` — 이미 결정된 Provider 를 명시하여 `ywc-tech-research` delegation(Step 2)을 건너뜀
- (선택) `--scope <system-name>` — 전체 Architecture 가 아닌 단일 Service/System 으로 설계 범위 제한
- (선택) `--skip-cloud-consult` — Step 3 의 read-only `ywc-cloud-engineer` Persona feasibility consult 생략

## 출력

- `infra-design.md` — Requirements / Provider Decision / Topology(Network/Compute/Storage/IAM) / 3-Lens Pre-Check Results / ADR Log 로 구성된 Input Contract 문서
- `ywc-iac-author` 가 Step 1 에서 바로 로드할 수 있는 완결된 설계 산출물

## 관련 Skill

- `ywc-tech-research` — upstream. Provider 가 결정되지 않았을 때 비교를 담당하며 본 Skill 에 결과를 공급
- `ywc-iac-author` — downstream. 본 Skill 이 산출한 `infra-design.md` 를 로드하여 실제 Terraform 작성
- `ywc-infra-review` — downstream. 작성된 IaC 를 검토 (본 Skill 은 아직 작성되지 않은 Infrastructure 를 설계)
- `ywc-cloud-engineer` — Step 3 의 read-only topology feasibility consult (authoring 아님)
- `ywc-project-scaffold` — Source Code Folder Layout 담당 (Infrastructure Architecture 아님)
- `ywc-docker-isolate` — Local Worktree Docker Port 격리 전용, Production Infrastructure 아님
