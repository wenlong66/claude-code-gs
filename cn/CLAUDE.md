# Claude Code Game Studios -- 游戏工作室智能体架构

通过 48 个协调的 Claude Code 子智能体管理独立游戏开发。
每个智能体都拥有特定领域，强调职责分离和质量控制。

## 技术栈

- **引擎**：[选择：Godot 4 / Unity / Unreal Engine 5]
- **语言**：[选择：GDScript / C# / C++ / Blueprint]
- **版本控制**：使用 trunk-based development 的 Git
- **构建系统**：[选择引擎后指定]
- **资源管线**：[选择引擎后指定]

> **注意**：Godot、Unity 和 Unreal 都有对应的引擎专用智能体，以及专门的子专业人员。请使用与你所选引擎匹配的那一组。

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

- 智能体在使用 Write/Edit 工具前必须询问“我可以把它写到 [filepath] 吗？”
- 智能体在请求批准前必须先展示草案或摘要
- 多文件更改需要对完整变更集明确批准
- 未经用户指示，不提交任何内容

参见 `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md` 了解完整协议和示例。

> **首次会话？** 如果项目尚未配置引擎，且还没有游戏概念，请运行 `/start` 进入引导式入门流程。

## 编码标准

@.claude/docs/coding-standards.md

## 上下文管理

@.claude/docs/context-management.md
