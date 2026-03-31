---
name: hotfix
description: "紧急修复工作流程，绕过正常冲刺流程并提供完整审计跟踪。创建热修复分支、跟踪批准并确保正确反向移植修复。"
argument-hint: "[bug-id or description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---
当此技能被调用时：

> **仅显式调用**：此技能只应在用户显式使用 `/hotfix` 请求时运行。不要基于上下文匹配自动调用。

1. **评估紧急程度** — 读取缺陷描述或 ID。确定严重性：
   - **S1（严重）**：游戏无法游玩、数据丢失、安全漏洞 — 立即热修复
   - **S2（主要）**：重要功能破损、有变通方法 — 24 小时内热修复
   - 如果严重性是 S3 或更低，建议改用正常缺陷修复工作流程

2. **在 `production/hotfixes/hotfix-[date]-[short-name].md` 创建热修复记录**：

   ```markdown
   ## 热修复：[简短描述]
   日期：[日期]
   严重性：[S1/S2]
   报告人：[发现者]
   状态：进行中

   ### 问题
   [清楚描述什么破损了以及对玩家的影响]

   ### 根本原因
   [在调查期间填写]

   ### 修复
   [在实施期间填写]

   ### 测试
   [测试了什么以及如何测试]

   ### 批准
   - [ ] 修复由 lead-programmer 审查
   - [ ] 回归测试通过（qa-tester）
   - [ ] 发布批准（producer）

   ### 回滚计划
   [如果修复导致新问题如何回滚]
   ```

3. **创建热修复分支**（如果 git 已初始化）：
   ```
   git checkout -b hotfix/[short-name] [release-tag-or-main]
   ```

4. **调查并实施修复** — 专注于解决该问题的最小更改。不要在热修复旁边进行重构、清理或添加功能。

5. **验证修复** — 对受影响的系统运行针对性测试。检查相邻系统的回归。

6. **使用根本原因、修复详情和测试结果更新热修复记录**。

6b. **收集批准** — 使用 Task 工具请求签字：
   - `subagent_type: lead-programmer` — 审查修复的正确性和副作用
   - `subagent_type: qa-tester` — 对受影响的系统运行针对性回归测试
