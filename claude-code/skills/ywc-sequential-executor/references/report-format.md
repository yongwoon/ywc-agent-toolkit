# Completion Report Format — `ywc-sequential-executor`

> Reference for the report body displayed after a run. Linked from the skill's "Completion Report" section. The `Completion Status` table and the Operational Self-Improvement / State cleanup rules stay in `SKILL.md`.

## 1. Report Content

After all tasks are executed, display:

- Total tasks executed: N
- Each task: name, PR URL, PR status (draft / open / merged) — or `local-merge` with the merge commit SHA when `--local-merge` is used
- Any tasks that were skipped or failed (with reason)
- Current branch and sync status
- Changed public contracts (interfaces/signatures/DTOs altered), tests that first failed (RED) then passed, and any critical-path tasks that triggered `/ywc-security-audit`
- If in draft/skip-ci-wait mode: remind user that PRs need manual review and merge
- If in local-merge mode: remind user that no PR was created and no CI ran remotely — only the local verification from Step 4 gates the merge

**When `--terse` is set**, omit all prose reminders and mode-specific explanations. Emit only:
1. The task table (name | status | PR URL or merge SHA)
2. The `Completion Status` line

This is the preferred format for CI scripts or automation that parse the report output.

**Reporting Symbols**: Use the shared vocabulary in [symbols.md](../../references/symbols.md) for the per-task status column and inline step traces. The symbol is a scan aid, not a replacement for the status text — keep both. For multi-step traces inside a single task report, use the flow operator `»` (e.g. `branch ✅ » impl ✅ » verify ✅ » PR ✅ » merge ✅`). Do not use symbols inside commit messages, PR titles, or generated source code — they belong to the report layer only.

Example task table row:

```
000003-010-add-auth-middleware  | ✅ merged   | https://github.com/.../pull/142
000003-020-add-rate-limiting    | 🚫 blocked  | depends on 000003-010 (failed)
```

## 2. Placement

The report is displayed once, after the final task of the run completes. The `Completion Status` line from `SKILL.md` is always the last line of the report; nothing in this reference follows it.
