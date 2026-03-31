---
name: team-combat
description: "协调战斗团队：协调 game-designer、gameplay-programmer、ai-programmer、technical-artist、sound-designer 和 qa-tester 端到端设计、实现和验证战斗功能。"
argument-hint: "[combat feature description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---
当此技能被调用时，通过结构化管线协调战斗团队。

**决策点：** 在每个阶段转换时，使用 `AskUserQuestion` 向用户呈现子智能体的提议作为可选选项。在对话中写满智能体的完整分析，然后用简洁的标签捕获决策。在进入下一阶段之前，用户必须批准。

## 团队组成
- **game-designer** — 设计机制、定义公式和边缘情况
- **gameplay-programmer** — 实现核心游戏玩法代码
- **ai-programmer** — 为功能实现 NPC/敌人 AI 行为
- **technical-artist** — 创建 VFX、着色器效果和视觉反馈
- **sound-designer** — 定义音频事件、打击声音和环境战斗音频
- **qa-tester** — 编写测试用例并验证实现

## 如何委托

使用 Task 工具将每个团队成员作为子智能体生成：
- `subagent_type: game-designer` — 设计机制、定义公式和边缘情况
- `subagent_type: gameplay-programmer` — 实现核心游戏玩法代码
- `subagent_type: ai-programmer` — 实现 AI 行为
- `subagent_type: technical-artist` — 创建 VFX、着色器效果、视觉反馈
- `subagent_type: sound-designer` — 定义音频事件、打击声音、环境音频
- `subagent_type: qa-tester` — 编写测试用例并验证实现

始终在每个智能体的提示中提供完整上下文（设计文档路径、相关代码文件、约束）。在管线允许的地方并行启动独立智能体（例如，阶段 3 智能体可以同时运行）。

## 管线

### 阶段 1：设计
委托给 **game-designer**：
- 在 `design/gdd/` 中创建或更新涵盖以下内容的设计文档：机制概述、玩家幻想、详细规则、带变量定义的公式、边缘情况、依赖关系、带安全范围的调优旋钮和验收标准
- 输出：已完成的设计文档

### 阶段 2：架构
委托给 **gameplay-programmer**（如果涉及 AI 则加上 **ai-programmer**）：
- 审查设计文档
- 设计代码架构：类结构、接口、数据流
- 识别与现有系统的集成点
- 输出：带文件列表和接口定义的架构草图

### 阶段 3：实现（可能并行）
并行委托：
- **gameplay-programmer**：实现核心战斗机制代码
- **ai-programmer**：实现 AI 行为（如果功能涉及 NPC 反应）
- **technical-artist**：创建 VFX 和着色器效果
- **sound-designer**：定义音频事件列表和混音备注

### 阶段 4：集成
- 连接游戏代码、AI、VFX 和音频
- 确保所有调优旋钮都已暴露且数据驱动
- 验证功能与现有战斗系统配合工作
