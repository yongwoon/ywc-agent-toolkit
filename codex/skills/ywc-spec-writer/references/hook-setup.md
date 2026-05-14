# Hook Setup

Install a git pre-commit hook that marks when a spec update is needed after significant code changes.
The hook itself is intentionally lightweight — no Claude API calls inside git hooks.

## How It Works

1. Pre-commit hook runs `detect-affected-sections.sh` on staged files
2. If spec-relevant changes are detected, creates `.spec-update-pending` with the affected sections list
3. After the commit completes, user runs `/ywc-spec-writer` which reads the marker and updates the spec

This design keeps commits fast while ensuring spec updates are never forgotten.

## Marker File Format

`.spec-update-pending` (add to `.gitignore`):

```
abc1234
02-features.md
03-data.md
```

Line 1: commit hash. Remaining lines: spec sections that need updating.

## Installation

Run `/ywc-spec-writer --setup-hook` or manually:

```bash
cp codex/skills/ywc-spec-writer/scripts/spec-update-hook.sh tools/scripts/
ln -sf ../../tools/scripts/spec-update-hook.sh .git/hooks/pre-commit
chmod +x tools/scripts/spec-update-hook.sh
echo ".spec-update-pending" >> .gitignore
```

## What the Hook Does

1. Check if `docs/specification/` exists — if not, skip (no spec yet)
2. Run staged files through `detect-affected-sections.sh`
3. If sections detected: write `.spec-update-pending` with commit hash + section list
4. Print: `[spec-writer] Spec update pending — run /ywc-spec-writer after this commit`
5. Always exit 0 — never block the commit

## Processing a Pending Update

When `/ywc-spec-writer` is invoked without flags and `.spec-update-pending` exists:

1. Read the marker to get commit hash and affected sections
2. Run `git diff <hash>^..<hash>` for the relevant changed files
3. Update only the listed spec sections
4. Delete `.spec-update-pending` after a successful update

## Codex PostToolUse Alternative

For teams using Codex exclusively, add to `Codex approval settings`:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "command": "tools/scripts/spec-check-on-commit.sh"
    }]
  }
}
```

The script checks if the Bash tool just ran a `git commit` command, then creates the `.spec-update-pending` marker if spec-relevant files were committed.

## Uninstall

```bash
rm .git/hooks/pre-commit
```
