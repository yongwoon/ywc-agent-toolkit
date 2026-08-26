# 000010-010-docs-reviewer-anti-triggers

## Purpose
언어 리뷰어 에이전트 3종(`ywc-go-reviewer`, `ywc-python-reviewer`, `ywc-typescript-reviewer`)의 `Do not use for` 절에 형제 에이전트명(`ywc-*` 토큰)을 명시하여, `score.py` 의 FR6 충돌 억제기가 매칭하도록 한다. 이로써 A2 충돌 캡(현재 3)이 해제된다(FR1).

## Scope
- 3개 리뷰어 에이전트 frontmatter `description` 의 `Do not use for` 절에 형제 에이전트명 추가
- `ywc-python-reviewer.md` 본문의 stale 노트 1건 정정

## Spec Reference
### Primary Sources
- `docs/ywc-plans/ywc-toolkit-activation-fixes.md` — FR1, Amendment A1(인용 정정 `:31`/`:101`), A8
### Summary
세 리뷰어의 현재 절은 언어명("TypeScript / Python / Go")만 명시하고 에이전트명을 명시하지 않아 `_excluded_in_anti_trigger` 가 매칭하지 못한다. 절 내부(첫 `Do not use for` ~ 설명 끝)에 `ywc-<형제>` 토큰을 추가하면 `collision_pairs` 가 비고 `a2_collision_cap` 이 null 이 된다. 대칭을 위해 양쪽 모두 명시한다.
### Out of Scope (from spec)
- Codex 미러(`codex/agents/*.toml`) — 후속 plan
- 스코어러(score.py) 로직 변경 — 변경 없음

## Dependencies
### Depends On
- (없음) — Phase 000010 의 독립 편집 태스크
### Depended By
- `000011-010-infra-rebaseline-rescore` — 변경된 A2(캡 해제)를 기준선에 반영하고 재채점

## Key Files
- `claude-code/agents/ywc-go-reviewer.md` (frontmatter `Do not use for` ~:35)
- `claude-code/agents/ywc-python-reviewer.md` (frontmatter `Do not use for` :31, 본문 stale 노트 :101)
- `claude-code/agents/ywc-typescript-reviewer.md` (frontmatter `Do not use for` :16)

## Notes
- 토큰은 반드시 `Do not use for` 절 **내부**에 위치해야 한다(절 이전 문장의 언급은 FR6 가 인식하지 못함, A2).
- `--ci` 는 본 태스크에서 실행 금지(기준선 조기 덮어쓰기 방지). 검증은 `--format json` 읽기 전용으로만.

## Out of Scope
- 다른 에이전트/스킬 description
- history.mechanical.json 재기준선화(→ 000011-010)

## Parallel Execution Metadata
- **Ownership:** `claude-code/agents/ywc-go-reviewer.md`, `claude-code/agents/ywc-python-reviewer.md`, `claude-code/agents/ywc-typescript-reviewer.md`
- **Shared Surfaces:** score.py 충돌 채점 결과(편집은 안 함; 000011 이 기준선 반영) — 파일 비중첩
- **Conflicts With:** (None identified)
- **Parallelizable After:** (없음 — 즉시 실행 가능)
- **Task Verify:**
  - `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --format json` → 3개 리뷰어의 `collision_pairs` 가 `[]`, `a2_collision_cap` 가 `null`
  - `grep -c 'ywc-typescript-reviewer' claude-code/agents/ywc-go-reviewer.md` ≥ 1 (및 대칭)
