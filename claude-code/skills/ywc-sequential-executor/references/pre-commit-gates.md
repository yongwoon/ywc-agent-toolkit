# Pre-Commit Gates (Step 3, before first commit)

Run both gates below before creating the first commit for a task.

## Completeness Gate

Run a stub-pattern check on all modified files:

```bash
files="$(git ls-files -co --exclude-standard | grep -vE '(^|/)(test|tests|spec|__tests__)/|\.test\.' || true)"
if [ -n "$files" ]; then
  printf '%s\n' "$files" | xargs grep -lnE \
    "TODO|FIXME|XXX|HACK|raise NotImplementedError|throw new Error\(.*[Nn]ot [Ii]mplemented" \
    2>/dev/null || echo "OK: no stub patterns found"
else
  echo "OK: no files to scan"
fi
```

If any stub patterns appear in implementation files, complete the implementation before committing. Stubs committed here become Step 4 verification failures; catching them before the first commit saves the entire retry cycle.

**Exception**: `TODO` comments in *test* files (e.g., `// TODO: add edge case for overflow`) are permitted. `TODO` in implementation files are not.

## Ownership-scope Gate

Mechanize the prose Surgical-changes rule. Run `git diff --name-only HEAD` and confirm every changed path falls within the task's declared Ownership from `README.md`. Any file outside Ownership is a scope-creep signal — either it is a genuine dependency the task missed (stop and report `BLOCKED`) or a drive-by edit (revert it). Do not commit out-of-Ownership files with an unexplained justification.

```bash
git diff --name-only HEAD   # every path must match the README Ownership globs
```
