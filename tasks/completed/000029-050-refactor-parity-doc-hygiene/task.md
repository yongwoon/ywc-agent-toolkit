# Task: 000029-050-refactor-parity-doc-hygiene

## Prerequisites

- [ ] batch 단일 branch에서 작업 중인지 확인
- [ ] upstream 참조: `gh pr diff 140 --repo yongwoon/develop-with-llm` (claude-code 경로만)
- [ ] 사실 확인: `rg -c legalforce claude-code/skills/ywc-gen-testcase/references/testsheet-template.md` = 0 (reference 무변경 근거), `rg -n "Rust|Axum" claude-code/skills/ywc-project-scaffold/SKILL.md` >0 (SKILL 무변경 근거)

## Allowed Edit Scope

- `claude-code/skills/ywc-gen-testcase/{SKILL.md, README.*.md}` (`references/testsheet-template.md` 무변경)
- `claude-code/skills/ywc-project-docs/README.*.md`
- `claude-code/skills/ywc-project-scaffold/README.*.md`
- `claude-code/skills/references/project-docs-structure.md` (claude-code 사본만)
- 그 외 경로 편집 금지(특히 `codex/**`, `plugins/**`, `evals/`).

## Stop Conditions

- README 파일구조 트리에 `evals/`를 추가하려는 충동 발생 시 중단(toolkit에 부재).
- `references/testsheet-template.md`에 legalforce URL이 발견되면(예상 0건과 불일치) 중단·재평가.
- project-docs/scaffold의 SKILL.md를 변경하려는 충동 발생 시 중단(README-only).

## Implementation Steps

- [ ] `ywc-gen-testcase/SKILL.md`: Source 보고 줄 `Source: <pr#N | task:<name> | diff>`→`… | range:<start>..<end> | diff>`; 예시 URL `legalforce/cas-marketing-on`→`acme/web-app`.
- [ ] `ywc-gen-testcase/README.{md,en,es,ja,ko,zh}.md`: 예시 URL→`acme/web-app`.
- [ ] `ywc-project-docs/README.{md,en,es,ja,ko,zh}.md`: 언어 선택 계약 정정(자동 추정 금지; `--lang kr|ja` 우선, 없으면 질문), 호출명 `/project-docs`→`/ywc-project-docs`(+`--lang` 예시), 설치 경로 `project-docs/`→`ywc-project-docs/`. 파일구조 트리에 `└── evals/` **추가 금지**.
- [ ] `ywc-project-scaffold/README.{md,en,es,ja,ko,zh}.md`: 호출명 `/project-scaffold`→`/ywc-project-scaffold`(다중 예시 포함), language 표에 Rust, framework 표에 Actix Web/Axum 추가, 파일구조에 `rust.md` + locale README 행. `evals/` 행 **추가 금지**.
- [ ] `claude-code/skills/references/project-docs-structure.md`: stale `ywc-project-docs-ja`/`-kr` 문장을 "Used by `ywc-project-docs` (single skill) …" 단일 문장으로 교체.

## Task Verify

- [ ] `! rg -n "legalforce/cas-marketing-on" claude-code/skills/ywc-gen-testcase` (잔존 0)
- [ ] `rg -n "acme/web-app" claude-code/skills/ywc-gen-testcase/SKILL.md` (>0)
- [ ] `rg -n -- "range:" claude-code/skills/ywc-gen-testcase/SKILL.md` (Source 줄)
- [ ] `rg -n "ywc-project-docs" claude-code/skills/ywc-project-docs/README.md` 및 `! rg -n "/project-docs\b" claude-code/skills/ywc-project-docs/README.md`
- [ ] `rg -n "Axum|Actix" claude-code/skills/ywc-project-scaffold/README.md` (>0)
- [ ] `! rg -rn "evals/" claude-code/skills/ywc-project-docs claude-code/skills/ywc-project-scaffold`
- [ ] `! rg -n "ywc-project-docs-ja|ywc-project-docs-kr" claude-code/skills/references/project-docs-structure.md`
- [ ] `git diff --stat claude-code/skills/ywc-gen-testcase/references/testsheet-template.md` → 변경 없음(빈 결과)

## Verification

- [ ] `bash scripts/validate.sh`
- [ ] `npx markdownlint-cli2 --config /tmp/ml.json "claude-code/skills/ywc-gen-testcase/README*.md" "claude-code/skills/ywc-project-docs/README*.md" "claude-code/skills/ywc-project-scaffold/README*.md"` (0 errors)
- [ ] `git diff --name-only` 결과가 Allowed Edit Scope 내부로 한정(특히 `codex/`·`plugins/` 미포함)
