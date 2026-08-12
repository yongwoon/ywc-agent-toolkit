# Architecture invariants v1 contract

This is the normative closed contract. Objects reject unknown fields recursively.
All arrays are deterministic, sorted, and duplicate-free where stated. Paths are
POSIX, repository-relative, non-empty, contain no `.`, `..`, NUL, backslash, or
escaping symlink. Globs permit literal segments, `*` (one segment), and terminal
`**` (zero or more segments); `?`, character classes, and braces are invalid.

## Manifest

```json
{"version":1,"owner":"team","enforcement":"advisory","components":[{"id":"api","paths":["src/api/**"],"owner":"platform","shared":false}],"rules":[{"id":"api-forbids-ui","source":"api","target":"ui","policy":"forbid","rationale":"layering"}]}
```

`components` and `rules` are non-empty. IDs match `^[a-z][a-z0-9-]*$`; endpoints
must exist, self-edges and duplicate source/target pairs are rejected. There are
no verifier, command, shell, script, argv, registry, or executable fields.

## Evidence and audit result

Evidence has exactly `version`, `scope_paths`, `scope_digest`, `covered_rule_ids`,
and `edges`. The digest is `sha256:` plus SHA-256 of the UTF-8 newline-joined,
sorted scope paths. Each edge has exactly `rule_id`, source/target components,
evidence path, and positive `line`; its path is in scope and its endpoints match
the declared rule.

Audit output has exactly:

```json
{"version":1,"aggregate_verdict":"MAINTAINED","rule_results":[{"rule_id":"api-forbids-ui","verdict":"MAINTAINED","evidence_paths":["src/api/route.ts"]}]}
```

Rule verdicts are `VIOLATED`, `NEEDS_CONTEXT`, `MAINTAINED`, or `N/A`. Aggregate
precedence is `VIOLATED > NEEDS_CONTEXT > MAINTAINED > N/A`; no affected rules is
`N/A`. Forbidden observed edges violate; allowed observed edges maintain; an absent
forbidden edge maintains only with complete coverage; absent allowed-edge evidence
is `N/A`.

## Modes and RED-first coverage plan

`draft` requires `--proposal`, a new root-relative `--output`, and
`--approve-write`; it writes only a validated proposal. `validate` returns advisory
`DONE`, enforced `BLOCKED` (there is no v1 executor), invalid input `NEEDS_CONTEXT`,
or no-manifest `N/A`. `audit` requires changed paths and evidence, requires their
normalized sets and digest to match, and returns the closed audit result. It never
executes a verifier or changes source.

Named RED-first cases recorded before implementation: `closed-unknown-fields`,
`explicit-manifest-no-fallback`, `glob-zero-segment`, `glob-single-segment`,
`glob-terminal-multi-segment`, `ambiguous-non-shared-mapping`,
`scope-digest-mismatch`, `incomplete-rule-coverage`, `forbid-observed-edge`,
`allow-observed-edge`, `verdict-precedence`, `no-manifest-fallback`, and
`zero-child-processes`.
