# 000059-010-refactor-description-word-cap — Implementation Checklist

## Prerequisites

- [ ] Phase 000058이 닫혔다 (`000058-010` GO 또는 `000058-020` NO-GO 중 하나가 merge됨).
- [ ] `000055-010`의 수리된 추출기가 merge되어 46/46 parity를 낸다.
- [ ] `score.py:286-288`의 A2/A3/A4 판정을 **직접 읽었다** — 이 셋이 재작성의 제약이다.
- [ ] `docs/ywc-plans/skill-pruning-pilot.md` FR-5, AC12, AC14를 원문으로 읽었다.

## Allowed Edit Scope

- [ ] `claude-code/skills/ywc-*/SKILL.md`의 **`description:` 값만** 편집한다.
- [ ] body, `name:`, `category:`, 그 외 frontmatter key는 건드리지 않는다.
- [ ] `score.py`는 **읽기 전용**이다 (Critical Surface).
- [ ] `validate-skill.sh`는 읽기 전용이다 (상한 검사는 `000059-020`이 넣는다).

## Stop Conditions

- [ ] **A4를 깨야만 80단어에 들어갈 것 같으면 멈춘다.** 한글이나 일본어를 전부 지우면 그 skill의 S2가 5→4로 떨어지고 `score.py --ci`가 build를 FAIL시킨다.
- [ ] 80단어에 맞추려면 사용자가 그 skill에 닿는 데 필요한 trigger를 지워야 할 것 같으면 **멈추고 finding으로 보고한다.** 예산 초과인 채로 두는 것이 정답이다 — 상한은 목표가 아니라 예산이다.
- [ ] `Do not invoke ...` 로 쓰고 싶어지면 멈춘다 — `validate-skill.sh`는 통과시키지만 `score.py`의 A3가 떨어뜨린다.
- [ ] `(ywc) Use before ...` 처럼 `Use when` 이외로 시작하고 싶어지면 멈춘다 — `score.py`의 A2는 `startswith("(ywc) Use when")` 이다.
- [ ] `wc -w`를 locale 고정 없이 쓰고 싶어지면 멈춘다.
- [ ] `invocation:` 같은 frontmatter key를 추가하고 싶어지면 멈춘다 — 이 spec에서 잘려나갔다.

## Implementation Steps

- [ ] **baseline을 먼저 측정하고 기록한다** (AC14): 수리된 추출기로 46개 description 단어 수 합계를 낸다. **사양의 리터럴을 쓰지 않고 도구의 출력을 쓴다.**
- [ ] 80단어 초과 skill 목록을 **재측정**한다 (README의 29개 목록은 착수 시점 기준).
- [ ] 각 초과 skill의 description을 다음 순서로 줄인다:
  1. 같은 trigger의 반복 표현 제거
  2. trigger를 부정형으로 되풀이하기만 하는 anti-trigger 항목 제거
  3. skill body와 중복되는 산문 제거
  4. 다국어 trigger 목록 **압축** — 단, **한글과 일본어는 반드시 남긴다** (A4)
- [ ] 각 재작성 후 4종 검사를 확인한다: ≤80단어 / `(ywc) Use when` 시작 / `Do not use (for|during|when|in)` 포함 / 한글·일본어 둘 다 존재.
- [ ] 80단어 안에서 도달 가능하게 만들 수 없는 skill이 있으면 **예산 초과인 채로 두고 finding으로 기록한다.**
- [ ] **rewrite 후 값을 같은 도구로 재측정**하고 baseline · post · delta를 기록한다 (AC14). 투영치는 4,154 → 3,445 단어(−17 %)다.

## Task Verify

- [ ] 46개 전부 (또는 보고된 finding을 제외한 전부) description ≤ 80단어
- [ ] `python3 -c` 등으로 46개 전부에 대해 한글·일본어 문자가 **둘 다** 존재함을 확인 (A4)
- [ ] 46개 전부 `(ywc) Use when` 으로 시작 (A2, `score.py` 기준)
- [ ] 46개 전부 `Do not use (for|during|when|in)` 포함, `Do not invoke` 사용 0건 (A3, `score.py` 기준)
- [ ] AC14 기록에 baseline · post · delta 세 값이 있고 셋 다 동일 추출기로 측정
- [ ] `git diff`가 `description:` 값 외의 frontmatter 줄이나 body를 건드리지 않는다

## Verification

- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` → **regression 0건** (AC13 — 어떤 skill의 S2도 내려가지 않았다)
- [ ] `bash scripts/validate.sh` 통과.
- [ ] `for d in claude-code/skills/ywc-*/; do bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh "$d" || echo "FAILED: $d"; done` → `FAILED:` 없음.
- [ ] `git diff`에 RD 섹션 삭제 줄 0건 (AC2).
- [ ] `codex/`, `plugins/` 아래 변경 0건.
