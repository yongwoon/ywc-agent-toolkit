# yw-000019-010-domain-review-learnings-mining-contract — Implementation Checklist

## Prerequisites
- [ ] Confirm the source spec is `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md`.

## Allowed Edit Scope
- [ ] Stay within the three files declared in `README.md` Ownership.
- [ ] Stop before editing the new skill or generated package.

## Stop Conditions
- [ ] Stop if the existing confirmation gate or source grammar requires a behavior change beyond `mining`.
- [ ] Stop if a shared catalog write path is requested.

## Hardening Gate
- [ ] Classify as contract documentation and eval-fixture behavior change.
- [ ] Record existing contract-eval coverage before production-document edits.
- [ ] Treat the README Interface Contract as bounded worker input; return `NEEDS_CONTEXT` on mismatch.
- [ ] Apply the duplicate-sensitive side-effect fields in README; no runtime write code is introduced.

## Implementation Steps
- [ ] Update `codex/skills/ywc-review-learnings/SKILL.md` so `--source mining` is an allowed update source with aggregated distinct-PR provenance and confirmation requirements.
- [ ] Update `codex/skills/ywc-review-learnings/references/capture-sources.md` with the mining evidence path, representative-evidence rule, and conservative drop behavior.
- [ ] Add a mining-source eval fixture covering confirmed changeset, rule, why, polarity, target, representative evidence, and distinct PR list.
- [ ] Verify existing `feedback`, `review`, and `pr` source wording remains intact and no direct catalog-write authority is added.

## Task Verify
- [ ] `rg -n -- "--source mining|source.*mining|distinct-PR|confirmed changeset|representative evidence" codex/skills/ywc-review-learnings/SKILL.md codex/skills/ywc-review-learnings/references/capture-sources.md`
- [ ] `python3 -m json.tool codex/skills/ywc-review-learnings/evals/evals.json >/dev/null`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`

## Verification
- [ ] lint: N/A — no package lint command exists for this Markdown/JSON-only change
- [ ] typecheck: N/A — no typed application source
- [ ] tests: `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] build: N/A — repository distributes documentation and shell skills
