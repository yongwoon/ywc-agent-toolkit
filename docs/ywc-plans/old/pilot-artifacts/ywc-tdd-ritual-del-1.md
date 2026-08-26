# Dispatch artifact: ywc-tdd-ritual (deleted body, run 1)

**Key**: claude-code/skills/ywc-tdd-ritual/SKILL.md:42-42
**Scenario**: I need help with the following: implementing any new feature, bug fix, or behavior change, before any production code is written.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: The request text — "implementing any new feature, bug fix, or behavior change, before any production code is written" — is the skill's trigger description, not an actual feature/bug specification. It names no target repository, no file, no expected input/output, no acceptance criterion, and no existing failing behavior to fix. Step 1 of the procedure requires writing "one minimal test that captures one behavior the production code is required to exhibit" with "a clear, intention-revealing name" — that is impossible to satisfy without knowing what behavior is being requested. Rather than inventing a behavior to test-drive (which the procedure does not license) or performing exploratory tool calls against an unspecified target, the correct move under this procedure is to stop before Step 1 and ask the user what they actually want built or fixed.

## Actions
- Read the single specified file via Read tool (done)
- Recognize the incoming request text matches the ywc-tdd-ritual activation trigger verbatim but contains no concrete feature/bug/behavior specification
- Escalate: ask a clarifying question instead of proceeding to Step 1 (RED)
- No Bash, Write, Edit, Grep, or Glob calls made or planned until the missing behavior spec is supplied

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-tdd-ritual-42-42.md (read only)

## Gates enforced
- Step 1 (RED) precondition: 'one minimal test that captures one behavior the production code is required to exhibit' — cannot be satisfied without a stated behavior
- Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST — cannot even reach the test-writing stage without a target
- Rationalization Defense table checked — no excuse was raised, so this is not a skip-the-cycle situation, it's a missing-input situation
- Announce-at-start requirement noted but not yet issued, since issuing it would falsely signal the cycle is starting when it cannot

## Full narrative

I read the procedure file at docs/ywc-plans/pilot-artifacts/variant-ywc-tdd-ritual-42-42.md in full, using only the Read tool, and took its contents as the entire governing instruction set (the ywc-tdd-ritual skill: enforce RED → GREEN → REFACTOR with a mandatory watch-it-fail gate before any production code, Iron Law "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST").

Here is exactly what I would do next, concretely, if this were live.

First, I'd check whether the incoming request actually gives me something to test-drive. It doesn't. "I need help with the following: implementing any new feature, bug fix, or behavior change, before any production code is written" restates the skill's own trigger condition — it names no repository, no module, no function, no bug report, no acceptance criterion, and no expected input/output pair. Step 1 of the cycle requires "one minimal test that captures one behavior the production code is required to exhibit," with "a clear, intention-revealing name" (the skill's own example: "`rejects offset > total with 400`" beats "`pagination test 3`"). I have no behavior to name. I have nothing to assert on, no function signature to import-and-fail against, and no project even identified (I don't know if this is genbatime, homepage, our-assets-lp, beacon, or some other repo entirely — each has a different test runner: Vitest for genbatime, presumably a different setup elsewhere).

I would not fabricate a placeholder feature to keep the ritual moving — the procedure explicitly forbids writing a test "against the implementation you secretly already drafted in your head," and inventing a feature out of thin air is the same failure mode one level up: it would produce a test that isn't grounded in an actual requirement, which is exactly the kind of low-signal test the Iron Law exists to prevent.

I'd also check the Rationalization Defense table before deciding how to respond, since that table is the first thing to consult "when tempted to skip the cycle." None of its ten entries apply here — this isn't someone offering an excuse to skip TDD, it's simply a missing input. So this isn't a case of enforcing the discipline against a user trying to shortcut it; it's a case where I structurally cannot enter Step 1 at all.

Given that, I would not issue the mandated start-of-skill announcement ("I'm using the ywc-tdd-ritual skill to enforce RED → GREEN → REFACTOR...") yet, because doing so would imply the cycle is underway when it cannot begin. I would not run any Bash commands (no test runner invocation — there is nothing to run RED against), not create or edit any test file, not touch any production file, and not attempt to infer a runner from package.json/pyproject.toml/go.mod since I don't even know which project directory the user means.

Instead, I would ask a clarifying question along these lines: "Could you tell me the specific feature, bug, or behavior change you'd like implemented, and which project/repository it belongs to? Specifically I'd need: (1) the expected behavior in concrete terms — what input leads to what output, or what currently-wrong behavior should change to what; (2) the target file(s) or module the behavior belongs to, if known; (3) confirmation this isn't a throwaway prototype you've explicitly opted out of TDD for. With that, I'll write one minimal failing test first, run it to confirm it fails for the right reason, then implement the minimal code to pass it, following RED → Verify RED → GREEN → Verify GREEN → REFACTOR → Verify GREEN."

Only once the user supplies a concrete target would I proceed into the actual mechanics the procedure specifies: identify the project's test runner from its config (e.g., `npm test -- <path>` for a Vitest/Jest project, `pytest <path>::<test>` for Python, `go test -run <TestName> ./<pkg>` for Go); write one test file or one test case in an existing test file naming one behavior; run only that new test via Bash and confirm from its output that it ran, failed for the expected assertion reason (not a stray import/typo error), and didn't cascade into unrelated failures; then, and only then, write the minimal production code; re-run the same test plus the broader suite via Bash to confirm both are green with clean output; then do a REFACTOR pass under green, re-verifying after; and finally produce the three commit shapes (`test: <behavior>`, `feat:`/`fix: <behavior>`, `refactor: <what was tightened>`) each with its own command → exit-code → claim verification block, before handing off to `ywc-verify-done` for the completion claim. But none of that can start until the missing behavior specification is provided, so the first and only action here is the clarifying question.
