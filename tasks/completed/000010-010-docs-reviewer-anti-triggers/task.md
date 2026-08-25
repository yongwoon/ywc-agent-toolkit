# 000010-010-docs-reviewer-anti-triggers — 구현 체크리스트

## Prerequisites
- [ ] (없음) — Phase 000010 독립 편집 태스크

## Allowed Edit Scope
- `claude-code/agents/ywc-go-reviewer.md`
- `claude-code/agents/ywc-python-reviewer.md`
- `claude-code/agents/ywc-typescript-reviewer.md`
- 그 외 파일 수정 금지

## Stop Conditions
- `--ci` 실행 금지(기준선 조기 덮어쓰기 → 000011 소관). 본 태스크는 `--format json` 읽기 전용 검증만.
- 편집 후에도 `collision_pairs` 가 비지 않으면 중단·보고(토큰이 `Do not use for` 절 외부에 있을 가능성 — 위치 재확인)

## Implementation Steps
- [ ] `ywc-go-reviewer.md` `Do not use for` 절(~:35)의 "non-Go code (TypeScript / Python / …)" 를 에이전트명 형태로 교체: `use ywc-typescript-reviewer for TypeScript/JavaScript, ywc-python-reviewer for Python` (Swift/Rust 는 follow-up 유지)
- [ ] `ywc-python-reviewer.md` `Do not use for` 절(:31)에 `ywc-typescript-reviewer` + `ywc-go-reviewer` 명시
- [ ] `ywc-python-reviewer.md` 본문 stale 노트(:101) ".go to a Go reviewer (future Tier 2)" → ".go to ywc-go-reviewer"
- [ ] `ywc-typescript-reviewer.md` `Do not use for` 절(:16)에 `ywc-python-reviewer` + `ywc-go-reviewer` 명시
- [ ] 토큰이 모두 첫 `Do not use for` 이후 구간에 위치하는지 확인(FR6 슬라이싱 범위)

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --format json` → go/python/typescript-reviewer 의 `collision_pairs == []` 및 `a2_collision_cap == null`
- [ ] `grep -c 'ywc-typescript-reviewer' claude-code/agents/ywc-go-reviewer.md` ≥ 1, `grep -c 'ywc-go-reviewer' claude-code/agents/ywc-typescript-reviewer.md` ≥ 1 (대칭)
- [ ] `grep -c 'future Tier 2' claude-code/agents/ywc-python-reviewer.md` == 0 (stale 노트 제거 확인)

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] `--ci` 미실행(기준선 불변) — `git diff --quiet .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
