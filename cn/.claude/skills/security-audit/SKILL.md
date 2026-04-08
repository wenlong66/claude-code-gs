---
name: security-audit
description: "审计游戏中的安全漏洞：存档篡改、作弊向量、网络利用、数据暴露和输入验证缺口。生成优先级明确的安全报告并附带修复指导。建议在任何公开发布或多人游戏上线前运行。"
argument-hint: "[full | network | save | input | quick]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, Task
agent: security-engineer
---

# Security Audit

安全不是任何已发售游戏中的可选项。即使是单机游戏，也存在存档篡改向量。多人游戏还存在作弊面、数据暴露风险以及拒绝服务潜力。这个技能会系统性地审计代码库中最常见的游戏安全失败，并给出优先级明确的修复计划。

**运行这个技能：**
- 在任何公开发布之前（Polish → Release gate 的必需项）
- 在启用任何在线/多人功能之前
- 在实现任何读取磁盘或网络的系统之后
- 当收到安全相关 bug 报告时

**输出：** `production/security/security-audit-[date].md`

---

## 第 1 阶段：解析参数和范围

**模式：**
- `full` —— 所有类别（发布前推荐）
- `network` —— 仅网络/多人
- `save` —— 仅存档文件和序列化
- `input` —— 仅输入验证和注入
- `quick` —— 仅高严重度检查（最快，适合迭代使用）
- 无参数 —— 运行 `full`

读取 `.claude/docs/technical-preferences.md` 以确定：
- 引擎和语言（影响要搜索哪些模式）
- 目标平台（影响适用哪些攻击面）
- 是否将多人/网络功能纳入范围

---

## 第 2 阶段：spawn Security Engineer

通过 Task spawn `security-engineer`。传入：
- 审计范围/模式
- technical preferences 中的引擎和语言
- 所有源目录的清单：`src/`、`assets/data/`、任何配置文件

security-engineer 会跨 6 个类别运行审计（见 Phase 3）。在继续之前，收集其完整发现。

---

## 第 3 阶段：审计类别

security-engineer 会评估以下各项。跳过与项目范围无关的类别。

### 类别 1：存档文件和序列化安全
- 载入存档前是否进行了验证？（不是盲目反序列化）
- 存档路径是否由用户输入拼接？（路径遍历风险）
- 存档是否经过校验和或签名？（篡改检测）
- 游戏是否在未做边界检查的情况下信任存档中的数值？
- 在存档加载附近是否存在 eval() 或动态代码执行调用？

Grep 模式：`File.open`、`load`、`deserialize`、`JSON.parse`、`from_json`、`read_file` —— 逐个检查其是否有验证。

### 类别 2：网络和多人安全（如果是纯单机则跳过）
- 游戏状态是否由服务器权威，还是客户端决定结果？
- 入站网络包是否按大小、类型和数值范围进行验证？
- 玩家位置和状态变更是否在服务器端验证？
- 对任何网络调用是否有速率限制？
- 认证 token 是否正确处理（绝不明文发送）？
- 游戏是否在 release build 中暴露了任何调试端点？

Grep：`recv`、`receive`、`PacketPeer`、`socket`、`NetworkedMultiplayerPeer`、`rpc`、`rpc_id` —— 检查每个调用点是否有验证。

### 类别 3：输入验证
- 是否有玩家提供的字符串被用于文件路径？（路径遍历）
- 是否有玩家提供的字符串在未清理的情况下写入日志？（日志注入）
- 数值输入（例如物品数量、角色属性）在使用前是否做了范围检查？
- 成就/统计数值在写入任何后端前是否经过检查？

Grep：`get_input`、`Input.get_`、`input_map`、用户可见文本字段 —— 检查验证。

### 类别 4：数据暴露
- `src/` 或 `assets/` 中是否硬编码了 API key、凭据或 secret？
- release build 中是否包含调试符号或过于详细的错误信息？
- 游戏是否把敏感玩家数据记录到磁盘或控制台？
- 是否向玩家暴露了内部文件路径或系统信息？

Grep：`api_key`、`secret`、`password`、`token`、`private_key`、`DEBUG`、`print(` 在面向 release 的代码中。

### 类别 5：作弊和反篡改向量
- 关键玩法数值是否只保存在内存中，而不是易编辑文件里？
- 是否有任何关键进度标志（例如“已购买 DLC”）在服务器端验证？
- 对于多人游戏，是否有防止内存编辑工具（如 Cheat Engine）的方法？
- 排行榜/分数提交在接受前是否经过验证？

注意：客户端反作弊大体上无法强制执行。重点放在任何竞技或变现内容的服务器端验证上。

### 类别 6：依赖和供应链
- 是否使用了第三方插件或库？把它们列出来。
- 这些插件版本是否存在已知 CVE？
- 插件来源是否经过验证（官方商店、审查过的仓库）？

Glob：`addons/`、`plugins/`、`third_party/`、`vendor/` —— 列出所有外部依赖。

---

## 第 4 阶段：分类发现

对每条发现指定：

**Severity：**
| Level | Definition |
|-------|-----------|
| **CRITICAL** | 远程代码执行、数据泄露，或可轻易利用并破坏多人完整性的作弊漏洞 |
| **HIGH** | 绕过进度的存档篡改、凭据暴露，或绕过服务器权威 |
| **MEDIUM** | 客户端作弊启用、信息泄露，或影响有限的输入验证缺口 |
| **LOW** | Defense-in-depth 改进——可降低攻击面，但没有直接可利用漏洞 |

**Status：** Open / Accepted Risk / Out of Scope

---

## 第 5 阶段：生成报告

```markdown
# Security Audit Report

**Date**: [date]
**Scope**: [full | network | save | input | quick]
**Engine**: [engine + version]
**Audited by**: security-engineer via /security-audit
**Files scanned**: [N source files, N config files]

---

## Executive Summary

| Severity | Count | Must Fix Before Release |
|----------|-------|------------------------|
| CRITICAL | [N] | Yes — all |
| HIGH | [N] | Yes — all |
| MEDIUM | [N] | Recommended |
| LOW | [N] | Optional |

**Release recommendation**: [CLEAR TO SHIP / FIX CRITICALS FIRST / DO NOT SHIP]

---

## CRITICAL Findings

### SEC-001: [Title]
**Category**: [Save / Network / Input / Data / Cheat / Dependency]
**File**: `[path]` line [N]
**Description**: [What the vulnerability is]
**Attack scenario**: [How a malicious user would exploit it]
**Remediation**: [Specific code change or pattern to apply]
**Effort**: [Low / Medium / High]

[repeat per finding]

---

## HIGH Findings

[same format]

---

## MEDIUM Findings

[same format]

---

## LOW Findings

[same format]

---

## Accepted Risk

[Any findings explicitly accepted by the team with rationale]

---

## Dependency Inventory

| Plugin / Library | Version | Source | Known CVEs |
|-----------------|---------|--------|------------|
| [name] | [version] | [source] | [none / CVE-XXXX-NNNN] |

---

## Remediation Priority Order

1. [SEC-NNN] — [1-line description] — Est. effort: [Low/Medium/High]
2. ...

---

## Re-Audit Trigger

Run `/security-audit` again after remediating any CRITICAL or HIGH findings.
The Polish → Release gate requires this report with no open CRITICAL or HIGH items.
```

---

## 第 6 阶段：写报告

先在对话中展示报告摘要（Executive Summary + CRITICAL/HIGH findings only）。

询问："May I write the full security audit report to `production/security/security-audit-[date].md`?"

只有在获得批准后才写入。

---

## 第 7 阶段：门控集成

该报告是 **Polish → Release gate** 的必需产物。

修复发现后，再运行：`/security-audit quick`，确认 CRITICAL/HIGH 项已解决，然后再运行 `/gate-check release`。

如果存在 CRITICAL findings：
> "⛔ CRITICAL security findings must be resolved before any public release. Do not proceed to `/launch-checklist` until these are addressed."

如果没有 CRITICAL/HIGH findings：
> "✅ No blocking security findings. Report written to `production/security/`. Include this path when running `/gate-check release`."

---

## 协作协议

- **不要假定某个模式是安全的**——把它标出来，让用户决定
- **Accepted risk 是合法结果**——对于 solo team，某些 LOW findings 可以接受；要记录决定
- **多人游戏门槛更高**——多人场景中的任何 HIGH finding 都应视为 CRITICAL
- **这不是渗透测试**——该审计覆盖常见模式；在任何竞技或变现的多人上线前，仍建议由人类安全专业人士做一次真实 pentest
