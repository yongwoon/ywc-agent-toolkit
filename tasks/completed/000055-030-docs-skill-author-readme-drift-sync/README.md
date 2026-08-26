# 000055-030-docs-skill-author-readme-drift-sync

## Purpose

`ywc-skill-author`의 6개 locale README에 있는 **기존 드리프트**를 먼저 잡는다. READMEs는 규칙을 "A1–A13"이라 적지만 skill은 이미 A14에 있고, "18개 production ywc-* skill"이라 적지만 실제로는 46개다. FR-4/FR-5가 이 드리프트를 더 벌리기 전에 baseline을 맞춘다.

## Scope

- `claude-code/skills/ywc-skill-author/README.md` 및 `README.{en,ja,ko,es,zh}.md`의 rule 범위 표기를 실제 최고 rule ID(A14)에 맞춘다.
- 같은 파일들의 skill 수 표기를 실제 수(46)에 맞춘다.
- 그 외 rule 목록/설명이 `SKILL.md`와 어긋난 부분을 동기화한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-pruning-pilot.md#fr-7-sync-ywc-skill-authors-readme-locale-set`
- `docs/ywc-plans/skill-pruning-pilot.md` AC16
- `docs/ywc-plans/skill-pruning-pilot.md#existing-constraints-touched` — `ywc-skill-author/README*.md` 행

### Summary

이것은 **기존 드리프트만** 고치는 task다. AC16의 진짜 요구("A7/A15/A16을 바꾸는 변경은 **같은 커밋**에서 README를 갱신한다")는 규칙을 실제로 바꾸는 task들(`000058-010`, `000059-040`)이 각자 자기 커밋 안에서 지킨다. 이 task를 먼저 착지시키는 이유는, 그 뒤의 규칙 변경 task들이 드리프트 수정과 규칙 변경을 한 커밋에 뒤섞지 않고 순수하게 자기 규칙 변경만 반영하게 하려는 것이다.

### Out of Scope (from spec)

- **A7 quota 제거를 선반영하지 않는다.** AC9의 증거 게이트는 아직 실행되지도 않았다. 여기서 "≥5 요구가 사라졌다"고 문서화하면 게이트가 실패했을 때 거짓 문서가 남는다.
- A15/A16 (아직 존재하지 않는 규칙) 문서화
- `codex/skills/**`, `plugins/**` README

## Criticality

`normal` — 문서 전용. 실행 가능한 규칙이나 CI 게이트를 건드리지 않는다.

## Dependencies

### Depends On

- `000053-010-refactor-skill-author-audit-workflow` — 부모 spec이 `ywc-skill-author`에 audit workflow를 추가하며 README를 건드릴 수 있으므로, 그 위에 쌓는다.

### Depended By

- `000058-010-infra-retire-a7-quota` — 깨끗한 README baseline 위에서 A7 변경만 반영한다.
- `000059-040-infra-invocation-tier-validator` — 같은 이유로 A15/A16 추가만 반영한다.

## Key Files

- `claude-code/skills/ywc-skill-author/README.md`
- `claude-code/skills/ywc-skill-author/README.en.md`
- `claude-code/skills/ywc-skill-author/README.ja.md`
- `claude-code/skills/ywc-skill-author/README.ko.md`
- `claude-code/skills/ywc-skill-author/README.es.md`
- `claude-code/skills/ywc-skill-author/README.zh.md`

## Notes

- rule 범위와 skill 수는 **`SKILL.md`와 파일 시스템에서 직접 확인해서** 쓴다. 사양이 인용한 수(A14, 46)도 재확인하라 — `000053-010`이 규칙을 추가했다면 최고 rule ID가 A14보다 높을 수 있다.
- 6개 locale이 **모두** 갱신되어야 한다. 하나라도 빠지면 AC16의 "no README states a rule range ending below the highest rule ID" 관찰식이 깨진다.

## Out of Scope

- `SKILL.md` 규칙 본문 수정
- 새 규칙 추가

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-skill-author/README{,.en,.ja,.ko,.es,.zh}.md` (6개 파일, 단독 소유)

### Shared Surfaces

- README locale set — `000058-010`과 `000059-040`이 나중에 같은 6개 파일을 편집한다(다른 phase이므로 충돌 없음).

### Conflicts With

- (동일 phase 내에서는 없음 — `000055-010/-020/-040`과 파일이 겹치지 않는다.)

### Parallelizable After

- `000053-010-refactor-skill-author-audit-workflow`

### Task Verify

- 6개 README 어느 것도 `SKILL.md`의 최고 rule ID보다 낮은 값에서 끝나는 rule 범위를 적지 않는다
- 6개 README 어느 것도 실제 skill 수(`ls claude-code/skills/ | grep -c '^ywc-'`) 외의 수를 적지 않는다
- 6개 README 모두 같은 커밋에 포함된다
