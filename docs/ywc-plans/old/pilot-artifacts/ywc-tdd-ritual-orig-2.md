# Dispatch artifact: ywc-tdd-ritual (original body, run 2)

**Key**: claude-code/skills/ywc-tdd-ritual/SKILL.md:42-42
**Scenario**: I need help with the following: implementing any new feature, bug fix, or behavior change, before any production code is written.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The request as given is not an actual concrete feature/bug/behavior description — it restates the skill's own trigger condition verbatim ("implementing any new feature, bug fix, or behavior change, before any production code is written") without naming what behavior is to be implemented or which project/repo it lives in. Step 1 (RED) of the ritual requires writing "one minimal test that captures one behavior the production code is required to exhibit" — there is no behavior specified to write a test against, so I cannot begin the cycle. I would ask a clarifying question rather than fabricate a behavior to test.

## Actions
- Read claude-code/skills/ywc-tdd-ritual/SKILL.md (already done)
- Announce skill invocation per the mandated announce-at-start line
- Ask a clarifying question: what specific feature/bug/behavior-change is being implemented, and which project/repo (to identify test runner)
- (Pending answer) Read package.json / pyproject.toml / go.mod or equivalent to infer test runner per Step 2's instructions
- (Pending answer) Write one new test file/case capturing exactly one required behavior (RED)
- (Pending answer) Run the scoped test command (e.g. `npm test -- <path>`, `pytest <path>::<test>`, `go test -run <TestName> ./<pkg>`) and inspect output for correct failure reason (Verify RED)
- (Pending answer) Edit/create the minimal production code file to satisfy only that test (GREEN)
- (Pending answer) Re-run the scoped test plus the full suite (Verify GREEN)
- (Pending answer) Refactor under green, re-run full suite (Verify after REFACTOR)
- (Pending answer) Create three commits per behavior: `test: <behavior>`, `feat:/fix: <behavior>`, `refactor: <what tightened>` (skip refactor commit if none needed)
- (Pending answer) Repeat RED→GREEN→REFACTOR per remaining behavior
- (Pending answer) Hand off to ywc-verify-done for the final completion claim (build + lint + full suite + evidence block)

## Files touched
- claude-code/skills/ywc-tdd-ritual/SKILL.md (read only)

## Gates enforced
- Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
- Step 2 Verify RED gate (test must fail for the expected reason, not typo/skip/error)
- Step 4 Verify GREEN gate (new test passes + full suite passes + pristine output)
- Step 6 Verify-after-REFACTOR gate (suite stays green)
- Rationalization Defense table check before any 'skip the test' impulse
- Ask-before-running gate: test runner must be asked about if it cannot be inferred from project config
- Downstream handoff gate to ywc-verify-done for the completion claim

## Full narrative

I would begin by announcing the skill exactly as the procedure requires: "I'm using the ywc-tdd-ritual skill to enforce RED → GREEN → REFACTOR with a watch-it-fail gate before any production code."

Immediately after that, I would stop and ask a clarifying question rather than proceed, for a concrete procedural reason: the ritual's Step 1 (RED) requires writing "one minimal test that captures one behavior the production code is required to exhibit." The request I received — "implementing any new feature, bug fix, or behavior change, before any production code is written" — names no actual behavior, no file, no repository, and no acceptance criterion. It is the trigger condition for the skill, not a task the skill can act on. Writing a test requires knowing what it must assert; I have nothing to assert yet. So I would ask two things directly:

1. "What specific feature, bug, or behavior change do you want implemented — described concretely enough that I can name one behavior to write a test against (e.g., 'reject offset > total with a 400')?"
2. "Which repository/project is this in, so I can identify the configured test runner?" — this maps directly to the procedure's Step 2 instruction: "If the runner cannot be inferred from the project config, ask the user before running," which covers npm/pnpm/yarn (via the `test` script in `package.json`), pytest (via `pyproject.toml`/`pytest.ini`), or `go test`.

I would explicitly decline to invent a placeholder behavior or a placeholder test just to have something to show — that would violate the Iron Law's spirit ("NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST") by producing a test that doesn't correspond to any real required behavior, which the Rationalization Defense table calls out under "writing the test against the implementation you secretly already drafted in your head."

Once the user supplies a concrete behavior and confirms the project, here is exactly what I would do, in order, with no step skipped or silently merged:

- Read the project's `package.json` (or `pyproject.toml`/`pytest.ini`, or `go.mod`) to confirm the test command and existing test-directory conventions, so the new test lands in the right location using the right runner invocation.
- Write one new test — a single file edit or new test file — that names one behavior only (splitting immediately if the description contains "and"), using a clear intention-revealing test name, hitting real code paths, and mocking only true boundaries (network/clock/filesystem) — never mocking the unit under test itself. I would not touch any production file in this step. If the test references a not-yet-existing function, that's acceptable — the import/compile error is a valid RED as long as it's noted and not confused with the assertion actually firing.
- Run the scoped test only (`npm test -- <path>`, `pytest <path>::<test>`, or `go test -run <TestName> ./<pkg>` depending on the stack identified above) via Bash, and read the output to confirm three things per the procedure: the test actually ran (not skipped/errored before assertions), the failure matches the expected reason (assertion fired, not a stray typo or missing import), and no unrelated test broke. If the test passes on the first run, I would treat that as a defective test per the procedure and rewrite it rather than advance.
- Only after a confirmed, correctly-reasoned RED would I write the GREEN code: the smallest production-code edit that makes that one test pass — no extra options, no speculative abstractions, no drive-by cleanup of adjacent code, and no additional tests bundled in.
- Run the scoped test again plus the full suite via Bash, and confirm the new test passes, the full suite is green, and there are no new warnings/errors in the output. If the broader suite breaks, I would revert the GREEN change rather than silence or skip the newly-broken test.
- Only then would I refactor (dedupe, rename, extract helpers used 2+ times, tighten types) with no behavior change, re-running the full suite after the refactor to confirm it stays green; any test breakage at this stage would be treated as a behavior change and reverted, not patched.
- I would produce up to three commits per behavior in this exact shape and order: `test: <one-line behavior>` (captured while red), `feat: <behavior>` or `fix: <bug>` (captured green), and `refactor: <what was tightened>` (only if cleanup actually happened) — each with a verification block (command → exit code → claim) in `ywc-verify-done`'s format.
- I would loop back to a fresh RED for the next behavior if more remain, and only when every required behavior for the requested change is implemented would I hand off to `ywc-verify-done` for the final completion claim (build + lint + full test suite + per-claim evidence), rather than declaring the work done myself inside this cycle.

Throughout, if at any point I noticed myself about to write production code before a test existed and failed for the right reason, or about to keep "reference" code from a pre-TDD draft, I would stop, delete that code, and restart the cycle from RED — per the Iron Law, doing otherwise is treated as equivalent to writing tests after the fact, which the procedure explicitly forbids regardless of how much implementation time that discards.
