# Codex Read-only Agent Inline Return Contract

> Status: Draft
> Scale: Medium
> Created: 2026-09-17
> Author: Codex
> Spec Reference: [develop-with-llm PR #234](https://github.com/yongwoon/develop-with-llm/pull/234)

## Global Constraints

> ⚠️ SUPERSEDED by Iteration 1 — see §Iteration 1 Amendments

- “Codex custom agents are read-only TOML definitions.” — `CLAUDE.md:56`
- “Their output contract uses `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` plus concise findings and a `Next action:` when the caller needs to apply or inspect something.” — `CLAUDE.md:56`
- “Codex custom agents live under `codex/agents/` as one TOML file per agent.” — `codex/AGENTS.md:8`
- “For Codex skills, `codex/skills/` is the source of truth.” — `codex/AGENTS.md:9`
- “There is no project build pipeline or package manager in this repository.” — `codex/AGENTS.md:31`

## Purpose

PR #234 fixes a contract contradiction in read-only reviewer/advisor agents: a linked shared exception allowed inline returns, while local agent instructions still implied that a report must be written to an artifact file. Codex agents in this repository already use `sandbox_mode = "read-only"`, but the local contracts are not uniformly explicit. Port the Codex-side fix so a read-only agent has one unambiguous terminal path: bounded inline output, never an artifact-file promise.

## Scope

- Add an explicit no-artifact/inline-return qualifier to every read-only Codex custom agent.
- Clarify the shared `subagent-status-actions` exception so it applies to named read-only Codex agents and preserves the canonical status fields.
- Add mechanical validation that every read-only agent contains the qualifier and that write workers are not incorrectly subjected to it.
- Extend the temporary Codex-agent installation smoke test to verify the qualifier survives installation and model fallback substitution.
- Keep the generated marketplace skill mirror synchronized after the shared reference change.

## Out of Scope

- Claude Code agent files or Claude Code installer behavior; PR #234 is evidence, not a request to duplicate its Claude-side changes.
- Changes to `codex/agents/ywc-complexity-cleaner.toml` or `ywc-test-hardener.toml`; these are the two intentional `workspace-write` workers and need their existing write contracts.
- New agents, changes to agent models/tools/sandbox modes, or changes to `codex/agents/README.md`.
- Changes to skill behavior, `agents/openai.yaml`, root release/version files, or the upstream `develop-with-llm` repository.
- Artifact persistence, worktree lifecycle, concurrent writes, or a redesign of the shared status protocol.

## Quality Gate Contract

N/A — no project-owned complexity or mutation quality-gate contract applies. Repository validation, Codex-agent installation smoke tests, and marketplace sync checks remain required.

## Outcome Oracle

- **Target:** The eight `sandbox_mode = "read-only"` Codex reviewer/advisor agents have one exact local inline/no-artifact return contract; the shared reference, validator, installed-agent smoke test, and generated marketplace copy enforce or preserve it without changing the two `workspace-write` workers.
- **Quality threshold:** `ywc-spec-validate` returns `DONE` with zero Critical and Warning findings; all six acceptance criteria are testable; the Blind Spot action is `proceed`.
- **Evidence required:** A validation report with the required status, finding counts, advisor-budget status, complete Outcome Oracle, and Blind Spot result; the named repository commands pass; and the installed destination plus generated marketplace reference are checked rather than source-only assertions.
- **Stop condition:** Stop at the first validation result meeting the threshold, or return `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT` with the unresolved findings and no task-generator handoff.

## Module Boundaries

| Module | Owned public interface | Consumers | Allowed dependencies | Forbidden dependencies |
|---|---|---|---|---|
| `codex/agents/*.toml` read-only agents | `sandbox_mode = "read-only"`; bounded inline `Status` result; no `Artifacts:` promise | `ywc-code-gen`, `ywc-impl-review`, executor and advisor callers | Existing bounded evidence packet and shared status reference | File creation/editing, artifact-path waits, lifecycle mutation |
| `codex/skills/references/subagent-status-actions.md` | Read-only exception and canonical status-payload rules | Orchestrating Codex skills | Existing status fields and triage rules | Granting write authority or replacing per-agent Output contracts |
| `scripts/validate.sh` | Structural Rule 8-style validation for read-only agent contracts | Local CI and contributors | POSIX shell, repository files | Runtime agent dispatch or TOML mutation |
| `tests/install-codex-agents-test.sh` | Installed-agent regression smoke test | `scripts/validate.sh` / local verification | Temporary `CODEX_HOME`, existing installer | Real user home or network |

## Interfaces

The shared reference and each agent TOML share one contract boundary:

| Producer | Consumes | Produces |
|---|---|---|
| Read-only agent TOML | bounded caller evidence and the agent-specific Output contract | Inline `Status`, concise summary/findings/advice, and conditional `Concerns`, `Blocker`, or `Missing context`; no artifact path is required or promised |
| `subagent-status-actions.md` | the agent's `sandbox_mode` and returned status | Routing/triage rules; `Artifacts:` is present only when a write-enabled worker actually produced output |
| `scripts/validate.sh` | each `codex/agents/*.toml` and its `sandbox_mode` | PASS or a file-specific validation error when a read-only agent lacks the qualifier |

## Existing Constraints Touched

| Existing artifact | Behavior verified by reading the file | New code's interaction |
|---|---|---|
| `codex/agents/ywc-architect.toml:5-7,17-23,40-51` | Declares `read-only`, forbids file mutation, and returns a detailed advisor verdict, but does not explicitly say that artifact requests must be answered inline. | Add the qualifier in the same developer-instructions contract; preserve its architecture-specific Output shape. |
| `codex/agents/ywc-cloud-engineer.toml:5-7,18-23,35-43` | Declares read-only infrastructure review and forbids Terraform mutation; its Output already says not to create artifacts but lacks the shared qualifier wording. | Normalize the explicit qualifier without changing IaC review semantics. |
| `codex/agents/ywc-go-reviewer.toml:5-7,16-23,37-45` | Declares read-only Go review and bounded findings, but has no artifact prohibition. | Add inline-only instruction before language-specific checks. |
| `codex/agents/ywc-performance-engineer.toml:5,18-25,32-41` | Declares read-only review and says “Do not create artifacts” in Output, but does not bind that behavior to the terminal return contract. | Add the same local qualifier; retain performance categories and evidence requirements. |
| `codex/agents/ywc-python-reviewer.toml:5-7,16-23,37-44` | Declares read-only Python review with concise findings but no artifact prohibition. | Add inline-only instruction. |
| `codex/agents/ywc-root-cause-analyst.toml:5-7,17-24,31-41` | Declares read-only root-cause analysis and concise output but no artifact prohibition. | Add inline-only instruction. |
| `codex/agents/ywc-security-engineer.toml:5-7,18-25,39-48` | Declares read-only security review and redaction requirements but no artifact prohibition. | Add inline-only instruction; do not weaken secret/PII redaction. |
| `codex/agents/ywc-typescript-reviewer.toml:5-7,16-23,37-45` | Declares read-only TS/JS review with bounded findings but no artifact prohibition. | Add inline-only instruction. |
| `codex/skills/references/subagent-status-actions.md:14-43` | Defines a Phase 1 inline exception but generally says produced output belongs in files; it does not clearly cover all read-only Codex custom agents. | Expand the exception to named read-only agents and state that `Artifacts:` is omitted when no file can exist. |
| `scripts/install.sh:143-162,174-186` | Installs shared Codex references/scripts and copies/transforms Codex agent TOMLs for the destination. | No installer logic change; the smoke test verifies the new contract survives this existing path. |
| `scripts/validate.sh:542-615` | Validates Codex agent identity, required fields, model, sandbox mode, and Claude-only field absence. | Add the mechanical read-only qualifier check alongside existing agent checks. |
| `tests/install-codex-agents-test.sh:9-39` | Installs agents into temporary homes and checks model/sandbox behavior. | Check all eight read-only installed agents for the qualifier under supported and fallback model modes. |

The complement grep found ten Codex agents: eight read-only agents above and two write workers (`ywc-complexity-cleaner`, `ywc-test-hardener`). Only the eight read-only files require the new qualifier; the two write workers are intentionally unchanged.

## Acceptance Criteria

- [ ] **AC1 — Local read-only contract:** When any of the eight read-only Codex agents is dispatched, its developer instructions explicitly state that it cannot create artifacts and must return compact inline findings/advice; the statement is present in the agent's own contract, not only in a linked reference.
- [ ] **AC2 — Shared exception:** When an orchestrator receives a read-only Codex agent result, the shared reference permits inline output and does not require an impossible artifact path; `Status`, `Summary`, and conditional `Concerns`/`Blocker`/`Missing context` semantics remain intact.
- [ ] **AC3 — Write-worker separation:** When validation scans the two `workspace-write` workers, it does not require the read-only qualifier and does not change their write-boundary contract.
- [ ] **AC4 — Mechanical regression guard:** When a read-only agent's qualifier is removed or `sandbox_mode` is changed inconsistently, `bash scripts/validate.sh` reports a file-specific failure and exits nonzero.
- [ ] **AC5 — Installed parity:** When `tests/install-codex-agents-test.sh` installs agents into a temporary `CODEX_HOME` under both GPT-5.6-supported and fallback model paths, all eight installed read-only TOMLs retain the qualifier and the existing model/sandbox assertions still pass.
- [ ] **AC6 — Distribution parity:** When the Codex marketplace sync/validation runs, the generated `plugins/ywc-agent-toolkit/skills/references/subagent-status-actions.md` matches the source reference and no stale generated package remains.

## Functional Requirements

### FR-1: Explicit read-only agent qualifier

Insert one consistent contract paragraph into the developer instructions of `ywc-architect`, `ywc-cloud-engineer`, `ywc-go-reviewer`, `ywc-performance-engineer`, `ywc-python-reviewer`, `ywc-root-cause-analyst`, `ywc-security-engineer`, and `ywc-typescript-reviewer`. It must state: the agent has no write capability; it must return bounded findings/advice inline; it must not promise or wait for an artifact file; and `Artifacts:` is omitted unless a write-enabled caller separately produced an artifact. Preserve each agent's existing domain-specific Output contract.

### FR-2: Shared read-only routing exception

Update `codex/skills/references/subagent-status-actions.md` so the exception is named as a read-only reviewer/advisor exception, covers the eight named agents, and makes the write-authority boundary explicit. Keep the existing Phase 1 canonical target/finding limits and status triage rules; do not make the shared reference a second competing Output schema.

### FR-3: Mechanical validator

Extend `check_codex_agent_file()` in `scripts/validate.sh` with a rule that applies to every TOML whose `sandbox_mode` is `read-only`. The exact canonical qualifier that must appear inside the `developer_instructions` TOML value is: `Read-only inline/no-artifact contract: You have no write capability. Return bounded findings/advice inline; do not promise or wait for an artifact file. Omit Artifacts: unless a write-enabled caller separately produced an artifact.` The rule must inspect the developer-instructions body and require that exact qualifier; it must not be bypassed by the phrase appearing only in comments, another file, or a write worker's contract. Error messages must include the agent path/name.

### FR-4: Installed-agent regression coverage

Extend `tests/install-codex-agents-test.sh` with an explicit expected read-only agent set and checks against files in the temporary installed destination, not source files. Run the checks for the existing unsupported and supported Codex CLI version branches so `sed` model substitution cannot remove or corrupt the contract.

### FR-5: Generated package synchronization

After source edits, run `bash scripts/sync-codex-plugin.sh` and retain only the generated marketplace reference change. Do not hand-edit the generated package first. `bash scripts/validate.sh` remains the final source/package freshness oracle.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Safety | A read-only agent must never be instructed to perform an impossible file write or to wait for an artifact it cannot create. |
| Compatibility | Preserve existing Status values, domain-specific Output fields, model fallback substitution, and write-worker contracts. |
| Maintainability | Use one canonical qualifier and one validator rule rather than per-agent divergent wording or ad hoc tests. |
| Distribution | Source reference and generated marketplace reference must remain synchronized. |

## Data Model

N/A — no data model change.

## API Contract

N/A — no HTTP/API contract change. The affected interface is the bounded agent return contract described in `## Interfaces`.

## Edge Cases

- **Read-only agent requests an artifact:** Return inline bounded content with no `Artifacts:` field; do not stall waiting for a path.
- **Read-only agent returns `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT`:** Preserve the corresponding `Concerns`, `Blocker`, or `Missing context` payload required by the shared reference so the orchestrator can triage or re-dispatch.
- **Write worker is scanned:** Do not require the read-only qualifier when `sandbox_mode = "workspace-write"`; its existing bounded write contract remains authoritative.
- **GPT-5.4 fallback installation:** Agent text is transformed only for the model string; the inline qualifier must remain byte/semantically present.
- **Shared reference is installed through the marketplace package:** The generated copy must match source; a stale copy is a validation failure, not a reason to weaken the contract.
- **Agent has an existing “Do not create artifacts” sentence:** Still add the canonical local qualifier if the validator requires it; do not rely on a looser phrase or on the shared reference alone.

## Dependencies

- Existing `scripts/install.sh`, `scripts/sync-codex-plugin.sh`, and `scripts/validate.sh`.
- Existing temporary `CODEX_HOME` installation smoke test.
- No new library, runtime dependency, service, database, or custom agent.

## Open Questions

N/A — none identified. The target, read-only set, and implementation boundary are resolved by current TOML inventory and PR #234's Codex-side change.

## Blind Spot Pass

- **Current approach:** Port PR #234's Codex read-only inline-return contract and validator guard into this repository's `codex/` source of truth.
- **Assumption most likely to break it:** An existing read-only agent may be intentionally allowed to write through an external caller or may use a different terminal contract.
- **Repo evidence:** All eight review/advisor agents declare `sandbox_mode = "read-only"`; the only `workspace-write` agents are `ywc-complexity-cleaner` and `ywc-test-hardener`; existing contracts already forbid direct file mutation.
- **Action:** Apply the qualifier only to the eight read-only files, preserve the two write-worker files, and test the installed destination rather than source-only text.

## Confidence Gate

`ywc-confidence-gate` result: **92/100 — PROCEED**.

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 94 | User explicitly limited the target to Codex skill/agent; eight read-only agents and two write workers are enumerated. |
| Architecture compliance | 88 | Uses existing TOML contracts, shared status reference, shell validator, installer smoke test, and source-first package sync. |
| Evidence quality | 92 | PR #234, current files, collector snapshot, complement grep, and actual validation/install commands were inspected. |
| Reuse verified | 90 | Reuses existing `validate.sh`, installer test, shared reference, and package sync; no new framework/library. |
| Root cause identified | 96 | The failure is a contradictory local artifact expectation combined with read-only sandbox authority, not merely missing prose. |

## Self-Consistency Pass

- **Pass A:** AC1–AC3 map to FR1–FR2; AC4 maps to FR3; AC5 maps to FR4; AC6 maps to FR5. No HTTP status, data-model field, or numeric boundary is introduced.
- **Pass B:** Every “read-only” and “write worker” closure claim is backed by the complement inventory above. Existing installer and validator behavior is cited in `Existing Constraints Touched`; no adjacent Claude-side changes are included.
- **Pass C:** N/A — no schema, database relation, migration, or persistence change.

## Verification Commands

- `bash tests/install-codex-agents-test.sh`
- `bash scripts/install.sh --list --codex`
- `bash scripts/install.sh --list --codex-agents`
- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/validate.sh`
- `git diff --stat` and `git diff --check`

## Risks / Rollback

- **Risk:** A strict qualifier check may reject a legitimate read-only agent with a materially different but safe Output contract. Mitigation: keep the rule limited to `sandbox_mode = "read-only"`, inspect the exact developer-instructions body, and preserve domain-specific Output sections.
- **Risk:** Updating the shared reference can expose stale wording in downstream skill prompts. Mitigation: keep the canonical field names and Phase 1 limits unchanged, then run the full validator/eval suite.
- **Risk:** Generated marketplace files drift from source. Mitigation: sync from `codex/skills/` and let `scripts/validate.sh` detect stale copies.
- **Rollback:** Revert the agent TOML qualifier additions, shared reference change, validator assertion, test assertions, and generated marketplace reference as one change set; no runtime data or user installation is mutated by this plan.

## References

- [develop-with-llm PR #234](https://github.com/yongwoon/develop-with-llm/pull/234)
- `AGENTS.md`
- `codex/AGENTS.md`
- `CLAUDE.md`
- `codex/agents/*.toml`
- `codex/skills/references/subagent-status-actions.md`
- `scripts/install.sh`
- `scripts/validate.sh`
- `tests/install-codex-agents-test.sh`

## Handoff

After this spec is reviewed and converged:

1. Run `ywc-spec-validate --spec docs/ywc-plans/20260917-codex-readonly-agent-inline-contract.md`.
2. After validation returns `DONE`, run `ywc-task-generator` on this spec.
3. Execute the generated tasks with `ywc-sequential-executor` or `ywc-parallel-executor`.

## Iteration 1 Amendments

- **Requirements addressed:** The initial readiness pass identified a missing mandatory Outcome Oracle, an undefined canonical qualifier for FR-3/AC1/AC5, and an overbroad Global Constraints quotation that contradicted the two intentional `workspace-write` workers.
- **Amended approach:** Add the four-field Outcome Oracle above. Define one exact qualifier string and require it in each read-only agent's `developer_instructions` value; installed-agent checks must search for that same string. Correct the repository constraint to distinguish the eight read-only reviewer/advisor TOMLs from the two bounded write workers.
- **Updated Acceptance Criteria:** AC1 and AC5 use the exact qualifier defined in FR-3. AC3 explicitly remains the write-worker boundary check. The Outcome Oracle is authoritative for readiness and requires zero Critical/Warning findings plus a `proceed` Blind Spot action.
- **Corrected Global Constraints:** Codex custom agents are TOML definitions under `codex/agents/`; the repository currently contains eight read-only reviewer/advisor agents and two intentional `workspace-write` workers. The read-only contract in this spec applies only to the eight named read-only agents.
