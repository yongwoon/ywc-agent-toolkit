# Verification Block Examples

Concrete shapes for the verification block introduced in `SKILL.md` → Output Format. Pick the shape matching the claim. Each example shows the **before** (unverified assertion) and **after** (gated claim with block).

## Example 1 — Tests pass

**Before (forbidden):**

> Looks good, tests should pass now. Let me commit.

**After (gated):**

**Verification:**

```bash
$ pnpm test --reporter=summary
Test Files  12 passed (12)
     Tests  187 passed (187)
  Duration  6.42s
$ echo "exit=$?"
exit=0
```

**Claim:** All 187 unit tests pass.

## Example 2 — Build succeeds

**Before (forbidden):**

> Lint passed, the build will also pass.

**After (gated):**

**Verification:**

```bash
$ pnpm build
✓ built in 12.34s
$ echo "exit=$?"
exit=0
```

**Claim:** Production build completes with exit 0.

## Example 3 — Bug fix (red-green-red cycle)

**Before (forbidden):**

> I changed the off-by-one, that should fix it.

**After (gated):**

**Verification:**

```bash
$ git stash
$ pnpm vitest run tests/pagination.test.ts -t "rejects offset > total"
 ✗ tests/pagination.test.ts > rejects offset > total
   Expected 400, received 500
$ echo "exit=$?"
exit=1
$ git stash pop
$ pnpm vitest run tests/pagination.test.ts -t "rejects offset > total"
 ✓ tests/pagination.test.ts > rejects offset > total
$ echo "exit=$?"
exit=0
```

**Claim:** The pagination off-by-one is fixed. Reverting the fix returns the test to FAIL (red-green-red verified).

## Example 4 — Multi-command claim (build + test + lint)

When the claim covers multiple gates, run each command and surface one block per command, with a single Claim line at the end.

**Verification:**

```bash
$ pnpm lint
✓ no lint errors
$ echo "exit=$?"
exit=0
```

```bash
$ pnpm tsc --noEmit
$ echo "exit=$?"
exit=0
```

```bash
$ pnpm test
Tests  187 passed (187)
$ echo "exit=$?"
exit=0
```

**Claim:** Lint, type-check, and tests all pass.

## Example 5 — Subagent finished (independent verification)

**Before (forbidden):**

> Subagent reports `Status: DONE`. Moving on.

**After (gated):**

**Verification:**

```bash
$ git status --short
 M apps/web/src/components/PriceTag.tsx
 A apps/web/src/components/PriceTag.test.tsx
$ git diff --stat HEAD
 2 files changed, 87 insertions(+), 4 deletions(-)
$ pnpm vitest run apps/web/src/components/PriceTag.test.tsx
 ✓ 6 tests passed
$ echo "exit=$?"
exit=0
```

**Claim:** Subagent's PriceTag work is on disk (2 files, +87/-4) and its tests pass.

## Example 6 — PR ready to merge

**Before (forbidden):**

> CI looked green earlier, let me merge.

**After (gated):**

**Verification:**

```bash
$ gh pr checks 1234 --json name,state,conclusion
[{"name":"build","state":"COMPLETED","conclusion":"SUCCESS"},
 {"name":"test","state":"COMPLETED","conclusion":"SUCCESS"},
 {"name":"lint","state":"COMPLETED","conclusion":"SUCCESS"}]
$ bash "${CODEX_HOME:-$HOME/.codex}/skills/scripts/poll-pr-reviews.sh" 1234
exit=1   # = no bot reviews surfaced after 10×30s polling
```

**Claim:** PR #1234 has all required checks green and bot-review polling found no surfaced comments.

## Example 7 — Verification fails (NO completion claim)

**Verification:**

```bash
$ pnpm test
FAIL tests/auth.test.ts > login rejects expired token
  Expected: 401
  Received: 200
$ echo "exit=$?"
exit=1
```

**Actual state:** 1 test failing (`tests/auth.test.ts > login rejects expired token`). The fix in `apps/api/src/auth/verify.ts` does not match the expectation. Routing to `ywc-debug-rootcause` to investigate before any further fix attempt — this is failure #2 on the same test today.

(Note: no "done" or "ready" claim appears anywhere. The block always tells the truth; the next sentence either claims success or surfaces the failure with a routing decision.)

## Anti-shape — block AFTER the claim

> Done! Tests pass.
>
> Verification: `pnpm test` → 0 failures.

This is the most common misuse. The reader stops at "Done!" and never reaches the block. **Always put the block above the Claim sentence.**
