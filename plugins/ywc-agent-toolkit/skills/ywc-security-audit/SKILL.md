---
name: ywc-security-audit
description: >-
  (ywc) Use when reviewing authentication/authorization code, external-facing endpoints, code handling sensitive data, or for periodic security reviews. Triggers: "보안 점검", "security audit", "보안 감사", "OWASP", "취약점 분석", "보안 리뷰", "security check", "is this code secure", "セキュリティ監査". Do not use for general code review (use ywc-impl-review), product-level risk review (use ywc-product-review), or for code that does not touch auth/external input/sensitive data.
---

# ywc-security-audit

**Announce at start:** "I'm using the ywc-security-audit skill to inspect the code against OWASP Top 10 and project-specific threats."

Security Agent Skill for deep security analysis.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Code looks clean, OWASP scan is overkill" | Clean code can still leak. Walk OWASP Top 10 in order — every item, every time. |
| "This is internal-only, threat surface is low" | Internal-only ≠ trusted. Insider threat and lateral movement are real. Audit anyway. |
| "Auth library is well-known, trust it blindly" | Misuse of a good library is the #1 cause of auth bugs. Audit how it is configured. |
| "Severity feels High, mark it Critical to be safe" | Inflated severity wastes triage time. Use Critical only when exploit + impact are both demonstrable. |
| "User input is validated upstream, no need at this layer" | Defense in depth. Validate at every trust boundary, not just at the gateway. |
| "Token/secret/key is just for dev, exposure is fine" | Never. Dev secrets get committed, leak, and become prod credentials. Always flag. |
| "I cannot exploit it locally, finding is theoretical" | Theoretical findings still belong in the report. Mark as `unverified — theoretical` rather than dropping. |
| "OWASP scan is too fine-grained to parallelize" | Grouping into 3 domain clusters lets each worker focus deeply on 3-4 items; it also prevents cross-category contamination that degrades severity classification in a monolithic pass. |

**Violating the letter of these rules is violating the spirit.** A clean security report without honest dimensional coverage is dangerous.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--code` | `--code <path>` | `--code api/src/middleware/` | Code path to audit (required) |
| `--format` | `--format markdown\|html` | `--format html` | Output format. Default `markdown`. With `html`, writes a self-contained HTML report to `claudedocs/`. See [html-output.md](../references/html-output.md) |

## Execution Steps

1. **Collect Project Context** — Read `AGENTS.md`, `CODEX.md`, `package.json`, and equivalent project metadata where present to identify tech stack. Pay special attention to authentication method, deployment environment (internal/external), and security libraries in use
2. **Read Target Code Files** — Read all source files under the `--code` path
3. **Phase 1 — Parallel OWASP Analysis** — Use Codex subagent delegation when the current session exposes a delegation tool to run 3 workers in parallel. If no delegation tool is available, run the same three analysis slices inline and record the fallback in the report. Each slice covers a grouped subset of OWASP Top 10. For each item in its slice, the worker must: Grep/AST search for patterns, trace data flow (input → processing → output), and apply project context. Do not use Claude Code-only `Task(...)` fields, `subagent_type`, `tools`, or explicit Claude model pins in the Codex bundle.

   | Worker | Scope | OWASP Items |
   |---|---|---|
   | Auth & Data | Authentication and persistence | A01 Injection · A02 Broken Auth · A03 Sensitive Data Exposure |
   | Web Layer | Request/response and LLM prompt surfaces | A04 XSS · A05 Broken Access Control · A06 Security Misconfiguration · **PI Prompt Injection** (LLM-driven surfaces only — user-controlled string → prompt sink; see `references/prompt-injection-checklist.md`) |
   | Infra & Input | Network, validation, and abuse controls | A07 SSRF · A08 Input Validation · A09 Rate Limiting · A10 Timing Attacks |

   **Prompt-Injection slice (Web Layer sub-category)** — when the audit target includes an LLM-driven surface (agent / chatbot / prompt-template system / function-calling pipeline), the Web Layer worker additionally walks the four items in [`references/prompt-injection-checklist.md`](./references/prompt-injection-checklist.md): user-controlled string flowing directly into a prompt, system/user role separation, canary-token + ML-classifier defense, and external-tool / RAG-result sanitization. The checklist defines default severity and conditions for adjustment. Findings surface under the standard severity rubric below and are reported alongside the OWASP A04-A06 items in the Web Layer worker's output.

   Each worker classifies its findings:
   - **Critical**: Immediately exploitable (SQL injection, auth bypass, hardcoded secrets)
   - **High**: Conditionally exploitable (SSRF with internal network access, improper auth checks)
   - **Medium**: Potential risk (verbose errors, insufficient rate limiting)
   - **Low**: Best practice violation (timing attack potential, unnecessary information disclosure)

   Each worker returns:
   - **Confirmed findings** — severity, file:line, issue, risk, recommended fix
   - **Advisor candidates** — findings meeting the Advisor Escalation Policy conditions below (suspect code chain + hypothesized exploit, ≤100 lines each)

4. **Aggregate Phase 1 Results** — Combine findings from all 3 workers. Deduplicate by `{file}:{line}`. Cap advisor candidates at `advisor_budget` (default: 3), prioritizing Critical > High. Log any dropped candidates in the report.

5. **Phase 2 — Advisor Pass** — For each surviving advisor candidate, follow the **Advisor Escalation Policy** section below. When Codex custom-agent delegation is available, request one bounded `ywc-security-engineer` read-only advisor pass for OWASP/security verdict review. Send only trust boundaries, authn/authz flows, external inputs, suspected risks, and the relevant excerpt (≤100 lines), and expect `Status: <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>` plus confirmed/adjusted severity. If no delegation tool is available, run the same advisor decision inline and record the fallback. Merge verdicts into the findings list.

6. **Output Severity-Classified Security Report**

## Audit Checklist (OWASP Top 10)

1. Injection (SQL, Command, LDAP)
2. Broken Authentication (Token, Session management)
3. Sensitive Data Exposure (Logging, API Response, Storage)
4. XSS (Reflected, Stored, DOM-based)
5. Broken Access Control (Missing Auth Middleware, Privilege Escalation)
6. Security Misconfiguration (Default Config, Verbose Errors)
7. SSRF (Unvalidated URLs, Internal Service Access)
8. Input Validation (Missing Validation, Type Coercion)
9. Rate Limiting (Missing Rate Limits on Sensitive Endpoints)
10. Timing Attacks (Non-constant-time Comparisons for Secrets)

### LLM-Driven Surface Addendum (run when target uses an LLM SDK)

11. Prompt Injection — user input → prompt sink, role separation, canary
    / classifier defenses, external-tool / RAG result sanitization
    (full audit items + severity table in
    [`references/prompt-injection-checklist.md`](./references/prompt-injection-checklist.md))

## Output Format

```text
## Security Audit Result: {target path}

### Summary
- Critical: N, High: M, Medium: K, Low: L

### Findings
1. [{severity}] {file}:{line}
   - Issue: ...
   - Risk: ...
   - Recommended Fix: ...

### Overall Assessment
(Comprehensive security posture summary)
```

> **HTML mode (`--format html`)** — emits the same findings as a self-contained HTML report: severity color coding, tab navigation, and a `Copy as Markdown` button. Structure and conventions follow [html-output.md](../references/html-output.md). The Markdown surface is preserved inside the file, so downstream integration is unaffected.

## Advisor Escalation Policy

This skill runs the full OWASP Top 10 deep analysis on a single inherited-model executor. Because security findings are the highest-stakes output category in this repository, the executor applies a **permissive** escalation bar: when a suspected Critical or High finding has indirect evidence, escalate rather than risk mislabeling. This follows **Pattern A** from [advisor-pattern.md](../references/advisor-pattern.md) — frontier judgment applied at the specific decision points where it carries real value.

**Budget**: up to 3 advisor escalations per invocation. Security gets a slightly larger budget than spec-review because the downside cost of a missed vulnerability is much higher than the downside cost of a missed spec gap. Unused budget is still good; the bar for escalation must still be met.

**Escalation conditions** — a finding is an advisor candidate when it matches any of the following:

1. **Indirect exploit chain** — A parameter flow could enable SSRF, auth bypass, or injection, but the exploit requires two or more hops through functions the executor did not fully trace. The key advisor question is whether the chain is actually reachable.
2. **Two OWASP categories compete** — The same evidence fits two categories equally (for example A01 Broken Access Control and A07 Auth Failures). The correct category affects severity and remediation, so the choice is irreversible once reported.
3. **Business logic flaw (A04)** — A04 is the hardest category to judge mechanically because it depends on domain knowledge, not pattern matching. When a suspected business logic flaw has any ambiguity, escalate.
4. **Crypto decision (A02)** — The code makes a hashing or encryption choice and the executor cannot tell whether it is appropriate without knowing the threat model and data sensitivity. Frontier judgment with the spec excerpt is the right call.
5. **Critical severity with indirect evidence** — Any Critical-suspected finding where the unsafe path requires interpretation rather than direct observation. Direct means the unsafe call sits on a single visible line; indirect means the tainted value flows through multiple transformations before reaching the dangerous sink.

**Context payload rules** (critical for cost discipline):
- Forward only the decision point: the suspect code chain, the spec or threat-model excerpt, and 2-3 bullet points sketching the hypothesized exploit (≤100 lines total).
- Do NOT forward: the full audit target, the full project config, secrets, or the entire CLAUDE.md.
- The advisor returns a short verdict (≤200 words) containing confirmed severity, a one-line rationale, and either "confirmed" or "adjusted" with the new severity.
- Never include the full file, the full project config, or secrets. If the exploit chain needs information outside the snippet, summarize that information in 1-2 sentences rather than pasting it.

**Non-goals** — do NOT escalate for these:
- Trivial OWASP pattern matches — hardcoded secrets, raw string concatenation in SQL queries, unfiltered user strings assigned to innerHTML-style sinks. These are Critical and unambiguous; report them as Phase 1 confirmed findings.
- Missing standard hardening — no rate limit on an endpoint, missing security headers, absent CORS tightening. These are A05 misconfigurations with clear remediation.
- Low-severity best practice notes — timing attack potential, overly verbose error messages. Advisor adds no value at this severity.
- Well-understood vulnerable dependencies (A06) — a pinned CVE version is a mechanical finding.

Report escalations in the output: mark Phase 2 findings with `[P2]` prefix and include the advisor's verdict. This preserves auditability of which security calls involved frontier judgment and lets the user calibrate their trust in the severity assignments.

## Validation

Before returning the audit, verify that each finding cites a file/line or config source, maps to an OWASP category, includes severity rationale, redacts secrets from snippets, and records every advisor escalation as `[P2]` with budget usage.

## Integration

- **upstream**: After implementation or periodic review
- **downstream**: Fix implementation → PR
