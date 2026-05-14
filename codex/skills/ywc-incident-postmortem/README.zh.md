<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-incident-postmortem

一个用于在生产事故后撰写结构化事故复盘报告的 skill。
涵盖时间线重建、根因分析（5 个为什么）、影响评估、
预防行动项，以及可选的经过脱敏处理的客户端报告。

## 使用时机

| 情况 | 示例 |
|------|------|
| 服务中断 | DB 连接失败、部署后服务器宕机、CDN 中断 |
| 安全事故 | API 密钥泄露、认证绕过、可疑访问 |
| 数据丢失或损坏 | 迁移失败、误删除 |
| 支付错误 | 重复扣款、支付失败循环 |
| 突发性能下降 | 部署后响应时间飙升 |

## 使用方法

```
/ywc-incident-postmortem             # 交互式草稿模式（默认）
/ywc-incident-postmortem --template  # 输出空白模板供填写
/ywc-incident-postmortem --client    # 同时生成脱敏的客户端报告
```

## 输出

- **内部复盘** — 完整技术文档：时间线、5 个为什么、行动项
- **客户报告**（使用 `--client`）— 不含内部细节的用户影响摘要

## 相关 Skills

- `ywc-security-audit` — 在事故*发生前*主动进行安全审计
- `ywc-impl-review` — 通用代码质量审查
- `ywc-changelog-release-notes` — 补丁发布后记录更改
