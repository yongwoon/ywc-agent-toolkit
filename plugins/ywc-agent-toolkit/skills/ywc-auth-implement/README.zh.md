# ywc-auth-implement

这是一个 Codex 编排技能：将认证需求转换为受策略、安审和 E2E 门禁约束的实施路线。它不会输出密钥，也不会建议手写 JWT、密码或密钥加密逻辑。

## 适用场景

- 规划登录、OAuth、会话或账户删除
- 决定现有认证是 `new`、`extend` 还是 `migrate`
- 根据项目证据选择成熟的认证库或托管服务

## 调用

```text
$ywc-auth-implement
```

技能先完成只读预检和九部分策略访谈，然后只打印以下路线，不会自动执行任务生成：

```text
$ywc-plan → $ywc-spec-ready → $ywc-task-generator → $ywc-code-gen --spec <path> --feature <auth feature> --tdd --review
```

出现 Critical/High 审计结果时，会跳过 E2E、PR 建议和缓存。法律文案始终标记为 `법적 검토 전 임시본`。
