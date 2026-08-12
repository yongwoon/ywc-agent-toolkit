# ywc-team-assemble

사용자가 specialist team, subagent delegation, parallel agent work를 명시적으로 요청했을 때 사용하는 Codex skill입니다.

## 사용 시점

- 사용자가 team 구성, agent delegation, parallel 실행을 명시적으로 요청한 경우
- 독립적인 workstream이 2개 이상인 경우
- write scope를 분리할 수 있고 parent agent가 결과를 review한 뒤 통합할 수 있는 경우

단순 질문, 단일 파일 수정, 엄격히 순차적인 작업에는 사용하지 않습니다.

## 포함 파일

- `SKILL.md` — team assembly workflow
- `agents/openai.yaml` — Codex metadata
- `references/prompt-templates.md` — explorer, worker, reviewer prompt template
- `evals/evals.json` — role isolation, Claim/Evidence, cap, privacy contract eval

## Context Safety

Team prompt는 projection 전에 bounded Claims와 cited evidence를 검증합니다. Independent reviewer에는 scope와 artifact path만, dependent role에는 Claims와 해당 Claim이 인용한 artifact만 전달합니다. peer conclusion/recommendation, transcript, raw content, uncited artifact, invalid 또는 over-cap Claim은 거부합니다.
