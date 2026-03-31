# 游戏工作室智能体架构 -- 快速入门指南

## 这是什么？

这是一套完整的游戏开发 Claude Code 智能体架构。它将 48 个专业 AI 智能体组织成工作室层级结构，模拟真实游戏开发团队，具有明确定义的职责、委托规则和协调协议。它包括 Godot、Unity 和 Unreal 的引擎专家智能体——每个引擎都有针对主要引擎子系统的专业子智能体。所有设计智能体和模板都基于成熟的游戏设计理论（MDA 框架、自我决定理论、心流状态、巴特尔玩家类型）。使用与项目匹配的引擎集。

## 如何使用

### 1. 了解层级结构

智能体分为三个层级：

- **层级 1（Opus）**：做出高层决策的总监
  - `creative-director` -- 愿景和创意冲突解决
  - `technical-director` -- 架构和技术决策
  - `producer` -- 进度、协调和风险管理

- **层级 2（Sonnet）**：拥有各自领域的部门负责人
  - `game-designer`、`lead-programmer`、`art-director`、`audio-director`、
    `narrative-director`、`qa-lead`、`release-manager`、`localization-lead`

- **层级 3（Sonnet/Haiku）**：在各自领域执行的专业人员
  - 设计师、程序员、艺术家、作家、测试员、工程师

### 2. 为任务选择正确的智能体

问自己："在真实工作室中哪个部门会处理这个？"

| 我需要... | 使用这个智能体 |
|-------------|---------------|
| 设计新机制 | `game-designer` |
| 编写战斗代码 | `gameplay-programmer` |
| 创建着色器 | `technical-artist` |
| 写对话 | `writer` |
| 计划下一个冲刺 | `producer` |
| 审查代码质量 | `lead-programmer` |
| 编写测试用例 | `qa-tester` |
| 设计关卡 | `level-designer` |
| 修复性能问题 | `performance-analyst` |
| 设置 CI/CD | `devops-engineer` |
| 设计战利品表 | `economy-designer` |
| 解决创意冲突 | `creative-director` |
| 做架构决策 | `technical-director` |
| 管理发布 | `release-manager` |
| 准备翻译字符串 | `localization-lead` |
| 快速测试机制想法 | `prototyper` |
| 审查安全问题 | `security-engineer` |
| 检查可访问性合规性 | `accessibility-specialist` |
| 获取 Unreal Engine 建议 | `unreal-specialist` |
| 获取 Unity 建议 | `unity-specialist` |
| 获取 Godot 建议 | `godot-specialist` |
| 设计 GAS 能力/效果 | `ue-gas-specialist` |
| 定义 BP/C++ 边界 | `ue-blueprint-specialist` |
| 实现 UE 复制 | `ue-replication-specialist` |
| 构建 UMG/CommonUI 小部件 | `ue-umg-specialist` |
| 设计 DOTS/ECS 架构 | `unity-dots-specialist` |
| 编写 Unity 着色器/VFX | `unity-shader-specialist` |
| 管理 Addressable 资源 | `unity-addressables-specialist` |
| 构建 UI Toolkit/UGUI 屏幕 | `unity-ui-specialist` |
| 编写惯用 GDScript | `godot-gdscript-specialist` |
| 创建 Godot 着色器 | `godot-shader-specialist` |
| 构建 GDExtension 模块 | `godot-gdextension-specialist` |
| 规划直播活动和赛季 | `live-ops-designer` |
| 为玩家撰写补丁说明 | `community-manager` |
| 集思广益新游戏想法 | 使用 `/brainstorm` 技能 |

### 3. 使用斜杠命令执行常见任务

| 命令 | 功能 |
|---------|-------------|
| `/start` | 首次入职 -- 询问你处于什么阶段，引导你到正确的工作流程 |
| `/design-review` | 审查设计文档 |
| `/code-review` | 审查代码质量和架构 |
