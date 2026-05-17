---
name: ywc-incident-postmortem
description: >
  (ywc) Use when a production incident has occurred and you need a structured postmortem:
  timeline reconstruction, root cause analysis (5 Whys), impact assessment,
  prevention action items, and optionally a sanitized client-facing report.

  Trigger phrases: "장애 회고", "포스트모텀 작성", "postmortem", "incident report",
  "장애 보고서", "장애 원인 분석", "사고 회고록", "ポストモーテム", "インシデントレポート",
  "障害振り返り", "outage report", "incident postmortem"

  Do not use for: proactive security vulnerability scanning before an incident
  (use ywc-security-audit); general code quality review unrelated to an incident
  (use ywc-impl-review); generating changelog or release notes after a fix
  (use ywc-changelog-release-notes).
---

**Announce at start:** "I'm using the ywc-incident-postmortem skill to write a structured incident postmortem."

## Rationalization Defense

| Excuse | Reality |
|---|---|
| "This is a minor incident — no postmortem needed" | Even 5-minute outages teach systemic lessons. A short postmortem beats none. |
| "I remember what happened — no need to write it down" | Memory degrades within 48 hours. Root cause narratives shift without documentation. |
| "Solo developers don't need postmortems" | Client accountability and personal learning both require structured records. |
| "I'll write it later when things calm down" | Postmortem accuracy drops sharply after 24-48 hours. Write while logs are fresh. |
| "The root cause is obvious — fix and move on" | Obvious causes miss systemic contributors. 5 Whys reveals what quick fixes hide. |
| "I already fixed it — action items are unnecessary" | Fixes without follow-up items repeat. Action items create accountability. |
| "This happened before — no need to document again" | Repeat incidents signal systemic failure. Each recurrence needs its own record to track patterns. |

## Arguments

| Flag | Description |
|---|---|
| `--draft` | Interactive mode — asks questions and builds postmortem step by step (default) |
| `--template` | Output a blank postmortem template without asking questions |
| `--client` | Append a sanitized client-facing incident summary (no internal details) |
| `--format <markdown\|html>` | Output format. Default `markdown`. With `html`, writes a self-contained HTML report to `claudedocs/`. See [html-output.md](../references/html-output.md) |

## Dynamic Context

Before starting, gather incident evidence:

```bash
# Recent deployments to correlate with incident timeline
git log --oneline --since="3 days ago"

# Any recent tag or release
git describe --tags --abbrev=0 2>/dev/null || echo "(no tags)"
```

## Workflow (--draft mode)

**Step 1 — Gather basics**
Ask: service name, incident start time, end time, how detected (alert / user report / developer discovery), who responded.

**Step 2 — Reconstruct timeline**
Build a chronological event log with timestamps (detection → investigation → root cause identified → fix deployed → resolved).

**Step 3 — Assess impact**
Affected users (count or %), duration in minutes, severity (SEV1/SEV2/SEV3), SLA breach, revenue impact if known.

**Step 4 — Root cause analysis**
Apply 5 Whys. Identify the primary root cause and contributing factors separately.

**Step 5 — Actions taken during incident**
List mitigation steps taken in real time (rollback, hotfix, manual data correction).

**Step 6 — Prevention action items**
Generate specific, assignable items with deadlines. Not "improve monitoring" — "Add DB connection pool alert by YYYY-MM-DD".

**Step 7 — Lessons learned**
What went well, what failed, what was surprising.

**Step 8 — Client report (if --client)**
Generate sanitized summary: user impact + resolution + prevention steps. No internal names, stack traces, or architecture details.

## Severity Classification

| Level | Definition | Example |
|---|---|---|
| **SEV1** | Complete outage, data loss, or security breach | Payment service down |
| **SEV2** | Major feature unavailable or >10% user degradation | Login fails for subset of users |
| **SEV3** | Minor feature degraded, workaround available | Export button broken |

## Output Format

Produces one or two Markdown documents:
1. **Internal postmortem** — Full technical document (always generated)
2. **Client report** — Sanitized summary (only with `--client`)

See [references/postmortem-template.md](references/postmortem-template.md) for the full internal template.
See [references/client-report-template.md](references/client-report-template.md) for the sanitized client template.

> **HTML mode (`--format html`)** — writes the postmortem as a self-contained HTML report instead of Markdown: a color-coded severity banner, a collapsible event timeline, and a `Copy as Markdown` button. Structure and conventions follow [html-output.md](../references/html-output.md). When `--client` is also set, the sanitized client report is produced as a separate HTML file. The Markdown surface is preserved inside each file, so downstream integration is unaffected.

## Integration

- **After `ywc-security-audit`**: If audit reveals an active exploit or breach, use this skill to write the postmortem.
- **Before `ywc-changelog-release-notes`**: Incident action items may drive a patch release; key fixes feed into the next changelog.
- Not part of the standard development pipeline — activates reactively after incidents occur.

## Common Mistakes

| Mistake | Better approach |
|---|---|
| Writing "human error" as root cause | Human error is a symptom. Ask why the system allowed the error to cause impact. |
| Action items without deadline or owner | Every item needs an assignee and target date. "Fix monitoring" → "Add DB alert by YYYY-MM-DD" |
| Writing postmortem days later from memory | Write within 24-48 hours while logs and chat history are available. |
| Skipping impact quantification | Always quantify: number of users, duration, revenue or SLA impact if known. |
| Client report exposing internal details | Describe user impact and resolution only — no stack traces, service names, or architecture. |
