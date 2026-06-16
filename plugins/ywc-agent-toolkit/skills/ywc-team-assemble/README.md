# ywc-team-assemble

Codex에서 사용자가 명시적으로 specialist team, subagent delegation, parallel agent work를 요청했을 때 작업을 역할별로 나누고 통합하는 skill입니다.

## 언제 사용하나요

- 사용자가 "team을 구성해줘", "agent들에게 나눠서 맡겨줘", "parallel로 진행해줘"처럼 명시적으로 delegation을 요청한 경우
- 독립적인 workstream이 2개 이상 있고 write scope를 분리할 수 있는 경우
- subagent 결과를 review하고 하나의 결과로 synthesize해야 하는 경우

단순 질문, 단일 파일 수정, 엄격히 순차적인 작업에는 사용하지 않습니다.

## 포함 파일

- `SKILL.md` — team assembly workflow
- `agents/openai.yaml` — Codex metadata
- `references/prompt-templates.md` — explorer, worker, reviewer prompt template
