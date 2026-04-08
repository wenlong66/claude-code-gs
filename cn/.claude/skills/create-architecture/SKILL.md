---
name: create-architecture
description: "分章节引导式编写游戏主架构文档。读取所有 GDD、systems index、现有 ADR 与引擎参考库，生成在任何代码编写前所需的完整架构蓝图。支持引擎版本感知：标记知识空白，并按钉定引擎版本验证决策。"
argument-hint: "[focus-area: full | layers | data-flow | api-boundaries | adr-audit] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash, AskUserQuestion, Task
agent: technical-director
---

# Create Architecture

此技能会产出 `docs/architecture/architecture.md` —— 主架构文档，把所有已批准的 GDD 转换为具体的技术蓝图。
它位于设计与实现之间，且必须在 sprint planning 开始前存在。

**与 `/architecture-decision` 不同**：ADR 记录的是单个点决策。
此技能创建的是为 ADR 提供上下文的整套系统蓝图。

先解析 review mode（只做一次，并在本次运行所有 gate spawn 中复用）：
1. 如果传入 `--review [full|lean|solo]` → 使用它
2. 否则读取 `production/review-mode.txt` → 使用其值
3. 否则 → 默认 `lean`

完整检查模式见 `.claude/docs/director-gates.md`。

**参数模式：**
- **无参数 / `full`**：完整引导式流程——所有章节，从头到尾
- **`layers`**：只聚焦系统层图
- **`data-flow`**：只聚焦模块间数据流
- **`api-boundaries`**：只聚焦 API 边界定义
- **`adr-audit`**：仅审计现有 ADR 的引擎兼容性缺口

---

## 阶段 0：加载全部上下文

在做任何事情之前，按以下顺序加载完整项目上下文：

### 0a. 引擎上下文（关键）

完整读取引擎参考库：

1. `docs/engine-reference/[engine]/VERSION.md`
   → 提取：引擎名称、版本、LLM cutoff、切后风险等级
2. `docs/engine-reference/[engine]/breaking-changes.md`
   → 提取：所有 HIGH 和 MEDIUM 风险变更
3. `docs/engine-reference/[engine]/deprecated-apis.md`
   → 提取：应避免的 API
4. `docs/engine-reference/[engine]/current-best-practices.md`
   → 提取：与训练数据不同的切后最佳实践
5. `docs/engine-reference/[engine]/modules/` 下的所有文件
   → 提取：各领域当前 API 模式

如果没有配置引擎，则停止并提示：
> "未配置引擎。请先运行 `/setup-engine`。在不知道目标引擎与版本之前，无法编写 architecture。"

### 0b. 设计上下文 + 技术需求提取

读取所有已批准的设计文档，并从中提取技术需求：

1. `design/gdd/game-concept.md` —— 游戏 pillars、genre、core loop
2. `design/gdd/systems-index.md` —— 所有系统、依赖、优先级层级
3. `.claude/docs/technical-preferences.md` —— 命名约定、性能预算、允许库、禁止模式
4. `design/gdd/` 中的**每个 GDD** —— 对每个文件提取技术需求：
   - 游戏规则暗示的数据结构
   - 明示或隐含的性能约束
   - 系统所需的引擎能力
   - 跨系统通信模式（谁与谁通信、如何通信）
   - 必须持久化的状态（save/load 影响）
   - 线程或时序要求

构建一份**Technical Requirements Baseline**——一张扁平列表，列出从所有 GDD 中提取的所有需求，编号为 `TR-[gdd-slug]-[NNN]`。
这就是架构必须覆盖的全部内容。呈现为：

```
## Technical Requirements Baseline
Extracted from [N] GDDs | [X] total requirements

| Req ID | GDD | System | Requirement | Domain |
|--------|-----|--------|-------------|--------|
| TR-combat-001 | combat.md | Combat | Hitbox detection per-frame | Physics |
| TR-combat-002 | combat.md | Combat | Combo state machine | Core |
| TR-inventory-001 | inventory.md | Inventory | Item persistence | Save/Load |
```

这份基线会进入后续每一阶段。本次会话结束前，不应有任何 GDD 需求没有对应的架构决策支持。

### 0c. 现有架构决策

读取 `docs/architecture/` 下所有文件，了解已经做过哪些决策。
列出找到的所有 ADR 及其领域。

### 0d. 生成知识空白清单

在继续前，展示结构化摘要：

```
## Engine Knowledge Gap Inventory
Engine: [name + version]
LLM Training Covers: up to approximately [version]
Post-Cutoff Versions: [list]

### HIGH RISK Domains (must verify against engine reference before deciding)
- [Domain]: [Key changes]

### MEDIUM RISK Domains (verify key APIs)
- [Domain]: [Key changes]

### LOW RISK Domains (in training data, likely reliable)
- [Domain]: [no significant post-cutoff changes]

### Systems from GDD that touch HIGH/MEDIUM risk domains:
- [GDD system name] → [domain] → [risk level]
```

询问："This inventory identifies [N] systems in HIGH RISK engine domains. Shall I continue building the architecture with these warnings flagged throughout?"

---

## 阶段 1：系统层映射

把 `systems-index.md` 中的每个系统映射到一个 architecture layer。标准游戏架构层如下：

```
┌─────────────────────────────────────────────┐
│  PRESENTATION LAYER                         │  ← UI, HUD, menus, VFX, audio
├─────────────────────────────────────────────┤
│  FEATURE LAYER                              │  ← gameplay systems, AI, quests
├─────────────────────────────────────────────┤
│  CORE LAYER                                 │  ← physics, input, combat, movement
├─────────────────────────────────────────────┤
│  FOUNDATION LAYER                           │  ← engine integration, save/load,
│                                             │    scene management, event bus
├─────────────────────────────────────────────┤
│  PLATFORM LAYER                             │  ← OS, hardware, engine API surface
└─────────────────────────────────────────────┘
```

对每个 GDD 系统，询问：
- 它属于哪一层？
- 它的 module boundary 是什么？
- 它独占拥有什么？（data、state、behaviour）

在继续下一章节前，先呈现 proposed layer assignment 并请求批准。立即将获批的 layer map 写入 skeleton 文件。

**引擎感知检查**：对每个分配到 Core 与 Foundation 层的系统，如果它触及 HIGH 或 MEDIUM 风险的引擎领域，就做标记。直接展示相关引擎参考摘录。

---

## 阶段 2：模块所有权图

对阶段 1 定义的每个模块，明确所有权：

- **Owns**：该模块唯一负责哪些数据和状态
- **Exposes**：其他模块可以读取或调用什么
- **Consumes**：它会从哪些其他模块读取什么
- **Engine APIs used**：该模块直接调用哪些特定引擎 classes/nodes/signals（要注明版本与风险等级）

先按层级输出表格，再输出 ASCII 依赖图。

**引擎感知检查**：对每个列出的引擎 API，都要对照相应模块参考文档验证。如果 API 是切后版本，则标记：

```
⚠️  [ClassName.method()] — Godot 4.6 (post-cutoff, HIGH risk)
    Verified against: docs/engine-reference/godot/modules/[domain].md
    Behaviour confirmed: [yes / NEEDS VERIFICATION]
```

在写入前先让用户批准 ownership map。

---

## 阶段 3：数据流

定义关键游戏场景中，数据如何在模块之间流动。至少覆盖：

1. **Frame update path**：Input → Core systems → State → Rendering
2. **Event/signal path**：系统如何在不紧耦合的情况下通信
3. **Save/load path**：哪些状态被序列化，哪个模块负责序列化
4. **Initialisation order**：哪些模块必须先启动

如有帮助，可使用 ASCII sequence diagram。对每条数据流：
- 命名正在传递的数据
- 标明 producer 与 consumer
- 说明这是同步调用、signal/event，还是 shared state
- 标记跨线程边界的数据流

对每个场景分别请求用户批准后再写入。

---

## 阶段 4：API 边界

定义模块之间的公共契约。对每个边界说明：

- 模块向系统其余部分暴露的接口是什么？
- 入口点有哪些（functions/signals/properties）？
- 调用方必须遵守哪些不变量？
- 模块向调用方必须保证什么？

使用伪代码或项目的实际语言（来自 technical preferences）来编写。
这些契约就是程序员实现时要遵循的内容。

**引擎感知检查**：如果任何接口使用了引擎特定类型（例如 Godot 中的 `Node`、`Resource`、`Signal`），要标注版本并验证该类型在目标引擎版本中是否存在且签名未改变。

---

## 阶段 5：ADR 审计 + 追踪检查

对阶段 0c 中的所有现有 ADR，同时对照本次会话构建出的架构（阶段 1–4）以及阶段 0b 的 Technical Requirements Baseline 进行审查。

### ADR 质量检查

对每个 ADR：
- [ ] 是否有 Engine Compatibility 章节？
- [ ] 是否记录了引擎版本？
- [ ] 是否标记了切后 API？
- [ ] 是否有 "GDD Requirements Addressed" 章节？
- [ ] 是否与本次会话中做出的层级/所有权决策冲突？
- [ ] 是否仍适用于钉定的引擎版本？

| ADR | Engine Compat | Version | GDD Linkage | Conflicts | Valid |
|-----|--------------|---------|-------------|-----------|-------|
| ADR-0001: [title] | ✅/❌ | ✅/❌ | ✅/❌ | None/[conflict] | ✅/⚠️ |

### 追踪覆盖检查

把 Technical Requirements Baseline 中的每条需求映射到现有 ADR。
对每条需求，检查是否有任何 ADR 的 "GDD Requirements Addressed" 章节或决策文本覆盖了它：

| Req ID | Requirement | ADR Coverage | Status |
|--------|-------------|--------------|--------|
| TR-combat-001 | Hitbox detection per-frame | ADR-0003 | ✅ |
| TR-combat-002 | Combo state machine | — | ❌ GAP |
```

统计：X covered, Y gaps。每个 gap 都会成为一个**Required New ADR**。

### Required New ADRs

列出本次 architecture 会话中在阶段 1–4 做出的、但尚无对应 ADR 的所有决策，以及所有未覆盖的 Technical Requirements。
按层级分组——先 Foundation：

**Foundation Layer（在任何编码前都必须创建）：**
- `/architecture-decision [title]` → covers: TR-[id], TR-[id]

**Core Layer：**
- `/architecture-decision [title]` → covers: TR-[id]

---

## 阶段 6：缺失 ADR 清单

基于完整 architecture，生成一份应存在但尚未存在的 ADR 完整清单。按优先级分组：

**在开始编码前必须有（Foundation & Core decisions）：**
- [例如 “Scene management and scene loading strategy”]
- [例如 “Event bus vs direct signal architecture”]

**在相关系统被实现前应有：**
- [例如 “Inventory serialisation format”]

**可延后到实现时再定：**
- [例如 “Specific shader technique for water”]

---

## 阶段 7：写入主架构文档

所有章节都获批后，将完整文档写入 `docs/architecture/architecture.md`。

询问："May I write the master architecture document to `docs/architecture/architecture.md`?"

文档结构：

```markdown
# [Game Name] — Master Architecture

## Document Status
- Version: [N]
- Last Updated: [date]
- Engine: [name + version]
- GDDs Covered: [list]
- ADRs Referenced: [list]

## Engine Knowledge Gap Summary
[Condensed from Phase 0d inventory — HIGH/MEDIUM risk domains and their implications]

## System Layer Map
[From Phase 1]

## Module Ownership
[From Phase 2]

## Data Flow
[From Phase 3]

## API Boundaries
[From Phase 4]

## ADR Audit
[From Phase 5]

## Required ADRs
[From Phase 6]

## Architecture Principles
[3-5 key principles that govern all technical decisions for this project,
derived from the game concept, GDDs, and technical preferences]

## Open Questions
[Decisions deferred — must be resolved before the relevant layer is built]
```

---

## 阶段 7b：Technical Director 签署 + Lead Programmer 可行性审查

写完主架构文档后，在交接前执行一次明确的签署。

**步骤 1 — Technical Director 自审**（此技能以 technical-director 身份运行）：

对已完成文档应用 gate **TD-ARCHITECTURE**（见 `.claude/docs/director-gates.md`）作为自审。对照 gate 定义中的四项标准逐一检查。

**review mode 检查**——在 spawn LP-FEASIBILITY 前执行：
- `solo` → 跳过。注："LP-FEASIBILITY skipped — Solo mode." 进入阶段 8 交接。
- `lean` → 跳过（不是 PHASE-GATE）。注："LP-FEASIBILITY skipped — Lean mode." 进入阶段 8 交接。
- `full` → 正常 spawn。

**步骤 2 — 通过 Task 使用 gate LP-FEASIBILITY（`.claude/docs/director-gates.md`）spawn `lead-programmer`：**

传入：architecture 文档路径、Technical Requirements Baseline 摘要、ADR 列表。

**步骤 3 — 向用户同时展示两份评估：**

并排展示 Technical Director 评估与 Lead Programmer verdict。

使用 `AskUserQuestion` —— "Technical Director and Lead Programmer have reviewed the architecture. How would you like to proceed?"
选项：`Accept — proceed to handoff` / `Revise flagged items first` / `Discuss specific concerns`

**步骤 4 — 将签署记录到 architecture 文档中：**

更新 Document Status 章节：
```
- Technical Director Sign-Off: [date] — APPROVED / APPROVED WITH CONDITIONS
- Lead Programmer Feasibility: FEASIBLE / CONCERNS ACCEPTED / REVISED
```

询问："May I update the Document Status section in `docs/architecture/architecture.md` with the sign-off?"

---

## 阶段 8：交接

写完文档后，给出清晰交接：

1. **接下来运行这些 ADR**（来自阶段 6，已排序）：列出前三个
2. **门控检查**："The master architecture document is complete. Run `/gate-check pre-production` when all required ADRs are also written."
3. **更新会话状态**：向 `production/session-state/active.md` 写入摘要

---

## 协作协议

此技能在每个阶段都遵循协作设计原则：

1. **静默加载上下文**——不要把文件读取过程逐条讲出来
2. **呈现发现**——展示知识空白清单和层级提案
3. **先问再定**——对每项架构选择都呈现选项
4. **写入前先获批**——每个阶段的章节都要在用户批准后才写入
5. **增量写入**——每个获批章节都立即写入；不要攒到最后一次性写。这可以在会话崩溃时保住工作。

在没有用户输入前，绝不要做出有约束力的架构决定。如果用户犹豫，就先给 2–4 个带利弊的选项，再请求决定。

---

## 推荐下一步

- 对阶段 6 列出的每个 Required ADR 运行 `/architecture-decision [title]` —— Foundation layer ADR 优先
- 在必要 ADR 全部写完后运行 `/create-control-manifest`，生成 layer rules manifest
- 当所有必需 ADR 都写完且 architecture 完成签署后，运行 `/gate-check pre-production`