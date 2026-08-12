# Subagent Prompt Templates

Use these templates when `ywc-team-assemble` needs multiple specialist roles.

## Context packet contract

Before using any role template, assemble and validate one bounded packet:

```text
Included scope:
- <project-relative path or bounded scope>
Excluded scope:
- <project-relative path or explicit exclusion>
Artifacts:
- <project-relative artifact path>
Claims:
  - Statement: <factual statement, <= 1,024 characters>
    Evidence: <project-relative file:line or artifact path>
```

`Claims` is optional and may contain zero to three items. Each item has exactly
`Statement` and `Evidence`; evidence is required and must be a project-relative
`file:line` citation with a positive decimal line number or a project-relative
artifact path. Reject absolute paths, `..`, URIs, unlabelled prose, missing
evidence, malformed citations, and more than three Claims as `BLOCKED`.

Run recursive privacy validation over the complete source packet before
projection. Reject any key whose normalized name contains `transcript`,
`chain_of_thought`, `generated_source`, `full_diff`, `raw_tool_output`,
`raw_response`, or `tool_output`, including nested metadata and separator or
case variants. The rejection names only the field and rule. Do not redact,
summarize, retry, or forward a rejected packet.

The following role packets are constructed as allowlists, not as instructions
to ignore fields in a larger payload:

| Projection | Allowed input | Excluded input |
| --- | --- | --- |
| Independent reviewer | `Included scope`, `Excluded scope`, `Artifacts` (paths only) | `Claims`, peer conclusions, peer recommendations, transcript, raw content |
| Dependent role | `Claims`, and only the artifact paths cited by those Claims | uncited artifacts, peer transcript, peer conclusions, peer recommendations, raw content |

If a dependent role's cited artifact or citation is unavailable, return
`NEEDS_CONTEXT` with the missing path/citation and do not forward the producer
payload. An independent reviewer must form its own finding without peer
conclusions or recommendations.

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

Isolation:
- If this is an independent review, receive only the independent projection.
- Do not request or accept peer Claims, conclusions, recommendations, or transcript.
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

Claims:
- If a dependent consumer is explicitly requested, return no more than three
  factual Claims, each with one valid project-relative citation or artifact path.
- Do not include raw output, generated source, full diffs, or transcript fields.
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

Projection:
- Independent reviewers get scope and artifact paths only; omit peer Claims,
  conclusions, recommendations, transcript, and raw content.
- Dependent reviewers get only validated Claims and the artifacts those Claims
  cite; omit every uncited artifact and every peer/raw field.
- Validate the complete payload, including nested metadata, before projection.
```
