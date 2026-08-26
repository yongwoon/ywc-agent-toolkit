# Dispatch artifact: ywc-tdd-ritual (original body, run 3)

**Key**: claude-code/skills/ywc-tdd-ritual/SKILL.md:42-42
**Scenario**: I need help with the following: implementing any new feature, bug fix, or behavior change, before any production code is written.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The request restates the skill's own trigger condition ('implementing any new feature, bug fix, or behavior change, before any production code is written') but does not name a concrete project, feature, bug, or behavior to implement, nor which of the workspace's several projects (genbatime, homepage, our-assets-lp, beacon, etc.) it applies to. The skill's Step 1 requires 'one minimal test that captures one behavior the production code is required to exhibit,' which cannot be written without knowing the target. Rather than assume a project or invent a behavior, the correct move under the procedure is to ask a clarifying question first, then apply the RED-GREEN-REFACTOR cycle once the concrete target is known — this mirrors Step 2's own instruction to ask the user when the test runner cannot be inferred from project config.

## Actions
- Read claude-code/skills/ywc-tdd-ritual/SKILL.md in full (only tool used)
- Recognize the user request restates the skill's own activation trigger verbatim but names no concrete project, feature, bug, or behavior
- Ask a clarifying question instead of proceeding: which project in the workspace (genbatime / homepage / our-assets-lp / beacon / etc.), what the specific feature/bug/behavior change is, and whether a spec or task file already defines the acceptance criteria
- Once informed, announce the skill: 'I'm using the ywc-tdd-ritual skill to enforce RED → GREEN → REFACTOR with a watch-it-fail gate before any production code.'
- Determine the project's test runner from its config (e.g. Read package.json test script, pyproject.toml, or go.mod) rather than assume one; ask the user if it cannot be inferred
- If the project runs in Docker (genbatime, homepage, our-assets-lp per root CLAUDE.md), prefix every test command with docker exec <container>
- RED: Write one new test file or test case capturing exactly one required behavior, using Write/Edit, referencing not-yet-existing production symbols where needed
- Verify RED: run only the new test via Bash (e.g. docker exec genba-time-app pnpm test -- <path>, pytest <path>::<test>, or go test -run <Test> ./<pkg>) and confirm it fails for the expected assertion reason, not an import/setup error, and that no unrelated tests broke
- GREEN: Edit/Write the minimal production code needed to satisfy only that test, with no extra options or abstractions and no bundled cleanup
- Verify GREEN: re-run the new test plus the full suite via Bash, confirm pass with a clean (warning-free) output and no regressions elsewhere
- REFACTOR: clean up duplication/names/helpers under green with no behavior change, re-running the suite after each edit
- Verify after REFACTOR: re-run the full suite once more to confirm it stays green
- Commit in three shapes per behavior via git commit: 'test: <behavior>' (RED, tests failing at that commit), 'feat:'/'fix:' (GREEN), 'refactor:' (cleanup, skipped if none needed), each preceded by a command→exit-code→claim verification block
- Loop back to RED for the next behavior if more remain
- On completion of all behaviors, hand off to ywc-verify-done for the final completion claim (build + lint + full suite + evidence block) rather than self-declaring done
- Refuse to write any production code before a test has been observed failing in-session, and refuse to keep any pre-existing draft/spike code as 'reference' per the Iron Law and Rationalization Defense table

## Files touched
- /Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/claude-code/skills/ywc-tdd-ritual/SKILL.md

## Gates enforced
- Iron Law: no production code without a failing test first
- Watch-it-fail verification gate (Step 2) before advancing to GREEN
- Watch-it-pass + full-suite regression gate (Step 4) before advancing to REFACTOR
- Post-refactor green-suite gate (Step 6)
- Test-runner inference gate: ask the user if the runner cannot be determined from project config
- Missing-concrete-target gate: ask a clarifying question rather than assume a project/feature/behavior
- ywc-verify-done handoff gate at completion rather than self-certifying done
- Rationalization Defense table checked against any temptation to skip/reorder the cycle

## Full narrative

Before writing anything, I'd flag that the request as given describes *when* this discipline applies rather than *what* to build — it doesn't name a specific feature, bug, or behavior change, nor which project in this multi-project workspace (genbatime, homepage, our-assets-lp, beacon, develop-with-llm, propela, shell-utils) it belongs to. The ritual's Step 1 requires "one minimal test that captures one behavior the production code is required to exhibit," and that behavior has to come from somewhere concrete. So my first actual move would be to ask:

1. Which project is this for?
2. What is the specific feature, bug, or behavior change (ideally with acceptance criteria, or a pointer to an existing spec/task file under that project's `tasks/` or `docs/specification/` if one exists)?
3. Is there a preferred test file location / existing test suite convention to follow?

I would not guess a project or invent a feature to fill the gap, since a fabricated target produces a fabricated (and useless) test.

Once that's answered, here is exactly what I would do, concretely, under the ritual:

**Announce.** Post the required line verbatim: "I'm using the ywc-tdd-ritual skill to enforce RED → GREEN → REFACTOR with a watch-it-fail gate before any production code."

**Resolve the test runner (Step 2 prerequisite).** I would Read the target project's `package.json` (genbatime, homepage, our-assets-lp), `pyproject.toml`/`pytest.ini`, or `go.mod`, to find the configured test command. Per the root CLAUDE.md, genbatime, homepage, and our-assets-lp all run inside Docker, so any test/lint command I run would be prefixed accordingly, e.g. `docker exec genba-time-app pnpm test -- <path>` for genbatime (Vitest), or `docker exec our-assets-lp-app pnpm test -- <path>` if a test script exists there — and if I can't find a `test` script in a given project's `package.json`, I would ask rather than guess, exactly as Step 2 instructs.

**RED.** I'd Write or Edit exactly one new test (in the project's existing test directory/convention, discovered via Grep/Glob for sibling `*.test.ts`/`*.spec.ts`/`test_*.py` files first) that asserts one behavior with a clear, intention-revealing name (e.g. `rejects offset > total with 400`, not `pagination test 3`). No production code would be touched yet; if the test references a not-yet-existing function, that's expected and acceptable.

**Verify RED.** Run only that new test via Bash, e.g. `docker exec genba-time-app pnpm test -- src/foo/foo.test.ts`. I'd read the output for three things: the test actually ran (not skipped, not erroring before assertions), the failure reason matches the intended behavior gap, and no other test broke. If it passes on the first run, I would not advance — I'd treat that as a broken test and fix it first.

**GREEN.** I'd Edit the minimal production file(s) needed to satisfy just that one test — no extra parameters, no speculative abstractions, no incidental cleanup of adjacent code even if it's tempting.

**Verify GREEN.** Run the new test again plus the full suite for that project via Bash (e.g. `docker exec genba-time-app pnpm test`), confirming a clean pass with no new failures and no stray warnings/deprecation output.

**REFACTOR.** Only now would I clean up: remove duplication, tighten names, extract a helper if the same logic shows up 2+ times — re-running the test suite after each individual edit to make sure nothing regresses. No new behavior sneaks in here.

**Verify after REFACTOR.** One more full-suite run via Bash to confirm everything is still green.

**Commit shape.** Per behavior, up to three commits: `test: <behavior>` at the RED point (with the failing-test evidence in the message/PR description), `feat: <behavior>` or `fix: <bug>` at GREEN (with the passing-test + full-suite evidence), and `refactor: <what was tightened>` if cleanup happened (with the still-green evidence) — skipping the refactor commit if there was nothing to clean up. I would use `git add <specific files>` (never `git add -A`) and `git commit -m "..."` per the git-workflow rules already in scope, each preceded by a command → exit code → claim verification block matching `ywc-verify-done`'s format.

**Loop or hand off.** If more behaviors remain for the requested feature/fix, I'd return to RED for the next one. Once all behaviors are implemented, I would explicitly hand off to `ywc-verify-done` for the completion claim (build + lint + full test suite + per-claim evidence) rather than declaring the work done myself inside this cycle.

**What I would refuse to do**, regardless of pushback: write any production code before observing a test fail in this session for the expected reason; keep any pre-written/"reference" implementation code once TDD starts (delete and rewrite fresh from the test); bundle a "while I'm here" fix into a GREEN commit; skip the watch-it-fail or watch-it-pass verification steps even for something that looks trivially simple; or treat a compile/import error as if it were a real assertion failure. If the user pushed back with any of the excuses in the skill's Rationalization Defense table (e.g. "I already manually tested it," "too simple to need a test," "I'll write the test right after"), I would decline and cite the corresponding reality column rather than comply.
