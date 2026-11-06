# Handoff Skill (ywc-handoff)

> **User-invoked skill** — run it directly with `/ywc-handoff`. The model does not route to it automatically (`disable-model-invocation: true`), and other skills cannot call it through the Skill tool.

A Claude Code Skill that compacts the current conversation into a handoff document a fresh Agent session can pick up. Based on `handoff` from `mattpocock/skills`.

## Overview

- Written in eight sections: Goal / State / Decisions / Dead ends / Next step / Waiting on user / References / Suggested skills
- Each State thread starts with one status tag checked with `gh pr view` / `git branch`; when it cannot be checked, `[unverified]` is written with the reason
- Waiting on user records only the decisions the user alone can make, as call / pick / evidence / risk (`N/A — nothing waits on the user` when empty)
- Existing artifacts — spec, plan, ADR, issue, commit, diff — are **referenced by path or URL, never copied**
- API keys, passwords, tokens, and personal data are replaced with `<REDACTED>` **before** anything is written (body, code blocks, logs, URLs, file name, task name)
- Saved to the OS temp Directory (`${TMPDIR:-/tmp}`) only when its canonical path is outside the repository; the file is created with `mktemp` and its mode `0600` is checked

## Usage

```text
/ywc-handoff
/ywc-handoff next session only handles PR review responses
```

## Options Reference

- **Invocation**: `/ywc-handoff`
- **Input**: what the next session will be used for (optional) — when given, every section is tailored to it

No flags.
