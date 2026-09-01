# 000003-010-infra-update-toolkit-readme — Implementation Checklist

## Prerequisites
- [ ] `000002-010-infra-implement-hook-installer` 완료(merge) 확인
- [ ] `bash scripts/install.sh --list --hooks` 가 정상 출력되는지 확인 (CLI 인터페이스 확정 여부)

## Allowed Edit Scope
- [ ] `README.md` (root) 만 편집
- [ ] 이 범위 밖 편집이 필요한 경우 중단 후 보고

## Stop Conditions
- [ ] `bash scripts/install.sh --hooks` CLI 인터페이스가 Spec과 다른 경우 — Task 2 확인 후 보고
- [ ] 다국어 README(`README.ko.md` 등) 업데이트 요청 — Spec Out of Scope, 중단

## Implementation Steps

- [ ] **기존 README.md 구조 파악**
  - [ ] Key Commands 섹션 위치 확인
  - [ ] Skills 설치 예시 포맷 확인 (동일 스타일로 Hook 섹션 작성)

- [ ] **Hook 설치 섹션 추가**
  - [ ] "## Hooks" 또는 기존 "## Key Commands" 섹션 내 적절한 위치에 추가
  - [ ] 설치 명령 예시 코드 블록 작성:
    ```bash
    bash scripts/install.sh --hooks                         # 전체 global 설치
    bash scripts/install.sh --hooks --local                 # 전체 local 설치
    bash scripts/install.sh --hooks block-dangerous-commands cost-tracker  # 선택 설치
    bash scripts/install.sh --list --hooks                  # 설치 가능 목록
    ```
  - [ ] 의존성 안내 추가: `jq` 필수, `uv` 필수 (Python Hook 실행용)
  - [ ] 설치 가능 Hook 7개를 간단한 테이블로 나열 (이름, 역할)
  - [ ] `CCH_SLA_WEBHOOK` 환경변수가 필요한 `notify-permission` Hook 주석 추가

## Task Verify
- [ ] `grep -q '\-\-hooks' README.md && echo "Hook 섹션 존재"`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] `bash scripts/validate.sh` 통과 (markdownlint 포함)
- [ ] build 없음 (markdown-only 변경)
