# Readable Code Rubric — Shared SoT for ywc-* Skills

> Shared reference document. The single source of truth for "what readable, low-defect code looks like" across the `ywc-*` collection. Generation skills write *to* this rubric, review skills score *against* it, and planning skills set design expectations *from* it — one yardstick, three uses. This keeps "the standard we write to" and "the standard we review against" identical.
>
> Provenance: distilled from `docs/research/readable-code-and-anti-patterns.md` (~40 sources — The Art of Readable Code, refactoring.guru, martinfowler.com, sonarsource.com, GitClear, peer-reviewed studies). That digest holds the evidence and citations; this file is the operational distillation. Companion to [principles.md](./principles.md) (§5 Clarity points here).

## How skills use this file

- **Generation** — `ywc-code-gen` backend/frontend/qa agents: aim for clusters A–H while writing. Reuse before adding (§E); match the surrounding file's conventions (§A).
- **Review** — `ywc-impl-review` devex agent: score against A–H, but treat §"Countable vs relational" and §"Anti-dogma guardrails" as binding. Do not raise a finding a guardrail forbids.
- **Planning** — `ywc-plan`: when defining structure, naming, and boundaries, ground choices in §G (structural smells) and §"Anti-dogma" (do not specify speculative generality or premature abstraction the requirement does not yet need).

This file is **language-agnostic** on purpose. Language-specific idioms (Go pointer receivers, Python dunder methods, React hook rules, etc.) belong to the per-language reviewers (`ywc-typescript-reviewer`, `ywc-python-reviewer`, `ywc-go-reviewer`), not here.

## The one rule everything serves

Code should minimize the time the next reader needs to understand it well enough to change it, find bugs in it, and see how it fits the rest of the system. Shorter is *not* automatically better — compression only helps when it also reduces time-to-understand. Every cluster below is a means to this end; when a rule and this goal conflict, the goal wins.

When this rubric motivates a *cleanup* (a refactor or simplification, not new behavior), preserve exact behavior — change *how* the code does something, never *what* it does. A simplification that alters an output, a side effect, or an error path is a defect, not a cleanup.

## Rubric — 8 clusters

### A. Naming

- Pack information into names; a good name is a tiny comment. Reject generic names (`tmp`, `data`, `foo`, `retval`, `result`, `value`, `item`) unless the scope is a few lines and "temporary" is the variable's only salient property.
- Prefer specific verbs (`fetch`/`download` over `get`, `kill`/`pause` over `stop`) and concrete over abstract.
- Encode units and critical attributes (`delay_secs`, `size_mb`, `plaintext_password`, `raw_input`, `safe_html`); flag a bare number whose unit is not in the name.
- Disambiguate names whose inverse is plausible (`filter` → `select`/`exclude`); use `min_`/`max_` for inclusive limits, `is`/`has`/`can`/`should` + positive phrasing for booleans (`use_ssl`, not `disable_ssl`).
- Scale name length to scope; **match the naming already used in the surrounding file** rather than introducing a competing convention.

### B. Functions & control flow

- One task at one level of abstraction per function. Judge extraction by whether it *separates intention from implementation* (a name that hides detail), **not** by a line count.
- Flatten nesting with early returns / guard clauses; put the changing value on the left of a comparison (`if (length >= 10)`), handle the positive/simple case first, avoid `do/while` and `goto`.
- Avoid nested ternaries; prefer a `switch` or `if`/`else` chain for multiple conditions, and keep any `?:` to a single simple expression.
- Keep signatures lean (≤2 args preferred). Avoid flag/boolean arguments (a flag usually means the function does two things) and hidden side effects beyond what the name promises.

### C. Comments

- `GOOD CODE > BAD CODE + COMMENTS`. Do not comment to compensate for an unclear name — fix the name.
- Comment the *why* (intent, trade-off, rejected alternative, value rationale, surprising behavior), never restate the *what*. Show corner-case behavior with an input/output example; label non-obvious literal arguments.
- Tag known shortcuts with `TODO`/`FIXME`/`HACK`. Delete iterative-process debris (chat-artifact comments like `// now switching approach per feedback`).

### D. Variables & expressions

- Eliminate single-use temporary / intermediate / control-flow variables that add no clarity; shrink each variable's scope; prefer write-once (immutable) variables.
- Break a giant expression with an explaining or summary variable; simplify a negated boolean chain with De Morgan's laws rather than cramming logic onto one line.

### E. Duplication & reuse

- Before writing a helper, search the repo for an existing equivalent and reuse or extend it (the most common AI-code defect is a near-duplicate helper under a new name).
- Extract genuinely duplicated logic — **but** prefer leaving code duplicated over committing to an uncertain abstraction. An abstraction that grows boolean flags / conditional branches to serve divergent callers is "the wrong abstraction"; re-inline it. Wait until the commonality is obvious (Rule of Three / AHA).

### F. Size & complexity (countable — these are heuristic flags, not auto-fail)

- Function ≤ ~50 lines; file ≤ ~400–500 lines; nesting depth ≤ 3–4; parameters ≤ 4.
- Cyclomatic complexity ≤ 20; **cognitive complexity ≤ 15** — prefer cognitive complexity as the readability proxy (it penalises nesting and rewards a flat `switch`; cyclomatic only tracks testability).
- Replace magic numbers/strings with named constants; move hard-coded environment values (URLs, paths, ports, credentials) to config.
- Every threshold here is a flag that warrants a look, **not** a defect on its own. See §"Anti-dogma".

### G. Structural smells (relational — require judgment / AST, not a single count)

- One reason to change per unit (cohesion); low and stable coupling. Flag a unit that reaches into another's internals or that one logical change scatters across many files.
- Watch for: God Object (a class named `Manager`/`System`/`Driver` concentrating unrelated work), Feature Envy (a method using another object's data more than its own), Message Chains (`a.b().c().d()`), Data Class, Refused Bequest, Action-at-a-distance (behavior driven by distant shared mutable state).
- Remove speculative generality — unused extension points, parameters, or single-implementation interfaces with no stated second use (YAGNI).

### H. AI-agent specifics (highest-frequency failure modes of generated code)

- Validate inputs only at real, reachable boundaries; do not stack null/type/empty guards a single caller cannot trigger, nor end a `try`/`catch` in a hard-coded `null`/`[]`/`""`.
- Match the surrounding file's error-handling and immutability idioms; do not introduce a competing pattern for an existing concept.
- For any external/library API call, verify the signature against current docs (hallucinated APIs are the single largest source of AI-code bugs); cite the version/URL where the skill records evidence.
- Tests must assert real behavior; never mock the unit under test or weaken CI to pass (removing/skipping tests, lowering coverage thresholds, appending `|| true` is a hard block, not a fix).
- Keep the diff reviewable and incremental; split unrelated changes.

## Countable vs relational

The split tells a reviewer what a linter already enforces versus what needs human/agent judgment — so review effort lands where automation can't reach.

| Mechanically checkable (defer to the linter where one exists) | Requires judgment |
|---|---|
| Function/file length, nesting, params → ESLint `max-lines-per-function` / `max-lines` / `max-depth` / `max-params` | Whether an abstraction is *needed* vs speculative (§E, §G) |
| Cyclomatic / cognitive complexity → ESLint `complexity`, SonarQube cognitive complexity | Whether a new helper duplicates the *intent* of an existing one (semantic) |
| Magic numbers, unused vars, broad `except` → `no-magic-numbers`, `no-unused-vars`, ruff/pylint | Whether a defensive guard is genuinely unreachable |
| Duplication density → SonarQube, jscpd | Whether a comment explains *why* vs restates *what* |
| CI integrity (removed/skipped tests, `\|\| true`) → diff check | Whether the code is a "good citizen" of the local convention |

When a project already runs the linter, do not hand-flag what the linter owns — review the judgment column.

## Anti-dogma guardrails (do NOT enforce these as hard rules)

These guardrails bound the rubric so review does not generate false positives and generation does not over-engineer. The contested rules below are real engineering folklore that the evidence does not support enforcing mechanically.

1. **Do not force tiny functions (2–4 lines).** Judge by intention/implementation separation and naming, not LOC. Splitting a cohesive routine into a deep call chain of single-use wrappers reduces readability.
2. **Do not always prefer polymorphism over `switch`/`if-else`.** It is a trade (types vary → polymorphism; operations vary → `switch`), not an upgrade; a flat `switch` over a closed type set is readable, and replacing it in a hot path costs performance.
3. **Do not mirror every class with a 1:1 interface.** Add an interface only when a second implementation or a real architectural boundary (e.g. a hexagonal port) exists.
4. **Do not forbid all duplication.** Tolerate duplication until the right abstraction is obvious; the wrong abstraction is more expensive than the duplication.
5. **Do not enforce the Law of Demeter by counting dots.** Enforce the intent (don't reach through to a stranger's internals); allow fluent builders, collection pipelines (`map().filter()`), and stable public data structures.
6. **Do not treat more layers/indirection as inherently cleaner.** Flag over-architecture: a feature that can't be built within the existing abstractions, or behavior that needs a debugger to trace.
7. **Do not treat a complexity number as an automatic defect.** Empirically, cyclomatic and cognitive complexity are only weak predictors of understandability — use the thresholds in §F as review triggers, not pass/fail gates.
8. **Do not over-simplify.** Clarity beats brevity — reject clever dense one-liners and nested ternaries, do not merge unrelated concerns into one unit to cut lines, and keep an abstraction that genuinely aids organization. The goal is less time-to-understand, not fewer lines.

When a finding rests only on a §F threshold and a §"Anti-dogma" guardrail exempts it, drop the finding or downgrade it to a Suggestion with the reasoning stated.
