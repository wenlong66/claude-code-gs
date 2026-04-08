# 示例会话：/adopt —— 棕地项目入门

**上下文：** 开发者在发现这套智能体系统之前，已经做了 3 个月的游戏开发。他们有代码、一些设计文档和粗略笔记——但这些内容都没有按技能可用的格式整理。

**起始状态：**
- `src/gameplay/` —— 约 4000 行 Godot 4.6 GDScript
- `design/` —— 3 个 markdown 文件，只有粗略设计笔记（不是 GDD 模板格式）
- 没有 `design/gdd/` 目录
- 没有 `docs/architecture/` 目录
- 没有 `production/` 目录
- 没有 `design/gdd/systems-index.md`
- CLAUDE.md 存在（引擎已配置：Godot 4.6）

**会话时长：** 约 30 分钟
**轮数：** 8
**结果：** 写出了入门计划，并立即修复了最紧急的缺口（缺失的系统索引）

---

## 第 1 轮：用户调用 /adopt

**User：**
> /adopt

## 第 2 轮：智能体检测项目状态

**Agent（technical-director，通过 /adopt，context: fork）：**
> 正在运行棕地审计……
>
> **阶段 1：项目状态检测**
>
> | 工件类别 | 找到 | 说明 |
> |------------------|-------|-------|
> | 引擎配置 | ✅ | CLAUDE.md 中已配置 Godot 4.6 |
> | 源代码 | ✅ | `src/gameplay/` 中约 4000 行代码 |
> | 设计文档 | ⚠️ | `design/` 中 3 个文件，但不是 GDD 格式 |
> | 架构文档 | ❌ | 缺少 `docs/architecture/` |
> | 系统索引 | ❌ | 缺少 `design/gdd/systems-index.md` |
> | 生产追踪 | ❌ | 缺少 `production/` 目录 |
> | 冲刺/故事文件 | ❌ | 没有 |
>
> **阶段 2：格式审计（现有文件）**
>
> 现在检查这 3 个设计文件的内部结构……
>
> *`design/combat-notes.md`：*
> - 有非正式笔记，没有 GDD 模板部分
> - 包含：一些规则描述、一个伤害公式、粗略平衡数值
> - 相比 GDD 模板缺少：概述、玩家幻想、边缘情况、依赖、调优旋钮、验收标准（8 个部分中的 6 个）
>
> *`design/crafting-ideas.md`：*
> - 头脑风暴式笔记，没有结构
> - 没有公式，没有验收标准
> - 更像早期概念思考——可作为 GDD 输入，但还不是 GDD
>
> *`design/inventory.md`：*
> - 最接近 GDD——有概述和规则部分
> - 但缺少：玩家幻想、公式、边缘情况、调优旋钮、验收标准（8 个部分中的 5 个）
>
> **阶段 3：缺口分类**
>
> | 缺口 | 严重度 | 原因 |
> |-----|----------|--------|
> | 没有系统索引 | BLOCKING | `/design-system`、`/create-stories`、`/gate-check` 都需要它 |
> | GDD 文件不是模板格式 | HIGH | 技能无法从畸形 GDD 中引用 TR-ID |
> | 没有架构文档 | HIGH | 不能运行 `/architecture-review` 或 `/create-control-manifest` |
> | 没有生产追踪 | MEDIUM | 冲刺和故事技能还用不上，但到生产阶段前会需要 |
> | `design/crafting-ideas.md` —— 预 GDD 内容 | LOW | 可以作为输入；在正式编写 GDD 之前不会阻塞任何事情 |

## 第 3 轮：智能体呈现迁移计划

**Agent：**
> **阶段 4：迁移计划**
>
> 这里有 7 个按顺序执行的步骤，可以把你的项目对齐到完整流程。绝不会覆盖已有内容——每一步只补缺口。
>
> | # | 步骤 | 技能 | 优先级 | 说明 |
> |---|------|-------|----------|-------|
> | 1 | 创建 `design/gdd/systems-index.md` | `/map-systems` 或 `/adopt` 内联 | BLOCKING | 解锁所有下游技能 |
> | 2 | 回填 `design/inventory.md` → GDD 格式 | `/design-system retrofit design/inventory.md` | HIGH | 补齐缺失的 5 个部分，保留现有内容 |
> | 3 | 回填 `design/combat-notes.md` → GDD 格式 | `/design-system retrofit design/combat-notes.md` | HIGH | 补齐缺失的 6 个部分 |
> | 4 | 把 `design/crafting-ideas.md` 转成完整 GDD | `/design-system crafting`（新写作，使用 ideas 文件作为输入） | MEDIUM | 这不是 retrofit——内容太非正式，不能直接回填 |
> | 5 | 从现有代码创建架构 ADR | `/reverse-document` + `/architecture-decision` | HIGH | 记录已经写进代码的决策 |
> | 6 | 创建总架构文档 | `/create-architecture` | HIGH | 放在 ADR 之后 |
> | 7 | 建立生产追踪 | `/sprint-plan new` | MEDIUM | 放在架构阶段之后 |
>
> **重要：** 第 1 步必须先做。其他步骤可以并行或根据你的优先级重新排序。
>
> 我可以把这个计划写到 `docs/adoption-plan-2026-03-12.md` 吗？

**User：**
> Yes. Write it.

**Agent 写入 adoption plan。**

## 第 4 轮：智能体提出修复最紧急缺口

**Agent：**
> 最紧急的缺口是缺失的 `design/gdd/systems-index.md`。
>
> 我现在可以通过读取你的现有代码和设计文档，推断出你已经构建了哪些系统来创建它。这样比从头运行 `/map-systems` 更快——我会基于已有内容填充它，然后由你确认或调整。
>
> 现在要我做吗？

**User：**
> Yes, do it.

## 第 5 轮：智能体读取代码库并起草系统索引

**Agent：**
> 正在读取 `src/gameplay/` 来推断系统……
>
> 我找到了这些系统边界：
>
> - `src/gameplay/combat/` —— 伤害计算、命中检测、状态效果
> - `src/gameplay/inventory/` —— 物品管理、重量、堆叠
> - `src/gameplay/crafting/` —— 配方查询、结果生成（引用 inventory）
> - `src/gameplay/movement/` —— CharacterBody2D、地形修饰（被 combat 用于位置）
> - `src/gameplay/ui/` —— HUD、库存界面、对话框
> - `src/gameplay/world/` —— TileMap、地形类型、分块加载
>
> **系统索引草案：**
>
> | 系统 | 类别 | 优先级 | 依赖 | GDD 状态 |
> |------|----------|----------|--------------|------------|
> | Movement | 基础 | MVP | 无 | ❌ 缺失 |
> | World/Terrain | 基础 | MVP | Movement | ❌ 缺失 |
> | Combat | 核心 | MVP | Movement | ⚠️ 需要回填 |
> | Inventory | 核心 | MVP | 无 | ⚠️ 需要回填 |
> | Crafting | 功能 | MVP | Inventory | ❌ 只有前 GDD 内容 |
> | UI / HUD | 呈现 | MVP | Combat、Inventory、Movement | ❌ 缺失 |
>
> 这样对吗？有没有漏掉或分类错误的地方？

**User：**
> 看起来对。再加一个 Stamina 系统——它在 combat/ 里，但应该是独立系统。

**Agent：**
> 已加上 Stamina 作为核心 / MVP 系统：
>
> | Stamina | 核心 | MVP | Movement、Combat | ❌ 缺失 |
>
> 更新了依赖：Movement 依赖 Stamina（移动会消耗它）。
>
> 我可以把这个写到 `design/gdd/systems-index.md` 吗？

## 第 6 轮：用户批准

**User：**
> Yes

**Agent 写入 `design/gdd/systems-index.md`。**

## 第 7 轮：智能体展示现在解锁了什么

**Agent：**
> `design/gdd/systems-index.md` 已创建。
>
> **BLOCKING 缺口已解决。** 现在可以运行以下技能：
>
> - ✅ `/design-system [name]` —— 为任意系统按引导流程编写 GDD
> - ✅ `/design-system retrofit [path]` —— 补齐现有文档缺失部分
> - ✅ `/gate-check` —— 现在有 systems index 可验证
> - ✅ `/help` —— 现在能显示正确的阶段流程
>
> **推荐的下一步（来自迁移计划）：**
>
> 1. 运行 `/design-system retrofit design/inventory.md` —— 你现有文档里最完整、最容易先做的一份
> 2. 运行 `/design-system retrofit design/combat-notes.md`
> 3. 运行 `/design-system crafting` —— 用你的 ideas 文件作为输入来写 crafting GDD
>
> 在完成这 3 个之后，你会有 5/7 个系统拥有完整 GDD。然后运行 `/review-all-gdds`，在架构工作前先抓跨系统一致性问题。

## 第 8 轮：用户确认计划

**User：**
> Perfect. I'll start with the inventory retrofit.

**Agent：**
> 运行：
> ```
> /design-system retrofit design/inventory.md
> ```
>
> 技能会检测你现有的 Overview 和 Rules 部分，展示 8 个部分里哪些缺失，只对缺口运行章节循环。你已有的内容不会被触碰。

---

## 这个示例展示了什么

- **格式审计，而不是存在性审计**：`/adopt` 不只是检查文件在不在，而是检查内部结构是否符合技能预期。一个叫 `gdd.md` 但没有模板部分的文件会被标成缺口。
- **迁移，而不是替换**：现有内容永远不会被覆盖。计划只补缺口。
- **BLOCKING 缺口优先**：缺失系统索引被标记为 BLOCKING，因为它会让最多技能失效。
- **在内联中修复最紧急的缺口**：智能体不是只报告缺口，而是在同一个会话里主动提出立即修复。
- **从代码推断**：系统索引是从代码库结构启动生成的，不是从零乱写——棕地代码里本来就有答案。
- **Retrofit vs. 新写**：`/design-system retrofit` 处理已有但不完整的文档；完整的 `/design-system` 处理全新文档。迁移计划会区分哪种适用于哪个文件。
- **context: fork**：`/adopt` 在 fork 的上下文中运行，避免在主会话里因大范围读取整个代码库而污染上下文。
