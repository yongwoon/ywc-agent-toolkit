# ywc-receive-review

Review feedback 를 받았을 때 **performative agreement 를 차단하고 기술적 검증을 강제**하는 attitude-layer discipline skill 입니다.

## 무엇을 하나요

다음 Iron Law 를 강제합니다.

> **VERIFY BEFORE IMPLEMENTING. NO PERFORMATIVE AGREEMENT, EVER.**

리뷰의 모든 항목에 대해 6단계 Response Pattern 을 순서대로 실행합니다.

1. **READ** — 반응하지 않고 전체 feedback 을 읽음 (동의 / 반박 / 구현 tool 호출 모두 금지)
2. **UNDERSTAND** — 자기 언어로 기술 요구사항을 재진술. 불명확한 항목이 있으면 implement 전에 질문
3. **VERIFY** — 현재 codebase 에서 file open / test 실행 / grep 으로 reviewer 주장을 직접 확인
4. **EVALUATE** — 이 codebase 의 현재 상태에서 suggestion 이 성립하는가 (호환성·기존 결정·YAGNI·platform constraint 고려)
5. **RESPOND** — fix 문장으로 acknowledge 하거나 기술 reasoning 으로 push back. **금지**: "You're absolutely right!", "Great point!", "Thanks!"
6. **IMPLEMENT** — 한 번에 한 항목씩, 각각 test, `ywc-verify-done` 으로 verification block surface

**금지 어휘** (full list 는 references/forbidden-acknowledgments.md):

| 금지 | 대체 |
|---|---|
| "You're absolutely right!" | 수정 사항을 직접 진술: "Fixed — `<file:line>` now <behavior>" |
| "Great point!" / "Excellent feedback!" | 행동을 진술하거나 질문 surface |
| "Thanks for catching that!" / "Thanks for the review!" | 삭제. 수정 자체가 감사의 표현 |
| "Let me implement that right now" (Step 3 전) | "Verifying before implementing: <check>" |

## 언제 trigger 되나요

- 사용자가 "리뷰 받았어", "review feedback", "コメント返信" 등을 언급할 때
- `ywc-handle-pr-reviews` 가 inline-comment iteration 시 위임할 때
- `ywc-finish-branch` post-CI bot review 가 발견되어 응답이 필요할 때
- CodeRabbit / Codex Review / Claude Review 같은 자동 reviewer 코멘트를 처리하기 직전

## 언제 사용하지 않나요

- 직접 review 수행 → `ywc-impl-review`
- PR 생성 → `ywc-create-pr`
- PR 코멘트 fetching · threading · reply 자동화 → `ywc-handle-pr-reviews` (이 skill 의 attitude layer 를 호출하는 쪽)
- 완료 claim 검증 → `ywc-verify-done`

## 참고

상세 Response Pattern · Forbidden Acknowledgments · pushback 조건 · source-specific handling (human partner / external reviewer / bot reviewer) 은 [SKILL.md](./SKILL.md) 를 참조합니다. 원본 process discipline 은 `superpowers:receiving-code-review` 에서 차용하되 `ywc-handle-pr-reviews` 와의 분리 (attitude vs automation) 를 위해 조정했습니다.

## Localized Versions

- [한국어 (default)](./README.md)
- [English](./README.en.md)
- [日本語](./README.ja.md)
