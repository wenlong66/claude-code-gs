---
name: changelog
description: "从 git 提交、冲刺数据和设计文档自动生成变更日志。生成内部和面向玩家的版本。"
argument-hint: "[version|sprint-number]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash
context: |
  !git log --oneline -30 2>/dev/null
  !git tag --list --sort=-v:refname 2>/dev/null | head -5
---

当此技能被调用时：

1. **读取目标版本或冲刺编号的参数**。如果给定了版本，使用相应的 git 标签。如果给定了冲刺编号，使用冲刺日期范围。

1b. **检查 git 可用性** — 验证仓库是否已初始化：
   - 运行 `git rev-parse --is-inside-work-tree` 确认 git 可用
   - 如果不是 git 仓库，通知用户并正常中止

2. **读取自上一个标签或发布以来的 git log**：
   ```
   git log --oneline [last-tag]..HEAD
   ```
   如果没有标签，读取完整日志或合理的最近范围（最近 100 次提交）。

3. **读取相关时期的冲刺报告**从 `production/sprints/` 以了解计划工作和变更背后的上下文。

4. **读取此期间实现的新功能的已完成设计文档**从 `design/gdd/`。

5. **将每个变更分类到以下类别之一**：
   - **新功能**：全新的游戏系统、模式或内容
   - **改进**：现有功能的增强、UX 改进、性能提升
   - **缺陷修复**：破损行为的修正
   - **平衡变更**：游戏玩法值、难度、经济的调整
   - **已知问题**：团队知道但尚未解决的问题

6. **生成内部变更日志**（完整技术细节）：

```markdown
# 内部变更日志：[版本]
日期：[日期]
冲刺：涵盖的冲刺编号
提交：[计数]（[first-hash]..[last-hash]）

## 新功能
- [功能名称] -- [技术描述、受影响的系统]
  - 提交：[hash1]、[hash2]
  - 负责人：[实现者]
  - 设计文档：[适用则链接]

## 改进
- [改进] -- [技术上的变更和原因]
  - 提交：[哈希]
  - 负责人：[谁]
```
