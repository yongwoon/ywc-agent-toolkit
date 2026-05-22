---
name: ywc-verify-done
description: >-
  (ywc) Use when about to claim that work is complete, tests pass, the build
  succeeds, a bug is fixed, requirements are met, or a delegated subagent has
  finished — and before any commit, PR creation, executor handoff, or task
  transition. Triggers: "완료", "다 됐어", "끝났어", "끝났습니다", "verify
  done", "검증해줘", "done", "completed", "finished", "ready to merge",
  "完了", "終わった", "終わりました", "確認お願いします", "ywc-verify-done".
  Do not use for ongoing implementation drafting (use ywc-code-gen), root-cause
  debugging (use ywc-debug-rootcause), pre-implementation confidence assessment
  (use ywc-confidence-gate), or codebase exploration before planning (use
  ywc-plan).
category: discipline
phase: pre-handoff
requires: []
---

# ywc-verify-done

**Announce at start:** "I'm using the ywc-verify-done skill to gate the completion claim with fresh verification evidence."

This skill is the single canonical gate between "I did the work" and "I am telling someone the work is done." It exists because every downstream skill (`ywc-commit`, `ywc-create-pr`, `ywc-finish-branch`, `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-impl-review`) assumes the upstream caller verified its own claims. When that assumption breaks, the failure surfaces as a CI red, a reviewer rejection, or a production incident — costs that are 10–100× higher than running the verification command once. Adapted from `superpowers:verification-before-completion`.

## The Iron Law

```text
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE IN THIS MESSAGE
```

If the verification command has not been executed in the current message and its output read, the claim cannot be made. Cached confidence ("I ran it five turns ago") does not count — code may have changed since.

## The Gate Function

For every completion claim, execute these five steps in order. Skipping any step turns the claim into an unverified assertion.

| # | Step | Action |
|---|---|---|
| 1 | IDENTIFY | Name the exact shell command (or commands) whose output proves the claim. If you cannot name one, the claim is not yet verifiable — refine the claim. |
| 2 | RUN | Execute the command fresh in this message. No partial runs, no resumed background processes. |
| 3 | READ | Read the full output. Note exit code, failure count, warning count. |
| 4 | VERIFY | Map the output back to the claim. Does the evidence support the exact wording you are about to use? |
| 5 | CLAIM | Only after steps 1–4 pass, surface the claim — and surface it **with** the evidence (command + exit code + key line) so the reader can audit. |

## Forbidden Vocabulary

These phrases signal an unverified assertion and must be replaced with evidence or removed:

| Forbidden | Replace with |
|---|---|
| "should pass" / "should work" | Command output: `... 0 failed` (exit 0) |
| "probably done" / "probably fixed" | Test name + observed result |
| "seems to work" / "appears to" | Reproduction steps + observed behavior |
| "I think it's ready" | Verification block (command, exit code, output excerpt) |
| "Great!" / "Perfect!" / "Done!" before the verification block | Move the celebration to **after** the block |

When the verification block is present and the evidence supports the claim, positive language is fine. The rule is sequence, not tone.

## Rationalization Defense

When tempted to bypass the gate, check this table first:

| Excuse | Reality |
|---|---|
| "I just ran this command 30 seconds ago, re-running is wasteful" | A 30-second re-run is cheaper than one CI failure or one reviewer round-trip. Code state can change between turns (edits, branch switches, dependency installs). Fresh = in this message. |
| "The subagent's return payload says success, that's enough" | Subagent self-reports are the **second-most** common false-positive after "I think it works". Always check the VCS diff or run the verification yourself per `references/subagent-status-actions.md`. The §3.5 contract sends only paths — the work itself is on disk and must be verified. |
| "Lint passed, build will pass too" | Lint is not the compiler. Build is not the type-checker. Type-check is not the test suite. Each layer catches different defects; only the layer matching the claim counts as evidence. |
| "Tests passed in the last CI run on this branch" | Last CI ran against the previous commit. If you have made any edit since, the previous CI result is not evidence for the current state. Either push and let CI re-run, or run locally before claiming. |
| "The change is one line, verification is overkill" | The smaller the change, the easier the verification. There is no size threshold below which the gate stops applying. Skipping for "trivial" changes is the most common origin of broken-main incidents. |
| "I'll claim done now and run the verification in the next message" | The reader makes irreversible decisions (merge, deploy, hand off to the next skill) on the strength of the claim. Verification AFTER the claim is not verification. |
| "Test passes locally, that's good enough" | Local pass on a dirty working tree, with cached state, or with `.env` overrides is not equivalent to clean-environment CI. State the environment in the verification block so the reader can judge. |

**Violating the letter of these rules is violating the spirit.** The cost of the gate is seconds per claim; the cost of skipping it is rework measured in hours per incident.

## Claim Classification

Map every completion claim to one of these classes and use the matching verification.

| Claim class | Sufficient evidence | Insufficient evidence |
|---|---|---|
| Tests pass | Test command output showing 0 failures, exit 0 | "Should pass" / linter green / partial subset |
| Build succeeds | Build command exit 0 + no compilation errors in output | Lint passing / type-check passing |
| Type-check clean | Type-check command exit 0 + 0 errors reported | Lint passing / runtime succeeded once |
| Lint clean | Lint command exit 0 + 0 errors | "Looks clean" / partial files only |
| Bug fixed | Failing reproduction test now passes **and** rolls back to FAIL when the fix is reverted (red-green-red cycle) | Test passes once / "I changed the code" |
| Regression test exists | Red-green-red cycle observed in the current message | Test file committed without proof it ever failed |
| Requirements met | Line-by-line checklist against the spec / plan, each line marked with the evidence command | "All tasks done" / "Tests pass, so requirements pass" |
| Subagent finished | VCS diff (`git status`, `git diff --stat`) confirms expected files changed + structured return payload (§3.5) read | Agent's `Status: DONE` line alone |
| CI green | Remote CI status reported by `gh pr checks <pr>` showing all required checks passing | Local CI passing / "CI ran yesterday" |
| PR ready to merge | CI green **and** bot-review polling window closed with `BOT_COUNT == 0` (per `references/pr-bot-polling.md`) | "I created the PR" |

When the claim does not match any row, ask: "What command would I run to prove this?" and add the missing row to the local plan before claiming.

## Output Format

Every completion claim surfaces as a **verification block** in this shape:

````markdown
**Verification:**
```bash
$ <command exactly as run>
<key output lines, including failure/error counts>
$ echo "exit=$?"
exit=<code>
```

**Claim:** <one-line claim that the evidence supports>
````

For multi-command claims (e.g., build + test + lint), include one fenced block per command in order, then a single Claim line at the end. The reader must be able to reproduce the verification by copy-pasting the commands.

When verification fails, surface the failure with the same block shape and **no** completion claim. State the actual state, then route per Common Mistakes below.

## Workflow

### Step 1: Identify the claim and its proof

Before opening any tool, list every claim you are about to make and the command that proves each. If a claim has no command, downgrade it ("partial: tests for module X pass; module Y untested") or drop it.

### Step 2: Run verifications fresh

Execute each command in the current message. For long-running commands (full test suite, full build), run with `run_in_background: true` and resume when the harness notifies. Do not move to Step 3 until each command has terminated and the exit code is known.

### Step 3: Read the full output

Read the entire output, not just the last line. Some failures are reported mid-stream while the final line reads "Tests completed". Search for `FAIL`, `error`, `Error`, `✗`, non-zero exit, warning counts that exceeded baseline.

### Step 4: Map output to claim

For each claim, point to the specific line in the output that proves it. If the output is ambiguous (e.g., "passed" without a count), run a narrower command that yields an unambiguous result.

### Step 5: Surface the verification block, then the claim

Print the verification block first, then the claim. Do not invert the order — readers stop at the first "Done!" they see and may miss the block below.

### Step 6: On failure, classify and route

If verification fails, do not claim done and do not silently retry. Classify the failure and route:

| Failure shape | Route to |
|---|---|
| Single isolated test or compilation error | Fix in this session, then re-verify |
| Repeated failure after 2 fix attempts | `ywc-debug-rootcause` (root-cause investigation) |
| Subagent delivered wrong artifact | Re-dispatch with corrected prompt; do not patch the artifact in the orchestrator |
| Environment / infra issue (DB down, network out) | State the blocker, surface to user with proposed action — never claim done with "ignored env issue" |

## Integration

- **Upstream callers (must invoke before their own completion / handoff step):** `ywc-code-gen` (Step 7 verification gate), `ywc-impl-review` (Phase 1 / Phase 2 boundary), `ywc-sequential-executor` (per-task completion), `ywc-parallel-executor` (per-wave completion), `ywc-commit` (pre-commit), `ywc-create-pr` (pre-PR), `ywc-finish-branch` (pre-merge), `ywc-task-generator` (per-task validation block).
- **Pairs with:** `ywc-debug-rootcause` (when verification fails ≥2 times), `ywc-impl-review` (when downstream review needs the verification evidence as input).
- **Downstream effects:** None. This skill never modifies code or executes the next skill — it only gates the claim.

## Validation Checklist

Before stating that any work is "done", verify:

- [ ] Every claim in the upcoming message has a paired command identified
- [ ] Every command was executed in **this** message (no cached "from earlier")
- [ ] Every command's exit code was read and recorded
- [ ] The output excerpt in the verification block contains the line proving the claim (not just a generic "passed")
- [ ] No Forbidden Vocabulary appears in the claim sentence
- [ ] The verification block appears **before** the claim line, not after
- [ ] Subagent claims, if any, are backed by an independent VCS diff or re-run check — not by the subagent's own success report
- [ ] When verification failed, no "done" claim is surfaced; the failure is classified and routed instead

## Common Mistakes

(Procedural failure modes specific to this skill. Behavioral rationalizations are in the table above — do not duplicate here.)

- **Surfacing the claim above the verification block.** Readers parse top-down. "Done! Here's the evidence below." defeats the gate because the decision is already made by the time the block is read. Always: block first, claim second.
- **Verifying a different claim than the one stated.** "Tests pass" is verified by running tests, not by running the build. Map the command to the exact wording.
- **Treating a single red-green cycle as a regression test.** A regression test must also fail when the fix is reverted (red-green-red). Without the red-green-red cycle, the test may be passing for unrelated reasons.
- **Skipping the gate for "trivial" changes.** There is no size threshold. The smaller the change, the cheaper the verification — there is no reason to skip.
- **Inferring `--skip-post-ci-check` skipped verification entirely.** The flag suppresses the **caller's** repeated CI poll, not the gate itself. `ywc-verify-done` still applies; the verification is just performed once by the upstream caller (e.g., `ywc-finish-branch` Step 4) instead of twice.

## References

| Reference | Use when |
|---|---|
| [references/forbidden-vocabulary.md](references/forbidden-vocabulary.md) | Auditing a draft message for unverified-assertion language |
| [references/verification-block-examples.md](references/verification-block-examples.md) | Picking the right block shape for a multi-command claim |
| [../references/subagent-status-actions.md](../references/subagent-status-actions.md) | Verifying subagent return payloads (§3.5) and routing BLOCKED status |
| [../references/pr-bot-polling.md](../references/pr-bot-polling.md) | PR-ready claims that depend on bot-review polling outcomes |
