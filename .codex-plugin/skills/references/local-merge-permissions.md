# Pre-Authorizing Tool Permissions for `--local-merge`

> Used by: `ywc-sequential-executor`, `ywc-parallel-executor`

Read this when setting up unattended `--local-merge` execution, or when an executor keeps stopping for tool confirmation even though the skill says to continue.

## Why This Matters

Range executors run many short `git`, `gh`, `mv`, and `mkdir` commands per task or wave. If the tool permission layer prompts on each command, non-stop execution becomes interactive.

The Non-Stop Execution Principle governs LLM behavior. It cannot override the runtime's permission system. Configure Codex approval settings or project-local policy so the expected command prefixes can run without repeated prompts.

## Recommended Prefixes

Pre-authorize these command families for repositories where you intentionally run `--local-merge`:

```text
git status
git diff
git log
git branch
git checkout
git pull
git push
git merge
git add
git commit
git mv
git worktree
mkdir -p
mv tasks/
test -d
gh auth status
gh pr
```

Most are read-only or repository-scoped. The state-changing commands are the expected branch lifecycle: create branch, implement, commit, push, merge, and move task directories.

## Narrow Fallback

If policy must stay strict, pre-authorize only the state transitions that most often interrupt range mode:

```text
git checkout
git pull
git push
git merge
git mv
git worktree
```

The remaining commands may still prompt, but the core merge-to-next-task loop will have fewer interruptions.

## Safety Notes

- Branch protection and server-side rules still apply. Local approval for `git push` does not bypass remote protections.
- The skills still forbid broad staging such as `git add -A` unless explicitly allowed by the skill.
- Do not pre-authorize destructive commands such as `git reset --hard`, force-push, database deletion, or production deployment through this reference.

## Diagnosis

If execution still pauses after pre-authorization, check:

1. Whether the skill hit an allowed stop reason such as merge conflict, push rejection, or repeated verification failure.
2. Whether the invocation actually requested range mode and `--local-merge`.
3. Whether an advisor escalation is running; that is a bounded judgment pass, not a permission prompt.
