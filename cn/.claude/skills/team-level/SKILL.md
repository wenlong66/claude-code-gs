---
name: team-level
description: "协调关卡设计团队：level-designer + narrative-director + world-builder + art-director + systems-designer + qa-tester 完成完整区域/关卡创作。"
argument-hint: "[level name or area to design]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---

当此技能被调用时：

**决策点：** 在每个步骤转换时，使用 `AskUserQuestion` 向用户呈现子智能体的提议作为可选选项。在对话中写满智能体的完整分析，然后用简洁的标签捕获决策。在进入下一步之前，用户必须批准。

1. **读取参数** 获取目标关卡或区域（例如 `tutorial`、`forest dungeon`、`hub town`、`final boss arena`）。

2. **收集上下文**：
   - 阅读 `design/gdd/game-concept.md` 中的游戏概念
   - 阅读 `design/gdd/game-pillars.md` 中的游戏支柱
   - 阅读 `design/levels/` 中的现有关卡文档
   - 阅读 `design/narrative/` 中的相关叙事文档
   - 阅读该区域/派系的世界构建文档

## 如何委托

使用 Task 工具将每个团队成员作为子智能体生成：
- `subagent_type: narrative-director` — 叙事目的、角色、情感弧线
- `subagent_type: world-builder` — lore 上下文、环境叙事、世界规则
- `subagent_type: level-designer` — 空间布局、节奏、遭遇、导航
- `subagent_type: systems-designer` — 敌人组成、战利品表、难度平衡
- `subagent_type: art-director` — 视觉主题、配色方案、灯光、资源需求
- `subagent_type: qa-tester` — 测试用例、边界测试、游玩测试清单

始终在每个智能体的提示中提供完整上下文（游戏概念、支柱、现有关卡文档、叙事文档）。

3. **按顺序协调关卡设计团队**：

### 步骤 1：叙事上下文（narrative-director + world-builder）
生成 `narrative-director` 智能体以：
- 定义此区域的叙事目的（这里发生什么故事节拍？）
- 识别关键角色、对话触发器和 lore 元素
- 指定情感弧线（玩家进入、期间、离开时应该有什么感觉？）

生成 `world-builder` 智能体以：
- 提供该区域的 lore 上下文（历史、派系存在、生态）
- 定义环境叙事机会
- 指定影响该区域游戏玩法的任何世界规则

### 步骤 2：布局和遭遇设计（level-designer）
生成 `level-designer` 智能体以：
- 设计空间布局（关键路径、可选路径、秘密）
- 定义节奏曲线（紧张峰值、休息区、探索区）
- 放置难度递进的遭遇
- 设计环境谜题或导航挑战
- 定义兴趣点和地标以助寻路
- 指定入口/出口点和相邻区域的连接

### 步骤 3：系统集成（systems-designer）
