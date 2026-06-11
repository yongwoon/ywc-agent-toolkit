# ywc-confidence-gate

구현 착수 직전에 5차원 confidence 점수를 강제로 매기고 그 결과에 따라 PROCEED / REVIEW / STOP 의사결정을 surface 하는 pre-implementation discipline skill 입니다.

## 무엇을 하나요

다음 Iron Law 를 강제합니다.

> **NO IMPLEMENTATION WITHOUT AN EXPLICIT CONFIDENCE SCORE AND BAND DECISION**

5차원 rubric (각각 0~100) 으로 점수를 매기고 가중합으로 band 를 결정합니다.

| 차원 | 가중치 | 핵심 질문 |
|---|---|---|
| Scope clarity | 25% | 한 문장으로 in-scope 와 out-of-scope 를 명확히 쓸 수 있는가 |
| Architecture compliance | 25% | 기존 구조 / 명명 / abstraction 을 따르는가 |
| Evidence quality | 20% | 주장이 primary source (코드, 공식 docs, test 출력) 로 뒷받침되는가 |
| Reuse verified | 15% | 기존 utility / library 를 검색하고 각각 ruled out 한 이유가 있는가 |
| Root cause identified | 15% | Bug 라면 symptom 이 아닌 underlying cause, greenfield 라면 surface request 가 아닌 underlying need 를 명명했는가 |

| Band | Aggregate | 행동 |
|---|---|---|
| **PROCEED** | ≥ 90 | 구현 시작. 점수를 executor report 에 surface |
| **REVIEW** | 70~89 | 1~3개 alternative 또는 open question 제시, 약한 차원 해소 후 진행 |
| **STOP** | < 70 | 구현 금지. 약한 차원과 raise 방법 surface, 상위 skill 로 routing |

**단일 차원 `< 50` override**: aggregate 가 tentative band 를 정한 뒤 단일 차원이 50 미만이면 band 가 한 단계 강등됩니다 (PROCEED → REVIEW, REVIEW → STOP) — 항상 한 단계만이며 STOP 로 건너뛰지 않고, 정확히 50 인 차원은 trigger 하지 않습니다. 강한 차원이 fatal weakness 를 가리는 것을 막기 위한 장치입니다.

## 언제 trigger 되나요

- 사용자가 "구현 시작해도 돼?", "준비 됐어?", "ready to implement", "確信度チェック" 등을 언급할 때
- `ywc-code-gen` / `ywc-sequential-executor` / `ywc-parallel-executor` / `ywc-agentic` 의 시작 boundary
- `ywc-plan` 의 Scale 판정 후 downstream handoff 직전
- 의존성 큰 architectural 결정 commit 직전

## 언제 사용하지 않나요

- 완료 후 검증 → `ywc-verify-done` (반대편 gate, 같은 rubric)
- Spec quality 점검 → `ywc-spec-validate`
- 구현 결과 review 점수 → `ywc-impl-review` (이 skill 과 동일 rubric 사용, score 비교 가능)
- 의도 명확화 → `ywc-brainstorm`

## 참고

상세 workflow 와 anti-pattern 은 [SKILL.md](./SKILL.md), 표준 rubric 정의는 공유 reference [../references/confidence-gate.md](../references/confidence-gate.md) 에 있습니다. 원본 발상은 ECC 의 confidence-check skill 과 SuperClaude 의 PM Agent 에서 차용했습니다.

## Localized Versions

- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)
