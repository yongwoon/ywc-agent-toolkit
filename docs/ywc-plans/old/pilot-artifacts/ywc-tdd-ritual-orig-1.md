# Dispatch artifact: ywc-tdd-ritual (original body, run 1)

**Key**: claude-code/skills/ywc-tdd-ritual/SKILL.md:42-42
**Scenario**: I need help with the following: implementing any new feature, bug fix, or behavior change, before any production code is written.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The user's message restates the skill's own activation trigger ("implementing any new feature, bug fix, or behavior change, before any production code is written") rather than describing an actual feature, bug, or behavior to implement. The ywc-tdd-ritual procedure's Step 1 (RED) requires "one minimal test that captures one behavior the production code is required to exhibit" with a "clear, intention-revealing name," and Step 2 requires a known test runner (inferred from project config, or asked about explicitly if it cannot be inferred). Neither the target behavior nor the target project/runner is specified, so the RED step cannot begin. Per the Iron Law, no test and no production code may be written without that concrete behavior in hand, so the correct next action is to ask a clarifying question rather than to guess or scaffold something generic.

## Actions
- Read claude-code/skills/ywc-tdd-ritual/SKILL.md in full (only action taken)
- Recognize the user's message restates the skill's own trigger description rather than naming a concrete feature/bug/behavior
- Announce skill usage per the mandated opening line
- Check the Rationalization Defense table for applicable excuses (none apply — no code has been written yet)
- Determine that Step 1 (RED) cannot start because no single behavior is specified
- Ask a clarifying question instead of proceeding: request the concrete behavior, target repo/project, and test runner
- Withhold any Write/Edit/Bash calls until the clarifying question is answered (Iron Law: no production code, and no test either, without a defined behavior)
- Once clarified: identify target project + test runner (npm/pnpm/yarn test script in package.json, pytest config, or go test) — ask if not inferable
- Write one minimal failing test file for one behavior (RED)
- Run only that test via Bash using the project's configured runner and confirm it fails for the expected reason (Verify RED)
- Write minimal production code to pass the test (GREEN)
- Re-run the new test plus the full suite via Bash (Verify GREEN)
- Refactor under green, re-running the suite after each edit (REFACTOR + Verify)
- Create three git commits per behavior: test: ..., feat:/fix: ..., refactor: ... (skip refactor commit if none needed)
- Loop Step 1-6 for additional behaviors, or hand off to ywc-verify-done for the completion claim

## Files touched
- claude-code/skills/ywc-tdd-ritual/SKILL.md (read only)

## Gates enforced
- Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
- Step 1 RED prerequisite: one behavior per test with a clear, intention-revealing name — blocked because no behavior was specified
- Step 2 Verify RED: 'If the runner cannot be inferred from the project config, ask the user before running' — test-runner identity also unknown
- Rationalization Defense table check before any skip
- Downstream handoff gate to ywc-verify-done deferred until behaviors exist

## Full narrative

I'm using the ywc-tdd-ritual skill to enforce RED → GREEN → REFACTOR with a watch-it-fail gate before any production code.

Before doing anything else I ran the Rationalization Defense table in my head against this request — none of the listed excuses ("too simple," "I already tested manually," "I'll write the test after," etc.) apply, because no code exists yet at all. So the discipline isn't being resisted; the problem is upstream of it.

Looking at what was actually asked: "implementing any new feature, bug fix, or behavior change, before any production code is written" is not a feature, bug, or behavior — it's a restatement of the skill's own trigger condition (word-for-word close to the SKILL.md description's opening clause). There is no concrete behavior here for Step 1 (RED) to target. The skill is explicit that RED requires "one minimal test that captures one behavior the production code is required to exhibit," with a "clear, intention-revealing name" like `rejects offset > total with 400` — I have nothing like that to write. Step 2 (Verify RED) additionally requires knowing the project's configured test runner (npm/pnpm/yarn `test` script, pytest, `go test`, etc.), and the skill says explicitly: "If the runner cannot be inferred from the project config, ask the user before running." Given this repository is a multi-project workspace (genbatime, homepage, our-assets-lp, beacon, etc., per the root CLAUDE.md) with different stacks and package managers, I also don't know which project this even applies to.

So rather than fabricate a placeholder feature or scaffold a speculative test just to "do something," I would stop and ask a clarifying question back to the user, something like: "Could you specify the concrete feature, bug fix, or behavior change you'd like implemented — including the expected inputs/outputs or the bug's reproduction steps — and which project in this workspace it belongs to? I also need to confirm the test runner (e.g., the `test` script in that project's `package.json`, or its pytest/go test configuration) if it isn't obvious from the project's config." I would not call Read, Write, Edit, or Bash beyond what I already did to load the skill file, because there is nothing yet to test or implement.

Once that clarification came back with an actual behavior (say, "add input validation that rejects a negative `offset` param with a 400" in a specific project), the narrated procedure would be:

1. Read the relevant existing test file(s) and the target production module (e.g., via Read) to understand current shape and pick the exact assertion.
2. Confirm the test runner from that project's config (`package.json` "test" script for genbatime/homepage/our-assets-lp, or pytest/go equivalents elsewhere) rather than assuming.
3. RED — create or edit one test file with a single new test, one behavior, named descriptively (e.g., `rejects offset < 0 with 400`), using real code paths and mocking only true boundaries (network/clock/filesystem).
4. Verify RED — run only that new test via Bash using the project's exact configured command (e.g., `npm test -- <path>` inside the appropriate Docker container per this repo's CLAUDE.md, since genbatime/homepage/our-assets-lp commands are prefixed with `docker exec <container>`), and confirm from the output that it ran, failed for the expected reason (assertion fired, not an import/typo error), and nothing else broke.
5. GREEN — write the minimal production code change (Edit/Write) that makes only that test pass, with no bundled refactor and no extra tests.
6. Verify GREEN — re-run the new test plus the full suite via Bash, confirm both pass cleanly with no new warnings.
7. REFACTOR — clean up (dedupe, rename, extract) under green, re-running the suite after each edit; revert and split into a new cycle if anything breaks.
8. Verify after REFACTOR — final suite run to confirm still green.
9. Commit in three shapes per behavior via `git commit`: `test: <behavior>` (RED, tests failing at that commit), `feat: <behavior>` or `fix: <bug>` (GREEN), `refactor: <what was tightened>` (skipped if no cleanup was needed) — each with the verification block shape (command → exit code → claim) that `ywc-verify-done` defines.
10. Loop back to Step 1 for the next behavior if more remain.
11. When all behaviors for the request are done, hand off to `ywc-verify-done` for the completion claim (build + lint + full test suite + per-claim evidence block) rather than declaring completion myself inside this skill.

But none of steps 1–11 can start yet — they're contingent on the clarifying answer. As things stand, the concrete first action is the clarifying question, not a tool call.
