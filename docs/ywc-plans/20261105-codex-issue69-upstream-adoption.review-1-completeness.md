# Completeness review — Issue 69 Codex spec

Status: DONE_WITH_CONCERNS
Critical: 1, Warning: 3, Suggestion: 0
Spec: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md
Local source revision: 42664d667fdb58ae45a35b6b000515515f6c5907
Outcome Oracle: complete (Target, Quality threshold, Evidence required, Stop condition present at lines 14–19).
Blind Spot action: read-more, resolved locally: current orchestration has an interactive caller that owns readiness; source inspection exposes an omitted integration site.

## C-1 — Critical — Completeness — interactive agentic planner caller omitted from convergence opt-out contract

- Target: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md:162 (FR-10).
- Evidence: codex/skills/ywc-agentic/SKILL.md:118 invokes `ywc-plan [--non-interactive] --artifact-profile agentic`; `--non-interactive` is forwarded only when received. Lines 128–131 separately invoke `ywc-spec-ready` on Medium/Large. This site is absent from FR-10's concrete change list at line 161 and Module Boundaries. A generic instruction to investigate other callers does not close the named integration contract.
- Failure: interactive agentic begins readiness within plan, then runs its own readiness again; producer Result ownership may be confused by child output. The explicit auth-only opt-out is insufficient.
- Improvement: name `codex/skills/ywc-agentic/SKILL.md` as an FR-10 consumer; require `--no-converge` for initial planner invocation whenever agentic owns readiness, independent of `--non-interactive`, preserve `--artifact-profile agentic` Result contract, and add an interactive agentic call-count regression.
- Clarifying question: Should agentic retain sole readiness ownership? Current source says yes, so this is repository-resolvable.

## W-1 — Warning — Completeness — Brownfield baseline revisions absent

- Target: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md:23 (PR 검토 및 채택 결정) and line 139.
- Evidence: the 13 sources are mutable PR URLs and prose “최종 diff/#348 merge 시점”, without source SHA/content digest. Current local constraints also omit inspected checkout SHA. The validator's Brownfield Integrity rule requires bounded source evidence and a known source revision.
- Failure: later implementation cannot distinguish the reviewed #348 Mission baseline from later upstream changes, nor reproduce the exact imported behavior after a PR branch changes.
- Improvement: record each adopted PR's immutable merge SHA (or frozen patch/content digest) and local source revision; name exact upstream source paths for new Mission/Retro/Handoff and explicit approved/deferred decision state. Existing PR matrix can be extended rather than duplicated.
- Clarifying question: Which immutable snapshots define the approved port? Fetchable from reviewed PR metadata.

## W-2 — Warning — Completeness — test evidence destinations and executable gates unspecified

- Target: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md:205 (Verification).
- Evidence: FRs repeatedly request “관련 eval 수정”, and AC-6/AC-9 demand worker-call-count/push/cwd/polling observations, but listed commands only have current structural checks. `scripts/run-codex-skill-contract-evals.sh:214` explicitly reports structurally valid; agent checker is jq/shape assertions. The spec distinguishes live from static but does not say where new stub/Git scenario runners reside or which command gates their execution. `tests/codex_issue69_contract_test.py` currently compares fixture clauses, not worktree operation traces.
- Failure: task generator can assign eval JSON updates as satisfying AC-6/9 while required non-model Git/stub checks never execute in the mandated verification sequence.
- Improvement: assign concrete new/extended test/fixture paths and runner command(s) for behavioral Git/stub checks, connect them to `scripts/validate.sh` or explicitly required command list, map AC groups to source assertions vs executable stubs vs optional live. Runtime remains optional UNVERIFIED; deterministic Git/stub tests are required.
- Clarifying question: Which local gate must fail when these deterministic scenarios regress? Select an existing test entry point or add an explicit bounded one.

## W-3 — Warning — Completeness — Retro contract refers to seven categories without defining them

- Target: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md:118 (FR-4).
- Evidence: neither FR-4 nor AC-4 names the seven categories; HIGH/MEDIUM/LOW are not defined and tie handling / unknown-owner behavior are absent even though AC-4 requires owner/ordering evaluation. #345 Codex source in inherited task evidence defines Navigation, Automated checks, Coding standards, Steering files, Tool economy, No-ops, Information access; owner fallback and priority/tie semantics are part of that source contract.
- Failure: three implementers can each choose different categories, ordering, and owner inference yet claim the prose and “7 categories” count pass.
- Improvement: enumerate the seven canonical categories, priority definitions, distinct-occurrence tie ordering, unknown-owner literal fallback, no-evidence result. Link the immutable upstream file as canonical where exact wording is lengthy.
- Clarifying question: Is the #345 Codex contract authoritative? The PR matrix says yes; no user decision needed.

## Precedent site coverage

| Site | Coverage |
|---|---|
| codex/skills/ywc-auth-implement/SKILL.md:40 planner then readiness | Replicated explicitly by FR-10 |
| codex/skills/ywc-agentic/SKILL.md:118 initial planner, :131 owned readiness | OMITTED: C-1 |
| codex/skills/ywc-spec-ready/SKILL.md:63 goal mode planner --non-interactive | Deferred-with-reason: FR-10 preserves noninteractive opt-out; unchanged |
| codex/skills/ywc-agentic/SKILL.md:136 Re-plan profile caller | Replicated by FR-10 Re-plan opt-out preservation |

## Omission lenses

UI: no end-user graphical UI introduced; lens set N/A. Remote deletion is a pre-existing authorized action guard rather than a new delete UI.
Security: input validation/path containment covered by FR-4/9; sensitive exposure covered by redaction and API path restrictions. No credential introduction or new HTTP auth boundary. Actor remains authorized local user; PR same-repo identity guard is stated.
Data integrity: handoff exclusive creation, worktree failure preservation, side-effect reporting and no destructive fallback are specified. Polling persistence schema may merit Code Compatibility/Feasibility investigation; not duplicated as a finding here.

Graft saved approximately 18,735 tokens in one call.
