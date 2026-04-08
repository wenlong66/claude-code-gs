---
name: create-control-manifest
description: "在 architecture 完成后，生成一份给程序员直接执行的扁平规则清单——你必须做什么、你绝不能做什么，按系统与层级组织。内容来自所有 Accepted ADR、技术偏好和引擎参考文档。比 ADR（解释为什么）更直接可执行。"
argument-hint: "[update — regenerate from current ADRs]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task
agent: technical-director
---

# Create Control Manifest

Control Manifest 是一份扁平、可执行的程序员规则清单。它回答的是“我该做什么？”以及“我绝对不能做什么？”——按架构层级组织，来源于所有 Accepted ADR、技术偏好和引擎参考文档。ADR 解释 *为什么*，manifest 告诉你 *做什么*。

**输出：**`docs/architecture/control-manifest.md`

**运行时机：**在 `/architecture-review` 通过且 ADR 处于 Accepted 状态之后。每当有新的 ADR 被接受或已有 ADR 被修订时，重新运行。

---

## 1. 加载所有输入

### ADR
- Glob `docs/architecture/adr-*.md` 并读取每个文件
- 仅筛选 Accepted ADR（Status: Accepted）——跳过 Proposed、Deprecated、Superseded
- 记录每条规则的 ADR 编号与标题来源

### Technical Preferences
- 读取 `.claude/docs/technical-preferences.md`
- 提取：命名约定、性能预算、已批准库/插件、禁止模式

### Engine Reference
- 读取 `docs/engine-reference/[engine]/VERSION.md` 获取引擎与版本
- 读取 `docs/engine-reference/[engine]/deprecated-apis.md`——这些会变成禁止 API 条目
- 如果存在，读取 `docs/engine-reference/[engine]/current-best-practices.md`

报告：`"Loaded [N] Accepted ADRs, engine: [name + version]."`

---

## 2. 从每个 ADR 提取规则

对每个 Accepted ADR，提取：

### 必需模式（来自 "Implementation Guidelines" 章节）
- 所有包含 “must”、“should”、“required to”、“always” 的语句
- 所有被强制要求的具体模式或做法

### 禁止做法（来自 "Alternatives Considered" 章节）
- 所有被明确否决的替代方案——*为什么* 被否决，会变成规则（“never use X because Y”）
- 任何明确指出的反模式

### 性能护栏（来自 "Performance Implications" 章节）
- 预算约束："max N ms per frame for this system"
- 内存限制："this system must not exceed N MB"

### 引擎 API 约束（来自 "Engine Compatibility" 章节）
- 需要验证的切后 API
- 与默认 LLM 假设不同的已验证行为
- 在钉定引擎版本中行为不同的 API 字段或方法

### 层级分类
按规则所管辖的架构层级进行分类：
- **Foundation**：场景管理、事件架构、存档/加载、引擎初始化
- **Core**：核心玩法循环、主玩家系统、物理/碰撞
- **Feature**：次级系统、次级机制、AI
- **Presentation**：渲染、音频、UI、VFX、着色器

如果某条 ADR 跨多个层级，就把规则复制到每个相关层级。

---

## 3. 添加全局规则

汇总适用于所有层级的规则：

### 来自 technical-preferences.md：
- 命名约定（classes、variables、signals/events、files、constants）
- 性能预算（target framerate、frame budget、draw call 限制、memory ceiling）

### 来自 deprecated-apis.md：
- 所有弃用 API → Forbidden API 条目

### 来自 current-best-practices.md（如果可用）：
- 引擎推荐模式 → Required 条目

### 来自 technical-preferences.md 的 forbidden patterns：
- 直接复制所有 “Forbidden Patterns” 条目

---

## 4. 在写入前呈现规则摘要

在写 manifest 之前，先向用户展示摘要：

```
## Control Manifest Preview
Engine: [name + version]
ADRs covered: [list ADR numbers]
Total rules extracted:
  - Foundation layer: [N] required, [M] forbidden, [P] guardrails
  - Core layer: [N] required, [M] forbidden, [P] guardrails
  - Feature layer: ...
  - Presentation layer: ...
  - Global: [N] naming conventions, [M] forbidden APIs, [P] approved libraries
```

询问："Does this look complete? Any rules to add or remove before I write the manifest?"

---

## 4b. Director Gate — Technical Review

**review mode 检查**——在 spawn TD-MANIFEST 前执行：
- `solo` → 跳过。注："TD-MANIFEST skipped — Solo mode." 进入阶段 5。
- `lean` → 跳过。注："TD-MANIFEST skipped — Lean mode." 进入阶段 5。
- `full` → 正常 spawn。

通过 Task 使用 gate **TD-MANIFEST**（见 `.claude/docs/director-gates.md`）spawn `technical-director`。

传入：阶段 4 的 Control Manifest Preview（每层规则计数、完整规则列表）、已覆盖的 ADR 列表、引擎版本，以及来自 technical-preferences.md 或引擎参考文档的所有规则来源。

由 technical-director 评审：
- 所有必需 ADR 模式是否都被捕获且表述准确
- 禁止做法是否完整且归因正确
- 是否添加了任何缺少来源 ADR 或偏好文档支撑的规则
- 性能护栏是否与 ADR 约束一致

应用 verdict：
- **APPROVE** → 进入阶段 5
- **CONCERNS** → 用 `AskUserQuestion` 呈现，选项：`Revise flagged rules` / `Accept and proceed` / `Discuss further`
- **REJECT** → 不写 manifest；修复被标记的规则并重新展示摘要

---

## 5. 写入 Control Manifest

询问："May I write this to `docs/architecture/control-manifest.md`?"

格式：

```markdown
# Control Manifest

> **Engine**: [name + version]
> **Last Updated**: [date]
> **Manifest Version**: [date]
> **ADRs Covered**: [ADR-NNNN, ADR-MMMM, ...]
> **Status**: [Active — regenerate with `/create-control-manifest update` when ADRs change]

`Manifest Version` 是该 manifest 生成的日期。story 文件创建时会嵌入这个日期。`/story-readiness` 会把 story 中嵌入的版本与此字段比较，以检测是否基于旧规则编写。它总是与 `Last Updated` 相同——日期相同，但分别服务于不同消费者。

此 manifest 是一份从所有 Accepted ADR、技术偏好和引擎参考文档中提取出的程序员速查表。每条规则的原因，请参见对应 ADR。

---

## Foundation Layer Rules

*适用于：scene 管理、事件架构、存档/加载、引擎初始化*

### Required Patterns
- **[rule]** — source: [ADR-NNNN]
- **[rule]** — source: [ADR-NNNN]

### Forbidden Approaches
- **Never [anti-pattern]** — [简短原因] — source: [ADR-NNNN]

### Performance Guardrails
- **[system]**: max [N]ms/frame — source: [ADR-NNNN]

---

## Core Layer Rules

*适用于：核心 gameplay loop、主玩家系统、physics、collision*

### Required Patterns
...

### Forbidden Approaches
...

### Performance Guardrails
...

---

## Feature Layer Rules

*适用于：次级机制、AI systems、secondary features*

### Required Patterns
...

### Forbidden Approaches
...

---

## Presentation Layer Rules

*适用于：rendering、audio、UI、VFX、shaders、animations*

### Required Patterns
...

### Forbidden Approaches
...

---

## Global Rules (All Layers)

### Naming Conventions
| Element | Convention | Example |
|---------|-----------|---------|
| Classes | [from technical-preferences] | [example] |
| Variables | [from technical-preferences] | [example] |
| Signals/Events | [from technical-preferences] | [example] |
| Files | [from technical-preferences] | [example] |
| Constants | [from technical-preferences] | [example] |

### Performance Budgets
| Target | Value |
|--------|-------|
| Framerate | [from technical-preferences] |
| Frame budget | [from technical-preferences] |
| Draw calls | [from technical-preferences] |
| Memory ceiling | [from technical-preferences] |

### Approved Libraries / Addons
- [library] — approved for [purpose]

### Forbidden APIs ([engine version])
这些 API 对于 [engine + version] 来说已弃用或未验证：
- `[api name]` — deprecated since [version] / unverified post-cutoff
- Source: `docs/engine-reference/[engine]/deprecated-apis.md`

### Cross-Cutting Constraints
- [适用于所有地方的约束，无论层级]
```

---

## 6. 建议下一步

写完 manifest 后：

- 如果 epics/stories 还不存在："Run `/create-epics layer: foundation` then `/create-stories [epic-slug]` — programmers can now use this manifest when writing story implementation notes."
- 如果这是一次重建（manifest 之前已经存在）："Updated. Recommend notifying the team of changed rules — especially any new Forbidden entries."

---

## 协作协议

1. **静默加载**——在呈现任何内容前读取所有输入
2. **先展示摘要**——让用户在写入前看到范围
3. **写入前先问**——始终在创建或覆盖 manifest 前确认。写入时：结论：**COMPLETE** — control manifest written。拒绝时：结论：**BLOCKED** — user declined write。
4. **每条规则都要有来源**——绝不要添加没有来源 ADR、技术偏好或引擎参考文档支撑的规则
5. **不做再解释式改写**——按 ADR 原文提取规则；不要用会改变含义的方式改写