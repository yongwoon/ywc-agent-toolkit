# 000059-010-refactor-description-word-cap

## Purpose

46개 skill description 중 **80단어를 초과하는 29개**를 80단어 이하로 다시 쓴다. description은 매 턴 상주하는 context이므로, 이 축소가 곧 **≈1,000 토큰/턴** 절감이다.

## Scope

- 80단어 초과 29개 skill의 `description` 재작성 (측정치: 총 4,154단어, 평균 90.3, 최대 148 `ywc-design-renew`, 30단어 미만 0개).
- AC14 측정 의무: **수리된 추출기로** rewrite 전 baseline · rewrite 후 값 · delta를 기록한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-pruning-pilot.md#fr-5-a-flat-80-word-description-cap-ac11-ac12-ac14`
- `docs/ywc-plans/skill-pruning-pilot.md` AC12 (상한, 경계 포함), AC14 (측정 의무), AC12a (수리된 추출기)
- `docs/ywc-plans/skill-pruning-pilot.md#existing-constraints-touched` — `score.py:288` (A4) 행과 `score.py:286-287` vs `validate-skill.sh` (A2/A3 divergence) 행

### Summary

**재작성된 description은 네 가지를 동시에 만족해야 한다.** 이 네 개가 서로 다른 두 validator에 흩어져 있고 서로 다르게 판정하므로, 하나씩 확인하지 않으면 로컬은 통과하고 CI가 깨진다:

| | 요구 | 판정 위치 (canonical) |
|---|---|---|
| A2 | `(ywc) Use when` 으로 **시작** | `score.py:286` — `startswith` |
| A3 | `Do not use (for\|during\|when\|in)` 포함 | `score.py:287` — **`Do not invoke` 는 불허** |
| A4 | **한글과 일본어 문자를 둘 다 포함** | `score.py:288` — 46/46 현재 통과 |
| 상한 | ≤ **80단어** (80 PASS, 81 FAIL) | 신규 (`000059-020`이 강제) |

**A4를 절대 깨뜨리지 마라.** `bool(HANGUL.search(desc) and JAPANESE.search(desc))` 는 S2의 10개 검사 중 하나다. 하나라도 뒤집히면 `s2 = round(9/10*5)` = **4** 가 되어 5에서 떨어지고, `score.py --ci` 가 `history.mechanical.json` 대비 regression으로 **build를 FAIL**시킨다. AC13 위반이다.

다행히 **A4는 존재 검사이지 길이 검사가 아니다** — 한글 몇 글자, 일본어 몇 글자면 통과한다. 90단어가 된 원인은 A4가 아니라 저자들이 다국어 trigger 목록을 길게 쓴 선택이다. 그러니 다국어 trigger를 **압축하되 없애지는 마라**.

**상한은 예산이지 목표가 아니다.** 줄이는 방법은 중복 제거다 — 같은 trigger의 반복 표현, trigger를 부정형으로 되풀이하는 anti-trigger 목록, skill body와 겹치는 산문. **사용자가 그 skill에 닿는 데 실제로 필요한 trigger는 절대 지우지 않는다.** 80단어 안에서 도달 가능하게 만들 수 없는 skill은 **훼손할 description이 아니라 보고할 finding**이다 — 예산 초과인 채로 두고 기록하라.

### Out of Scope (from spec)

- `invocation:` tier — **이 spec에서 잘려나갔다.** 별도 spec으로 유예. frontmatter key를 추가하지 않는다.
- `score.py` 수정 (Critical Surface — FR-4만이 건드린다)
- `validate-skill.sh`에 상한 검사 추가 (`000059-020` 소유)
- `codex/skills/**`, `plugins/**`

## Criticality

`normal` — `score.py`를 읽기만 한다. 다만 **A4를 깨면 CI가 즉시 깨지므로**, 29개 각각에 대해 한글·일본어 문자 잔존을 기계적으로 확인해야 한다.

## Dependencies

### Depends On

- `000055-010-refactor-validate-skill-extractor-repair` — **신뢰할 수 있는 단어 수 없이는 이 task가 무의미하다.** 수리 전 추출기는 15개 skill에서 body를 삼켜 `ywc-parallel-executor`를 72단어 대신 8,465단어로 잰다.
- Phase 000058 완료 (hard gate) — FR-5의 enforcement 모드가 FR-3의 증거 게이트에 달려 있다.

### Depended By

- `000059-020-infra-description-cap-validator` — **모든 description이 이미 예산 안에 있어야** 상한 검사를 켤 수 있다. 순서를 뒤집으면 켜는 순간 CI가 깨진다.

## Key Files

- 80단어 초과 29개 `claude-code/skills/ywc-*/SKILL.md` — **`description:` 값만**
- AC14 측정 기록

## Notes

- 29개 목록(측정치): `ywc-design-renew`(148), `ywc-onboard-repo`(148), `ywc-refactor-clean`(128), `ywc-confidence-gate`(127), `ywc-worktrees`(127), `ywc-docker-isolate`(121), `ywc-receive-review`(116), `ywc-handle-pr-reviews`(112), `ywc-review-learnings`(112), `ywc-project-docs`(108), `ywc-tdd-ritual`(107), `ywc-plan`(106), `ywc-brainstorm`(102), `ywc-project-mission`(100), `ywc-iac-author`(99), `ywc-spec-writer`(98), `ywc-infra-design`(97), `ywc-infra-review`(97), `ywc-debug-rootcause`(96), `ywc-spec-ready`(95), `ywc-impl-review`(92), `ywc-changelog-release-notes`(90), `ywc-e2e-test-strategy`(90), `ywc-incident-postmortem`(89), `ywc-setup-language`(87), `ywc-project-scaffold`(86), `ywc-verify-done`(85), `ywc-finish-branch`(84), `ywc-ui-ux-review`(82). **구현 시 재측정하라** — 이 목록은 착수 시점 기준이다.
- **단어 세기는 locale 비의존이어야 한다.** `wc -w`는 CJK가 많은 46개 중 30개에서 locale에 따라 자기 자신과 불일치한다. `000055-010`이 쓴 도구를 그대로 쓴다.
- 파일이 29개로 많지만 편집은 각 파일의 `description:` 값 **한 곳**뿐이다.

## Out of Scope

- validator 구현, frontmatter key 추가, body 수정

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-*/SKILL.md` — **`description:` 값만** (다른 frontmatter key와 body는 건드리지 않는다)

### Shared Surfaces

- `.claude/skills/ywc-toolkit-eval/scripts/score.py` — **read-only.** A2/A3/A4의 canonical 판정처.
- `validate-skill.sh` — `000055-010`의 수리된 추출기를 read-only로 사용.

### Conflicts With

- `000059-020-infra-description-cap-validator` — 이 task가 켜는 검사의 대상이다. 반드시 `-010` 완료 후 `-020`.

### Parallelizable After

- Phase 000058 완료 **및** `000055-010` merge

### Task Verify

- 46개 전부 description ≤ **80단어** (수리된 추출기 기준)
- 46개 전부 A4 통과 — 한글·일본어 문자가 **둘 다** 남아 있다
- 46개 전부 `(ywc) Use when` 으로 시작하고 `Do not use (for|during|when|in)` 를 포함한다
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` → **regression 0건** (S2 점수가 하나도 안 내려간다)
- AC14 기록: baseline · post · delta 세 값, 모두 **같은 도구**로 측정
