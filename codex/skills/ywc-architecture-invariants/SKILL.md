---
name: ywc-architecture-invariants
description: >-
  (ywc) Validate an optional repository-root architecture-invariants.json
  contract and bounded normalized edge evidence. Triggers: "architecture
  invariants", "architecture boundary", "architecture contract",
  "boundary validation". Validation-only in v1; never executes verifier data.
  Do not use for: verifier execution, general architecture advisory or design
  trade-off judgment (use ywc-architect), or security review (use
  ywc-security-audit / ywc-security-engineer).
---

# ywc-architecture-invariants

Use the shared helper to validate the optional root `architecture-invariants.json`,
validate normalized evidence, and audit a bounded changed-path scope. The contract
is JSON-compatible and closed: unknown fields, unsafe paths, invalid globs,
ambiguous mappings, and incomplete coverage return `NEEDS_CONTEXT`.

## Interface

```text
ywc-architecture-invariants --mode draft --proposal <path> --output <path> --approve-write
ywc-architecture-invariants --mode validate [--manifest <path>]
ywc-architecture-invariants --mode audit --changed-path <path>... --evidence <path> [--manifest <path>]
```

V1 launches zero child processes and accepts no executable/verifier fields.
Omitted manifest discovery checks only the repository root. An absent discovered
manifest returns `N/A — no architecture contract`; an explicit missing or invalid
manifest never falls back. See [references/contracts.md](references/contracts.md)
for the exact schemas and verdict precedence.
