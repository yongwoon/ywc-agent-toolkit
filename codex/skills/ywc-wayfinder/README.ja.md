# ywc-wayfinder

大規模または不確実な変更を複数 session にわたって探索するときに使う discovery Skill です。ローカル Markdown map と 1 つの active ticket だけを維持し、実装ではなく次の routing を決めます。

## 使用シナリオ

- ordinary planning に入る前に unresolved decision が多すぎるとき
- 複数 session にまたがる discovery が必要なとき
- external tracker write なしで deterministic な handoff が必要なとき

## コア契約

- canonical map path: `docs/ywc-plans/<slug>-wayfinder.md`
- active ticket は常に 1 つだけ
- terminal resolved は `DONE` で final write なし
- terminal deferred / blocked は `NEEDS_CONTEXT` で final write なし
