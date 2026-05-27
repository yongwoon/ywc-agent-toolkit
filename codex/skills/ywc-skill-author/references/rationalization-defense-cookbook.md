# Rationalization Defense Cookbook

The Rationalization Defense table is the single most effective rule-bypass blocker in a ywc-* skill. This guide explains how to write tables that actually work, using patterns proven across production ywc-* skills.

## What Makes a Rationalization Defense Table Effective

An effective table:

1. **Captures the agent's actual self-talk verbatim**, in first-person quotation marks.
2. **Counters with a concrete reality**, not a slogan. The reality should reference a specific rule, threshold, or downstream consequence.
3. **Targets the rule most likely to be bypassed under pressure**, not the rules that are easy to follow.
4. **Lists 5–8 rows**. Fewer than 5 = under-defended. More than 8 = noise.

A table that lists generic "be careful" advice will be skipped by the agent. A table that names the exact shortcut the agent is about to take stops the bypass.

## Anatomy of a Strong Row

```markdown
| "<verbatim agent self-talk in first person>" | <concrete reality + rule reference + consequence> |
```

### Examples (good)

| Excuse | Reality |
|---|---|
| "These extra files probably belong here" | If you cannot point to a moment in this session when they were touched, they are OUT. Ask. |
| "Phase 1 had no findings, the spec is satisfied" | Absence of findings ≠ proof of conformance. State what was checked, not what was missing. |
| "Token budget is tight, truncating mid-function is OK" | Stop at a clean function boundary and write `[PAUSED — N of M files complete]`. Never mid-function. |

### Examples (weak — do not write tables like these)

| Excuse | Reality |
|---|---|
| "Be careful with edge cases" | Handle edge cases properly. |
| "Don't skip steps" | Follow all steps in order. |
| "Test the code" | Make sure tests pass. |

These rows are useless. They restate the rule instead of countering a specific bypass attempt.

## How to Discover the Real Excuses (RED Step)

Before writing the table, run a baseline scenario without the skill (or with the current version) and observe:

1. What did the agent say in plan-mode reasoning? Capture verbatim quotes.
2. What rules did it bend? Which rationalization phrases preceded each bend?
3. Which excuse repeats across multiple scenarios? That is a high-priority row.

If you write the table from imagination instead of observation, you will miss the real excuses. The agent will then find loopholes that match its actual reasoning patterns.

## Domain-Specific Patterns

Different skill domains have characteristic rationalizations. Use these as starting points but always adapt to the specific skill.

### Git / Commit / PR Skills

Common bypasses:
- "git add . is faster" / "stage everything to be safe"
- "Force push will resolve the rejection faster"
- "User said push, so amend + force push is implied"
- "This is just main, one direct commit is OK"
- "--no-verify just this once"

### Review Skills (impl, security, spec, product, ui-ux)

Common bypasses:
- "No findings means the spec is satisfied" (absence of evidence trap)
- "Severity feels High, mark it Critical to be safe" (severity inflation)
- "User wrote the spec, do not push back too hard" (sycophancy)
- "Skip dimension X, it does not apply here" (incomplete coverage)
- "Agent agreement = correctness" (groupthink)

### Code Generation Skills

Common bypasses:
- "// TODO: implement and let user fill in" (stub trap)
- "Token budget is tight, truncate mid-function" (clean-boundary violation)
- "Phase 1 looks fine, skip Phase 2 advisor" (false confidence)
- "Generate on main, branch is overhead" (branch-discipline bypass)
- "Test describe blocks count as test coverage" (empty-test trap)

### Executor Skills (sequential, parallel)

Common bypasses:
- "Tasks look independent, run all in parallel" (Ownership/Shared Surface ignorance)
- "Wave 1 partial failure, start Wave 2 anyway" (wave-gate bypass)
- "Skip CI wait, next task can start" (regression hiding)
- "Worktree cleanup is manual hassle" (stale state)

### Spec / Planning Skills

Common bypasses:
- "Spec is mostly clear, skip Feasibility check" (incomplete review)
- "Phase boundary is fuzzy, SEQUENCE expresses order" (hard-gate erosion)
- "Bundle DB migration with API task" (Safety Invariant violation)
- "20+ tasks is fine if they are small" (review-load denial)

### Documentation Skills

Common bypasses:
- "Existing docs use different naming, follow my own pattern" (drift)
- "Translate technical terms into Hangul/Katakana" (language-policy bypass)
- "Generic doc is fine when target type unclear" (under-specification)

## Writing the Closing Line

After the table, every Rationalization Defense section must end with:

```markdown
**Violating the letter of these rules is violating the spirit.** <one-sentence reminder of why honesty over shortcut matters in this domain>
```

The closing line cuts off "I'm following the spirit, not the letter" rationalizations. Examples:

- (commit) "If you find yourself rephrasing a rule to make an exception, stop and ask the user."
- (review) "Review without honest severity is theater."
- (code-gen) "A stub committed today is a runtime crash tomorrow."
- (parallel-execution) "Parallel execution is faster only when wave isolation is honored."
- (testsheet) "A testsheet that mixes audiences is sign-off theater."

Avoid generic closes like "Follow the rules" — they add no force.

## Sizing the Table

| Skill type | Recommended row count |
|---|---|
| Single-purpose utility (commit, release-pr-list) | 5–6 |
| Multi-step process (impl-review, code-gen) | 6–8 |
| Decision-heavy (task-generator, sequential-executor) | 7–8 |

If you find yourself writing more than 8 rows, the skill probably has multiple distinct concerns — consider splitting it or moving some excuses to a `## Common Mistakes` section.

## Iterating the Table

After deploying the skill, watch for new rationalizations:

1. The agent invents a new shortcut not covered by the table.
2. The agent rephrases an existing excuse to skirt the literal wording.

Both are signals to add a row. The table is a living artifact — expect to expand it 2–3 times in the first month after deployment.

## Anti-patterns (Never Do These)

- **Generic restatement of rules** — "Don't skip steps" → useless. Replace with a verbatim shortcut quote.
- **Sermon entries** — "Code review is important because..." → useless. Replace with a one-line counter.
- **Imaginary excuses** — excuses you think the agent might use, without observing it. Run the RED step first.
- **Single-row tables** — under-defended. Minimum 5 rows.
- **Copying tables verbatim across skills** — each table must be domain-specific.
