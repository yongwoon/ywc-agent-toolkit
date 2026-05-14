# Expert Profiles

Optional Council voice profiles. When `--focus <area>` is specified and Council
Escalation triggers, replace the 4 generic voices (Architect/Skeptic/Pragmatist/
Critic) with 3–4 profiles from the matching focus area below.

The profiles inherit the **Anti-anchoring rule** from SKILL.md's Council
Escalation section: each profile receives only the trade-off excerpt, never
the other profiles' verdicts. Synthesize after all profiles have responded
independently.

## Why named profiles

Generic Council voices apply general role-based skepticism. Named profiles bring
**discipline-specific heuristics** — Wiegers's testability filter is sharper for
requirements than a generic Skeptic; Fowler's interface-design instincts catch
architectural smells a generic Architect might miss. Use generic Council when
the trade-off is cross-cutting; use a focus profile when the trade-off lives
clearly inside one discipline.

## Focus → Profile Mapping

| `--focus` | Profiles to use (in order) |
|---|---|
| `requirements` | Requirements Quality + Specification by Example + Use Case Modeling |
| `architecture` | Interface Design + Service Boundaries + Integration Patterns + Production Resilience |
| `testing` | Risk-Based Testing + Three Amigos + Quality Attribute |
| `compliance` | Production Resilience + Cloud-Native Operations + Audit Trail |

If `--focus` is omitted, use the generic 4-voice Council from SKILL.md.

## Requirements Focus

### Profile R1 — Requirements Quality

Heuristic source: Karl Wiegers's requirement engineering frameworks.

- **Check for**: SMART criteria adherence, testability, measurable acceptance
  criteria, stakeholder traceability.
- **Default question**: "How would the validation team verify this requirement
  in production? What measurement makes the requirement true?"
- **Anti-bias**: Vague verbs (handle, support, gracefully) are critical until
  replaced with measurable behavior. Do not soften this for politeness.

### Profile R2 — Specification by Example

Heuristic source: Gojko Adzic's behavior-driven specification.

- **Check for**: Concrete Given/When/Then scenarios, executable examples,
  living-documentation viability.
- **Default question**: "Show one concrete real-world scenario where this
  requirement applies, and one where it explicitly does not."
- **Anti-bias**: Abstract-only requirements without examples are critical even
  when prose is clear — readers cannot validate intent without examples.

### Profile R3 — Use Case Modeling

Heuristic source: Alistair Cockburn's goal-oriented use case analysis.

- **Check for**: Identified primary actor, named business goal, complete
  scenario chain (trigger → main flow → exception flow).
- **Default question**: "Who is the primary actor, and what is the business
  goal that motivates them to invoke this? What stops them halfway?"
- **Anti-bias**: Feature-first phrasing ("system shall …") without an actor
  perspective is a completeness gap, not a stylistic choice.

## Architecture Focus

### Profile A1 — Interface Design

Heuristic source: Martin Fowler's design pattern catalog.

- **Check for**: Single responsibility at interface boundary, bounded context
  cohesion, evolution-friendly contract shape.
- **Default question**: "Does this interface have a single reason to change?
  Which two responsibilities does it currently couple?"
- **Anti-bias**: Convenience-driven coupling (one fat endpoint, mixed concerns)
  is critical even when current usage is small — interfaces survive longer than
  their first caller.

### Profile A2 — Service Boundaries

Heuristic source: Sam Newman's microservices decomposition.

- **Check for**: Service ownership, contract versioning strategy, backward
  compatibility plan, data ownership.
- **Default question**: "When this service changes its contract in 6 months,
  which downstream consumers break, and how do you stage the rollout?"
- **Anti-bias**: A spec that omits versioning is critical when the service is
  external-facing or cross-team; internal-only services may downgrade to
  warning.

### Profile A3 — Integration Patterns

Heuristic source: Gregor Hohpe's enterprise integration patterns.

- **Check for**: Message exchange pattern (request/reply, pub/sub, event-driven),
  delivery guarantees (at-most-once, at-least-once, exactly-once), ordering.
- **Default question**: "What is the exchange pattern, and what are the delivery
  and ordering guarantees? What happens on duplicate delivery?"
- **Anti-bias**: Silence on delivery guarantees is critical for any async
  boundary. Synchronous boundaries get a pass.

### Profile A4 — Production Resilience

Heuristic source: Michael Nygard's failure mode analysis.

- **Check for**: Named failure modes, circuit breaker / retry policy,
  observability (metrics, traces, logs), recovery mechanism.
- **Default question**: "List three failure modes for this component. For each,
  what alerts fire and what does the on-call engineer do?"
- **Anti-bias**: A spec without explicit failure mode coverage is critical for
  any production-facing component, regardless of complexity.

## Testing Focus

### Profile T1 — Risk-Based Testing

Heuristic source: Lisa Crispin's quality engineering.

- **Check for**: Risk-tier classification of requirements, test type assignment
  (unit/integration/E2E), edge case enumeration, failure scenario coverage.
- **Default question**: "Which requirement, if broken, has the largest blast
  radius? Where is its test, and is the test type appropriate to the risk?"
- **Anti-bias**: Uniform "all features get unit tests" is critical — high-risk
  paths need integration or E2E coverage that unit tests cannot provide.

### Profile T2 — Three Amigos

Heuristic source: Janet Gregory's collaborative testing.

- **Check for**: Acceptance criteria written collaboratively, definition of
  done, test cases derived from examples, whole-team quality conversation.
- **Default question**: "If a developer, a tester, and a product owner each
  read this requirement separately, would they each implement the same test?
  Where do they diverge?"
- **Anti-bias**: Acceptance criteria authored by one role only is a critical
  collaboration gap, not just a process preference.

### Profile T3 — Quality Attribute

Heuristic source: ISO 25010 quality attributes via Adzic-style examples.

- **Check for**: Non-functional requirements expressed measurably (latency,
  throughput, availability), test method specified.
- **Default question**: "For each non-functional requirement, what is the
  measurement method and the pass threshold? What instrument records it?"
- **Anti-bias**: NFRs expressed without thresholds (fast, reliable, scalable)
  are critical — they cannot be tested.

## Compliance Focus

### Profile C1 — Production Resilience

Same heuristic as Profile A4 (Nygard). Reuse the Architecture A4 profile
content above when assembling a Compliance focus Council.

### Profile C2 — Cloud-Native Operations

Heuristic source: Kelsey Hightower's cloud-native principles.

- **Check for**: Deployment topology spec, configuration externalization,
  observability (the three pillars), infrastructure-as-code coverage.
- **Default question**: "How is this deployed across environments? Which
  configuration values are environment-specific, and where do they live?"
- **Anti-bias**: A spec with hard-coded configuration assumptions is critical
  for any multi-environment system.

### Profile C3 — Audit Trail

Heuristic source: Wiegers's compliance requirement engineering.

- **Check for**: Regulatory mapping (which clause maps to which requirement),
  audit log content, retention period, immutability guarantee.
- **Default question**: "Which specific regulatory clause does this requirement
  satisfy? What evidence does an auditor see, and how long does it persist?"
- **Anti-bias**: Compliance requirements without explicit regulatory anchor
  are critical — implicit compliance breaks at audit time.

## Output Form

The Council output format in SKILL.md applies unchanged, except the voice
labels are replaced with profile names:

```text
[COUNCIL] {trade-off description}
- Requirements Quality: {verdict, ≤2 sentences}
- Specification by Example: {verdict, ≤2 sentences}
- Use Case Modeling: {verdict, ≤2 sentences}
Consensus: {agreed recommendation, or "No consensus — strongest dissent: <profile>: <reason>"}
```

The 2-advisor budget rule applies whether generic Council voices or focus
profiles are used. Do not exceed the budget by mixing the two modes within a
single invocation.

## When to fall back to generic Council

Use the generic 4-voice Council (Architect/Skeptic/Pragmatist/Critic) instead
of focus profiles when:

- The trade-off spans two or more focus areas (e.g., an API design decision
  that has both architecture and testing implications).
- The user explicitly requests a generic review.
- The spec under review covers multiple domains and no single focus dominates.

Mixing modes within a single Council session breaks the anti-anchoring rule —
pick one or the other.
