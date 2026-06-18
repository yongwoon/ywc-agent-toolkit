# Codex Agent Behavioral Evidence Strategy

Codex custom agents are read-only reviewer and advisor roles under
`codex/agents/*.toml`. A8 reaches reference quality only when behavior is backed
by smoke fixtures or eval evidence that passes. Until an executable harness
exists for custom agents, this document defines the fixture contract and the
limits of what can be claimed.

## Scope

This strategy covers the current Codex agents:

- `ywc-architect`
- `ywc-security-engineer`
- `ywc-root-cause-analyst`
- `ywc-performance-engineer`
- `ywc-typescript-reviewer`
- `ywc-python-reviewer`
- `ywc-go-reviewer`

All fixtures must be read-only. They must not require write access, app
execution, tests, profilers, network access, external services, or repository
state beyond the bounded evidence packet supplied in the fixture.

## Fixture Shape

Each smoke fixture should be a single bounded packet with these fields:

| Field | Required content |
|---|---|
| `agent` | One Codex agent name from `codex/agents/*.toml`. |
| `intent` | The caller's review or advisory question in one sentence. |
| `evidence_packet` | Minimal excerpts, paths, diffs, metrics, or logs needed for the role. |
| `expected_status` | One of `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT`. |
| `expected_signals` | Observable phrases, categories, routing decisions, or refusal behavior. |
| `forbidden_signals` | Behaviors that would violate the agent boundary. |

The fixture should verify behavior, not prose style. Good expected signals name
observable routing, severity, category, missing-context, or boundary handling.
Weak expected signals merely restate the prompt.

## Required Cases

An A8 fixture set should include at least these cases:

1. Happy path: the agent returns the expected status and scoped findings for a
   bounded packet in its domain.
2. Boundary routing: the agent redirects an adjacent concern to the correct
   sibling agent instead of answering out of scope.
3. Missing evidence: the agent returns `NEEDS_CONTEXT` with the exact missing
   signal when correctness depends on absent input.
4. Read-only discipline: the agent does not ask to edit files, run commands, run
   the app, call external services, or create artifacts.

## Agent Families

Architecture:

- Happy path should exercise module boundary, dependency direction, API
  contract, or irreversible design trade-off reasoning.
- Boundary case should route security, performance, root-cause, or
  language-idiom questions to the matching agent.

Security:

- Happy path should cite a concrete static trust-boundary finding with
  severity and narrow remediation.
- Boundary case should avoid non-security architecture, performance, or
  language-style review.
- Forbidden signals include echoing secrets, raw PII, or speculative findings
  without a scoped entry point.

Root cause:

- Happy path should rank hypotheses with evidence for and against each one.
- Missing-evidence case should request the single highest-information probe.
- Boundary case should route final architecture or security verdicts away.

Performance:

- Happy path should classify the issue using a performance category and cite a
  metric, budget, profiler clue, or bounded code path.
- Missing-evidence case should request profiler, budget, or Web Vitals context
  when severity cannot be decided.

Language reviewers:

- TypeScript, Python, and Go fixtures should each use language-specific
  categories from the agent output contract.
- Boundary cases should route architecture, security, performance, or another
  language to the matching agent.
- Forbidden signals include running compiler, linter, test, build, or formatter
  commands.

## Current Limitation

The current evaluator has mechanical TOML gates and manual A8 judgment, but no
agent smoke harness consumes these fixtures yet. Therefore:

- A8 can document this strategy and remain at 3.
- A8 should move to 4 only after fixture files exist, an agent smoke harness
  executes them, and the passing output is cited in the sweep report or
  scoreboard.
- Harness implementation is a separate evaluator task, not part of the current
  quality-improvement cycle.
