# develop-with-llm PR 132/133/134/140 Claude Code Port

> Status: Plan ready — direct execution, single branch
> Scale: Medium-breadth / single mechanical concern (see Scale note)
> Created: 2026-06-24
> Author: ywc-plan
> Spec Reference: `yongwoon/develop-with-llm` PR #132, #133, #134, #140
> Sibling plan: `develop-with-llm-pr132-133-134-140-codex-port.md` (Codex side — do not overlap)

## Goal

Port the **Claude Code** `ywc-*` skill changes from `develop-with-llm` PRs
#132/#133/#134/#140 into this toolkit's `claude-code/skills/` tree, in a **single
feature branch**, eliminating the drift between this distribution mirror and the
source repo. The Codex side is handled by the sibling plan and is out of scope here.

The four PRs deliver:

- **#132** — `ywc-plan`: opt-in `ywc-spec-ready` auto-converge prompt after Medium/Large spec handoff.
- **#133** — `ywc-handle-pr-reviews`: redefine "handling a PR" as leaving it **mergeable** (three independent gates — comments / CI / conflict), run CI + conflict gates on **every** invocation; plus executor rationalization-defense rows.
- **#134** — `ywc-create-pr` Author Self-Review Gate; `ywc-spec-validate --tasks` Cross-Artifact (Analyze) pass; plus context-compaction and AGENTS.md-reconcile improvements to `ywc-agentic`, `ywc-sequential-executor`, `ywc-onboard-repo`.
- **#140** — skill drift / hygiene fixes: `ywc-spec-validate` band-mapping, `ywc-spec-writer` model bump, `ywc-gen-testcase` URL hygiene + range source, `ywc-project-docs` language-selection contract, `ywc-project-scaffold` README sync, shared `project-docs-structure.md` wording.

## Why

This toolkit is the distribution mirror of the source repo's skills. PR-level
improvements made upstream (a reliability fix for #133, two new gates for #132/#134,
drift/hygiene corrections for #140) are absent here. Probes confirmed every target
change is missing locally **except** `ywc-project-scaffold`'s `SKILL.md` (already carries
Rust/Axum). A stale mirror ships outdated instruction contracts to every consumer who
installs from this toolkit.

## Scale note (why direct execution, not task-generator fan-out)

This spans ~10 skills / ~45 files, which by raw count reads Medium. But it is a **single
mechanical concern** (porting upstream skill drift) with **none** of the Small-path
hard-disqualifiers — no DB migration, no new library, no new API contract, no
cross-cutting *logic* change; these are instruction/documentation edits. Combined with
the requester's explicit **single-branch** directive (which overrides task-generator
fan-out into per-task PRs), the correct artifact is a direct execution plan organized as
a per-PR checklist. Phases are sequenced; the whole thing is one branch, one PR.

## Out of Scope

- **Codex mirror** (`codex/skills/**`, `plugins/ywc-agent-toolkit/**`) — handled by the
  sibling Codex-port plan. The pre-push hook only blocks a stale generated Codex package
  *on Codex changes*; touching no Codex file keeps it green.
- **`evals/` fixtures** — this toolkit has no eval harness or `evals/` directories. #140's
  `evals.json` additions and the `└── evals/` README structure lines are **not** ported
  (they would assert directories that do not exist here).
- **`develop-with-llm`-only content** — LLM study docs (`docs/studies/llm/*`),
  `prompts/LLM-CLI-command.md`, and `tasks/` artifacts from those PRs are repo-local to the
  source.
- **Pre-existing 500-line cap violation** in `ywc-parallel-executor/SKILL.md` (currently 501)
  — not introduced here; #133's edit must stay net-neutral. No reformat in this branch.
- **Root README / pipeline docs** — already synced in a prior branch.
- **`ywc-create-pr/evals/evals.json`** — pre-existing file, not introduced by any of these PRs.
  Leave untouched; do not reference it in any new README prose added in Phase 3.

## Done When

- All four PRs' Claude-Code-scoped changes are present in `claude-code/skills/**`, adapted
  for 6 README locales and the no-`evals/` reality.
- `bash scripts/validate.sh` passes (frontmatter + 4-locale set + `--list` dry run); the es/zh locale probe in the Verification commands block confirms the remaining two locales.
- `markdownlint` passes under the CI config (MD013/MD060 disabled).
- No `SKILL.md` exceeds 500 lines except the pre-existing `ywc-parallel-executor` (501, unchanged).
- A single PR is opened from one feature branch; `git diff main...HEAD` touches no `codex/` path.

## Existing Constraints Touched (verified 2026-06-24)

| Constraint | Evidence | Consequence for the port |
|---|---|---|
| Toolkit ships **6** README locales | target skills have `README.{md,en,es,ja,ko,zh}`; `validate.sh` enforces only 4 (md/en/ja/ko) — es/zh are **not** caught by CI | Every 4-locale upstream README hunk must also be applied to `README.es.md` + `README.zh.md`; verify via explicit `ls` probe, not `validate.sh` |
| No `evals/` dirs | `ls ywc-project-{docs,scaffold}/` has none | Drop `evals.json` + `└── evals/` README lines from #140 |
| `ywc-project-scaffold/SKILL.md` already has Rust/Axum | `SKILL.md:60`, `:88`; `references/rust.md` exists | Scaffold = README-only port; SKILL needs nothing |
| `ywc-spec-validate` touched by **#134 + #140** | #134: `--tasks`/Step 4c/rationalization; #140: band table + finding-count wording | Apply both — disjoint regions, two discrete edits |
| `ywc-sequential-executor` touched by **#133 + #134** | #133: rationalization row; #134: "Compaction on long ranges" paragraph | Apply both; file at 487 → keep additions tight, verify ≤500 |
| Toolkit "before" states match source "before" | handle-pr `### 1.`/`6.5`/`6.6`; create-pr `### 7. Create PR`; spec-validate `PROCEED (≥90) DONE` + `Critical/High/Medium/Low`; spec-writer `4-7`; `ywc-project-docs-ja/-kr` wording | Upstream `+` lines apply cleanly |
| Shared refs present | `references/{subagent-status-actions,pr-conflict-resolution}.md` | Compaction `§3.5` links resolve |

> **Path-convention note (verified — do not "fix" in this branch):** the toolkit's
> `ywc-handle-pr-reviews/SKILL.md:59` references `tools/claude-code/skills/...` (a
> pre-existing source-repo path) while `:177` already uses `claude-code/skills/...`. Apply
> only the **changed** (`+`) lines from each diff and leave unchanged context lines exactly
> as the toolkit currently has them. Reconciling the `tools/` prefix is a separate concern.

## Files to touch

Branch: `feature/port-dwl-skill-drift-20260624`

**#132 — `ywc-plan`:** `SKILL.md`, `README.{md,en,ja,ko,es,zh}`

**#133 — handle-pr + executors:** `ywc-handle-pr-reviews/{SKILL.md, README.{md,en,ja,ko,es,zh}}`,
`ywc-parallel-executor/SKILL.md` (net-neutral), `ywc-sequential-executor/SKILL.md` (rationalization row)

**#134 — create-pr / spec-validate / agentic / onboard / seq-exec:**
`ywc-create-pr/{SKILL.md, README×6}`, `ywc-spec-validate/{SKILL.md, README×6}`,
`ywc-agentic/SKILL.md`, `ywc-onboard-repo/{SKILL.md, README×6}` (**note:** `README.es.md`
and `README.zh.md` do not yet exist in this skill — they must be **created**, not edited),
`ywc-sequential-executor/SKILL.md` (compaction paragraph)

**#140 — drift / parity:** `ywc-spec-validate/SKILL.md` (band map),
`ywc-spec-writer/{SKILL.md, references/full-gen-workflow.md}`,
`ywc-gen-testcase/{SKILL.md, README×6}` (no reference-file edit — verified: the `legalforce/cas-marketing-on` URL lives only in `SKILL.md` + the 6 READMEs, **not** in `references/testsheet-template.md`; upstream #140's `references/examples.md` has no toolkit equivalent, so that hunk drops),
`ywc-project-docs/README×6` (minus evals), `ywc-project-scaffold/README×6` (minus evals),
`claude-code/skills/references/project-docs-structure.md`

## Implementation Steps

Apply in PR order. Run `bash scripts/validate.sh` after each phase. The toolkit's
"before" states match the source, so apply each diff's `+`/`-` hunks, then mirror every
README change into `.es.md` and `.zh.md` (upstream diffs only carry md/en/ja/ko).

### Phase 0 — Branch
- [ ] `git checkout main && git pull`
- [ ] `git checkout -b feature/port-dwl-skill-drift-20260624`

### Phase 1 — PR #132 (`ywc-plan`)
- [ ] `SKILL.md` Step 5 Medium/Large handoff → opt-in `ywc-spec-ready` y/n prompt block (replaces the old "Never proceed past the handoff" 3-step text).
- [ ] `SKILL.md` Validation line → opt-in `ywc-spec-ready` wording.
- [ ] `SKILL.md` Integration Medium/Large downstream line → `ywc-spec-ready (auto-converge shortcut) or ...`.
- [ ] README ×6: "Related Skills" — add `ywc-spec-ready` line + reword `ywc-spec-validate` to "manual next step".
- [ ] `bash scripts/validate.sh`

### Phase 2 — PR #133 (handle-pr-reviews + executors)
- [ ] `ywc-handle-pr-reviews/SKILL.md`: frontmatter `description` rewrite (mergeable framing + `fix PR CI` / `PR conflict 해결` triggers); Announce line; intro paragraph; +1 Rationalization row ("No unresolved comments — nothing to handle"); new `## Definition of Done` (3-gate table + mandatory TodoWrite); renumber `### 1.`→`### Step 1:` … through **Step 9**; Step 2 empty-array reroute (`[]` → still run Steps 7+8); `6.5`→**Step 7 CI Gate (EVERY invocation)**; `6.6`→**Step 8 Merge-Readiness Gate (EVERY invocation)**; `7. Final Summary`→**Step 9** (report all three gates). Fix internal cross-refs.
- [ ] handle-pr README ×6: intro mergeable/three-gates paragraph; Key Features bullet (en/ja) + 특징/실행 흐름 renumber (md/ko); es/zh equivalents.
- [ ] `ywc-parallel-executor/SKILL.md`: **net-neutral** — append the "clears CI + conflicts → leaves PR mergeable" clause to the existing `--draft` bot row (add **no** new line; file stays 501).
- [ ] `ywc-sequential-executor/SKILL.md`: +1 Rationalization row ("Bot comments addressed … clears only one of three blockers").
- [ ] `bash scripts/validate.sh`; confirm handle-pr Steps are contiguous 1–9 and DoD CI=Step7 / conflict=Step8.

### Phase 3 — PR #134 (create-pr / spec-validate / agentic / onboard / seq-exec)
- [ ] `ywc-create-pr/SKILL.md`: +1 Rationalization row ("I generated this code … just file the PR"); insert `### 6.5. Author Self-Review Gate (mandatory)` before `### 7. Create PR` (5-row check table + delegation note to `ywc-impl-review`).
- [ ] create-pr README ×6: Key Features self-review bullet; 실행 흐름 renumber (old 7 → 8; new 7 = Self-Review Gate); es/zh too.
- [ ] `ywc-spec-validate/SKILL.md`: +1 Rationalization row ("Spec passed and tasks generated … must agree"); add `--tasks` argument row; insert **Step 4c Cross-Artifact Consistency (Analyze)** (Requirement Coverage + Task Provenance tables); rewrite Integration "Not applicable" → "Cross-artifact (Analyze) … `--tasks <dir>`".
- [ ] spec-validate README ×6: `--tasks tasks/` usage example + Cross-Artifact note blockquote; es/zh too.
- [ ] `ywc-agentic/SKILL.md`: insert "Compaction on long runs (context engineering)" paragraph before `### Step 9: Completion Report`. (**SKILL.md only** — upstream #134 touches no agentic READMEs; `ywc-agentic` currently has only 4 locale files and that is not corrected in this branch.)
- [ ] `ywc-onboard-repo/SKILL.md`: +1 Rationalization row (AGENTS.md); Phase 1 "Agent-context pre-check" paragraph; Phase 4 (Output B) AGENTS.md-reconcile paragraph; +1 Validation line.
- [ ] onboard README ×6: Output B reconcile clause (AGENTS.md / .cursorrules). **`README.es.md` and `README.zh.md` do not exist yet — create them** (seed from `README.en.md` translated to es/zh respectively, then apply the reconcile clause).
- [ ] `ywc-sequential-executor/SKILL.md`: insert "Compaction on long ranges (context engineering)" paragraph. **Coordinate with Phase 2's seq-exec edit** (same file). **Line budget: current 487 lines, cap 500, headroom 13 lines. Rationalization row (Phase 2) ≤3 lines; this compaction paragraph ≤7 lines. Write to these caps before committing — do not rely on post-hoc tightening.** Verify `wc -l` ≤500.
- [ ] `bash scripts/validate.sh`

### Phase 4 — PR #140 (drift / parity)
- [ ] `ywc-spec-validate/SKILL.md`: split band-mapping table (`PROCEED ≥90, no Critical → DONE` / `PROCEED ≥90, Critical present → DONE_WITH_CONCERNS`); header note cites confidence-gate §5; `Critical/High/Medium/Low` → `Critical/Warning/Suggestion`. **Coordinate with Phase 3 spec-validate edits** (disjoint region).
- [ ] `ywc-spec-writer/SKILL.md`: `claude-opus-4-7` → `claude-opus-4-8` (body line + Model output-block line).
- [ ] `ywc-spec-writer/references/full-gen-workflow.md`: model priority `4-7 / 4-5` → `4-8 / 4-7`.
- [ ] `ywc-gen-testcase/SKILL.md`: Source report line add `range:<start>..<end>`; example URL `legalforce/cas-marketing-on` → `acme/web-app`.
- [ ] `ywc-gen-testcase` reference file: **no change** — verified `references/testsheet-template.md` contains zero `legalforce` occurrences (`grep -c legalforce … testsheet-template.md` = 0). Upstream #140 edited `references/examples.md`, which has no toolkit equivalent; the URL hygiene here is fully covered by the `SKILL.md` + README ×6 steps above. Recorded as "no change needed", not a missing step.
- [ ] gen-testcase README ×6: example URLs → `acme/web-app`.
- [ ] `ywc-project-docs` README ×6: language-selection contract ("never auto-detect; `--lang kr|ja` or ask"), invocation `/project-docs` → `/ywc-project-docs --lang …`, install-path `project-docs/` → `ywc-project-docs/`. **Omit the `└── evals/` line.** (Aligns READMEs to existing SKILL.md behavior; SKILL.md unchanged.)
- [ ] `ywc-project-scaffold` README ×6: invocation `/project-scaffold` → `/ywc-project-scaffold`; language/framework table add Rust / Actix Web / Axum; file-structure add `rust.md` + locale README rows. **Omit the `evals/` line.** Verify SKILL needs nothing (it already has Rust/Axum).
- [ ] `claude-code/skills/references/project-docs-structure.md`: replace stale `ywc-project-docs-ja`/`-kr` wording with the unified single-skill `ywc-project-docs` sentence. (Three copies exist in the repo; edit only this one — not `codex/skills/references/` or `plugins/ywc-agent-toolkit/skills/references/`.)
- [ ] `bash scripts/validate.sh`

### Phase 5 — Verify & deliver
- [ ] Full verification (below).
- [ ] Commit (per-phase or one cohesive commit) and open a single draft PR.

## Verification commands

```bash
bash scripts/validate.sh                       # frontmatter + 4-locale set (md/en/ja/ko) + --list dry run
# NOTE: validate.sh enforces only 4 locales — es/zh are NOT checked by CI

# SKILL.md line-cap audit (≤500, except pre-existing ywc-parallel-executor=501)
for s in ywc-handle-pr-reviews ywc-create-pr ywc-spec-validate ywc-onboard-repo \
         ywc-agentic ywc-sequential-executor ywc-parallel-executor ywc-plan \
         ywc-spec-writer ywc-gen-testcase; do
  printf '%-26s %s\n' "$s" "$(wc -l < claude-code/skills/$s/SKILL.md)"
done

# Drift-closed probes (each should now be > 0)
grep -c "ywc-spec-ready"          claude-code/skills/ywc-plan/SKILL.md
grep -c "Definition of Done"      claude-code/skills/ywc-handle-pr-reviews/SKILL.md
grep -c "Author Self-Review Gate" claude-code/skills/ywc-create-pr/SKILL.md
grep -c "Cross-Artifact"          claude-code/skills/ywc-spec-validate/SKILL.md
grep -c "Compaction on long"      claude-code/skills/ywc-agentic/SKILL.md \
                                  claude-code/skills/ywc-sequential-executor/SKILL.md

# es/zh locale presence for all skills whose READMEs are touched in this branch
# (ywc-agentic READMEs are not touched — excluded; validate.sh does NOT check es/zh)
for s in ywc-plan ywc-handle-pr-reviews ywc-create-pr ywc-spec-validate ywc-onboard-repo \
         ywc-gen-testcase ywc-project-docs ywc-project-scaffold; do
  for loc in es zh; do
    f="claude-code/skills/$s/README.$loc.md"
    [ -f "$f" ] && echo "OK  $f" || echo "MISSING $f"
  done
done

# No evals/ leaked into any touched skill README
# (ywc-create-pr/evals/evals.json is pre-existing and untouched — that directory is fine)
! grep -rn "evals/" \
    claude-code/skills/ywc-project-docs \
    claude-code/skills/ywc-project-scaffold \
    claude-code/skills/ywc-create-pr/README*.md \
    claude-code/skills/ywc-spec-validate \
    claude-code/skills/ywc-onboard-repo

# No legalforce URL remains; Codex untouched
! grep -rn "legalforce/cas-marketing-on" claude-code/skills/ywc-gen-testcase
git diff --name-only main...HEAD | grep -q "^codex/" && echo "ERROR: codex touched" || echo "codex clean"

# markdownlint — mirrors CI; must pass before opening PR
npx markdownlint-cli2 \
  --config <(printf '{"MD013":false,"MD031":false,"MD033":false,"MD037":false,"MD040":false,"MD041":false,"MD060":false}') \
  "claude-code/skills/*/README*.md"
```

## Risks / Rollback

| Risk | Mitigation |
|---|---|
| es/zh forgotten on a README edit | `scripts/validate.sh` enforces only 4 locales (md/en/ja/ko) — es/zh are **not** CI-gated; verify the 6-locale set manually with `ls claude-code/skills/<skill>/README*.md` for every edited skill |
| `ywc-sequential-executor` > 500 after #133 + #134 additions | Keep both terse; line-cap audit; tighten wording if over (do not split file this branch) |
| `ywc-parallel-executor` edit adds a line (→ 502) | Edit strictly net-neutral (append to existing row); verify `wc -l` stays 501 |
| spec-validate double-edit (#134 + #140) conflict | Regions disjoint (Step 4c/args vs band table); two discrete edits, re-read between |
| Copying an `evals/` reference that doesn't exist here | Out-of-scope rule + `! grep evals/` probe |
| markdownlint anchor/line-length breakage from new prose | Run markdownlint with the repo config before PR; source PRs all passed 0-error |
| Rollback | All changes isolated to `claude-code/skills/**` on one branch; `git checkout main` / delete branch reverts cleanly; no hooks fire on Claude-only changes |
