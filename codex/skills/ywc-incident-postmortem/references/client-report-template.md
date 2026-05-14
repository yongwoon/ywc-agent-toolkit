# Client-Facing Incident Report Template

Rules for this document:
- Write in plain language — no internal system names, stack traces, or architecture details
- Focus on user impact and the steps taken to restore service
- Keep technical explanation minimal — describe what users experienced, not what broke internally
- Always include what is being done to prevent recurrence

---

## Service Incident Report

**Date**: YYYY-MM-DD
**Time of impact**: HH:MM – HH:MM [timezone]
**Affected service**: [User-visible service name — e.g., "Login", "Payment Processing", "File Export"]
**Severity**: [High / Medium / Low — use user-impact language, not internal SEV levels]

---

### What happened

[Plain language description of what users experienced.

Example: "Users attempting to log in to [Service] between 14:30 and 16:15 KST encountered
an error message and were unable to access their accounts."]

---

### Impact

[Quantify user impact without revealing internal architecture.

Example: "Login attempts during this period were unsuccessful for a portion of our users.
Existing logged-in sessions were not affected."]

---

### What we did

[High-level resolution steps — describe actions, not internal systems.

Example:
1. Our team was alerted at 14:35 and began investigating immediately.
2. We identified the cause at 15:10 and deployed a fix at 16:00.
3. Service was fully restored and confirmed stable at 16:15.]

---

### What we are doing to prevent recurrence

[1-3 plain-language prevention measures.

Example:
- We are adding automated monitoring to detect this class of issue before users are affected.
- We are reviewing our deployment process to catch similar issues in staging before they reach production.
- We will conduct an internal review and share findings with the team by [date].]

---

### Our apology

We sincerely apologize for the disruption this caused to your work.
Reliability is a core commitment, and we take incidents like this seriously.

[Optional: If there is an SLA credit or compensation, describe it here.]

If you have questions, please contact us at [support contact].

---

*Report prepared by: [Name / Team]*
*Report date: YYYY-MM-DD*
*Internal reference: INC-[ID] (do not include in external-facing copy)*
