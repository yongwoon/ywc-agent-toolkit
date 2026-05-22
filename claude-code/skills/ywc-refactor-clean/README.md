# ywc-refactor-clean

Detection tool(knip / depcheck / ts-prune / vulture / deadcode / cargo-udeps) 기반 dead code 제거 Skill 입니다. SAFE / CAUTION / DANGER tier 로 finding 을 분류한 뒤 per-item 단위로 Test 를 돌리고 commit 합니다. behavior 변경(duplicate consolidation 중 semantics 재조정 등)은 본 Skill 범위 밖이며 `ywc-tdd-ritual` + `ywc-code-gen` 으로 routing 합니다.

## Localized Versions

- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)

## 사용 시나리오

- 사용자가 "dead code 제거", "knip 돌려줘", "unused import 정리" 라고 말할 때
- Sprint 종료 후 monthly cleanup branch 를 만들 때
- `ywc-onboard-repo` 가 신규 repo 진입 시 prior dead-code accumulation 으로 architecture 파악이 막힐 때

## 사용 방법

```bash
/ywc-refactor-clean --scope src/ --tier safe
```

또는 자연어로:

> "dead code 정리해줘"
> "knip 결과 보고 안전한 것부터 정리해줘"

## Iron Law

**3중 검증 없는 deletion 금지** — (1) detection tool 통과 + (2) grep 으로 reference 0 hit + (3) 매 batch 후 Test green.

## 입력

- (선택) `--scope <dir>` — detection / deletion 범위 (default: repo root)
- (선택) `--tier safe | safe+caution | all` — 어디까지 진행할지 (default: `safe`)
- (선택) `--dry-run` — report 만 emit, mutation 없음
- (선택) `--skip-verify-done` — 상위 caller 가 verify-done 을 별도로 수행하는 경우

## 출력

- Per-item 1-commit 시리즈 (`chore(cleanup): remove unused <symbol> (knip)`)
- 마지막 단계의 Verification Report (Output Format — `ywc-verify-done` block 포함)
- DANGER tier item 목록 (별도 PR 권장 사항)

## 관련 Skill

- `ywc-verify-done` — Step 7 의 mandatory handoff. PASS / FAIL evidence block format 제공
- `ywc-tdd-ritual` — duplicate consolidation 이 behavior 변경을 동반하면 여기로 routing
- `ywc-code-gen` — behavior 변경 동반 cleanup 은 본 Skill 이 아닌 여기서 처리
- `ywc-confidence-gate` — 경계 사례 (CAUTION ↔ DANGER) 판정 시 5-차원 rubric 활용
- `ywc-onboard-repo` — upstream caller (신규 repo 진입 후 hygiene pass)
