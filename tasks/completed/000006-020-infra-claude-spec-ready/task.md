# Task: 000006-020-infra-claude-spec-ready

## Prerequisites

- [ ] `main` baseline 최신화
- [ ] upstream source 접근 가능 (`gh pr diff 120 --repo yongwoon/develop-with-llm`)
- [ ] `docs/ywc-plans/port-upstream-skill-prs-110-120-129.md` Workstream B·D 숙지

## Allowed Edit Scope

- `claude-code/skills/ywc-spec-ready/**` (신규)
- `claude-code/skills/ywc-spec-validate/**` (SKILL.md + README locale set)
- `claude-code/skills/ywc-agentic/SKILL.md` (Step 3 영역)
- `README.md` (Planning & Spec catalog row + Claude count)
- `README.ko.md` / `README.ja.md` / `README.es.md` / `README.zh.md` / `CLAUDE.md` (Claude count 숫자만)
- `.claude/skills/ywc-toolkit-eval/evals/**` (baseline)

다른 skill, `codex/**`, `claude-code/agents/**`, `claude-code/skills/CLAUDE.md` script table, `CHANGELOG.md`, `VERSION`은 수정 금지.

## Stop Conditions

- port 후 `grep -rn "tools/claude-code" claude-code/skills/ywc-spec-ready`가 0이 아니면 멈추고 보고
- `ywc-spec-ready` 또는 `ywc-agentic` 안에 `@skill-name` force-load 참조가 남아 있으면 멈추고 보고
- `bash scripts/validate.sh` 실패 시 멈추고 원인 보고

## Implementation Steps

- [ ] `gh pr diff 120 --repo yongwoon/develop-with-llm`로 upstream `tools/claude-code/skills/ywc-spec-ready/` 7개 file과 spec-validate/agentic hunk 확보
- [ ] `claude-code/skills/ywc-spec-ready/` 생성 후 7개 file 작성: `SKILL.md`, `README.md`/`.en`/`.ja`/`.ko`, `references/convergence.md`/`loop-log.md`
- [ ] `SKILL.md` frontmatter `name:`가 `ywc-spec-ready`와 일치 확인, runtime path는 `claude-code/` / `../` style로 정리
- [ ] `claude-code/skills/ywc-spec-validate/SKILL.md`에 PR #120의 `--advisor-budget` 4개 hunk(arg row, `X of N` header, budget-override 단락, looped-consumer note) 반영
- [ ] `claude-code/skills/ywc-spec-validate/README.md`/`.en`/`.ja`/`.ko` 각 1줄 갱신
- [ ] `claude-code/skills/ywc-agentic/SKILL.md` Step 3 Medium/Large path를 spec-ready loop 위임으로 rewire + downstream integration list 갱신 (2 hunk)
- [ ] root `README.md` **Planning & Spec** table(`ywc-onboard-repo` 행 부근, `~:189`)에 `ywc-spec-ready` row 추가
- [ ] skill count `37 → 38`로 변경: `CLAUDE.md:7`, `README.md:11`, `README.ko.md:12`, `README.ja.md:12`, `README.es.md:11`, `README.zh.md:12` — Claude Code skill 숫자만
- [ ] `.claude/skills/ywc-toolkit-eval/`에 `ywc-spec-ready` baseline entry 등록

## Task Verify

```bash
bash scripts/validate.sh
grep -rn "tools/claude-code" claude-code/skills/ywc-spec-ready                # 0
grep -rn "@ywc-" claude-code/skills/ywc-spec-ready claude-code/skills/ywc-agentic/SKILL.md   # force-load 없음
grep -c "ywc-spec-ready" README.md                                            # >= 1
grep -n "advisor-budget" claude-code/skills/ywc-spec-validate/SKILL.md        # 존재
grep -n "38" CLAUDE.md README.md README.ko.md README.ja.md README.es.md README.zh.md  # Claude count = 38
```

## Verification

- [ ] `bash scripts/validate.sh` 통과 (skill 구조 + README locale set + name==dirname)
- [ ] `npx --yes markdownlint-cli2 "claude-code/skills/*/README*.md" "README*.md"` 통과
- [ ] `git diff --check` 통과
- [ ] `codex/**` / `claude-code/agents/**` / `CHANGELOG.md` / `VERSION` 무변경 확인
