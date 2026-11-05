# Durable mission anchor — scenarios

## AC-7 — read and durable update flow
1. Read a missing mission file and a legacy mission file.
2. Propose the first mission entry and a multi-entry ADD/MODIFY/DEPRECATE changeset; attempt a non-empty update before and after exact user confirmation.
3. Exercise dry-run and empty changeset paths.

Expected: missing read returns an empty anchor; legacy records remain readable; the complete file is read before proposal; non-empty durable writes occur only after confirmation of the exact changeset; dry-run and empty changeset make no file or date changes.

## AC-7 — identity and optional sections
1. Add an active mission with observable success criterion and rationale, a rejected approach with reason, and optional NG/CN rows with required reason/rationale.
2. Deprecate an NG/CN row, attempt ID reuse/deletion, then remove all active optional rows.

Expected: only one mission is active; IDs remain stable and deprecated history is retained; deprecated IDs cannot be reused/deleted; active-only anchors omit deprecated rows; optional sections disappear when no active rows remain while preserving history. Initial creation gives activation guidance without modifying AGENTS/CODEX files. Skill list/selected install discoverability is checked at distribution integration.
