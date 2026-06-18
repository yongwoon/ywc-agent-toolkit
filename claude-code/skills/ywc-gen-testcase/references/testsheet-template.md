# Testsheet Template and Length-Management Rules

Full single-file and split-file testsheet templates plus length-management
guidelines, extracted from `SKILL.md` Step 5. The generation flow references
this file when writing the output testsheet.

### Single-file template (default, A+B)

Write `<output-dir>/<filename>.md` using this skeleton. Keep front matter keys in English regardless of `--lang`; they are a machine surface. M/L tier inserts a TOC block and wraps Prerequisites/Edge Cases in `<details>`; S tier skips both.

````markdown
---
source: <pr#N | task:<name> | diff | range>
pr_url: <url or "">
range_spec: <e.g. "main..feature-x" or "">
range_start: <short SHA or tag, or "">
range_end: <short SHA or tag, or "">
branch: <head branch, or "" for ranges crossing branches>
base_branch: <base>
author: <username>
generated_at: <ISO 8601>
tier: <S | M | L>
dev_tester: ""
dev_status: pending
qa_tester: ""
qa_status: pending
---

# Test Case: <Title>

<!-- TOC block: M/L tier only -->
## Table of Contents
- [1. Summary](#1-summary)
- [2. Prerequisites](#2-prerequisites)
- [A. Developer Verification](#a-developer-verification)
  - [A.1 Database](#a1-database--table)
  - [A.2 API](#a2-api)
  - [A.3 Background Jobs](#a3-background-jobs--workers)
  - [A.4 Configuration](#a4-configuration)
  - [A.5 Dev Edge Cases](#a5-dev-edge-cases)
  - [A.6 Dev Sign-off](#a6-dev-sign-off)
- [B. QA / Browser Verification](#b-qa--browser-verification)
  - [B.1 UI / Browser Scenarios](#b1-ui--browser-scenarios)
  - [B.2 User-visible Edge Cases](#b2-user-visible-edge-cases)
  - [B.3 Regression](#b3-regression)
  - [B.4 QA Sign-off](#b4-qa-sign-off)

## 1. Summary

<2–4 sentences explaining what changed and why a human needs to verify it.>

## 2. Prerequisites

<!-- M/L tier: wrap in <details> tag, open by default -->

### 2.0 Common (both audiences)
- [ ] …

### 2.A Dev-only
- [ ] …

### 2.B QA-only
- [ ] …

## A. Developer Verification

> **Audience**: Backend / DB / DevOps engineer  
> **Tools**: psql, gh, curl, docker  
> **Gate**: pre-merge

### A.1 Database / Table
<only if surface exists>

#### A.1.1 <scenario name>
- [ ] **Goal**: …
- **Preconditions**: …
- **Steps**:
  1. …
- **Expected**: …

### A.2 API
### A.3 Background Jobs / Workers
### A.4 Configuration
### A.5 Dev Edge Cases

<!-- M/L tier: wrap A.5 in <details> -->

- [ ] <boundary / null / error path>

### A.6 Dev Sign-off
- **Tester**:
- **Date**:
- **Result**: ☐ Pass ☐ Fail ☐ Blocked
- **Notes**:

## B. QA / Browser Verification

> **Audience**: QA / PM / Product Owner / Designer  
> **Tools**: Chrome + DevTools, admin UI, test origin  
> **Gate**: pre-release

### B.1 UI / Browser Scenarios
<only if a browser-observable surface exists>

### B.2 User-visible Edge Cases

<!-- M/L tier: wrap in <details> -->

### B.3 Regression
<only if --include-regression>

### B.4 QA Sign-off
- **Tester**:
- **Date**:
- **Result**: ☐ Pass ☐ Fail ☐ Blocked
- **Notes**:

## Appendix
<optional — long SQL, payload samples, troubleshooting>
````

### Split-file variants (`--split` or `--audience`)

Each file contains only that audience's Summary, Prerequisites, Scenarios, and Sign-off. Add a **Cross-reference** line at the bottom pointing to the counterpart (`Developer sheet: ./<slug>-dev.md`, `QA sheet: ./<slug>-qa.md`). Omit cross-reference when `--audience` was explicit and only one file is produced.

## Length Management Guidelines

Apply these regardless of tier to keep testsheets lean:

1. **Prerequisites common-prefix + audience-suffix** — shared rows live once in `## 2.0 Common`; dev-only / qa-only rows live in `## 2.A` / `## 2.B`. Never duplicate.
2. **Extract long verification material** — any SQL / script > 20 lines lives in `scripts/qa/*.sql` (or similar) and the scenario references the path only. The scenario body stays short.
3. **Regression by reference** — instead of repeating known-good regression flows, link to prior testsheets (e.g. `[Stripe release testsheet](./pr-230-stripe-release.md)`).
4. **Appendix at the bottom** — overflow content (detailed troubleshooting, sample payloads) goes under `## Appendix` and is linked from the relevant scenario.

Applied consistently, these four rules keep most M-tier testsheets under ~800 lines and prevent L-tier by shifting volume out of the main flow.
