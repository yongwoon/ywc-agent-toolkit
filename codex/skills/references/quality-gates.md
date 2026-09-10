# Quality Gate Contract for Codex Skills

> Shared reference document. This is the canonical source for opt-in quality-gate semantics used by planners, task generators, executors, workers, and implementation review.

## 1. Purpose and safety boundary

The Quality Gate Contract lets a caller carry bounded complexity and mutation evidence through the task lifecycle. It is opt-in: a task without a valid declaration keeps the existing verification and review workflow.

This reference defines metadata and routing decisions only. It never grants authority to emit, copy, or execute raw commands; retain raw command output, transcripts, secrets, or full diffs; or stage, commit, push, create a PR, merge, or otherwise deliver changes. Approved command information is represented only by an immutable identifier and digest. Evidence is represented only by sanitized artifacts and normalized results.

## 2. Contract states

`contract_state` is required whenever a contract field is present and must be exactly one of these values:

| State | Meaning and routing |
|---|---|
| `N/A — no quality gate contract` | No contract was declared. Do not emit an empty packet, select either worker, or change the current executor/review path. |
| `report-only` | A valid packet may record sanitized gate evidence and gaps, but must not dispatch write-enabled Cleaner or Hardener workers. |
| `advisory` | A valid packet may dispatch eligible gates. A threshold miss, unavailable authorized tool, or residual survivor is a concern and maps to `DONE_WITH_CONCERNS`. |
| `enforced` | A valid packet may dispatch eligible gates. An unavailable authorized tool, threshold miss, or capped residual survivor maps to `BLOCKED`. |
| `NEEDS_CONTEXT` | The declaration or packet is incomplete, contradictory, unauthorized, or outside the defined boundary. Do not infer a pass or dispatch a worker. |

The exact no-contract sentinel is `N/A — no quality gate contract` (including capitalization, spacing, and em dash). It is a valid compatibility state, not a failure.

## 3. Canonical bounded packet

A present packet contains only the following bounded metadata. Producers must omit the conditional packet entirely when the exact no-contract sentinel applies.

| Field | Required content and constraints |
|---|---|
| `contract_state` | One allowed state from §2. A declaration that claims `report-only`, `advisory`, or `enforced` must include every other required field. |
| `ownership.production_paths` | Exact task-owned production paths that Cleaner may change. Paths must be narrow enough to enforce and must not include tests or fixtures. |
| `ownership.production_symbols` | Exact changed production functions, methods, classes, or more granular symbols/locators within `production_paths`. A production packet without this changed-function-level boundary is incomplete. |
| `ownership.test_fixture_paths` | Exact task-owned test and fixture paths that Hardener may change. Paths must not include production code. |
| `ownership.test_fixture_symbols` | Exact test/fixture functions, cases, fixtures, or more granular locators within `test_fixture_paths`; these define the Hardener edit boundary rather than authorizing an entire test file by implication. |
| `approved_command_ids` | Immutable identities for caller-approved baseline, complexity, and mutation checks. IDs are opaque references, never executable text. |
| `approved_command_digests` | Digest for each approved command identity, bound immutably to the packet. Missing or mismatched digests are `NEEDS_CONTEXT`. |
| `sanitized_evidence_paths` | Repository-relative destinations for redacted, normalized evidence artifacts. Each value is one bounded file path, not a glob or directory authority; it is metadata, not permission to read or disclose raw output. |
| `complexity_threshold` | Caller-approved maximum CRAP value, ordinarily in the 6–8 range. A measured value above the maximum is a complexity-gate miss. |
| `mutation_target` | Caller-approved minimum mutation score, ordinarily at least 90%. A measured score below the target leaves mutation work eligible. |
| `attempt_cap` | Maximum Hardener attempts. The canonical cap is three; a higher value is invalid. |
| `residual_survivors` | Sanitized list of mutation survivors and their bounded evidence references, where applicable. Every survivor must remain reportable; none may be declared equivalent. |

Task generation binds this packet to the task’s exact Ownership, including changed production symbols and test/fixture symbols. Downstream consumers may carry fields forward, but may not broaden paths or symbols, replace command identities or digests, invent thresholds, or add raw command-like data.

## 4. Evidence boundary and redaction

Gate results may contain only normalized, reviewable facts such as:

- terminal status;
- approved command identity and digest;
- whether the approved baseline test was observed before and after a Cleaner change;
- measured maximum CRAP and the configured complexity threshold;
- mutation score, configured target, attempt count, and the sanitized residual-survivor list;
- changed paths checked against the packet’s Ownership; and
- sanitized artifact paths.

Before evidence crosses a worker, executor, reviewer, or completion-report boundary, remove raw executable command text, raw stdout/stderr, transcripts, credentials and other secrets, and full diffs. A result missing required sanitized evidence is not a pass: return `NEEDS_CONTEXT` when the packet or boundary cannot be verified, or apply the state-specific unavailable-tool rule in §7 when the authorized tool cannot produce the evidence.

Every `sanitized_evidence_paths` value must pass validation at the canonical boundary before the packet is accepted or forwarded. It must be repository-relative (no leading `/`, drive/UNC prefix, home-directory form, or `./` authority), contain no `..` segment, resolve beneath the repository root after normalization, and not escape through a symlink or other path indirection. It must identify a bounded destination rather than a glob, wildcard, directory, or unrestricted temporary location. The path and artifact must be non-secret: reject secret-bearing path components or filenames (for example, credential, token, password, or key material) and redact secrets from the artifact itself. Do not normalize an invalid path into an accepted one; reject it as `NEEDS_CONTEXT`.

## 5. Gate ordering and dispatch eligibility

The gate order is Cleaner before Hardener:

1. Resolve and validate the packet. `N/A — no quality gate contract` and `report-only` select neither write-enabled worker.
2. For `advisory` or `enforced`, validate task eligibility, all required IDs/digests and validated evidence paths, and both path and changed-symbol Ownership boundaries. Dispatch Cleaner only when complexity evidence exceeds `complexity_threshold`; when complexity is at or below the threshold, record the sanitized passing evidence and mark Cleaner as legitimately skipped.
3. Cleaner may change only `ownership.production_paths`. It must not change tests or fixtures, and it has no staging or delivery authority.
4. Dispatch Hardener only when sanitized evidence establishes remaining mutation survivors or mutation work and either (a) Cleaner was legitimately skipped because complexity was at or below `complexity_threshold`, or (b) Cleaner returned a permitted result (`DONE` or `DONE_WITH_CONCERNS`). A legitimate skip is not a Cleaner result and must not be treated as one. Hardener may change only `ownership.test_fixture_paths` and may not change production code.
5. Hardener makes at most three approved attempts. It reports every residual survivor and its sanitized evidence, without claiming equivalence or success merely because an attempt completed.
6. Aggregate the gate results before optional implementation review or delivery. A later `DONE` cannot erase an earlier concern.

Cleaner `BLOCKED` or `NEEDS_CONTEXT` is a disallowed result: do not dispatch Hardener, even when mutation work remains. A complexity-at-or-below-threshold skip is the sole non-result path that permits Hardener without a Cleaner status. A request that crosses either production/test boundary, exceeds path or symbol Ownership, lacks an approved identity/digest, or lacks a required validated evidence destination returns `NEEDS_CONTEXT` and performs no edit.

## 6. Worker result contracts

Cleaner returns a sanitized production-only result containing status, pre/post baseline-test evidence, measured maximum CRAP, and changed paths. It performs behavior-preserving complexity reduction only; it must not edit tests or fixtures.

Hardener returns a sanitized test-only result containing status, mutation score or bounded mutation evidence, attempts used, every residual survivor, and changed paths. It hardens assertions or fixtures only; it must not edit production code and must not label survivors equivalent.

Neither worker may stage, commit, push, create a PR, merge, deliver, or delegate those actions. A worker that cannot prove its exact input packet or Ownership returns `NEEDS_CONTEXT` before editing.

## 7. Thresholds, unavailable tools, and residuals

Complexity uses the caller-approved maximum CRAP threshold. Mutation uses the caller-approved minimum score. The ordinary defaults described in §3 are guidance, not permission to invent a value; the packet remains authoritative.

If an authorized tool is unavailable:

| Contract state | Result |
|---|---|
| `report-only` | Record the sanitized gap without mutation or worker dispatch. |
| `advisory` | Return `DONE_WITH_CONCERNS` and retain the unavailable-tool evidence. |
| `enforced` | Return `BLOCKED` and retain the unavailable-tool evidence. |

If Hardener reaches the three-attempt cap with survivors, `advisory` preserves all survivors as `DONE_WITH_CONCERNS`; `enforced` returns `BLOCKED`. The survivors remain unresolved evidence in either case. A missing packet field, invalid digest, unbounded path or symbol, invalid repository-relative evidence path, secret-bearing evidence artifact, or unverifiable evidence boundary is always `NEEDS_CONTEXT`, regardless of enforcement mode.

## 8. Status aggregation

When multiple gate or worker results are combined, use this fixed precedence from strongest stop to clean completion:

`BLOCKED > NEEDS_CONTEXT > DONE_WITH_CONCERNS > DONE`

Aggregation is monotonic: retain the strongest status and all sanitized residual concerns from every result. A later `DONE` never masks an earlier `DONE_WITH_CONCERNS`, unavailable-tool concern, capped survivor, `NEEDS_CONTEXT`, or `BLOCKED` result. The aggregate completion report contains statuses and sanitized evidence references only.

## 9. No-contract path and downstream citation

For a plan, scaffold, or task with no declaration, carry exactly `N/A — no quality gate contract` as the compatibility state where a state must be recorded. Do not create placeholder fields, dispatch Cleaner or Hardener, require a tool, or alter the established verification, review, or delivery lifecycle.

All downstream Codex surfaces cite this file for quality-gate states, packet fields, redaction, ordering, boundaries, thresholds, retry caps, unavailable-tool handling, and aggregation. They may describe their local handoff, but must not copy a divergent state table or authorize raw commands, raw output, secrets, full diffs, or delivery actions.
