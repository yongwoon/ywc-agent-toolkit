# Operational safety evidence — yk-000001-070

## Pre-edit audit and baseline

- Rewrite-level ambiguities: none. The frozen FR-6 / AC-6, test.md and source
  ownership agree; no callable signature or runtime dispatcher is introduced.
- Prerequisite: parent confirmed 060 merged/completed in selected base `91ccd3a1`.
- Baseline: `python3 tests/codex_issue69_contract_test.py` PASS (3 tests).
- RED before source edits: same command FAIL, operational-safety fixture missing
  `**Remote deletion guard**` in finish-branch. Existing source also gates only
  isolation exit 1, contains a global internal-only downgrade, and does not
  preserve polling state across chunks. These are source failures, not observed
  model rationalizations or live invocation failures.
- Frozen source consulted: GitHub commit files API for #346 merge
  `6fe84d96e910d1d56137862366161ab0780d91f1` and #341 merge
  `b529b0594f1db8534a34359f4bd625ae4f023d6a`; approved port boundaries from spec.

## Interface and data-integrity contract

- Input authority: original caller's repository, validated branch and intended
  base; no guessed values. Missing owner/input/output/status agreement is
  `NEEDS_CONTEXT`. Normal merge/delete and local cleanup remain their owners.
- Standalone remote deletion: validate branch, successful parsed empty open-PR
  list, and if merged is the reason, matching actual base plus current remote
  tip. Any failed query or mismatch means zero deletion requests. A tip-bound
  lease protects the final write against concurrent pushes. Retry requires a
  fresh full guard, including after an uncertain deletion response; absent
  remote ref is reported as already absent, not a new deletion. Partial delivery
  is never completion. No real remote write is exercised here.
- Setup: existing Docker helper owns worktree-local state; executor owns worker
  admission. Every nonzero status, including 127, blocks that task before spawn
  and preserves its Git lifecycle. Retrying must inspect retained setup state;
  successful setup does not authorize another worker for an already active task.
- Polling: one invocation/repository/queue owner serializes state, preserves one
  original deadline, atomically replaces complete state, and refuses ambiguous
  resume. Rebase requests keep per-PR durable success markers. A transport error
  with uncertain comment delivery requires reconciliation before retry.
- Severity: row-local exceptions, item 2 no downgrade. Explicit-invocation
  preference is metadata, not a runtime enforcement guarantee.
- Shared hardening guidance read from installed reference:
  `/Users/yongwoon.kim/.codex/skills/references/data-integrity-hardening.md`.
  It is absent from this repository; no shared file is copied or added.

## Evidence classes

- Source assertions and expected traces prove instruction contracts only.
- Docker setup tests execute the existing helper in temporary Git repositories
  with an injected failing subprocess; duplicate setup and Git preservation are
  checked. They do not prove model worker invocation counts.
- Extracted Dockerfile diff detector is executed with fake `gh`; the polling
  snippet remains descriptive lane scheduling, so polling uses expected traces.
- Live API/worker calls, remote deletion, real CI and live severity decisions:
  **UNVERIFIED — instruction contract only**.
