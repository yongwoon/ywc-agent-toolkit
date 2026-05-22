# RED-GREEN-REFACTOR Step Checklist

Walk through the per-step entry / exit conditions during the cycle. Each step has explicit gates — do not advance until the exit condition is met.

## Step 1 — RED: Write the failing test

### Entry conditions

- [ ] The behavior to implement is named in one sentence
- [ ] No production code for this behavior exists yet (search the codebase before writing the test)
- [ ] If exploration was needed, the spike was discarded — no carry-over code

### The test

- [ ] One behavior per test (no "and" in the test name)
- [ ] Intent-revealing name (a future reader can guess the production code's purpose from the name alone)
- [ ] Real code paths (no mock of the unit under test; mock only the boundaries the test cannot cross — network, clock, file system)
- [ ] Minimal setup (if setup exceeds ~10 lines for a unit test, the design is too coupled — listen to the test and simplify before writing more)

### Exit condition

The test file exists, asserts the desired behavior, and references symbols (functions / classes / methods) that may not yet exist in the production code.

## Step 2 — Verify RED: Watch it fail

### Entry conditions

- [ ] Step 1 exited; test file committed locally (or stashed in a clean working tree)
- [ ] Test runner is configured for the project

### The run

```bash
<project test command> <path/to/test>
```

### Read the output

- [ ] The test actually ran (not skipped, not collection-error)
- [ ] The failure originated at the assertion line, not at imports / setup
- [ ] The failure message matches the expected mismatch (got X, expected Y)
- [ ] No other test broke as a side effect

### Decision

| Outcome | Action |
|---|---|
| Failed for the expected reason | Advance to Step 3 |
| Failed at import / setup | Fix the test setup, do **not** advance |
| Passed on first run | The test is wrong — fix it; do **not** advance |
| Other tests broke | The test mutated shared state — isolate, do **not** advance |

### Exit condition

The test runner output, in this message, shows the new test failing with the expected assertion message, and no other test broke.

## Step 3 — GREEN: Write the minimal code

### Entry conditions

- [ ] Step 2 exit condition satisfied
- [ ] The test's exact failure message has been read; the production code knows precisely what it must produce

### The implementation

- [ ] Smallest production change that turns the failing test green
- [ ] No options the test does not exercise (no `maxRetries`, no `backoff`, no `onError` callback unless a test demands it)
- [ ] No "while I'm here" fixes in adjacent code
- [ ] No additional tests in this commit

### Exit condition

The production code exists in the codebase and is committed locally (not yet verified).

## Step 4 — Verify GREEN: Watch it pass

### The run

```bash
<project test command> <path/to/test>
<project test command>                # full suite
<project lint command>                # optional but recommended
```

### Read the output

- [ ] The new test passes
- [ ] The broader suite passes (no test that was passing before now fails)
- [ ] Output is pristine — no errors, no new warnings, no deprecation notices that were not there before

### Decision

| Outcome | Action |
|---|---|
| New test passes, suite passes, output clean | Advance to Step 5 |
| New test passes, suite broken | The GREEN edit was too aggressive — revert and narrow the change |
| New test still fails | The GREEN edit was too narrow — extend, do **not** weaken the test |
| New warning appeared | Read the warning; if it indicates a real new issue, fix before advancing |

### Exit condition

A verification block per `ywc-verify-done` is surfaced in this message showing the test command exit 0 and the new test name in the pass list.

## Step 5 — REFACTOR: Clean up

### Entry conditions

- [ ] Step 4 exit condition satisfied
- [ ] All tests are green

### The refactor

- [ ] Remove duplication that the GREEN step introduced
- [ ] Improve names of new identifiers
- [ ] Extract helpers if the same logic appears in 2+ places
- [ ] Tighten types or invariants where the GREEN step left them loose

### Forbidden during refactor

- [ ] No new behavior (the same tests must pass before and after each edit)
- [ ] No new tests
- [ ] No "while I'm here" cleanup in unrelated code

### Exit condition

The implementation is the smallest, clearest version that still satisfies the same tests.

## Step 6 — Verify after REFACTOR

### The run

```bash
<project test command>
```

### Read the output

- [ ] Every test that passed at Step 4 still passes
- [ ] No new warnings

### Decision

| Outcome | Action |
|---|---|
| All tests pass | Cycle complete |
| Any test broke | The refactor changed behavior — revert immediately; if the new behavior is desired, restart from Step 1 with a new RED |

### Exit condition

A second verification block (per `ywc-verify-done`) is surfaced showing the suite still green after the refactor edits.

## Step 7 — Loop or hand off

### Loop

If there are more behaviors required for the feature, return to Step 1 with the next behavior. Each behavior gets its own RED-GREEN-REFACTOR cycle; do not combine.

### Hand off

When all required behaviors are implemented:

1. Run `ywc-verify-done` for the completion claim — full build, full lint, full test suite, evidence block per claim.
2. If this skill was invoked by `ywc-code-gen --tdd`, return control with the three per-behavior commits (RED, GREEN, REFACTOR) and the final `ywc-verify-done` block.
3. If this skill was invoked by `ywc-debug-rootcause` Phase 4 §1, the regression test from Step 1 plus the fix from Step 3 satisfy that phase's exit condition.
