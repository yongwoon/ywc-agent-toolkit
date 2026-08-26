# 000065-010-domain-results-artifacts-ablation — Implementation Checklist

## Prerequisites

- [ ] `000064-020-domain-isolated-runner-adapter` is completed and merged.

## Allowed Edit Scope

- [ ] Stay within result, ablation, test, and generated-run exclusion paths in `README.md`.
- [ ] Stop if changing runner invocation, fixture content, or GitHub workflow behavior is required.

## Stop Conditions

- [ ] Stop if a status is not exactly one of the five specified values.
- [ ] Stop if redaction cannot occur before artifact persistence.
- [ ] Stop if a candidate decision lacks six paired trials, same case/model/CLI metadata, or complete costs.
- [ ] Stop if summary writes need a repository-wide locking mechanism beyond evaluator ownership.

## Hardening Gate

- [ ] Classify this task as behavior change touching sensitive artifact retention and shared mutable reports.
- [ ] Add failing tests for oversized artifact, secret redaction, duplicate run ID, incomplete cost, and insufficient trials.
- [ ] Record result JSON and ablation decision interface contracts before implementation.
- [ ] Apply shared-state hardening with atomic summary writes and repeat-safe pruning.
- [ ] Require full implementation review before `DONE`.

## Implementation Steps

- [ ] Define result record/status serialization in `results.py`.
  - [ ] Record run ID, profile, case, attempt, duration, CLI version/arguments, target/dependency set, verdicts, and activation observability.
  - [ ] Exclude credentials, raw environment, controllable unsupported seed fields, and unbounded transcripts.
  - [ ] Ensure `SKIPPED_UNAVAILABLE` and `ERROR` cannot update baselines or count as quality passes.
- [ ] Implement bounded artifact lifecycle.
  - [ ] Delete successful workspaces immediately.
  - [ ] Retain failed workspaces only for explicit opt-in, cap per-run content at 10 MB, redact before write, and prune after seven days.
  - [ ] Write machine-readable `summary.json` and human report data under the documented run root.
- [ ] Implement metrics and paired ablation aggregation in `ablation.py`.
  - [ ] Omit trigger precision/recall when activation selection is unavailable.
  - [ ] Aggregate with/without arms only across identical case/model/CLI metadata.
  - [ ] Emit `CANDIDATE_FOR_REVIEW` only for six paired trials, no more than one additional without-skill failure, complete cost data, and human approval; otherwise emit `INCONCLUSIVE`.
- [ ] Add result/redaction/retention/aggregation tests and generated artifact ignore rules.

## Task Verify

- [ ] `python3 -m unittest discover -s .codex/skills/ywc-codex-toolkit-eval/scripts -p 'test_results.py'`
- [ ] Run fake six-paired-trial fixtures for both complete-cost candidate and incomplete-cost inconclusive outcomes.

## Verification

- [ ] Result and ablation tests pass.
- [ ] `bash scripts/validate.sh` passes.
- [ ] Successful workspaces and secret-bearing fields are absent from persisted records.
