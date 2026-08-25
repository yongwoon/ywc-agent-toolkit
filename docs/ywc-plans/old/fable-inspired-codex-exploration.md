# Fable-Inspired Codex Exploration Enhancements

> Operative Sections: Read the base spec together with `## Iteration 1 Amendments`. Where Iteration 1 resolves or narrows an earlier open choice, Iteration 1 is authoritative.

## Purpose

Introduce a small, explicit set of Fable-inspired exploration rules into the Codex bundle so planning and implementation skills surface unknowns earlier, preserve useful discovery notes, and avoid over-constraining exploratory work with excessive examples. The goal is not to loosen evidence or safety discipline, but to improve how the bundle handles ambiguity and hidden assumptions before code is written.

## Scope

This change covers three concrete additions to the Codex skill bundle:

1. Add a new shared reference that defines an `Unknown Matrix` style prompt for surfacing:
   - known knowns
   - known unknowns
   - unknown knowns
   - unknown unknowns
2. Integrate that reference into the skills whose job is discovery or pre-implementation framing:
   - `ywc-brainstorm`
   - `ywc-plan`
   - `ywc-tech-research`
   - `ywc-onboard-repo`
3. Add a lightweight `implementation notes` convention for code-producing / execution skills so hidden decisions discovered during implementation are recorded instead of silently disappearing:
   - `ywc-code-gen`
   - `ywc-sequential-executor`
   - `ywc-parallel-executor`
4. Update `ywc-skill-author` so future exploratory skills prefer context, decision frames, and repository references over heavy few-shot/example cargo-culting.

## Out of Scope

- Relaxing reviewer or advisor evidence boundaries
- Changing custom agent TOML files under `codex/agents/`
- Rewriting existing HTML output conventions
- Introducing a new mandatory artifact for every task or plan
- Applying the new exploration language to every existing skill in the bundle
- Claude Code bundle parity in this change set unless a follow-up explicitly requests it

## Existing Constraints Touched

- `ywc-plan` already delegates vague requests to `ywc-brainstorm`, requires codebase investigation, and enforces complement-grep / blind-spot reduction; the new guidance must extend that behavior rather than replace it.
- `ywc-skill-author` already enforces strict trigger-focused frontmatter and progressive disclosure; the new rule must fit inside that model and must not encourage bloated SKILL bodies.
- `ywc-spec-ready` already maintains a loop log; the new `implementation notes` convention must not conflict with that existing spec-readiness log vocabulary.
- `ywc-code-gen` already uses a shared implementer base prompt and Contract Snapshot; any new implementation-notes rule should hook into those existing structures instead of creating a separate unrelated workflow.
- `ywc-onboard-repo` is intentionally Glob + Grep first; unknown-surfacing guidance must not degrade into read-every-file exploration.

## Acceptance Criteria

1. When reading the resulting bundle, another Codex instance can identify a single shared reference that explains how to surface hidden unknowns during discovery and planning.
2. `ywc-brainstorm`, `ywc-plan`, `ywc-tech-research`, and `ywc-onboard-repo` each contain an explicit pointer telling the reader when to apply the new unknown-surfacing reference.
3. `ywc-code-gen`, `ywc-sequential-executor`, and `ywc-parallel-executor` each define where implementation-time discovery notes should be recorded and what kinds of decisions belong there.
4. `ywc-skill-author` explicitly warns skill authors not to overfit exploratory skills with excessive static examples when a context-first decision frame is more appropriate.
5. None of the updated skills weaken existing evidence, scope, or safety rules.
6. Repository validation still passes after the documentation-only changes.

## Functional Requirements

### FR1. Shared Unknown-Matrix Reference

Create `codex/skills/references/unknown-matrix.md` as a shared reference document. It must:

- define the four quadrants in plain operational language
- explain when to use the matrix
- give a compact prompt pattern for discovery/planning skills
- distinguish unknown-surfacing from unbounded speculation
- state that verified repository/context evidence still outranks imagination

### FR2. Brainstorm Integration

Update `codex/skills/ywc-brainstorm/SKILL.md` so the discovery flow explicitly includes a blind-spot pass when:

- the request is broad
- the user has a strong but weakly-validated preference
- trade-offs are unclear

The integration should point to `references/unknown-matrix.md` rather than duplicating the full framework inline.

### FR3. Plan Integration

Update `codex/skills/ywc-plan/SKILL.md` so Step 1.0 / Step 2 guidance explicitly says to use the unknown-matrix reference when codebase investigation reveals missing design assumptions that are not yet strong enough to become direct implementation questions.

The added text must preserve the existing rule that unresolved implementation-blocking ambiguity still becomes `NEEDS_CONTEXT` or brainstorm routing rather than silent inference.

### FR4. Research Integration

Update `codex/skills/ywc-tech-research/SKILL.md` so the research workflow includes a short “unknowns surfaced” output component when recommendation quality depends on missing or weakly sourced dimensions.

This is not a license to speculate. The skill must continue to label inferred or missing evidence explicitly.

### FR5. Onboarding Integration

Update `codex/skills/ywc-onboard-repo/SKILL.md` so reconnaissance/architecture mapping can explicitly surface “unknown but high-value to verify later” repository questions without over-claiming conventions.

This integration must preserve the current Glob + Grep first discipline.

### FR6. Implementation Notes Convention

Add a shared reference for implementation notes or a clearly shared convention across the relevant skills. The convention must define:

- what belongs in implementation notes
- what does not belong there
- when notes are required vs optional
- where the note should live (for example: task artifact, completion summary, or implementation report section)

At minimum, the convention must capture:

- unexpected constraints found during implementation
- alternatives considered then rejected
- assumptions that were verified or invalidated mid-flight

### FR7. Code-Generation Integration

Update `codex/skills/ywc-code-gen/SKILL.md` and, if necessary, `prompts/implementer-base.md` so workers are instructed to return implementation notes when they encounter non-obvious decisions that affect final code shape.

The change must reuse existing artifacts such as Contract Snapshot / Per-Agent Summary / final report structure where possible.

### FR8. Executor Integration

Update `codex/skills/ywc-sequential-executor/SKILL.md` and `codex/skills/ywc-parallel-executor/SKILL.md` so execution summaries preserve implementation-discovery notes instead of collapsing them into silent local reasoning.

The convention must remain lightweight. It must not force long narrative logging between every task or wave.

### FR9. Skill-Author Guidance

Update `codex/skills/ywc-skill-author/SKILL.md` so future skill authors are instructed:

- not to overuse static worked examples in exploration-heavy skills
- to prefer concise context, decision framing, and selective references
- to treat examples as useful only when they reduce fragility rather than constrain reasoning

## Non-Functional Requirements

- Keep each modified SKILL body within existing bundle constraints, especially `ywc-skill-author`'s 500-line discipline and progressive disclosure rules.
- Prefer one new shared reference over repeated inline prose across multiple skills.
- Keep new wording operational and brief; avoid philosophical manifesto language.
- Preserve the bundle's current tone: strict, concrete, evidence-aware.

## Data Model / API Contract

N/A — documentation/routing change only; no runtime API or persisted data shape changes.

## Edge Cases

- A skill may already have a stronger local discovery discipline than the shared unknown-matrix prompt. In that case, the new reference is supplementary, not authoritative-over-local.
- Implementation notes must not become a dumping ground for routine status chatter, full logs, or repeated evidence already present elsewhere.
- Research skills must not use “unknowns surfaced” to mask a weak recommendation that should really be `DONE_WITH_CONCERNS`.
- Onboarding output must not label a guess as a convention just because the unknown-matrix pass surfaced it as interesting.
- Executor flows must not violate the non-stop execution rule by inserting mandatory human-facing progress commentary between tasks/waves.

> ⚠️ SUPERSEDED by Iteration 1 — see `## Iteration 1 Amendments`
## Open Questions

1. Should the implementation-notes convention live in a new shared reference file, or stay as a repeated but aligned lightweight rule in the three implementation/executor skills?
2. Should `ywc-tech-research` surface unknowns in the main report body, or only in `DONE_WITH_CONCERNS` / gaps sections?
3. Should `ywc-brainstorm` explicitly name the matrix in the visible user dialogue, or keep it as internal skill guidance only?

## Recommended Approach

Implement this in two passes:

1. **Shared references first**
   - Add `references/unknown-matrix.md`
   - Decide whether a second shared `implementation-notes.md` reference is warranted after checking token cost vs duplication
2. **Targeted skill wiring second**
   - Add short pointers and one-step workflow hooks in the affected skills
   - Reuse existing report sections and artifacts instead of inventing new files or mandatory logs

This keeps the change coherent, minimizes duplication, and preserves the bundle's current evidence-first architecture.

## Validation

- `bash scripts/validate.sh`
- `rg -n "unknown-matrix|implementation notes|few-shot|over-constraining examples" codex/skills codex/skills/references`
- `find codex/skills -path '*/agents/openai.yaml' -o -name 'SKILL.md' | sort`

## Iteration 1 Amendments

### Findings addressed

- **Completeness Critical** — The original spec left the canonical `implementation notes` shape unresolved in `Open Questions`, but task generation needs a single chosen implementation surface.
- **Code Compatibility Critical** — The original spec did not require synchronized updates to `agents/openai.yaml` for the touched skills, even though the bundle's own skill-authoring rules treat stale UI metadata as a defect.
- **Feasibility Critical** — `ywc-sequential-executor/SKILL.md` and `ywc-parallel-executor/SKILL.md` are already 498 lines each. Adding even a small inline subsection can violate the 500-line cap unless the change is written as a no-net-growth edit or paired with extraction to `references/`.
- **Consistency Warning** — The original spec did not define exactly where `ywc-tech-research` should surface “unknowns surfaced,” leaving report-shape drift likely.
- **Consistency Warning** — The original spec did not state whether `ywc-brainstorm` should expose “Unknown Matrix” wording to the user or keep it as internal workflow guidance.

### Chosen decisions

1. **Canonical implementation-notes surface**
   - Create a shared reference at `codex/skills/references/implementation-notes.md`.
   - The shared rule is:
     - default surface = existing completion/report section, not a new standalone artifact
     - required only when the skill encountered a non-obvious decision that materially affected final output
     - forbidden contents = routine status chatter, raw logs, duplicated evidence already recorded elsewhere
   - Per-skill application:
     - `ywc-code-gen` adds an `Implementation Notes` subsection to the final output format, adjacent to `Per-Agent Summary`
     - `ywc-sequential-executor` and `ywc-parallel-executor` record implementation notes in the existing completion report / per-task summary surface, not a new file

2. **Unknown-matrix visibility**
   - `ywc-brainstorm` keeps the Unknown Matrix as **internal skill guidance by default**.
   - The user-facing dialogue may ask blind-spot questions, but it does not need to literally name the framework unless doing so clarifies the conversation.

3. **Tech-research report placement**
   - `ywc-tech-research` adds `### Unknowns Surfaced` between `Project-Specific Considerations` and `References`.
   - The section is:
     - `N/A — no unresolved decision-shaping unknowns` when none exist
     - otherwise a short bullet list of unresolved but decision-relevant unknowns
   - If the recommendation materially depends on one of those unknowns, final status must be `DONE_WITH_CONCERNS`, not `DONE`.

4. **Metadata and locale sync**
   - Every touched skill in this spec must update `agents/openai.yaml` when `SKILL.md` meaningfully changes:
     - `ywc-brainstorm`
     - `ywc-plan`
     - `ywc-tech-research`
     - `ywc-onboard-repo`
     - `ywc-code-gen`
     - `ywc-sequential-executor`
     - `ywc-parallel-executor`
     - `ywc-skill-author`
   - For each touched skill, review the locale README set already shipped in the skill directory and update any files whose usage/behavior description materially changed. Tier 1 locale files are mandatory; Tier 2 locale files (`README.zh.md`, `README.es.md`) must stay aligned when present for that skill.

5. **500-line-cap mitigation for executor skills**
   - `ywc-sequential-executor/SKILL.md` and `ywc-parallel-executor/SKILL.md` must remain `<=500` lines after the change.
   - Therefore the implementation may not simply append new prose. It must use one of:
     - a no-net-growth replacement of existing wording, or
     - extraction of static content to `references/` before adding the new pointer/rule
   - Any task plan that edits those two skills must include a line-count check as part of verification.

### Additional functional requirements

### FR10. Metadata Sync

For every skill whose `SKILL.md` changes in this change set, regenerate or update the corresponding `agents/openai.yaml` so `interface.display_name`, `interface.short_description`, and `interface.default_prompt` remain aligned with the revised skill behavior.

### FR11. Locale README Sync Review

For every touched skill, review the required locale README set and update any README whose behavior/usage text is now stale because of the new exploration or implementation-notes rules. When `README.zh.md` / `README.es.md` exist for that skill, they must be kept aligned as well.

### FR12. Executor Line-Cap Safety

The implementation must preserve the `<=500` line cap for:

- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/SKILL.md`

If the new rule cannot fit as a minimal replacement, extract sufficient static content to `references/` first and add only a compact inline pointer.

### Updated acceptance criteria

7. Every touched skill still has synchronized `agents/openai.yaml` after the change.
8. `ywc-sequential-executor/SKILL.md` and `ywc-parallel-executor/SKILL.md` both remain at or below 500 lines after the change.
9. `ywc-tech-research` has an explicit `Unknowns Surfaced` output location rather than an implied or free-form placement.

### Updated validation

- `bash scripts/validate.sh`
- `wc -l codex/skills/ywc-sequential-executor/SKILL.md codex/skills/ywc-parallel-executor/SKILL.md`
- `find codex/skills -path '*/agents/openai.yaml' | sort`
- `rg -n "Unknowns Surfaced|Implementation Notes|unknown-matrix|implementation-notes" codex/skills codex/skills/references`
