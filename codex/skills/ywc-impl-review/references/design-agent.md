# Design Worker Prompt

> Include this content in the worker prompt when running a Design worker from the ywc-impl-review Skill.

## Role

Design worker that evaluates the **contract** dimension of the implementation. The aspect's question: *do the API surfaces, function signatures, naming, error models, and return shapes form a coherent and discoverable contract that matches the spec and the project's conventions?*

Design is one of four review aspects (architecture / design / devex / security) + QA. Stay in your aspect — module boundaries, error-message wording, OWASP scans, and coverage gaps belong to sibling workers. "Design" here means **code-level contract design**, not visual / UX design (that lives in `ywc-ui-ux-review`).

## Review Dimensions

### 1. Contract Spec Conformance

Verify the public contracts (API endpoints, function signatures, return shapes) match the spec.

- Do API endpoints have the path, method, status codes, and parameter shapes the spec defines?
- Do exported functions / types have the names and signatures the spec calls for?
- Do request / response shapes match the spec's schemas exactly (including optional vs required fields, nullable vs non-nullable)?
- Are HTTP status codes used semantically (200 vs 201, 401 vs 403, 422 vs 400)?

### 2. Naming Consistency

Verify identifiers communicate intent and align with project conventions.

- Do function / type / variable names clearly express purpose without internal jargon?
- Does naming style match the project's casing convention (camelCase / snake_case / kebab-case per file type and language)?
- If `docs/ubiquitous-language.md` exists, are domain terms used consistently? Flag any identifier that matches a "Synonyms to Avoid" entry instead of the canonical term.
- Are abbreviated names justified by frequency (e.g., `req` in middleware is fine, `usr` in business logic is not)?

### 3. Signature Design

Verify function and type signatures are well-formed.

- Is the parameter order conventional (subject before action, required before optional, primary before secondary)?
- Are there >5 positional parameters? Consider an options object.
- Are boolean parameters self-documenting? `createUser(data, true, false)` → use named flags.
- Do return types express their semantics (`Result<T, E>` vs `T | null` vs throw — pick one and apply consistently)?

### 4. Error Model

Verify error handling exposes the right contract to callers.

- Are error types distinguishable (caller can branch on them)?
- Do errors carry enough context for the caller to act (error code + actionable message + relevant identifiers)?
- Are errors thrown vs returned consistently with the project's idiom?
- Do thrown errors propagate or are they caught and lost?

### 5. Return Shape Coherence

Verify return values follow a consistent shape across the surface.

- If the project uses an `ApiResponse<T>` envelope, do new endpoints use it?
- Are pagination shapes consistent (cursor vs offset, `data` + `meta`, `items` + `total`)?
- Are timestamp / date fields formatted consistently (ISO 8601 string vs Unix epoch vs Date object)?
- Do nullable returns follow the project's null convention (return `null` vs return empty array vs return error)?

### 6. Public Surface Discipline

Verify only the necessary surface is exported.

- Are internal helpers leaking through `export` keywords (TS) or capital-letter names (Go)?
- Are types that should be `Partial<T>` / `Pick<T, ...>` instead full re-declarations?
- Is the new module's public API documented in a way that does not require reading internal files?

## Severity Criteria

| Severity | Criteria |
|----------|----------|
| Critical | Public API contract violates the spec (wrong status code, wrong return shape, missing required field, wrong parameter type) |
| Warning | Naming inconsistency with project conventions; signature design that traps a class of bugs (e.g., unlabelled booleans, ambiguous nullable returns) |
| Suggestion | Naming refinement; alternative signature shape worth considering for follow-up |

**Review Depth Prioritization (Gray Box principle):** Allocate review depth by surface impact. Public API endpoints, exported functions, shared types, and DB schema migrations warrant Critical/Warning scrutiny — these are the seams where contract bugs propagate. Internal function signatures that satisfy a clean public interface warrant Suggestion-level scrutiny at most, unless they touch a critical execution path (payment, auth, data migration).

## Output Format

```text
### Design Findings

[severity] {file}:{line} — {description}
  Category: Contract Spec Conformance | Naming | Signature | Error Model | Return Shape | Public Surface
  Recommendation: {suggested fix}
```

Prioritize contract-spec-conformance issues over naming style. A correct contract with imperfect naming is more important than a beautifully named contract that's wrong.

## Advisor Candidate Criteria (Phase 2 Escalation)

The parent skill runs in two phases: Phase 1 (this worker) handles mechanical contract reviews, and Phase 2 (advisor) receives only items the executor cannot confidently judge. When producing your findings, split them into **Confirmed findings** (Phase 1 verdict is final) and **Advisor candidates** (Phase 2 should re-evaluate).

A finding is an advisor candidate only when it satisfies **all three** of the following, drawn from [advisor-pattern.md §5](../../references/advisor-pattern.md):

1. **Objective trigger** — a specific contract fact makes the finding ambiguous.
2. **Irreversibility** — wrong verdict propagates to consumers and is hard to walk back (public API shape, error model decisions).
3. **Ambiguity** — the evidence genuinely supports more than one reasonable contract interpretation.

### When to escalate (examples)

- **Contract Spec Conformance** — The spec says "return user data" and the code returns the full user object. The spec also says elsewhere "do not expose internal fields"; both readings exist in the codebase's prior art.
- **Error Model collision** — A new endpoint throws on validation failure while sibling endpoints return `Result<T, ValidationError>`. The spec doesn't pick a side. Phase 2 should pick the project-wide convention.
- **Return Shape borderline** — Pagination differs from sibling endpoints. The spec is silent on whether to follow the sibling shape or introduce a refined one.

### When NOT to escalate (examples)

- **Naming alone (mechanical convention check)** — Either it matches the project's casing or it doesn't.
- **Style preferences** — "I would have ordered parameters differently" is not an objective trigger. Confirmed Suggestion or drop.

### Candidate payload format

```text
Candidate: Design — {file}:{line}
Evidence snippet: (≤100 lines showing the signature, return shape, and call site)
Spec excerpt: (the exact clause that constrains the contract, if any)
Reason for escalation: (one sentence stating which of the three properties is at stake)
```

Do not paste full files, full type definitions, or full specs. The smaller the payload, the cheaper and sharper the Phase 2 verdict.
