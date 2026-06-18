---
name: ywc-tdd-ritual
description: >-
  (ywc) Use when implementing any new feature, bug fix, or behavior change,
  before any production code is written. Enforces the RED → GREEN → REFACTOR
  cycle with a mandatory "watch the test fail" step and forbids "I'll write
  tests after" patterns. Triggers: "TDD", "tdd", "test first", "test-first",
  "테스트 먼저", "테스트 우선", "RED-GREEN", "regression test", "회귀
  테스트", "テスト先行", "テストファースト", "ywc-tdd-ritual", "ywc-code-gen
  --tdd" (delegation). Do not use for throwaway prototypes the user has
  explicitly opted out of (declared in same turn), debugging an existing
  test failure (use ywc-debug-rootcause), generated or config files, or
  for completion-claim verification (use ywc-verify-done — TDD is the
  writing discipline, ywc-verify-done is the claiming discipline).
---

# ywc-tdd-ritual

**Announce at start:** "I'm using the ywc-tdd-ritual skill to enforce RED → GREEN → REFACTOR with a watch-it-fail gate before any production code."

This skill is the canonical writing-time discipline for ywc. It exists because every implementation skill (`ywc-code-gen`, `ywc-sequential-executor`, `ywc-parallel-executor`) can run with or without TDD, and the cost of running without is borne later by `ywc-debug-rootcause`, `ywc-impl-review`, and CI — typically 3–10× the cost of writing the test first. Adapted from `superpowers:test-driven-development`, tightened to delegate completion claims to `ywc-verify-done` and root-cause work to `ywc-debug-rootcause`.

## The Iron Law

```text
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If production code was written before the test, delete it and start over from RED. "Adapt the existing code while writing the test" is the same as "writing the test after"; it produces a test biased by the implementation that does not actually catch defects.

## Rationalization Defense

When tempted to skip the cycle, check this table first:

| Excuse | Reality |
|---|---|
| "I'll write the test right after implementing — same result" | Tests written after the code pass immediately. A test that passes the first time it runs proves nothing — it might be testing the wrong thing, the wrong path, or the wrong assertion. You never saw it catch the bug, so it cannot be trusted to catch one later. Test-first forces the test to fail for the right reason first. |
| "Too simple to need a test" | "Simple" code is where unchecked assumptions land. The test takes 30 seconds; the bug found in production takes hours. There is no size threshold below which the gate stops applying. |
| "I already manually tested every edge case" | Manual testing is ad-hoc and leaves no artifact. The next change will re-introduce the bug because there is no automated guard. Manual coverage is not coverage. |
| "Deleting the X hours of implementation I already wrote is wasteful" | Sunk cost. The time is gone either way. The choice now is (a) delete and rewrite under TDD with high confidence, or (b) keep the unverified code and inherit a debugging debt that will cost more later. Keeping it is the more expensive option. |
| "I'll keep the code as reference while I write the test first" | "Reference" becomes "model to copy", which becomes "the test I built around the existing code" — i.e., a test-after with extra steps. Delete means delete. Implement fresh from the test. |
| "I need to explore the design first; TDD blocks exploration" | Exploration is fine. Treat the exploration as a spike — keep notes, then **throw away the spike code** before starting TDD. The TDD cycle begins from the test, not from the spike. |
| "The test setup is so big the cycle slows me down" | A test that needs a 200-line setup is signal that the design is wrong. Listen to the test: extract a seam, inject the collaborator, or simplify the interface. Hard-to-test code is hard-to-use code. |
| "I'll skip the 'watch it fail' step — I know it would fail" | The watch-it-fail step is not for the test, it is for **you**. It catches: (a) the test passing for an unrelated reason (e.g., the assertion is wrong), (b) typos that turn the test into a no-op, (c) the test exercising code that already exists. Without this step, the cycle silently degrades into test-after. |
| "I have 6 features to add — I'll TDD the hard one and skip the easy ones" | The easy ones are exactly where the bug hides, because attention is elsewhere. The discipline applies per feature, not per session. |
| "This is a refactor, no behavior change — tests not needed" | Refactor = same behavior, different structure. The existing test suite must pass before and after. If no test covers the surface being refactored, write the test first (RED on the *existing* behavior), then refactor under it. Refactoring without tests is rewriting. |

**Violating the letter of this discipline is violating the spirit.** The cycle is the only mechanism in the ywc workflow that catches design defects before they ship.

## The Red-Green-Refactor Cycle

```text
RED → Verify RED → GREEN → Verify GREEN → REFACTOR → Verify GREEN → Next
```

Each transition has a verification step that **must** be executed in the current message — no transition is silent.

### Step 1: RED — Write the failing test

Write one minimal test that captures **one** behavior the production code is required to exhibit.

**Requirements:**

- **One behavior per test.** If the test name contains "and", split it.
- **Clear, intention-revealing name.** "`rejects offset > total with 400`" beats "`pagination test 3`".
- **Real code paths.** Mocks are allowed only for boundaries the test cannot cross (network, clock, file system). Mocking the unit under test is forbidden — it tests the mock, not the code.
- **No production code yet.** If the test references a function that does not exist, that is fine — the import error counts as failure.

### Step 2: Verify RED — Watch it fail

```bash
<run the test, scoped to just the new test>
```

Confirm three things from the output:

1. The test ran (not skipped, not errored before reaching assertions).
2. The failure reason matches what was expected (the assertion fired, not a typo or missing import).
3. No other test broke — if the test runner shows new failures elsewhere, the test is interacting with shared state and must be fixed before advancing.

**If the test passes the first time it runs**, the test is wrong:

- It is testing existing behavior — the feature is already implemented, or
- The assertion is trivially satisfied (e.g., `expect(x).toBeDefined()` where `x` is always defined), or
- The test is reading a cached / stale value.

Fix the test. Do not advance to GREEN with a passing-on-first-run test.

### Step 3: GREEN — Write the minimal code

Write the simplest production code that makes the failing test pass.

**Requirements:**

- **Minimal.** No options the test does not exercise. No abstractions the test does not require. YAGNI applies hard here.
- **No bundled refactor.** Adjacent code that "could be cleaner" is not touched in this step. Save it for REFACTOR.
- **No additional tests.** This step makes the existing test green; new tests belong to the next cycle.

### Step 4: Verify GREEN — Watch it pass

```bash
<run the new test>
<run the broader suite to confirm no regression>
```

Confirm:

1. The new test passes.
2. The full suite passes (no other test broke).
3. The output is pristine — no errors, no warnings, no deprecation notices that were not there before.

If the broader suite breaks, the GREEN code is too aggressive (touched a public surface other tests rely on) or too narrow (mutated shared state). Either revert or extend the suite — never silence a failing test to advance.

### Step 5: REFACTOR — Clean up under green

Now, and only now, improve the implementation:

- Remove duplication.
- Improve names.
- Extract helpers if the same logic appears in 2+ places.
- Tighten types or invariants.

**No new behavior** during refactor. The same tests must pass after each edit. If a refactor breaks a test, the refactor changed behavior — revert and split into a separate cycle.

### Step 6: Verify after REFACTOR

Re-run the suite after the refactor. If it stays green, the cycle is complete. If a test breaks, treat as Step 5 violation.

### Step 7: Loop or hand off

If there are more behaviors to implement, return to Step 1 with the next test.
When all required behaviors are implemented, hand off to `ywc-verify-done` for the completion claim (build + lint + full test suite + per-claim evidence block).

## Output Format

The cycle produces three commit shapes per behavior, in this order. (Skip the REFACTOR commit when no cleanup was needed.)

| Stage | Commit message shape | Verification at commit time |
|---|---|---|
| RED | `test: <one-line behavior>` (tests fail at this commit) | Test fails for the expected reason |
| GREEN | `feat: <one-line behavior>` or `fix: <bug>` | New test passes; broader suite passes |
| REFACTOR | `refactor: <what was tightened>` | All tests still pass |

Per-stage verification blocks follow `ywc-verify-done`'s shape (command → exit code → claim). The RED commit's verification block proves the test failed; the GREEN commit's proves it passes; the REFACTOR commit's proves nothing broke.

When delegated from `ywc-code-gen --tdd`, the executor emits these three commits per behavior automatically and threads the verification block into its per-step report.

## Integration

- **Upstream callers**: user invocation; `ywc-code-gen` with `--tdd` flag (Step 7.5 enforces the cycle per generated module); `ywc-debug-rootcause` Phase 4 §1 (regression test for the bug).
- **Downstream**: `ywc-verify-done` (every Verify step uses its evidence-block format and forbidden-vocabulary rules); `ywc-debug-rootcause` (if the RED step itself uncovers an unexpected pre-existing failure, that is a Phase 1 finding — route there).
- **Pairs with**: `ywc-confidence-gate` (pre-cycle ≥90 confidence reduces RED rewrite churn); `ywc-impl-review` (downstream code review uses the test as the spec evidence).

## Validation Checklist

Before declaring a behavior complete, verify:

- [ ] A test for the behavior exists in the repository
- [ ] The test was **observed failing** in the current session for the expected reason (RED commit's verification block in this session's history)
- [ ] The production code was written **after** the test failed
- [ ] No "kept as reference" code was retained from a pre-TDD draft
- [ ] The GREEN code is minimal — every line traces to a test-required behavior
- [ ] The broader suite passes (per `ywc-verify-done`)
- [ ] If refactoring was performed, all tests stayed green throughout

## Common Mistakes

(Procedural failure modes specific to TDD. Behavioral rationalizations are in the table above — do not duplicate here.)

- **Treating a compile / import error as "test failed".** A test that errors before reaching its assertions has not exercised the production code. Fix the test setup (stub the missing import, then re-run) so the failure is at the assertion, not the import.
- **Writing the test against the implementation you secretly already drafted in your head.** The test reads the desired *behavior*, not the algorithm you imagine. If the test mentions a private helper name before that helper exists in the codebase, you are testing the implementation, not the contract.
- **Bundling the GREEN edit with a "while I'm here" fix in adjacent code.** Adjacent fixes mean the GREEN commit is no longer minimal, and you cannot bisect cleanly if the next cycle breaks. Save adjacent fixes for their own RED-GREEN-REFACTOR.
- **Letting a refactor introduce a "harmless" behavior tweak.** "It was already broken anyway" is not license to fix it in the refactor commit. Either write a RED for the new behavior or revert the tweak.
- **Skipping `ywc-verify-done` at the end of the cycle because "the cycle already verified it".** The cycle verifies one behavior; `ywc-verify-done` verifies the **claim** (build green, lint green, suite green, claim wording free of forbidden vocabulary). Both are required for completion.

## References

| Reference | Use when |
|---|---|
| [references/red-green-checklist.md](references/red-green-checklist.md) | Walking through the per-step entry / exit conditions during the cycle |
| [references/test-shape-cookbook.md](references/test-shape-cookbook.md) | Picking the right shape of test for the behavior (state vs interaction, unit vs integration, snapshot vs assertion) |
| `ywc-verify-done` | Per-step verification block shape (command + exit code + claim) |
| `ywc-debug-rootcause` | When an existing test starts failing during a cycle, route the investigation here before another fix attempt |
