# Incident Postmortem Template

Copy this template and fill in each section within 24-48 hours of the incident.

---

## Incident: [Short descriptive title]

| Field | Value |
|---|---|
| **Date** | YYYY-MM-DD |
| **Severity** | SEV1 / SEV2 / SEV3 |
| **Duration** | HH:MM (from first user impact to full resolution) |
| **Detected by** | Monitoring alert / User report / Developer discovery |
| **Service affected** | [User-visible service or feature name] |
| **Author** | [Name] |
| **Status** | Resolved / Monitoring / Ongoing |

---

## Executive Summary

[3-5 sentences. What happened, which users were affected, how long, how resolved.
Write for a non-technical stakeholder.]

---

## Timeline

All times in [timezone]. Start from first sign of trouble, not when it was reported.

| Time | Event |
|---|---|
| HH:MM | [First symptom or anomaly] |
| HH:MM | Incident detected (how: alert / report / discovery) |
| HH:MM | Investigation started |
| HH:MM | Hypothesis: [what was suspected] |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied: [describe action] |
| HH:MM | Fix deployed |
| HH:MM | Service restored / user impact ended |
| HH:MM | All-clear confirmed |

---

## Impact

| Metric | Value |
|---|---|
| Users affected | [number or estimated percentage] |
| Duration of user impact | [minutes] |
| Revenue impact | [if applicable — or "N/A"] |
| SLA breached | Yes / No |
| Data loss | Yes / No / Unknown (describe if Yes) |

---

## Root Cause Analysis

### Primary Root Cause

[One to three sentences. Be specific: "A database migration script removed column X,
which the API still referenced at runtime" rather than "Database error".]

### 5 Whys

1. **Why** did users experience [symptom]? → [Answer]
2. **Why** did [answer to 1] happen? → [Answer]
3. **Why** did [answer to 2] happen? → [Answer]
4. **Why** did [answer to 3] happen? → [Answer]
5. **Why** did [answer to 4] happen? → [Systemic root cause]

### Contributing Factors

Conditions that made the incident worse or harder to detect:

- [e.g., No automated alert for DB schema drift]
- [e.g., Staging environment did not replicate production data volume]
- [e.g., Deploy and migration ran without rollback verification]

---

## Actions Taken During Incident

| Time | Action | Result |
|---|---|---|
| HH:MM | [Describe mitigation step] | [Outcome] |
| HH:MM | [Rollback / hotfix / manual intervention] | [Outcome] |

---

## Prevention Action Items

Each item must have an owner and a specific target date.
"Improve monitoring" is not acceptable — "Add alert for X condition by DATE" is.

| # | Action | Owner | Target Date | Status |
|---|---|---|---|---|
| 1 | [Specific, measurable action] | [Name] | YYYY-MM-DD | Open |
| 2 | [Specific, measurable action] | [Name] | YYYY-MM-DD | Open |
| 3 | [Specific, measurable action] | [Name] | YYYY-MM-DD | Open |

---

## Lessons Learned

### What went well
- [e.g., Alert fired within 2 minutes of impact]
- [e.g., Rollback procedure executed without data loss]

### What could be improved
- [e.g., Root cause identification took 45 minutes due to missing logs]
- [e.g., No runbook existed for this failure mode]

### What surprised us
- [e.g., The feature had zero monitoring despite being on the critical path]

---

## References

- [Link to incident logs / log query]
- [Link to monitoring dashboard snapshot]
- [Link to relevant PRs or commits]
- [Link to any related previous postmortem]
