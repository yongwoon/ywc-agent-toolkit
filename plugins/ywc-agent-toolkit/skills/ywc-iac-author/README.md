# ywc-iac-author

Infrastructure-as-Code 작성 Skill 입니다. Infrastructure 설계(`ywc-infra-design` 산출물) 또는 명시적으로 정리한 inline intent 를 바탕으로 Terraform 을 작성하고, Module 단위로 `ywc-cloud-engineer` Persona 를 가진 Codex Worker 에게 Dispatch 한 뒤 `terraform validate` / `terraform plan` 으로 검증하고, apply 전에 blast-radius summary 를 보고합니다. 본 toolkit 에서 **Terraform 은 유일하게 고정된 IaC Tool** 이며, Kubernetes/Helm Resource 도 Terraform 의 `kubernetes` / `helm` Provider 로 표현합니다 — raw manifest 나 별도 IaC Tool 은 사용하지 않습니다.

## Localized Versions

- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)

## 사용 시나리오

- 사용자가 "IaC 작성", "terraform 작성", "인프라 코드", "write terraform", "provision infrastructure" 라고 말할 때
- `ywc-infra-design` 산출물(`infra-design.md`)이 준비되어 실제 Terraform 으로 구현해야 할 때
- 작고 이해도가 높은 Infrastructure 변경이라 별도 설계 단계 없이 inline intent 로 바로 진행하고 싶을 때

## 사용 방법

```bash
$ywc-iac-author --design-doc infra-design.md
```

또는 자연어로:

> "이 설계 기반으로 Terraform 작성해줘"
> "network Module IaC 작성해줘"

## 입력

- (선택) `--design-doc <path>` — 작성 기준으로 삼을 `ywc-infra-design` 산출물. 생략 시 inline intent 확인으로 대체
- (선택) `--scope <module-path>` — 특정 Terraform Module 로 작성 범위 제한 (default: 설계에서 파생되는 모든 Module)
- (선택) `--skip-review-recommendation` — 상위 caller 가 `ywc-infra-review` 를 별도로 스케줄링하는 경우에만 유효

## 출력

- Dispatch 별로 작성된 Terraform Module — 각각 `terraform validate` clean, `terraform plan` 완료
- IaC Authoring Report — blast-radius summary(add/change/destroy, stateful Resource 의 destructive change 명시), state 취급 확인, Secret 외부화 점검
- `apply` 이전 `ywc-infra-review` 실행 권고 (skip 하지 않은 경우)

## 관련 Skill

- `ywc-infra-design` — upstream. 본 Skill 이 로드하는 `infra-design.md` 산출
- `ywc-cloud-engineer` — 각 Terraform Module 을 작성/검증하는 Worker Persona
- `ywc-infra-review` — downstream. Apply 전 권장 리뷰
- `ywc-infra-optimize` — 기존 Infrastructure 의 비용/right-sizing 개선 (본 Skill 범위 아님)
- `ywc-backend-coder` — Application Server / Business Logic (Infrastructure 아님)
- `ywc-docker-isolate` — Local Worktree Docker Port 격리 전용, Production Infrastructure 아님
