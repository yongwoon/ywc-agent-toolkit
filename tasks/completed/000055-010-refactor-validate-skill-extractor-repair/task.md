# 000055-010-refactor-validate-skill-extractor-repair — Implementation Checklist

## Prerequisites

- [ ] `000053-010-refactor-skill-author-audit-workflow` is completed and merged.
- [ ] `.claude/skills/ywc-toolkit-eval/scripts/score.py`의 `split_frontmatter()`(`:66-75`)와 `parse_yaml_lite()`(`:91`)를 읽고 reference 동작을 확인했다.

## Allowed Edit Scope

- [ ] `claude-code/skills/ywc-skill-author/scripts/validate-skill.sh` 만 편집한다.
- [ ] `score.py`는 읽기 전용이다. 어떤 skill의 `SKILL.md`도 편집하지 않는다.

## Stop Conditions

- [ ] 수리 후 46개 중 어느 하나라도 reference parser와 카운트가 불일치하면 멈추고 보고한다.
- [ ] A2 또는 A3 판정이 어느 skill에서든 뒤집히면 멈춘다 — 그것은 substring 검사를 깨뜨렸다는 뜻이다.
- [ ] 두 번째 parser를 추가해야만 통과할 것 같다면 멈춘다 (사양이 금지한다).

## Implementation Steps

- [ ] `validate-skill.sh:31-35`의 awk 추출기를 읽고, 현재 정지 조건이 `^[A-Za-z_]+:` 뿐임을 확인한다.
- [ ] **Part 1**: 추출기를 frontmatter 블록에 묶는다 — 여는 `---` 이후 시작, 닫는 `---`에서 정지. body 라인은 절대 읽지 않는다.
- [ ] **Part 2**: next-key 정규식을 `^[A-Za-z_][A-Za-z0-9_-]*:` 로 교체한다 (`score.py::parse_yaml_lite:97`의 `^([A-Za-z_][\w-]*):`와 동일 의미). 하이픈을 매칭해야 `allowed-tools:`가 값으로 새지 않는다.
- [ ] word count를 locale 비의존으로 만든다: awk의 whitespace 토큰 카운트를 쓰거나 `LC_ALL=C`를 고정한다. `wc -w`를 locale 고정 없이 쓰지 않는다.
- [ ] 46개 skill 전체를 도는 parity 확인 루프를 실행해, repaired 추출기의 단어 수가 reference(`split_frontmatter` → `parse_yaml_lite`) 카운트와 **모두** 일치함을 확인한다.
- [ ] 네 개의 regression fixture를 확인한다: `ywc-parallel-executor` 72, `ywc-plan` 106, `ywc-impl-review` 92, `ywc-handle-pr-reviews` 112.
- [ ] corpus 합계가 **4,154 단어**임을 확인하고 기록한다 (`000059-030`의 AC14 baseline 근거가 된다).

## Task Verify

- [ ] `for d in claude-code/skills/ywc-*/; do bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh "$d" || echo "FAILED: $d"; done` — `FAILED:` 라인이 하나도 없다.
- [ ] parity 루프가 46/46 일치를 출력한다.
- [ ] 네 fixture가 72 / 106 / 92 / 112를 낸다.

## Verification

- [ ] `bash scripts/validate.sh` 통과.
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 통과 (AC13).
- [ ] `git diff`가 `validate-skill.sh` 외의 파일을 건드리지 않는다.
