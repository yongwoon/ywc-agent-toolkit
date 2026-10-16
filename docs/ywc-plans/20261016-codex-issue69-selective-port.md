# Codex selective adoption of develop-with-llm issue #69

> Status: Ready for task generation — implementation has not started
> Scale: Large — three delivery stages across the planning, review, and delivery workflow
> Created: 2026-10-16 (Asia/Tokyo)
> Baseline revision: `614096d3` (`1.38.0`)
> Input: [develop-with-llm issue #69](https://github.com/yongwoon/develop-with-llm/issues/69) and the preceding selective-adoption review
> Document language: English, from project `.codex/ywc.json` (`lang: en`)

## Purpose

Improve the existing Codex workflow by adopting upstream changes that close verified local gaps: incomplete spec-review monitoring, omitted requirements and verification paths, redundant confirmations, and weak review evidence. Reuse the toolkit's existing contracts rather than importing the upstream bundle or its release history.

**What:** Deliver the selected Codex contract improvements in three separately reviewable PRs.
**Why:** Prevent stalled reviews, silently omitted requirements, and unnecessary interaction while keeping evidence and authorization checks intact.
**Done When:** AC-1 through AC-10 pass, each stage has its stated regression evidence, generated packaging matches source, and implementation review has no unresolved Critical/High findings. Creating or merging PRs requires a subsequent execution request; this planning invocation writes this document only.

**Outcome Oracle:** A spec-review run resolves unavailable reviewers honestly; task generation exposes unmapped requirements; advisory-only Suggestions do not create another approval loop; and PR/test/review outputs carry relevant, verified evidence. Evidence consists of focused contract regressions, structural validation, install checks where applicable, and explicitly labeled behavioral observations. Static fixture success alone does not prove live model behavior.

## Scope

| Stage | Adopted upstream work | Local adaptation |
|---|---|---|
| 1: review monitoring | PRs #241, #252 (Codex portion), #267 | Event-aware reconciliation and a read-only spec-review availability gate |
| 2: omission and traceability | PRs #257, #260, #268, selected #282 changes | Conditional UI/security lenses, Failure Modes, generation-time coverage, interface checks, and AC-to-verification links |
| 2 dependency | PR #259, absent from the issue's list | Bring the security lens definition with its consumers; no dangling cross-skill reference |
| 3: interaction and evidence | Selected PRs #266, #258, #262, #263 | Bounded Suggestion handling, removal of duplicate confirmations, optional PR Impact, SDK verification, and narrow trigger corrections |

The stage boundaries are delivery gates, not permission to implement the deferred items below. PR numbers identify upstream intent; source paths and behavior in this document define the local implementation.

## Out of Scope

- Claude Code skills, agents, hooks, `ScheduleWakeup`, or named-teammate `TaskStop` release logic (#235, #290, #294).
- Re-porting already present work: shared-asset installation and read-only agent contracts (#234), task-size guidelines (#236), monorepo references (#238), mobile-first wiring (#239), trusted executable resolution (#244).
- Evidence collectors/script extraction (#240), new agentic handoff or run-lock machinery and evaluator migration (#279), Fastify scaffolds (#251), screenshot publishing (#283), model routing/install recovery (#288), executor router/nested-PR discovery (#289), Docker Compose authoring (#293), and incident-document maintenance (#295).
- Config-key expansion (#237), full SCS/Use Case/Entity profiles, a new `--criticality` propagation surface, and initializer guidance from #282. These require separate plans if later selected.
- Importing upstream scorecards, task archives, release metadata, historic model pins, or unrelated application changes.
- New runtime dependencies, database changes, network services, and broad prompt cleanup. Do not change version/release metadata during implementation unless a separate release operation requests it.

## Global Constraints

The following constraints are quoted from repository guidance:

- "For Codex skills, `codex/skills/` is the source of truth. The marketplace package under `plugins/ywc-agent-toolkit/skills/` is generated from it by `bash scripts/sync-codex-plugin.sh`; do not edit the generated package first." — `codex/AGENTS.md`
- "Codex `SKILL.md` frontmatter must contain only those two fields; do not copy Claude-only fields such as `version`, `category`, or `requires`." — root `AGENTS.md` (`name` and `description`)
- "Shared Codex material belongs in `codex/skills/references/` or `codex/skills/scripts/`." — root `AGENTS.md`
- "Use portable Bash for scripts with `set -euo pipefail`." — root `AGENTS.md`
- "There is no package test runner. Treat `bash scripts/validate.sh` as the required pre-PR test." — root `AGENTS.md`
- "Use `CLAUDE_SKILLS_DIR` and `CODEX_HOME` to test installs in temporary directories before touching real user skill folders." — root `AGENTS.md`

Each changed skill retains its Tier 1 READMEs and `agents/openai.yaml`; maintain existing Tier 2 locales when behavior-facing documentation changes. Existing description-length checks still apply. Generated package changes are allowed only as output of source synchronization. Shared validation may be extended for Codex without changing Claude Code behavior.

## Quality Gate Contract

N/A — no quality gate contract. This change concerns Markdown contracts and bounded regression checks; it does not introduce a CRAP/mutation gate or dispatch write-enabled Cleaner/Hardener agents. Use the verification matrix below.

## Module Boundaries

| Owner | Responsibility and public contract | Consumers / dependency direction |
|---|---|---|
| `references/subagent-async-monitoring.md` | Canonical target attribution, event processing, liveness, bounded escalation, and quiescence | Spec/implementation review and executors consume it; consumer fallbacks do not redefine liveness |
| `references/subagent-status-actions.md` | Terminal-status actions and bounded read-only return exception | Spec/implementation review consume it; no new status vocabulary |
| `ywc-plan` and `ywc-spec-validate` | Failure Modes and conditional omission checks | Produce/check spec evidence consumed by task generation |
| `ywc-task-generator` | Requirements-to-task mapping, owned-interface compatibility, and verification references | Reuses spec evidence; does not execute a task's verification commands |
| `ywc-spec-ready`, `ywc-plan`, `ywc-agentic` | Consistent Suggestion policy and existing handoff/preview contracts | Callers propagate policy; task-generator remains owner of preview validation |
| `ywc-create-pr`, `ywc-gen-testcase`, `ywc-impl-review` | Conditional Impact, security scenarios, and SDK-source verification | Consume existing diff/context and lens references; no extra broad collection phase |
| Existing evals, `scripts/`, `tests/` | Deterministic contract checks and clearly labeled behavioral evidence | Validate source; `sync-codex-plugin.sh` generates package output |

Paths in this table are relative to `codex/skills/` unless explicitly rooted elsewhere. No architecture-advisor delegation is needed: existing ownership determines the design; no new service/module boundary is introduced.

## Existing Constraints Touched

Line anchors refer to the baseline revision and must be rechecked before edits.

| Baseline evidence | Verified behavior | Planned interaction |
|---|---|---|
| `codex/skills/references/subagent-async-monitoring.md:16` | Dispatch records retain a returned canonical target; missing identity is non-terminal | Preserve attribution; never derive identity from a requested label |
| `codex/skills/references/subagent-async-monitoring.md:44` | Event-first processing currently asks for complete-roster reconciliation | Permit skipping a redundant query under FR-1; retain final complete-roster proof |
| `codex/skills/references/subagent-async-monitoring.md:61` | Existing worker threshold is 600 seconds; heartbeats are at most 60 seconds; request/interrupt are bounded | Reuse these limits; no second escalation algorithm |
| `codex/skills/references/subagent-status-actions.md:14` | Inline read-only exception names eight reviewer/advisor agents | Extend to explicitly designated spec-review workers without granting artifact writes |
| `codex/skills/ywc-spec-validate/SKILL.md:74` | Four dimensions run with delegation, with inline fallback when delegation is absent | Add availability handling before aggregation; keep all four dimensions |
| `codex/skills/ywc-spec-validate/SKILL.md:100` | `--tasks` already checks requirement coverage and task provenance | Reuse this vocabulary; extend generation-time checks rather than create a competing model |
| `codex/skills/ywc-impl-review/SKILL.md:168` and `:233` | Read-only Phase 1 output and possibly-live precedence already exist | Preserve the implementation-review policy; spec direct fallback is a separate consumer policy |
| `codex/skills/ywc-task-generator/SKILL.md:73` | Approved preview consumption requires matching identity/revision/digest; preview-only cannot write tasks | Preserve these checks and write boundaries |
| `codex/skills/ywc-task-generator/SKILL.md:427` and `:458` | Final validation includes structure/consistency checks | Add explicit completeness and interface checks at this existing boundary |
| `codex/skills/ywc-spec-ready/SKILL.md:18`, `:92`, `:144` | Suggestions currently require a user decision; the non-interactive apply path can return missing-policy status again | Replace these duplicated policies together under FR-5 |
| `codex/skills/ywc-plan/SKILL.md:364`; `codex/skills/ywc-agentic/SKILL.md:58`, `:130`, `:157` | Planner handoff and agentic preflight restate the current Suggestion decision | Update the caller-facing policy with its owner; do not leave stale instructions |
| `scripts/run-codex-skill-contract-evals.sh:94` | Existing preview/agentic assertions cover the protected handoff shape | Extend relevant assertions and fixtures; retain negative cases |
| `codex/skills/ywc-create-pr/SKILL.md:203`, `:230` | Author review has already read the diff before PR body generation | Reuse that evidence for Impact |
| `codex/skills/references/shared-script-resolution.md:3` | Trusted executable resolution is already defined | No new resolver or target-relative executable fallback |
| `tests/install-shared-assets-test.sh:3`; `scripts/validate.sh:886` | Real installation smoke coverage is already available | Reuse it for newly introduced references |
| `codex/skills/references/context-handoff.md:3` | Executor handoff is a non-authoritative reconstruction cache | No change; do not introduce #279's second handoff mechanism |

## Acceptance Criteria

| ID | Trigger and observable result | FR / verification |
|---|---|---|
| AC-1 | When an attributable terminal notification provides target and status, the monitor can process it without an immediate redundant roster call; ambiguity and final batch closure still require complete reconciliation | FR-1; M1/M2 |
| AC-2 | When a spec-review lane remains possibly live, the result is `BLOCKED` with monitoring evidence and no aggregation/direct fallback; when quiescence is proved, one parent review covers that dimension and records degraded provenance | FR-2; M1/M2 |
| AC-3 | When a spec touches UI or a defined security boundary, validation records the applicable omission lenses and findings; an unrelated spec receives no fabricated UI/security requirements | FR-3; O1 |
| AC-4 | When an AC, FR, or Failure Modes row has no task, generation reports its ID as uncovered and cannot emit clean `DONE`; agentic stops before preview consumption or executor dispatch on unresolved coverage; an incompatible consumed interface is reported with both producer/consumer evidence | FR-4; O2 |
| AC-5 | When task/test artifacts are generated, each applicable AC is linked to a verification location; a claimed command baseline has actual recorded evidence or an explicit unmeasured gap, and no untrusted command is executed by spec validation | FR-4; O2/O3 |
| AC-6 | When Suggestions are the remaining findings, default handling performs at most one amendment/revalidation; residual advisory Suggestions alone do not cause another policy prompt or `NEEDS_CONTEXT: --suggestions` | FR-5; I1 |
| AC-7 | When a matching preview already has approval evidence, consume proceeds without duplicate confirmation; unapproved or stale previews never gain approval through this change, and preview-only writes no tasks | FR-6; I2 |
| AC-8 | When a diff changes observable behavior, PR generation adds concise localized Impact evidence without re-fetching the diff; relevant security test scenarios use the same security lenses | FR-7; E1 |
| AC-9 | When a review relies on SDK exception inheritance, it cites version-relevant primary evidence or exposes the uncertainty; six bounded Codex selection trials choose the expected skills at the inspected revision, with all six observations recorded and existing description limits satisfied | FR-8; E2 |
| AC-10 | When each stage is packaged, generated Codex content matches source, required metadata/locales remain, focused checks and `bash scripts/validate.sh` pass, and Claude Code source has no changes | FR-9; P1 |

## Functional Requirements

### FR-1: Event-aware monitoring (AC-1)

Update the canonical monitoring reference and the parallel-executor consumer wording. Skip an immediate roster query only when a notification is attributable to a captured dispatch, parseable, and contains a terminal status. Process delivered events first; retain elapsed-time tracking for other outstanding targets. Ambiguous, target-mismatched, malformed, or status-less messages remain non-terminal. At batch closure perform complete reconciliation; a missing entry alone is never proof of completion. Preserve the 600-second worker threshold (elapsed >= 600 seconds), heartbeat <= 60 seconds, and one-request/one-interrupt guard per dispatch.

### FR-2: Spec-review availability gate (AC-2)

Wire `ywc-spec-validate` to the shared monitor before aggregate/Phase 2 processing. Extend the shared read-only exception to these dimension workers: canonical identity, Status, one-line Summary, up to five confirmed findings and two advisor candidates, plus applicable bounded concern/blocker/context fields. No artifact write or promised artifact is allowed.

A possibly-live lane blocks ordinary aggregation, reporting, and downstream handoff. For a lane proved quiescent but unavailable, the parent reviews that dimension exactly once using the same spec/context/rubric, then records target, elapsed time, final roster state, evidence category, and direct-review result. A resulting `DONE` may be valid only with an explicit degraded-coverage label; never manufacture a worker terminal result. Failed dispatch or missing identity follows existing failure handling and cannot be treated as quiescent absence. Existing no-delegation inline review remains available and is reported separately.

### FR-3: Conditional omission lenses (AC-3)

Add `ywc-spec-validate/references/ui-qa-lenses.md` and `security-qa-lenses.md` with bounded trigger/check tables. UI checks cover round-trip fidelity, loading/empty/error, optimistic updates, IME composition, and keyboard accessibility where applicable. Security checks cover authentication, authorization/IDOR, input validation, secrets, rate limits, sensitive output, CSRF, and file/path handling where triggered. Report applicability and missing observable requirements; do not invent product requirements for unrelated surfaces. Wire both references into validation and the security reference into testcase generation.

### FR-4: Failure modes and requirement traceability (AC-4, AC-5)

Extend `ywc-plan/SKILL.md` and `references/spec-template.md` with Failure Modes rows: ID, triggering path, observable failure, handling/detection, and verification. Missing handling plus missing detection/test evidence is an explicit gap, never a silent pass. Legacy specs without this section remain valid; check rows when present.

Task generation checks ACs, FRs, and present Failure Modes rows against tasks. Use `COVERED`, `DEFERRED_WITH_REASON`, and `UNCOVERED`, consistent with existing spec validation. Any uncovered or deferred in-scope requirement prevents clean `DONE`, is listed by ID under `DONE_WITH_CONCERNS`, and is not silently reclassified as out of scope. The implementer may add a task within approved scope to close a gap. Each task records covered AC IDs and associated verification files/scenarios; existing tests may use a documented mapping when inline AC comments are inappropriate.

In the same Stage 2 change, `ywc-agentic` must check the existing task-generator terminal `Status` and its coverage summary immediately after **each** preview-only and approved-preview consume call. The bounded summary reports the counts of covered, deferred-in-scope, and uncovered requirements plus deduplicated unresolved requirement IDs, attributable to that call's spec and preview identity. It is report evidence, not a checkpoint field or a planner/ready `Result` schema extension. Continue only on `DONE` with zero deferred-in-scope and uncovered requirements and no contradictory IDs. An attributable non-`DONE` status propagates unchanged and preserves the existing artifacts; missing, malformed, contradictory, or mismatched coverage/status evidence is `BLOCKED`. An unresolved preview result permits zero consume calls; an unresolved consume result permits zero executor calls. Do not mark tasks complete or begin execution to repair generation-time coverage. Repair returns to the existing spec/task preparation path within approved scope; no automatic execution is authorized.

When a dependency explicitly defines an owned public interface, compare consumed names/signatures to that declaration and report mismatches. Do not invent an interface for a prose-only legacy dependency; record missing contract evidence if correctness depends on it. Absorb incidental setup/config/docs into the owning deliverable while preserving mandatory separate library-introduction and DB-migration tasks.

Command-bearing ACs record observed baseline, revision/context, and evidence, or explicitly state `not measured` with the gap. Validation is read-only: it inspects recorded baseline evidence and does not execute commands copied from a spec. Existing command-execution capabilities elsewhere are unchanged. QA implementation review consumes AC-to-verification mapping to identify unverified requirements; no new criticality flag is introduced.

### FR-5: Bounded Suggestion policy (AC-6)

Make `ywc-spec-ready` the owner of the policy. Preserve explicit `--suggestions apply|defer`; explicit user instructions take precedence. With no explicit policy and no Critical/Warning findings, attempt one Suggestion-focused amendment and revalidate once in either interactive or non-interactive mode. Explicit `defer` records the deferral against the valid reviewed artifact and performs no amendment. Suggestions remaining after the single apply pass are reported as advisory and handed off without a second Suggestion pass or policy prompt.

If revalidation introduces Critical/Warning findings, route through the existing bounded blocking-finding convergence policy; never hand off as ready. Missing/malformed validation evidence retains its existing failure status. Invalid explicit policy values remain `NEEDS_CONTEXT`. Update planner handoff text, agentic argument/preflight/propagation, references, examples, and eval expectations that encode the replaced policy. Do not change agentic Result parsing or artifact-authority rules.

### FR-6: Remove duplicate confirmations within preview authority (AC-7)

Apply #266 narrowly: do not reconfirm an already approved, unchanged preview. Preserve `--preview-only`, explicit `--approve-preview`, path containment, identity/revision/digest matching, and consume-only semantics. This change never auto-approves a newly generated preview and does not treat the task-generation request alone as evidence approving its concrete contents. Existing language, granularity, initials, and genuine ambiguity resolution remain. Make caller wording and preview evals agree with this boundary.

### FR-7: Impact and security scenario evidence (AC-8)

Add an optional localized Impact block for observable behavior changes, containing affected scope and concrete Before/After behavior. Reuse already-read diff evidence, respect repository PR templates, and omit the block when there is no behavior change. Do not modify PR publishing authority or add screenshot operations. Testcase generation adds a negative-path scenario for each triggered security lens, deduplicating overlapping scenarios. Keep the Codex input-acquisition design: do not add unconditional PR-body fetching solely to import Impact text.

### FR-8: Verified review evidence and narrow trigger corrections (AC-9)

Add SDK exception-hierarchy verification to the Devex review reference and verification methodology. SDK-specific findings cite the inspected version's source or official error reference; absent verification is uncertainty, not a confirmed assertion based on an inline comment.

For #263, limit trigger remediation to three collision pairs: technical comparison versus product/business ROI; security threat modeling versus product risk review; implementation conformance review versus code generation. Preserve each existing positive trigger and test paired positive/negative prompts. Strengthen product findings to drop unsupported conclusions rather than invent evidence. Retain the existing evaluator location/schema and description-length ceiling; do not import upstream agent types absent from this toolkit.

PR 3 requires one bounded observed Codex selection trial for each prompt below, using the changed toolkit revision and recording the prompt, actual selected skill, expected skill, source revision, and relevant installed catalog identity. Use a manual Codex session or an available live harness; stop after skill selection and before the requested implementation, security audit, or publishing operation executes. A static source check or prewritten fixture is not an observed trial. All six selections must match; an unavailable trial or mismatch leaves AC-9 unmet and prevents a clean implementation completion claim. Record bounded observations without credentials or full transcripts. These checks do not require adding a live provider to CI.

| Trial | Prompt | Expected skill |
|---|---|---|
| T1 | Compare implementation libraries and their technical trade-offs before writing a spec. | `ywc-tech-research` |
| T2 | Assess whether this feature is worth building for the business, including user value and ROI. | `ywc-product-review` |
| T3 | Threat-model this existing authenticated file-upload implementation and its trust boundaries. | `ywc-security-audit` |
| T4 | Review the product's adoption and monetization risks. | `ywc-product-review` |
| T5 | Check whether this completed implementation conforms to its approved specification. | `ywc-impl-review` |
| T6 | Generate Backend, Frontend, and QA layers in parallel from this approved specification. | `ywc-code-gen` |

### FR-9: Distribution and validation (AC-10)

Update affected skill evals and usage documentation with behavior changes. Extend the existing contract runner for structural/negative assertions; store bounded scenario fixtures under `tests/fixtures/codex-issue69/` and a focused runner at `tests/codex_issue69_contract_test.py` if reusable deterministic checks require one. Wire this runner into `scripts/validate.sh` so CI's existing entry point executes it. Use stdlib Python; it must inspect trusted source/fixtures without invoking an LLM, shell snippets from specs, or network publishing.

Distinguish source assertions, predetermined fixture expectations, and observed live behavioral evidence in reports. No parser/replay harness may be presented as proof of autonomous runtime behavior. Synchronize the generated plugin after source edits and validate both temporary installation and package freshness.

## Implementation Sequence

These are work packages for later task generation, not allocated task IDs. Shared files are intentionally edited sequentially.

| Package | Delivery | Owned change | Depends on |
|---|---|---|---|
| W1 | PR 1 | Monitoring reference and read-only exception (FR-1/2) | Baseline |
| W2 | PR 1 | Spec availability gate and parallel consumer alignment | W1 |
| W3 | PR 1 | Monitoring regression scenarios, docs, package sync | W2 |
| W4 | PR 2 | UI/security lens references and spec wiring (FR-3) | PR 1 accepted |
| W5 | PR 2 | Failure Modes, task/interface coverage, agentic task-phase coverage gate, QA traceability (FR-4) | W4 |
| W6 | PR 2 | Omission/coverage regressions, docs, package sync | W5 |
| W7 | PR 3 | Suggestion policy and planner/agentic propagation (FR-5) | PR 2 accepted |
| W8 | PR 3 | Duplicate-confirmation boundary and preview regressions (FR-6) | W7 |
| W9 | PR 3 | PR Impact and testcase security scenarios (FR-7) | W8; W4 security lenses |
| W10 | PR 3 | SDK evidence and three trigger collision pairs (FR-8) | W9 |
| W11 | PR 3 | Integration regressions, documentation, package sync | W10 |

Potential PR descriptions: `fix: harden Codex spec review monitoring`; `feat: trace Codex spec requirements through verification`; `fix: streamline Codex approvals and review evidence`. Split a package further if task ownership cannot be made exclusive; do not expand scope to fill a phase.

### Planned Files

- PR 1: `codex/skills/references/{subagent-async-monitoring,subagent-status-actions}.md`, `ywc-spec-validate/SKILL.md`, `ywc-parallel-executor/SKILL.md`, affected evals and READMEs.
- PR 2: `ywc-spec-validate/references/{ui-qa-lenses,security-qa-lenses}.md` (new), its `SKILL.md`; `ywc-plan/{SKILL.md,references/spec-template.md}`; `ywc-task-generator/{SKILL.md,references/README.md.template,references/task.md.template}`; `ywc-agentic/SKILL.md` (task-phase coverage boundary); `ywc-impl-review/references/qa-agent.md`; affected evals and READMEs.
- PR 3: `ywc-spec-ready/SKILL.md`, its convergence reference if the replaced policy is present there, `ywc-plan/SKILL.md`, `ywc-agentic/SKILL.md`, `ywc-task-generator/SKILL.md`; `ywc-create-pr/SKILL.md`, `ywc-gen-testcase/SKILL.md`; `ywc-impl-review/references/{devex-agent,coderabbit-methodology}.md`; `ywc-{tech-research,product-review,security-audit,code-gen,impl-review}/SKILL.md` where the selected trigger boundary needs correction; affected evals and READMEs.
- Each PR: focused test fixtures/runner as needed, `scripts/run-codex-skill-contract-evals.sh`, narrowly scoped validation wiring, and generated `plugins/ywc-agent-toolkit/skills/` output.

Skill paths after the first full path in each bullet are relative to `codex/skills/`. A listed candidate is not permission for unrelated edits; before implementation, inspect its exact consumer wording and omit files already satisfying the requirement.

## Verification

| ID | Scenarios / evidence | Expected outcome |
|---|---|---|
| M1 | Attributable terminal; malformed/status-less/target-mismatched payload; ambiguous notification; final batch reconciliation | No redundant immediate query for complete terminal events; attribution and full closure remain required |
| M2 | Quiescent unavailable; possibly live; monitoring API error; completion during escalation; missing canonical target; no delegation tool | One parent fallback only with quiescence proof; possibly-live blocks; late valid terminal event wins; no fabricated success |
| O1 | UI spec; auth/upload spec; unrelated documentation spec; legacy spec without Failure Modes | Applicable lenses checked; irrelevant lenses skipped; no new mandatory legacy section |
| O2 | Unmapped AC/FR/failure row; justified deferral; incompatible declared signature; existing tests without inline IDs; preview/consume coverage non-DONE, absent, contradictory, or identity-mismatched | Gaps visible by ID, no clean DONE for gaps; unresolved preview allows zero consume calls and unresolved consume allows zero executor calls; malformed evidence blocks; actionable signature finding; mapping fallback accepted |
| O3 | Recorded baseline; unmeasured baseline; spec containing destructive/network command text | Recorded evidence checked; gap explicit; command text is never executed |
| I1 | No Suggestions; default single pass; explicit apply/defer; residual Suggestions; new Warning; malformed validation | No extra policy loop; explicit override honored; blocking findings and invalid evidence retain failure routing |
| I2 | Matching approved preview; new unapproved preview; changed digest/revision; escaping path; preview-only | Existing approval accepted once; no implicit approval; stale/unsafe inputs rejected without task writes |
| E1 | Behavior diff; docs-only diff; repository template; overlapping security lenses | Relevant localized Impact/scenarios, no redundant broad diff query, no duplicate scenarios |
| E2 | Verified SDK inheritance; unsupported SDK comment; observed Codex selections T1–T6 at the changed revision | Verified finding or explicit uncertainty; six of six observed selections match, otherwise AC-9 remains unmet; no description-length regression |
| P1 | Source assertions, fixture suite, metadata/locales, temp install, plugin freshness | Required checks pass; evidence types reported honestly; no Claude Code source changes |

Implementation commands, after source edits and package synchronization:

```bash
python3 tests/codex_issue69_contract_test.py
bash scripts/run-codex-skill-contract-evals.sh
bash scripts/check-codex-skill-descriptions.sh
bash scripts/check-codex-agent-evals.sh
bash scripts/sync-codex-plugin.sh
bash scripts/validate.sh
bash scripts/install.sh --list --codex
```

The first command becomes required when FR-9 creates/wires the runner. `scripts/validate.sh` already runs installed-asset coverage; repeat individual install checks only if packaging failures need diagnosis. Install only into a temporary `CODEX_HOME`. A representative delegated review observation is desirable after PR 1; if unavailable, report that gap and do not label static evidence as a live pass. The six PR 3 selection observations under FR-8 are mandatory acceptance evidence, run separately from these offline commands. If the observation environment is unavailable, report AC-9 as unverified and do not claim implementation complete.

## Non-Functional Requirements

- Keep long lens/scenario details in references and tests; inline only the action and blocking precedence needed for reliable execution.
- Do not add a network request, repeated broad diff/context read, or model call to mechanical verification.
- Do not claim token/latency improvement without measurements. Script-extraction performance work remains deferred.
- Keep status vocabulary, canonical identity, preview protection, and trusted executable boundaries compatible with the existing bundle.
- Retain locale metadata and readable instruction examples. No user-facing application UI or responsive-layout change is involved.

## Data Model

N/A — no application schema or persisted executor-state migration. Coverage tables, lens references, and scenario fixtures are documentation/test contracts. Do not add checkpoint fields or change the handoff wire schema.

## API Contract

N/A — no application HTTP API or new CLI flag. Existing `--suggestions`, preview, and planner/ready Result schemas remain; FR-5 changes default Suggestion policy and FR-6 preserves approval identity semantics. FR-4 adds a bounded task-generator coverage report alongside its existing terminal Status, consumed by agentic without modifying the closed planner/ready Result schemas.

## Edge Cases

- Terminal evidence arriving during escalation wins before fallback; a roster status alone does not fabricate a missing worker payload.
- A generic spec reviewer is read-only even if its parent can write; parent direct review never impersonates the absent worker.
- A spec can legitimately lack UI, security, or Failure Modes content; applicability and legacy compatibility must be distinguished from an omitted applicable requirement.
- A Suggestion amendment can introduce a Warning; the single Suggestion-pass limit does not waive blocking-finding convergence.
- A policy change does not authorize scope expansion, implicit preview approval, automatic implementation, or publishing.
- Shared files such as `ywc-plan/SKILL.md` and contract evals are edited in more than one stage; later stages must rebase onto accepted earlier stages.

## Failure Modes

| ID | Failure | Handling / visibility | Verification |
|---|---|---|---|
| FM-1 | Query-skip rule hides another outstanding reviewer | Continue outstanding-target timing; reconcile ambiguous signals and final batch | M1/M2 |
| FM-2 | Stalled reviewer is treated as successful absence | Possibly-live blocks; direct review requires complete quiescence evidence | M2 |
| FM-3 | New security consumer references an absent lens file | Ship #259's lens with consumers; validate installed reference resolution | O1/P1 |
| FM-4 | Coverage reports success while dropping a requirement | Enumerate AC/FR/present failure rows; report each uncovered/deferred in-scope ID | O2 |
| FM-5 | Baseline guidance executes a command supplied by a spec | Spec validation only reads recorded evidence | O3 |
| FM-6 | Old planner/agentic instructions restore the removed Suggestion prompt | Reconcile owner and caller prose/evals in one PR | I1 |
| FM-7 | Removing confirmations bypasses digest/approval checks | Keep identity/authorization negatives in the same regression suite | I2 |
| FM-8 | Fake fixtures are reported as runtime model success | Label structural, fixture, and live evidence separately | P1/report inspection |
| FM-9 | Source changes leave the marketplace package stale | Generate package and run existing freshness validation | P1 |

## Dependencies and Rollback

No new dependency installation is planned. Stage 2 depends on accepted Stage 1; Stage 3 depends on accepted Stage 2. Stage 2 security lens definitions precede Stage 3 testcase consumption. Stage 2 ships generation-time coverage and its agentic consumer gate atomically. Stage 3 changes the Suggestion owner and its callers atomically. Observed selections require an available Codex session or live harness at PR 3 acceptance time; this is separate from offline CI and must not be silently waived.

Rollback a stage by reverting its source, matching eval/documentation changes, and regenerating the package from the reverted source. Do not revert only the generated package or only a policy owner while leaving its callers on a new contract. No runtime data migration is required.

## Planning Readiness and Self-Consistency

Confidence scorer result: **93/100 — PROCEED for the planning handoff**, not authorization to implement. Scope 95 (selected/deferred upstream matrix), architecture 94 (existing contract ownership), evidence 90 (current source and upstream changes inspected; no live run yet), reuse 94 (existing monitor/coverage/preview/evaluator retained), root cause 92 (missing wiring and duplicated policy identified). Each implementation task must reassess readiness at its narrower boundary.

Blind Spot Pass: The assumption most likely to invalidate a literal port is that upstream approval and monitoring contracts match this repository. Current preview identity and canonical-target evidence disproved that assumption; FR-1/2/6 explicitly adapt those boundaries. This does not depend on a new architecture choice.

Self-consistency: Pass A maps AC-1..10 to FR-1..9 and verification IDs above; no orphan requirement. Pass B uses baseline source anchors and preserves existing monitoring, preview, and handoff authority; excluded upstream work stays excluded. Pass C is N/A after checking that no DB, application data model, or state-schema change is proposed. Independent four-dimension spec validation converged after one amendment and two validation iterations (0 Critical, 0 Warning, 0 Suggestion). Runtime implementation behavior remains unverified.

## Open Questions

N/A — no unresolved scope or design decision blocks spec review. Live delegated-review availability is an evidence gap to report during implementation, not a prerequisite for writing this plan. The six routing observations are explicitly required before implementation completion; unavailable evidence leaves AC-9 unmet rather than opening an implicit waiver. Later task granularity is selected when task generation is requested.

## Planning Artifact Checks

- Required sections, AC/FR identifiers, fenced blocks, filename convention, and referenced existing task templates: passed on 2026-10-16.
- `git diff --check`: passed.
- `bash scripts/validate.sh`: passed (`All checks passed.`), including existing executable-resolution, checkpoint/worktree, agent-installation, and installed-shared-assets regressions. This establishes the current baseline; it does not validate the unimplemented requirements above.
- Independent `ywc-spec-validate` review: `DONE` on validation iteration 2; 0 Critical, 0 Warning, 0 Suggestion; 0 of 4 total Phase 2 advisor calls used. Reports: `20261016-codex-issue69-selective-port.validation-1.md` and `20261016-codex-issue69-selective-port.validation-2.md`; append-only log: `20261016-codex-issue69-selective-port.spec-ready-log.md`. No task directories or implementation changes were created.

## Next Step

Spec validation has converged with `DONE`. Next, when task generation is requested, run `ywc-task-generator docs/ywc-plans/20261016-codex-issue69-selective-port.md`. Do not execute implementation or create task directories as part of this spec-readiness request.

## References

- [Upstream issue #69](https://github.com/yongwoon/develop-with-llm/issues/69), inspected 2026-10-16.
- Monitoring: [#241](https://github.com/yongwoon/develop-with-llm/pull/241), [#252](https://github.com/yongwoon/develop-with-llm/pull/252), [#267](https://github.com/yongwoon/develop-with-llm/pull/267).
- Omission/coverage: [#257](https://github.com/yongwoon/develop-with-llm/pull/257), [#259](https://github.com/yongwoon/develop-with-llm/pull/259), [#260](https://github.com/yongwoon/develop-with-llm/pull/260), [#268](https://github.com/yongwoon/develop-with-llm/pull/268), [#282](https://github.com/yongwoon/develop-with-llm/pull/282).
- Interaction/review evidence: [#266](https://github.com/yongwoon/develop-with-llm/pull/266), [#258](https://github.com/yongwoon/develop-with-llm/pull/258), [#262](https://github.com/yongwoon/develop-with-llm/pull/262), [#263](https://github.com/yongwoon/develop-with-llm/pull/263).
- Optimization trust boundary: [issue #242](https://github.com/yongwoon/develop-with-llm/issues/242), fixed by [PR #244](https://github.com/yongwoon/develop-with-llm/pull/244); existing local hardening plan: `docs/ywc-plans/20260919-codex-executable-resolution-hardening.md` (historical context, not an inherited scope specification).
- Repository constraints and verified local contracts are listed under Existing Constraints Touched; upstream field names/paths are not authoritative for local implementation.

## Amendment Log

### Iteration 1 — 2026-10-16

- Driven by: validation-1 Warning W1 (observed routing evidence), Warning W2 (agentic coverage consumer), and Suggestion S1 (stage wording).
- Signatures: `feasibility:routing-observation-evidence`; `code-compatibility:agentic-coverage-gate`; `consistency:security-lens-stage-order`.

| Section edited | What changed | Why |
|---|---|---|
| Acceptance Criteria | AC-4 includes downstream blocking; AC-9 requires six observed selections | Replaces output-only coverage and unproven routing claims |
| FR-4: Failure modes and requirement traceability (AC-4, AC-5) | Defines bounded coverage report and agentic checks after both generation calls | Existing task phase lacked a gate before executor selection |
| FR-8: Verified review evidence and narrow trigger corrections (AC-9) | Names T1–T6 prompts, expected skills, and mandatory bounded observations | Static schema/token checks cannot prove actual selection |
| Implementation Sequence / Planned Files | W5 and PR 2 include the agentic task-phase gate | Producer and consumer must ship together |
| Verification | O2 tests zero downstream calls; E2 requires six observations; separates offline and observed evidence | Previous checks could pass without proving the AC |
| API Contract | Distinguishes new task-generator report from unchanged planner/ready schemas | Prevents widening a closed Result schema accidentally |
| Dependencies and Rollback | Corrects Stage 2/3 security ordering and names atomic coverage wiring | Removes inconsistent stage wording and unsafe partial delivery |
| Open Questions | Records unavailable routing evidence as unmet AC-9 | Evidence is required, not an implicit exception |

### Validation closure — 2026-10-16

- Driven by: validation iteration 2, all four dimensions returned no confirmed findings.
- Signatures: `validation:ready-metadata`.

| Section edited | What changed | Why |
|---|---|---|
| Status metadata | Draft becomes ready for task generation | All blocking findings were repaired and independently revalidated |
| Planning Readiness and Self-Consistency | Records completed validation, preserving the runtime evidence limitation | Replaces stale pending-review text |
| Planning Artifact Checks | Records the final result and report/log paths | Keeps verification provenance auditable |
| Next Step | Points to task generation without executing it | Readiness workflow stops at the handoff |
