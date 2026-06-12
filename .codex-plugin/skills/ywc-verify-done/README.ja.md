# ywc-verify-done

完了主張の前に fresh verification evidence を強制する process discipline skill です。

## 何をするか

「作業完了 / Tests pass / Build 成功 / Bug 修正 / 要件達成」のような完了主張を surface する直前にこの skill を呼び出します。次の 5 段階 Gate Function を強制します。

1. **IDENTIFY** — その主張を証明する正確な shell command を名指す
2. **RUN** — その command を **現在の message 内で fresh に** 実行する
3. **READ** — 全 output と exit code を読む
4. **VERIFY** — output が主張文の表現を裏付けているか確認する
5. **CLAIM** — 1〜4 を通過した場合のみ、verification block と共に主張を surface する

「should」「probably」「seems」のような未検証語彙は禁止されます。

## いつ trigger されるか

- ユーザーが「完了」「終わった」「done」などの完了 signal を出した時
- Commit / PR 作成 / Merge の直前
- Executor (`ywc-sequential-executor`, `ywc-parallel-executor`) の task transition 直前
- Subagent return payload を受け取った直後

## 使わない場面

- 実装の最中 → `ywc-code-gen`
- Bug の root cause 調査 → `ywc-debug-rootcause`
- 実装着手前の confidence 判断 → その判断を扱う planning または spec-review skill
- Plan 段階の codebase exploration → `ywc-plan`

## 参考

詳細な rule・Output Format・Rationalization Defense は [SKILL.md](./SKILL.md) を参照してください。元の process discipline は `superpowers:verification-before-completion` を参考にしています。

## Localized Versions

- [한국어 (default)](./README.md)
- [English](./README.en.md)
- [한국어 (full)](./README.ko.md)
