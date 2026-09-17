# ywc-verify-done

완료 선언 전에 fresh verification evidence 를 강제하는 process discipline skill 입니다.

## 무엇을 하나요

이 skill 은 "작업이 끝났다 / 테스트 통과했다 / Build 성공했다 / Bug 수정했다 / 요구사항 충족했다" 같은 모든 완료 주장 (completion claim) 을 surface 하기 직전에 호출됩니다. 다음 5단계 Gate Function 을 강제합니다.

1. **IDENTIFY** — 그 주장을 증명할 정확한 shell command 를 명시
2. **RUN** — 해당 command 를 **현재 message 내에서 fresh 하게** 실행
3. **READ** — 전체 output 과 exit code 확인
4. **VERIFY** — output 이 주장 문장의 정확한 표현을 뒷받침하는지 확인
5. **CLAIM** — 1~4 가 통과한 경우에만 verification block 과 함께 주장을 surface

"should", "probably", "seems" 같은 미검증 어휘는 차단됩니다.

## 언제 trigger 되나요

- 사용자가 "완료", "끝났어", "done", "完了" 등 완료 신호를 보낼 때
- Commit / PR 생성 / Merge 직전
- Executor (`ywc-sequential-executor`, `ywc-parallel-executor`) 의 task transition 직전
- Subagent return payload 을 받은 직후

## 언제 사용하지 않나요

- 구현 진행 중 → `ywc-code-gen`
- Bug 의 root cause 조사 → `ywc-debug-rootcause`
- 구현 착수 전 confidence 판단 → 해당 결정을 소유한 planning 또는 spec-review skill
- Plan 단계 codebase exploration → `ywc-plan`

## 참고

상세 규칙·Output Format·Rationalization Defense 는 [SKILL.md](./SKILL.md) 를 참조합니다. 원본 process 규율은 `superpowers:verification-before-completion` 에서 차용했습니다.

## 선택 사항: Gate Ledger

여러 명령이나 accepted subagent artifact를 하나의 주장으로 묶을 때만 추가 escalation으로 사용합니다. 설치된 checker의 `--status`는 subprocess를 실행하지 않고 bytes를 보존하며, bare mode는 정확히 일치하는 cached `PASS`가 없는 gate만 재개하고 `--reverify`는 모든 runnable gate를 fresh하게 실행합니다. `MANUAL` gate는 건너뜁니다. `CHECK`는 임의의 shell이므로 실행 전에 검토하고, absence를 주장할 때는 positive control을 사용하세요. PR-ready 주장에는 독립적인 600초 review poll, `--verify` head-SHA, CI, PR-health 증거가 계속 필요합니다. 문법은 [gate-ledger.md](./references/gate-ledger.md)를 참조하세요.

## Localized Versions

- [한국어 (default)](./README.md)
- [English](./README.en.md)
- [日本語](./README.ja.md)
