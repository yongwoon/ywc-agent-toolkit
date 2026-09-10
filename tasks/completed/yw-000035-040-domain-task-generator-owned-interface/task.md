# yw-000035-040-domain-task-generator-owned-interface — Implementation Checklist

## Prerequisites
- [ ] None — root task.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `claude-code/skills/ywc-task-generator/references/README.md.template` only.

## Stop Conditions
- [ ] Stop if `### Owned Interface` already exists in the file at task start.
- [ ] Stop if `### Ownership` heading is missing (insertion anchor gone).

## Implementation Steps
- [ ] Run `grep -n "^### Ownership\|^### Shared Surfaces" claude-code/skills/ywc-task-generator/references/README.md.template` to confirm exact line numbers.
- [ ] Insert `### Owned Interface` immediately after the `### Ownership` block's content and before `### Shared Surfaces`:
  - [ ] Body text: "Public interface this task confirms and owns; other tasks trust this signature and do not read the implementation."
  - [ ] Sentinel line: `(None — no public interface owned)`.
  - [ ] An HTML `<!-- NOTE: ... -->` comment matching the template's existing NOTE-comment style, explaining the distinction from the broader `### Ownership` field (Ownership = files a task may edit; Owned Interface = the specific signature other tasks may trust without reading the implementation).
- [ ] Check `claude-code/skills/ywc-task-generator/references/dependency-graph.md.template` for any Ownership-related content that would need mirroring — confirmed during investigation it has none; skip if still true.

## Task Verify
- [ ] `grep -n "^### Owned Interface" claude-code/skills/ywc-task-generator/references/README.md.template`
- [ ] Line-number check: `### Ownership` < `### Owned Interface` < `### Shared Surfaces`
- [ ] `grep -q "None — no public interface owned" claude-code/skills/ywc-task-generator/references/README.md.template`

## Verification
- [ ] `bash scripts/validate.sh` exits 0
- [ ] No lint/typecheck/build/test toolchain applies to this repository.
