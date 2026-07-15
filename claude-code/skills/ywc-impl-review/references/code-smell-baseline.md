# Code Smell Baseline (Fowler 12)

> Shared reference for the `ywc-impl-review` Architecture and Design subagents.
> Each agent reads the smells mapped to its aspect and folds them into its
> Phase 1 pass. The parallel/sequential executors point `--review` here too, so
> the same classes are caught **before** the PR opens.

This is a **maintainability** baseline — the recurring structural/naming smells
from Fowler's *Refactoring* that a language-agnostic reviewer can spot in a diff.
It complements `recurring-defects.md`, which catalogs runtime **correctness**
defects (access boundary, error handling, contract/status, security, test
fidelity). When a smell here has a runtime-defect twin there, this file
delegates rather than duplicates.

## Top principles (read before applying any row)

1. **Repo documentation standards override this baseline.** If the project's
   `CLAUDE.md` / `AGENTS.md` / style guide takes a different position on a smell
   (allowed duplication threshold, accepted delegation pattern, naming rules),
   the repo standard wins. This file is the default, not the authority.
2. **Every item is a judgement call, not a lint rule.** A smell is a *signal to
   look closer*, never an automatic finding. Name the concrete cost (harder to
   change, easy to break, misleads the reader) before flagging; if you cannot,
   drop it. Severity follows the aspect agent's own rubric.
3. **Skip items already enforced by tooling.** If the project's linter /
   formatter / type checker already rejects the smell (dead code, unused
   symbols, cyclomatic-complexity gates, naming-case rules), do not re-flag it
   here — the tool is the source of truth and the review depth is better spent
   elsewhere. Note the skip; do not invent a finding to fill the table.

## The 12 smells

| Smell | Definition | Detection signal | Fix direction |
|---|---|---|---|
| Mysterious Name | A name does not communicate what the thing is or does, forcing readers into the body to understand it. | Identifiers needing a comment to explain them; `data`, `tmp`, `handle`, `manager`; jargon or single letters outside tight loops. | Rename to intent-revealing terms. Also flagged by the Design aspect — see `design-agent.md` §2 (Naming Consistency) and the project's `docs/ubiquitous-language.md` if present. |
| Duplicated Code | The same structure appears in more than one place, so a change must be made in every copy. | Copy-pasted blocks; parallel branches with identical bodies; the same literal/logic repeated across files. | Extract Function/Method, pull up to a shared module, or parameterize. Confirm it is real duplication (same reason to change), not incidental similarity. |
| Feature Envy | A function is more interested in another module's data than its own, reaching across the boundary repeatedly. | A method calling many getters/fields of another object; logic that "belongs" to the data it manipulates. | Move Function to the envied module, or Extract the envious slice and relocate it. |
| Data Clumps | The same group of values travels together through many signatures. | The same 3+ parameters recurring across functions; fields that always appear as a set. | Introduce a value object / struct / parameter object and pass it as one unit. |
| Primitive Obsession | Domain concepts are represented by raw primitives instead of small types, so validation and meaning are scattered. | Bare `string`/`number` for money, IDs, dates, ranges, units; validation logic duplicated at each use site. | Introduce a typed value object with validation at construction. Where the primitive is an unvalidated external identifier that fails deep in a side-effecting path, that is the runtime twin — delegate to `recurring-defects.md` §3 (Validation strictness & fail-fast) instead of duplicating the rejection guidance. |
| Repeated Switches | The same `switch`/`if-else` on the same type code appears in multiple places. | Identical `switch (kind)` or type-tag chains scattered across the codebase. | Replace with polymorphism (a type per case) or a lookup table, so a new case is added in one place. |
| Shotgun Surgery | One conceptual change forces small edits across many modules. | A single feature change touching many unrelated files; edits that must stay in lock-step. | Move Function/Field to consolidate the scattered responsibility into one module (inverse of Divergent Change). |
| Divergent Change | One module is changed for many unrelated reasons. | A file edited by nearly every feature; a class mixing several axes of change. | Split the module along its axes of change so each has a single reason to change. Architecture-aspect concern — see `architecture-agent.md` §2 (Pattern Consistency). |
| Speculative Generality | Abstraction added for a future that has not arrived, paid for now in complexity. | Unused hooks/params, single-implementation interfaces, generic base classes for one case, "in case we need it later". | Collapse the abstraction (Inline, Remove Parameter) to the minimum the spec requires. Architecture-aspect concern — see `architecture-agent.md` §4 (Simplicity / Over-Abstraction, YAGNI). |
| Message Chains | A client navigates a long chain of objects (`a.getB().getC().getD()`), coupling it to the whole path. | Sequences of accessor calls tunnelling through intermediate objects. | Hide Delegate — expose a method on the first object so callers stop knowing the chain's shape. |
| Middle Man | A class delegates most of its work to another, adding no value of its own. | A wrapper whose methods only forward to a collaborator; near-empty pass-through layer. | Remove Middle Man and let callers talk to the real object, or fold the small residual logic in. |
| Refused Bequest | A subclass inherits methods/data it does not want or use, breaking the substitution contract. | Subclass overriding parents to throw/no-op; inherited members left unused; `is-a` that is really `has-a`. | Push Down the unwanted members, or replace inheritance with delegation (composition). |

## Aspect mapping (which agent owns which smell)

- **Architecture aspect** (`architecture-agent.md`): Duplicated Code, Divergent
  Change, Shotgun Surgery, Speculative Generality, Middle Man, Refused Bequest,
  Message Chains, Repeated Switches — structural/coupling smells.
- **Design aspect** (`design-agent.md`): Mysterious Name (naming), plus
  Data Clumps and Primitive Obsession where they surface at the public
  signature / contract seam.

A smell can inform both aspects; flag it in the lane that owns the fix and
cross-reference the other at most as a one-liner. Do not duplicate a sibling
agent's finding.
