# 000067-020-domain-eval-runner-workspace-boundary — Implementation Checklist

## Prerequisites

- [ ] `000067-010` 머지 완료 — manifest 정규화와 registry 조회가 존재한다
- [ ] `docs/skill-agent-eval/claude/spike-2026-07-22.md` 의 "확정된 계약" 표를 읽었다

## Allowed Edit Scope

`scripts/runner.py`, `scripts/claude_adapter.py`, `scripts/test_runner.py` 신규 3파일과 `.gitignore` 의 아티팩트 루트 1줄. `score.py` 는 건드리지 않는다.

## Stop Conditions

- 스냅샷 비교로 미선언 변경을 잡지 못하는 구조가 되면 중단 — 이것이 없으면 파괴적 skill 을 평가할 수 없다
- `.gitignore` 규칙이 리포트까지 제외해버리면 중단하고 규칙을 재검토

## Hardening Gate

- [ ] RED 먼저: 미선언 경로에 쓰는 fake skill 이 `FAIL` 로 잡히는 테스트
- [ ] 연속 2회 실행에서 직전 workspace/아티팩트가 다음 실행에 보이지 않음을 증명
- [ ] **호스트 파일시스템 비관측성을 주장하지 않는다** — 테스트 이름과 주석에 `best-effort` 를 명시

## Implementation Steps

- [ ] `.gitignore` 에 `docs/skill-agent-eval/*/runs/` 1줄 추가 — 리포트(형제 `<date>-<name>.md`)는 추적이 유지되어야 한다
- [ ] `claude_adapter.py` 에 `dispatch(skill, prompt, cwd, disable_skills=False) -> dict` 작성 — `claude -p "/<skill> <prompt>" --output-format json` 을 `subprocess` 로 호출, `is_error`/`result` 파싱
- [ ] 동일 파일에 `FakeAdapter` 추가 — 테스트가 실제 CLI 없이 돌아야 한다
- [ ] `runner.py` 에 `make_workspace(run_id) -> Path` / `cleanup(ws, keep_on_fail)` 작성 — run id 별 고유 임시 디렉터리
- [ ] `runner.py` 에 `snapshot(ws) -> dict` 와 `diff_snapshot(before, after, allowed_paths) -> list` 작성 — 미선언 추가/수정/삭제/symlink 재지정을 반환
- [ ] `runner.py` 에 `run_case(case) -> dict` 작성 — 결정적 check 우선, 상태 enum 하나 반환, `activation_observability: "unavailable"` 기록
- [ ] 결과 레코드를 `docs/skill-agent-eval/claude/runs/<run-id>/` 에 리댁션하여 기록. 성공 workspace 즉시 삭제, 실패분은 `--retain-failed-artifacts` 로만 보존
- [ ] `test_runner.py` 작성: fake adapter PASS/FAIL, 미선언 쓰기 거부, symlink escape, 타임아웃 정리, 연속 실행 격리, run id 충돌 없음
- [ ] runner 시작 시 예상 dispatch 수와 예상 비용($0.54/dispatch 기준)을 stderr 로 출력

## Task Verify

- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/test_runner.py` 통과
- [ ] fake adapter 로 1 케이스 실행 후 `git status` 가 실행 전과 동일

## Verification

- [ ] `bash scripts/validate.sh` exit 0
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exit 0, baseline git diff 없음
