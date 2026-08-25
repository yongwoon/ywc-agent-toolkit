# 000014-010-docs-shared-tdd-boundary-contract — 구현 체크리스트

## Prerequisites
- [ ] `docs/ywc-plans/claude-code-executor-tdd-deep-module-gray-box.md`의 FR-1, AC1 확인
- [ ] 기존 `claude-code/skills/references/` 디렉터리 컨벤션 확인(`readable-code.md` 등)

## Allowed Edit Scope
- `claude-code/skills/references/tdd-deep-module-gray-box.md` (신규 생성만)

## Stop Conditions
- 개별 skill SKILL.md/README를 수정해야 할 것 같으면 중단(후속 task 소관)
- `codex/skills/**` 또는 `plugins/**`를 수정해야 할 것 같으면 중단
- 구조 변경이 `ywc-skill-author` 규칙과 충돌하면 중단하고 메타 skill 경유

## Implementation Steps
- [ ] `claude-code/skills/references/tdd-deep-module-gray-box.md` 생성, 6개 섹션 작성:
  - [ ] `When This Applies` — behavior change / bug fix / new public contract / cross-layer generation / task execution
  - [ ] `Feedback Loop (headlights, 함정 3)` — behavior change는 구현 확정 전 failing test가 RED로 성립(의도된 이유로 실패)해야 함; 최소 구현으로 GREEN; green 이후에만 refactor
  - [ ] `Deep Module Boundary (함정 4)` — body 전에 public interface(signature/DTO/props/service method) 설계, shallow wrapper 남발 금지; `readable-code.md` §G anti-dogma 인용
  - [ ] `Gray Box + Critical-Module Exception (함정 5)` — 기본은 contract 검증·internal 위임; critical module은 internal review 필수; canonical critical-path list(auth/authn/authz/session/oauth/jwt/token/password/credential/secret/crypto/encrypt/sign/payment/billing/invoice/checkout/finance/ledger/wallet/PII/webhook/upload/deserialize) + `CLAUDE.md` `critical_paths` override
  - [ ] `Allowed Exceptions` — docs-only/formatting/metadata/README locale/mechanical은 RED skip 가능하되 사유 명시
  - [ ] `Reporting Contract` — changed public contracts / RED로 처음 실패한 tests / internal review된 critical module / 명시적 예외
- [ ] critical-path 감지 시점 차이 명시: code-gen은 생성 후 파일 기준, executor는 task Ownership(구현 전) 기준(spec-validate Warning 반영)
- [ ] `readable-code.md`, `principles.md`, `confidence-gate.md`, `subagent-status-actions.md` 인용 링크 추가

## Task Verify
- [ ] `test -f claude-code/skills/references/tdd-deep-module-gray-box.md`
- [ ] `rg -n "Critical-Module Exception|Deep Module|headlights|Reporting Contract|critical_paths" claude-code/skills/references/tdd-deep-module-gray-box.md`

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] `git diff --name-only`에 `codex/` 및 `plugins/` 경로가 없음
