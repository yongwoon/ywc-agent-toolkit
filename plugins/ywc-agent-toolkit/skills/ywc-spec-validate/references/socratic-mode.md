# Socratic Mode

Output learning questions in place of a finding report. Use when the user is
learning to write specs, training a junior teammate, or preparing for a spec
workshop — situations where the user grows more from discovering gaps than
from being handed a fix list.

The 4-Dimension analysis still runs internally — Socratic Mode reshapes the
**output**, not the analysis. Findings that would have been Critical become
Foundational/Assumption questions; Warnings become Stakeholder/Alternative
questions. Dimensions with no weakness produce no questions.

## Triggering

- `--mode socratic` on the SKILL invocation.
- Output a question list instead of the standard finding report.
- Confidence Gate scoring still runs and appears in the header for awareness,
  but the gate does not produce a DONE/BLOCKED status in this mode.

## Question Taxonomy

Each question category maps to dimensions the internal 4-Dimension review
found weak. The mapping below is the default — the executor may deviate when
a specific spec calls for emphasis.

| Category | Triggered by weak dimension | Purpose |
|---|---|---|
| Foundational | Completeness (Critical) | Force the author to restate the spec's reason for existing |
| Stakeholder | Completeness (Warning) | Surface unnamed actors and their goals |
| Assumption | Feasibility | Make implicit environment assumptions explicit |
| Alternative | Code Compatibility | Probe whether the spec or the existing code should move |
| Operational | Feasibility (production-facing) | Force the author to describe steady-state operation |
| Validation | Consistency | Surface how the author would verify the spec is satisfied |

## Question Heuristics

### Foundational Questions

Use when Completeness has Critical findings (missing scope, undefined goal,
no problem statement).

Templates:

- "If this spec did not exist, what observable user pain or business loss would persist?"
- "In one sentence, what problem are you solving, and for whom?"
- "What is *not* in scope for this spec, and why?"

### Stakeholder Questions

Use when actors, roles, or affected parties are absent or implicit.

Templates:

- "Name the 1st-, 2nd-, and 3rd-most affected stakeholder. What does each gain or lose?"
- "If a non-technical stakeholder reads this spec, what section would confuse them first?"
- "Whose decision is required to ship this? Have they seen this spec?"

### Assumption Questions

Use when Feasibility has Warning or Critical findings (implicit performance,
version, or environment assumptions).

Templates:

- "Which assumption about the runtime environment, if wrong, would make this unimplementable?"
- "What does this spec assume about traffic, data volume, or concurrency that is not written down?"
- "Which dependency version is this spec implicitly tied to? What breaks at the next major version?"

### Alternative Questions

Use when Code Compatibility has findings, or when a single design choice
dominates the spec.

Templates:

- "What is the simplest version of this spec that still solves the core problem?"
- "Name two alternative designs you considered and rejected. Why did you reject them?"
- "If you had 30% of the proposed effort, what would you cut first, and what user value remains?"

### Operational Questions

Use for production-facing features when failure modes or operational concerns
are absent.

Templates:

- "List three failure modes for this feature. For each, what alerts fire?"
- "How does the on-call engineer know this is working in production right now?"
- "What is the rollback plan, and how long does it take?"

### Validation Questions

Use when acceptance criteria are vague or untestable.

Templates:

- "Write the test name that proves this requirement is satisfied."
- "What is the measurable threshold that distinguishes 'done' from 'not done'?"
- "Six months from now, how would a new team member verify this spec is still being met?"

## Selection Rules

- Generate 5–10 questions total. More than 10 reads as a quiz; fewer than 5
  misses too many dimensions.
- Cover at least 3 categories — single-category outputs feel one-note.
- Order: Foundational → Stakeholder → Assumption → Alternative → Operational
  → Validation. Foundational must appear first; without it, downstream
  questions lack anchor.
- Never include the answer or the suggested fix. Socratic Mode's value
  collapses when the question hints at its answer.

## Output Format

```text
## Spec Socratic Review: {filename}

### Header
- Gate score: {NN}/100 ({band})
- Dimensions probed: {comma-separated list of weak dimensions}

### Foundational
1. {question}
2. {question}

### Stakeholder
3. {question}

### Assumption
4. {question}
5. {question}

### Alternative
6. {question}

### Validation
7. {question}

### Completion Status
SOCRATIC (this mode does not produce DONE/BLOCKED — the user owns the next step)
```

The Completion Status `SOCRATIC` signals to downstream skills (especially
`ywc-task-generator`) that this run was a teaching pass, not a gate decision.
**Do not hand off to `ywc-task-generator` from a Socratic run.**

## When Not to Use

- The user wants a quick yes/no on whether the spec is shippable — use
  `--mode standard`.
- The spec is already at gate PROCEED level — there is nothing left to teach.
- The user is under time pressure and explicitly asked for fixes — Socratic
  Mode is for learning, not for crisis response.

If the user invokes Socratic Mode but seems to want answers, surface the
mismatch and offer the switch:

> "Socratic mode returns questions, not fixes. If you need an actionable
> finding list, rerun with `--mode standard`."

## Pair with Other Skills

- After a Socratic run, the user typically edits the spec and reruns with
  `--mode standard` to validate the new state. The mode switch is the
  workflow.
- Pair with `ywc-ubiquitous-language` when Stakeholder questions surface
  naming inconsistencies — those are vocabulary gaps, not just teaching
  opportunities.
- For team workshops, run Socratic Mode once and use the question list as
  the agenda; reconvene with `--mode standard` after the workshop to validate
  the revised spec.
