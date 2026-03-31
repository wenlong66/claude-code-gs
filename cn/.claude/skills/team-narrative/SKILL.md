---
name: team-narrative
description: "协调叙事团队：协调 narrative-director、writer、world-builder 和 level-designer 创建内聚的故事内容、世界设定和叙事驱动的关卡设计。"
argument-hint: "[narrative content description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion, TodoWrite
---
当此技能被调用时，通过结构化管线协调叙事团队。

**决策点：** 在每个阶段转换时，使用 `AskUserQuestion` 向用户呈现子智能体的提议作为可选选项。在对话中写满智能体的完整分析，然后用简洁的标签捕获决策。在进入下一阶段之前，用户必须批准。

## 团队组成
- **narrative-director** — 故事弧线、角色设计、对话策略、叙事愿景
- **writer** — 对话写作、 lore 条目、物品描述、游戏内文本
- **world-builder** — 世界规则、派系设计、历史、地理、环境叙事
- **level-designer** — 为叙事服务的关卡布局、节奏、环境叙事节拍

## 如何委托

使用 Task 工具将每个团队成员作为子智能体生成：
- `subagent_type: narrative-director` — 故事弧线、角色设计、叙事愿景
- `subagent_type: writer` — 对话写作、 lore 条目、游戏内文本
- `subagent_type: world-builder` — 世界规则、派系设计、历史、地理
- `subagent_type: level-designer` — 为叙事服务的关卡布局、节奏

始终在每个智能体的提示中提供完整上下文（叙事简报、 lore 依赖、角色档案）。在管线允许的地方并行启动独立智能体（例如，阶段 2 智能体可以同时运行）。

## 管线

### 阶段 1：叙事方向
委托给 **narrative-director**：
- 定义此内容的叙事目的：它服务于什么故事节拍？
- 识别涉及的角色、他们的动机以及这如何契合整体弧线
- 设定情感基调和平稳目标
- 指定任何 lore 依赖或这引入的新 lore
- 输出：带故事需求的叙事简报

### 阶段 2：世界基础（并行）
并行委托：
- **world-builder**：为此内容创建或更新相关的派系、地点和历史的 lore 条目。交叉引用现有 lore 以发现矛盾。设置新条目的规范级别。
- **writer**：使用角色档案起草角色对话。确保所有行不超过 120 个字符，使用命名占位符表示变量，并支持本地化。

### 阶段 3：关卡叙事整合
委托给 **level-designer**：
- 审查叙事简报和 lore 基础
- 在关卡中设计环境叙事元素
- 放置叙事触发器、对话区域和发现点
- 确保节奏同时服务于游戏玩法和故事

### 阶段 4：审查和一致性
委托给 **narrative-director**：
- 根据角色声音档案审查所有对话
- 验证新条目和现有条目之间的 lore 一致性
- 确认叙事节奏与关卡设计一致
- 检查所有谜题都有记录在案的"正确答案"

### 阶段 5：打磨
