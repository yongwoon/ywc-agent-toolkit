# Project Scaffold - Directory Structure Generator

프로그램 언어, Framework, Architecture Pattern, 통신 Protocol, Project 규모를 조합하여 최적의 Directory 구조를 Markdown으로 생성하는 Codex Skill입니다.

## 개요

새 프로젝트를 시작할 때 "이 스택에서 Directory 구조를 어떻게 잡아야 하지?"라는 고민을 해결합니다. 단순한 언어별 구조뿐 아니라 **복합 조건** (예: FastAPI + GraphQL + Clean Architecture)도 지원하며, 각 Directory가 **왜 그 위치에 있는지** 설명을 함께 제공합니다.

### 주요 특징

- **복합 조건 지원**: 언어 + Framework + Protocol + Architecture를 자유롭게 조합
- **Scale별 구조 제공**: Small(MVP) / Medium(프로덕션) / Large(엔터프라이즈) 규모 대응
- **구조 설명 포함**: 각 Directory의 역할, 선택 이유, 의존 방향까지 설명
- **Domain 고려**: E-commerce, SaaS, Chat 등 프로젝트 특성 반영

## 지원 Tech Stack

| 분류 | 지원 항목 |
| --- | --- |
| **Language** | Python, Ruby, Go, JavaScript, TypeScript |
| **Framework** | FastAPI, Flask, Rails, Hanami, Gin, Echo, Next.js, NestJS, Astro, Express.js |
| **Architecture** | MVC, Layered, Clean Architecture, Hexagonal, DDD |
| **Protocol** | REST API, GraphQL, gRPC, WebSocket, Message Queue (Kafka, RabbitMQ) |
| **Scale** | Small (1-3명, MVP), Medium (3-8명, 프로덕션), Large (8명+, 엔터프라이즈) |

## 사용 방법

### 기본 사용

Codex에서 다음과 같이 입력합니다:

```
/project-scaffold FastAPI + Clean Architecture, medium scale
```

### 복합 조건 사용

여러 조건을 조합하여 입력할 수 있습니다:

```
/project-scaffold FastAPI + GraphQL + Clean Architecture, medium scale, SaaS 프로젝트
/project-scaffold Go + gRPC + DDD, large scale, e-commerce
/project-scaffold NestJS + WebSocket + REST API, small scale, chat app
/project-scaffold Rails API + GraphQL, medium scale
```

### 입력 요소

| 요소 | 필수 여부 | 설명 | 기본값 |
| --- | --- | --- | --- |
| Language | 필수 | 프로그래밍 언어 | - |
| Framework | 선택 | 사용할 Framework | 언어에 따라 추천 |
| Architecture | 선택 | Architecture Pattern | Framework 관례 따름 |
| Protocol | 선택 | 통신 Protocol | REST API |
| Scale | 선택 | 프로젝트 규모 | medium |
| Domain | 선택 | 프로젝트 도메인 | 범용 |

명시하지 않은 항목은 합리적인 기본값이 적용됩니다.

## Output 예시

Skill을 실행하면 다음과 같은 형태의 결과를 제공합니다:

```markdown
# My SaaS Project Directory Structure

> **Stack**: Python + FastAPI + GraphQL
> **Architecture**: Clean Architecture
> **Scale**: medium

## Directory Structure

project-root/
├── app/
│   ├── domain/                   # Domain layer - 순수 비즈니스 로직
│   │   ├── entities/             # Domain entities (Framework 의존성 없음)
│   │   ├── value_objects/        # Immutable value types
│   │   └── repositories/        # Repository interfaces (ABC)
│   ├── application/              # Use cases layer
│   │   ├── use_cases/            # 각 Use case 구현
│   │   └── dto/                  # Data Transfer Objects
│   ├── infrastructure/           # 외부 의존성 구현체
│   │   ├── database/
│   │   └── external/
│   ├── presentation/             # FastAPI router & schemas
│   │   └── api/v1/
│   └── graphql/                  # GraphQL layer
│       ├── types/
│       ├── queries/
│       └── mutations/
├── tests/
├── alembic/
└── pyproject.toml

## 주요 Directory 설명

### `app/domain/`
역할: 비즈니스 로직의 핵심. Framework 의존성 없는 순수 Python 코드.
이 구조를 선택한 이유: Clean Architecture에서 domain은 ...
의존 방향: 어디에도 의존하지 않음 (최내부 layer)
```

## Skill 파일 구조

```
project-scaffold/
├── SKILL.md                    # Skill 정의 (Workflow, Input 분석 로직)
├── README.md                   # 이 파일
└── references/                 # 언어/Protocol별 Reference
    ├── python.md               # Python (FastAPI, Flask)
    ├── ruby.md                 # Ruby (Rails, Hanami, Pure Ruby)
    ├── javascript.md           # JS/TS (Next.js, NestJS, Astro, Express)
    ├── go.md                   # Go (Standard, Gin/Echo, Go Kit)
    └── protocols.md            # GraphQL, gRPC, WebSocket, Message Queue
```

### Reference 파일 구성

각 Reference 파일은 다음과 같이 구성되어 있습니다:

- **Framework별 섹션**: 각 Framework에 대해 Small / Medium / Large 규모별 구조 제공
- **Architecture 변형**: 같은 Framework라도 Layered, Clean Architecture, DDD 등 패턴별 구조 수록
- **핵심 포인트**: 각 구조에서 중요한 설계 결정과 그 이유 설명
- **Convention**: 해당 언어/Framework의 공식 관례 정리

## 확장 방법

### 새로운 언어/Framework 추가

1. `references/` 디렉토리에 새 Reference 파일 생성 (예: `rust.md`)
2. Scale별(Small / Medium / Large) Directory 구조 작성
3. `SKILL.md`의 Reference 로드 섹션에 매핑 추가

### Protocol 추가

1. `references/protocols.md`에 새 Protocol 섹션 추가
2. 추가되는 Directory 구조와 Framework별 차이점 작성

## 관련 문서

- [Codex Skills Guide](../../README.md)
- [Release PR List Skill](../release-pr-list/SKILL.md) - 다른 Skill 작성 예시 참고
