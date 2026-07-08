# 000044-010-infra-cloud-engineer-agent

## Purpose
`ywc-cloud-engineer` 워커 에이전트를 신규 생성한다. `ywc-backend-coder`가 명시적으로 배제한 인프라/IaC 실장 레인을 담당하는 read-write 워커이며, 이후 모든 인프라 스킬의 dispatch 대상이다.

## Scope
- `claude-code/agents/ywc-cloud-engineer.md` (CC 에이전트 정의)
- `codex/agents/ywc-cloud-engineer.toml` (Codex 에이전트 정의, `Status: DONE|DONE_WITH_CONCERNS|BLOCKED|NEEDS_CONTEXT` 출력 계약)

## Spec Reference
### Primary Sources
- `docs/ywc-plans/infra-skill-suite-design.md` §3 (신규 에이전트 ywc-cloud-engineer)
### Summary
Terraform 단일 고정(§7). 에이전트는 IaC 작성·수정과 `terraform validate`/`terraform plan` 검증, 신뢰성 렌즈 리뷰를 수행한다. tools: Read, Write, Edit, Bash, Grep, Glob.
### Out of Scope (from spec)
앱 서버 로직(backend-coder), 아키텍처 판단(architect), 앱 보안 정적분석(security-engineer), 인프라 토폴로지 초기 설계 결정(infra-design 스킬 소유).

## Criticality
normal — 에이전트 정의 문서. (Notes: `infra`/`secret` 경로를 다루는 워커이나 정의 자체는 실행 코드가 아님.)

## Dependencies
- **Depends On**: (None)
- **Depended By**:
  - `000045-020-docs-iac-author-skill` — dispatch 대상 워커 제공
  - `000045-040-docs-infra-review-skill` — reliability lens review 모드 워커 제공
  - `000045-050-docs-infra-optimize-skill` — SAFE 변경 실행 워커 제공

## Key Files
- `claude-code/agents/ywc-cloud-engineer.md`
- `codex/agents/ywc-cloud-engineer.toml`

## Notes
- backend-coder / frontend-coder 에이전트 파일의 스타일·frontmatter 구조를 그대로 따른다.
- Codex .toml은 기존 `codex/agents/ywc-*.toml` 출력 계약과 일치시킨다.

## Out of Scope
- 스킬(SKILL.md) 저작 — 별도 태스크.
- 실제 Terraform 코드 작성 — 런타임 산출물, 저작 대상 아님.

## Parallel Execution Metadata
- **Ownership**: `claude-code/agents/ywc-cloud-engineer.md`, `codex/agents/ywc-cloud-engineer.toml`
- **Shared Surfaces**: 에이전트 레지스트리(신규 파일이라 충돌 낮음)
- **Conflicts With**: (None identified)
- **Parallelizable After**: (batch baseline)
- **Task Verify**: `test -f claude-code/agents/ywc-cloud-engineer.md && test -f codex/agents/ywc-cloud-engineer.toml && bash scripts/validate.sh`
