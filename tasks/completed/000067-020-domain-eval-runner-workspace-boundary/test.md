# 000067-020-domain-eval-runner-workspace-boundary — Manual Test Plan

`claude` CLI 라는 외부 실행체를 호출하므로 fake adapter 만으로는 덮이지 않는 구간이 있다.

## 1. 실제 CLI 로 1 케이스 실행

**Steps**
1. 안전한 대상(파일을 쓰지 않는 skill)으로 case 를 하나 준비한다
2. `python3 .claude/skills/ywc-toolkit-eval/scripts/runner.py --case <id>` 실행

**Expected Result**
- 상태가 `PASS` 또는 `FAIL` 중 하나로 나온다 (`ERROR` 가 아니다)
- 결과 레코드가 `docs/skill-agent-eval/claude/runs/<run-id>/` 에 생성된다
- `git status` 에 해당 `runs/` 가 나타나지 않는다 (gitignore 적용)

## 2. 파괴적 skill 의 workspace 봉쇄

**Steps**
1. 파일을 생성·커밋하는 skill 을 대상으로 case 를 준비한다
2. 저장소 루트에서 `git status --porcelain` 을 기록한다
3. runner 를 실행한다
4. 다시 `git status --porcelain` 을 기록해 비교한다

**Expected Result**
- 두 출력이 **바이트 단위로 동일**하다
- skill 의 산출물은 임시 workspace 안에만 존재한다

## 3. 인증 부재 처리

**Steps**
1. `claude auth logout` 상태를 만들거나, CLI 를 PATH 에서 가린다
2. runner 를 실행한다

**Expected Result**
- 상태가 `SKIPPED_UNAVAILABLE` 또는 `ERROR` 이며 **`PASS` 가 아니다**
- baseline 을 갱신하지 않는다
