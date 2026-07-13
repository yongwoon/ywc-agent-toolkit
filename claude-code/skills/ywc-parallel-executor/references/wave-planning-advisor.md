# Wave Planning Advisor (Pattern C) — ywc-parallel-executor

> Tier-3 reference extracted from `SKILL.md` (ywc-skill-author A8/A14). The executor links this file from its `#### Planning Advisor (optional, Pattern C)` pointer in Step 2. The invoke-trigger conditions stay inline in `SKILL.md` — this file holds the payload, questions, budget, and output format only, to avoid the same condition list living (and drifting) in two places.

Full invocation procedure for the optional upfront Opus advisor pass in Step 2
(Plan Waves). This is Pattern C from
[advisor-pattern.md](../../references/advisor-pattern.md): a **single**
upfront advisor call before worktree creation begins, because a wrong wave
boundary cascades into unnecessary serialization (waste) or unsafe
parallelism (merge conflicts and broken dependencies) across every
subsequent wave — damage that is expensive to undo once worktrees and
feature branches exist.

## How to Invoke

Use the Task tool with `model: opus`. Payload (≤200 lines total):

- Dependency graph excerpt — tasks + `Depends On` + `Conflicts With` +
  `Shared Surfaces` only; do not forward full task READMEs.
- First-pass wave assignment from your topological sort.
- Category distribution per wave (Backend N / Frontend M / QA K / etc).

Ask the advisor for three things:

1. **Wave boundary confirmation** — does the first-pass assignment group
   tasks safely, or should any task move to a different wave?
2. **Agent assignment risk** — any task whose Category-based agent
   assignment is a poor fit (for example, a `refactor` task that is
   actually a domain logic rewrite in disguise)?
3. **Conflict detection** — any Shared Surfaces the topological sort missed
   that would cause merge conflicts during Wave Merge (Step 4e)?

## Budget

Exactly **1** Opus call per invocation. Mid-wave escalation is explicitly
disallowed — per-wave task agents run in isolated worktrees and handle their
own decisions. If the initial wave plan proves wrong during Step 4, stop
execution, report to the user, and re-run the skill with refined input
rather than calling Opus mid-flight.

## Advisor Output Format (≤300 words)

- Wave boundary verdict (confirm, or specific relocations)
- Agent assignment verdict (confirm, or specific reassignments)
- Conflict warnings (if any, with the affected Shared Surface named)
- Single "proceed" or "reconsider with refinements" verdict

After the verdict, either continue to Step 3 with the adjusted wave plan, or
surface the "reconsider" verdict to the user for plan refinement before
proceeding.
