# 000045-010-infra-agent-lens-extensions

## Purpose
기존 리뷰 에이전트를 확장해 인프라 리뷰 렌즈를 흡수한다(신규 리뷰어 남발 방지). `ywc-security-engineer`에 IaC 오구성 reference, `ywc-performance-engineer`에 FinOps reference를 추가한다.

## Scope
- `ywc-security-engineer` (CC .md + Codex .toml) + `references/iac-security.md`
- `ywc-performance-engineer` (CC .md + Codex .toml) + `references/finops.md`

## Spec Reference
### Primary Sources
- `docs/ywc-plans/infra-skill-suite-design.md` §3 (기존 에이전트 확장), §2.3 (infra-review 3-lens)
### Summary
security-engineer는 IaC 오구성 taxonomy를, performance-engineer는 right-sizing/예약·스팟/데이터 전송 비용을 참조하도록 description 트리거를 보강하고 reference를 링크한다.
### Out of Scope (from spec)
신규 리뷰어 에이전트 생성 금지(확장으로 처리). 가용성/신뢰성 렌즈는 cloud-engineer가 담당.

## Criticality
critical — Notes: `ywc-security-engineer` 확장은 보안 표면을 다룸(heuristic: security keyword). 정의 문서 편집이므로 실제 위험은 낮으나 critical로 기록, 오탐 시 normal 강등 가능.

## Dependencies
- **Depends On**: `000044-020` — lens taxonomy 공유
- **Depended By**: `000045-040-docs-infra-review-skill` — 확장된 에이전트를 dispatch

## Key Files
- `claude-code/agents/ywc-security-engineer.md`, `codex/agents/ywc-security-engineer.toml`
- `claude-code/agents/ywc-performance-engineer.md`, `codex/agents/ywc-performance-engineer.toml`
- `references/iac-security.md`, `references/finops.md`

## Notes
- description 확장 시 기존 앱-보안/앱-성능 트리거를 훼손하지 않도록 append-only로 보강.

## Out of Scope
- infra-review 스킬 자체 — 045-040.

## Parallel Execution Metadata
- **Ownership**: 위 4개 에이전트 파일 + `references/iac-security.md`, `references/finops.md`
- **Shared Surfaces**: 기존 에이전트 description(앱 리뷰 경로와 공유) — 회귀 주의
- **Conflicts With**: (None identified)
- **Parallelizable After**: `000044-020`
- **Task Verify**: `test -f references/iac-security.md && test -f references/finops.md && bash scripts/validate.sh`
