# Parallel task worktree 정리 실행 위치 안전성 개선 계획

> Status: Draft
> Scale: Medium
> Created: 2026-11-05

## Purpose

병렬 executor가 완료 task의 worktree를 정리할 때 cleanup helper를 삭제 대상 worktree 내부에서 실행해 현재 작업 디렉터리까지 제거하는 문제를 방지한다. 최근 session에서는 helper가 worktree를 삭제한 뒤 `Unable to read current working directory` 오류를 냈지만 `PASS`를 출력해 cleanup 결과도 오인할 수 있었다.

- What: cleanup 호출을 안정적인 controller checkout에서 실행하고, helper가 현재 checkout을 삭제하려는 요청을 거부하며, cleanup 및 검증 실패를 성공으로 표시하지 않도록 한다.
- Why: task range 실행 중 현재 worktree가 사라지면 후속 task 작업과 도구 호출이 중단되고, 거짓 성공 표시는 복구 시점을 늦춘다.
- Out of Scope: 성공한 DONE task worktree를 4g에서 정리하는 lifecycle 자체, BLOCKED task 보존 정책, Claude Code 동작, executor 전반의 routing 재설계, 별도 원인이 확인되지 않은 `.worktrees/continuation-base` 부재.
- Done When: 재현 시나리오에서 self-target cleanup은 실패하며 target과 branch가 보존되고, controller checkout에서 수행한 정상 cleanup은 의도한 target만 제거하며, prune/검증 오류는 nonzero와 실패 결과로 끝나고 `PASS`가 출력되지 않는다.

## Outcome Oracle

- Target: Codex parallel task range cleanup이 현재 실행 중인 checkout을 삭제하거나 삭제 실패를 성공으로 보고하지 않는다.
- Quality threshold: regression 시나리오 3종(self-target 거부, 안정 경로의 정상 cleanup, Git cleanup/검증 failure injection)이 모두 기대한 종료 코드·디렉터리·branch·출력으로 확인된다. 기존 branch preserve/delete 동작은 유지한다.
- Evidence required: task-range session의 호출 cwd와 helper 결과, 수정 source 및 생성 plugin mirror, 임시 Git repository 기반 실행 결과.
- Stop condition: cleanup 전에 기록한 invocation preflight checkout root를 controller cwd로 사용할 수 없거나 해당 checkout이 삭제 대상이면 cleanup을 시작하지 않고 NEEDS_CONTEXT로 종료한다. 필수 검증 실패 시 구현 완료를 선언하지 않는다. live Codex 호출을 실행하지 못하면 관련 항목을 UNVERIFIED로 보고하며 runtime 지원 보장을 하지 않는다.

## Scope

- `codex/skills/ywc-parallel-executor/SKILL.md`에서 invocation preflight 시점의 repository root를 controller checkout으로 기록하고 Step 4g cleanup 호출의 working directory로 사용한다. 이 경로가 없거나 cleanup target과 같으면 cleanup하지 않고 NEEDS_CONTEXT로 종료한다.
- `codex/skills/ywc-worktrees/scripts/cleanup-worktree.sh`에서 요청 target이 현재 checkout과 같을 때 삭제 전에 fail-closed 한다.
- cleanup, prune, metadata/directory/branch verification 오류가 발생하면 실패 종료하고 `PASS`를 내지 않도록 helper의 결과 처리를 바로잡는다.
- 기존 cleanup test를 확장해 self-target, 정상 외부 target, 검증 실패 경로를 확인한다.
- `tests/codex_issue69_behavior_test.py`에 Step 4g controller-root/cwd 계약의 source assertion 또는 expected trace를 추가한다. 이는 Markdown 계약 증거이며 live Codex runtime 증거로 표시하지 않는다.
- `plugins/ywc-agent-toolkit/skills/` 생성 mirror를 source에서 sync하고 source와 mirror 일치를 확인한다.
- DONE task cleanup 및 BLOCKED task 보존 조건은 변경하지 않는다.

## Out of Scope

- DONE task worktree를 병렬 실행 완료 시 제거하는 시점 변경: 최근 실행의 4g lifecycle은 의도된 동작이며 문제는 실행 위치와 helper의 self-target 방어다.
- BLOCKED/실패 task worktree 보존 정책 변경: 기존 복구 가능 상태를 유지한다.
- `.worktrees/continuation-base`가 사라진 별도 사건의 원인 규명: 조사한 session 기록에서 해당 경로를 제거한 명령을 확인하지 못했으며, 이번 cleanup 호출의 증거와 연결되지 않는다.
- `ywc-task-executor`의 전체 실행 topology나 다른 runtime의 worktree 정책 변경.
- 실제 사용자 설치 경로의 skill 변경.

## Global Constraints

- Codex skills live under `codex/skills/` in a flat `codex/skills/<skill-name>/` structure. (`codex/AGENTS.md:7-8`)
- For Codex skills, `codex/skills/` is the source of truth. The marketplace package under `plugins/ywc-agent-toolkit/skills/` is generated from it by `bash scripts/sync-codex-plugin.sh`; do not edit the generated package first. (`codex/AGENTS.md:12`)
- `bash scripts/validate.sh` validates source install structure and marketplace package freshness. (`codex/AGENTS.md:22-24`)
- Existing task `yk-000001-100-domain-pr-worktrees` owns `codex/skills/ywc-worktrees/` while that task is active; its scope is FR-9 and it does not include runtime routing redesign. This follow-up must be scheduled after that ownership is released or coordinated as an explicit amendment. (`tasks/yk-000001-100-domain-pr-worktrees/README.md:16-20,62-79`)

## Existing Constraints Touched

| Existing artifact | Behavior (verified by reading the file) | New code's interaction |
|---|---|---|
| `codex/skills/ywc-worktrees/scripts/cleanup-worktree.sh:80-85` | Resolves `REPO_ROOT` using `git rev-parse --show-toplevel` from the caller's current repository, then changes directory to that root. | Add a guard before destructive work so a target equal to the active checkout cannot be removed; ensure caller context remains a stable controller checkout. |
| `codex/skills/ywc-worktrees/scripts/cleanup-worktree.sh:159-184` | Runs `git worktree remove` for the requested target and records a failed remove in `FAILED`. | Preserve exact target selection and existing dirty/locked failure behavior. |
| `codex/skills/ywc-worktrees/scripts/cleanup-worktree.sh:186-217` | Preserves or deletes the requested branch, then ignores `git worktree prune` failure with `|| true` and prints an unconditional prune success line. | Retain branch mode semantics; propagate prune failure and avoid success output on failure. |
| `codex/skills/ywc-worktrees/scripts/cleanup-worktree.sh:219-235` | Verifies directory/metadata/branch state after cleanup; verification is skipped when prior cleanup sets `FAILED`. | Make verification command failures observable and ensure final success requires all required checks to complete successfully. |
| `codex/skills/ywc-parallel-executor/SKILL.md:378-406` | Step 4g removes delivered DONE task worktrees and preserves BLOCKED tasks; it directs cleanup through `ywc-worktrees --mode prune`. | Keep lifecycle and branch policy; capture the preflight checkout root before worker dispatch and explicitly run cleanup in that controller checkout, never the target being removed. |
| `codex/skills/ywc-worktrees/scripts/test-cleanup-worktree.sh:20-34` | Tests branch preservation and deletion only when cleanup is invoked from the fixture repository root. | Extend this executable seam to cover cleanup invoked from inside its own target and injected Git command failures. |
| `tasks/yk-000001-100-domain-pr-worktrees/README.md:6-20,62-79` | Active FR-9 task owns the worktrees skill directory and excludes runtime routing redesign. | Sequence this follow-up after ownership release or record explicit coordination before implementation to prevent concurrent edits. |

## Module Boundaries

| Module | Owned public interface | Consumers | Allowed dependencies | Forbidden dependencies |
|---|---|---|---|---|
| `ywc-parallel-executor` cleanup instructions | invocation preflight checkout root and Step 4g working-directory contract | parallel task-range run | `ywc-worktrees` prune contract; preflight checkout root captured before worker dispatch | target task worktree as helper process cwd; cleanup when controller root equals target |
| `ywc-worktrees` cleanup helper/tests | cleanup script arguments, exit status, output, Git worktree/branch effects | parallel executor and direct helper callers | Git CLI and existing repository state | deleting the current checkout; treating failed verification as success |
| Generated plugin package | mirrored skill files | installed marketplace users | source files under `codex/skills/` | direct-first edits |

## Acceptance Criteria

- [ ] **AC-1 — Active checkout is protected**: When cleanup is requested from inside the exact worktree named as its target, helper exits nonzero before removing files or Git metadata, observable as target directory and its branch remaining present and no success marker in output.
- [ ] **AC-2 — Parallel cleanup uses stable cwd**: When Step 4g cleans a DONE task, the executor invokes `ywc-worktrees --mode prune` with cwd equal to the repository root captured during preflight before worker dispatch, observable as a passing source-contract assertion/expected trace in `tests/codex_issue69_behavior_test.py`; this is instruction evidence, not live Codex runtime evidence.
- [ ] **AC-3 — Intended cleanup succeeds**: When invoked from the stable controller checkout for a separate eligible target, helper removes only that target, preserves or deletes its branch according to the existing option, and exits zero only after verification succeeds.
- [ ] **AC-4 — Failure is not reported as success**: When prune, metadata listing, or required verification fails, helper exits nonzero and emits no final `PASS`/success result; the failure is visible in its diagnostic output.
- [ ] **AC-5 — Task lifecycle policy remains intact**: When Step 4g processes DONE and BLOCKED tasks, only eligible DONE worktrees enter cleanup and BLOCKED worktrees remain preserved.
- [ ] **AC-6 — Distribution stays synchronized**: After source changes are synchronized, generated plugin copies of the changed skill/helper/test artifacts match their source and `bash scripts/validate.sh` accepts the bundle.

## Functional Requirements

### FR-1: Stable cleanup execution context

Parallel executor must capture its invocation preflight repository root before worker dispatch and use that exact path as the cwd for Step 4g cleanup. If the path is missing or equals the cleanup target, it must stop cleanup and return NEEDS_CONTEXT without attempting deletion. The caller must not rely on a shell retaining a current directory whose path cleanup removes. Existing successful-DONE eligibility, BLOCKED preservation, branch handling, and task-state reporting remain unchanged.

### FR-2: Self-target deletion guard

Before any destructive operation, helper resolves the current checkout and canonical target path sufficiently to compare identity. If target is the current checkout (including equivalent relative/absolute spellings), it returns a clear failure and performs no directory, metadata, or branch mutation. If the helper cannot establish the identity safely, it fails closed.

### FR-3: Truthful cleanup result

Every required Git operation, including prune and postcondition checks, contributes to the final status. Any failed command or unverifiable postcondition causes nonzero exit and a failure diagnostic. `PASS` is emitted only after all required cleanup and verification operations succeed. Preserve current `--keep-branch` behavior and safe branch deletion checks.

### FR-4: Regression coverage and bundle parity

Extend the existing temporary-repository cleanup test rather than creating a parallel helper harness. Add the Step 4g invocation cwd contract to `tests/codex_issue69_behavior_test.py` as a source assertion/expected trace; label it as instruction evidence rather than live runtime evidence. Include controlled failure injection for a prune or verification command without relying on destructive changes to the developer's repository. Update source-of-truth files first and regenerate the marketplace mirror using the documented sync script.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Safety | Cleanup is bounded to the explicitly selected worktree; inability to establish target/current identity or verify required postconditions fails closed. |
| Compatibility | Existing CLI flags, branch-preservation semantics, and DONE/BLOCKED lifecycle remain compatible unless a specific unsafe invocation now exits nonzero. |
| Maintainability | The regression extends the existing helper test seam and avoids a new runtime dependency. |

## Data Model / API Contract

- Data Model: N/A — no data model change.
- API Contract: N/A — no HTTP/API contract change. The shell helper's existing CLI is retained; exit/output correctness is specified in FR-3 and AC-1/3/4.

## Edge Cases

- Relative target path and symlink/canonical path resolving to the active checkout: reject before mutation.
- Worktree already absent but metadata remains: report only according to existing supported behavior, while still checking command success and metadata state.
- `git worktree prune` fails after target removal: return failure and do not emit PASS; report that filesystem removal may already have occurred.
- Target is another linked worktree and current checkout is a separate controller: permit cleanup only when all existing safety checks and postconditions pass.
- Branch deletion is refused by Git because it is unmerged or checked out elsewhere: preserve the existing failure and never force-delete.

## Failure Modes

| ID | New path | Realistic failure | Covered by (AC / test / error handling) | User-visible? |
|---|---|---|---|---|
| `FM-1` | Self-target guard | Canonicalization or Git context lookup fails | AC-1; fail closed before mutation | Yes, nonzero diagnostic |
| `FM-2` | Prune/verification | Git command fails after worktree directory removal | AC-4; injected command failure, nonzero result and explicit partial-cleanup diagnostic | Yes |
| `FM-3` | Caller working directory | Controller checkout path is unavailable or itself scheduled for cleanup | AC-2; caller must stop before cleanup and surface context failure | Yes, run blocked |

## Dependencies

- Active ownership of `codex/skills/ywc-worktrees/` in task `yk-000001-100-domain-pr-worktrees` must be released or explicitly coordinated before implementation.
- `yk-000002-010-infra-distribution` owns generated plugin distribution; schedule mirror sync after source changes or coordinate its ownership boundary.
- Existing Git CLI and current temporary-repository shell test; no new external library.

## Open Questions

- N/A — no unresolved scope decision. If implementation cannot preserve or pass the preflight repository root through Step 4g, it must follow the specified NEEDS_CONTEXT stop condition. The separate missing `.worktrees/continuation-base` event remains outside this plan because the examined session contains no deletion command tying it to this cleanup path.

## References

- `codex/skills/ywc-parallel-executor/SKILL.md` — Step 4g lifecycle and cleanup call.
- `codex/skills/ywc-worktrees/scripts/cleanup-worktree.sh` — cleanup implementation.
- `codex/skills/ywc-worktrees/scripts/test-cleanup-worktree.sh` — existing executable regression seam.
- `docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md` — FR-9 parent scope and existing task boundaries.
- Session evidence: `/Users/yongwoon.kim/.codex/sessions/2026/11/05/rollout-2026-11-05T14-04-17-01a1aa17-eedf-7822-84f0-9ee4e1168c55.jsonl`.

## Planning Gate / Self-Consistency

`ywc-confidence-gate --assessment scored`: Scope 95, Architecture 90, Evidence 95, Reuse 85, Root cause 95 → weighted aggregate 92, PROCEED. The weakest dimension is Reuse (85): the existing cleanup helper and shell test are reused; no new cleanup mechanism is proposed. The decision is bounded to the caller's cwd contract and helper safety/result handling.

Pass A: AC-1~6 map to FR-1~4 and the named regression/distribution checks. Pass B: existing helper branch semantics, lifecycle eligibility, source-of-truth and plugin sync constraints are recorded above. Pass C: no data model; API contract is N/A. Blind Spot: The anchor must remain the preflight repository root captured before worker dispatch; if the executor cannot retain it or if it equals a cleanup target, Step 4g stops with NEEDS_CONTEXT. Caller source assertion and expected trace verify the written contract only, not a live Codex run. The separate continuation-base disappearance is not attributed to this root cause.

## Next

`ywc-spec-ready --spec docs/ywc-plans/20261105-worktree-cleanup-execution-context.md` must converge the spec before `ywc-task-generator` decomposes it. This plan does not implement the change.
