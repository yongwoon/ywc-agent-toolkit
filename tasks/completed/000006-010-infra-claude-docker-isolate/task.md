# Task: 000006-010-infra-claude-docker-isolate

## Prerequisites

- [ ] `main` baseline 최신화 (`git -C . pull`)
- [ ] upstream source 접근 가능 (`gh pr diff 110 --repo yongwoon/develop-with-llm`)
- [ ] `docs/ywc-plans/port-upstream-skill-prs-110-120-129.md` Workstream A·D 숙지

## Allowed Edit Scope

- `claude-code/skills/ywc-docker-isolate/**` (신규)
- `claude-code/skills/ywc-parallel-executor/SKILL.md` (Docker hook 라인만)
- `claude-code/skills/CLAUDE.md` (script catalog table)
- `README.md` (Task & Execution catalog row + Claude count)
- `README.ko.md` / `README.ja.md` / `README.es.md` / `README.zh.md` / `CLAUDE.md` (Claude count 숫자만)
- `.claude/skills/ywc-toolkit-eval/evals/**` (baseline)

다른 skill, `codex/**`, `claude-code/agents/**`, `CHANGELOG.md`, `VERSION`은 수정 금지.

## Stop Conditions

- port 후 `grep -rn "tools/claude-code"`가 docker-isolate / parallel-executor에서 0이 아니면 멈추고 보고
- `bash scripts/validate.sh` 실패 시 멈추고 원인 보고
- count surface가 6개 file에서 일관되게 잡히지 않으면(예: 어떤 locale이 다른 값) 멈추고 보고

## Implementation Steps

- [ ] `gh pr diff 110 --repo yongwoon/develop-with-llm`로 upstream `tools/claude-code/skills/ywc-docker-isolate/` 12개 file 내용 확보
- [ ] `claude-code/skills/ywc-docker-isolate/` 생성 후 12개 file 작성: `SKILL.md`, `README.md`/`.en`/`.ja`/`.ko`, `references/port-allocation.md`/`preconditions.md`, `scripts/_lib.sh`/`setup-docker-ports.sh`/`teardown-docker.sh`/`audit-docker-stacks.sh`
- [ ] `SKILL.md` frontmatter `name:`가 `ywc-docker-isolate`(디렉터리명)와 일치하는지 확인
- [ ] port한 모든 file에서 runtime path `tools/claude-code/skills/` → `claude-code/skills/`로 rewrite
- [ ] `chmod +x claude-code/skills/ywc-docker-isolate/scripts/*.sh`
- [ ] `claude-code/skills/ywc-parallel-executor/SKILL.md`에 PR #110의 3개 hunk(Pre-flight audit hook, Step 4a-isolate setup hook, Step 4g teardown hook) 추가하며 hook 명령의 path를 `bash claude-code/skills/ywc-docker-isolate/scripts/...`로 작성
- [ ] root `README.md` **Task & Execution** table(`ywc-worktrees` 행 뒤, `~:201`)에 `ywc-docker-isolate` row 추가
- [ ] `claude-code/skills/CLAUDE.md` Script catalog table(`:213`)에 docker-isolate script 3 rows 추가 (setup/teardown/audit, exit code 포함)
- [ ] skill count `36 → 37`로 변경: `CLAUDE.md:7`, `README.md:11`, `README.ko.md:12`, `README.ja.md:12`, `README.es.md:11`, `README.zh.md:12` — Claude Code skill 숫자만
- [ ] `.claude/skills/ywc-toolkit-eval/`에 `ywc-docker-isolate` baseline entry 등록(eval skill 절차 따름)

## Task Verify

```bash
bash scripts/validate.sh
grep -rn "tools/claude-code" claude-code/skills/ywc-docker-isolate claude-code/skills/ywc-parallel-executor   # 0
bash -n claude-code/skills/ywc-docker-isolate/scripts/*.sh
grep -c "ywc-docker-isolate" README.md                              # >= 1
grep -c "ywc-docker-isolate/scripts" claude-code/skills/CLAUDE.md   # = 3
grep -n "37" CLAUDE.md README.md README.ko.md README.ja.md README.es.md README.zh.md  # Claude count = 37
```

## Verification

- [ ] `bash scripts/validate.sh` 통과 (skill 구조 + README locale set + name==dirname)
- [ ] `bash -n` 4개 script 통과
- [ ] `npx --yes markdownlint-cli2 "claude-code/skills/*/README*.md" "README*.md"` 통과
- [ ] `git diff --check` 통과
- [ ] `codex/**` / `claude-code/agents/**` / `CHANGELOG.md` / `VERSION` 무변경 확인
