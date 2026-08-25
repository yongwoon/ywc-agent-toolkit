# Task: Runtime-Fit Wording Polish

## Summary

Clean Codex runtime wording in selected high-value skills while preserving behavior and examples.

## Implementation Steps

- [ ] Confirm target skills from the 2026-06-18 report.
  - Related AC/FR: AC3, FR-3
  - Contract / Behavior Change: Work only on high-value S7=3 candidates confirmed by the report, or record why a listed target is skipped.
  - Verification Command / Evidence: Cite the report section that identifies S7 runtime-fit candidates.
- [ ] Inspect each selected `SKILL.md` for Codex runtime mismatches.
  - Related AC/FR: AC3, FR-3
  - Contract / Behavior Change: Identify Claude-only phrasing, ambiguous slash invocation, workspace-specific absolute paths, or tool assumptions that do not fit Codex.
  - Verification Command / Evidence: `rg -n "Claude Code-only|Task\\(|subagent_type|tools/claude-code|/Users/|^/" <selected SKILL.md files>`
- [ ] Rewrite wording narrowly.
  - Related AC/FR: AC3, FR-3
  - Contract / Behavior Change: Preserve behavior, command examples, and user-facing intent; only clarify runtime-specific wording.
  - Verification Command / Evidence: Review `git diff -- codex/skills/ywc-plan/SKILL.md codex/skills/ywc-code-gen/SKILL.md codex/skills/ywc-finish-branch/SKILL.md codex/skills/ywc-refactor-clean/SKILL.md codex/skills/ywc-tdd-ritual/SKILL.md`.
- [ ] Run targeted mechanical scoring for touched skills.
  - Related AC/FR: AC3, FR-3
  - Contract / Behavior Change: Mechanical scoring must not regress touched skills.
  - Verification Command / Evidence: Run `score.py --target codex/skills --item <skill-name> --format markdown` for each touched skill.

## Task Verify

```bash
for item in ywc-plan ywc-code-gen ywc-finish-branch ywc-refactor-clean ywc-tdd-ritual; do
  python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item "$item" --format markdown
done
git diff -- codex/skills/ywc-plan/SKILL.md codex/skills/ywc-code-gen/SKILL.md codex/skills/ywc-finish-branch/SKILL.md codex/skills/ywc-refactor-clean/SKILL.md codex/skills/ywc-tdd-ritual/SKILL.md
```

Expected Passing Signal:

- Touched skills score without regression.
- Diff shows wording-only changes in selected `SKILL.md` files.

Pre-change Failing Evidence / Exception:

- The 2026-06-18 report identifies S7 runtime-fit wording candidates or records scorer limitations for candidates.

Contract/Test Evidence:

- No behavior-changing workflow steps are added or removed without explicit report evidence.

## Out of Scope

- Plugin sync; final sync is handled by `000021-010`.
- Eval fixture additions; those belong to `000020-040`.
