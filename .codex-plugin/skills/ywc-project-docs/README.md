# project-docs

프로젝트의 `docs/` 디렉터리 구조와 규칙에 맞춰 한국어 또는 일본어 문서를 생성하는 Codex Skill.

대화 언어에 따라 자동으로 언어를 선택합니다. 기본값은 **한국어**이며, 일본어로 대화하거나 명시적으로 요청하면 일본어 문서를 생성합니다.

## 사용 방법

### 자동 트리거

아래 표현을 사용하면 Skill이 자동으로 활성화됩니다:

```
"문서 작성해줘"
"문서 만들어줘"
"문서 추가해줘"
"document this"
"write a doc"
"task 문서 만들어줘"
"아키텍처 문서 추가해줘"
"제품 문서 작성해줘"
"ドキュメント作成して"
"ドキュメントを書いて"
```

### 수동 호출

```
/project-docs
```

## Skill이 하는 일

1. **언어 선택** — 대화 언어를 감지하여 한국어 또는 일본어로 문서 생성
2. **디렉터리 라우팅** — 문서의 목적에 따라 올바른 디렉터리에 배치
3. **네이밍 규칙 적용** — 영문 소문자 + 하이픈, 접미사 최소화
4. **문서 구조 Template** — 관련 문서 블록, 목차, 섹션 넘버링 자동 적용
5. **교차 참조** — 관련 문서 간 양방향 링크 추가
6. **언어 정책** — 본문은 선택 언어, 기술 용어는 영문 유지 (음차 금지)
7. **LLM 읽기 순서** — `product → architecture → specification → plans` 순서 보장
8. **안티패턴 방지** — 폴더 경계 혼합, 중복 저장, 초안/공식 혼동 방지

## 디렉터리 매핑

### 공식 축 (핵심 문서)

| 요청 유형 | 배치 위치 |
|-----------|----------|
| 제품 목표, 범위, PRD | `docs/product/` |
| 시스템 설계, 기술 선택 | `docs/architecture/` |
| 기능별 상세 규칙, 구현 기준 | `docs/specification/` |
| 구현 순서, milestone | `docs/plans/` |

### 보조 축 (운영·자산·임시)

| 요청 유형 | 배치 위치 |
|-----------|----------|
| 운영 절차, 설정 Guide | `docs/manuals/` |
| 장애 대응, Known Issue | `docs/troubleshooting/` |
| 화면 시안, 디자인 자산 | `docs/design/` |
| 문서용 보조 이미지 | `docs/imgs/` |
| 미확정 아이디어, 임시 메모 | `docs/todo/` |

## 사용 예시

### Product 문서 생성

```
"제품 개요 문서 작성해줘"
→ docs/product/product-overview.md 생성
→ 제품 목표, 대상 사용자, 핵심 기능, 범위 섹션 포함
```

### Architecture 문서 생성

```
"인증 시스템 아키텍처 문서 작성해줘"
→ docs/architecture/authentication.md 생성
→ 시스템 개요, 계층 구조, 워크플로우, 비즈니스 로직 섹션 포함
```

### Specification 문서 생성

```
"결제 기능 스펙 문서 만들어줘"
→ docs/specification/billing.md 생성
→ Expected behavior, Constraint, Edge case, Acceptance criteria 포함
```

### 운영 Guide 생성

```
"OAuth 설정 가이드 문서 작성해줘"
→ docs/manuals/google-oauth-setup.md 생성
→ 설정 절차, 환경 구성, 체크리스트 포함
```

### 일본어 문서 생성

```
"認証システムのアーキテクチャドキュメントを書いて"
→ docs/architecture/authentication.md 생성 (일본어)
→ System 개요, Layer 구조, Workflow, Business 로직 섹션 포함
```

## 설치 위치

```
~/.codex/skills/project-docs/
├── README.md     ← 이 파일 (한국어)
├── README.en.md  ← English
├── README.ja.md  ← 日本語
├── README.ko.md  ← 한국어 (사본)
└── SKILL.md      ← Skill 정의
```

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
