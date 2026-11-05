# ywc-incident-postmortem

A skill for writing structured incident postmortems after a production incident.
Covers timeline reconstruction, root cause analysis (5 Whys), impact assessment,
prevention action items, and optionally a sanitized client-facing report.

## When to use

| Situation | Examples |
|-----------|---------|
| Service outage | DB connection failure, server down after deploy, CDN outage |
| Security incident | API key exposure, auth bypass, suspicious access |
| Data loss or corruption | Failed migration, accidental deletion |
| Payment errors | Double charge, payment failure loop |
| Sudden performance degradation | Response time spike after deployment |

## Usage

```
/ywc-incident-postmortem             # Interactive draft mode (default)
/ywc-incident-postmortem --template  # Output a blank template to fill in
/ywc-incident-postmortem --client    # Also generate a sanitized client-facing report
```

## Output

- **Internal Postmortem** — Full technical document: timeline, 5 Whys, action items
- **Client Report** (with `--client`) — User-impact summary with no internal details

## Related Skills

- `ywc-security-audit` — Proactive security auditing *before* incidents
- `ywc-impl-review` — General code quality review
- `ywc-changelog-release-notes` — Document changes after a patch release

## Analyst contract

`Caller: ywc-incident-postmortem` · `analysis_mode=incident_five_whys`

Set Caller and analysis_mode explicitly. Missing, unknown or mismatched pairs return `NEEDS_CONTEXT` without inference. Validate Status → Summary → Finding counts → Analysis mode; retain the original caller gate.

Return exactly five numbered Why steps with evidence at every step; separate primary root cause from contributing factors. Missing causal evidence returns `NEEDS_CONTEXT` rather than invented steps.

Live runtime: `UNVERIFIED — instruction contract only`.
