# ywc-spec-writer

Project specification writer. Creates and maintains the `docs/specification/` directory with human-readable markdown. Written for both developers and non-developers — no program code, just goals, features, data, user flows, and non-functional requirements.

## Use Cases

- **New project**: Write the first full specification when none exists
- **Task-based update**: Reflect a single `ywc-task-generator` task document into the spec
- **Task Range / Multi update**: Reflect several tasks (range, glob, or multi-id) in a single pass
- **PR-based update**: Update the spec from one or more PR diffs together with PR narrative context
- **Post-commit sync**: Sync the spec after code changes
- **Full refresh**: Regenerate the entire specification from the current codebase

## Usage

```bash
/ywc-spec-writer                          # Auto mode (commit-based update)
/ywc-spec-writer --full                   # Full spec generation (requires confirmation)
/ywc-spec-writer --update                 # Regenerate all sections
/ywc-spec-writer --from-task tasks/000002-010-api-user/
/ywc-spec-writer --from-tasks 000002-010..000003-020   # Task range (may span phases)
/ywc-spec-writer --from-tasks '000002-*' 000003-010    # Glob + single id mix
/ywc-spec-writer --from-commit HEAD
/ywc-spec-writer --from-pr 42                          # Single PR
/ywc-spec-writer --from-prs 42 43 51                   # Multiple PRs (union diff)
/ywc-spec-writer --setup-hook             # Install git hook
/ywc-spec-writer --lang ja                # Write in Japanese
```

## Inputs

- (optional) `--full` / `--update` — full generation or refresh
- (optional) `--from-task <path>` — single task directory path
- (optional) `--from-tasks <id-or-pattern> ...` — task range / glob / multi-id (resolves active + completed)
- (optional) `--from-commit <ref>` — commit reference (default: `HEAD`)
- (optional) `--from-pr <num>` — single PR (requires gh CLI)
- (optional) `--from-prs <num> ...` — multiple PRs, union diff (duplicate files auto-deduplicated)
- (optional) `--lang ko|ja|en` — output language (default: `ko`)
- (optional) `--setup-hook` — install git pre-commit hook

> `--from-pr` / `--from-prs` require the `gh` CLI to be installed and authenticated. PR title / body / `headRefOid` are recorded as narrative context and audit trail when the spec is updated.

## Output

```
docs/specification/
├── README.md              # Index + change log
├── 01-overview.md         # Project overview
├── 02-features.md         # Feature requirements (user story format)
├── 03-data.md             # Data model
├── 04-interfaces.md       # External interfaces
├── 05-user-flows.md       # User flows
├── 06-requirements.md     # Non-functional requirements
└── 07-glossary.md         # Glossary
```

## Sharing With Non-Developers (HTML Export)

`docs/specification/` is a version-controlled canonical document and stays in markdown. For sharing with PMs, clients, or other non-developer stakeholders, use the read-only export script:

```bash
python3 tools/scripts/spec-to-html.py
# Produces: claudedocs/spec-export-YYYY-MM-DD.html
```

- Single self-contained HTML file (one tab per section + Copy as Markdown)
- No external dependencies (Python 3 stdlib only)
- Canonical markdown source is never modified — one-way derivation

The skill itself does **not** expose `--format html`. The convention forbidding HTML output for canonical documents is defined in [references/html-output.md](../references/html-output.md) §1.

## Related Skills

- `ywc-plan` — produces feature specs that feed into this skill
- `ywc-spec-validate` — validates the written specification
- `ywc-task-generator` — decomposes the reviewed spec into tasks
- `ywc-ubiquitous-language` — aligns spec vocabulary with domain terms
