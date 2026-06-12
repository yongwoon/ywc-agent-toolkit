# ywc-ubiquitous-language

프로젝트의 Ubiquitous Language (공유 도메인 어휘) 문서를 생성하거나 업데이트하는 Skill입니다. 개발자, 도메인 전문가, LLM이 동일한 용어로 소통할 수 있도록 `docs/ubiquitous-language.md`를 관리합니다.

세 가지 Mode를 지원합니다: **new** (인터뷰 기반 신규 작성), **extract** (기존 Codebase에서 용어 추출), **update** (기존 문서 갱신).

## 사용 시나리오

- 프로젝트 초기에 팀 공용 도메인 용어집을 작성하고 싶을 때
- 기존 Codebase를 분석하여 암묵적으로 쓰이던 도메인 용어를 문서화하고 싶을 때
- 새로운 Feature 추가 후 용어집에 신규 개념을 반영하고 싶을 때
- LLM이 프로젝트 도메인 용어를 정확하게 이해하도록 CLAUDE.md에 참조를 추가하고 싶을 때

## 사용 방법

```bash
/ywc-ubiquitous-language
```

또는 자연어로 호출:

> "유비쿼터스 언어 문서 만들어줘"
> "도메인 용어 정리해줘"
> "ubiquitous language 업데이트해줘"
> "코드베이스에서 도메인 용어 추출해줘"

### Mode 자동 감지

| 조건 | 자동 선택 Mode |
|------|--------------|
| `docs/ubiquitous-language.md` 존재 | `update` |
| 파일 없음 + Source 파일 존재 (`src/`, `app/` 등) | `extract` |
| 파일 없음 + Source 파일 없음 | `new` |

Mode를 직접 지정하려면 `--mode new\|extract\|update` 사용.

## 입력

- (선택) 도메인 설명 — "우리 서비스는 B2B 전자상거래야"
- (선택) `--mode new|extract|update` — Mode 강제 지정
- (선택) `--context <이름>` — 특정 Bounded Context만 대상
- (선택) `--ddd` — DDD Type 컬럼 추가 (Entity / Value Object / Aggregate 등)
- (선택) `--output <경로>` — 출력 파일 경로 (기본: `docs/ubiquitous-language.md`)

## 출력

- `docs/ubiquitous-language.md` — Bounded Context별 용어 Table
- 완료 후: CLAUDE.md에 `@docs/ubiquitous-language.md` 추가를 권장하는 메시지 출력

## 출력 예시

```markdown
# Ubiquitous Language — ShopBot

<!-- updated: 2026-05-02 -->

## Bounded Contexts

| Context | Responsibility |
|---------|---------------|
| Order   | 주문 생성 ~ 완료 |

---

## Order

| Term      | Korean   | Definition                              | Synonyms to Avoid |
|-----------|----------|-----------------------------------------|------------------|
| Order     | 주문     | 고객이 상품 구매를 확정한 단위           | Cart, Purchase    |
| OrderItem | 주문 항목 | Order 내 단일 상품+수량 쌍 (불변)        | LineItem, CartItem |
```

## 관련 Skill

- `ywc-plan` — Spec 작성 전 용어집을 먼저 정의할 때 함께 사용
- `ywc-project-docs` — Project 전체 문서 구조 생성 (docs/ Directory skeleton)
- `ywc-spec-validate` — Spec 내 용어가 용어집과 일치하는지 검토
- `ywc-task-generator` — 용어집 확립 후 Task로 분해할 때 downstream
- `ywc-code-gen` — 코드 생성 시 용어집의 Canonical naming 적용
