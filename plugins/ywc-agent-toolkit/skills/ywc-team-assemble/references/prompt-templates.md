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

Explorer is an independent role. Pass the independent projection only: the
three allowlisted fields below and nothing else. There is no free-form
background field, because a free-form field can smuggle a peer conclusion, raw
content, or a diff past the allowlist.

```text
Included scope:
- {project-relative path or bounded scope}
Excluded scope:
- {project-relative path or explicit exclusion}
Artifacts:
- {project-relative artifact path}

Goal:
Answer this bounded codebase question: {question}

Scope:
- Read only the paths listed under `Included scope` and `Artifacts`.
- Do not read anything listed under `Excluded scope`.
- Do not edit files.
- Do not run destructive commands.

Output:
- Direct answer
- Relevant file references
- Confidence level
- Open questions, if any

Isolation:
- This packet contains only `Included scope`, `Excluded scope`, and `Artifacts`
  (paths). Never add diff content, raw file content, peer Claims, peer
  conclusions, peer recommendations, or transcript to any field.
- Do not request or accept those fields if offered.
- If the question cannot be answered from the allowlisted scope, return
  `NEEDS_CONTEXT` naming the missing path or citation.
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
  Claims. Each Claim has exactly two fields, named `Statement` and `Evidence` —
  no more and no fewer.
  - `Statement`: factual, at most 1,024 characters.
  - `Evidence`: exactly one valid project-relative `file:line` citation with a
    positive line number, or one project-relative artifact path.
- Do not rename these fields, and do not add any third field to a Claim.
- Do not include raw output, generated source, full diffs, or transcript fields.
```

## Reviewer

Choose exactly one projection and pass only that projection's allowlisted
fields. Do not include a free-form background field in either variant.

Independent reviewer packet:

```text
Included scope:
- {project-relative path or bounded scope}
Excluded scope:
- {project-relative path or explicit exclusion}
Artifacts:
- {project-relative artifact path}
```

Dependent reviewer packet:

```text
Claims:
  - Statement: {factual statement, <= 1,024 characters}
    Evidence: {project-relative file:line or artifact path}
Artifacts:
- {only the project-relative artifact paths cited by the Claims above}
```

Body of the prompt, appended to whichever packet was selected:

```text
Goal:
Review the allowlisted scope for {risk area}.

Scope:
- Independent: inspect only the paths under `Included scope` and `Artifacts`,
  and never anything under `Excluded scope`.
- Dependent: inspect only the artifact paths cited by `Claims`.
- Never place diff content, raw file content, or peer conclusions in any field
  of either packet.
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
