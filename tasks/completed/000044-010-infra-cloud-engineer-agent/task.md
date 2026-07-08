# task: 000044-010-infra-cloud-engineer-agent

## Prerequisites
- [ ] (없음 — 배치 첫 태스크)

## Allowed Edit Scope
`claude-code/agents/ywc-cloud-engineer.md`, `codex/agents/ywc-cloud-engineer.toml` 만.

## Stop Conditions
- backend-coder 에이전트 frontmatter 스키마가 예상과 다르면 중단 후 보고.

## Implementation Steps
- [ ] `claude-code/agents/ywc-backend-coder.md`를 참조 템플릿으로 열어 frontmatter/본문 구조 파악
- [ ] `claude-code/agents/ywc-cloud-engineer.md` 생성: name/description(트리거 KR/EN/JP + "Do not use for" 포함), Mission=Terraform 단일 IaC 작성·`terraform validate/plan` 검증·reliability lens 리뷰, tools=Read/Write/Edit/Bash/Grep/Glob
- [ ] `codex/agents/ywc-cloud-engineer.toml` 생성: 기존 `codex/agents/ywc-*.toml` 구조 준수, 출력 계약 `Status: DONE|DONE_WITH_CONCERNS|BLOCKED|NEEDS_CONTEXT` + `Next action:` 명시
- [ ] description "Do not use for"에 backend-coder/architect/security-engineer/infra-design 경계 명시

## Task Verify
- [ ] `test -f claude-code/agents/ywc-cloud-engineer.md`
- [ ] `test -f codex/agents/ywc-cloud-engineer.toml`

## Verification
- [ ] `bash scripts/validate.sh` exit 0
