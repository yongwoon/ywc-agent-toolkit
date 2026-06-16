# ywc-incident-postmortem

프로덕션 장애 발생 후 구조화된 Postmortem 문서를 작성하는 Skill입니다.
Timeline 재구성, Root Cause 분석 (5 Whys), 영향 범위 산정, 재발 방지 Action Item 생성,
그리고 선택적으로 Client 대응용 sanitized 보고서까지 생성합니다.

## 사용 시나리오

| 상황 | 예시 |
|------|------|
| 서비스 장애 | DB 연결 실패, 배포 후 서버 다운, CDN 장애 |
| 보안 사고 | API Key 노출, 인증 우회, 의심스러운 접근 |
| 데이터 손실/오염 | 잘못된 Migration, 실수로 인한 데이터 삭제 |
| 결제 오류 | 이중 결제, 결제 실패 루프 |
| 성능 급락 | 배포 후 Response Time 급상승 |

## 사용 방법

```
/ywc-incident-postmortem             # 대화형 Draft 모드
/ywc-incident-postmortem --template  # 빈 Template 출력
/ywc-incident-postmortem --client    # Client 대응용 보고서 추가 생성
```

## 출력물

- **Internal Postmortem** — 기술 상세, Timeline, 5 Whys, Action Item 포함
- **Client Report** (--client 시) — 내부 정보 제거, User 영향 중심 요약

## 관련 Skill

- `ywc-security-audit` — 장애 **예방** 목적 보안 감사 (pre-incident)
- `ywc-impl-review` — 일반 코드 품질 Review
- `ywc-changelog-release-notes` — Patch Release 후 변경 이력 문서화

## Localized Versions

- [English](README.en.md)
- [日本語](README.ja.md)
- [한국어](README.ko.md)
