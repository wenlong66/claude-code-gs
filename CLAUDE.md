# Claude Code Game Studios —— 游戏工作室代理架构

通过 48 个协同工作的 Claude Code 子代理来管理独立游戏开发。
每个代理负责一个特定领域，以确保关注点分离和质量控制。

## 技术栈

- **引擎**：[选择：Godot 4 / Unity / Unreal Engine 5]
- **语言**：[选择：GDScript / C# / C++ / Blueprint]
- **版本控制**：基于主干开发（trunk-based development）的 Git
- **构建系统**：[选择引擎后再指定]
- **资源流水线**：[选择引擎后再指定]

> **注意**：已为 Godot、Unity 和 Unreal 提供引擎专项代理及其专属子专家代理。
> 请使用与你所选引擎匹配的那一组代理。

## 项目结构

@.claude/docs/directory-structure.md

## 引擎版本参考

@docs/engine-reference/godot/VERSION.md

## 技术偏好

@.claude/docs/technical-preferences.md

## 协调规则

@.claude/docs/coordination-rules.md

## 协作协议

**由用户驱动的协作，而非自主执行。**
每个任务都遵循：**提问 -> 选项 -> 决策 -> 草案 -> 批准**

- 代理在使用 Write/Edit 工具前，必须先询问：“我可以将其写入 [filepath] 吗？”
- 代理在请求批准前，必须先展示草案或摘要
- 涉及多文件变更时，必须对完整变更集获得明确批准
- 未经用户指示不得提交（commit）

完整协议与示例见 `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`。

> **First session?** 如果项目尚未配置引擎且没有游戏概念，
> 请运行 `/start` 开始引导式初始化流程。

## 编码标准

@.claude/docs/coding-standards.md

## 上下文管理

@.claude/docs/context-management.md
