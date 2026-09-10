#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EVALS="$REPO_ROOT/codex/agents/evals/evals.json"
CLEANER="$REPO_ROOT/codex/agents/ywc-complexity-cleaner.toml"
HARDENER="$REPO_ROOT/codex/agents/ywc-test-hardener.toml"

command -v jq >/dev/null 2>&1 || { echo "ERROR: jq is required for Codex agent evals" >&2; exit 1; }
test -f "$EVALS" && test -f "$CLEANER" && test -f "$HARDENER"
jq empty "$EVALS" >/dev/null

jq -e '
  .surface == "codex-agents"
  and .contract_reference == "codex/skills/references/quality-gates.md"
  and ([.evals[].name] | index("cleaner-missing-packet"))
  and ([.evals[].name] | index("cleaner-scope-boundary"))
  and ([.evals[].name] | index("cleaner-unavailable-advisory"))
  and ([.evals[].name] | index("cleaner-unavailable-enforced"))
  and ([.evals[].name] | index("hardener-residual-cap"))
  and ([.evals[].name] | index("hardener-scope-and-status"))
  and ([.evals[].name] | index("no-contract-compatibility"))
  and ([.evals[] | select(.name == "cleaner-unavailable-advisory") | .contract_state] | . == ["advisory"])
  and ([.evals[] | select(.name == "cleaner-unavailable-advisory") | .expected_status] | . == ["DONE_WITH_CONCERNS"])
  and ([.evals[] | select(.name == "cleaner-unavailable-enforced") | .contract_state] | . == ["enforced"])
  and ([.evals[] | select(.name == "cleaner-unavailable-enforced") | .expected_status] | . == ["BLOCKED"])
  and ([.evals[] | select(.name == "no-contract-compatibility") | .agent] | . == [null])
  and ([.evals[] | select(.name == "no-contract-compatibility") | .expected_dispatch] | . == ["none"])
  and all(.evals[]; (.expectations | type == "array" and length > 0))
' "$EVALS" >/dev/null

grep -Fq 'exact task-owned production paths and production symbols' "$CLEANER"
grep -Fq 'request that crosses the production/test boundary or exceeds a path or symbol boundary' "$CLEANER"
grep -Fq 'Never edit tests, fixtures' "$CLEANER"
grep -Fq 'Never stage, commit, push, create a PR, merge, release, or otherwise deliver changes.' "$CLEANER"
grep -Fq 'exact task-owned test/fixture paths and symbols' "$HARDENER"
grep -Fq 'request that crosses the test/fixture boundary or exceeds a path or symbol boundary' "$HARDENER"
grep -Fq 'Never edit production code' "$HARDENER"
grep -Fq 'Never stage, commit, push, create a PR, merge, release, or otherwise deliver changes.' "$HARDENER"

echo "PASS: Codex agent evals cover packet/state mapping, exact path boundaries, residuals, and no-delivery authority"
