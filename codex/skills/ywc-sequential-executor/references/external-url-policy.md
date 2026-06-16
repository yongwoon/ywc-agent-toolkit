# External URL Policy

Use this policy when a task's `README.md` includes `Spec Reference > Primary Sources` entries that point to `http://` or `https://` URLs.

## Why the policy exists

- Prevent mid-run hangs caused by auth walls, rate limits, or flaky external services.
- Avoid exposing external documents to the model without an explicit project decision.
- Preserve the sequential executor's non-stop execution behavior across a task range.

## Project-level decision

Run this check once during Pre-flight, before touching any task.

1. Read `.codex/settings.local.json`.
2. Look for `ywDevSequentialExecutor.externalSpecUrls`.
3. If it exists, use it silently.
4. If it does not exist, ask the user once and persist the answer under `ywDevSequentialExecutor`.

Expected shape:

```jsonc
{
  "permissions": { /* preserve existing keys */ },
  "ywDevSequentialExecutor": {
    "externalSpecUrls": "deny",
    "externalSpecUrlAllowlist": [
      "github.com",
      "figma.com/file"
    ],
    "decidedAt": "2026-04-05"
  }
}
```

If the file does not exist, create it with both the existing `permissions` structure and the `ywDevSequentialExecutor` key.

## Prompt when no policy exists

Ask once with a concrete choice:

> Some tasks may list external URLs in their Spec Reference. How should I handle them: `deny` (recommended), `allow`, or `allowlist`? I will save the choice to `.codex/settings.local.json` so I do not need to ask again.

## Enforcement during Step 1

- `deny`: ignore external URLs, rely on project-relative paths and the Summary field, and log skipped URLs.
- `allow`: fetch every external URL. Treat network or auth failures as warnings, not fatal errors.
- `allowlist`: fetch only URLs whose host or host-plus-path prefix matches an allowed entry. Skip the rest and log them.

## Rationale

Persisting the choice per project avoids repeated prompts that would break range execution while still keeping the decision explicit and auditable.
