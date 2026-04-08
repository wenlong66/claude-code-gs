---
name: adopt
description: "棕地式入门——审计现有项目工件的模板格式合规性（不只是是否存在），按影响程度分类缺口，并生成编号迁移计划。适用于加入进行中的项目或从旧模板版本升级时。不同于 /project-stage-detect（它检查有哪些东西存在）——这个技能检查这些东西是否真的能按模板技能正常工作。"
argument-hint: "[focus: full | gdds | adrs | stories | infra]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
agent: technical-director
---

# Adopt — 棕地模板迁移

此技能会审计一个已有项目的工件，检查其与模板技能流水线的**格式兼容性**，然后生成一份优先级排序的迁移计划。

**这不是 `/project-stage-detect`。**
`/project-stage-detect` 回答的是：*现有什么？*
`/adopt` 回答的是：*现有内容是否真的能和模板技能一起正常工作？*

项目可以有 GDD、ADR 和故事文件——但如果这些工件的内部格式不对，任何依赖格式的技能都可能静默失败，或者产生错误结果。

**输出：**`docs/adoption-plan-[date].md` —— 一份持久、可检查的迁移计划。

**参数模式：**

**审计模式：**`$ARGUMENTS[0]`（空白 = `full`）

- **无参数 / `full`**：完整审计——所有工件类型
- **`gdds`**：仅 GDD 格式合规性
- **`adrs`**：仅 ADR 格式合规性
- **`stories`**：仅故事格式合规性
- **`infra`**：仅基础设施工件缺口（registry、manifest、sprint-status、stage.txt）

---

## 阶段 1：检测项目状态

在读取之前先输出一行：`"Scanning project artifacts..."` —— 这可确认技能正在静默读取阶段运行。

然后在呈现任何内容前保持静默读取。

### 存在性检查
- `production/stage.txt` —— 如果存在则读取（权威阶段）
- `design/gdd/game-concept.md` —— 概念是否存在？
- `design/gdd/systems-index.md` —— 系统索引是否存在？
- 统计 GDD 文件数量：`design/gdd/*.md`（排除 game-concept.md 和 systems-index.md）
- 统计 ADR 文件数量：`docs/architecture/adr-*.md`
- 统计故事文件数量：`production/epics/**/*.md`（排除 EPIC.md）
- `.claude/docs/technical-preferences.md` —— 引擎是否已配置？
- `docs/engine-reference/` —— 是否存在引擎参考文档？
- Glob `docs/adoption-plan-*.md` —— 若存在，记录最近一份先前计划的文件名

### 推断阶段（如果没有 stage.txt）
使用与 `/project-stage-detect` 相同的启发式规则：
- `src/` 中有 10+ 个源文件 → Production
- `production/epics/` 中存在故事 → Pre-Production
- 存在 ADR → Technical Setup
- `systems-index.md` 存在 → Systems Design
- `game-concept.md` 存在 → Concept
- 什么都没有 → Fresh（不是棕地项目——建议 `/start`）

如果项目看起来是全新项目（完全没有工件），使用 `AskUserQuestion`：
- "这看起来像一个全新项目——没有找到现有工件。`/adopt` 适用于需要迁移已有工作的项目。你想怎么做？"
  - "运行 `/start` —— 开始首次引导式入门"
  - "我的工件在非标准位置——帮我找出来"
  - "取消"

然后停止——无论用户选择哪项，都不要继续审计（每个选项都指向不同技能或人工调查）。

报告：`"Detected phase: [phase]. Found: [N] GDDs, [M] ADRs, [P] stories."`

---

## 阶段 2：格式审计

根据参数模式，针对每种工件类型，不仅检查文件是否存在，还要检查它是否包含模板要求的内部结构。

### 2a：GDD 格式审计

对于找到的每个 GDD 文件，扫描标题并检查 8 个必需章节：

| 必需章节 | 要查找的标题模式 |
|---|---|
| 概述 | `## Overview` |
| 玩家幻想 | `## Player Fantasy` |
| 详细规则 / 设计 | `## Detailed` 或 `## Core Rules` 或 `## Detailed Design` |
| 公式 | `## Formulas` 或 `## Formula` |
| 边界情况 | `## Edge Cases` |
| 依赖项 | `## Dependencies` 或 `## Depends` |
| 调优旋钮 | `## Tuning` |
| 验收标准 | `## Acceptance` |

对每个 GDD 记录：
- 哪些章节存在
- 哪些章节缺失
- 现有章节里是有真实内容，还是只有占位文字
  （`[To be designed]` 或同类内容）

另外检查：每个 GDD 的头部块里是否有 `**Status**:` 字段。
有效值：`In Design`、`Designed`、`In Review`、`Approved`、`Needs Revision`。

### 2b：ADR 格式审计

对于找到的每个 ADR 文件，检查这些关键章节：

| 章节 | 缺失时的影响 |
|---|---|
| `## Status` | **阻断**——`/story-readiness` 的 ADR 状态检查会静默放过所有内容 |
| `## ADR Dependencies` | 高——`/architecture-review` 的依赖顺序会失效 |
| `## Engine Compatibility` | 高——无法判断切后版本 API 风险 |
| `## GDD Requirements Addressed` | 中——可追踪性矩阵会失去覆盖 |
| `## Performance Implications` | 低——不是流水线关键项 |

对每个 ADR 记录：哪些章节存在、哪些缺失，以及如果 `Status` 章节存在，则记录其当前值。

### 2c：systems-index.md 格式审计

如果 `design/gdd/systems-index.md` 存在：

1. **带括号的状态值**——用 Grep 查找任何包含括号的 Status 单元格：`"Needs Revision ("`、`"In Progress ("` 等。
   这些会破坏 `/gate-check`、`/create-stories` 和 `/architecture-review` 中的精确字符串匹配。**阻断。**

2. **有效状态值**——检查 Status 列值是否只来自以下集合：
   `Not Started`、`In Progress`、`In Review`、`Designed`、`Approved`、`Needs Revision`
   标记所有无法识别的值。

3. **列结构**——检查表格至少是否包含：系统名称、层级、优先级、状态列。缺少这些列会削弱技能功能。

### 2d：故事格式审计

对于找到的每个故事文件：

- **`Manifest Version:` 字段**——是否存在于故事头部？（低——即使缺失也会自动通过）
- **TR-ID 引用**——故事中是否包含 `TR-[a-z]+-[0-9]+` 模式？（中——没有陈旧性追踪）
- **ADR 引用**——故事是否至少引用了一个 ADR？（检查 `ADR-` 模式）
- **Status 字段**——是否存在且可读？
- **验收标准**——故事是否包含复选框列表（`- [ ]`）？

### 2e：基础设施审计

| 工件 | 路径 | 缺失时的影响 |
|---|---|---|
| TR registry | `docs/architecture/tr-registry.yaml` | 高——没有稳定的需求 ID |
| Control manifest | `docs/architecture/control-manifest.md` | 高——故事没有层级规则 |
| Manifest version stamp | 在 manifest 头部：`Manifest Version:` | 中——陈旧性检查失明 |
| Sprint status | `production/sprint-status.yaml` | 中——`/sprint-status` 会回退到 markdown |
| Stage file | `production/stage.txt` | 中——阶段自动检测不可靠 |
| Engine reference | `docs/engine-reference/[engine]/VERSION.md` | 高——ADR 引擎检查失明 |
| Architecture traceability | `docs/architecture/architecture-traceability.md` | 中——没有持久矩阵 |

### 2f：技术偏好审计

读取 `.claude/docs/technical-preferences.md`。检查每个字段是否仍为 `[TO BE CONFIGURED]`：
- 引擎、语言、渲染、物理 → 未配置时为高（ADR 技能会失败）
- 命名约定 → 中
- 性能预算 → 中
- 禁止模式、允许库 → 低（按设计初始为空）

---

## 阶段 3：对缺口分类并排序

将所有审计中发现的缺口整理为四个严重级别：

**阻断（BLOCKING）**——会导致模板技能现在就静默地产生错误结果。
示例：ADR 缺少 Status 字段、systems-index 中存在括号状态值、
已有 ADR 但引擎未配置。

**高（HIGH）**——会导致故事生成时缺少安全检查，或者基础设施引导失败。
示例：ADR 缺少 Engine Compatibility、GDD 缺少 Acceptance Criteria
（无法据此生成故事）、tr-registry.yaml 缺失。

**中（MEDIUM）**——降低质量和流水线跟踪，但不会破坏功能。
示例：GDD 缺少 Tuning Knobs 或 Formulas 章节、故事缺少 TR-ID、
sprint-status.yaml 缺失。

**低（LOW）**——可回溯改进，属于锦上添花但不紧急。
示例：故事缺少 Manifest Version 时间戳、GDD 缺少 Open Questions 章节。

按每个等级统计总数。如果没有阻断项也没有高优先项：报告项目与模板兼容，
只剩建议性改进。

---

## 阶段 4：构建迁移计划

编写一个编号、排序好的行动计划。排序规则：
1. 先处理阻断项（在任何流水线技能可靠运行前必须修复）
2. 再处理高优先项，先基础设施后 GDD/ADR 内容（引导阶段需要正确格式）
3. 中优先项的顺序：先 GDD 缺口，再 ADR 缺口，再故事缺口（故事依赖 GDD 和 ADR）
4. 最后处理低优先项

对每个缺口，生成一条计划项，包括：
- 清晰的问题说明（一句话，避免行话）
- 如果有技能可处理，给出精确命令
- 需要直接编辑时的人工步骤
- 预计耗时（粗略：5 分钟 / 30 分钟 / 1 次会话）
- 用 `- [ ]` 复选框进行跟踪

**特殊情况——systems-index 中带括号的状态值：**
若存在，此项永远排第一。显示需要修改的精确值以及精确替换文本。并在写计划前提出立即修复的邀请。

**特殊情况——ADR 缺少 Status 字段：**
对每个受影响的 ADR，修复命令是：
`/architecture-decision retrofit docs/architecture/adr-[NNNN]-[slug].md`
将每个 ADR 作为单独可勾选项列出。

**特殊情况——GDD 缺少章节：**
对每个受影响的 GDD，列出缺失章节并给出修复命令：
`/design-system retrofit design/gdd/[filename].md`

**基础设施引导顺序**——始终按以下顺序呈现：
1. 先修复 ADR 格式（registry 依赖读取 ADR 的 Status 字段）
2. 运行 `/architecture-review` → 引导生成 `tr-registry.yaml`
3. 运行 `/create-control-manifest` → 创建带版本戳的 manifest
4. 运行 `/sprint-plan update` → 创建 `sprint-status.yaml`
5. 运行 `/gate-check [phase]` → 权威写入 `stage.txt`

**已有故事**——要明确说明：
> "现有故事可继续与所有模板技能一起工作——当字段缺失时，所有新的格式检查都会自动通过。它们在重新生成之前，不会受益于 TR-ID 陈旧性追踪或 manifest 版本检查。这是刻意设计：不要重新生成已经进行中的故事。"

---

## 阶段 5：呈现摘要并请求写入

在写入前先呈现简洁摘要：

```
## Adoption Audit Summary
Phase detected: [phase]
Engine: [configured / NOT CONFIGURED]
GDDs audited: [N] ([X] fully compliant, [Y] with gaps)
ADRs audited: [N] ([X] fully compliant, [Y] with gaps)
Stories audited: [N]

Gap counts:
  BLOCKING: [N] — template skills will malfunction without these fixes
  HIGH:     [N] — unsafe to run /create-stories or /story-readiness
  MEDIUM:   [N] — quality degradation
  LOW:      [N] — optional improvements

Estimated remediation: [X blocking items × ~Y min each = roughly Z hours]
```

在请求写入之前，显示一个 **Gap Preview**：
- 用一行要点列出每个阻断缺口，描述实际问题
  （例如 `systems-index.md: 3 rows have parenthetical status values`，
  `adr-0002.md: missing ## Status section`）。不要给数量——只展示实际条目。
- HIGH / MEDIUM / LOW 仅显示数量（例如 `HIGH: 4, MEDIUM: 2, LOW: 1`）。

这样用户在提交写入文件前就能判断范围。

如果在阶段 1 检测到了先前的 adoption plan，再加上一条说明：
> "之前已有计划位于 `docs/adoption-plan-[prior-date].md`。新计划将反映当前项目状态——不会与上一次运行做 diff。"

使用 `AskUserQuestion`：
- "准备写迁移计划了吗？"
  - "是——写入 `docs/adoption-plan-[date].md`"
  - "先给我看完整计划预览（暂不写入）"
  - "取消——我自己手动处理迁移"

如果用户选择“先给我看完整计划预览”，则把完整计划输出为一个带 fenced 的 markdown 块。然后用同样的三个选项再次询问。

---

## 阶段 6：写入迁移计划

如果获得批准，写入 `docs/adoption-plan-[date].md`，结构如下：

```markdown
# Adoption Plan

> **Generated**: [date]
> **Project phase**: [phase]
> **Engine**: [name + version, or "Not configured"]
> **Template version**: v1.0+

按照以下步骤依次进行。完成每项后勾选。
随时重新运行 `/adopt` 以检查剩余缺口。

---

## Step 1: Fix Blocking Gaps

[每个阻断缺口一个子章节，包含问题、修复命令、预计耗时、复选框]

---

## Step 2: Fix High-Priority Gaps

[每个高优先缺口一个子章节]

---

## Step 3: Bootstrap Infrastructure

### 3a. Register existing requirements (creates tr-registry.yaml)
运行 `/architecture-review` —— 即使 ADR 已存在，这次运行也会从现有 GDD 和 ADR 中引导生成 TR registry。
**时间**：1 次会话（大型代码库时 review 可能很长）
- [ ] tr-registry.yaml created

### 3b. Create control manifest
运行 `/create-control-manifest`
**时间**：30 分钟
- [ ] docs/architecture/control-manifest.md created

### 3c. Create sprint tracking file
运行 `/sprint-plan update`
**时间**：5 分钟（如果 sprint plan 已经以 markdown 形式存在）
- [ ] production/sprint-status.yaml created

### 3d. Set authoritative project stage
运行 `/gate-check [current-phase]`
**时间**：5 分钟
- [ ] production/stage.txt written

---

## Step 4: Medium-Priority Gaps

[每个中优先缺口一个子章节]

---

## Step 5: Optional Improvements

[每个低优先缺口一个子章节]

---

## What to Expect from Existing Stories

现有故事可继续与所有模板技能一起工作。新的格式检查
（TR-ID 验证、manifest 版本陈旧性）在字段缺失时会自动通过——因此不会出错。
它们在重新生成之前不会受益于陈旧性追踪。不要重新生成正在进行中或已完成的故事。

---

## Re-run

在完成 Step 3 后再次运行 `/adopt`，以验证所有阻断项和高优先项已解决。
新一轮运行会反映项目的当前状态。
```

---

## 阶段 6b：设置 Review Mode

在写入 adoption plan 之后（或用户取消写入时），检查 `production/review-mode.txt` 是否存在。

**如果存在**：读取它并记录当前模式——"Review mode is already set to `[current]`."——跳过提示。

**如果不存在**：使用 `AskUserQuestion`：

- **提示**："还有一个设置步骤：在你推进工作流时，希望获得多少设计评审支持？"
- **选项**：
  - `Full` —— Director specialists 会在每个关键工作流步骤进行评审。适合团队、学习流程，或希望每个决策都得到充分反馈时。
  - `Lean (recommended)` —— Director 只在阶段门转换（/gate-check）时介入。跳过每个技能的单独评审。对独立开发者和小团队来说更平衡。
  - `Solo` —— 完全不进行 Director 评审。速度最快。适合 game jam、原型，或如果评审感觉像额外负担。

在选择后立即把结果写入 `production/review-mode.txt`——不需要单独再问“可以写吗？”：
- `Full` → 写入 `full`
- `Lean (recommended)` → 写入 `lean`
- `Solo` → 写入 `solo`

如果目录不存在，创建 `production/` 目录。

---

## 阶段 7：提供第一个行动

写完计划后不要就此结束。选出最高优先级的单个缺口，并使用 `AskUserQuestion` 立即提出处理建议。按以下第一个适用分支选择：

**如果 systems-index.md 中存在带括号的状态值：**
使用 `AskUserQuestion`：
- "最紧急的修复是 `systems-index.md`——有 [N] 行包含带括号的状态值（例如 `Needs Revision (see notes)`），它们现在就会破坏 /gate-check、
  /create-stories 和 /architecture-review。我可以直接就地修复。"
  - "现在修复——编辑 systems-index.md"
  - "我自己修"
  - "完成——把计划留给我"

**如果 ADR 缺少 `## Status`（且没有括号问题）：**
使用 `AskUserQuestion`：
- "最紧急的修复是给 [N] 个 ADR 添加 `## Status`： [list filenames]。
  没有它，/story-readiness 会静默放过所有 ADR 检查。要先从 [first affected filename] 开始吗？"
  - "是——现在改造 [first affected filename]"
  - "逐个改造全部 [N] 个 ADR"
  - "我自己处理 ADR"

**如果 GDD 缺少 Acceptance Criteria（且上面没有阻断项）：**
使用 `AskUserQuestion`：
- "最紧急的缺口是 [N] 个 GDD 缺少 Acceptance Criteria：
  [list filenames]。没有它们，/create-stories 无法生成故事。要先从 [highest-priority GDD filename] 开始吗？"
  - "是——现在给 [GDD filename] 添加 Acceptance Criteria"
  - "把全部 [N] 个 GDD 一个个处理完"
  - "我自己处理 GDD"

**如果没有 BLOCKING 或 HIGH 缺口：**
使用 `AskUserQuestion`：
- "没有阻断缺口——这个项目与模板兼容。接下来做什么？"
  - "带我看中优先改进"
  - "运行 /project-stage-detect 做更广泛的健康检查"
  - "就到这里——我会按自己的节奏执行计划"

---

## 协作协议

1. **静默读取**——在呈现任何内容前完成完整审计
2. **先展示摘要**——让用户在请求写入前先看到范围
3. **写入前先询问**——始终在创建 adoption plan 文件前确认
4. **提供建议，不要强迫**——计划仅供参考；用户决定修什么、何时修
5. **一次只做一件事**——把计划交出去后，只提供一个具体下一步，而不是六件同时做
6. **永远不要重新生成现有工件**——只补齐已有内容中的缺口；
   不要重写已经有内容的 GDD、ADR 或故事文件