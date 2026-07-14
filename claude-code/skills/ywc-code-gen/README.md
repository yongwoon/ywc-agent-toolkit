# ywc-code-gen

여러 Layer 에 걸친 코드를 동시에 생성하는 Skill 입니다. Backend + Frontend + QA Agent 를 병렬로 실행합니다.

## Test-first, Deep Module, Critical Module Review

기본 경로는 headlights 를 gate 합니다: QA lane 이 Backend/Frontend 구현 확정 전에 실패하는(RED) test 를 먼저 작성합니다. `--tdd` 는 더 강한 full RED → GREEN → REFACTOR ritual 을 opt-in 하며 기본 minimal gate 를 대체합니다. Public interface 를 body 보다 먼저 설계합니다(deep module). `--review` 를 주면 Step 8 에서 `/ywc-impl-review` 를 실행하고, Critical/High finding 은 **1 회** fix cycle 로만 수정한 뒤 잔존 시 `DONE_WITH_CONCERNS` 로 보고합니다. 생성 파일이 critical path(auth, payment, crypto, PII, external input)를 건드리면 `--review` 없이도 `/ywc-impl-review` 와 `/ywc-security-audit` 를 강제 실행합니다(`ywc-sequential-executor` 와 동일한 계약). merge 권한이 없으므로 이 gate 는 blocking 이 아니라 advisory 입니다. Verification Gate 는 `git diff --stat` 으로 spec 명시 파일만 바뀌었는지(diff scope) 확인하고, Confidence Gate 는 Minimalism 차원으로 동작하지만 과복잡한 코드(working ≠ minimal)를 실패 처리합니다. 또한 생성 중 spec 과 실제 codebase 가 어긋난 지점(spec↔reality divergence)은 Step 6.5 에서 `implementation-notes.md` 에 기록하고, material 한 경우 `ywc-plan --update-spec` 재계획을 권고합니다. 자세한 내용은 `references/tdd-deep-module-gray-box.md` 를 참고하세요.

## 사용 방법

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "area exposure heatmap"

# 생성 직후 Step 8 에서 /ywc-impl-review 까지 실행 (1 회 fix cycle)
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API" --review
```

## 실행 Agent

| Agent | 생성물 |
|-------|--------|
| Backend Agent (sonnet) | API Route, Service, DB Migration |
| Frontend Agent (sonnet) | UI Component, Query Hook, State 관리 |
| QA Agent (sonnet) | Unit Test, Integration Test, E2E Scenario |

## sequential-executor 와의 관계

- **sequential-executor**: 순차 실행 (의존성이 있는 작업에 적합)
- **/ywc-code-gen**: 독립 Layer 병렬 생성 (SDK/API/Web 동시 필요 시)
- 보완적으로 사용

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
