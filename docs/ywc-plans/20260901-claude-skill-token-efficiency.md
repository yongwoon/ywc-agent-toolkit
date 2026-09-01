# Spec: Claude Code ywc-* Skill Token Efficiency (L1 Lazy Reference Loading + L2 Deterministic Resolution Scripts)

> Status: Draft — pending `/ywc-spec-validate`
> Scale: Medium
> Created: 2026-09-01
> Confidence Gate: 87/100 — REVIEW (Scope 90 / Architecture 85 / Evidence 90 / Reuse 90 / Root cause 80)

## Purpose

Reduce the token cost of activating and running `claude-code/skills/ywc-*` skills **without changing any
observable behavior**. Two root causes are addressed:

1. **Eager reference loading.** `claude-code/skills/CLAUDE.md` currently *mandates* the
   `> **Action required**: Read [references/X.md]` directive form for four shared references, and skill
   bodies place those directives at the top of a step rather than at the branch that actually needs them.
   A single `ywc-sequential-executor` invocation therefore pays **16,590 tokens of body + ~6,600 tokens of
   eagerly-read references ≈ 23,000 tokens before the first task begins** — much of it for branches
   (`--non-interactive`, `--aggregate-pr`, external-URL prompts) that the run never enters.
2. **Determinism encoded as prose.** `references/language-resolution.md` is 121 lines read by
   **6 skills** whose entire yield is one of `ko | ja | en | es | zh`.
   `references/initials-resolution.md` is 190 lines yielding one `^[a-z0-9]{2,4}$` string.
   The repository already has the correct pattern for this (`CLAUDE.md` §"Bundled Execution Scripts":
   *"Scripts execute without loading their body into LLM context — use them instead of inlining equivalent
   logic in SKILL.md bodies"*), but these two resolutions never adopted it.

Measured session totals for context: 48 skill `description` fields = 28,106 chars ≈ **7,026 tokens loaded
in every session**; all 48 `SKILL.md` bodies = ≈231,667 tokens; all references = ≈172,630 tokens.

## Scope

- **L1 — Lazy reference loading.** Convert the 24 `**Action required**` directives across 12 skills from
  unconditional-at-step-entry to explicitly condition-gated, and relocate each to the branch that consumes it.
- **L2 — Deterministic resolution scripts.** Add one bundled script that performs output-language resolution
  and one that performs task-initials resolution, printing the resolved value. Skill bodies invoke the script
  and keep a ≤3-line inline pointer instead of reading the full reference.
- **Policy amendment.** Amend `claude-code/skills/CLAUDE.md` so the reference-loading convention it mandates
  is the lazy/scripted one, otherwise the next authored skill reintroduces the pattern.
- **Verification.** Before/after comparison via `ywc-toolkit-eval` to prove identical outputs plus a measured
  token reduction.

## Out of Scope

- **L3 — Body deduplication in `ywc-sequential-executor` / `ywc-parallel-executor` / `ywc-plan`.** Deferred by
  user decision: highest payoff but carries real behavior-drift risk when Rationalization Defense wording is
  condensed.
- **L4 — A15 description trimming.** 16 of 48 skills exceed the documented 80-word cap (max 95,
  `ywc-project-docs`), but total recoverable is only ~400 tokens and trimming trigger phrases degrades
  activation quality. `validate-skill.sh` keeps A15 advisory pending its own evidence gate.
- **`codex/` skills.** Maintained independently per `CLAUDE.md` §"Codex-skill: Maintained Independently".
  The sibling plan `docs/ywc-plans/20260901-small_codex-skill-creator-token-efficiency.md` covers the Codex
  side and explicitly excludes `claude-code/`; this spec is its mirror-image and must not touch `codex/`.
- **Deleting `references/principles.md`.** Initially suspected orphaned; verified NOT orphaned — it is linked
  by `readable-code.md:5`, `question-first-gate.md:74`, and `tdd-deep-module-gray-box.md:5`.
- Any change to skill workflow logic, step ordering, gates, or status vocabulary.

## Global Constraints

Copied verbatim from `claude-code/skills/CLAUDE.md` and `ywc-skill-author/SKILL.md`:

- "`README.md` — written in Korean; `README.[LOCALE].md` — written in the corresponding locale language;
  All other files — written in English"
- A8: "SKILL.md body MUST be ≤500 lines; longer sections MUST be extracted to `references/<topic>.md` with a
  brief inline pointer"
- A9: "Cross-references to sibling ywc-* skills MUST use the skill name only. Never use `@` syntax"
- A15: "`description` SHOULD be ≤80 words … Enforcement mode … is advisory (warn, do not fail the build)"
- "All paths are relative to the repository root. When authoring a new `ywc-*` skill that needs deterministic
  parsing or a bounded wait loop, add a script to `<skill>/scripts/` and reference it with a one-line Bash
  invocation in the SKILL.md body rather than describing the logic inline."
- "No-block invariant: absence of any `## Language Policy` never blocks, delays, or errors a consuming
  skill — resolution falls through to each skill's existing fallback, so a project with no policy behaves
  exactly as it does today."

## Existing Constraints Touched

| Constraint | Source (`file:line`) | Consequence for this spec |
|---|---|---|
| Mandated eager directive form for bot polling | `claude-code/skills/CLAUDE.md` §"Bot Review Polling Parameters" — *"Skills must reference the file with an explicit `> **Action required**: Read [references/pr-bot-polling.md]` directive, not a bare hyperlink, so the LLM actually reads the canonical parameters"* | L1 cannot simply weaken these to hyperlinks. The amendment must preserve "actually reads" while adding "only on the branch that needs it". |
| Same, for PR conflict resolution | `CLAUDE.md` §"PR Conflict & Merge-Readiness Resolution" | Same treatment. |
| Same, for language resolution | `CLAUDE.md` §"Language Resolution" — *"Do not inline or approximate the precedence chain, code list, or `## Language Policy` section format in a SKILL.md body"* | L2's script must become the canonical executor so the "do not inline" rule is satisfied by *invoking*, not *restating*. |
| Same, for task initials | `CLAUDE.md` §"Task Initials Resolution" | Same treatment. Single consumer (`ywc-task-generator`). |
| Script-over-prose precedent already established | `CLAUDE.md` §"Bundled Execution Scripts" table (15 existing scripts, e.g. `ywc-task-generator/scripts/compact-dependency-graph.py`) | L2 adopts an existing, documented pattern — no new architecture. |
| Language precedence chain, terminal rung is NOT forced `en` | `references/language-resolution.md:22-33` — *"This terminal rung is deliberately **NOT** a hardcoded `en` — routing through each skill's own fallback is what preserves no-regression behavior"* | The script must return a distinct "unresolved" sentinel, never `en`, so each caller applies its own fallback (`ywc-spec-writer` → `ko`, `ywc-task-generator` → infer-then-ask → `en`, `ywc-create-pr` → prompt). |
| Initials resolution has a human-confirmation rung | `references/initials-resolution.md:24-26` — *"derive from `git config user.email` / `user.name`, present the derived value for user confirmation, cache on approval"* | The script cannot complete rung 3 unattended; it must emit a `NEEDS_CONFIRM` status with the derived candidate and let the skill run the prompt. |
| `ywc-setup-language` *writes* the canonical section, not just reads it | `ywc-setup-language/SKILL.md:55,66,73` | This consumer needs the canonical `## Language Policy` section text, not just a resolved code. The script needs an `--emit-section <code>` mode, or this consumer keeps its reference read. |
| `--non-interactive` directive is already correctly gated | `ywc-sequential-executor/SKILL.md:78` — *"Action required **when `--non-interactive` is set**"* | This is the target shape. Use it as the canonical exemplar in the amended policy; do not "fix" it. |
| Stale entry in the bundled-scripts table | `CLAUDE.md` §"Bundled Execution Scripts" lists `ywc-confidence-gate/scripts/score-gate.py`; `claude-code/skills/ywc-confidence-gate/scripts/` **does not exist** | Since the amendment edits this table anyway, correct or remove the stale row in the same change. |

## Module Boundaries

| Module | Public interface | Owner |
|---|---|---|
| `claude-code/skills/scripts/resolve-language.sh` | `resolve-language.sh [--lang <code>] [--emit-section <code>]` → stdout one of `ko\|ja\|en\|es\|zh` or `UNRESOLVED`; exit 0 always (no-block invariant) | new, shared across 6 consumers |
| `claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh` | `resolve-initials.sh [--initials <s>]` → stdout `RESOLVED <s>` \| `NEEDS_CONFIRM <candidate>` \| `NONE`; exit 0 always | new, single consumer |
| `claude-code/skills/CLAUDE.md` | Authoring policy consumed by `ywc-skill-author` and every future skill author | amended |

## Acceptance Criteria

| # | Criterion |
|---|---|
| AC1 | When `bash claude-code/skills/scripts/resolve-language.sh --lang Japanese` is run, the system prints exactly `ja` and exits 0, observable as `[ "$(bash claude-code/skills/scripts/resolve-language.sh --lang Japanese)" = "ja" ]`. |
| AC2 | When `resolve-language.sh` runs in a repository whose `CLAUDE.md` and `~/.claude/CLAUDE.md` both lack a `## Language Policy` section and no `--lang` is passed, the system prints `UNRESOLVED` (never `en`) and exits 0, observable as a shell assertion in the script's own test file. |
| AC3 | When project `CLAUDE.md` declares `ko` and user `~/.claude/CLAUDE.md` declares `ja`, the system prints `ko` (project beats user), observable via a fixture-directory test. |
| AC4 | When `resolve-initials.sh` runs with no `--initials` flag, no `## Task Initials` section, and `git config user.email` set to `yongwoon.kim@example.com`, the system prints `NEEDS_CONFIRM yk` and exits 0 — it never writes the value itself. |
| AC5 | When `resolve-initials.sh` runs with no flag, no section, and no resolvable git identity, the system prints `NONE` and exits 0, and `ywc-task-generator` proceeds without an initials namespace (no-block invariant preserved). |
| AC6 | Every one of the 6 SKILL.md files carrying a `language-resolution.md` `**Action required**` directive (`ywc-auth-implement:50`, `ywc-create-pr:56`, `ywc-task-generator:48`, `ywc-setup-language:24`, `ywc-spec-writer:92`, `ywc-commit:135`) either invokes `resolve-language.sh` or states an explicit read condition. Observable via a **broad identifier grep**, not an anchored one — the six directives use three different link forms (parenthesized, bare-bracket, and one indented 3 spaces at `ywc-create-pr:56`), so an anchored regex shares the blind spot it is meant to catch: `grep -rn 'Action required' claude-code/skills/*/SKILL.md \| grep -c 'language-resolution'` returns 0. |
| AC7 | Every remaining `**Action required**` directive in `claude-code/skills/*/SKILL.md` states an explicit condition ("when `<flag>` is set", "before `<named step>`", "when `<branch>` is entered"), observable as a grep whose every hit matches `Action required (when\|before\|if)`. |
| AC8 | `bash scripts/validate.sh` exits 0 after all changes. |
| AC9 | `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh <dir>` exits 0 for each of the 12 modified skill directories. |
| AC10 | `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json` produces a mechanical score no lower than the recorded pre-change baseline on every modified skill. |
| AC11 | For each of at least 3 representative skills, a `ywc-toolkit-eval` before/after run over its `evals/fixtures/` produces the same observable outcome, recorded with `s3_source: "runner"`; skills lacking fixtures are recorded `(read-only)` and are not counted as behavioral evidence. |
| AC12 | The measured activation cost of `ywc-sequential-executor` (body tokens + tokens of references its default no-flag path reads) is strictly lower than the recorded 23,000-token baseline, reported as a before/after number in the completion summary. |
| AC13 | `claude-code/skills/CLAUDE.md` states the amended convention in all four mandating sections (Bot Polling / PR Conflict / Language Resolution / Task Initials), and the stale `ywc-confidence-gate/scripts/score-gate.py` row is corrected or removed. |
| AC14 | `git diff --name-only -- codex/ plugins/` is empty. |

## Functional Requirements

| # | Requirement | Satisfies |
|---|---|---|
| FR1 | Add `claude-code/skills/scripts/resolve-language.sh` implementing the 4-rung precedence chain from `references/language-resolution.md:22-33` verbatim, plus the `normalize()` full-name→code mapping, printing `UNRESOLVED` for the terminal rung. | AC1, AC2, AC3 |
| FR2 | Add `--emit-section <code>` to `resolve-language.sh`, printing the canonical `## Language Policy` section body from `references/language-resolution.md:44-52`, so `ywc-setup-language` writes it without reading the reference. | AC1, AC6 |
| FR3 | Add a shell test file next to each new script asserting AC1–AC5, runnable without network or git-write side effects. | AC1–AC5 |
| FR4 | Add `claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh` implementing the precedence chain and derivation algorithm from `references/initials-resolution.md:22-50`, returning `RESOLVED` / `NEEDS_CONFIRM` / `NONE` and never prompting or writing. | AC4, AC5 |
| FR5 | Replace the `language-resolution.md` `**Action required**` directive in all 6 consumers with a ≤3-line block: the one-line script invocation, the meaning of each of the three return values, and a conditional pointer to the reference for the section-format details. | AC6 |
| FR6 | Replace the `initials-resolution.md` directive in `ywc-task-generator:114` the same way, keeping the confirmation prompt in the skill body where the human interaction belongs. | AC4, AC6 |
| FR7 | For each of the 17 remaining `**Action required**` directives, relocate it to the branch that consumes it and prefix its condition, using `ywc-sequential-executor:78` as the canonical shape. Directives whose consuming branch is genuinely always entered stay put but state that explicitly ("before Step N, always"). | AC7 |
| FR8 | Amend `claude-code/skills/CLAUDE.md`: in the four mandating sections, change the required form from "read the file" to "read the file **on entering the branch that needs it**", and in the Language/Initials sections make script invocation the canonical mechanism with the reference retained as the human-maintained source of truth. | AC13 |
| FR9 | Add both new scripts to the `CLAUDE.md` §"Bundled Execution Scripts" table and correct or remove the stale `score-gate.py` row. | AC13 |
| FR11 | Run `ywc-toolkit-eval` before and after the change: the mechanical tier (`scripts/score.py --target claude-code/skills --format json`) over all modified skills, and the behavioral tier (`scripts/runner.py`) over the fixture-backed subset identified in Q2. Record `s3_source` per item so measured and read-only evidence are never merged. | AC10, AC11 |
| FR10 | Record a before baseline (per-skill `wc -c` of `SKILL.md`, plus the reference set each default path reads) prior to any edit, and re-measure after, reporting both. | AC12 |

## Non-Functional Requirements

| # | Requirement |
|---|---|
| NFR1 | Both scripts must be POSIX-`sh`-compatible bash and pass `shellcheck`, which `.github/workflows/validate.yml` runs over `scripts/`. |
| NFR2 | Both scripts must exit 0 in every path, including "not found" and "malformed input" — the no-block invariant makes a non-zero exit a behavior change. |
| NFR3 | No script may write to `CLAUDE.md`, `~/.claude/CLAUDE.md`, or any repository file. Resolution is read-only; writing stays with `ywc-setup-language`. |
| NFR4 | Each modified `SKILL.md` must remain ≤500 lines (A8) and must not lose its `**Announce at start:**` line or `## Rationalization Defense` section (`validate-skill.sh` hard-fails on both). |
| NFR5 | Token reduction must not come from deleting a rule. Any directive removed must have its content reachable at the branch that needs it. |

## Data Model / API Contract

N/A — no database, no HTTP surface. The two script CLIs are specified under Module Boundaries and FR1/FR2/FR4.

## Critical Surfaces

None. This change touches skill instruction text and two read-only resolution scripts; no auth, payment, crypto, PII, or external-input handling. Gray-box review is sufficient; `/ywc-security-audit` is not forced.

## Edge Cases

| # | Case | Required behavior |
|---|---|---|
| E1 | `## Language Policy` section present but its code is not in `ko\|ja\|en\|es\|zh` | Script prints `UNRESOLVED`, exits 0. Callers fall through to their own fallback — a malformed policy must not be more blocking than a missing one. |
| E2 | Both project and user `CLAUDE.md` contain `## Language Policy` | Project wins (`references/language-resolution.md:36-37`). Covered by AC3. |
| E3 | Two `## Language Policy` sections in one file (setup replaced-in-place invariant violated by hand-editing) | Script takes the first and exits 0. Never errors. |
| E4 | `--lang` passed with a full name in mixed case (`Japanese`, `JAPANESE`) | `normalize()` is case-insensitive; both yield `ja`. Covered by AC1. |
| E5 | `git config user.email` unset but `user.name` set | Fall back to `user.name` per `initials-resolution.md:47`. |
| E6 | Derived initials shorter than 2 characters | Take first 2–4 lowercase alphanumeric chars of the local-part per `initials-resolution.md:50-52`; if still invalid, print `NONE`. |
| E7 | A skill is invoked with a flag whose branch is never entered (e.g. `ywc-sequential-executor` without `--aggregate-pr`) | Its `aggregate-pr.md` reference is not read. This is the intended saving and must be asserted, not assumed. |
| E8 | Installed skills at `~/.claude/skills/` are stale relative to the repo after this change | `bash scripts/install.sh --cc` must be re-run before any behavioral before/after comparison, or the "after" run measures the old text. |
| E9 | `ywc-setup-language` needs the section format while `--emit-section` is unimplemented | This consumer keeps its reference read until FR2 lands; FR2 and FR5 must ship together for this skill. |
| E10 | A relocated directive lands inside a branch the skill can reach by two paths, one of which now skips it | Each relocation must be verified by enumerating every entry path into the consuming branch, not just the one path being edited. |

## Open Questions

> ⚠️ SUPERSEDED by Iteration 1 — see [Iteration 1 Amendments](#iteration-1-amendments). Q1–Q3 are resolved there; treat the amendment as authoritative.

| # | Question | Impact if unresolved |
|---|---|---|
| Q1 | Should `resolve-language.sh` live at `claude-code/skills/scripts/` (shared, matching `scripts/poll-pr-reviews.sh`) or be duplicated per consumer? Shared is assumed. | Path appears in 6 skill bodies; changing it later is a 6-file edit. |
| Q2 | Which 3+ skills have usable `evals/fixtures/` for the AC11 behavioral comparison? Must be enumerated before implementation, not discovered during verification. | If fewer than 3 have fixtures, AC11 degrades to `(read-only)` evidence and the "동일 결과" claim weakens to structural equivalence. |
| Q3 | Does `~/.claude/skills/` need reinstalling between the before and after eval runs (E8), and does `ywc-toolkit-eval` read the repo source or the installed copy? | A wrong answer invalidates the entire AC11/AC12 measurement. |

---

## Handoff

Downstream: `/ywc-spec-validate --spec docs/ywc-plans/20260901-claude-skill-token-efficiency.md`
→ `/ywc-task-generator` → `/ywc-sequential-executor`.

Note on Step 3.5: the Architectural Advisor Gate was **skipped**. The only structural choice —
prose reference vs bundled script for deterministic resolution — is already adjudicated by
`claude-code/skills/CLAUDE.md` §"Bundled Execution Scripts" and by 15 existing precedents.

---

## Operative Sections

`ywc-task-generator` must treat the following as authoritative: all sections above **except**
`## Open Questions`, which is superseded in full by Iteration 1 below. Where Iteration 1 amends a
numbered requirement (NFR1, FR5, AC7, AC11), the Iteration 1 text wins.

## Iteration 1 Amendments

Input: `ywc-spec-validate` iteration 1 — 1 Critical, 4 Warnings, 1 Suggestion; Confidence Gate 90 (PROCEED).

### A1.1 — Critical: shellcheck coverage claim was false (amends NFR1, adds FR12, amends AC8)

`.github/workflows/validate.yml:23` runs shellcheck with `scandir: ./scripts` — the repo-root directory
only. Neither new script location falls under it, and `scripts/validate.sh` runs no shellcheck of its own,
so the original NFR1 asserted CI coverage that does not exist.

**NFR1 (amended)**: Both new scripts must be POSIX-compatible bash and must pass `shellcheck`. CI coverage
for their locations does not exist today and is added by FR12; until FR12 lands, a passing `scripts/validate.sh`
is **not** evidence that either script is lint-clean.

**FR12 (new)**: Extend `.github/workflows/validate.yml`'s ShellCheck step to also scan
`claude-code/skills` (second `scandir` entry or a matrix over both roots), so
`claude-code/skills/scripts/resolve-language.sh` and
`claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh` are linted. Pre-existing shellcheck
findings in the 4 already-present shared **shell** scripts (`mark-complete.sh`, `poll-pr-reviews.sh`,
`scan-stubs.sh`, `test-poll-pr-reviews.sh`) must be triaged — the fifth file, `update-state.py`, is Python and
is outside shellcheck's scope in the same change — either fixed, or suppressed with an inline
`# shellcheck disable=` carrying a reason. Silencing the whole new scandir to make CI green is not acceptable.
→ Satisfies AC15.

**AC15 (new)**: When the ShellCheck workflow step runs on a branch containing both new scripts, it scans
them and exits 0, observable as `shellcheck claude-code/skills/scripts/resolve-language.sh
claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh` exiting 0 locally **and** the workflow's
ShellCheck step reporting a non-empty file list for the `claude-code/skills` scandir.

**AC8 (amended)**: `bash scripts/validate.sh` exits 0 **and** the ShellCheck step of
`.github/workflows/validate.yml` passes with `claude-code/skills` in scope. The original AC8 alone does not
prove script lint-cleanliness.

### A1.2 — Warnings 1–3: Open Questions Q1–Q3 resolved from the codebase

All three were answerable by reading, which `ywc-plan`'s Codebase-Fact Pre-check requires. `## Open Questions`
is superseded; the resolved facts move into Existing Constraints Touched:

| Was | Resolution (`file:line`) |
|---|---|
| Q1 — where does `resolve-language.sh` live? | `claude-code/skills/scripts/` is the established shared home; it already holds 5 scripts, and `scripts/install.sh:154,307` (`install_cc_support_dirs`, called from `run_cc_install`) installs it on **both** full and partial `--cc` runs. No install change needed. |
| Q2 — which skills have usable eval fixtures? | 10 skills carry `evals/`; 5 are in this spec's modified set: `ywc-auth-implement`, `ywc-commit`, `ywc-create-pr`, `ywc-sequential-executor`, `ywc-task-generator`. |
| Q3 — does the eval read repo source or the installed copy? | Repo source. `score.py --target claude-code/skills` scans the given root; `runner.py:58` sets `FIXTURE_ROOT = SKILL_ROOT / "evals" / "fixtures"`. Reinstall is not a precondition for the mechanical tier. |

**AC11 (amended)**: The before/after behavioral comparison runs over exactly these 5 fixture-backed skills —
`ywc-auth-implement`, `ywc-commit`, `ywc-create-pr`, `ywc-sequential-executor`, `ywc-task-generator` — each
recorded with `s3_source: "runner"`. The remaining 7 modified skills are recorded `(read-only)` and are
explicitly **not** counted as behavioral evidence.

**E8 (amended)**: Reinstalling `~/.claude/skills/` is required only for a run performed against the installed
copy. The FR11 measurement runs against the repo source and needs no reinstall.

**Open Questions (superseding entry)**: `N/A — none identified`. Q1–Q3 resolved above.

### A1.3 — Warning 4: FR5 invocation string fixed

All six precedent call sites (`ywc-create-pr:354`, `ywc-finish-branch:251`,
`ywc-parallel-executor:128,339,352,358`) use one repo-root-relative form. FR5 left the string free, inviting
six spellings.

**FR5 (amended)**: The replacement block in each of the 6 consumers must invoke the script with exactly:

```bash
bash claude-code/skills/scripts/resolve-language.sh
```

(plus `--lang <code>` or `--emit-section <code>` where the consumer needs them), matching the existing
convention verbatim. FR6's initials block uses the same form with its own path.

**AC16 (new)**: All 6 consumers spell the invocation identically, observable as
`grep -rho 'bash claude-code/skills/scripts/resolve-language\.sh' claude-code/skills/*/SKILL.md | sort -u | wc -l`
returning exactly 1.

### A1.4 — Suggestion 1: AC7 grep broadened

`ywc-finish-branch:156` reads `**Action required**: Read [...] **now** before proceeding` — genuinely
conditioned, but the qualifier follows `Read`, so the original anchored regex would have rejected a compliant
directive.

**AC7 (amended)**: Every remaining `**Action required**` directive states an explicit condition. Observable by
extracting each directive line and confirming it contains at least one of `when` / `before` / `if` / `only`
**anywhere in the line**, not immediately after `Action required`:
`grep -rh 'Action required' claude-code/skills/*/SKILL.md | grep -vcE '\b(when|before|if|only)\b'` returns 0.
