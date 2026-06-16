# Project Scaffold - Directory Structure Generator

프로그래밍 언어, Framework, Architecture Pattern, Protocol, 프로젝트 규모를 조합해 적절한 Directory 구조를 Markdown으로 생성하는 Codex Skill입니다.

## 개요

새 프로젝트를 시작할 때, 선택한 스택에 맞는 Directory 구조를 정리할 수 있도록 돕는 Skill입니다.

### 주요 기능

- 언어, Framework, Protocol, Architecture의 복합 조건 지원
- Small, Medium, Large 규모별 구조 제안
- 각 Directory의 역할과 배치 이유 설명
- SaaS, E-commerce, Chat 등 Domain 특성 반영

## 사용 방법

```text
/project-scaffold FastAPI + Clean Architecture, medium scale
/project-scaffold Go + gRPC + DDD, large scale, e-commerce
```

자연어 Trigger는 [SKILL.md](./SKILL.md)에 정의되어 있습니다.

## Reference

- Framework 및 언어별 Reference는 [`references/`](./references)에 있습니다
- Trigger 조건과 상세 Workflow는 [SKILL.md](./SKILL.md)에 있습니다

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Japanese](./README.ja.md)
