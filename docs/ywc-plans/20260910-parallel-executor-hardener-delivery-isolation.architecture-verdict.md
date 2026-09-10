# Architecture Verdict — Wave Hardener Delivery Isolation

> Produced by `ywc-plan` Step 3.5 (Architectural Advisor Gate), advisor `ywc-architect`.
> Date: 2026-09-10
> Consumed by: `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md`
> Advisor status: `DONE_WITH_CONCERNS`

Subsequent planning cites this file rather than re-litigating the decision.

## The framed decision

`ywc-parallel-executor`'s wave-boundary mutation gate (Hardener, Step 4e.5) runs *after* the wave's tasks have already been delivered into the base branch, so an `enforced` gate returning `BLOCKED` cannot prevent anything. The proposed remedy is a temporary **wave integration branch**: merge wave tasks there, run Hardener against it, and promote to base only on success.

The question put to the advisor was narrower than "should we do this": the four delivery modes are structurally different, so should the integration-branch model apply **uniformly**, or should one or more modes deliberately diverge — and by what *rule*, not by per-mode enumeration.

## Verdict

**Not uniform.** Apply the wave integration branch to `--local-merge`, `--draft`, and `--aggregate-pr`. `--per-task-pr` deliberately diverges and cannot be isolated at the wave boundary.

**The principled rule** (verbatim from the advisor):

> *An isolation branch can only protect state whose point-of-no-return sits after the gate.*

For three modes the point-of-no-return is end-of-run (`--draft` / `--aggregate-pr`) or a re-pushable local base (`--local-merge`) — both after 4e.5. For `--per-task-pr` the point-of-no-return is `gh pr merge --delete-branch` **inside** the wave, once per task. No branch topology moves a per-task irreversibility boundary behind a wave boundary. It is a timing property, not a topology one.

## Trade-off table

| Option | Cost | Benefit |
|---|---|---|
| **A. Integration branch for the 3 local modes; `--per-task-pr` carved out** (chosen) | One carve-out to document; `--per-task-pr` keeps the known-weak gate | Generalizes existing prior art (`ywc-sequential-executor`'s `work/<name>` and `--worktree` integration branch); branch lineage unchanged across waves |
| B. Uniform — retarget per-task PRs to `wave-int/<N>` | A second int→base PR per wave = a full extra CI + bot cycle; required-checks / branch protection are configured for the real base, not `wave-int/*`; per-task PRs are no longer reviewed against base | Superficial uniformity |
| C. Severity-scoped — isolate only `enforced` contracts | Two branch topologies selected at runtime by contract severity; resume must know which one ran | Slightly cheaper on advisory waves |

Option B is a rebuild of `--aggregate-pr` under a different flag name. Rejected.

## `--per-task-pr` specifically

Retargeting each task PR's base to the wave integration branch is **unsound** — it destroys the exact signal the mode exists to buy (bot review + CI + branch protection evaluated against the real base).

**Honest fallback**: `--per-task-pr` may not declare `enforced` at the wave boundary. Cap it at `advisory` there, and let its blocking authority live at Step 4c.5 (per-task, pre-PR), where a gate can still stop something. The cross-task interaction check in this mode is **reporting only**, and the skill must say why.

## Branch lineage — the constraint dissolves

Step 4e's rule "downstream waves branch from it" appeared to force a run-wide lineage change. It does not.

Wave N delivers onto `wave-int/<N>` (branched from base). On Hardener pass, promote by fast-forwarding base to `wave-int/<N>`, then push (`--local-merge`) or defer (`--draft` / `--aggregate-pr`). Post-promotion base content is identical to the integration branch, so wave N+1 still branches from base. **Lineage changes within a wave only, never across waves**, and Step 4e's existing statement stays true.

## Checkpoint and resume impact

Minimal. No new subcommand is strictly required:

- `task-merged <N> <task>` — semantics shift from "merged onto base" to "merged onto `wave-int/<N>`". No schema change.
- `wave-complete <N>` — becomes the **promotion** checkpoint, stamped only after Hardener passes and the fast-forward lands. Its existing "refuses if any task is still pending" guard already fits.
- Add exactly one field: `waves[].integration_branch`. Resume needs the branch name to find un-promoted work.

Resume stays coherent and in fact improves: a wave with `pending: []` and `status != completed` becomes unambiguously "merged onto integration, not yet promoted" → re-run Hardener (a measurement gate, idempotent) and retry promotion. Today that same interruption is indistinguishable from a completed wave.

## Codex variant

The codex prose ("Before delivery, aggregate…") is the **correct intent**; the numbering/placement is the bug. Fix the placement to match this model rather than treating it as deliberate runtime divergence.

## Advisor concerns (`DONE_WITH_CONCERNS`) — quoted verbatim

**Concern 1.**

> Validate one assumption before acting: that the projects consuming `--local-merge` tolerate a **wave-granular** push instead of the current per-task immediate push. If any consumer depends on per-task remote visibility mid-wave, `--local-merge` moves into the `--per-task-pr` carve-out and only `--draft`/`--aggregate-pr` get isolation. Check this before writing the rule, because it decides whether the carve-out has one member or two.

**Concern 2.**

> Promotion is described as a fast-forward. That holds only if base did not advance during the wave. If an external push moved base, the fast-forward fails and promotion silently becomes a merge — which can introduce conflicts *after* the Hardener already passed on the un-merged integration branch. Specify the behavior for that case explicitly (re-run Hardener after the merge, or `BLOCKED`); do not leave it implied.

## ADR recommendation

**`ADR Recommendation: yes`.** The trade-off is a permanent mode carve-out (one of four delivery modes structurally cannot honor an `enforced` wave gate) plus a change to `wave-complete`'s meaning. Both are surprising to a future reader and expensive to reverse once the checkpoint semantics ship — which satisfies `ywc-adr`'s three-part test (hard to reverse + surprising without context + real trade-off).
