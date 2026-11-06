# PR worktree identity and preservation — scenarios

## AC-9 — existing-branch and pinned PR selection
1. In a temporary Git repository, test existing local and exact `origin/<H>` refs plus absent, network-failure, checked-out, dirty, and locked cases; pass `--existing-branch` with and without `--base-branch`.
2. Test `--worktree` without a positive PR number, with a closed/foreign-repository PR, and with a valid same-repository open PR whose head changes during the run.

Expected: flags are mutually exclusive; existing local/exact remote refs are distinguished from absent/network/locked states; a positive same-repository open PR and head are pinned for the invocation; branch allowlist and check-ref-format reject unsafe refs.

## AC-9 — worktree lifecycle and failure handling
1. Exercise clean canonical worktrees in in-place, reused, and created states; inject local-ahead, divergence, dirty state, fetch failure, cwd reset once, repeated cwd reset, commit/push/CI failure.
2. Capture fetch/fast-forward/push commands and cleanup guidance.

Expected: only exact fetch and fast-forward are allowed; no main-checkout fallback; cwd/root/branch is rechecked before each read/mutation/API/commit/push/CI operation; cwd re-entry is allowed once only; push uses `HEAD:refs/heads/$H`. A required command failure stops retries and later mutations and reports prior side effects. Created worktrees get branch-preserving prune guidance; reused/in-place worktrees are never automatically deleted. Existing audit/cleanup helper tests run in temp repos; actual model choices remain source/trace evidence unless live.
