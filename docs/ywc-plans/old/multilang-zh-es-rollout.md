# Spec: Roll out zh / es output support to sibling multi-language skills (claude-code only)

> Scale: **Medium** · Path: `ywc-spec-validate` → `ywc-task-generator`
> Prior art (template): `ywc-project-docs` — claude-code commit `8f7458c`, PR #118.
> **Implementation target: `claude-code/skills/` only.** The codex bundle and the `plugins/` mirror are explicitly out of scope for this rollout.

## Purpose

`ywc-project-docs` now generates its deliverable in five languages (KR / JA / EN / **ZH** / **ES**). The sibling **content-output** skills in the claude-code bundle still stop at three (KR/JA/EN). This spec propagates the same **Simplified Chinese (`zh`)** and **Spanish (`es`)** output support to those siblings so every artifact-generating claude-code skill offers one consistent language set.

## Why

- Consistency: a user who can request Chinese/Spanish project docs reasonably expects the same for specs, tasks, and testsheets.
- The pattern is proven and low-risk — `ywc-project-docs` PR #118 established the exact edit shape and CI gates to replicate.

## Scope

Target skills (content-output only), **`claude-code/skills/` bundle only**:

| Skill | Current `--lang` set | Add | Policy file |
|---|---|---|---|
| `ywc-spec-writer` | `ko \| ja \| en` (default `ko`) | `zh`, `es` | `references/language-policy.md` (extend) |
| `ywc-task-generator` | `korean \| japanese \| english` (default `english`) | `chinese`, `spanish` | `references/language-policy.md` (extend) |
| `ywc-gen-testcase` | `ja \| ko \| en` (default auto-detect) | `zh`, `es` | none — rules inline in SKILL.md |

Per-skill change set (all under `claude-code/skills/<skill>/`):

1. **SKILL.md** — extend the `--lang` argument table, the language-inference/selection prose, and any inline language enumeration to include `zh` + `es`. Broaden the frontmatter `description` "Supports … output" clause and add `zh`/`es` trigger phrases. Bump the `version:` field (minor).
2. **`references/language-policy.md`** (spec-writer, task-generator only) — add a **Chinese (Simplified)** section and a **Spanish** section following the existing per-language shape (register + technical-term table + user-story format). Canonical content is in [Appendix A](#appendix-a-canonical-zh--es-policy-content).
3. **`ywc-gen-testcase`** — no policy file; add `zh`/`es` to the `--lang` arg table and the detection-fallback list inline in SKILL.md. The existing "YAML keys/section numbers stay English, only prose follows `--lang`" invariant already covers zh/es.
4. **README locale set** (`README.md` + `.en`/`.ja`/`.ko`/`.zh`/`.es`) — update the "supported output languages" wording that currently reads "KR/JA/EN".

## Out of Scope

- **codex bundle (`codex/skills/`) and the `plugins/ywc-agent-toolkit/` mirror** — this rollout is claude-code only. No codex SKILL.md, `agents/openai.yaml`, `evals/evals.json`, or plugin-package edits; do not run `scripts/sync-codex-plugin.sh`. (A later PR may mirror these changes into codex deliberately.)
- **Category B skills** (`ywc-create-pr`, `ywc-finish-branch`, `ywc-agentic`, `ywc-spec-ready`): PR-title / report-text language selection. Deferrable follow-up.
- **`ywc-project-docs`**: already done (PR #118) — no further change.
- **Language-code unification**: `ywc-project-docs` uses `kr` for Korean while spec-writer/gen-testcase use `ko`. Do **not** unify codes here — add `zh`/`es` in each skill's *existing* code convention (`chinese`/`spanish` for task-generator's word-style flags). Code harmonization is a separate refactor.
- **Traditional Chinese (`zh-Hant`)**: only Simplified `zh`, matching `ywc-project-docs`.
- **README prose re-translation**: update the language-support wording in each locale README; do not re-translate unrelated README prose.
- **Default-language behavior**: each skill keeps its current default (`ko` / `english` / auto-detect). `zh`/`es` are opt-in via `--lang`, never a new default.

## Acceptance Criteria

- **AC1** — For each target skill, invoking it with `--lang zh` produces the deliverable with prose in Simplified Chinese and technical terms kept in English; `--lang es` produces Spanish prose with English technical terms. Observable: run the skill with each flag and inspect that body prose is in the requested language while `API`/`Backend`/`Database` remain English.
- **AC2** — `ywc-spec-writer` and `ywc-task-generator` `references/language-policy.md` each contain a Chinese (Simplified) and a Spanish section following the existing per-language structure (register + term table + user-story format).
- **AC3** — Each target skill's frontmatter `description` names Chinese and Spanish in its "supports … output" wording and includes at least one `zh` and one `es` trigger phrase.
- **AC4** — Each target skill's full README locale set states the updated language set (KR/JA/EN/ZH/ES) wherever it previously said KR/JA/EN.
- **AC5** — `bash scripts/validate.sh` returns `All checks passed.` and the markdownlint CI command (README globs) returns 0 errors after all edits. No file under `codex/skills/` or `plugins/` is modified (verify with `git status`).
- **AC6** — No change to any skill's default output language; `zh`/`es` remain opt-in.

## Functional Requirements

- **FR1** (→ AC1, AC2) — Extend each `--lang` acceptance set to include `zh`/`es` (or `chinese`/`spanish` for task-generator), and add the corresponding policy content so the skill knows the register and term rules for each new language.
- **FR2** (→ AC1) — For `ywc-gen-testcase`, add `zh`/`es` to the `--lang` arg table and detection fallback inline; confirm the "prose-only follows `--lang`" invariant already scopes zh/es correctly (no template-skeleton translation).
- **FR3** (→ AC3) — Update frontmatter descriptions and triggers per skill.
- **FR4** (→ AC4) — Update README language-support wording across all six locale files per skill.
- **FR5** (→ AC5) — Run local CI (`validate.sh` + markdownlint) and fix any failures before handoff to review; confirm the working tree touches only `claude-code/`.

## Non-Functional Requirements

- **Idempotent doc edits only** — no code, no DB, no new dependency, no API contract. (Confirms Medium, not Large-by-risk.)
- **claude-code-only footprint** — the diff must stay entirely within `claude-code/skills/`. Because no `codex/skills/` file is staged, the `.githooks/pre-commit` codex-sync path never fires and `plugins/` stays untouched.
- **Version bump** — bump the claude-code SKILL `version:` field for each changed skill (minor, feature addition), matching the `ywc-project-docs` 2.2.0 → 2.3.0 precedent.

## Existing Constraints Touched

- `claude-code/skills/ywc-spec-writer/references/language-policy.md:1-58` — KR/JA/EN sections; each has **Formality/Register + technical-term table + user-story format**. New zh/es sections must match this exact three-part shape.
- `claude-code/skills/ywc-task-generator/references/language-policy.md:1-45` — same three-part shape; task-generator `--lang` values are **words** (`korean|japanese|english`), so add `chinese`/`spanish`, not codes.
- `claude-code/skills/ywc-gen-testcase/SKILL.md:57,276-283` — `--lang` arg table (`ja,ko,en`), detection order (CLAUDE.md → recent testsheets → README → English fallback), and the invariant "YAML keys, section numbers, template skeleton stay English regardless of `--lang`; only prose follows." No policy file exists — do not create one unless the skill's inline rules prove insufficient.
- `claude-code/skills/ywc-project-docs/SKILL.md` (template reference) — the shape of a completed 5-language skill: `--lang kr|ja|en|zh|es` table, per-language Language Policy blocks, per-language Document Structure Template. Use as the visual template, **but keep each target skill's own code convention** (`ko` not `kr`).
- `.github/workflows/markdownlint.yml` — lints `claude-code/skills/*/README*.md` with `MD013/MD031/MD033/MD037/MD040/MD041/MD060` disabled. README edits must pass this exact config.

## Edge Cases

- **Task-generator word-flags vs codes** — `--lang chinese` / `--lang spanish` must be accepted (not `zh`/`es`) to match its existing word-style convention; the inference-from-CLAUDE.md path must not misclassify.
- **gen-testcase auto-detect** — a project whose CLAUDE.md declares Chinese/Spanish docs should now resolve to `zh`/`es`; verify the detection fallback list includes them so auto mode can pick them.
- **README anchor integrity** — if any locale README uses in-page anchors that include language names, keep anchors valid (the `ywc-project-docs` Spanish-anchor accent fix is the precedent).
- **codex drift acknowledged** — after this PR, the claude-code and codex copies of these three skills diverge (codex still KR/JA/EN). This is accepted and recorded here so a future codex-mirror PR is a deliberate, known follow-up rather than an accidental inconsistency.

## Open Questions

- **Scope confirmation** — proceeding on "content-output skills only" + "Simplified `zh`" + "claude-code bundle only" (per user direction). If Category B (PR/report language), Traditional Chinese, or the codex mirror is later wanted, extend this spec with an `## Iteration 2 Amendments` section rather than a rewrite.

## Suggested Task Breakdown (for `ywc-task-generator`)

Natural decomposition — one task per skill, each confined to `claude-code/skills/<skill>/`:

1. **T1 — `ywc-spec-writer` zh/es** — SKILL.md (`--lang`, description, triggers, version bump) + `references/language-policy.md` (add zh/es sections) + README×6.
2. **T2 — `ywc-task-generator` zh/es** — same shape; note word-style flags (`chinese`/`spanish`).
3. **T3 — `ywc-gen-testcase` zh/es** — SKILL.md inline (`--lang` table + detection fallback + version bump) + README×6 (no policy file).
4. **T4 — Verification** — `scripts/validate.sh` + markdownlint across all changed READMEs; `git status` confirms no `codex/` or `plugins/` file changed; fix-loop until green. (May fold into each task's own verification.)

Tasks T1–T3 are mutually independent and parallelizable; each is self-contained per `ywc-project-docs` precedent.

---

## Appendix A: Canonical zh / es policy content

Drop-in sections for `ywc-spec-writer` / `ywc-task-generator` `references/language-policy.md`, matching the existing KR/JA/EN three-part shape.

```markdown
## Chinese (Simplified) (`zh`)

**Register**: 书面语 (formal written register) — appropriate for technical documentation.

**Technical terms**: Keep in English. Do not translate core terms into Chinese.

| Correct | Incorrect |
|---------|-----------|
| Database 连接配置 | 数据库连接配置 |
| API Endpoint 说明 | 接口端点说明 |
| User Flow | 用户流程 |
| Backend Service | 后端服务 |

**User story format**:
> "作为[用户类型]，我希望[操作]，以便[目的]。"
```

```markdown
## Spanish (`es`)

**Register**: Plain business Spanish, formal *usted* register.

**Technical terms**: Keep in English. Do not translate core terms into Spanish.

| Correct | Incorrect |
|---------|-----------|
| Configuración de Database | Configuración de base de datos |
| Descripción de API Endpoint | Descripción de punto final |
| User Flow | Flujo de usuario |
| Backend Service | Servicio de backend |

**User story format**:
> "Como [tipo de usuario], quiero [acción] para [beneficio]."
```

For `ywc-task-generator`, use the same two blocks but keep its word-style flag names in the SKILL.md arg table (`chinese` / `spanish`); the policy-file section headings can stay code-tagged (`zh` / `es`) for parallelism with spec-writer.
