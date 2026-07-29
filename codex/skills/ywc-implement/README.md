# ywc-implement

승인된 단일 specification 또는 ticket을 직접 구현하는 Codex Skill입니다.

## 입력

`--spec <repo-relative-path>` 또는 `--ticket <reference>` 중 하나만 허용합니다.
승인 증거와 acceptance criteria가 없으면 `NEEDS_CONTEXT`를 반환합니다.

## 흐름

깨끗한 baseline과 feature branch를 확인하고, 기존 패턴을 조사합니다. 동작 변경은 TDD를 수행합니다. Focused check와 전체 검증 후 `ywc-impl-review`를 실행하고, 통과한 경우에만 conventional commit을 만듭니다.

다중 Layer 생성은 `ywc-code-gen`, task directory 실행은 `ywc-sequential-executor`를 사용합니다.

## 보고

변경 파일, 검증 명령과 exit status, review status, commit SHA, 미해결 우려를 보고합니다. PR 생성과 force-push는 하지 않습니다.

자세한 설명은 [English README](./README.en.md)를 참고하세요.
