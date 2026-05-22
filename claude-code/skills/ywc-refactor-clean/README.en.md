# ywc-refactor-clean

Dead-code removal skill backed by detection tools (knip / depcheck / ts-prune / vulture / deadcode / cargo-udeps). Findings are sorted into SAFE / CAUTION / DANGER tiers, deleted per-item with a scoped test run before and after each deletion, then closed out with a Verification Report that follows `ywc-verify-done`'s evidence-block format. Behavior changes (e.g., duplicate consolidation that needs semantics reconciliation) are explicitly out of scope and route to `ywc-tdd-ritual` + `ywc-code-gen`.

## Localized Versions

- [한국어 (entry)](./README.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)

## When to Use

- The user says "remove dead code", "run knip", "clean unused imports"
- After a sprint, as a scheduled monthly hygiene pass on its own branch
- When `ywc-onboard-repo` detects that dead-code accumulation blocks architecture comprehension in a freshly-entered repo

## How to Invoke

```bash
/ywc-refactor-clean --scope src/ --tier safe
```

Or in natural language:

> "clean up the dead code"
> "run knip and remove the safe findings"

## The Iron Law

**Never delete without three witnesses**: (1) detection tool flags it, (2) grep finds zero references, (3) tests stay green after each batch.

## Inputs

- (optional) `--scope <dir>` — restrict detection + deletion to a path (default: repo root)
- (optional) `--tier safe | safe+caution | all` — stop after the named tier (default: `safe`)
- (optional) `--dry-run` — emit a report without mutating files
- (optional) `--skip-verify-done` — only valid when the upstream caller handles verify-done itself

## Outputs

- A per-item commit series (`chore(cleanup): remove unused <symbol> (knip)`)
- A final Verification Report (Output Format — embeds `ywc-verify-done`'s evidence block)
- A list of DANGER-tier items not deleted (recommended for a separate PR)

## Related Skills

- `ywc-verify-done` — mandatory Step 7 handoff; supplies the PASS / FAIL evidence-block format
- `ywc-tdd-ritual` — escalation target when consolidation requires behavior reconciliation
- `ywc-code-gen` — behavior-changing cleanup belongs here, not this skill
- `ywc-confidence-gate` — borderline CAUTION ↔ DANGER classification via the 5-dimension rubric
- `ywc-onboard-repo` — upstream caller after entering a new repository
