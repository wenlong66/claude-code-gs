---
name: reverse-document
description: "从现有实现生成设计或架构文档。从代码/原型逆向工作以创建缺失的计划文档。"
argument-hint: "<type> <path> (例如 'design src/gameplay/combat' 或 'architecture src/core')"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# 逆向文档

此技能分析现有实现（代码、原型、系统）并生成适当的设计或架构文档。在以下情况下使用此技能：
- 你构建了一个功能但没有先编写设计文档
- 你继承了一个没有文档的代码库
- 你原型化了一个机制并需要将其正式化
- 你需要记录现有代码背后的"为什么"

---

## 工作流程

### 1. 解析参数

**格式**：`/reverse-document <type> <path>`

**类型选项**：
- `design` → 生成游戏设计文档（GDD 部分）
- `architecture` → 生成架构决策记录（ADR）
- `concept` → 从原型生成概念文档

**路径**：要分析的目录或文件
- `src/gameplay/combat/` → 所有战斗相关代码
- `src/core/event-system.cpp` → 特定文件
- `prototypes/stealth-mech/` → 原型目录

**示例**：
```bash
/reverse-document design src/gameplay/magic-system
/reverse-document architecture src/core/entity-component
/reverse-document concept prototypes/vehicle-combat
```

### 2. 分析实现

**阅读并理解代码/原型**：

**对于设计文档（GDD）：**
- 识别机制、规则、公式
- 提取游戏玩法值（伤害、冷却时间、范围）
- 找到状态机、能力系统、进度
- 检测代码中处理的边缘情况
- 映射依赖关系（哪些系统交互？）

**对于架构文档（ADR）：**
- 识别模式（ECS、单例、观察者等）
- 理解技术决策（线程化、序列化等）
- 映射依赖关系和耦合
- 评估性能特征
- 找到约束和权衡
