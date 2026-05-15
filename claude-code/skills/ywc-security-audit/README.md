# ywc-security-audit

인증/결제/개인정보 관련 코드 변경 시, 또는 정기 보안 점검을 수행하는 Security Agent Skill 입니다.

## 사용 방법

```text
/ywc-security-audit --code api/src/middleware/
```

## 점검 항목 (OWASP Top 10)

1. Injection (SQL, Command, LDAP)
2. Broken Authentication (Token, Session)
3. Sensitive Data Exposure
4. XSS (Reflected, Stored, DOM)
5. Broken Access Control
6. Security Misconfiguration
7. SSRF
8. Input Validation
9. Rate Limiting
10. Timing Attacks

## 실행 Agent

### Phase 1 — 병렬 OWASP 분석 (Sonnet × 3)

| Subagent | OWASP 항목 |
|---|---|
| Auth & Data Subagent | A01 Injection · A02 Broken Auth · A03 Sensitive Data Exposure |
| Web Layer Subagent | A04 XSS · A05 Broken Access Control · A06 Security Misconfiguration |
| Infra & Input Subagent | A07 SSRF · A08 Input Validation · A09 Rate Limiting · A10 Timing Attacks |

### Phase 2 — Advisor (Opus, 최대 3회)

간접 증거를 가진 Critical/High Findings에 한해 Opus Advisor가 판단을 제공합니다.

## 특히 실행을 권장하는 상황

- middleware/ 변경 시 (인증/인가 로직)
- 외부 입력을 받는 API Endpoint 추가/변경 시
- 정기 보안 점검 (월 1회 등)

## 출력 형식

Critical / High / Medium / Low 심각도별 분류, 각 발견 사항에 file:line, 위험 설명, 권장 수정 포함

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
