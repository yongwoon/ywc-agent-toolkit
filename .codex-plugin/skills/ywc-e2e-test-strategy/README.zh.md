<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-e2e-test-strategy

一个使用 Playwright 设计和实现自动化 E2E 测试策略的 skill。处理新项目 Playwright 配置、现有覆盖率差距分析、单个用户流程测试生成以及 GitHub Actions CI 集成。

## 使用场景

- **新项目**："配置 Playwright"、"首次添加 E2E 测试"
- **现有项目审计**："查找关键路径覆盖缺口"、"检查 E2E 差距"
- **单个流程**："为登录流程编写 Playwright 测试"、"生成结账 E2E 测试"
- **CI 集成**："将 Playwright 接入 GitHub Actions"

## 使用方法

```bash
/ywc-e2e-test-strategy --init           # 从头配置 Playwright
/ywc-e2e-test-strategy --audit          # 审计现有 E2E 覆盖率
/ywc-e2e-test-strategy --flow login     # 为特定流程生成测试
/ywc-e2e-test-strategy --init --ci      # 初始化 + GitHub Actions 工作流
```

或使用自然语言调用：

> "使用 Playwright 设计 E2E 测试策略"
> "自动化关键用户路径"
> "审计我的 E2E 覆盖率"

## 模式

| 模式 | 标志 | 使用时机 |
|------|------|---------|
| Init | `--init` | 未找到 `playwright.config.*` |
| Audit | `--audit` | 已有 E2E 测试存在 |
| Flow | `--flow <name>` | 添加单个用户流程测试 |

不带标志时，skill 自动从文件系统检测模式。

## 输出

- `playwright.config.ts` — 基于环境变量的 baseURL 配置
- `e2e/*.spec.ts` — 按关键路径划分的测试文件
- `.github/workflows/e2e.yml` — CI 工作流（`--ci` 或 `--init`）
- 审计报告 — 覆盖率差距和不稳定测试风险分析

## 相关 Skills

- `ywc-gen-testcase` — 手动验证测试表（人工验证，非自动化）
- `ywc-impl-review` — 代码级实现审查
- `ywc-security-audit` — 认证和输入处理流程的安全审计
