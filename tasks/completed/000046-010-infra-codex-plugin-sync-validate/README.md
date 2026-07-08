# 000046-010-infra-codex-plugin-sync-validate

## Purpose
신규 Codex 스킬·에이전트를 플러그인 패키지에 동기화하고 리포 전체 검증을 통과시킨다(스펙 §6 롤아웃 마감).

## Scope
- `bash scripts/sync-codex-plugin.sh` 실행 → `plugins/ywc-agent-toolkit/skills/` 미러
- `.codex-plugin/plugin.json` 갱신
- `bash scripts/validate.sh` green, markdownlint 통과

## Spec Reference
### Primary Sources
- `docs/ywc-plans/infra-skill-suite-design.md` §6 (롤아웃 체크리스트, Codex 플러그인 동기화 사이트)
### Summary
스킬은 install.sh가 자동 탐색하므로 등록 편집 불필요. Codex 패키지는 sync 스크립트로 생성물이므로 직접 편집 금지, 스크립트로 재생성.
### Out of Scope (from spec)
스킬/에이전트 내용 저작 — 선행 태스크에서 완료.

## Criticality
normal

## Dependencies
- **Depends On**: `000045-010`, `000045-020`, `000045-030`, `000045-040`, `000045-050` (모든 Codex 스킬/에이전트 존재)
- **Depended By**: (None — 배치 마감)

## Key Files
- `plugins/ywc-agent-toolkit/skills/**` (생성물)
- `.codex-plugin/plugin.json`

## Notes
- `plugins/ywc-agent-toolkit/skills/`는 `codex/skills`에서 생성되는 미러 — 직접 편집 금지(pre-commit 훅이 강제).

## Out of Scope
- 신규 스킬 로직 변경.

## Parallel Execution Metadata
- **Ownership**: `plugins/ywc-agent-toolkit/**`, `.codex-plugin/plugin.json`
- **Shared Surfaces**: 전체 Codex 패키지 매니페스트 — 반드시 단독 실행
- **Conflicts With**: 모든 000045 스킬 태스크(선행 완료 필요, 병렬 금지)
- **Parallelizable After**: 모든 `000045-*`
- **Task Verify**: `bash scripts/sync-codex-plugin.sh && bash scripts/validate.sh`
