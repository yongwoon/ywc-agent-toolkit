# 000055-010-refactor-validate-skill-extractor-repair

## Purpose

`validate-skill.sh`의 `description` 추출기를 수리한다. 현재 두 가지 결함이 겹쳐 있어 정확한 단어 수 측정이 불가능하며, 이 수리 없이는 FR-5의 Tier-1 예산(AC12)이 실제 description 길이와 무관하게 15개 skill을 hard-fail 시킨다.

## Scope

- `claude-code/skills/ywc-skill-author/scripts/validate-skill.sh:31-35`의 awk 추출기를 in-place 수리한다.
- 수리는 **두 부분 모두** 필요하다. 하나만 적용하면 추출기는 여전히 틀린다.
  1. frontmatter 블록 경계(닫는 `---`)에서 멈추게 한다.
  2. next-key 정규식을 `^[A-Za-z_][A-Za-z0-9_-]*:` 로 넓힌다(하이픈 매칭).
- 46개 skill 전체에 대해 reference parser와 count parity를 검증한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-pruning-pilot.md#fr-5a-repair-the-description-extractor-prerequisite-for-fr-5-ac12a`
- `docs/ywc-plans/skill-pruning-pilot.md` AC12a (Reference parser / Word-counting method / Regression fixtures)
- `docs/ywc-plans/skill-pruning-pilot.md#existing-constraints-touched` — `validate-skill.sh:31-35` 행

### Summary

추출기는 frontmatter `---` 경계를 모른다. 유일한 정지 조건이 `^[A-Za-z_]+:` 에 매칭되는 body 라인이므로, **`description:`이 frontmatter의 마지막 key인 46개 중 15개 skill**에서는 body 전체를 삼킨다(`ywc-parallel-executor`가 실제 72 단어 대신 **8,465 "단어"**를 낸다). 같은 정규식이 하이픈을 매칭하지 않아 `ywc-handle-pr-reviews/SKILL.md:5`의 `allowed-tools:` key도 값 안으로 빨려 들어간다. 오늘 이 버그가 보이지 않는 이유는 A2/A3가 boolean substring 검사(`contains "(ywc) Use "`)여서 더 긴 capture가 깨뜨리지 못하기 때문이다.

canonical reference는 `score.py::split_frontmatter()` **다음** `parse_yaml_lite()` 이며, **이 순서가 지켜져야 한다**. `parse_yaml_lite`를 파일 전체에 호출하면 바로 이 버그를 재현한다. 엄격한 YAML은 쓸 수 없다 — `yaml.safe_load`는 46개 중 8개에서 실패한다(따옴표 없는 `description:` 값 안의 `Triggers: ` 콜론-공백이 plain scalar로서 invalid YAML).

### Out of Scope (from spec)

- 두 번째 parser 추가 (in-place 수리가 엄격히 낫다 — A2/A3의 잠재적 취약성도 함께 제거된다)
- `invocation:` key, tier 예산, word-count FAIL 로직 (000059 트랙 소유)
- `codex/skills/**`, `plugins/**`

## Criticality

`normal` — 사양의 Critical Surfaces는 `.claude/skills/ywc-toolkit-eval/**` 뿐이며 이 task는 그것을 건드리지 않는다. `validate-skill.sh`는 skill-local validator로, 이 변경은 A2/A3의 판정 결과를 바꾸지 않는다(더 짧아진 capture에서도 substring 검사는 동일하게 통과해야 하며, 그것이 Verification 항목이다).

## Dependencies

### Depends On

- `000053-010-refactor-skill-author-audit-workflow` — 부모 spec이 `ywc-skill-author/scripts/`에 audit script를 추가하므로, 같은 디렉토리를 편집하기 전에 merge되어 있어야 한다.

### Depended By

- `000059-030-refactor-callee-only-description-trim` — 신뢰할 수 있는 단어 수 없이는 trim 대상을 고를 수 없다.
- `000059-040-infra-invocation-tier-validator` — AC12의 예산 검사가 이 추출기 위에 세워진다.

## Key Files

- `claude-code/skills/ywc-skill-author/scripts/validate-skill.sh` (수정)

## Notes

- **선행 시도의 실패 사례가 사양에 기록되어 있다**: part 1만 명세한 수정이, 정규식까지 *조용히* 넓힌 구현으로 검증되어 통과했다. 명세된 수정은 여전히 깨져 있었는데도 검사는 초록이었다. 두 부분을 모두 명시적으로 확인하라.
- **word count는 locale에 의존하면 안 된다.** `wc -w`는 CJK가 많은 46개 중 30개 description에서 locale에 따라 자기 자신과 불일치한다 — 동일 파일이 dev 머신과 CI에서 다른 수를 낸다. awk 또는 Python으로 세거나 `LC_ALL=C`를 고정하라.
- `validate-skill.sh:9`가 `set -uo pipefail`(`-e` 없음)을 쓰는 것은 **의도된 것**이다 — `fail()` accumulator가 실패하는 `grep -q`에서 살아남아야 한다. 이 편차는 기존 것이며 유지한다.

## Out of Scope

- description 내용 자체의 수정 (측정만 한다)
- `score.py` 수정 (reference로 읽기만 한다)

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-skill-author/scripts/validate-skill.sh` (단독 소유)

### Shared Surfaces

- `claude-code/skills/ywc-skill-author/scripts/**` — `000053-010`이 같은 디렉토리에 audit script를 추가한다(다른 파일).
- `.claude/skills/ywc-toolkit-eval/scripts/score.py` — read-only reference로만 사용.

### Conflicts With

- `000059-040-infra-invocation-tier-validator` — 같은 파일을 편집한다. 반드시 순차 실행.

### Parallelizable After

- `000053-010-refactor-skill-author-audit-workflow`

### Task Verify

- 46개 skill 전체에 대해 repaired extractor 카운트 == reference(`split_frontmatter` → `parse_yaml_lite`) 카운트
- Regression fixtures: `ywc-parallel-executor` **72**, `ywc-plan` **106**, `ywc-impl-review` **92**, `ywc-handle-pr-reviews` **112**
- Corpus baseline: **4,154 단어**
- 46개 skill 전체 `validate-skill.sh` exit 0 (A2/A3 판정 불변)
