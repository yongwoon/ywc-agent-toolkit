# yw-000008-010-test-collector-contract-harness — Implementation Checklist

## Prerequisites
- [ ] Confirm the current collector exists at `codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`.

## Allowed Edit Scope
- [ ] Modify only `codex/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py`.
- [ ] Stop and report before touching the production collector or generated package.

## Stop Conditions
- [ ] Stop if the current collector output requires a production schema or behavior change to test.
- [ ] Stop if a fixture requires network access, real `gh` authentication, or writes outside a temporary directory.
- [ ] Stop if the test file must be split across another task-owned surface.

## Hardening Gate
- [ ] Classify this as uncovered behavior/test hardening.
- [ ] Record the new unittest module as the RED-first feedback path before finalizing production-facing assertions.
- [ ] Record the stdout JSON and exit/stderr contract before implementation body work.
- [ ] Mark Data Integrity Hardening N/A because the harness is read-only and temporary.
- [ ] Critical-surface review is N/A under the spec.

## Implementation Steps
- [ ] Create `codex/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py` using only `tempfile`, `pathlib`, `subprocess`, `json`, and `unittest`.
  - [ ] Create a temporary executable fake `gh` that logs argv and dispatches exact `api user`, four API fetches, and `pr view` responses.
  - [ ] Fail the test on unexpected argv, unexpected invocation order, nonzero fake responses, or leaked temporary state.
- [ ] Build deterministic fixtures for review comments, issue comments, reviews, and `pr view` health data.
  - [ ] Assert unanswered threads, self-response suppression, and newer reviewer reopen behavior.
  - [ ] Assert addressed and legacy markers, external PR comments, and normalized `artifact_type`, `fingerprint`, `reply_api`, `id`, `body`, `path`, `line`, `user`, and `state` fields.
- [ ] Cover review submissions and health gates.
  - [ ] Include external non-empty `COMMENTED`/`CHANGES_REQUESTED` reviews and suppress approval, empty, self-authored, marker, and addressed reviews.
  - [ ] Include failed/pending status checks, success/skipped/neutral suppression, optional-field precedence, non-clean merge readiness, clean suppression, and `UNKNOWN` fallback.
- [ ] Add an authentication/API failure scenario asserting exit code 3 and the relevant stderr contract without relying on real credentials.
- [ ] Run the focused unittest and shell syntax check; confirm no production or excluded-path diff is present.

## Task Verify
- [ ] `python3 -m unittest codex/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py`
- [ ] `bash -n codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`
- [ ] `git diff -- codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh claude-code plugins | sed -n '1,120p'` shows no out-of-scope production, Claude, or generated edits.

## Verification
- [ ] lint passes (`bash scripts/validate.sh` — repository validation gate)
- [ ] typecheck passes (N/A — Python standard-library test module)
- [ ] unit tests pass (focused unittest command above)
- [ ] integration tests pass (N/A — subprocess harness is the integration boundary)
- [ ] app builds without error (N/A — tooling repository has no build pipeline)
