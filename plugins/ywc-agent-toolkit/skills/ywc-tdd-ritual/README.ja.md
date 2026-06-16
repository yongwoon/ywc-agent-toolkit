# ywc-tdd-ritual

実装着手前に RED → GREEN → REFACTOR cycle を強制する TDD discipline skill です。

## 何をするか

次の Iron Law を強制します:

> **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**

7 段階の cycle を通過してから production code を commit します。

1. **RED** — 1 つの behavior に対する minimal failing test を作成 (production code はまだ無い)
2. **Verify RED** — Test が実際に失敗するかを **目視確認** (skip 厳禁)
3. **GREEN** — その test を通すだけの最小 production code を書く
4. **Verify GREEN** — 新 test + 全 suite が通過することを確認
5. **REFACTOR** — Green 状態を保ちながら重複除去・命名改善
6. **Verify after REFACTOR** — Refactor 後も全 test が通過すること
7. 次の behavior に loop するか、`ywc-verify-done` へ handoff

「Code を先に書いて test は後で」というパターンは禁止されます。後付けで書いた test は初回実行で必ず通ってしまい、実際に欠陥を捉えるかどうか検証できないためです。

## いつ trigger されるか

- ユーザーが「TDD」「test first」「テスト先行」「RED-GREEN」などを言及した時
- 新規 feature / bug fix / behavior 変更を実装する時
- `ywc-code-gen --tdd` が委任してきた時
- `ywc-debug-rootcause` Phase 4 §1 の regression test を書く時

## 使わない場面

- ユーザーが明示的に throwaway prototype と宣言した場合
- 既存 test failure の root-cause 調査 → `ywc-debug-rootcause`
- Generated code / config ファイル
- 完了 claim の検証 → `ywc-verify-done` (TDD は書く discipline、verify-done は主張する discipline)

## 参考

詳細な cycle 規則・Rationalization Defense・Output Format は [SKILL.md](./SKILL.md) を参照してください。元の process discipline は `superpowers:test-driven-development` を参考にし、ywc の handoff 流れ (`ywc-verify-done`, `ywc-debug-rootcause`) に合わせて調整しています。

## Localized Versions

- [한국어 (default)](./README.md)
- [English](./README.en.md)
- [한국어 (full)](./README.ko.md)
