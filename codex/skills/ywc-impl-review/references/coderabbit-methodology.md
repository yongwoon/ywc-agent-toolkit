# CodeRabbit-Derived Review Methodology

> Reference for `ywc-impl-review`. Distilled from CodeRabbit's published review
> methodology and adapted to this skill's two-phase, multi-agent shape. The point
> is not to imitate a hosted bot — it is to import the concrete techniques that
> make its reviews high-signal, in a runtime-agnostic form that works whether or
> not the project uses CodeRabbit.

## Why import these

CodeRabbit's reviews are valued for high precision (few false positives) and for
getting *sharper per repository over time*. Both qualities come from a small set
of transcribable mechanisms, listed below. Several already exist in this skill
(severity rubric, two-phase advisor, Confidence Gate, recurring-defects catalog);
this file names the gaps worth closing and the principles behind them.

## 1. Verbosity dial — `chill` vs `assertive`

The single most impactful noise control. The reviewer's default posture should be
**chill**: surface only bugs, security, logic errors, and runtime-failure risks;
stay silent on style, naming polish, missing docs, and minor quality unless asked.
**assertive** adds those back. Noise is the enemy of adoption — a review that
raises ten nitpicks for one real bug trains the reader to ignore all ten-and-one.

Mapping for this skill: `--profile chill` (default) suppresses `Low`/`Info`
findings whose category is Style/Devex-polish/Docs unless they block correctness;
`--profile assertive` emits them. Critical/High/Medium are never suppressed by the
profile — only the nitpick tail is.

## 2. Verify-before-surface (the precision lever)

CodeRabbit's biggest precision gain is an agentic verification step: each candidate
finding is checked for accuracy *before* it is posted, and unsubstantiated ones are
dropped. This skill already separates authoring (Phase 1) from frontier judgment
(Phase 2) and gates on Evidence quality. Strengthen it with an explicit rule:

> Before a reviewer surfaces a finding, it must cite primary evidence — the exact
> file:line, the symbol traced to its definition/callers, or fresh command/test
> output. A finding that cannot be substantiated by re-reading the code or running
> a scoped check is **dropped**, not surfaced with a hedge. "This might be wrong"
> without evidence is noise.

This is the mechanism behind the Confidence Gate's Evidence-quality dimension —
make it a per-finding gate, not only a report-level one.

### SDK hierarchy evidence gate

Use the [Devex SDK exception check](./devex-agent.md#sdk-exception-hierarchy-evidence) for SDK-specific catch/retry findings. Retain inspected package/version, version-relevant primary source or official error-reference citation, actual exception inheritance and the reviewed throw/catch path as provenance. Unavailable or version-mismatched primary evidence is uncertainty: record the verification gap separately and do not emit a confirmed SDK hierarchy finding based on an inline comment or recollection. A version match alone does not prove a defect; require the traced hierarchy and affected operation to establish it. No unconditional network phase or new SDK dependency belongs in mechanical verification; use existing bounded review acquisition and report missing evidence honestly. Offline source assertions and predetermined fixtures are not observed SDK review behavior.

## 3. Context phase before commenting

CodeRabbit never reviews the diff in isolation: it builds a dependency picture of
the change (callers/callees, cross-file impact) and extracts *intent* from the PR
description and linked issues, then reviews against that intent. For this skill:

- Trace each changed symbol to its callers and callees before judging it — a
  change that is locally fine can break a caller's contract.
- Treat the spec (or PR description) as the statement of intent; a finding is
  stronger when it names which intent the code violates, not just a style gap.
- Maintain a rough 1:1 code-to-context ratio: for the lines under review, pull in
  an equal weight of the surrounding code that determines whether they are correct.

## 4. Static analysis as evidence, not verdict

Run the project's own linters/scanners (ruff, eslint, golangci-lint, shellcheck,
semgrep, gitleaks, hadolint, ast-grep — whatever the repo already has) and feed
their output to the reviewers as *evidence*. The LLM's job is to triage, explain,
and assign severity — not to re-derive what a deterministic tool already proves.
A finding backed by a tool hit plus an explanation is higher-signal than either
alone. Never let a tool's raw output *be* the review; never ignore it either.

### Targeted rules for recurring defects

Use only already installed, stack-appropriate tools on changed files. Check the
installed version's supported flags and existing project configuration first.
Never install a tool or change lint configuration during review.
Report each unavailable tool as `unavailable` without blocking unrelated review scope.
Missing required configuration or unsupported flags are verification gaps; record
why the targeted check cannot run, then apply the catalog scan cues manually.

| Changed files | Installed check (read-only) | Scope / limitations |
|---|---|---|
| `*.py` | `ruff check --select S110,BLE001,B904 <changed-files>` | §2 swallowed/broad exceptions and exception chaining; no fix mode |
| `.github/workflows/*` | `zizmor --offline <changed-workflows>` | Inspect `artipacked` and `unpinned-uses`; A-005 requires a later exposure step |
| `*.ts` / `*.tsx` | Project ESLint on changed files | Only if existing type-aware configuration enables `no-floating-promises` and `no-misused-promises`; check `ignoreVoid: false` coverage, otherwise scan `void p` manually |
| `*.go` | `golangci-lint run --enable-only errcheck <changed-pkgs>` | If supported by installed version; package analysis is necessary, but retain only hits in changed files. `_ =` and unchecked assertions require existing `check-blank` / `check-type-assertions`; otherwise apply A-007 scan cues manually |

Every linter hit must pass §2 verify-before-surface before becoming a finding.
Trace the affected operation, callers, handling and severity rationale; broad
`except` that logs and re-raises is legitimate. A tool hit alone never decides a
finding. No hit does not prove the defect class absent.
Record tool/version, checked paths, rule, output location and verification result;
keep unavailable checks separate from confirmed findings. Finding provenance also
retains primary `file:line` or fresh scoped output and the relevant catalog ID.

Frozen behavioral source: PR #340 at
`2b7c54058da6f15f6c16b9aee5de021fac35f42f`,
`tools/claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md`.
These instructions and offline fixtures are not live linter/model execution evidence.

## 5. Every comment is a patch

A finding lands better as a concrete, committable suggestion plus a one-line
rationale ("why it matters") than as prose. Where the fix is unambiguous, include
the corrected snippet. This skill's findings should carry the fix direction, not
just the diagnosis — the reader should be able to act without a second round-trip.

## 6. Effort signal

CodeRabbit tags findings with an effort estimate (quick win / heavy lift / poor
tradeoff / low value). A reader triaging a long list needs to know which fixes are
cheap. Optional for this skill: annotate Medium/Low findings with a one-word effort
hint so the Fix Priority section is actionable, not just severity-sorted.

## 7. Per-project learnings (the compounding mechanism)

This is what makes CodeRabbit improve per repository: an accumulating, natural-
language memory of review preferences, each recording *what + why*, applied on
every subsequent review. In this toolkit that memory is `docs/review-learnings.md`,
owned by `ywc-review-learnings`. The integration:

- **Before review** — load the learnings whose scope matches the changed files and
  inject them into each reviewer (a `DO`/`DO-NOT` learning becomes an extra check;
  a `FALSE-POSITIVE` learning tells the reviewer to *stop* raising a known non-issue).
- **After review** — promote confirmed, recurring findings into new `DO` learnings,
  and capture user-dismissed findings as `FALSE-POSITIVE` learnings with the reason.

The why-storage is essential: a learning that records only *what* cannot generalize
to similar-but-different code and decays into a brittle keyword match.

## Sources

CodeRabbit official docs and engineering blog — learnings, code-review overview,
tools reference, YAML configuration, context-engineering, and agentic code
validation posts (docs.coderabbit.ai, coderabbit.ai/blog). Exact emoji/label
strings should be confirmed against the live docs before being transcribed
verbatim into output; this skill uses its own shared severity vocabulary
([symbols.md](../../references/symbols.md)) rather than copying CodeRabbit's label set.
