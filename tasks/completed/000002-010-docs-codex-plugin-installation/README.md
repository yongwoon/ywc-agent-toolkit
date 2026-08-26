# 000002-010-docs-codex-plugin-installation

## Purpose

Codex CLI/App 사용자가 plugin install path와 기존 bash fallback을 명확히 구분할 수 있도록 root README와 localized README 정책을 정리한다.

## Scope

- `README.md` Installation section에 Codex CLI `/plugins` 안내 추가
- `README.md` Installation section에 Codex App sidebar Plugins 안내 추가
- Bash install fallback 안내 유지
- Marketplace availability 표현을 실제 상태에 맞게 보수적으로 작성
- Localized root README update 또는 explicit defer 정책 적용
- Translation dry-run으로 번역 영향 확인

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-plugin-distribution.md#functional-requirements` — FR-5
- `docs/ywc-plans/codex-plugin-distribution.md#iteration-1-amendments` — final package layout to describe
- `docs/ywc-plans/codex-plugin-distribution.md#out-of-scope` — marketplace submission exclusion

### Summary

문서 task는 구현된 Codex plugin package layout을 사용자에게 설명한다. README는 marketplace에 이미 등재된 것처럼 쓰면 안 되고, 실제 배포 가능 상태에 맞춰 future-safe wording을 사용해야 한다. Root README를 변경하면 localized README 처리 여부도 명시적으로 결정해야 한다.

### Out of Scope (from spec)

- Manifest/package layout implementation — `000001-010-infra-codex-plugin-package-layout`
- Validation implementation — `000001-020-infra-codex-plugin-validation`
- Official Codex marketplace submission — out of this feature scope

## Dependencies

### Depends On

- `000001-010-infra-codex-plugin-package-layout` — provides final manifest and package layout
- `000001-020-infra-codex-plugin-validation` — provides validation behavior to mention in docs

### Depended By

- (None — final documentation task)

## Key Files

- `README.md` — primary English/root install docs
- `README.ko.md` — Korean localized root README if same-PR translation is chosen
- `README.ja.md` — Japanese localized root README if same-PR translation is chosen
- `README.es.md` — Spanish localized root README if same-PR translation is chosen
- `README.zh.md` — Chinese localized root README if same-PR translation is chosen
- `CONTRIBUTING.md` — reference only for translation policy

## Notes

- Do not claim official Codex marketplace availability unless it is already true.
- If localized root README updates are deferred, state the deferral in PR description and include `bash scripts/translate.sh --dry-run` evidence.
- Keep bash install instructions available for local/manual install.
- Mention restart requirements only if already present or still correct.

## Parallel Execution Metadata

### Ownership

- `README.md`
- `README.ko.md`
- `README.ja.md`
- `README.es.md`
- `README.zh.md`
- Documentation wording for Codex plugin installation

### Shared Surfaces

- Root documentation
- Translation warning workflow
- Release/user-facing install instructions

### Conflicts With

- (None identified after Phase 000001 is merged)

### Parallelizable After

- `000001-010-infra-codex-plugin-package-layout`
- `000001-020-infra-codex-plugin-validation`

### Task Verify

- `bash scripts/translate.sh --dry-run`
- `bash scripts/validate.sh`
- `bash scripts/install.sh --list`

## Out of Scope

- Do not change skill README files unless translation tooling requires it.
- Do not change plugin manifest behavior.
- Do not add marketplace submission claims or badges.

