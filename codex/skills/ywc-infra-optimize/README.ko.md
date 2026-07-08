# ywc-infra-optimize (한국어)

기존에 Provision 된 Infrastructure 를 개선하기 위한 보수적 planning Skill 입니다 — Cost Right-Sizing, 미사용 Resource 제거, Reserved/Spot 전환, Drift 탐지, Reliability Hardening 을 다룹니다. `ywc-refactor-clean` 의 SAFE/CAUTION/DANGER Tier 판별과 Iron Law(3중 Witness) 원칙을 Infrastructure 에 적용하지만, Codex v1 에서는 직접 실행하지 않고 분류와 handoff 만 수행합니다. Cost/Utilization Signal 은 `ywc-performance-engineer` Persona 를 가진 Codex Worker 가 수집하고, 필요 시 read-only `ywc-cloud-engineer` Persona 에 feasibility / blast-radius advisory 를 요청합니다. 실제 Terraform 수정은 `ywc-iac-author` 로 넘기며, 모든 분석은 `terraform plan` 까지만 진행하고 `apply` 는 수행하지 않습니다.

## Localized Versions

- [한국어](./README.md)
- [English](./README.en.md)
- [日本語](./README.ja.md)

## 사용 시나리오

- 사용자가 "인프라 개선", "비용 최적화", "right-sizing", "drift 점검", "미사용 리소스 정리", "cost optimization", "optimize infrastructure", "terraform drift", "インフラ最適化" 라고 말할 때
- `ywc-infra-review` 가 발견한 Cost/Drift/Reliability Finding 을 실제로 Remediation 하고 싶을 때
- 정기적인 Infrastructure 최적화(비용 절감, 미사용 Resource 정리) 를 수행하고 싶을 때

## 사용 방법

```bash
$ywc-infra-optimize --scope infra/modules/compute
```

또는 자연어로:

> "미사용 리소스 정리해줘"
> "이 인스턴스들 right-sizing 해줘"

## 입력

- (선택) `--scope <path>` — 전체 IaC Tree 가 아닌 단일 Terraform Module/Path 로 범위 제한
- (선택) `--dry-run` — Gather+Classify 만 수행하고 SAFE Item 실행 없이 Report 만 출력
- (선택) `--skip-verify-done` — 마무리의 `ywc-verify-done` Handoff 생략 (Upstream Caller 가 이미 Verify 를 수행하는 경우에만 유효)

## 출력

- Drift/Cost/Utilization Signal 을 기반으로 한 SAFE/CAUTION/DANGER 분류 Report
- SAFE Item 에 대해서도 실제 수정 대신 좁은 후속 action 을 제안
- CAUTION/DANGER Item 은 실행하지 않고 Escalate 만 수행
- `ywc-verify-done` 형식의 최종 Verification Block

## 관련 Skill

- `ywc-infra-review` — upstream. 본 Skill 이 Remediation 하는 Cost/Drift/Reliability Finding 을 진단
- `ywc-verify-done` — downstream. 최종 Verification Claim
- `ywc-iac-author` — Escalate 된 CAUTION/DANGER Item 의 재작성 경로
- `ywc-performance-engineer` / `ywc-cloud-engineer` Persona — 각각 Cost/Utilization Signal 수집과 read-only feasibility/blast-radius advisory 담당 Persona
- `ywc-infra-design` — Greenfield Infrastructure 설계 담당 (기존 Infrastructure 개선 아님)
- `ywc-refactor-clean` — 본 Skill 이 원용한 SAFE/CAUTION/DANGER Iron Law 의 원조 (Application Code 대상)
