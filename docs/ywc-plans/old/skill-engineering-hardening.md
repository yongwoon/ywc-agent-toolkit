# Skill Engineering Hardening for Claude Code and Codex

> Status: Draft
> Scale: Medium
> Created: 2026-07-13
> Author: Codex
> Spec Reference: `develop-with-llm/docs/studies/insights/MATT_POCOCK_SKILL_HELL_ENGINEERING.md`

## Purpose

Apply the useful parts of the Skill Hell engineering guidance without creating a
second, overlapping audit skill. Make `ywc-skill-author` the explicit,
read-only-first entry point for auditing and pruning distributed skills, and
make the cross-skill architecture easier to govern across the Claude Code and
Codex skill bundles.

The outcome is a repeatable way to find trigger collisions, oversized inline
material, redundant instructions, undocumented Claude/Codex drift, and unsafe
same-tier calls before they become more procedural debt.

## Scope

- Update `claude-code/skills/ywc-skill-author/` and
  `codex/skills/ywc-skill-author/` with a bounded audit-and-prune workflow.
- Add equivalent, on-demand audit rubric/reference material to each bundle.
- Add a portable, read-only audit script to each bundle that reports mechanical
  findings; retain model judgment for redundancy and deletion-test decisions.
- Add evaluation fixtures for the new audit behavior where the bundle's
  existing skill convention supports them.
- Extend the two cross-skill graphs with explicit role classification:
  interface, orchestrator, and discipline.
- Narrow the high-impact `ywc-agentic` trigger wording in both bundles so a
  full autonomous lifecycle runs only on an explicit autonomy request.
- Run the audit once in report-only mode and use its findings to select a
  follow-up, separately reviewed pruning pilot among the near-500-line skills.

## Out of Scope

- Creating a separate `ywc-skill-audit` skill. This duplicates the existing
  `ywc-skill-author` audit trigger and would worsen activation ambiguity.
- Editing any skill other than `ywc-skill-author` and `ywc-agentic` in this
  change; the pruning pilot is a subsequent change after evidence is reviewed.
- Changing `claude-code/agents/`, `codex/agents/`, hooks, plugin packaging,
  installation scripts, repository CI, or root validation logic.
- Enforcing automatic deletion or introducing a CI failure for style/rubric
  findings. Mechanical output is advisory until representative evaluations
  demonstrate a stable signal.
- Requiring strict byte-for-byte parity between Claude Code and Codex. Platform
  invocation syntax and runtime-specific instructions remain legitimate
  differences.

## Existing Constraints Touched

| Existing artifact | Behavior (verified) | New code's interaction |
|---|---|---|
| `claude-code/skills/CLAUDE.md` | Structural changes to a `ywc-*` skill must invoke `ywc-skill-author`; Claude examples use `/skill-name`. | Keep the authoring rules authoritative and use Claude slash examples only in Claude files. |
| `codex/skills/ywc-skill-author/SKILL.md` | Already triggers on auditing existing skills and defines 3-tier loading, a 500-line cap, required resources, and Codex-only frontmatter. | Extend this skill rather than add a competing audit skill; keep new details in references. |
| `claude-code/skills/ywc-skill-author/SKILL.md` | Mirrors the authoring/audit role for Claude Code, with platform-specific metadata rules. | Keep the audit workflow and rubric semantically aligned while preserving Claude-specific syntax. |
| `codex/skills/ywc-skill-author/references/cross-skill-graph.md` | Defines pipeline, anti-trigger pairs, flag propagation, and a no-overlap rule for new skills. | Add role/calling-boundary classification without invalidating existing orchestrator-to-discipline delegations. |
| `claude-code/skills/ywc-agentic/SKILL.md` and `codex/skills/ywc-agentic/SKILL.md` | Orchestrate planning, task generation, execution, and evaluation from a high-level goal. | Restrict activation language to explicit autonomous/full-lifecycle requests; do not change the workflow in this scope. |
| `scripts/validate.sh` | Validates required bundle structure and Codex metadata, but not semantic redundancy or cross-bundle behavioral parity. | Continue using it as the release gate; do not expand it in this change. |

## Acceptance Criteria

- [ ] **AC1 — Single audit entry point**: When a user asks to audit, prune, or
  deletion-test a distributed `ywc-*` skill, `ywc-skill-author` directs a
  report-only audit workflow; no `ywc-skill-audit` directory exists in either
  target bundle.
- [ ] **AC2 — Mechanical report**: When the bundled audit script is run against
  either target skill root, it deterministically reports skill line counts,
  missing reference pointers, explicit sibling-call edges, and Claude/Codex
  counterpart presence without modifying files.
- [ ] **AC3 — Deletion test discipline**: When a candidate instruction is
  proposed for removal, the workflow requires a baseline and revised run over
  the same representative prompt(s), records observable deltas, and rejects
  automatic deletion.
- [ ] **AC4 — Calling boundary**: The shared graph documents interface,
  orchestrator, and discipline roles; it permits orchestrator-to-discipline
  calls while prohibiting undocumented same-tier peer calls.
- [ ] **AC5 — Explicit autonomous trigger**: A generic request to plan or make
  a normal code change does not describe `ywc-agentic` as the route; an explicit
  request for autonomous end-to-end execution still does.
- [ ] **AC6 — Distribution validity**: The affected Claude and Codex skills
  retain their required localized README assets; affected Codex skills retain
  valid `agents/openai.yaml`; `bash scripts/validate.sh` passes.

## Functional Requirements

### FR-1: Add an audit-and-prune mode to `ywc-skill-author`

Add an explicit `--audit` / report-only workflow (or a clearly equivalent
argument convention matching the existing skill style). Require a target scope:
one skill, a selected group, or the current bundle. The mode must inspect before
recommending changes and return findings ordered by risk and evidence.

The workflow must distinguish mechanical findings from judgment findings. It
must never delete text, rewrite other skills, or call an autonomous executor.

### FR-2: Define the deletion-test protocol

Place the detailed protocol in a direct child reference of each
`ywc-skill-author` folder. The main skill body should retain only the decision
sequence: establish baseline prompts and observable criteria; make one bounded
removal; rerun the same prompts; compare; retain, revert, or escalate.

Include safe test cases for trigger precision, required procedure adherence,
and expected artifact shape. Do not ask a test agent to validate against a
leaked expected answer.

### FR-3: Provide deterministic audit evidence

Add a portable Bash script under each `ywc-skill-author/scripts/` directory.
It must accept roots/paths explicitly, be read-only, use stable sorted output,
and return non-zero only for invocation/input errors—not for advisory findings.

Its report must cover line-cap proximity, local-reference pointer integrity,
`@ywc-` force-load violations, declared `ywc-*` call edges, and missing
cross-bundle counterpart directories. It must not claim semantic duplication
or behavioral equivalence from text matching alone.

### FR-4: Formalize roles and parity review

Extend each `cross-skill-graph.md` with role definitions and a calling matrix.
Record that interface skills may hand off to orchestrators/discipline skills;
orchestrators may delegate to discipline skills; discipline skills must not
invent peer orchestration. Existing documented exception edges must be named,
not silently treated as violations.

Add an audit rubric section for Claude/Codex parity: compare user-visible
workflow, safety/verification gates, and handoff conditions; exempt invocation
syntax, supported tool instructions, and required metadata differences.

### FR-5: Reduce `ywc-agentic` activation breadth

Rewrite only the trigger/anti-trigger wording and corresponding localized usage
documentation needed to clarify that `ywc-agentic` is for a user explicitly
requesting autonomous, end-to-end lifecycle execution. Preserve its workflow,
arguments, and downstream routing.

### FR-6: Validate and select—not execute—a pruning pilot

Run report-only audit output against both bundles. Use it to nominate one of
`ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-gen-testcase`, or
`ywc-task-generator` for a later deletion-test/pruning change. The pilot choice
must cite findings and must not be folded into this scope.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Safety | Audit commands are read-only; findings never mutate bundle content or alter CI behavior. |
| Portability | Scripts use portable Bash with `set -euo pipefail` and standard shell utilities already used by the repository. |
| Context efficiency | Keep workflow-level directives in `SKILL.md`; put detailed rubric/examples in direct references. |
| Compatibility | Preserve required locale README assets and Codex `agents/openai.yaml` validity. |
| Determinism | Mechanical output is sorted and stable for the same filesystem input. |

## Data Model

N/A — no persistent application data or schema changes. Audit reports are
terminal output; evaluation fixtures are versioned skill resources only.

## API Contract

N/A — no network or service API. The local script command contract must be
documented with positional target/root arguments and its advisory exit behavior.

## Edge Cases

- A skill has no same-named counterpart in the other bundle: report it as a
  parity-review item, not an automatic failure, because platform-specific
  skills may be intentional.
- A local reference is intentionally unlinked because it is test-only: exclude
  it only through an explicit, documented convention; do not silently skip it.
- A skill is near 500 lines because it contains necessary ordered procedure:
  report proximity, then require a deletion test before extracting/removing it.
- A source-level textual difference is platform syntax only: classify it as an
  allowed parity difference, not behavioral drift.
- A proposed deletion changes an output's safety gate or required artifact:
  retain the instruction and record the failed deletion test.

## Dependencies

- Existing `ywc-skill-author` structure and validator in both target bundles.
- Existing `cross-skill-graph.md` references in both target bundles.
- Existing repository validation command: `bash scripts/validate.sh`.

## Open Questions

N/A — none block the plan. The audit script's exact flags should follow the
argument conventions discovered during implementation, while preserving the
read-only contract above.

## Implementation Sequence

1. Invoke `ywc-skill-author` for each bundle and inventory its local resources,
   README/eval conventions, and graph consumers.
2. Add the audit/deletion-test workflow and the one-level-deep rubric reference
   to Claude Code and Codex `ywc-skill-author` in parallel, preserving platform
   invocation syntax and Codex interface metadata.
3. Implement and exercise the read-only audit scripts with controlled fixtures:
   clean input, line-cap warning, missing counterpart, and invalid invocation.
4. Add/adjust skill eval fixtures where the existing bundle evaluation format
   supports deterministic assertions.
5. Update both cross-skill graphs with the role model, calling matrix, and
   parity-review rubric; verify existing documented edges remain allowed.
6. Narrow `ywc-agentic` descriptions and only the README wording that explains
   activation; update Codex `agents/openai.yaml` if its short/default prompt
   repeats the old activation promise.
7. Run audit scripts in report-only mode, validate both distributions, inspect
   diffs for scope, and publish the nominated follow-up pruning pilot without
   editing it.

## Validation Plan

- Run each new audit script on its own skill root and a deliberately invalid
  path; confirm advisory findings do not cause a failure exit.
- Run the existing `ywc-skill-author/scripts/validate-skill.sh` for each
  changed skill in both bundles.
- Confirm required README files exist for every changed skill and inspect
  affected translations for correct platform invocation syntax.
- For Codex, validate `agents/openai.yaml` fields against the revised
  `ywc-agentic` and `ywc-skill-author` descriptions.
- Run `bash scripts/validate.sh`.
- Use the same representative audit prompts before/after the workflow changes;
  verify they return a bounded, report-only outcome and do not create a second
  audit skill or modify targets.

## Risks and Rollback

- **False-positive audit findings**: Keep output advisory and require human
  deletion-test review. Roll back rubric/script changes independently if they
  prove noisy.
- **Trigger regression for `ywc-agentic`**: Preserve explicit multilingual
  autonomy phrases and test them against generic planning requests. Revert only
  the frontmatter/README wording if activation becomes too narrow.
- **Claude/Codex drift from duplicate edits**: Compare the shared audit contract
  and role matrix after edits; retain only intentional platform differences.
- **Context bloat**: Move examples and detailed procedures to references; do
  not add a second meta-skill or force-load sibling skills.

## References

- `develop-with-llm/docs/studies/insights/MATT_POCOCK_SKILL_HELL_ENGINEERING.md`
- `claude-code/skills/CLAUDE.md`
- `claude-code/skills/ywc-skill-author/SKILL.md`
- `codex/skills/ywc-skill-author/SKILL.md`
- `codex/skills/ywc-skill-author/references/cross-skill-graph.md`
- `docs/skill-agent-eval/codex/2026-07-06-full-sweep-mechanical.md`

## Iteration 1 Amendments

### Operative Sections

This amendment supplements FR-3, FR-4, the Implementation Sequence, and the
Validation Plan. Its explicit audit-script contract and parity rules take
precedence over the earlier statement that implementation may choose arbitrary
argument conventions.

### Amendment A — Audit script contract

The two copies of the script use this fixed, read-only interface:

```text
bash scripts/audit-skills.sh \
  --root <current-bundle-skills-root> \
  --counterpart-root <other-bundle-skills-root> \
  [--near-line-cap <integer>]
```

- `--root` and `--counterpart-root` are required existing directories.
- `--near-line-cap` defaults to `450` and must be an integer from `1` through
  `500` inclusive.
- Invalid arguments, nonexistent roots, and non-directory roots print a concise
  usage/error message to stderr and exit `2`.
- A valid audit exits `0` even when it reports findings.
- The script writes sorted, stable Markdown/plain-text sections in this order:
  `Inventory`, `Near Line Cap`, `Unpointed Local References`, `Force-load
  References`, `Declared Sibling Calls`, and `Counterpart Coverage`.
- Empty sections print `none`; the script never suppresses a section, mutates a
  file, invokes another skill, or declares a semantic duplicate.

The audit workflow must use this command before model judgment. The model may
then classify reported items as retain, investigate with a deletion test, or
documented exception; it must not infer that a mechanical finding is safe to
remove.

### Amendment B — Bundle-parity rule

`audit-skills.sh` is a shared deterministic contract even though it is stored
once in each target bundle. The Claude Code and Codex copies must be byte-for-
byte identical. The implementation validation compares them with `cmp -s`.

The paired audit rubric and graph additions must be semantically equivalent.
Allowed differences are only platform invocation syntax, Codex
`agents/openai.yaml`, and required localized README language. Any other
workflow, safety gate, role-matrix, or deletion-test difference must be called
out in the implementation report with a reason.

### Amendment C — Revised validation steps

Add these checks to the Validation Plan before `bash scripts/validate.sh`:

```bash
bash claude-code/skills/ywc-skill-author/scripts/audit-skills.sh \
  --root claude-code/skills --counterpart-root codex/skills
bash codex/skills/ywc-skill-author/scripts/audit-skills.sh \
  --root codex/skills --counterpart-root claude-code/skills
cmp -s \
  claude-code/skills/ywc-skill-author/scripts/audit-skills.sh \
  codex/skills/ywc-skill-author/scripts/audit-skills.sh
```

Also test the invalid-path exit-2 behavior and one fixture for each non-empty
report section. Run the existing per-skill authoring validator after the new
reference/script/README/eval assets are present, so the audit feature itself
obeys the same resource and pointer rules it audits.
