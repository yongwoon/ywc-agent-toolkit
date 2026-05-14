# Gen Testcase Skill (ywc-gen-testcase)

This Codex Skill takes a GitHub PR, a completed task directory, or the current git diff and produces a **dual-audience checkbox-driven markdown testsheet**: Section A for developers (pre-merge gate) and Section B for QA/Browser (pre-release gate). The default output path is the project's `docs/test-case/` directory.

Backend engineers and QA/PM/Product Owner can each sign off on their own section independently and in parallel — so a merge decision and a release decision are cleanly separated.

## Usage

### Basic Usage

Generate a testsheet from a PR URL:

```text
/ywc-gen-testcase https://github.com/legalforce/cas-marketing-on/pull/250
```

Within the same repository, a PR number is sufficient:

```text
/ywc-gen-testcase 250
```

### Task-based generation

```text
/ywc-gen-testcase 000001-010-db-create-users-table
```

### Git Range generation

Generate from an arbitrary commit range. SHA, tag, branch name, and `HEAD~N` all work.

```text
/ywc-gen-testcase v1.2..v1.3
/ywc-gen-testcase HEAD~5..HEAD
/ywc-gen-testcase main..feature-x
/ywc-gen-testcase --range abc1234..def5678
```

> Range supports only the **two-dot `A..B`** form. Three-dot `A...B` is rejected because its merge-base semantics silently change scope.
> If the range HEAD is part of an open/merged PR (≥80% commit overlap), the Skill auto-suggests switching to PR mode — PR body / labels / Acceptance Criteria produce materially better scenarios.
> If commit-message quality is low (≥70% of headlines ≤10 characters), the Skill warns before proceeding.

### Diff-based generation

```text
/ywc-gen-testcase --from-diff
```

### Options

| Option | Description | Example |
| --- | --- | --- |
| `--output-dir <path>` | Override output directory (default: `docs/test-case/`) | `--output-dir ./qa/manual-tests` |
| `--lang <code>` | Testsheet language (`ja`, `ko`, `en`). Default: auto-detect | `--lang ja` |
| `--filename <name>` | Filename override (without `.md`) | `--filename release-v2-smoke` |
| `--tasks-dir <path>` | Tasks directory (default: `tasks/`) | `--tasks-dir ./docs/tasks` |
| `--include-regression` | Add a Regression section (B.3) | |
| `--audience <who>` | `dev` \| `qa` \| `both`. Default: `both` (single file, A+B) | `--audience qa` |
| `--split` | Physically split into `<slug>-dev.md` + `<slug>-qa.md` | |
| `--force-single` | Bypass the L-tier split suggestion; always single file | |
| `--no-toc` | Suppress auto-TOC for M/L tier | |
| `--from-diff` | Generate from `git diff HEAD` | |
| `--range <spec>` | Explicit git range (`A..B`). Equivalent to positional | `--range v1.2..v1.3` |
| `--dry-run` | Show the generation plan only (no file written) | |

> PR identifier, task specifier, range (`A..B`), and `--from-diff` are mutually exclusive. `--split` and `--force-single` are mutually exclusive. If incompatible flags are passed, the Skill stops and asks which mode you intended.

## Two audiences, two gates

The core design principle of the testsheet is to split by **"who runs this, when, with which tools"**.

| Section | Audience | Tools | Gate |
| --- | --- | --- | --- |
| **A. Developer Verification** | Backend / DB / DevOps engineer | psql, gh CLI, curl, docker | **Pre-merge** — contracts, migrations, workers, containers |
| **B. QA / Browser Verification** | QA, PM, Product Owner, designer | Chrome + DevTools, admin UI, test origin | **Pre-release** — end-user experience and any browser-observable effect |

Dev and QA can work in parallel; each reads only their own section.

## Automatic Tier decision

Layout is chosen automatically by scenario count, protecting readers from unread 1000-line walls.

| Tier | Scenarios | Layout |
| --- | --- | --- |
| **S** | ≤ 20 | Single file, A+B sections, no TOC, no collapsible |
| **M** | 21–40 | Single file, A+B sections, auto-TOC at top, `<details>` collapsible for Prerequisites + Edge Cases |
| **L** | > 40 | Asks the user: single file with TOC / `--split` / split by phase, then proceeds |

Most PRs land in S or M tier naturally; the L-tier prompt is a safety net for massive releases.

## Execution Cycle

```text
Step 1: Input Resolution
  └─ PR: fetch metadata and diff via gh pr view / gh pr diff
  └─ Task: load task.md / README.md from <tasks-dir>/<name>/ (prefer completed/)
  └─ Diff: capture git diff HEAD + recent commit log

Step 2: Audience and Surface Classification
  └─ Audience tag: A (Developer) or B (QA / Browser)
  └─ Surface: UI / Database / API / Background job / Configuration / Docs
  └─ Browser-observable effects: add a B section even for backend-only PRs when appropriate

Step 3: Scenario Generation
  └─ 2–5 scenarios per (audience, surface) pair
  └─ Each scenario: Goal / Preconditions / Steps / Expected / Checkbox
  └─ Source priority: PR body or Task Acceptance Criteria > commits > surface > diff edge cases

Step 4: Tier Decision
  └─ Count scenarios and decide S / M / L
  └─ L tier asks the user how to proceed before writing

Step 5: Write the Testsheet
  └─ Single file (default) or split (--split / --audience)
  └─ M/L tier inserts TOC and wraps Prerequisites/Edge Cases in <details>
  └─ If the target already exists, append -v<N> (never overwrite)

Step 6: Validate & Report
  └─ File exists, checkbox count, concrete Expected, TOC anchors
  └─ Report tier / audience / surface summary
```

## Default Filename Rule

| Input | Single file (default) | `--split` |
| --- | --- | --- |
| PR | `pr-<number>-<slug>.md` | `pr-<number>-<slug>-dev.md` + `...-qa.md` |
| Task | `task-<phase>-<sequence>-<slug>.md` | `...-dev.md` + `...-qa.md` |
| Range | `range-<short-start>-<short-end>-<slug>.md` (tag names used when both endpoints are tags, e.g. `range-v1.2-v1.3-<slug>.md`) | `...-dev.md` + `...-qa.md` |
| Diff | `<yyyymmdd-HHMM>-<branch-slug>.md` | `...-dev.md` + `...-qa.md` |

## Testsheet Structure (single-file default)

```text
1. Summary
2. Prerequisites
   2.0 Common
   2.A Dev-only
   2.B QA-only
A. Developer Verification  [pre-merge gate]
   A.1 Database / Table
   A.2 API
   A.3 Background Jobs / Workers
   A.4 Configuration
   A.5 Dev Edge Cases
   A.6 Dev Sign-off
B. QA / Browser Verification  [pre-release gate]
   B.1 UI / Browser Scenarios
   B.2 User-visible Edge Cases
   B.3 Regression (with --include-regression)
   B.4 QA Sign-off
Appendix (optional)
```

YAML front matter carries `dev_tester` / `dev_status` / `qa_tester` / `qa_status` as independent gates.

Every scenario must include a **concrete Expected result**. Vague phrasing like "check that it works" is forbidden.

## Length Management Guidelines

Built-in principles to prevent bloat:

1. **Prerequisites: Common prefix + audience suffix** — no duplication
2. **Extract > 20-line verification material** into `scripts/qa/*.sql` (or similar); reference only the path
3. **Regression by reference** — link to prior testsheets instead of duplicating
4. **Long troubleshooting / payload examples → `## Appendix`**, linked from the relevant scenario

Applied consistently, most M-tier testsheets stay under ~800 lines.

## Language Detection

Priority when `--lang` is not specified:

1. **CLAUDE.md / AGENTS.md** — directives such as `PR言語: 日本語`, `Documentation: Korean`
2. **Recent testsheets** in `docs/test-case/`
3. **Project `README.md`** language
4. **Fallback** — English

YAML front matter keys, section numbers, and template scaffolding stay in English regardless of `--lang`.

## Error Handling

| Situation | Behaviour |
| --- | --- |
| No input given | Stop; ask for PR / task / `--from-diff` |
| Multiple inputs given | Stop; ask which mode |
| `--split` + `--force-single` both set | Stop; ask which is intended |
| `gh` not authenticated (PR input) | Ask user to run `gh auth login`; stop |
| PR not found | Report the PR number; stop |
| Task not found | List similar tasks (fuzzy match); stop |
| Empty diff (diff input) | Report "nothing to test"; stop |
| Output directory not writable | Report failing path; stop (no silent fallback) |
| Target file already exists | Append `-v<N>` suffix |
| L tier detected without `--split`/`--force-single` | Stop and ask the user how to proceed |

## Integration

Downstream of the implementation-oriented `ywc` skills:

- **ywc-sequential-executor** — generates the PR/Task to be tested (upstream)
- **ywc-parallel-executor** — same, for parallel execution (upstream)
- **ywc-merge-dependabot** — merged dependency bumps that need a smoke testsheet (upstream)

## Example Prompts

### Generate from a PR URL (default: single file A+B)

```text
/ywc-gen-testcase https://github.com/legalforce/cas-marketing-on/pull/250
```

### Physical split into two files

```text
/ywc-gen-testcase 250 --split --lang ja
```

### QA-only testsheet (to hand to the QA team)

```text
/ywc-gen-testcase 250 --audience qa --lang ja
```

### Force single file even for a large PR

```text
/ywc-gen-testcase 250 --force-single
```

### Task-based with regression section

```text
/ywc-gen-testcase 000001-010-db-create-users-table --include-regression
```

### Git Range (between two tags)

```text
/ywc-gen-testcase v1.2..v1.3 --lang ja
```

### Pre-PR local range

```text
/ywc-gen-testcase HEAD~5..HEAD
```

### Dry-run

```text
/ywc-gen-testcase 250 --dry-run
```

## Triggering

Trigger conditions for this Skill are defined in the `description` field of [SKILL.md](./SKILL.md).
