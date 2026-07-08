# ywc-infra-review

이미 작성된 IaC / Cloud Configuration 을 Apply 하기 전에 검토하는 Skill 입니다. Security(오구성·Least-Privilege)/Cost(Right-Sizing·낭비)/Reliability(SPOF·Backup·Health) 3-lens 로 Fan-out 하여 각각 `ywc-security-engineer`, `ywc-performance-engineer`, `ywc-cloud-engineer`(Review Mode) Persona 를 가진 Codex Worker 에 Dispatch 하고, 모든 Finding 을 Severity(Critical/High/Medium/Low)로 취합합니다. CRITICAL/HIGH Finding 은 Apply Blocking 을 권고합니다. 본 Skill 은 IaC 를 직접 작성하거나 수정하지 않습니다 — Terraform 이 본 toolkit 의 유일하게 고정된 IaC Tool 이며, Provider 는 AWS/GCP/Azure/K8s 를 Terraform Provider 로 다룹니다.

## Localized Versions

- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어 (요약)](./README.ko.md)

## 사용 시나리오

- 사용자가 "인프라 리뷰", "IaC 리뷰", "terraform 검토", "보안 그룹 점검", "iam 과권한", "infra review", "review my terraform", "IaC review", "インフラレビュー" 라고 말할 때
- `ywc-iac-author` 로 작성된 Terraform 을 Apply 하기 전에 오구성/비용/신뢰성을 점검하고 싶을 때
- 기존에 Provision 된 Infrastructure 의 Security Group, IAM Policy, Public Exposure 를 점검하고 싶을 때

## 사용 방법

```bash
$ywc-infra-review --scope infra/modules/network
```

또는 자연어로:

> "이 Terraform 변경사항 리뷰해줘"
> "payments-api 인프라의 보안 그룹이랑 IAM 점검해줘"

## 입력

- (선택) `--scope <path>` — 전체 IaC Tree 가 아닌 단일 Terraform Module/Path 로 리뷰 범위 제한
- (선택) `--skip-optimize-recommendation` — 마무리의 `ywc-infra-optimize` 권고 생략 (Upstream Caller 가 이미 Remediation 을 스케줄링한 경우에만 유효)

## 출력

- Security/Cost/Reliability 3-lens Severity-rated Findings 취합 Report
- CRITICAL/HIGH Finding 발견 시 Apply Blocking 권고
- Remediation 실행을 위한 `ywc-infra-optimize` (또는 재작성을 위한 `ywc-iac-author`) 권고

## 관련 Skill

- `ywc-iac-author` — upstream. 본 Skill 이 리뷰하는 Terraform 을 산출
- `ywc-infra-optimize` — downstream. 본 Skill 이 발견한 Cost/Drift Finding 의 Remediation 실행
- `ywc-security-engineer` / `ywc-performance-engineer` / `ywc-cloud-engineer`(Review Mode) Persona — 각 Lens 의 Fan-out Worker
- `ywc-security-audit` — App-code Auth/Injection Review 담당 (IaC 오구성 아님)
- `ywc-impl-review` — 일반 Application Code Review 담당 (Infrastructure 아님)
