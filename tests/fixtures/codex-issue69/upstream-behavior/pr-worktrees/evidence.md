# PR worktree evidence

- Frozen source: `yongwoon/develop-with-llm` #347, merge `76200680f059d34d295b3f01da527c29ea782dc2`; bounded worktrees and handle-pr-reviews SKILL files were fetched read-only.
- Baseline: shared contract suite 3 passed; existing behavior suite 4 passed; existing cleanup helper test passed.
- RED before source edits: focused fixture made the shared contract suite exit 1 for missing `--existing-branch <H>`.
- Final: `git diff --check`, shared contract suite (3 tests), Codex skill contract eval runner, and behavior suite (10 tests) all passed. The eval runner also ran the agent-eval structural gate.
- Required-clause negative controls: all 39 removals failed the real shared source assertion in temporary copies; 0 misses. Every scenario is bound to its own required source clause.
- Source command recipe execution: 16 existing-branch cases and 7 exact-refresh cases ran the original marked Bash blocks. Tests used temporary local/bare Git repositories and an argv-logging Git transport wrapper, including wrong/duplicate refs, lookup/fetch failure, checked-out/dirty/locked states, local-ahead/divergence and no later worktree-add/merge after refusal.
- Existing helper execution: audit retained clean, MISSING, LEAKED, DRIFT and STALE classifications. Cleanup refused dirty/locked worktrees, preserved their paths/branches, and retained the head branch on clean `--keep-branch` cleanup. The existing cleanup regression script also ran.
- Static source/expected traces: 11 PR API selection, lifecycle/cwd budget, push/failure and cleanup scenarios are checked against their exact fixture scenario. They are not a simulated dispatcher or live model evidence.
- Live PR/API/agent behavior: `UNVERIFIED — instruction contract only`. No remote PR mutation, real network Git transport, model dispatch or live cwd-recovery claim was made.
- Evaluation provenance: existing worktrees cases retain upstream string IDs in `source_id`; new cases use explicit `local-fr9-*` IDs because frozen #347 supplied no matching worktree-mode eval cases.
- Full generated-package validation belongs to parent integration/distribution; this worker changed no generated plugin paths and did not run sync.

Ruling: yk-000001-100-domain-pr-worktrees — omit upstream's one-time post-create-failure reuse attempt — approved FR-9 requires stopping retries after a required command failure — cost if wrong: recovery requires a new invocation rather than same-invocation reuse.
