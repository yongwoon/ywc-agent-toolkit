# ywc-team-assemble

ユーザーが specialist team、subagent delegation、parallel agent work を明示的に依頼したときに使う Codex skill です。

## 使う場面

- ユーザーが team 編成、agent への delegation、parallel 実行を明示的に依頼している
- 独立した workstream が 2 つ以上ある
- write scope を分離でき、親 agent が結果を review して統合できる

単純な質問、単一ファイル編集、厳密に順次実行する作業には使いません。

## 含まれるファイル

- `SKILL.md` — team assembly workflow
- `agents/openai.yaml` — Codex metadata
- `references/prompt-templates.md` — explorer、worker、reviewer prompt template
- `evals/evals.json` — role isolation、Claim/Evidence、cap、privacy の contract evals

## Context Safety

Team prompt は projection 前に bounded Claims と cited evidence を検証します。Independent reviewer には scope と artifact path のみ、dependent role には Claims とそれらが引用する artifact のみを渡します。peer conclusion/recommendation、transcript、raw content、uncited artifact、invalid または over-cap Claim は拒否します。
