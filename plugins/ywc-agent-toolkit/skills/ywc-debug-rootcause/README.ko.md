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

최소 feedback loop의 관측 실패와 catches/misses를 기록하고 3–5개 반증 가능한 가설을 순위화한 뒤 한 번에 한 변수만 실험합니다. 자동 재현 불가 시 수동 근거와 제약을 기록하며 RED를 꾸미지 않습니다. 세 번 실패 후 기본 중단합니다. 별도 evidence-linked `Fix #4 signal: fix harder`와 `Next fix worth attempting: <one concrete minimal change>`가 모두 유효한 debug 응답에 있을 때만 네 번째 시도를 한 번 허용하며, 실패 후 다섯 번째 시도는 없습니다.

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

- [한국어 (default)](./README.md)
- [English](./README.en.md)
- [日本語](./README.ja.md)

## Analyst contract

`Caller: ywc-debug-rootcause` · `analysis_mode=debug_hypotheses`

Caller와 analysis_mode를 명시합니다. 누락·unknown·mismatch는 추론 없이 `NEEDS_CONTEXT`이며, 응답의 Status → Summary → Finding counts → Analysis mode를 검증하고 기존 caller gate를 유지합니다.

최소 feedback loop의 관측 실패와 catches/misses를 기록하고 3–5개 반증 가능한 가설을 순위화한 뒤 한 번에 한 변수만 실험합니다. 자동 재현 불가 시 수동 근거와 제약을 기록하며 RED를 꾸미지 않습니다. 세 번 실패 후 기본 중단합니다. 별도 evidence-linked `Fix #4 signal: fix harder`와 `Next fix worth attempting: <one concrete minimal change>`가 모두 유효한 debug 응답에 있을 때만 네 번째 시도를 한 번 허용하며, 실패 후 다섯 번째 시도는 없습니다.

Live runtime: `UNVERIFIED — instruction contract only`.
