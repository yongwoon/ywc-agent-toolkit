# 000010-020-docs-agent-dispatch-boundaries — 구현 체크리스트

## Prerequisites
- [ ] (없음) — Phase 000010 독립 편집 태스크

## Allowed Edit Scope
- `claude-code/agents/ywc-qa-engineer.md`
- `claude-code/agents/ywc-doc-writer.md`
- 그 외 파일 수정 금지

## Stop Conditions
- `--ci` 실행 금지(→ 000011 소관). 읽기 전용 `--format json` 검증만.
- A3(tool-grant) 점수 상승을 목표로 Bash 권한을 제거하지 말 것(권한은 정당; 범위 밖)

## Implementation Steps
- [ ] FR2: `ywc-qa-engineer.md` `Do not use for` 절에 "test-first discipline (use ywc-tdd-ritual)" + "E2E strategy / Playwright setup (use ywc-e2e-test-strategy)" 추가
- [ ] FR2: in-scope 문장에서 "E2E suites" 제거(E2E 소유 주장 철회)
- [ ] FR3: `ywc-doc-writer.md` `Do not use for` 절(:10)에 `ywc-project-docs` + `ywc-skill-author` + `ywc-changelog-release-notes` 명시(라인 8 디스패처-컨텍스트 문장이 아니라 절 내부)
- [ ] FR3: 범용 문서 트리거를 구체 문구(README locale entry / in-code WHY comment / CHANGELOG entry)로 교체
- [ ] (선택, A6 명료성) qa-engineer Boundaries 에 "Bash 는 테스트 러너 호출 한정" 1줄 — A3 점수 변경 주장 금지

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --format json` 무오류
- [ ] `grep -c 'ywc-tdd-ritual' claude-code/agents/ywc-qa-engineer.md` ≥ 1 및 `grep -c 'ywc-e2e-test-strategy' claude-code/agents/ywc-qa-engineer.md` ≥ 1
- [ ] `grep -c 'E2E suites' claude-code/agents/ywc-qa-engineer.md` == 0
- [ ] `ywc-doc-writer.md` 에서 `ywc-skill-author` 가 첫 `Do not use for` 이후 구간에 존재(절 내부 배치 확인)

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] 기준선 불변: `git diff --quiet .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
