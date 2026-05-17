---
name: ywc-gen-testcase
version: 1.0.0
description: (ywc) Use when generating a manual verification testsheet (developer + QA gate) from a PR, task directory, git range, or diff. Triggers: "generate test case", "testsheet", "QA checklist", "PR 테스트 케이스", "테스트시트", "テストシート作って", "manual test", "release 범위 test", "수기 검증". Do not use for writing automated unit/integration tests, code-level test generation, or in-IDE test scaffolding.
category: review
phase: quality
requires: []
advisor_budget: 2
---

# Generate Testsheet

**Announce at start:** "I'm using the ywc-gen-testcase skill to produce a dual-audience (developer + QA) testsheet."

Produce a **dual-audience** testsheet (markdown with checkboxes) from one of three inputs — a GitHub PR, an implemented task directory, or the current git diff. The testsheet cleanly separates what the **developer** does (DB queries, curl contracts, container logs) from what a **QA/PM/Product Owner** does in a browser, so both gates — pre-merge and pre-release — can be signed off independently and in parallel.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Two input modes given, pick the more specific one silently" | Stop and ask. Inputs cover different scopes (a PR vs a diff). Wrong choice produces a testsheet with mismatched scope. |
| "Developer test cases are obvious, focus on QA cases" | Both audiences need explicit cases. Pre-merge gate (dev) and pre-release gate (QA) must be parallel-signable. |
| "Mix dev curl checks into the QA section for completeness" | Each audience must own its section. Cross-contamination breaks parallel sign-off. |
| "Testsheet output without prerequisites/setup is fine" | Prerequisites (env, credentials, DB state) must be explicit. A testsheet that cannot be started is not a testsheet. |
| "Negative test cases (failure paths) are out of scope" | Always include critical negative cases. Happy-path-only testsheets miss most regressions. |
| "Browser-dependent steps belong in dev section" | UI verification belongs to QA. Dev section stays in terminal/curl/DB. |
| "Expected: 'the feature works correctly' is clear enough" | Weak criteria require constant clarification. Expected must name concrete values: status codes, row counts, UI text, exact error messages. |

**Violating the letter of these rules is violating the spirit.** A testsheet that mixes audiences is sign-off theater.

## Inputs

Exactly one input mode must resolve. If more than one is given, stop and ask — they cover different scopes (a PR spans many commits; a diff spans only the current working tree), and silently picking one would produce a testsheet whose title, scope, and sign-off surface do not match the user's intent.

| Input mode | How to specify | Primary source |
|---|---|---|
| **PR** | PR URL or PR number | `gh pr view`, `gh pr diff` |
| **Task** | Task name or `<phase>-<sequence>` prefix | `<tasks-dir>/<task>/task.md` + `README.md` |
| **Range** | Positional `<start>..<end>` (SHA / tag / branch / `HEAD~N`) or `--range <spec>` | `git log`, `git diff <start>..<end>` |
| **Diff** | `--from-diff` flag | Current `git diff HEAD` |

If no input is resolvable, stop and ask. Do not guess.

## Arguments

Parse `$ARGUMENTS`.

| Parameter | Format | Example | Description |
|---|---|---|---|
| PR identifier | URL or number | `250` | Fetches PR metadata + diff via `gh` |
| Task specifier | name or prefix | `000001-010` | Prefix match against `<tasks-dir>` |
| `--from-diff` | flag | | Use `git diff HEAD` |
| `--range <spec>` | `<start>..<end>` | `--range v1.2..v1.3` | Explicit range form (equivalent to positional `A..B`). Two-dot only — three-dot `A...B` is rejected |
| `--output-dir <path>` | path | `--output-dir ./docs/qa` | Override `docs/test-case/` |
| `--lang <code>` | `ja`,`ko`,`en` | `--lang ja` | Prose language. Default: auto-detect |
| `--filename <name>` | string | `--filename release-smoke` | Override derived filename (no `.md`) |
| `--tasks-dir <path>` | path | `--tasks-dir ./docs/tasks` | Tasks directory (Task input only) |
| `--include-regression` | flag | | Add Regression section (B side) |
| `--audience <who>` | `dev`\|`qa`\|`both` | `--audience qa` | Generate only one audience. Default: `both` (single file, A+B sections) |
| `--split` | flag | | Force physical split into `<slug>-dev.md` + `<slug>-qa.md`. Mutually exclusive with `--force-single` |
| `--force-single` | flag | | Bypass the L-tier split suggestion and always produce one file |
| `--no-toc` | flag | | Suppress TOC auto-insertion for M/L tier |
| `--dry-run` | flag | | Show plan (tier, filenames, section counts) without writing |
| `--format` | `markdown`\|`html` | `--format html` | Output format. Default `markdown`. With `html`, writes an interactive HTML testsheet (see Step 5). |

**Flag conflicts**: `--split` and `--force-single` cannot coexist — stop and ask. `--audience dev|qa` implies a single-audience file; `--split` in that combination is redundant and is silently ignored. **Range input** is mutually exclusive with PR, Task, and `--from-diff` — stop and ask if more than one is given. Range accepts only the two-dot `A..B` form; three-dot `A...B` is rejected because its merge-base semantics silently change scope and surprise the tester.

## Context

- Repository: !`gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null || echo "not a gh repo"`
- Current branch: !`git branch --show-current`
- Changed files (diff mode reference): !`git status --short`
- Default output directory: `docs/test-case/`

## Pre-flight

1. **Inside a repository** — `git rev-parse --show-toplevel` must succeed; run subsequent commands from the repo root.
2. **`gh` CLI authenticated** (PR input only) — `gh auth status` must succeed.
3. **Output directory writable** — `mkdir -p <output-dir>` must succeed.
4. **Exactly one input mode resolved** — if more than one input is present, stop and ask.
5. **Flag conflicts** — see Arguments note above.

## Step 1: Input Resolution

### 1a. PR input

```bash
gh pr view <N> --json number,title,body,author,headRefName,baseRefName,url,files,commits,labels
gh pr diff <N>
```

Capture PR URL, title, body, author, head/base branches, labels, changed files, commit messages. Lift any explicit "How to test" / "Acceptance Criteria" / "動作確認" block from the PR body into scenario goals verbatim.

### 1b. Task input

- Resolve the task directory via prefix match. Prefer `<tasks-dir>/completed/<name>/` over `<tasks-dir>/<name>/` — a testsheet after merge is the common case.
- Read `task.md` (Implementation Steps, Acceptance Criteria, Verify commands) and `README.md` in full.

### 1c. Diff input

- `git diff HEAD` plus `git log <base>..HEAD --oneline` (auto-detect `<base>`: `develop` > `main` > `master`). Stop on empty diff.

### 1d. Range input

Positional `<start>..<end>` or `--range <spec>`. Each endpoint accepts SHA, tag, branch, or a relative ref like `HEAD~5`. Reject the three-dot form `A...B` explicitly.

Collect:

- `git rev-parse <start>` and `git rev-parse <end>` — fail fast on unknown refs
- `git log --oneline <start>..<end>` — commit list (used as scenario source)
- `git diff <start>..<end>` — the change set (used for surface classification)
- Stop immediately on an empty range

### 1e. Range quality checks (range input only)

Range mode lacks PR body / Task Acceptance Criteria, so scenario quality is sensitive to commit-message hygiene and scope size. Three protective checks run before Step 2 to prevent low-quality testsheets from being generated silently:

1. **PR auto-suggest** — run `gh pr list --search <head-sha> --state all --json number,title,commits` on the range's HEAD commit. If an open or merged PR exists and its commit set covers ≥ 80% of the range, stop and ask:

   ```text
   Range HEAD is part of PR #<NNN> "<title>" (covers N of M commits).
   PR mode provides PR body, labels, and explicit "How to test" context —
   scenario quality is meaningfully better.

       [a] Switch to PR #<NNN> mode (recommended)
       [b] Keep range mode (PR metadata will be ignored)
   ```

2. **Commit-message quality** — if ≥ 70% of commit headlines in the range are ≤ 10 characters (e.g. `wip`, `fix`, `tmp`, `update`), warn and ask whether to proceed. Low-signal headlines force scenario generation to rely on diff inference alone, which is materially weaker than structured acceptance criteria.

3. **Range size guard** — if the range contains > 50 commits, escalate directly to L-tier handling in Step 4 regardless of scenario count. Review burden grows with commit lineage length, not just with scenario count.

## Step 2: Audience and Surface Classification

Every scenario carries **two** tags: **audience** (who runs it) and **surface** (what it verifies). Classifying on both axes is what makes the final testsheet useful to different readers.

### 2a. Audience tagging

| Audience | Who | Tools | Gate |
|---|---|---|---|
| **A. Developer** | Backend / DB / DevOps engineer | `psql`, `gh`, `curl`, `docker`, `kubectl`, unit/integration test runners | **Pre-merge** — contracts, migrations, worker runners, container orchestration |
| **B. QA / Browser** | QA, PM, Product Owner, designer | Chrome + DevTools, admin UI, test HTML origin, mobile device/emulator | **Pre-release** — end-user experience and any browser-observable effect |

Scenarios that require both (e.g. "SDK loader works end-to-end") belong to **B**, with the data setup moved into A's Prerequisites. This prevents duplicate work.

### 2b. Surface classification

| Surface | File patterns (typical) | Scenarios produced | Typical audience |
|---|---|---|---|
| UI / Browser | `*.tsx`,`*.vue`,`*.svelte`,`app/**`,`pages/**`,`components/**`,`*.css`,`*.html` | Route/screen walkthrough, form validation, empty/loading/error states | B |
| Database / Table | `migrations/**`,`*.sql`,`prisma/schema.prisma`,`supabase/migrations/**` | Row visibility, constraint enforcement, index presence, rollback safety | A |
| API | `app/api/**`,`*.controller.*`,`**/route.ts`,`src/routes/**`,`api/**/*.py` | Status codes, response shape, auth boundary, validation errors | A primarily; B when endpoint is browser-consumed |
| Background job / Webhook | `workers/**`,`jobs/**`,`webhook*`,`cron*`,`*.worker.ts` | Trigger condition, retry, idempotency | A |
| Configuration | `*.env*`,`*.yaml`,`*.toml`,`Dockerfile`,`docker-compose*`,`.github/workflows/**` | Env presence, build/runtime, CI green | A |
| Docs only | `*.md`,`docs/**` | Docs review checklist | A or B depending on audience of the doc |

**Do not fabricate surfaces that do not exist in the diff.** An empty section tells the tester nothing and dilutes the real work.

### 2c. Browser-observable effects (even in backend-only PRs)

File-pattern matching alone is not sufficient to decide the B section. A backend-only PR can still have browser-observable effects that only a real browser can verify — curl cannot reliably reproduce CORS preflight, cookie partitioning, `<script>` tag loading, `Content-Type` sniffing, or downstream dashboard behaviour.

**Include a B (QA/Browser) section even when no frontend files changed, if any of the following are true:**

| Browser-observable effect | B-section scenario to include |
|---|---|
| Public endpoint consumed by a browser (`/config/:id`, SDK loader, webhook receiver) | "Fetch from DevTools Console" scenario |
| CORS / preflight behaviour changed | Preflight-from-real-browser scenario (curl does not fully simulate preflight) |
| `Content-Type` / CSP / cookie attributes changed | DevTools Network tab verification |
| Backend APIs consumed by an **existing unchanged** frontend in the same repo | Consumer-renders-successfully scenario (regression-style) |
| Script/asset delivered to end-user browsers (SDK, embed, widget) | "Load from test HTML page" scenario |

The test for whether to include a B section is not "did a `.tsx` file change" but **"can a human verify this change by opening a browser?"** When in doubt, include a minimal B section of 1–2 scenarios rather than omit it — a missing B section on a release that touches public endpoints is a common source of production surprises.

## Step 3: Scenario Generation

For each (audience, surface) pair that exists, generate 2–5 scenarios. A scenario is one testable behaviour, not one changed file.

Each scenario has:

- **Goal** — one sentence
- **Preconditions** — state the app must be in
- **Steps** — numbered, imperative, specific enough for a tester who did not write the code
- **Expected** — concrete values (`expect 3 rows with status = 'active'`), not "it should work"
- **Checkbox** — one `- [ ]` at the top

**Anti-pattern**: `- [ ] Test that the feature works`. That is not a scenario. If you cannot state *what to run/click and what to see*, the scenario is not ready.

Scenario sources, in priority order:

1. PR body / task Acceptance Criteria ("How to test", "動作確認", "Reviewer should verify")
2. Commit messages
3. Surface-driven scenarios (from 2b)
4. Diff edge cases (new `NOT NULL` → null-input scenario; new permission check → unauthorised-role scenario)

## Step 4: Tier Decision

Count scenarios after Step 3. Use the count to choose layout. This protects testsheets from becoming unread 1000-line walls.

| Tier | Scenarios | Layout |
|---|---|---|
| **S** | ≤ 20 | Single file, A+B sections, **no TOC**, **no collapsible details** |
| **M** | 21–40 | Single file, A+B sections, **auto-TOC** at top, **`<details>` collapsible** for Prerequisites + Edge Cases |
| **L** | > 40 scenarios **OR** range > 50 commits | **Ask user** before writing:<br>1. Single file with TOC + collapsible (as M)<br>2. `--split` into `<slug>-dev.md` + `<slug>-qa.md`<br>3. Split by Phase / feature (user names each file)<br>Proceed only after the user chooses. `--force-single` bypasses the prompt. |

Explicit flags override the tier default:

- `--split` → physical split, regardless of tier
- `--audience dev|qa` → single-audience file, skip the other section entirely
- `--force-single` → one file even if count > 40
- `--no-toc` → suppress TOC even in M/L

## Step 5: Write the Testsheet

### Output format

Default is a Markdown testsheet (`.md`) — keep this for the existing `-v<N>`
append and front-matter sign-off workflow. With `--format html`, write an
**interactive HTML testsheet** instead, following
[html-output.md](../references/html-output.md): each scenario checkbox is
clickable, sign-off state (tester name, Pass/Fail/Blocked, notes) persists in
the browser via `localStorage`. The embedded Markdown block is the original
testsheet template (identical to `--format markdown` output). The `Copy as
Markdown` button assembles the *current* state on the fly — original content
with sign-off annotations drawn from `localStorage` — so the exported Markdown
reflects the reviewer's completed work and can be pasted into a PR or
committed. HTML mode is recommended when the testsheet will be handed to a
QA/PM who signs off in a browser; the filename follows the Default filename
table below with an `.html` extension.

### Default filename

| Input | Single file (default) | `--split` mode |
|---|---|---|
| PR | `pr-<number>-<slug>.md` | `pr-<number>-<slug>-dev.md` + `...-qa.md` |
| Task | `task-<phase>-<sequence>-<slug>.md` | `...-dev.md` + `...-qa.md` |
| Range | `range-<short-start>-<short-end>-<slug>.md` (tag names used verbatim when both endpoints are tags, e.g. `range-v1.2-v1.3-<slug>.md`) | `...-dev.md` + `...-qa.md` |
| Diff | `<yyyymmdd-HHMM>-<branch-slug>.md` | `...-dev.md` + `...-qa.md` |

If the target file already exists, append `-v<N>` (never overwrite). Existing files may carry a tester's partial sign-off.

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

## Step 6: Validate and Report

Before finishing:

1. File(s) exist and non-empty.
2. Checkbox count ≥ 3.
3. Every scenario has a concrete **Expected** result.
4. If M/L tier and `--no-toc` not set, TOC present at the top with anchors matching headings.
5. If split layout, cross-reference line present in each file.

Report:

```text
Testsheet generated: <absolute path(s)>
Source: <pr#N | task:<name> | diff>
Tier: <S | M | L>
Layout: <single | split>
Audiences: <A only | B only | A+B>
Scenarios by surface: UI (3), DB (1), API (2), Jobs (4), Config (2)
Scenarios by audience: Dev <n>, QA <m>
Total: <scenarios> scenarios, <checkboxes> checkboxes
Language: <detected-or-specified>
Next steps:
  - Dev signs off on Section A (pre-merge gate)
  - QA signs off on Section B (pre-release gate)
  - Update front-matter `dev_status:` / `qa_status:` as work progresses
```

## Language Detection

When `--lang` is not specified, choose in this order. A testsheet is read by humans, so match the language humans speak on this project — not the language the code is written in.

1. **CLAUDE.md / AGENTS.md** — directives such as `UI/User-facing text: Japanese`, `Documentation: Korean`, `PR言語` → the strongest signal.
2. **Recent testsheets in the output directory** — match dominant prose language.
3. **Project `README.md`** — language of the root README.
4. **Fallback** — English.

YAML front matter keys, section numbers, and the template skeleton stay in English regardless of `--lang`. Only prose (Summary, Goal, Steps, Expected, Notes, Edge Cases) follows the chosen language.

## Dry Run Mode

With `--dry-run`, perform Steps 1–4 as usual, then print:

- Resolved input mode and source
- Tier decision (S/M/L) and scenario count
- Target filename(s) and full output path(s)
- Surface classification (which sections will exist)
- Scenarios per (audience, surface) pair
- Detected language

Do **not** write any file. Exit after printing.

## Error Handling

| Situation | Behaviour |
|---|---|
| No input given | Stop, ask for PR / task / range / `--from-diff` |
| Multiple inputs given (PR + Range, Task + Range, Range + `--from-diff`, etc.) | Stop, ask which mode |
| Three-dot range `A...B` passed | Reject and ask for the two-dot `A..B` form instead |
| Range ref invalid (`git rev-parse` fails on `<start>` or `<end>`) | Report which ref failed; stop |
| Range empty (`<end>` has no commits absent from `<start>`) | Report "range is empty"; stop |
| Range > 50 commits | Escalate to L-tier handling (ask user how to proceed) |
| Range HEAD belongs to an open/merged PR (≥ 80% overlap) | Stop and ask whether to switch to PR mode |
| Range has ≥ 70% low-quality commit headlines | Warn and ask whether to proceed |
| `--split` and `--force-single` both set | Stop, ask which is intended |
| `gh` not authenticated (PR input or range PR auto-suggest) | Ask user to run `gh auth login`; stop |
| PR not found | Report the PR number and stop |
| Task not found | List similar tasks (fuzzy match) and stop |
| Empty diff (diff input) | Report "nothing to test" and stop |
| Output directory not writable | Report failing path and stop (no silent fallback) |
| Target file already exists | Append `-v<N>` suffix; report new filename |
| L tier detected and no explicit `--split`/`--force-single` | Ask user how to proceed before writing |

## Integration

Downstream of the implementation-oriented `ywc` skills:

- **ywc-sequential-executor** — generates the PR/Task this skill tests
- **ywc-parallel-executor** — same, for parallel execution
- **ywc-merge-dependabot** — merged dependency bumps that often warrant a smoke testsheet

Invoke this skill after those finish, when a human tester is ready to validate.

## Examples

### Example 1: PR URL, default (single file, A+B)

```text
/ywc-gen-testcase https://github.com/legalforce/cas-marketing-on/pull/250
```

### Example 2: Force physical split (two files)

```text
/ywc-gen-testcase 250 --split --lang ja
```

### Example 3: QA-only testsheet (to hand to QA team)

```text
/ywc-gen-testcase 250 --audience qa --lang ja
```

### Example 4: Force single file even if L tier

```text
/ywc-gen-testcase 250 --force-single
```

### Example 5: Task-based with regression

```text
/ywc-gen-testcase 000001-010-db-create-users-table --include-regression
```

### Example 6: Current diff, custom filename

```text
/ywc-gen-testcase --from-diff --filename smoke-before-release
```

### Example 7: Range between two tags

```text
/ywc-gen-testcase v1.2..v1.3
```

Generates `range-v1.2-v1.3-<slug>.md`. Auto-suggest will propose PR mode if the HEAD of the range is in a PR.

### Example 8: Pre-PR local range

```text
/ywc-gen-testcase HEAD~5..HEAD --lang ja
```

Useful when you have local commits that are not yet pushed or PR'd and want a testsheet for review.

### Example 9: Explicit `--range` flag form

```text
/ywc-gen-testcase --range abc1234..def5678
```

### Example 10: Dry-run to preview tier decision

```text
/ywc-gen-testcase 250 --dry-run
```
