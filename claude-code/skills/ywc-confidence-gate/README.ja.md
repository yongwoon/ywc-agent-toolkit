# ywc-confidence-gate

実装着手直前に 5 次元 confidence score を強制し、PROCEED / REVIEW / STOP の判断を surface する pre-implementation discipline skill です。

## 何をするか

次の Iron Law を強制します:

> **NO IMPLEMENTATION WITHOUT AN EXPLICIT CONFIDENCE SCORE AND BAND DECISION**

5 次元 rubric (各 0〜100) で採点し、加重合計で band を決定します。

| 次元 | 重み | 1 文の問い |
|---|---|---|
| Scope clarity | 25% | In-scope と out-of-scope を 1 文ずつ曖昧語なしで書けるか |
| Architecture compliance | 25% | 既存構造 / 命名 / abstraction に従っているか |
| Evidence quality | 20% | 主張が primary source (コード、公式 docs、test 出力) に基づいているか |
| Reuse verified | 15% | 既存 utility / library を検索し、各々を除外する理由を述べているか |
| Root cause identified | 15% | Bug なら symptom ではなく underlying cause、新規なら surface request ではなく underlying need を名指せているか |

| Band | Aggregate | 単一次元規則 | 行動 |
|---|---|---|---|
| **PROCEED** | ≥ 90 | 全て > 50 | 実装開始。Executor report にスコアを surface |
| **REVIEW** | 70〜89 | 単一 < 50 が無いとき | 1〜3 個の alternative or 未確定事項を提示し、弱い次元を解消してから進む |
| **STOP** | < 70 | 単一 ≤ 50 で強制 downgrade | 実装禁止。弱い次元と raise 方法を surface し、上流 skill に routing |

**単一次元 ≤ 50 規則**: aggregate が threshold を超えても、単一次元が 50 以下なら band を 1 段階下げます。強い次元が fatal weakness を隠さないための装置です。

## いつ trigger されるか

- ユーザーが「実装着手してよいか」「準備できた?」「ready to implement」「確信度チェック」などを言及した時
- `ywc-code-gen` / `ywc-sequential-executor` / `ywc-parallel-executor` / `ywc-agentic` の境界
- `ywc-plan` の Scale 判定後、downstream handoff の直前
- アーキテクチャ影響の大きい commit の直前

## 使わない場面

- 完了後の検証 → `ywc-verify-done` (対称な gate、同じ rubric)
- Spec 品質レビュー → `ywc-spec-validate`
- 実装結果の review score → `ywc-impl-review` (この skill と同じ rubric を使うため score を比較可能)
- 意図の明確化 → `ywc-brainstorm`

## 参考

詳細な workflow と anti-pattern は [SKILL.md](./SKILL.md)、標準 rubric 定義は共有 reference [../references/confidence-gate.md](../references/confidence-gate.md) にあります。発想は ECC の confidence-check と SuperClaude の PM Agent rubric から引いています。

## Localized Versions

- [한국어 (default)](./README.md)
- [English](./README.en.md)
- [한국어 (full)](./README.ko.md)
