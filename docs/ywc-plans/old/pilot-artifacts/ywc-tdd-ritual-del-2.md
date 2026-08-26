# Dispatch artifact: ywc-tdd-ritual (deleted body, run 2)

**Key**: claude-code/skills/ywc-tdd-ritual/SKILL.md:42-42
**Scenario**: I need help with the following: implementing any new feature, bug fix, or behavior change, before any production code is written.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: The request does not name an actual feature, bug, or behavior change to implement -- it restates the skill's own activation condition rather than describing concrete work. Step 1 of the ritual requires 'one minimal test that captures one behavior the production code is required to exhibit,' which is impossible to write without knowing what that behavior is, which repository/module it belongs to, or what the expected inputs/outputs/error conditions are. Inventing a placeholder behavior to keep moving would itself be a rationalization the skill explicitly guards against (fabricating scope is not listed as a legitimate exception, and doing so risks producing a test 'biased by' assumptions rather than a real requirement). The correct next action under this procedure is to ask a clarifying question before any test or code is written.

## Actions
- Read docs/ywc-plans/pilot-artifacts/variant-ywc-tdd-ritual-42-42.md (the only instruction source, per task constraints)
- Match user request against SKILL.md frontmatter trigger phrase ('implementing any new feature, bug fix, or behavior change, before any production code is written') -> confirms ywc-tdd-ritual applies
- Emit the mandated announce line: "I'm using the ywc-tdd-ritual skill to enforce RED -> GREEN -> REFACTOR with a watch-it-fail gate before any production code."
- Check request against the Iron Law and Step 1 (RED) requirement of 'one minimal test that captures one behavior' -> determine no concrete behavior, repo, file, or acceptance criterion was supplied
- Decide NOT to invent a placeholder feature or scaffold any test/code, since doing so would violate 'no production code (or speculative test) without a real, specified behavior' and would just be guessing at requirements
- Ask the user a clarifying question specifying exactly what is missing before any Step 1 work can start
- (Deferred, contingent on the user's answer) Read package.json / pyproject.toml / pytest.ini / go.mod in the target repo to infer the configured test runner per the Step 2 instruction: 'If the runner cannot be inferred from project config, ask the user before running'
- (Deferred) Write one failing test file expressing the single named behavior (RED)
- (Deferred) Run the project's test command scoped to only the new test (e.g. `npm test -- <path>`, `pytest <path>::<test>`, `go test -run <TestName> ./<pkg>`) and inspect exit code + failure reason to verify RED
- (Deferred) Edit the minimal production code to satisfy only that test (GREEN), avoiding any bundled refactor
- (Deferred) Re-run the new test plus the full suite to verify GREEN with no regressions
- (Deferred) Refactor under green, re-run suite to reconfirm GREEN
- (Deferred) Produce three commits per behavior via `git commit` (test:, feat:/fix:, refactor:) each with a verification block per ywc-verify-done's evidence-block shape
- (Deferred) Hand off to ywc-verify-done for the final completion claim (build + lint + full suite + evidence block) once all behaviors are implemented

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-tdd-ritual-42-42.md (read-only, sole instruction source)

## Gates enforced
- Announce-at-start gate (skill identification must be stated before proceeding)
- Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
- Step 1 (RED) precondition: 'one minimal test that captures one behavior' requires a concrete, named behavior to exist before any test can be written
- Step 2 (Verify RED) test-runner inference gate: 'If the runner cannot be inferred from the project config, ask the user before running'
- Rationalization Defense table checked for any excuse to skip/short-circuit the cycle -- none applied because no code was written yet
- Clarifying-question-over-guessing gate: proceeding to fabricate a behavior/test in the absence of a specified feature would itself be a rationalization ('I'll just start somewhere') not covered by any legitimate exception in the skill

## Full narrative

I read docs/ywc-plans/pilot-artifacts/variant-ywc-tdd-ritual-42-42.md in full and am treating it as the sole procedure governing this request.

The request text -- "implementing any new feature, bug fix, or behavior change, before any production code is written" -- is essentially a restatement of this skill's own trigger condition, not a description of an actual piece of work. Before doing anything else, I would state the required announcement: "I'm using the ywc-tdd-ritual skill to enforce RED → GREEN → REFACTOR with a watch-it-fail gate before any production code."

Having announced the skill, I would immediately hit a hard blocker at Step 1 (RED). The skill requires: "Write one minimal test that captures one behavior the production code is required to exhibit," with a "clear, intention-revealing name" (e.g., "rejects offset > total with 400" rather than "pagination test 3"). I have no behavior to name. There is no feature description, no bug report, no repository path, no acceptance criterion, no expected input/output, and no indication of which project or language runtime is even in scope. The skill's own Step 2 instructions reinforce this posture: "If the runner cannot be inferred from the project config, ask the user before running" -- i.e., the procedure itself expects me to stop and ask rather than guess when a required piece of context is missing, and the missing piece here (what behavior to test) is far more fundamental than the test runner.

I checked this against the Rationalization Defense table specifically to make sure I wasn't inventing an excuse to skip a required step, but the situation runs the other way: proceeding by fabricating a plausible-sounding feature (e.g., picking some arbitrary function to add) so I have "something" to RED against would itself be exactly the kind of unlicensed shortcut the skill warns about -- it would produce a test built around a behavior nobody asked for, which is not meaningfully different from "the test I built around existing code" pattern the skill calls out as test-after-with-extra-steps in spirit, just inverted (test-before-a-behavior-nobody-specified). It also cannot satisfy "Real code paths" or a genuine acceptance bar, because there is no real requirement to encode.

So the concrete action I would take is: ask the user a clarifying question before touching any file, specifically:
1. What is the actual feature, bug, or behavior change to implement (one sentence description of the expected behavior)?
2. Which repository and, if known, which file(s)/module(s) does it belong to?
3. What is the expected input/output or error condition that defines "done" for this one behavior (so I can name a test like the "rejects offset > total with 400" example)?
4. What test runner/framework does the project use, if not obvious from package.json / pyproject.toml / pytest.ini / go.mod (so Step 2's "watch it fail" command can be chosen correctly)?

I would not create any test file, would not touch any production file, and would not run any test or build command until those answers come back, because every subsequent step in the ritual (RED test content, the "watch it fail" command, the minimal GREEN implementation, the REFACTOR pass, and the eventual three-commit output shape test:/feat:/refactor: with verification blocks) is defined relative to "the behavior," and no behavior has been specified yet.

Once the user supplies that information, the concrete sequence I would then execute is: read the relevant existing source/test files and the project's dependency manifest to confirm the test runner; write one new test file (or add one test to an existing suite) expressing exactly the named behavior; run only that test via the inferred runner command and inspect the failure reason to confirm genuine RED (not an import/compile error passed off as a test failure); write the minimal production code edit to make only that test pass; re-run the new test plus the full suite to confirm GREEN with zero new regressions; perform any needed REFACTOR pass and re-verify GREEN; and finally produce the three-stage commit sequence (test: ..., feat:/fix: ..., refactor: ...) each carrying a ywc-verify-done-shaped verification block, before handing off the completion claim to ywc-verify-done. But none of that begins until the missing behavior is named, per the clarifying question above.
