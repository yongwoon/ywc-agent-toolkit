# Mine Review History

Batch-mine bot review comments across a bounded window of merged PRs and present recurring defect classes as confirmation-gated review-learning proposals. Use `--limit` or `--since`; recurrence counts distinct PRs. Resolution plus later-fix evidence is required for `DO`, while reasoned human dismissal is required for `FALSE-POSITIVE`; ambiguous evidence is dropped.

The skill never writes project learnings or a shared catalog directly. Confirmed local changes delegate to `$ywc-review-learnings --mode update --source mining`; shared-catalog matches are maintainer proposals only.

```text
$ywc-mine-review-history --limit 50
$ywc-mine-review-history --since 2026-01-01 --min-recurrence 4
```

See [SKILL.md](./SKILL.md) for the complete workflow and helper contract.
