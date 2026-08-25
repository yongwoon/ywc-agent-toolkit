# 000077-010-test-context-safety-evaluation-matrix — Implementation Checklist

## Prerequisites
- [ ] All five Phase `000076` implementation tasks are merged.

## Allowed Edit Scope
- [ ] Edit only affected `codex/skills/*/evals/evals.json` files and explicitly cited shared fixtures.

## Stop Conditions
- [ ] Stop if a case cannot state expected status, downstream-call count, and handoff outcome.
- [ ] Stop if a fixture requires raw response, transcript, chain-of-thought, or raw tool output.
- [ ] Stop if an eval case silently accepts a guessed artifact path or prompt fallback.

## Hardening Gate
- [ ] Start from failing focused cases for every matrix row.
- [ ] Record the fixture interface and expected terminal-status contract.
- [ ] Require full review because the matrix guards privacy and authority boundaries.

## Implementation Steps
- [ ] Add plan/spec-ready Result parser cases for exact fields, duplicates, missing fields, invalid roots, and non-Markdown artifacts.
- [ ] Add agentic cases for Small/Medium/Large routing, guessed-path rejection, missing `--mode`/`--lang`/`--suggestions`/`--resume-disposition`, and zero downstream calls.
- [ ] Add suggestion closure and sequential/parallel prompt-closure cases for resume, conflicts, CI wait/timeout, and URL policy.
- [ ] Add handoff location, atomic failure preservation, malformed/stale/mismatched recovery, and checkpoint/task-source fallback cases.
- [ ] Add Claim cap, evidence, independent/dependent isolation, and recursive forbidden-field rejection cases.

## Task Verify
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `python3 -m json.tool codex/skills/ywc-agentic/evals/evals.json >/dev/null`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] all focused eval cases pass
- [ ] install inventory and structure validation remain green

## Implementation Notes

