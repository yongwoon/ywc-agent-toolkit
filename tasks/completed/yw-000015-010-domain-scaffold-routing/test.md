# yw-000015-010-domain-scaffold-routing — Manual Test Plan

## Preconditions
- [ ] Read `codex/skills/ywc-project-scaffold/SKILL.md` and the source spec.

## Test Scenarios
### Scenario 1: Uncontested medium scaffold
**Steps:**
1. Submit a medium, non-contested scaffold request.
2. Inspect the expected behavioral path.

**Expected Result:**
- Trend Check is skipped and the existing structured scaffold report remains the fast baseline.

### Scenario 2: Large or contested scaffold
**Steps:**
1. Submit a large request or explicitly challenge its architecture.
2. Inspect the research handoff and resulting report rules.

**Expected Result:**
- `ywc-tech-research --depth 25` is required; only material deltas appear in a labelled Extras callout, and unavailable evidence produces `DONE_WITH_CONCERNS` without changing the tree silently.

### Scenario 3: Reference refresh
**Steps:**
1. Ask to refresh `references/go.md` without supplying a framework.
2. Inspect the mode, inferred target, evidence route, proposal, and approval boundary.

**Expected Result:**
- The skill returns `Mode: reference-refresh`, uses language-only research when needed, proposes additive changes, displays a diff, and stops for explicit approval before editing.
