# 000056-010-refactor-skill-author-deletion-test — Implementation Checklist

## Prerequisites

- [ ] Phase 000055의 4개 task가 모두 완료·merge되었다 (hard gate).
- [ ] `enumerate-rd-rows.sh --self-check`가 `PARITY OK: 46/46`을 낸다.
- [ ] `docs/ywc-plans/skill-pruning-pilot.md`의 FR-1, AC5, AC5a, AC6, AC7을 **원문으로** 읽었다.
- [ ] `claude-code/skills/references/subagent-status-actions.md` §3.5의 반환 payload 계약을 읽었다.

## Allowed Edit Scope

- [ ] `claude-code/skills/ywc-skill-author/SKILL.md` (audit mode 섹션)
- [ ] `claude-code/skills/ywc-skill-author/references/deletion-test-rubric.md` (신규)
- [ ] 다른 skill, `score.py`, 어떤 RD table도 편집하지 않는다.

## Stop Conditions

- [ ] `SKILL.md`가 500줄(A8)을 넘게 되면 멈추고 rubric reference로 더 밀어낸다.
- [ ] 새 skill 디렉토리를 만들어야 할 것 같으면 멈춘다 (AC1이 금지).
- [ ] 문턱 공식을 `T = floor(floor_rate × 9)`(평균)로 적고 싶어지면 멈춘다 — 사양이 명시적으로 거부한 공식이며, 진짜 inert 행의 37–61 %를 오분류한다.
- [ ] rubric이 "어떤 텍스트 차이든 behavioral"이 되면 멈춘다 — 그러면 아무것도 inert로 라벨되지 않고 pilot이 no-op이 된다.

## Implementation Steps

- [ ] `SKILL.md`의 audit mode에 Deletion Test 진입점과 8단계 절차 요약을 추가한다.
- [ ] **1단계 Enumerate**: `enumerate-rd-rows.sh`로 후보를 만든다. 후보 1개 = data row 1개, key는 `<file>:<start>-<end>`.
- [ ] **2단계 층화 추출** (AC6): Stratum A(행 위치 1–4)에서 40개, Stratum B(위치 5+)에서 40개, **skill·stratum 당 최대 1행**, 각 stratum이 ≥40개 서로 다른 skill에 걸치도록. 추출된 후보 목록은 **어떤 dispatch보다 먼저 report에 기록**하고, 재개된 run은 다시 뽑지 않고 그 목록을 읽는다.
- [ ] **3단계 시나리오 결속**: skill에 `evals/evals.json`이 있으면 그 `prompt`를 축자적으로 재사용하고, 없으면 `description` trigger에서 합성한다. report에 기록한다. **`expected_output`은 절대 읽지 않는다** (부모 FR-2의 no-leaked-answer 규칙).
- [ ] **4단계 variant 생성**: `build-variant.sh`로만 만든다. LLM이 손으로 편집하지 않는다.
- [ ] **5단계 blind 3+3 dispatch**: 원본 body에 3개, 삭제 body에 3개, 모두 같은 시나리오. **어느 subagent에게도 자기가 든 variant, deletion test의 존재, authoring rule의 존재를 알리지 않는다.** 각자 artifact **경로만** 반환한다 (§3.5).
- [ ] **6단계 비교**: within-variant 불일치 = 원본 3쌍 + 삭제 3쌍 (C(3,2)=3씩, 총 6). cross-variant 불일치 = 3×3 = 9. 동등성은 `deletion-test-rubric.md`가 판정한다.
- [ ] **7단계 floor pooling + ceiling**: `floor_rate = (표본 전체 within-variant 불일치 합) / (6 × 80)`. **labeling보다 먼저** 계산한다. `floor_rate > 0.25`면 run은 `INCONCLUSIVE`이고 80개 전부 `indeterminate`이며 증거 게이트는 통과할 수 없다 (AC5a).
- [ ] **8단계 labeling**: `T` = `X ~ Binomial(9, floor_rate)`에 대해 `P(X ≤ t) ≥ 0.95`를 만족하는 최소 `t`. cross 불일치 ≤ `T` → `inert` (**경계 포함**), > `T` → `load-bearing`, 6개 run 중 BLOCKED/NEEDS_CONTEXT가 있으면 `indeterminate`. 재시도 금지.
- [ ] `deletion-test-rubric.md` 작성 (≥30줄): 동등한 것(표현, 동등 항목의 순서)과 동등하지 않은 것(수행한 행동, 건드린 파일, 강제한 게이트, 발한 거부)을 구체 예시와 함께 명시한다.
- [ ] **단측 경계 경고문을 문서에 명시한다**: `T`는 싼 오류만 통제하며, `inert` 라벨은 **증거이지 삭제 허가가 아니다**.
- [ ] `SKILL.md`에 rubric pointer를 추가한다.

## Task Verify

- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh claude-code/skills/ywc-skill-author/` → exit 0
- [ ] `test "$(wc -l < claude-code/skills/ywc-skill-author/references/deletion-test-rubric.md)" -ge 30`
- [ ] `test "$(wc -l < claude-code/skills/ywc-skill-author/SKILL.md)" -le 500`
- [ ] `grep -q 'deletion-test-rubric.md' claude-code/skills/ywc-skill-author/SKILL.md`
- [ ] `ls claude-code/skills/ | grep -E 'ywc-skill-(prune|audit)'` → 결과 없음 (AC1)

## Verification

- [ ] `bash scripts/validate.sh` 통과.
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 통과 (AC13).
- [ ] `for d in claude-code/skills/ywc-*/; do bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh "$d" || echo "FAILED: $d"; done` → `FAILED:` 없음.
- [ ] 문서화된 문턱 공식이 사양 AC5의 꼬리-경계 표(`floor_rate` 0.00→T 0, 0.05→2, 0.10→3, 0.15→3, 0.20→4, 0.25→4)를 재현한다.
- [ ] `git diff`에 RD 섹션 삭제 줄이 없다 (AC2).
