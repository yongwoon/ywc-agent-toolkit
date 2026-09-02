# Spec: Port develop-with-llm PR #220 into Codex `ywc-project-scaffold`

> Status: Draft — pending `ywc-spec-validate`
> Scale: Medium
> Created: 2026-09-02
> Source: [develop-with-llm PR #220](https://github.com/yongwoon/develop-with-llm/pull/220)
> Confidence Gate: 92/100 — PROCEED (Scope 95 / Architecture 90 / Evidence 95 / Reuse 90 / Root cause 90)

> Operative Sections: the original sections above remain the baseline; the
> `## Iteration 1 Amendments` section below is authoritative where it adds or
> clarifies readiness contracts.

## Purpose

Port the applicable behavior from PR #220 into the **Codex-only**
`ywc-project-scaffold` skill:

1. Make large-scale or explicitly contested architecture scaffold requests run a
   lightweight, current-practice check through `ywc-tech-research`, while
   keeping the loaded reference as the baseline and surfacing—not silently
   applying—material differences.
2. Add an approval-gated `reference-refresh` mode for reviewing this skill's
   own language reference files against repository evidence or research.
3. Enrich the Go and JavaScript/TypeScript references with the generic,
   upstream-proven conventions and variants from the PR.

The requested outcome is a Codex-native port, not a byte-for-byte copy of the
Claude Code diff. The current Codex skill has a smaller input-resolution and
structured-output contract, so the new routing must fit that contract without
inventing Claude slash-command syntax or changing unrelated behavior.

## Why

`references/*.md` are shared, curated baselines. They can drift from current
practice, and an unreviewed edit changes every future scaffold generated for
that language. PR #220 addresses both risks: research is conditional where an
architecture decision has high cost, and reference-file changes are additive
and require user approval. Its Go and JavaScript additions also supply concrete
patterns that the current Codex references lack.

## Scope

- `codex/skills/ywc-project-scaffold/SKILL.md`: extend discovery, routing,
  behavioral flow, output contract, boundaries, and validation for Trend Check
  and `reference-refresh`.
- `codex/skills/ywc-project-scaffold/references/javascript.md`: add shared
  naming and component-logic-colocation guidance, with narrow links from the
  affected Next.js/Astro variants.
- `codex/skills/ywc-project-scaffold/references/go.md`: add the Layered,
  Connect-RPC large-service alternative and generic `injector/`, `gen/`, and
  `converter/` convention entries.
- `codex/skills/ywc-project-scaffold/evals/evals.json`: add Codex-format
  contract fixtures for the new conditional-research and approval-gated modes.
- Regenerate `plugins/ywc-agent-toolkit/skills/` from the changed Codex source
  with `bash scripts/sync-codex-plugin.sh`; do not edit generated files.

## Out of Scope

- Any `claude-code/skills/` file. This is expressly a Codex-only port.
- Altering unrelated language references (`python.md`, `ruby.md`, `rust.md`,
  `protocols.md`) or changing an existing reference variant/removing a pattern.
- Automatically executing research, changing a reference, or creating project
  files while preparing this plan.
- Adding a library, framework, network client, or external tooling.
- Hand-editing `plugins/ywc-agent-toolkit/skills/`.
- README locale rewrites. The existing six README files remain structurally
  required and are validation inputs, but PR #220 changes skill workflow and
  reference guidance rather than the packaged README format. Revisit them only
  if implementation shows a user-facing invocation example is now misleading.

## Existing Constraints Touched

| Constraint | Evidence | Consequence |
|---|---|---|
| Codex source is authoritative; marketplace content is generated | `codex/AGENTS.md` §Project Structure; `scripts/sync-codex-plugin.sh` | Edit only `codex/skills/...`; regenerate the plugin afterward. |
| A Codex skill requires only `name` and `description` frontmatter plus `agents/openai.yaml` | root `AGENTS.md` §Project Structure and §Coding Style | Preserve the existing two-field frontmatter and metadata file; do not import Claude-only fields. |
| Existing skill output is a structured report with status | `codex/skills/ywc-project-scaffold/SKILL.md:173-184` | Add `reference-refresh` to the report mode/value surface and make its proposal/approval stop explicit. |
| Current normal input model defaults Scale to medium | `codex/skills/ywc-project-scaffold/SKILL.md:56-67` | Do not copy upstream's broader Input Resolution Gate verbatim. `reference-refresh` must instead bypass normal framework/scale collection and require only target reference path(s). |
| Research skill exists and accepts topic plus `--depth 25` | `codex/skills/ywc-tech-research/SKILL.md` §§Arguments, Execution Steps | Refer to the sibling by its Codex skill name; require its sourced, recency-checked output rather than embedding current-practice claims in scaffold. |
| Generated plugin freshness is enforced by validation/hooks | `.githooks/pre-commit:14-35`; `scripts/validate.sh` package checks | The implementation and verification sequence must sync before the final validation. |
| JavaScript reference still uses lowercase framework/tool-owned filename examples | `codex/skills/ywc-project-scaffold/references/javascript.md:30-50, 80-89, 403-410` | Naming guidance must explicitly exempt Next App Router, layout partials, and UI-kit-generated filenames; it cannot be a blanket PascalCase rule. |
| Go currently offers DDD as its only large standard-Go variant | `codex/skills/ywc-project-scaffold/references/go.md:102-175` | Add Layered/Connect RPC beside—not in place of—DDD, with selection criteria. |
| Codex skills carry machine-readable contract eval fixtures | `codex/skills/ywc-project-scaffold/evals/evals.json:1-34`; `scripts/run-codex-skill-contract-evals.sh:91-99` | Extend the established JSON fixture rather than creating a new test mechanism. |

## Acceptance Criteria

| ID | Acceptance criterion |
|---|---|
| AC1 | A normal large-scale scaffold request loads its applicable reference, invokes a lightweight `ywc-tech-research` check, and reports a material delta as an Extras callout; it neither silently rewrites the tree from research nor edits a reference. |
| AC2 | A small/medium request with no contested architecture skips the Trend Check and retains the existing fast baseline behavior. |
| AC3 | A user explicitly questioning/contesting the architecture triggers the same check even when Scale is not large. |
| AC4 | A request to review/refresh/audit one or more `references/<language>.md` files routes to `reference-refresh`, identifies language from the target path, and does not require framework or scale. |
| AC5 | `reference-refresh` uses supplied real repository/documentation evidence when available; otherwise it requests appropriately scoped `ywc-tech-research` (language-only if framework is unresolved, language/framework if resolved). |
| AC6 | `reference-refresh` proposes only additive changes, displays the diff, and stops for approval before any reference edit. It never removes or overwrites an existing valid variant under this mode. |
| AC7 | The JavaScript reference defines cross-framework naming conventions, explicit reserved/generated filename exceptions, component-private logic colocation, and staged promotion from component → feature → app-shared. Affected Next.js/Astro sections link to the shared rule rather than duplicate it. |
| AC8 | The Go reference offers `Go Large (Layered, Connect RPC)` as a sibling to DDD, explains when to choose each, accurately states `usecase/port` versus aggregate-local repository interface ownership, and limits top-level `gen/` to protobuf/Connect stubs. |
| AC9 | The Go conventions table documents `injector/`, `gen/`, and `converter/` without implying that Small/Medium projects need them. |
| AC10 | Existing four scaffold eval fixtures remain valid JSON and new fixtures assert (a) large/contested Trend Check behavior and (b) approval-gated `reference-refresh`; no fixture expects a silent edit. |
| AC11 | `bash scripts/sync-codex-plugin.sh` followed by `bash scripts/validate.sh` succeeds, and the generated plugin contains the source changes. |

## Functional Requirements

### FR1 — Discriminating discovery and routing

Update the `ywc-project-scaffold` description/triggers only enough to make
reference-file review discoverable, while retaining its new-project-scaffold
boundary. Add a distinct `reference-refresh` route for review/refresh/audit of
this skill's own `references/<language>.md`; do not make generic documentation
review a match. Extend Rationalization Defense and Common Mistakes with the two
non-obvious safeguards: Trend Check is conditional, and shared reference edits
are proposal-first.

### FR2 — Conditional Trend Check for ordinary scaffold generation

After the relevant language/protocol references are selected and before the
tree is finalized, add a branch that runs when either:

- Scale is `large`; or
- the user explicitly questions/contests the requested or selected
  architecture.

The branch delegates a focused topic such as
`<language>/<framework> project structure conventions` to
`ywc-tech-research --depth 25`. Compare findings with the loaded reference:

- confirmed baseline → continue without extra prose;
- material delta → add a clearly labelled Extras callout;
- research unavailable/inconclusive → retain the baseline and report
  `DONE_WITH_CONCERNS` with the evidence gap, not an invented trend.

It must not silently substitute research output into the tree and must not edit
references. Explicitly skip this branch for uncontested small/medium requests.

### FR3 — `reference-refresh` mode

Add a separately headed mode in `SKILL.md`, positioned before normal output
rules, with this behavior:

1. Identify one or more target language reference paths; infer language from
   each path. If no target can be resolved, return `NEEDS_CONTEXT`.
2. Gather supplied real-world source evidence directly. If none is supplied,
   call `ywc-tech-research --depth 25`; construct a language-only topic when
   framework is unknown and a language/framework topic only when it is known.
3. Compare evidence to the current reference and exclude mere rephrasing or
   already-documented patterns.
4. Produce an additive proposal: a sibling variant or entries in an existing
   conventions/key-points section. Preserve existing alternatives.
5. Return the proposal/diff in `Mode: reference-refresh` and wait for explicit
   user approval. Only a later approved turn may edit the skill-owned reference,
   then run Markdown lint/structural validation.

Make the normal-project boundary precise: it still never edits the user's
target project; this mode's narrow exception is only the skill's own reference
after approval.

### FR4 — JavaScript/TypeScript reference enrichment

In `references/javascript.md`:

- Add TOC entries and shared `Naming Convention` and `Component Logic
  Colocation` sections before framework-specific sections.
- Specify kebab-case directories, PascalCase component files, and camelCase
  utility/config files, then name the existing valid exceptions: Next App
  Router special files, informal layout partials, and UI-kit CLI-generated
  files.
- Define component-local `hooks/` and `functions/` alongside a component;
  promote reuse first to a feature and only then to app-shared locations when
  it crosses features. Note that Astro guidance applies to interactive islands,
  not normally static `.astro` components.
- Link only affected existing Key Points (Next.js small/medium/large and Astro
  medium) to the common sections. Preserve their current examples and do not
  mechanically rename them to satisfy the new convention.

### FR5 — Go reference enrichment

In `references/go.md`:

- Add the new large Layered/Connect RPC section and TOC entry immediately after
  the existing DDD alternative. Include the `cmd/`, tier-first `internal/`,
  generated Connect/protobuf `gen/`, migration, and test-infrastructure
  surfaces from PR #220.
- Retain DDD and make choice criteria explicit: Layered fits a single deployable
  with shared infrastructure and CRUD-shaped domains; DDD remains the option
  for genuinely diverging bounded contexts.
- Preserve the clarification from the PR review: aggregate-local repository
  contracts live with their aggregate, while consumer-side external/non-
  aggregate contracts live in `usecase/port`; the same contract is never in
  both locations. `usecase/types` is optional for complex usecase IO, and
  handler/repository converters may map directly to domain entities for simple
  CRUD.
- Add concise `injector/`, `gen/`, and `converter/` rows to the existing
  conventions table. State that top-level `gen/` is only generated
  protobuf/Connect stubs and is never hand-edited; DB code generation belongs
  under its own DB package.

### FR6 — Codex contract coverage and packaging

Append two contract-eval cases to the existing JSON fixture in its current
schema. One must exercise a large or contested scaffold request and assert
conditional research/delta handling; the other must ask to refresh `go.md` and
assert target inference, additive proposal, and approval stop. Update no
README merely to list eval internals. Regenerate the marketplace package only
via `scripts/sync-codex-plugin.sh` after source edits.

## Non-Functional Requirements

- Keep Codex `SKILL.md` frontmatter limited to `name` and `description`; retain
  valid `agents/openai.yaml` metadata.
- Keep instructional Markdown concise and in English outside localized
  README files, per repository guidance.
- Do not add a dependency declaration or new tooling.
- Keep all source changes under `codex/skills/ywc-project-scaffold/`; generated
  plugin diffs are expected only after sync.
- Do not claim current-practice facts without evidence supplied to the future
  Trend Check/refresh flow; research findings remain sourced by
  `ywc-tech-research`.

## Data Model / API Contract

No database or HTTP API is involved. The behavioral contract additions are:

| Surface | Contract |
|---|---|
| Normal output | Existing structured report remains; ordinary generation may include a labelled Trend Check delta in Extras. |
| New output mode | `Mode: reference-refresh` communicates that the output is a proposal, not an edit. |
| Approval boundary | A displayed reference diff is terminal for the current turn until explicit user approval. |
| Status behavior | Missing refresh target → `NEEDS_CONTEXT`; unavailable/inconclusive Trend Check → baseline plus `DONE_WITH_CONCERNS`; successful proposal/generation → `DONE`. |

## Implementation Sequence

1. Edit `SKILL.md` first so its routing and behavior exactly define both modes;
   keep normal scaffold flow intact and make the mode-specific boundary
   explicit.
2. Add the shared JavaScript conventions, then add only cross-references from
   the four affected variants. Validate the TOC anchors and preserve lowercase
   reserved/tool-generated examples.
3. Add the Go variant beside DDD, its TOC entry, and conventions-table rows;
   validate the ownership/DTO/generated-code wording against FR5.
4. Add the two Codex eval fixtures, ensuring expectations use the existing
   `prompt` / `expected_output` / `files` shape.
5. Run source checks, regenerate the plugin, then run final repository
   validation. Review the generated diff; never manually repair it.

## Verification

Run from the repository root:

```bash
python3 -m json.tool codex/skills/ywc-project-scaffold/evals/evals.json >/dev/null
bash scripts/install.sh --list --codex
bash scripts/sync-codex-plugin.sh
bash scripts/validate.sh
```

Additionally:

- Run `npx markdownlint-cli2@0.22.1` (or the repository's installed equivalent)
  against the three edited Markdown source files; fix only violations introduced
  by this change.
- `rg -n 'reference-refresh|Trend Check|Naming Convention|Component Logic Colocation|Go Large \(Layered, Connect RPC\)' codex/skills/ywc-project-scaffold`
  confirms all requested surfaces are present.
- Compare the regenerated plugin copy with source content for the target skill
  and inspect `git diff --check` for whitespace errors.
- Manually exercise the two eval prompts against the instructions: confirm the
  large/contested path does not silently alter a tree, and the refresh path
  stops after its additive proposal.

## Risks and Rollback

| Risk | Mitigation / rollback |
|---|---|
| Trend Check becomes unconditional and slows ordinary scaffolds | AC2 and the corresponding eval require it only for large/contested requests. Revert the isolated `SKILL.md` branch if it proves too broad. |
| Research is mistaken for authority over curated references | FR2 allows a labelled delta only; it cannot rewrite the tree or reference silently. |
| New naming rules contradict existing examples | The exception note is mandatory and existing framework/tool-owned names remain unchanged. |
| Layered guidance is read as replacing DDD | Make both sections sibling variants with explicit selection criteria; rollback is a documentation-only revert. |
| Plugin source and package drift | Always sync from Codex source then use `scripts/validate.sh`; rollback source and regenerate package together. |

## Handoff

✅ Spec drafted: `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md`

Next: run `ywc-spec-validate --spec docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md`, then (after it passes) `ywc-task-generator`.

## Iteration 1 Amendments

### Readiness Contract

This amendment resolves the readiness-contract gap without changing the
requested implementation scope.

#### Outcome Oracle

- **Target:** The Codex `ywc-project-scaffold` skill supports conditional
  Trend Check behavior and approval-gated `reference-refresh`, with the Go and
  JavaScript/TypeScript references enriched and the generated Codex plugin in
  sync.
- **Quality threshold:** Large or explicitly contested scaffold requests run
  the check and surface only a labelled material delta; uncontested small or
  medium requests skip it. Refresh requests produce an additive proposal and
  stop before editing. Existing variants remain intact, and all source/package
  contract checks pass.
- **Evidence required:** `python3 -m json.tool` on the eval fixture;
  `bash scripts/install.sh --list --codex`; `bash scripts/sync-codex-plugin.sh`;
  `bash scripts/validate.sh`; Markdown lint for the three edited source
  Markdown files; targeted `rg` checks; generated/source comparison; and
  manual exercise of both new eval prompts.
- **Stop condition:** Handoff is permitted only when validation reports
  `DONE`, with no unresolved Critical or Warning findings, the Blind Spot
  action is `proceed`, and the evidence commands and generated-content
  comparison pass. `DONE_WITH_CONCERNS` remains the stop condition when a
  Trend Check is unavailable or inconclusive.

#### Blind Spot Pass

- **Most rewrite-sensitive assumption:** The existing Codex scaffold output
  contract can express both a research delta and an approval-gated proposal
  without requiring a new mode/status schema incompatible with the current
  skill.
- **Repository evidence:** The current skill already has a structured report
  and the spec explicitly requires preserving that contract; the new mode is
  separately named and its approval stop is explicit.
- **Action:** `proceed`; implementation must preserve the existing report
  fields and add only the scoped mode/value surfaces described by FR1–FR6.

## Global Constraints

- Codex source is authoritative; generated marketplace content is produced by
  `bash scripts/sync-codex-plugin.sh` (`codex/AGENTS.md`).
- Codex `SKILL.md` frontmatter contains only `name` and `description`, and the
  skill retains `agents/openai.yaml` (`AGENTS.md`, Coding Style).
- Do not edit `plugins/ywc-agent-toolkit/skills/` by hand; validate source and
  generated content with `bash scripts/validate.sh` (`codex/AGENTS.md`).
- No new dependency, library, framework, network client, or external tooling
  is introduced (original Non-Functional Requirements).

## Quality Gate Contract

N/A — no project-owned complexity or mutation quality-gate contract is
defined. Repository structural validation, JSON validation, Markdown lint,
plugin synchronization, and targeted inspection are the required evidence.

## Module Boundaries

| Module | Owned public interface | Consumers | Allowed dependencies | Forbidden dependencies |
|---|---|---|---|---|
| `codex/skills/ywc-project-scaffold` | Structured scaffold report plus `reference-refresh` proposal/approval-stop contract | Codex users and downstream skill invocation | Its existing reference files and sourced `ywc-tech-research` output | Silent reference edits, silent research substitution, Claude slash-command syntax |
| `plugins/ywc-agent-toolkit/skills/ywc-project-scaffold` | Generated copy of the Codex skill | Marketplace/package consumers | Exact synchronized source content | Independent hand edits |

## Edge Cases

- A large or contested request with unavailable or inconclusive research keeps
  the loaded baseline and returns `DONE_WITH_CONCERNS`; it does not invent a
  delta or alter the tree.
- A refresh request with no resolvable `references/<language>.md` target returns
  `NEEDS_CONTEXT` and does not call research or edit files.
- A refresh request with supplied evidence does not call research solely to
  validate the same evidence; it excludes rephrasing and already-documented
  patterns from the proposal.
- A refresh proposal containing a removal or overwrite is invalid under this
  scope and must be revised to an additive proposal before approval.
- A generated plugin mismatch after synchronization is a validation failure;
  no hand-edited generated copy is accepted.

## Open Questions

N/A — none identified for task decomposition. Future implementation may still
encounter ordinary evidence availability, but the required behavior and stop
status for that case are specified above.
