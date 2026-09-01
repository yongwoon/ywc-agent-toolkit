# Plan: Reduce Codex skill-author activation context without changing its observable workflow

> Status: Ready for implementation
> Scale: Small
> Created: 2026-09-01

> Operative sections: all original sections remain authoritative except where
> explicitly amended by [Iteration 1 Amendments](#iteration-1-amendments).

## Goal

Reduce activation-time instruction tokens for the Codex-only skill-authoring workflow while retaining the current authoring and report-only audit outcomes. The repository-distributed equivalent of the installed `$skill-creator` is `codex/skills/ywc-skill-author`; the installed system skill at `/Users/yongwoon.kim/.codex/skills/.system/skill-creator/` is not a repository source and is out of scope.

The current source is 279 lines / approximately 3,045 words. Its main opportunity is repeated static guidance: Mandatory Rules are repeated in the Validation Checklist and overlap with Format Conventions and Anti-patterns. The refactor will keep decision-critical activation instructions inline and route only mode-specific static detail to existing or new on-demand references.

## Out of Scope

- Editing the installed OpenAI system `$skill-creator` outside this repository.
- Changing any `claude-code/` source or attempting cross-platform wording parity.
- Relaxing the `ywc-*` contract (frontmatter, locale README, metadata, validation, audit safety) or adding a new competing meta-skill.
- Claiming universal output equivalence; equivalence is bounded to the existing representative authoring/audit scenarios and the documented structural invariants.

## Files to Touch

| File | Change Type | Reason |
|---|---|---|
| `codex/skills/ywc-skill-author/SKILL.md` | Modify | Remove duplicated activation-time prose, retain the executable router and canonical rules, and point to conditional detail only when its mode needs it. |
| `codex/skills/ywc-skill-author/references/authoring-rules.md` | Add | Hold the detailed static rule/rationale matrix that is needed for authoring/restructuring but not report-only audit runs. |
| `codex/skills/ywc-skill-author/evals/evals.json` | Modify | Add a compact-routing scenario and make the existing scenarios the explicit behavioral baseline for the refactor. |
| `plugins/ywc-agent-toolkit/skills/ywc-skill-author/**` | Generated sync | Regenerate from `codex/skills/`; never hand-edit this package. |

## Implementation Steps

- [ ] Step 1: Establish a before baseline for `codex/skills/ywc-skill-author/SKILL.md`: record line, word, and byte counts; run its mechanical validator; retain the two current eval prompts as the required outcome contract.
      → verify: `wc -l -w -c codex/skills/ywc-skill-author/SKILL.md` is captured, and `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-skill-author` exits 0.

- [ ] Step 2: Classify every main-body section as always-needed routing/execution guidance or conditional static detail. Preserve inline: invocation boundary, Rationalization Defense, minimum canonical constraints needed before an edit, RED → GREEN → REFACTOR workflow, audit safety boundary, validator command, and completion checks. Move only duplicated/reference-like detail; do not move a rule merely to meet a line-count target.
      → verify: each moved item has one source of truth, an explicit `SKILL.md` link, a mode/condition for reading it, and no audit-only invocation is instructed to read authoring detail.

- [ ] Step 3: Rewrite `SKILL.md` as a compact mode router. Collapse duplicate descriptions of A1–A16 and their validation restatements into canonical references, merge overlapping format/anti-pattern explanations, and retain all enforcement semantics. Add precise routing for new skill, restructure, audit, scripts, metadata, and forward-test cases.
      → verify: frontmatter remains Codex-valid; the first announcement, report-only no-auto-delete boundary, script validation command, and all existing `references/` pointers remain reachable.

- [ ] Step 4: Add `references/authoring-rules.md` with the detailed, deduplicated authoring rules and rationale needed only by create/restructure work. Update `evals/evals.json` so a routine authoring request proves it follows the compact router and an audit request proves it does not unnecessarily load or apply authoring-only requirements.
      → verify: every new reference is at least 30 lines and is explicitly linked; all eval JSON remains valid; expected outputs still require the same Rationalization Defense quality and bounded deletion-test behavior.

- [ ] Step 5: Measure the candidate against the Step 1 baseline and run the focused plus bundle verification. Regenerate the marketplace copy from the Codex source and confirm no Claude Code path changed.
      → verify: `wc -l -w -c` shows a lower `SKILL.md` word count; `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-skill-author`, `bash scripts/sync-codex-plugin.sh`, and `bash scripts/validate.sh` all exit 0; the plugin copy matches the source; `git diff -- claude-code/` is empty.

## Verification

```bash
wc -l -w -c codex/skills/ywc-skill-author/SKILL.md
bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-skill-author
bash scripts/sync-codex-plugin.sh
bash scripts/validate.sh
git diff --check
git diff -- claude-code/
```

Expected outcome: the source `SKILL.md` is smaller by word count, validation and marketplace-sync checks pass, and the two pre-existing evaluation contracts still describe the required observable behavior.

## Risks and Rollback

| Risk | Likelihood | Mitigation / Rollback |
|---|---|---|
| A rule becomes invisible because it was moved behind the wrong route | Medium | Keep a canonical-rules index in the entrypoint, add a routing eval, and restore the rule inline if the baseline scenario changes. |
| Token reduction is only cosmetic or degrades behavior | Medium | Compare word/byte baseline and representative outputs; revert the specific extraction rather than weakening the invariant. |
| Generated marketplace package diverges from source | Low | Run the sync script followed by full validation; do not edit generated files manually. |

## Acceptance Criteria

- [ ] Codex-only source changes land under `codex/skills/ywc-skill-author/`; no `claude-code/` file changes.
- [ ] The activation-time `SKILL.md` has fewer words than the recorded baseline, with no duplicate static rule text retained in two sections.
- [ ] New/restructure calls can locate every mandatory rule through a direct, conditionally routed pointer before editing a target skill.
- [ ] Audit calls preserve the bounded report-only workflow and never authorize automatic deletion or target edits.
- [ ] The existing two behavioral eval contracts and the focused structural validator pass, and `bash scripts/validate.sh` passes after generated-plugin synchronization.

## Confidence Gate

Aggregate: 94/100 — PROCEED

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 95 | Target is the Codex-only distributed counterpart; installed system skill and Claude Code are explicitly excluded. |
| Architecture compliance | 95 | `codex/skills/` is source of truth and `plugins/ywc-agent-toolkit/skills/` is generated by the repository sync script. |
| Evidence quality | 95 | Current body statistics, rules, evaluation scenarios, validator, and package-sync contract were inspected. |
| Reuse verified | 85 | Existing progressive-disclosure, audit, template, and validator resources are reusable; the new reference is justified only for the currently duplicated routing detail. |
| Root cause identified | 95 | The cost comes from static prose repeated at activation, not from missing capabilities or tooling. |

## Iteration 1 Amendments

### Findings addressed

- The original word-count-only finish line did not prove the stated
  activation-token reduction.
- Moving the canonical rules behind an authoring-only route would leave audit
  mode without the full criteria it must assess.
- The original validation commands established file structure, but did not
  prove local-reference routing, metadata alignment, or the intended
  authoring/audit behavior.

### Amended approach

Keep a compact canonical-rule and audit-criteria index in `SKILL.md` for every
mode. It must preserve an immediately readable route for A1–A16, the
Rationalization Defense, the RED → GREEN → REFACTOR workflow, report-only audit
boundary, validator command, and completion checks. Extract only explanatory
rationale, worked decision detail, and create/restructure-specific guidance to
`references/authoring-rules.md`. Create/restructure requests must read that
reference before editing; audit requests must use the inline rule index plus
`references/audit-workflow.md` and must not be instructed to read the
authoring-only reference.

Before editing, record these immutable baselines in the implementation notes:

| Measure | Baseline | Method |
|---|---:|---|
| Lines / words / bytes | 279 / 3,045 / 20,856 | `wc -l -w -c codex/skills/ywc-skill-author/SKILL.md` |
| Activation-token estimate | 4,724 | `python3 -c 'import tiktoken; print(len(tiktoken.get_encoding("o200k_base").encode(open("codex/skills/ywc-skill-author/SKILL.md").read())))'` |

`o200k_base` is the fixed comparison encoding for this refactor; it is a
repeatable proxy, not a claim about every possible future Codex tokenizer. A
candidate passes the efficiency threshold only when it is at most 4,251
`o200k_base` tokens (a reduction of at least 10%) and has fewer than 3,045
words. If `tiktoken` or the named encoding is unavailable, stop before judging
the threshold and record the missing reproducibility prerequisite; do not
substitute a different tokenizer silently.

Create a rule ledger as a temporary implementation artifact. It must give one
row for each of A1–A16 and for the audit safety invariants, identifying its
canonical source after the refactor (`SKILL.md` or `authoring-rules.md`), every
mode that must consult it, and its structural, behavioral, or manual evidence
witness. The ledger is the preservation check; no rule may be removed merely
because a validator does not parse it.

Include `codex/skills/ywc-skill-author/agents/openai.yaml` in the source review.
Update it only if the compact router changes the user-facing purpose or default
prompt; in either case, inspect all three `interface` fields against the final
`SKILL.md` and let the normal generated-plugin sync carry the result.

Forward-test the final router in fresh agent contexts and save the response
artifacts outside the skill source. Run the existing authoring and audit prompts
from `evals/evals.json` plus the new compact-routing prompt. A reviewer checks:

| Scenario | Required observable behavior | Forbidden behavior |
|---|---|---|
| New/restructure | Announces the skill, keeps the inline canonical index, and explicitly routes to `authoring-rules.md` before target edits | Treats the reference as optional or omits an A1–A16 route |
| Audit | Uses the complete inline audit criteria and report-only protocol | Instructs the user to load `authoring-rules.md`, edits a target, or authorizes deletion |
| Compact routing | Distinguishes conditional authoring detail from always-loaded executable rules | Claims output equivalence without the specified scenario evidence |

This is a documented manual behavioral comparison; `evals/evals.json` and
`scripts/run-codex-skill-contract-evals.sh` remain structural-contract checks
only and must not be described as executing these prompts.

### Updated acceptance criteria and verification

- [ ] The final `SKILL.md` is ≤4,251 `o200k_base` tokens and has fewer than
  3,045 words, measured with the exact commands above; line and byte counts are
  retained as diagnostics.
- [ ] An A1–A16 plus audit-invariant ledger shows one canonical, reachable
  route and an evidence witness for every preserved rule.
- [ ] `authoring-rules.md` contains only conditional authoring/restructure
  detail, is at least 30 substantive lines, and is linked directly from
  `SKILL.md`; audit routing does not point to it.
- [ ] `agents/openai.yaml` has been reviewed and its `display_name`,
  `short_description`, and `default_prompt` match the final skill purpose.
- [ ] The three forward-test artifacts satisfy the observable/forbidden
  behavior table above; the two existing eval records are validated as
  structural JSON contracts, not claimed as executable agent tests.

Run the original verification commands with these additions:

```bash
python3 -c 'import tiktoken; print(len(tiktoken.get_encoding("o200k_base").encode(open("codex/skills/ywc-skill-author/SKILL.md").read())))'
rg -n '\[references/authoring-rules\.md\]\(references/authoring-rules\.md\)' codex/skills/ywc-skill-author/SKILL.md
for ref in codex/skills/ywc-skill-author/references/*.md; do
  base="$(basename "$ref")"
  rg -F "$base" codex/skills/ywc-skill-author/SKILL.md
done
bash scripts/run-codex-skill-contract-evals.sh
git diff --exit-code -- claude-code/
```

## Iteration 2 Amendments

### Findings addressed

- The first amendment required preserved-rule and forward-test evidence but did
  not give that evidence a durable, reviewable location.
- A combined new/restructure test did not prove the restructure route itself.
- The proposed reference check found filenames but did not prove a direct,
  resolvable Markdown link.

### Amended evidence and routing contract

Add the following committed evidence artifact to the Files to Touch list and
keep it with the refactor:

```text
docs/ywc-plans/evidence/20260901-small_codex-skill-creator-token-efficiency.md
```

Its required sections are: the immutable baseline table; the A1–A16 plus audit
invariant ledger (rule, canonical final location, modes, and evidence witness);
one subsection each for `new-skill`, `restructure`, `audit`, and
`compact-routing`; and a final reviewer verdict. Each scenario subsection must
record the exact prompt, that it was run in a fresh context, the unedited agent
response, the required/forbidden-behavior checklist, and PASS or FAIL. The
artifact contains the manual forward-test evidence only; it must not contain
secrets, installed-skill copies, or generated plugin files.

The explicit restructure scenario is: “Use `$ywc-skill-author` to restructure
an existing ywc-* skill by extracting a static decision table while preserving
all mandatory rules and its report-only audit behavior.” It passes only when
the response announces the skill, directs create/restructure work to
`authoring-rules.md` before edits, retains an inline canonical rule/audit
index, and names focused validation; it fails if it moves workflow,
Rationalization Defense, Validation Checklist, or audit safety behind the
reference. The original authoring prompt remains the distinct new-skill
scenario. Together with the audit and compact-routing scenarios, this produces
four saved scenario subsections (not three).

Replace the filename-only reference check with this fail-fast check. It proves
the direct Markdown pointer for the new reference and that every named local
reference exists; run it with Bash under `set -e` semantics:

```bash
set -euo pipefail
skill_dir="codex/skills/ywc-skill-author"
rg -q '\[references/authoring-rules\.md\]\(references/authoring-rules\.md\)' "$skill_dir/SKILL.md"
while IFS= read -r target; do
  test -f "$skill_dir/$target"
done < <(rg -o '\]\(references/[A-Za-z0-9._-]+\.md\)' "$skill_dir/SKILL.md" | sed -E 's/^\]\(//; s/\)$//' | sort -u)
diff -u \
  <(rg -o 'references/[A-Za-z0-9._-]+\.md' "$skill_dir/SKILL.md" | sort -u) \
  <(rg -o '\]\(references/[A-Za-z0-9._-]+\.md\)' "$skill_dir/SKILL.md" | sed -E 's/^\]\(//; s/\)$//' | sort -u)
test -f docs/ywc-plans/evidence/20260901-small_codex-skill-creator-token-efficiency.md
```

### Updated acceptance criteria

- [ ] The committed evidence artifact has the prescribed baseline, complete
  rule ledger, four fresh-context scenario records, and reviewer verdict.
- [ ] New-skill and restructure are independently tested; audit and
  compact-routing remain independently tested.
- [ ] Every local reference used by the final router exists, and
  `authoring-rules.md` has the exact direct Markdown link from `SKILL.md`.
