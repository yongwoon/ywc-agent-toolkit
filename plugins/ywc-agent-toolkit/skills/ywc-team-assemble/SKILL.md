---
name: ywc-team-assemble
description: >-
  (ywc) Use when the user explicitly asks Codex to assemble a specialist team,
  delegate work to subagents, run a swarm, or split a complex task across
  parallel expert roles. Triggers: "assemble a team", "use agents", "delegate",
  "parallel agents", "swarm", "specialist team", "팀 구성", "전문가 팀",
  "エージェントチーム", "専門家チーム". Do not use for simple questions,
  single-file edits, strictly sequential work, or any task where the user has
  not explicitly authorized subagents/parallel/delegated execution.
---

# Team Assemble

**Announce at start:** "I'm using the ywc-team-assemble skill to split explicitly authorized work across specialist roles."

Use this skill to decompose complex work into specialist roles, run independent roles in parallel with Codex subagents, and synthesize the results into one coherent outcome.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "This is complex, so subagents are automatically allowed" | Complexity is not authorization. Use subagents only when the user explicitly asked for team, parallel, delegated, or agent work. |
| "The hardest task can go to a worker while I wait" | Keep the immediate critical-path blocker local. Delegate sidecar work that can run in parallel. |
| "Two workers can edit nearby files if they coordinate" | Assign disjoint write scopes. Shared ownership causes merge conflicts and lost work. |
| "A broad prompt gives specialists flexibility" | Broad prompts waste context and produce overlapping work. Give concrete scope, exclusions, ownership, and output format. |
| "Subagent results are accepted by default" | Review every returned output before integration. Subagents are contributors, not source of truth. |
| "One slow agent should be waited on repeatedly" | Wait only when its result blocks the next critical-path decision. Continue non-overlapping local work otherwise. |

**Violating the letter of these rules is violating the spirit.** Team execution is useful only when boundaries are explicit.

## Eligibility Gate

Proceed only when all conditions are true:

1. The user explicitly requests a team, swarm, parallel execution, delegated agents, or specialist roles.
2. The work has at least two independent or partially independent workstreams.
3. The subagent outputs can be integrated without shared write conflicts.

If the task is a generated task wave from `ywc-task-generator`, prefer `ywc-parallel-executor`. If the task is a normal implementation with one clear critical path, work locally or use `ywc-sequential-executor`.

## Workflow

1. Analyze the task and identify role boundaries.
2. Decide what must stay local on the critical path.
3. Assign only sidecar or independent workstreams to subagents.
4. Give each subagent a concrete scope, expected output, and write boundary.
5. Continue useful local work while subagents run.
6. Review returned outputs, integrate only relevant changes, and report the final result.

## Role Design

Use a small team. Two to four roles is usually enough.

| Role type | Use for | Typical mode |
|---|---|---|
| Researcher | external or repo-aware investigation that can run independently | read-only report |
| Explorer | bounded codebase questions with no file edits | read-only answer |
| Worker | implementation in a disjoint file or module scope | direct file edits |
| Reviewer | focused verification of a completed or near-completed change | findings report |

Keep role ownership explicit:

- Files or modules the role may edit
- Files or modules the role must not edit
- Commands the role should run, when known
- Output format expected from the role

## Subagent Rules

Use `spawn_agent` only for tasks that are independent enough to run in parallel with local work.

Do not delegate:

- The immediate blocker for the next local step
- Broad ownership of the whole repository
- Destructive git, deploy, database, or production operations
- Work that requires secrets or live credentials unless the user has explicitly approved that path

When delegating implementation, tell each worker:

- It is not alone in the codebase.
- It must not revert changes made by others.
- It must adapt to concurrent changes.
- It must list the files it changed in its final response.

## Prompt Template

Use `references/prompt-templates.md` when preparing prompts for multiple subagents or when the task has dependencies between roles.

Each subagent prompt should include:

1. Context
2. Goal
3. Scope and exclusions
4. Ownership boundary
5. Output format
6. Whether file edits are allowed

## Execution Pattern

Start independent subagents in the same turn when possible. After spawning, immediately continue local work that does not overlap with delegated scopes.

Wait for subagents only when their results are needed for the next critical-path decision. Review their outputs before treating them as accepted work.

For dependent roles, pass only the necessary prior result into the next subagent. Avoid forwarding full transcripts or unrelated context.

## Output Format

Return a concise synthesis:

- Team roles used
- Local work completed
- Subagent outputs accepted or rejected
- Files changed
- Verification run
- Remaining risks or follow-up decisions

```text
Status: <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>
Team: <roles used and why>
Accepted outputs: <subagent outputs accepted or rejected>
Local work: <what the main agent completed>
Verification: <commands or checks run>
Next action: <follow-up decision or "none">
```

## Validation

Before finalizing, verify that each subagent had a bounded prompt, ownership boundaries did not overlap unsafely, accepted outputs were reviewed before use, files changed are listed, and any verification gaps or rejected outputs are reported.
