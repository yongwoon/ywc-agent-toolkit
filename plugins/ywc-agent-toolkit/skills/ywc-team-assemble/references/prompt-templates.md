# Subagent Prompt Templates

Use these templates when `ywc-team-assemble` needs multiple specialist roles.

## Read-only Explorer

```text
Context:
{project or task background}

Goal:
Answer this bounded codebase question: {question}

Scope:
- Read only these paths when possible: {paths}
- Do not edit files.
- Do not run destructive commands.

Output:
- Direct answer
- Relevant file references
- Confidence level
- Open questions, if any
```

## Implementation Worker

```text
Context:
{project or task background}

Goal:
Implement {specific change}.

Ownership:
- You may edit: {allowed files or directories}
- Do not edit: {excluded files or directories}
- You are not alone in the codebase. Do not revert changes made by others. Adapt to concurrent changes where needed.

Verification:
Run {commands} if feasible.

Output:
- Summary of implementation
- Files changed
- Verification results
- Remaining risks
```

## Reviewer

```text
Context:
{project or task background}

Goal:
Review {scope} for {risk area}.

Scope:
- Inspect: {paths or diff}
- Do not edit files.
- Prioritize concrete bugs, regressions, and missing tests.

Output:
- Findings first, ordered by severity
- File and line references where possible
- Test gaps
- Residual risk
```
