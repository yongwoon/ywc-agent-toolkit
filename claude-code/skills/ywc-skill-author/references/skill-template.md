# ywc-* Skill Template

Use this as the starting structure for a new ywc-* skill. Replace every `<...>` placeholder. Remove sections that genuinely do not apply (using `N/A — <reason>` rather than silent removal where the section heading still belongs).

---

## SKILL.md

```markdown
---
name: ywc-<short-noun-or-verb>
description: (ywc) Use when <primary trigger condition>. Triggers: "<한국어>", "<english>", "<日本語>", "<other natural-language phrases users would actually say>". Do not use for <anti-trigger 1>, <anti-trigger 2 — point to ywc-X if a sibling skill is the right one>.
requires: [<ywc-X if upstream skill is required, else omit>]
---

# <Skill Display Name>

**Announce at start:** "I'm using the ywc-<name> skill to <one-sentence purpose>."

<2-3 sentence summary of what the skill does and the canonical scenario it solves. State the input the user provides and the output the skill produces.>

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "<the most likely shortcut the agent will try>" | <why that shortcut produces a wrong result> |
| "<the second most likely shortcut>" | <reality counter> |
| "<a domain-specific anti-pattern, e.g., 'force-merge if CI is yellow'>" | <reality counter> |
| "<a vague-language temptation, e.g., 'appropriate severity'>" | <reality counter — pick a concrete threshold> |
| "<a scope-creep temptation, e.g., 'fix this unrelated bug while I'm here'>" | <reality counter — boundary> |

**Violating the letter of these rules is violating the spirit.** <One-sentence reminder of why honesty over speed matters in this domain.>

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--<flag>` | `--<flag> <value>` | `--<flag> example` | <one-line description> |

(Remove this section if the skill takes no flags or positional arguments.)

## Workflow

Numbered steps describing the process. Each step should be:

- Concrete enough that an agent can execute it without inference.
- Reference specific commands, files, or sibling skills.
- Include stop-conditions where applicable.

### Step 1: <Action>

<Description of what to do, what to read, and what success looks like.>

### Step 2: <Action>

<...>

## Output Format

```text
<sample of the artifact this skill produces — exact format the agent should emit>
```

## Validation

Before declaring the skill's task complete, verify:

- [ ] <verifiable condition 1>
- [ ] <verifiable condition 2>
- [ ] <verifiable condition 3>

## Common Mistakes

- **<Mistake A>** — <why it happens, how to avoid it>
- **<Mistake B>** — <why it happens, how to avoid it>

## Integration

- **Upstream**: <which ywc-* skill, if any, must run before this one>
- **Downstream**: <which ywc-* skill, if any, typically follows this one>
- **Pairs with**: <related skills that operate on the same artifact>

(Use `N/A — standalone skill` if the skill has no pipeline relationships.)
```

---

## README.md (Korean — 기본 진입 문서)

```markdown
# ywc-<name>

<2-3 sentence Korean summary, technical terms in English per project policy>

## 사용 시나리오

- <시나리오 1: 사용자가 "<자연어 한국어 trigger>" 라고 말할 때>
- <시나리오 2>

## 사용 방법

\`\`\`bash
/<slash-command-name> <arguments>
\`\`\`

또는 자연어로 호출:

> "<한국어 trigger 예시>"

## 입력

- <필수 input 설명>
- (선택) <옵션 input 설명>

## 출력

- <skill 이 생성하는 artifact 설명>

## 관련 Skill

- `ywc-<upstream>` — <관계 설명>
- `ywc-<downstream>` — <관계 설명>
```

---

## README.en.md / README.ja.md / README.ko.md

These follow the same structure as the Korean `README.md` but in their respective languages. Always create the full locale set together so the documentation cannot drift between languages.

For Korean and Japanese, **keep technical terms in English** (Database, API, Backend, etc.) per the project-wide language policy in `claude-code/skills/CLAUDE.md`.

---

## Optional: references/

Create this directory only when long-form content (>30 lines of static rules, lookup tables, or templates) lives outside the workflow path. Examples from existing skills:

- `references/granularity-modes.md` (ywc-task-generator) — full mode specification
- `references/language-policy.md` (ywc-task-generator) — locale-specific writing rules
- `references/parallel-execution-metadata.md` (ywc-task-generator) — Ownership / Shared Surfaces / Conflicts With detail

The SKILL.md body should contain a brief summary plus a one-line pointer:

```markdown
For the full <topic>, see [references/<file>.md](references/<file>.md).
```

---

## Optional: evals/evals.json

When the skill produces objectively verifiable output (file transforms, structured reports, code generation), add an evals harness following the schema used by other ywc-* skills.

```json
{
  "skill_name": "ywc-<name>",
  "evals": [
    {
      "id": 1,
      "prompt": "<realistic user prompt>",
      "expected_output": "<description of what the skill should produce>",
      "files": []
    }
  ]
}
```
