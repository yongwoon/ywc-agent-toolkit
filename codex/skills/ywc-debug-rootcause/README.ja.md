# ywc-debug-rootcause

Bug · Test failure · Build failure などすべての defect に対して **root cause を先に特定**することを強制する process discipline skill です。

## 何をするか

次の Iron Law を強制します:

> **NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

Phase 1 (Investigation) を通過するまではいかなる fix も提案できません。4 段階 process は:

1. **Phase 1 — Root-cause investigation** — Error メッセージを最後まで読む、確実に再現、recent change を確認、multi-component の境界に diagnostic instrumentation、data flow を origin まで遡る
2. **Phase 2 — Pattern analysis** — 同じ codebase の working sibling を end-to-end で読み、broken との差分をすべて列挙する (「効かなそう」と思った差分も含む)
3. **Phase 3 — Hypothesis and testing** — 「X が root cause; 最小変更 Z で解決する」形式の単一仮説、一度に一変数のみ変更
4. **Phase 4 — Implementation** — Regression test → 単一 fix → red-green-red 検証 → `ywc-verify-done` で gating

最小 feedback loop の失敗と catches/misses を記録し、3–5 個の反証可能な候補を順位付けして一度に一変数を試します。自動再現不可なら手動の証拠と制約を示し、RED を捏造しません。3 回失敗後は停止。正しい debug 応答に別々の evidence-linked `Fix #4 signal: fix harder` と `Next fix worth attempting: <one concrete minimal change>` が両方ある場合だけ最後の 4 回目を一度許可し、失敗後の 5 回目は禁止です。

## いつ trigger されるか

- ユーザーが「バグ」「デバッグ」「落ちる」「通らない」「debug」などに言及した時
- Test / build / type-check の failure
- 同じ surface で 2 回以上 fix 試行が失敗した直後
- `ywc-verify-done` の failure routing 表から誘導された時

## 使わない場面

- 実装の作成段階 → `ywc-code-gen`
- Incident 終了後の retrospective → `ywc-incident-postmortem`
- Security finding triage → `ywc-security-audit`
- 実装着手前の confidence 判断 → その判断を扱う planning または spec-review skill

## 参考

Phase ごとの checklist と Rationalization Defense は [SKILL.md](./SKILL.md) を参照してください。元の process discipline は `superpowers:systematic-debugging` を参考にしています。

## Localized Versions

- [한국어 (default)](./README.md)
- [English](./README.en.md)
- [한국어 (full)](./README.ko.md)

## Analyst contract

`Caller: ywc-debug-rootcause` · `analysis_mode=debug_hypotheses`

Caller と analysis_mode を明示します。欠落・unknown・不一致は推測せず `NEEDS_CONTEXT`。Status → Summary → Finding counts → Analysis mode を検証し、既存 caller gate を維持します。

最小 feedback loop の失敗と catches/misses を記録し、3–5 個の反証可能な候補を順位付けして一度に一変数を試します。自動再現不可なら手動の証拠と制約を示し、RED を捏造しません。3 回失敗後は停止。正しい debug 応答に別々の evidence-linked `Fix #4 signal: fix harder` と `Next fix worth attempting: <one concrete minimal change>` が両方ある場合だけ最後の 4 回目を一度許可し、失敗後の 5 回目は禁止です。

Live runtime: `UNVERIFIED — instruction contract only`.
