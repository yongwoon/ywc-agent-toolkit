# 000016-040-docs-skill-author-future-proofing

## Purpose
`ywc-skill-author`가 앞으로 생성하거나 개선하는 skill에 Karpathy-style failure defense를 domain-specific하게 반영하도록 만든다. 이 task는 generic slogan boilerplate 대신 실제 domain failure mode를 Rationalization Defense에 쓰게 한다.

## Scope
- `codex/skills/ywc-skill-author/SKILL.md` mandatory authoring rules 보강
- acceptable / unacceptable Rationalization Defense examples 추가
- template/cookbook reference가 있으면 같은 rule을 반영
- `ywc-skill-author` eval harness 존재 여부 확인 및 객관적 coverage 추가 또는 omission 기록

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-karpathy-guideline-integration.md#fr-4-update-skill-author-guidance` — skill author 요구사항
- `docs/ywc-plans/codex-karpathy-guideline-integration.md#fr-6-update-evals-where-objective` — eval 판단 요구사항
- `codex/skills/ywc-skill-author/SKILL.md` — main authoring rules
- `codex/skills/ywc-skill-author/references/rationalization-defense-cookbook.md` — cookbook reference if updated
- `codex/skills/ywc-skill-author/references/skill-template.md` — generated skill template if updated

### Summary
이 task는 future skills가 assumption, scope creep, overbuilding, missing verification failure를 domain-specific Rationalization Defense로 다루도록 만든다. Generic "do not hallucinate" 같은 문구만 복사하는 것은 충분하지 않다. 변경은 skill-author documentation/reference에 한정한다.

### Out of Scope (from spec)
- Individual existing skill Rationalization Defense rewrite — out of scope for this spec
- Custom agent prompt 변경 — handled by `000016-050-docs-custom-agent-bounded-evidence`
- generated plugin sync/validation — handled by `000017-010-infra-codex-karpathy-validation`

## Dependencies

### Depends On
- `000016-010-docs-principles-guideline-gap` — shared assumption/scope/verification vocabulary

### Depended By
- `000017-010-infra-codex-karpathy-validation` — generated plugin sync and validation

## Key Files
- `codex/skills/ywc-skill-author/SKILL.md` — main authoring rules
- `codex/skills/ywc-skill-author/references/rationalization-defense-cookbook.md` — domain-specific defense examples if needed
- `codex/skills/ywc-skill-author/references/skill-template.md` — template rule if needed
- `codex/skills/ywc-skill-author/evals/evals.json` — only if adding a new eval file matches local conventions

## Notes
- Current repository has no existing `codex/skills/ywc-skill-author/evals/evals.json`; inspect conventions before adding one.
- Prefer a concise rule in `SKILL.md` and examples in the existing cookbook if the examples would make `SKILL.md` too long.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-skill-author/SKILL.md`
- `codex/skills/ywc-skill-author/references/rationalization-defense-cookbook.md`
- `codex/skills/ywc-skill-author/references/skill-template.md`
- `codex/skills/ywc-skill-author/evals/evals.json` if created

### Shared Surfaces
- Future skill authoring contract: Rationalization Defense rules

### Conflicts With
- `(None identified)`

### Parallelizable After
- `000016-010-docs-principles-guideline-gap`

### Task Verify
- `rg -n "domain-specific|guessing missing context|adjacent cleanup|overbuilding|goal-specific verification|generic" codex/skills/ywc-skill-author`
- `python tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --root . --skill ywc-skill-author --format json || true`

## Out of Scope
- Updating every existing skill's Rationalization Defense.
- Adding broad new skill-author workflows.
- Editing generated plugin package manually.
