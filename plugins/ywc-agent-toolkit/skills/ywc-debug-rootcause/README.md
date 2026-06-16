# ywc-debug-rootcause

Bug · Test failure · Build failure 등 모든 defect 에 대해 **root cause 를 먼저 식별**하도록 강제하는 process discipline skill 입니다.

## 무엇을 하나요

이 skill 은 다음 Iron Law 를 강제합니다.

> **NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

Phase 1 (Investigation) 을 통과하지 않으면 어떤 fix 도 제안할 수 없습니다. 4단계 process 는:

1. **Phase 1 — Root-cause investigation** — Error 메시지 정독, 재현, recent change 점검, multi-component 경계에 diagnostic instrumentation, data flow 를 upstream 으로 추적
2. **Phase 2 — Pattern analysis** — 같은 codebase 의 working reference 를 end-to-end 정독, broken 과 차이를 모두 list (특히 "matter 안 할 것 같은" 차이 포함)
3. **Phase 3 — Hypothesis and testing** — "X 가 root cause; minimal change Z 로 해결될 것" 형식의 단일 가설, 한 번에 한 변수만 변경
4. **Phase 4 — Implementation** — Regression test 작성 → 단일 fix → red-green-red verification → `ywc-verify-done` 으로 gating

**3회 이상 같은 surface 에서 fix 가 실패하면** 그 상황은 "fix harder" 가 아니라 "architecture wrong" 입니다. 4번째 fix 를 시도하지 말고 사용자에게 설계 재논의를 surface 합니다.

## 언제 trigger 되나요

- 사용자가 "왜 안돼", "버그", "debug", "落ちる", "通らない" 등을 언급할 때
- Test failure / build failure / type-check error
- 동일 surface 에서 fix 시도가 2회 이상 실패한 직후
- `ywc-verify-done` 의 failure routing 표가 가리킬 때

## 언제 사용하지 않나요

- 구현 중 작성 단계 → `ywc-code-gen`
- Incident 종료 후 retrospective → `ywc-incident-postmortem`
- Security finding triage → `ywc-security-audit`
- 구현 착수 전 confidence 판단 → 해당 결정을 소유한 planning 또는 spec-review skill

## 참고

상세 phase 별 checklist 와 Rationalization Defense 는 [SKILL.md](./SKILL.md) 를 참조합니다. 원본 process discipline 은 `superpowers:systematic-debugging` 에서 차용했습니다.

## Localized Versions

- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)
