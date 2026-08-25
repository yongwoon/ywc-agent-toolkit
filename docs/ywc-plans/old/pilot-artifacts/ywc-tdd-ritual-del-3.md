# Dispatch artifact: ywc-tdd-ritual (deleted body, run 3)

**Key**: claude-code/skills/ywc-tdd-ritual/SKILL.md:42-42
**Scenario**: I need help with the following: implementing any new feature, bug fix, or behavior change, before any production code is written.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: The request only restates the skill's trigger condition (\"implementing any new feature, bug fix, or behavior change, before any production code is written\") without naming an actual feature, bug, or behavior change, target repository, or affected file/module. The procedure's Step 1 (RED) requires writing \"one minimal test that captures one behavior the production code is required to exhibit,\" which is impossible without knowing what that behavior is. Rather than fabricate a target, I would ask a clarifying question before proceeding into the cycle.

## Actions
- Recognize the request matches the trigger conditions in the procedure's frontmatter ("implementing any new feature, bug fix, or behavior change, before any production code is written") and announce: "I'm using the ywc-tdd-ritual skill to enforce RED → GREEN → REFACTOR with a watch-it-fail gate before any production code."
- Check the request for a concrete target behavior to test — find none (the request only restates the trigger phrase, not an actual feature/bug/behavior description, target repo, or file)
- Ask a clarifying question instead of proceeding to Step 1 (RED), since the procedure requires 'one minimal test that captures one behavior the production code is required to exhibit' and no behavior, repo, module, or acceptance criteria was given
- Ask which test runner/framework applies (or state I will infer it from package.json / pyproject.toml / go.mod once the target repo is known) per the procedure's Step 2 runner-detection rule
- (Once behavior is specified) Read the target module/interface and any related existing tests to understand current code paths before writing the test
- (RED) Write one minimal failing test with an intention-revealing name capturing exactly one behavior; use mocks only at true boundaries (network/clock/filesystem), never mock the unit under test
- (Verify RED) Run only the new test via the project's configured runner (e.g. `npm test -- <path>`, `pytest <path>::<test>`, or `go test -run <TestName> ./<pkg>`) and confirm it ran, failed for the expected reason (assertion fired, not import/typo error), and did not break other tests
- (GREEN) Write the minimal production code — no extra options, no bundled refactor, no additional tests — that makes only that test pass
- (Verify GREEN) Re-run the new test plus the full suite; confirm the new test passes, the full suite is green, and output is free of new errors/warnings
- (REFACTOR) Clean up under green — remove duplication, improve names, extract helpers for logic duplicated 2+ times, tighten types — introducing no new behavior
- (Verify after REFACTOR) Re-run the full suite to confirm it stays green; treat any break as a refactor violation and revert
- Commit in three shapes per behavior: `test: <behavior>` (RED, tests fail), `feat: <behavior>` or `fix: <bug>` (GREEN, tests pass), `refactor: <what was tightened>` (still green) — skipping the refactor commit if no cleanup was needed
- Loop back to Step 1 for the next behavior if more remain
- On completion of all behaviors, hand off to ywc-verify-done for the completion claim (build + lint + full test suite + per-claim evidence block) rather than declaring done from inside this cycle
- If the RED step surfaces an unexpected pre-existing failure unrelated to the new test, stop and route that investigation to ywc-debug-rootcause instead of patching around it

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-tdd-ritual-42-42.md (read only, per instructions)

## Gates enforced
- Iron Law gate: no production code before a failing test exists
- clarifying-question gate: cannot enter Step 1 (RED) without a concrete behavior/feature/bug description, target repo, and affected module
- watch-it-fail gate (RED must fail for the expected assertion reason, not import/typo error, and must not break other tests)
- watch-it-pass + full-suite-green gate (GREEN)
- no-bundled-refactor gate during GREEN
- no-new-behavior gate during REFACTOR, with full-suite re-verification
- downstream handoff gate to ywc-verify-done for the completion claim (this skill's own cycle verification is not sufficient to declare the task done)
- reroute gate to ywc-debug-rootcause if RED uncovers a pre-existing unrelated failure

## Full narrative

I read the procedure at docs/ywc-plans/pilot-artifacts/variant-ywc-tdd-ritual-42-42.md in full (the ywc-tdd-ritual skill definition). It is a writing-time discipline that enforces RED → GREEN → REFACTOR with a mandatory "watch it fail" gate before any production code, and it matches the trigger language in the request almost verbatim.

Given the request, my first action would be to announce the skill per its explicit instruction: "I'm using the ywc-tdd-ritual skill to enforce RED → GREEN → REFACTOR with a watch-it-fail gate before any production code."

However, before doing anything else, I would stop and ask a clarifying question rather than start the cycle. The request as written — "implementing any new feature, bug fix, or behavior change, before any production code is written" — does not actually specify a feature, a bug, or a behavior change. It restates the skill's own activation trigger, not a task. The procedure's Step 1 (RED) is explicit that I must "write one minimal test that captures one behavior the production code is required to exhibit," with "a clear, intention-revealing name" (e.g. "rejects offset > total with 400"). I cannot write that test — or infer the correct test runner invocation, or identify the target file/module — without knowing what behavior is being requested. So I would ask something like: "Could you tell me which feature, bug fix, or behavior change you'd like implemented? Specifically I'll need: (1) a description of the desired behavior/acceptance criteria, (2) the repository and the module or file it belongs to, and (3) confirmation of the test framework in use if it isn't obvious from the project config (package.json's `test` script, pytest.ini/pyproject.toml, or go.mod)." I would not guess at a feature to avoid the ambiguity, since guessing wrong would mean writing a test against an invented behavior, which the procedure's Rationalization Defense table explicitly calls out as a way the discipline degrades.

Once a concrete behavior is supplied, here is precisely how I would execute the cycle:

1. I would inspect the target repository's config file (package.json, pyproject.toml, or go.mod) via Read to determine the test runner, since the procedure requires inferring it from project config and only asking the user if it cannot be inferred.

2. RED: I would create or edit the relevant test file (e.g. via Write for a new test file or Edit for an existing suite) with exactly one new test, named for the single behavior under test (not "and"-joined), using only real code paths — mocks reserved strictly for network/clock/filesystem boundaries, never for the unit under test itself. If the test references a not-yet-existing function, that's expected and acceptable at this stage.

3. Verify RED: I would run only that new test via Bash, using the project's inferred command shape — e.g. `npm test -- <path or name>`, `pytest <path>::<test>`, or `go test -run <TestName> ./<pkg>` — and inspect the output for three things: the test actually ran (not skipped/errored pre-assertion), the failure reason is the intended assertion firing (not an import error or typo), and no other tests regressed. If the test passed on first run, I would treat that as a broken test (testing existing behavior, a trivial assertion, or a stale read) and fix the test rather than advance.

4. GREEN: I would write the minimal production code via Edit/Write that makes only that failing test pass — no extra config options, no speculative abstractions, no drive-by refactors of adjacent code, and no additional tests bundled in.

5. Verify GREEN: I would re-run the new test and then the full suite via Bash (e.g. `npm test`, `pytest`, `go test ./...`) to confirm the new test passes, the full suite stays green, and there's no new warning/error noise. If the broader suite broke, I would either revert the GREEN change or extend the suite — never silence the failing test.

6. REFACTOR: Only once green, I would clean up — deduplicate, rename for clarity, extract a helper if the same logic showed up 2+ times, tighten types — introducing no new behavior in this pass.

7. Verify after REFACTOR: Re-run the full suite via Bash; if anything broke, treat it as a Step 5 violation, revert, and split the fix into its own RED-GREEN-REFACTOR cycle.

8. Commit in the three prescribed shapes using `git commit`: `test: <one-line behavior>` at the RED checkpoint (with the verification block showing the expected failure), `feat: <one-line behavior>` or `fix: <bug>` at GREEN (verification block showing new test + suite green), and `refactor: <what was tightened>` at REFACTOR if cleanup occurred (verification block showing nothing broke). I would follow the git-workflow conventions already established for this repository (conventional commit types, no `--no-verify`, no forced pushes).

9. If more behaviors remain for the same feature/bug, I would loop back to Step 1 with the next test rather than trying to cover multiple behaviors in one test.

10. Once all required behaviors are implemented, I would explicitly hand off to `ywc-verify-done` for the completion claim (build + lint + full test suite + per-claim evidence block) rather than declaring the work done from inside the TDD cycle itself — the procedure is explicit that the cycle verifies one behavior at a time, while `ywc-verify-done` verifies the overall claim.

11. If, during the RED step, an existing test in the suite turned out to already be failing for unrelated reasons, I would stop and route that specific investigation to `ywc-debug-rootcause` rather than absorb it into the current cycle or paper over it.

Throughout, I would not proceed to write any production code before a test exists and has been observed failing for the correct reason in the current session, and I would not retain any pre-existing draft implementation "as reference" — the procedure treats that as equivalent to test-after and requires deleting such code and restarting from RED.
