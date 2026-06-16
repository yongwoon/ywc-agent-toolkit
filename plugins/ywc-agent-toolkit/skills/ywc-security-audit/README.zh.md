<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-security-audit

一个安全代理 Skill，用于在身份验证、支付或个人数据相关代码发生变更时执行安全审计，或用于定期安全审查。

## 使用方法

```text
/ywc-security-audit --code api/src/middleware/
```

## 审计检查清单（OWASP Top 10）

1. 注入（SQL、命令、LDAP）
2. 身份验证失效（令牌、会话）
3. 敏感数据暴露
4. XSS（反射型、存储型、DOM 型）
5. 访问控制失效
6. 安全配置错误
7. SSRF
8. 输入验证
9. 速率限制
10. 时序攻击

## 执行代理

- **Security Agent**（claude-opus-4-20250514）

## 推荐使用场景

- 修改 middleware/（身份验证/授权逻辑）时
- 添加或修改接受外部输入的 API 端点时
- 定期安全审查（如每月）

## 输出格式

按严重程度分类：Critical / High / Medium / Low。每条发现包含文件:行号、风险描述和建议修复方案。

## 触发条件

此 Skill 的触发条件在 [SKILL.md](./SKILL.md) 的 `description` 字段中定义。

## 本地化版本

- [英语](./README.en.md)
- [日语](./README.ja.md)
- [韩语](./README.ko.md)
