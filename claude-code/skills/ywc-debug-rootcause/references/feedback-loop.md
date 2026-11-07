# Feedback Loop Construction (Phase 1)

A **tight**, **red-capable** loop is the core of every investigation. With one, bisection, hypothesis testing, and instrumentation all have a signal to consume; without one, reading code only produces theories. Spend disproportionate effort here, and keep going when the first idea fails.

Adapted from `mattpocock/skills` `diagnosing-bugs` Phase 1.

## Ways to construct a loop (try roughly in this order)

| # | Loop | Use when |
|---|---|---|
| 1 | **Failing test** at whatever seam reaches the bug (unit / integration / E2E) | A test seam reaches the failing code path |
| 2 | **curl / HTTP script** against a running dev server | The symptom is an API response |
| 3 | **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot | The code path is reachable from a command |
| 4 | **Headless browser script** (Playwright / Puppeteer) asserting on DOM / console / network | The symptom only shows in the UI |
| 5 | **Replay a captured trace** — save a real request / payload / event log to disk, replay it through the code path in isolation | Production-only input shape |
| 6 | **Throwaway harness** — a minimal subset of the system (one service, mocked deps) exercising the bug path with one call | Full boot is slow or unavailable |
| 7 | **Property / fuzz loop** — run 1000 random inputs and look for the failure mode | "Sometimes wrong output" |
| 8 | **Bisection harness** — automate "boot at state X, check" so `git bisect run` can drive it | The bug appeared between two known states |
| 9 | **Differential loop** — same input through old vs new version (or two configs), diff the outputs | A regression against a known-good version |
| 10 | **Human-in-the-loop script** — a bash script that prompts the human for each manual step and captures their observation | Last resort: a human must click |

## Tighten the loop

Treat the loop as a product. Once a loop exists:

- **Faster** — cache setup, skip unrelated init, narrow the test scope.
- **Sharper** — assert on the specific symptom, not "did not crash".
- **Deterministic** — pin time, seed the RNG, isolate the filesystem, freeze the network.

A 30-second flaky loop is barely better than none; a 2-second deterministic loop is tight.

## Non-deterministic bugs

The goal is a **higher reproduction rate**, not a clean repro. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50% reproduction rate is debuggable; 1% is not — keep raising the rate until it is.

## When no loop can be built

Stop and say so explicitly. List every loop type tried and why it failed. Ask the user for one of:

- (a) access to the environment that reproduces it;
- (b) a captured artifact with secrets redacted (HAR file, log dump, core dump, screen recording with timestamps);
- (c) permission to add temporary production instrumentation.

Do not advance to hypotheses without a loop.

## Completion criterion

Phase 1's loop step is done when you can name **one command** (script path, test invocation, curl) that you have **already run at least once**, with its invocation and output shown (secrets redacted), and that is:

- [ ] **Red-capable** — it drives the actual bug code path and asserts the user's exact symptom, so it goes red on this bug and green once fixed.
- [ ] **Deterministic** — same verdict every run (for flaky bugs: a pinned, high reproduction rate).
- [ ] **Fast** — seconds, not minutes.
- [ ] **Agent-runnable** — runs unattended (a human only through a loop-type-10 script).

## Minimise

Once the loop is red, shrink the scenario to the smallest one that still goes red. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut. Done when **every remaining element is load-bearing**: removing any one of them turns the loop green. The minimal repro shrinks the hypothesis space in Phase 3 and becomes the regression test in Phase 4.

## Redaction

Commands, outputs, and captured artifacts shown in the investigation carry secrets. Write `<REDACTED>` in place of every credential, build loops against environment variables so the credential stays in the environment, and quote only the lines of a captured artifact that carry the signal.
