# Applied scope and bounded FinOps — scenarios

## AC-8 — scoped-only evidence
1. Supply scoped-only inputs with missing evidence, unbound path, `applied=no`, valid path binding with absent content, and truncated content.

Expected: missing/unbound/unapplied evidence returns BLOCKED with zero reviewer calls; valid binding with missing/truncated content returns NEEDS_CONTEXT with zero calls. `Scope evidence:` records evidence type, target, and rejection reason. No provider/state system is queried and no extra repository/revision fields are required.

## AC-8 — mixed and fresh-only evidence
1. Supply fresh plan/diff plus eligible and ineligible scoped paths; separately omit fresh payload and truncate validly bound content.
2. Exercise fresh-only and topology-only input headers.
3. Give bounded alternatives/utilization/cost evidence, then remove one cost basis.

Expected: all three reviewer lenses receive identical fresh-plus-eligible content; only invalid scoped sets are excluded and documented. Missing fresh input or truncated eligible content returns NEEDS_CONTEXT with zero calls and no excluded-set fallback. N/A headers and existing topology packets remain supported. FinOps compares options using given evidence and requests context instead of estimating missing prices/savings. Agent returns inline content; aggregator owns report files.
