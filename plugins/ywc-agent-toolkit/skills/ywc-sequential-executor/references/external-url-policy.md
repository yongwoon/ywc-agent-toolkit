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
3. If it exists and validates, use it silently.
4. If it does not exist or does not validate, return `NEEDS_CONTEXT` and do not create or modify configuration.

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

The non-interactive contract names the missing input precisely:
`NEEDS_CONTEXT: .codex/settings.local.json:ywDevSequentialExecutor.externalSpecUrls`.
The executor must not prompt, invent `deny`, or write the missing setting.

## Enforcement during Step 1

- `deny`: ignore external URLs, rely on project-relative paths and record only a bounded policy status.
- `allow`: fetch every external URL; network or auth failures become bounded terminal status, not a prompt.
- `allowlist`: require a non-empty list of canonical HTTPS origins and fetch only matching URLs. Invalid or missing profiles return `NEEDS_CONTEXT`.

## Rationale

Reading the existing profile once per project keeps task ranges deterministic while preserving an explicit, auditable decision boundary.
