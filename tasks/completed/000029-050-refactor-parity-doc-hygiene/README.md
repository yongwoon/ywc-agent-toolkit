# 000029-050-refactor-parity-doc-hygiene

## Purpose

develop-with-llm PR #140 의 drift/hygiene 변경을 claude-code 트리에 port한다. `ywc-gen-testcase`(예시 URL hygiene + range source), `ywc-project-docs`(언어 선택 계약), `ywc-project-scaffold`(호출명 rename + stack 표 sync), 공유 `references/project-docs-structure.md`(단일 skill 문구 정정).

## Scope

- `ywc-gen-testcase/SKILL.md`: Source 보고 줄에 `range:<start>..<end>` 추가 + 예시 URL `legalforce/cas-marketing-on`→`acme/web-app`.
- `ywc-gen-testcase/README` 6 locale: 예시 URL→`acme/web-app`.
- `ywc-project-docs/README` 6 locale: 언어 자동 추정 금지(`--lang kr|ja` 우선, 없으면 질문), 호출명 `/project-docs`→`/ywc-project-docs --lang …`, 설치 경로 `project-docs/`→`ywc-project-docs/`. **`└── evals/` 줄은 제외**(toolkit에 evals 없음). 이 변경은 README를 기존 SKILL.md 동작에 맞추는 정정으로 SKILL.md는 미변경.
- `ywc-project-scaffold/README` 6 locale: 호출명 `/project-scaffold`→`/ywc-project-scaffold`, language/framework 표에 Rust / Actix Web / Axum 추가, 파일구조에 `rust.md` + locale README 행. **`evals/` 줄 제외**. SKILL.md는 이미 Rust/Axum 보유 → 미변경.
- `claude-code/skills/references/project-docs-structure.md`: stale `ywc-project-docs-ja`/`-kr` 문구를 단일 `ywc-project-docs` 문장으로 교체.

## Spec Reference

**Primary Sources**

- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-claude-code-port.md` (Phase 4 #140 — gen-testcase, project-docs, project-scaffold, project-docs-structure)
- 대응 upstream PR: `yongwoon/develop-with-llm` #140

**Summary**

#140의 hygiene 묶음을 claude-code에 적용한다. upstream과의 핵심 차이: (1) toolkit에 `evals/` 없음 → eval 추가·`evals/` README 줄 제외; (2) `ywc-gen-testcase`의 `legalforce` URL은 SKILL.md + 6 README에만 존재하고 `references/testsheet-template.md`에는 없음(reference 파일 미변경); (3) `ywc-project-scaffold/SKILL.md`는 이미 Rust/Axum 보유(README-only).

**Out of Scope (from spec)**

- `evals.json` 추가(toolkit에 eval harness 없음).
- `ywc-gen-testcase` reference 파일 변경(`testsheet-template.md`에 legalforce URL 없음 — 변경 불필요, "no change needed").
- `ywc-project-scaffold/SKILL.md` 변경(이미 Rust/Axum).
- `codex/skills/references/` 및 `plugins/` 사본(다른 경로의 3 copy 중 claude-code 것만 편집).

## Criticality

`normal` — instruction/doc 편집만 수행.

## Dependencies

**Depends On**: (없음 — root)

**Depended By**: (없음)

## Key Files

- `claude-code/skills/ywc-gen-testcase/SKILL.md`
- `claude-code/skills/ywc-gen-testcase/README.{md,en,es,ja,ko,zh}.md`
- `claude-code/skills/ywc-project-docs/README.{md,en,es,ja,ko,zh}.md`
- `claude-code/skills/ywc-project-scaffold/README.{md,en,es,ja,ko,zh}.md`
- `claude-code/skills/references/project-docs-structure.md`

## Notes

- **evals 제외**: project-docs/scaffold README의 파일구조 트리에 `└── evals/`를 추가하지 말 것(toolkit에 부재 — 허위 디렉터리 주장 방지).
- **gen-testcase reference 무변경**: `references/testsheet-template.md`에는 `legalforce` URL이 0건이므로 변경 대상 아님(upstream의 `references/examples.md` hunk는 toolkit 대응 파일 없음).
- **3-copy 주의**: `project-docs-structure.md`는 repo에 3곳 존재 — `claude-code/skills/references/`만 편집, `codex/skills/references/`·`plugins/ywc-agent-toolkit/skills/references/`는 미접촉.
- gen-testcase/project-docs/project-scaffold 모두 es/zh 존재 → 편집(생성 아님).

## Out of Scope

- spec/executor/agentic/onboard 계열 skill.
- 호출명 외 SKILL.md 동작 변경.

## Parallel Execution Metadata

**Ownership**

- `claude-code/skills/ywc-gen-testcase/**` (단, `references/testsheet-template.md`는 무변경)
- `claude-code/skills/ywc-project-docs/README.*.md`
- `claude-code/skills/ywc-project-scaffold/README.*.md`
- `claude-code/skills/references/project-docs-structure.md` (claude-code 사본 1개만)

**Shared Surfaces**: `bash scripts/validate.sh` + markdownlint CI 게이트. `references/project-docs-structure.md`는 같은 이름의 codex/plugins 사본과 의미상 형제이나 경로가 달라 파일 충돌은 없음(claude-code 것만 편집).

**Conflicts With**: (None identified)

**Parallelizable After**: 즉시(root).

**Task Verify**

- `! rg -n "legalforce/cas-marketing-on" claude-code/skills/ywc-gen-testcase` (잔존 0)
- `rg -n "acme/web-app" claude-code/skills/ywc-gen-testcase/SKILL.md`
- `rg -n -- "range:<start>" claude-code/skills/ywc-gen-testcase/SKILL.md`
- `rg -n "ywc-project-docs --lang|never auto-detect|자동 추정" claude-code/skills/ywc-project-docs/README.md`
- `rg -n "Axum|Actix" claude-code/skills/ywc-project-scaffold/README.md`
- `! rg -rn "evals/" claude-code/skills/ywc-project-docs claude-code/skills/ywc-project-scaffold` (evals 누출 없음)
- `! rg -n "ywc-project-docs-ja|ywc-project-docs-kr" claude-code/skills/references/project-docs-structure.md`
