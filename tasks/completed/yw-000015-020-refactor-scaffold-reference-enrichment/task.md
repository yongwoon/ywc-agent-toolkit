# yw-000015-020-refactor-scaffold-reference-enrichment — Implementation Checklist

## Prerequisites
- [ ] Confirm the source spec and the current JavaScript and Go references are available.
- [ ] Confirm no other task edits either reference file concurrently.

## Allowed Edit Scope
- [ ] Edit only `codex/skills/ywc-project-scaffold/references/javascript.md` and `references/go.md`.

## Stop Conditions
- [ ] Stop if a requested change requires removing an existing variant or renaming a preserved example.
- [ ] Stop if a framework/library dependency or generated file is proposed.
- [ ] Stop if Go interface ownership would place one contract in both aggregate and consumer locations.

## Implementation Steps
- [ ] Add JavaScript TOC entries and shared `Naming Convention` guidance for kebab-case directories, PascalCase components, camelCase utilities/config, and explicit Next/layout/UI-kit exceptions.
  - Related AC/FR: AC7 / FR4
  - Contract / Behavior Change: cross-framework naming is clear without a blanket rule that invalidates framework-owned filenames.
  - Verification Command / Evidence: `rg -n 'Naming Convention|Next App Router|UI-kit|PascalCase|camelCase' references/javascript.md`
- [ ] Add `Component Logic Colocation` describing component-local `hooks/` and `functions/`, staged promotion to feature then app-shared reuse, and Astro interactive-island scope.
  - Related AC/FR: AC7 / FR4
  - Contract / Behavior Change: reuse boundaries are explicit for React/Next/Astro component logic.
  - Verification Command / Evidence: `rg -n 'Component Logic Colocation|hooks/|functions/|interactive islands|app-shared' references/javascript.md`
- [ ] Link only Next.js small/medium/large and Astro medium Key Points to the shared sections while preserving their current trees and lowercase examples.
  - Related AC/FR: AC7 / FR4
  - Contract / Behavior Change: variants consume shared guidance without duplication or mechanical renames.
  - Verification Command / Evidence: manual diff review of the four affected Key Points blocks.
- [ ] Add Go Large (Layered, Connect RPC) beside DDD, its selection criteria, precise aggregate/usecase port ownership, optional usecase types, converter guidance, and convention rows for `injector/`, `gen/`, and `converter/`.
  - Related AC/FR: AC8–AC9 / FR5
  - Contract / Behavior Change: large Go services can choose layered CRUD structure while preserving DDD for diverging bounded contexts.
  - Verification Command / Evidence: `rg -n 'Go Large \(Layered, Connect RPC\)|usecase/port|aggregate|usecase/types|injector/|gen/|converter/' references/go.md`

## Task Verify
- [ ] `python3 - <<'PY'
from pathlib import Path
for name in ('javascript.md', 'go.md'):
    text = Path('codex/skills/ywc-project-scaffold/references', name).read_text()
    assert text.count('## Table of Contents') == 1
    assert '## Conventions' in text or name == 'javascript.md'
print('reference structure checks passed')
PY`
  - Expected Passing Signal: exit 0 and the structure check passes.
  - Pre-change Failing Evidence / Exception: N/A — additive documentation task.
  - Contract/Test Evidence: targeted assertions plus diff review.
- [ ] `git diff --check -- codex/skills/ywc-project-scaffold/references/javascript.md codex/skills/ywc-project-scaffold/references/go.md`
  - Expected Passing Signal: exit 0 with no whitespace errors.
  - Pre-change Failing Evidence / Exception: N/A — Markdown-only task.
  - Contract/Test Evidence: source diff inspection.

## Verification
- [ ] lint passes (`npx markdownlint-cli2@0.22.1 codex/skills/ywc-project-scaffold/references/javascript.md codex/skills/ywc-project-scaffold/references/go.md` or installed equivalent)
- [ ] typecheck passes (N/A — Markdown-only task)
- [ ] unit tests pass (N/A — contract fixture is a later task)
- [ ] app builds without error (N/A — repository has no application build)
