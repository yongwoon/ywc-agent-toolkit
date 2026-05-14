# Merge Dependabot Skill

Dependabot이 생성한 Pull Request를 안전하게 일괄 Merge하는 Codex Skill입니다.

## 개요

Dependabot PR을 탐지하고 사전 안전 검증을 수행한 뒤, PR 번호 오름차순으로 순차 처리합니다.

### 주요 기능

- Dependabot PR 일괄 탐지 및 Merge
- Security 관련 PR만 처리하는 모드 지원
- Dockerfile Base Image 변경, Major Version 업그레이드, CI Status 사전 점검
- 가능한 경우 Conflict 자동 해결 시도
- 처리 후 Summary Report 생성

## 사용 방법

```text
/merge-dependabot
/merge-dependabot security
```

자연어 Trigger는 [SKILL.md](./SKILL.md)에 정의되어 있습니다.

## 전제 조건

- `gh` CLI 설치 및 인증 완료
- 저장소에 대한 Merge 권한 보유
- Dependabot PR이 이미 존재함

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Japanese](./README.ja.md)
