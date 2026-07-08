# task: 000045-040-docs-infra-review-skill

## Prerequisites
- [ ] `000044-010`(reliability lens 워커), `000044-020`(lens refs), `000045-010`(확장 에이전트) 완료

## Allowed Edit Scope
`claude-code/skills/ywc-infra-review/**`, `codex/skills/ywc-infra-review/**` 만.

## Stop Conditions
- anti-trigger 경계가 기존 스킬과 겹쳐 오라우팅 위험이 있으면 중단 후 보고.

## Implementation Steps
- [ ] `claude-code/skills/ywc-infra-review/SKILL.md` 저작 — 스펙 §2.3 (ywc-infra-review)의 frontmatter(name+description, 트리거+anti-trigger)와 body 구조 반영
- [ ] `README.en.md` 저작 후 `README.md`(Korean)/`README.ja.md`/`README.ko.md` 작성(Tier1 필수)
- [ ] 공유 references(providers/iac-tools/lenses) 링크
- [ ] `codex/skills/ywc-infra-review/` 미러 — SKILL.md에서 CC 전용 frontmatter 필드 제거, README 4종, `agents/openai.yaml`(display_name/short_description/default_prompt)
- [ ] dispatch/anti-trigger 문구를 스펙 §4·§5와 정합

## Task Verify
- [ ] `test -f claude-code/skills/ywc-infra-review/SKILL.md`
- [ ] `test -f codex/skills/ywc-infra-review/agents/openai.yaml`
- [ ] `for f in README.md README.en.md README.ja.md README.ko.md; do test -f claude-code/skills/ywc-infra-review/$f || echo MISSING; done`

## Verification
- [ ] `bash scripts/validate.sh` exit 0
- [ ] markdownlint 통과
