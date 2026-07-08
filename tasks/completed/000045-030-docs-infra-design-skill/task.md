# task: 000045-030-docs-infra-design-skill

## Prerequisites
- [ ] `000044-020`(공유 refs) 완료

## Allowed Edit Scope
`claude-code/skills/ywc-infra-design/**`, `codex/skills/ywc-infra-design/**` 만.

## Stop Conditions
- anti-trigger 경계가 기존 스킬과 겹쳐 오라우팅 위험이 있으면 중단 후 보고.

## Implementation Steps
- [ ] `claude-code/skills/ywc-infra-design/SKILL.md` 저작 — 스펙 §2.1 (ywc-infra-design)의 frontmatter(name+description, 트리거+anti-trigger)와 body 구조 반영
- [ ] `README.en.md` 저작 후 `README.md`(Korean)/`README.ja.md`/`README.ko.md` 작성(Tier1 필수)
- [ ] 공유 references(providers/iac-tools/lenses) 링크
- [ ] `codex/skills/ywc-infra-design/` 미러 — SKILL.md에서 CC 전용 frontmatter 필드 제거, README 4종, `agents/openai.yaml`(display_name/short_description/default_prompt)
- [ ] dispatch/anti-trigger 문구를 스펙 §4·§5와 정합

## Task Verify
- [ ] `test -f claude-code/skills/ywc-infra-design/SKILL.md`
- [ ] `test -f codex/skills/ywc-infra-design/agents/openai.yaml`
- [ ] `for f in README.md README.en.md README.ja.md README.ko.md; do test -f claude-code/skills/ywc-infra-design/$f || echo MISSING; done`

## Verification
- [ ] `bash scripts/validate.sh` exit 0
- [ ] markdownlint 통과
