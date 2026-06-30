# Codex Agent Evaluation Rubric

Score every Codex custom agent under `codex/agents/*.toml` on eight
dimensions. These agents are TOML files installed to `${CODEX_HOME:-~/.codex}/agents`.

| Level | Meaning |
|---|---|
| 0 | Missing or invalid |
| 1 | Present but materially weak |
| 2 | Adequate operating baseline |
| 3 | Strong and reliable |
| 4 | Exemplary reference quality |

Composite grade: `A >= 3.5`, `B 2.5-3.49`, `C 1.5-2.49`, `D < 1.5`.

| Dim | Weight |
|---|---:|
| A1 Routing description | 0.16 |
| A2 TOML structural validity | 0.14 |
| A3 Mission and boundaries | 0.16 |
| A4 Sandbox and least privilege | 0.13 |
| A5 Model and reasoning fit | 0.10 |
| A6 Output contract | 0.14 |
| A7 Caller integration | 0.09 |
| A8 Behavioral evidence | 0.08 |

## A1: Routing Description

| Score | Criteria |
|---|---|
| 0 | Missing or empty `description` |
| 1 | Generic capability blurb with unclear routing |
| 2 | Describes the main task adequately |
| 3 | Names precise review/advisor surface and adjacent exclusions |
| 4 | L3 plus avoids every plausible sibling-agent collision |

Evidence: TOML `description`, sibling agent catalog.

## A2: TOML Structural Validity

| Score | Criteria |
|---|---|
| 0 | TOML cannot parse |
| 1 | Missing required keys |
| 2 | Required keys exist: `name`, `description`, `developer_instructions` |
| 3 | L2 plus `model`, reasoning effort, and `sandbox_mode` are present where needed |
| 4 | L3 plus filename/name match and no stale Claude-only fields |

Evidence: `inventory_gate.py` agent gate.

## A3: Mission and Boundaries

| Score | Criteria |
|---|---|
| 0 | Instructions lack a mission |
| 1 | Mission exists but boundaries are boilerplate |
| 2 | Mission and basic exclusions are understandable |
| 3 | Boundaries name what to refuse and where to redirect |
| 4 | L3 plus boundaries are testable by a caller |

Evidence: `developer_instructions` sections or equivalent labels.

## A4: Sandbox and Least Privilege

| Score | Criteria |
|---|---|
| 0 | Write access granted to a read-only role without justification |
| 1 | Sandbox is over-broad for the mission |
| 2 | Sandbox is plausible |
| 3 | Sandbox exactly matches role and edit boundary |
| 4 | L3 plus dangerous capabilities are deliberately excluded |

Evidence: `sandbox_mode`, mission, boundaries.

## A5: Model and Reasoning Fit

| Score | Criteria |
|---|---|
| 0 | Missing or invalid model field |
| 1 | Clear mismatch between model tier and cognitive load |
| 2 | Plausible model choice |
| 3 | Model and reasoning effort fit the mission |
| 4 | L3 plus cost/latency/depth trade-off is explicit or obvious from role |

Evidence: `model`, `model_reasoning_effort`, mission complexity.

## A6: Output Contract

| Score | Criteria |
|---|---|
| 0 | No output instructions |
| 1 | Prose-only output guidance |
| 2 | Required sections are named |
| 3 | Starts with shared status and defines concise result shape |
| 4 | L3 plus caller can consume the result without post-parsing guesswork |

Evidence: output block and required `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`.

## A7: Caller Integration

| Score | Criteria |
|---|---|
| 0 | No skill or workflow appears to call this agent |
| 1 | Intended caller is unclear |
| 2 | At least one Codex skill references the agent |
| 3 | Caller passes a bounded packet and respects the agent boundary |
| 4 | L3 plus fallback path is documented when custom-agent dispatch is unavailable |

Evidence: `rg <agent-name> codex/skills`.

## A8: Behavioral Evidence

| Score | Criteria |
|---|---|
| 0 | Instructions would likely produce harmful or unusable output |
| 1 | Happy-path behavior is underspecified |
| 2 | Happy path can be reasoned from instructions |
| 3 | Edge cases and refusal cases are covered |
| 4 | L3 plus smoke fixtures or eval evidence exist and pass |

Evidence: eval fixtures if present; otherwise reasoned estimate with uncertainty.
