---
name: create-epics
description: "把已批准的 GDD + architecture 转换为 epics——每个 architectural module 一个 epic。定义范围、主管 ADR、引擎风险和未追踪需求。不要拆分为 stories——每创建完一个 epic 后运行 /create-stories [epic-slug]。"
argument-hint: "[system-name | layer: foundation|core|feature|presentation | all] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
agent: technical-director
---

# Create Epics

Epic 是一段有名称、有边界的工作，映射到一个 architectural module。它定义**要建什么**以及**架构上由谁负责**。它不规定实现步骤——那是 stories 的工作。

**在开发接近某个层级时，每个层级只运行一次此技能。**不要在 Core 还未接近完成时创建 Feature layer epics——设计会变。

**输出：**`production/epics/[epic-slug]/EPIC.md` + `production/epics/index.md`

**每个 epic 的下一步：**`/create-stories [epic-slug]`

**运行时机：**在 `/create-control-manifest` 和 `/architecture-review` 通过之后。

---

## 1. 解析参数

先解析 review mode（只做一次，并在本次运行所有 gate spawn 中复用）：
1. 如果传入 `--review [full|lean|solo]` → 使用它
2. 否则读取 `production/review-mode.txt` → 使用其值
3. 否则 → 默认 `lean`

完整检查模式见 `.claude/docs/director-gates.md`。

**模式：**
- `/create-epics all` —— 按层级顺序处理所有系统
- `/create-epics layer: foundation` —— 仅 Foundation layer
- `/create-epics layer: core` —— 仅 Core layer
- `/create-epics layer: feature` —— 仅 Feature layer
- `/create-epics layer: presentation` —— 仅 Presentation layer
- `/create-epics [system-name]` —— 单个特定系统
- 无参数 —— 询问："Which layer or system would you like to create epics for?"

---

## 2. 加载输入

### 步骤 2a — 摘要扫描（快速）

在完整读取之前，先 Grep 所有 GDD 的 `## Summary` 章节：

```
Grep pattern="## Summary" glob="design/gdd/*.md" output_mode="content" -A 5
```

对于 `layer:` 或 `[system-name]` 模式：根据 Summary 快速参考，只筛选范围内 GDD。跳过所有范围外内容的完整读取。

### 步骤 2b — 完整文档加载（仅限范围内系统）

利用步骤 2a 的 grep 结果，识别哪些系统在范围内。**只完整读取范围内系统的文档**——不要读取范围外系统或层级的 GDD 或 ADR。

读取范围内系统的：

- `design/gdd/systems-index.md` —— 权威系统列表、层级、优先级
- 仅范围内 GDD（Approved 或 Designed 状态，按步骤 2a 结果筛选）
- `docs/architecture/architecture.md` —— 模块归属与 API 边界
- 仅涵盖范围内系统的 Accepted ADR——读取它们的 "GDD Requirements Addressed"、"Decision" 和 "Engine Compatibility" 章节；跳过无关域的 ADR
- `docs/architecture/control-manifest.md` —— 头部的 Manifest Version 日期
- `docs/architecture/tr-registry.yaml` —— 追踪需求到 ADR 覆盖情况
- `docs/engine-reference/[engine]/VERSION.md` —— 引擎名称、版本、风险等级

报告：`"Loaded [N] GDDs, [M] ADRs, engine: [name + version]."`

---

## 3. 处理顺序

按依赖安全的层级顺序处理：
1. **Foundation**（无依赖）
2. **Core**（依赖 Foundation）
3. **Feature**（依赖 Core）
4. **Presentation**（依赖 Feature + Core）

在每个层级内，按 `systems-index.md` 中的顺序执行。

---

## 4. 定义每个 Epic

对每个系统，将其映射到 `architecture.md` 中的 architectural module。

根据 TR registry 检查 ADR 覆盖：
- **Traced requirements**：有 Accepted ADR 覆盖的 TR-ID
- **Untraced requirements**：没有 ADR 的 TR-ID——在继续之前发出警告

在写任何东西之前先向用户展示：

```
## Epic: [System Name]

**Layer**: [Foundation / Core / Feature / Presentation]
**GDD**: design/gdd/[filename].md
**Architecture Module**: [module name from architecture.md]
**Governing ADRs**: [ADR-NNNN, ADR-MMMM]
**Engine Risk**: [LOW / MEDIUM / HIGH — highest risk among governing ADRs]
**GDD Requirements Covered by ADRs**: [N / total]
**Untraced Requirements**: [list TR-IDs with no ADR, or "None"]
```

如果存在 untraced requirements：
> "⚠️ [N] requirements in [system] have no ADR. The epic can be created, but stories for these requirements will be marked Blocked until ADRs exist. Run `/architecture-decision` first, or proceed with placeholders."

询问："Shall I create Epic: [name]?"
选项："Yes, create it"、"Skip"、"Pause — I need to write ADRs first"

---

## 4b. Producer Epic Structure Gate

**review mode 检查**——在 spawn PR-EPIC 前执行：
- `solo` → 跳过。注："PR-EPIC skipped — Solo mode." 进入步骤 5（写 epic 文件）。
- `lean` → 跳过（不是 PHASE-GATE）。注："PR-EPIC skipped — Lean mode." 进入步骤 5（写 epic 文件）。
- `full` → 正常 spawn。

在当前层级的所有 epics 都定义完（步骤 4 对所有范围内系统完成）且在写任何文件之前，通过 Task 使用 gate **PR-EPIC**（`.claude/docs/director-gates.md`）spawn `producer`。

传入：完整 epic 结构摘要（所有 epics、其范围摘要、主管 ADR 数量）、当前处理的层级、里程碑时间线与团队容量。

展示 producer 的评审。如果为 UNREALISTIC，先允许用户在写入前修正 epic 边界（拆分范围过大的 epics 或合并过小的 epics）。如果为 CONCERNS，把它们展示出来并让用户决定。不要在 producer gate 解决前写 epic 文件。

---

## 5. 写入 Epic 文件

获批后，询问："May I write the epic file to `production/epics/[epic-slug]/EPIC.md`?"

用户确认后，写入：

### `production/epics/[epic-slug]/EPIC.md`

```markdown
# Epic: [System Name]

> **Layer**: [Foundation / Core / Feature / Presentation]
> **GDD**: design/gdd/[filename].md
> **Architecture Module**: [module name]
> **Status**: Ready
> **Stories**: Not yet created — run `/create-stories [epic-slug]`

## Overview

[1 paragraph describing what this epic implements, derived from the GDD Overview
and the architecture module's stated responsibilities]

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|-----|-----------------|-------------|
| ADR-NNNN: [title] | [1-line summary] | LOW/MEDIUM/HIGH |

## GDD Requirements

| TR-ID | Requirement | ADR Coverage |
|-------|-------------|--------------|
| TR-[system]-001 | [requirement text from registry] | ADR-NNNN ✅ |
| TR-[system]-002 | [requirement text] | ❌ No ADR |

## Definition of Done

This epic is complete when:
- All stories are implemented, reviewed, and closed via `/story-done`
- All acceptance criteria from `design/gdd/[filename].md` are verified
- All Logic and Integration stories have passing test files in `tests/`
- All Visual/Feel and UI stories have evidence docs with sign-off in `production/qa/evidence/`

## Next Step

Run `/create-stories [epic-slug]` to break this epic into implementable stories.
```

### 更新 `production/epics/index.md`

创建或更新主索引：

```markdown
# Epics Index

Last Updated: [date]
Engine: [name + version]

| Epic | Layer | System | GDD | Stories | Status |
|------|-------|--------|-----|---------|--------|
| [name] | Foundation | [system] | [file] | Not yet created | Ready |
```

---

## 6. Gate-Check 提示

写完请求范围内的所有 epics 后：

- **Foundation + Core complete**：这些是 Pre-Production → Production gate 的必需项。运行 `/gate-check production` 检查 readiness。
- **Reminder**：Epics 定义范围。Stories 定义实现步骤。程序员接手前，先为每个 epic 运行 `/create-stories [epic-slug]`。

---

## 协作协议

1. **一次只做一个 epic**——在询问创建前，先展示每个 epic 的定义
2. **对缺口发出警告**——继续前先标记未追踪需求
3. **写入前先问**——每个 epic 都要单独批准后才能写文件
4. **不凭空发明**——所有内容都来自 GDD、ADR 和 architecture 文档
5. **绝不创建 stories**——此技能止步于 epic 层级

处理完所有请求的 epics 后：

- **Verdict: COMPLETE** —— 已写入 [N] 个 epic。每个 epic 都运行 `/create-stories [epic-slug]`。
- **Verdict: BLOCKED** —— 用户拒绝全部 epics，或没有找到可用系统。