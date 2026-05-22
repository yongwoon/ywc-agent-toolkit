# ywc-tdd-ritual

구현 직전에 RED → GREEN → REFACTOR cycle 을 강제하는 TDD discipline skill 입니다.

## 무엇을 하나요

다음 Iron Law 를 강제합니다.

> **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**

7단계 cycle 을 통과해야만 production code 가 commit 됩니다.

1. **RED** — 1개 behavior 에 대한 minimal failing test 작성 (production code 는 아직 없음)
2. **Verify RED** — 테스트가 실제로 실패하는지 **눈으로 확인** (skip 절대 금지)
3. **GREEN** — 그 test 만 통과시키는 가장 단순한 production code
4. **Verify GREEN** — 새 test + 전체 suite 통과 확인
5. **REFACTOR** — green 상태 유지하며 중복 제거 · 이름 개선
6. **Verify after REFACTOR** — refactor 후에도 모든 test 통과
7. 다음 behavior 로 loop 하거나, `ywc-verify-done` 으로 handoff

"코드 먼저 쓰고 test 는 나중에" 패턴은 차단됩니다. 그렇게 쓴 test 는 첫 실행에서 통과해버려 실제 결함을 잡는지 검증할 수 없기 때문입니다.

## 언제 trigger 되나요

- 사용자가 "TDD", "test first", "테스트 먼저", "RED-GREEN" 등을 언급할 때
- 새 feature / bug fix / behavior change 구현 시
- `ywc-code-gen --tdd` 가 위임할 때
- `ywc-debug-rootcause` Phase 4 §1 의 regression test 작성 시점

## 언제 사용하지 않나요

- 사용자가 명시적으로 throwaway prototype 으로 선언한 경우
- 기존 test failure 의 root-cause 조사 → `ywc-debug-rootcause`
- Generated code / config 파일
- 완료 claim 검증 → `ywc-verify-done` (TDD 는 쓰는 discipline, verify-done 은 주장하는 discipline)

## 참고

상세 cycle 규칙·Rationalization Defense·Output Format 은 [SKILL.md](./SKILL.md) 를 참조합니다. 원본 process discipline 은 `superpowers:test-driven-development` 에서 차용했습니다.

## Localized Versions

- [한국어 (default)](./README.md)
- [English](./README.en.md)
- [日本語](./README.ja.md)
