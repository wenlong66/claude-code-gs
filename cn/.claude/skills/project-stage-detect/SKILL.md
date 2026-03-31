---
name: project-stage-detect
description: "自动分析项目状态、检测阶段、识别差距并基于现有产物推荐下一步骤。"
argument-hint: "[optional: role filter like 'programmer' or 'designer']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash
---

# 项目阶段检测

此技能扫描你的项目以确定其当前开发阶段、产物的完整性和需要关注的差距。在以下情况下特别有用：
- 从现有项目开始
- 加入代码库
- 在里程碑前检查缺少什么
- 了解"我们在哪里？"

---

## 工作流程

### 1. 扫描关键目录

分析项目结构和内容：

**设计文档**（`design/`）：
- 统计 `design/gdd/*.md` 中的 GDD 文件
- 检查 game-concept.md、game-pillars.md、systems-index.md 是否存在
- 如果 systems-index.md 存在，统计总系统数 vs. 已设计系统数
- 分析完整性（概述、详细设计、边缘情况等）
- 统计 `design/narrative/` 中的叙事文档
- 统计 `design/levels/` 中的关卡设计

**源代码**（`src/`）：
- 统计源文件（与语言无关）
- 识别主要系统（5+ 文件的目录）
- 检查 core/、gameplay/、ai/、networking/、ui/ 目录
- 估算代码行数（粗略规模）

**生产产物**（`production/`）：
- 检查活动冲刺计划
- 查找里程碑定义
- 找到路线图文档

**原型**（`prototypes/`）：
- 统计原型目录
- 检查 README（已记录 vs 未记录）
- 评估原型是归档还是活动

**架构文档**（`docs/architecture/`）：
- 统计 ADR（架构决策记录）
- 检查概述/索引文档

**测试**（`tests/`）：
- 统计测试文件
- 估算测试覆盖率（粗略启发式）

### 2. 分类项目阶段

基于扫描的产物，确定阶段。首先检查 `production/stage.txt` —
