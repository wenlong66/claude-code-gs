# Claude Code 游戏工作室 -- 游戏工作室智能体架构

通过 48 个协调的 Claude Code 子智能体管理独立游戏开发。
每个智能体拥有特定领域，强调关注点分离和质量。

## 技术栈

- **引擎**：[选择：Godot 4 / Unity / Unreal Engine 5]
- **语言**：[选择：GDScript / C# / C++ / Blueprint]
- **版本控制**：基于主干开发的 Git
- **构建系统**：[选择引擎后指定]
- **资产管道**：[选择引擎后指定]

> **注意**：针对 Godot、Unity 和 Unreal 存在引擎专家智能体，以及专门的子专家。使用与你引擎匹配的集合。

## 项目结构

@.claude/docs/directory-structure.md

## 引擎版本参考

@docs/engine-reference/godot/VERSION.md

## 技术偏好

@.claude/docs/technical-preferences.md

## 协调规则

@.claude/docs/coordination-rules.md

## 协作协议

**用户驱动的协作，而非自主执行。**
每个任务都遵循：**提问 -> 选项 -> 决策 -> 草案 -> 批准**

- 智能体必须在请求批准前展示草案或摘要
- 未经用户指示不提交

参见 `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md` 了解完整协议和示例。

> **首次会话？** 如果项目没有配置引擎且没有游戏概念，运行 `/start` 开始引导式入职流程。

## 编码标准

@.claude/docs/coding-standards.md

## 上下文管理

@.claude/docs/context-management.md
