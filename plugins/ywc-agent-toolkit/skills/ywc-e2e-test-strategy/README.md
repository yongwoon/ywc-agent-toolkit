# ywc-e2e-test-strategy

Playwright 기반 자동화 E2E 테스트 전략을 설계하고 구현하는 Skill입니다. 새 프로젝트의 Playwright 초기 설정부터 기존 프로젝트의 Coverage 점검, 특정 User Flow 테스트 생성, GitHub Actions CI 연동까지 한 번에 처리합니다.

## 사용 시나리오

- **신규 프로젝트**: "Playwright 설정해줘", "E2E 테스트 처음 추가하려고 해"
- **기존 프로젝트 점검**: "E2E coverage 어디가 부족한지 봐줘", "빠진 critical path 찾아줘"
- **단일 Flow 추가**: "로그인 flow E2E 테스트 작성해줘", "결제 페이지 Playwright 테스트 만들어줘"
- **CI 연동**: "GitHub Actions에 E2E 붙이고 싶어"

## 사용 방법

```bash
/ywc-e2e-test-strategy --init           # 새 프로젝트 Playwright 설정
/ywc-e2e-test-strategy --audit          # 기존 Coverage 점검
/ywc-e2e-test-strategy --flow login     # 특정 Flow 테스트 생성
/ywc-e2e-test-strategy --init --ci      # 초기 설정 + GitHub Actions 연동
```

또는 자연어로 호출:

> "Playwright로 E2E 테스트 전략 잡아줘"
> "Critical path 자동화해줘"
> "E2E 커버리지 점검해줘"

## Mode별 동작

| Mode | Flag | 언제 사용 |
|------|------|-----------|
| Init | `--init` | `playwright.config.*` 없을 때 |
| Audit | `--audit` | 기존 E2E 테스트 있을 때 |
| Flow | `--flow <name>` | 특정 User Flow 테스트 추가 시 |

Flag 없이 호출하면 파일시스템 상태로 자동 감지합니다.

## 출력

- `playwright.config.ts` — 환경변수 기반 baseURL 설정
- `e2e/*.spec.ts` — Critical path별 테스트 파일
- `.github/workflows/e2e.yml` — CI 연동 Workflow (`--ci` 또는 `--init` 시)
- Audit report — Coverage 갭 및 Flaky 위험 분석

## 관련 Skill

- `ywc-gen-testcase` — 수동 검증 Testsheet 생성 (자동화가 아닌 사람이 확인)
- `ywc-impl-review` — 코드 레벨 구현 검토
- `ywc-security-audit` — 인증/입력 처리 보안 감사
