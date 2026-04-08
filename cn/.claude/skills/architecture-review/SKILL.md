---
name: architecture-review
description: "验证项目架构相对于所有 GDD 的完整性与一致性。构建一张可追踪矩阵，将每个 GDD 的技术需求映射到 ADR，识别覆盖缺口，检测跨 ADR 冲突，验证所有决策在已钉定引擎版本上的兼容性，并给出 PASS/CONCERNS/FAIL 结论。相当于架构层面的 /design-review。"
argument-hint: "[focus: full | coverage | consistency | engine | single-gdd path/to/gdd.md]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
agent: technical-director
model: opus
---

# 架构审查

架构审查会验证整套架构决策是否覆盖了全部游戏设计需求、内部是否一致，并且是否正确针对项目钉定的引擎版本。它是 Technical Setup 与 Pre-Production 之间的质量门。

**参数模式：**
- **无参数 / `full`**：完整审查——所有阶段
- **`coverage`**：仅追踪性——哪些 GDD 需求没有 ADR
- **`consistency`**：仅跨 ADR 冲突检测
- **`engine`**：仅引擎兼容性审计
- **`single-gdd [path]`**：只审查某个特定 GDD 的架构覆盖
- **`rtm`**：Requirements Traceability Matrix——在标准矩阵基础上扩展到包含故事文件路径和测试文件路径；输出 `docs/architecture/requirements-traceability.md`，包含完整的 GDD 需求 → ADR → Story → Test 链路。用于 Production 阶段（此时已有故事和测试时）。

---

## 阶段 1：加载全部内容

### 阶段 1a — L0：摘要扫描（快速、低 token）

在读取任何完整文档之前，先用 Grep 从所有 GDD 和 ADR 中提取 `## Summary` 章节：

```
Grep pattern="## Summary" glob="design/gdd/*.md" output_mode="content" -A 4
Grep pattern="## Summary" glob="docs/architecture/adr-*.md" output_mode="content" -A 3
```

对于 `single-gdd [path]` 模式：使用目标 GDD 的摘要，识别哪些 ADR 引用了同一系统（用系统名 Grep ADR），然后只完整读取这些 ADR。完全跳过无关 GDD 的完整读取。

对于 `engine` 模式：只完整读取 ADR——引擎检查不需要 GDD。

对于 `coverage` 或 `full` 模式：继续读取下面的全部内容。

### 阶段 1b — L1/L2：完整文档加载

按模式读取所有相关输入：

### 设计文档
- 范围内的所有 GDD：完整读取每个文件
- `design/gdd/systems-index.md`——系统的权威清单

### 架构文档
- 范围内的所有 ADR：完整读取每个文件
- 如果存在，读取 `docs/architecture/architecture.md`

### 引擎参考
- `docs/engine-reference/[engine]/VERSION.md`
- `docs/engine-reference/[engine]/breaking-changes.md`
- `docs/engine-reference/[engine]/deprecated-apis.md`
- `docs/engine-reference/[engine]/modules/` 下的所有文件

### 项目标准
- `.claude/docs/technical-preferences.md`

报告数量：`"Loaded [N] GDDs, [M] ADRs, engine: [name + version]."`

**如果存在，也要读取 `docs/consistency-failures.md`。**提取其中 Domain 与当前审查系统相关（Architecture、Engine，或当前覆盖的任何 GDD 域）的条目。把反复出现的模式作为 “Known conflict-prone areas” 注释放在第 4 阶段冲突检测输出顶部。

---

## 阶段 2：从每个 GDD 提取技术需求

### 预加载 TR Registry

在提取任何需求之前，如果存在，先读取 `docs/architecture/tr-registry.yaml`。按 `id` 和规范化后的 `requirement` 文本（小写、去首尾空格）建立索引。这样可避免每次审查时需求 ID 重编号。

对每个提取到的需求，匹配规则为：
1. **与同一系统的现有 registry 条目完全/近似匹配** → 复用该条目的 TR-ID，不变更。只有当 GDD 文案变了（意图相同、措辞更清晰）时才更新 registry 里的 `requirement` 文本，并添加 `revised: [date]` 字段。
2. **没有匹配** → 分配新 ID：该系统下下一个可用的 `TR-[system]-NNN`，从现有最大序号 + 1 开始。
3. **有歧义**（部分匹配、意图不清）→ 询问用户：
   > "Does '[new requirement text]' refer to the same requirement as `TR-[system]-NNN: [existing text]'`, or is it a new requirement?"
   用户回答："Same requirement"（复用 ID）或 "New requirement"（新 ID）。

对于 registry 中 `status: deprecated` 的需求——跳过。
它们是故意从 GDD 中移除的。

对每个 GDD，读取它并提取所有**技术需求**——即架构必须提供的、让系统正常工作的内容。技术需求是任何暗示需要特定架构决策的陈述。

需要提取的类别：

| 类别 | 示例 |
|----------|---------|
| **数据结构** | “每个实体都有 health、max health、status effects” → 需要组件/数据 схем  |
| **性能约束** | “碰撞检测必须在 200 个实体下保持 60fps” → 物理预算 ADR |
| **引擎能力** | “角色动画需要 inverse kinematics” → IK 系统 ADR |
| **跨系统通信** | “伤害系统同时通知 UI 和音频” → 事件/信号架构 ADR |
| **状态持久化** | “玩家进度在会话间保留” → 存档系统 ADR |
| **线程/时序** | “AI 决策在主线程外执行” → 并发 ADR |
| **平台要求** | “支持键鼠、手柄、触摸” → 输入系统 ADR |

对每个 GDD，生成结构化列表：

```
GDD: [filename]
System: [system name]
Technical Requirements:
  TR-[GDD]-001: [requirement text] → Domain: [Physics/Rendering/etc]
  TR-[GDD]-002: [requirement text] → Domain: [...]
```

这会成为**需求基线**——架构必须覆盖的全部内容。

---

## 阶段 3：构建追踪矩阵

对阶段 2 中提取的每条技术需求，搜索 ADR：

1. 读取每个 ADR 的 "GDD Requirements Addressed" 章节
2. 检查是否明确引用了该需求或其 GDD
3. 检查 ADR 的决策文本是否隐含覆盖了该需求
4. 标记覆盖状态：

| 状态 | 含义 |
|--------|---------|
| ✅ **Covered** | 某个 ADR 明确处理了该需求 |
| ⚠️ **Partial** | 某个 ADR 部分覆盖，或覆盖关系有歧义 |
| ❌ **Gap** | 没有 ADR 处理该需求 |

构建完整矩阵：

```
## Traceability Matrix

| Requirement ID | GDD | System | Requirement | ADR Coverage | Status |
|---------------|-----|--------|-------------|--------------|--------|
| TR-combat-001 | combat.md | Combat | Hitbox detection < 1 frame | ADR-0003 | ✅ |
| TR-combat-002 | combat.md | Combat | Combo window timing | — | ❌ GAP |
| TR-inventory-001 | inventory.md | Inventory | Persistent item storage | ADR-0005 | ✅ |
```

统计总数：X covered，Y partial，Z gaps。

---

## 阶段 3b：故事与测试链路（仅 RTM 模式）

*除非参数是 `rtm`，或 `full` 且已有 stories，否则跳过此阶段。*

此阶段会把阶段 3 的矩阵扩展为每条需求对应的实现故事与验证测试——形成完整的 Requirements Traceability Matrix（RTM）。

### 步骤 3b-1 — 加载 stories

Glob `production/epics/**/*.md`（排除 EPIC.md 索引文件）。对每个故事文件：
- 从 Context 章节提取 `TR-ID`
- 提取 story 文件路径、标题、Status
- 提取 `## Test Evidence` 章节中的测试文件路径

### 步骤 3b-2 — 加载测试文件

Glob `tests/unit/**/*_test.*` 和 `tests/integration/**/*_test.*`。
建立索引：system → [test file paths]。

对步骤 3b-1 中的每个测试文件路径，再用 Glob 确认该文件是否真实存在。若路径不存在，标记为 MISSING。

### 步骤 3b-3 — 构建扩展 RTM

对阶段 3 矩阵中的每个 TR-ID，新增：
- **Story**：引用该 TR-ID 的 story 文件路径（可多个）
- **Test File**：故事的 Test Evidence 章节中声明的测试文件路径
- **Test Status**：COVERED（测试文件存在）/ MISSING（声明了路径但未找到）/ NONE（没有声明测试路径，故事类型可能是 Visual/Feel/UI）/ NO STORY（需求还没有 story——pre-production 缺口）

扩展矩阵格式：

```
## Requirements Traceability Matrix (RTM)

| TR-ID | GDD | Requirement | ADR | Story | Test File | Test Status |
|-------|-----|-------------|-----|-------|-----------|-------------|
| TR-combat-001 | combat.md | Hitbox < 1 frame | ADR-0003 | story-001-hitbox.md | tests/unit/combat/hitbox_test.gd | COVERED |
| TR-combat-002 | combat.md | Combo window | — | story-002-combo.md | — | NONE (Visual/Feel) |
| TR-inventory-001 | inventory.md | Persistent storage | ADR-0005 | — | — | NO STORY |
```

RTM 覆盖摘要：
- COVERED：[N] —— 需求有 ADR + story + 通过的测试
- MISSING test：[N] —— story 存在但未找到测试文件
- NO STORY：[N] —— 需求有 ADR 但还没有 story
- NO ADR：[N] —— 需求没有架构覆盖（来自阶段 3 的缺口）
- Full chain complete（COVERED）：[N/total]（[%]）

---

## 阶段 4：跨 ADR 冲突检测

把每个 ADR 与其他每个 ADR 逐一比较，检测矛盾。满足以下任一情况即为冲突：

- **数据所有权冲突**：两个 ADR 都声称对同一数据拥有独占所有权
- **集成契约冲突**：ADR-A 假设系统 X 有接口 Y，但 ADR-B 将系统 X 定义为另一种接口
- **性能预算冲突**：ADR-A 给物理分配了 N ms，ADR-B 给 AI 分配了 N ms，加起来超过总帧预算
- **依赖循环**：ADR-A 说系统 X 先于 Y 初始化；ADR-B 说 Y 先于 X 初始化
- **架构模式冲突**：ADR-A 对某子系统使用事件驱动；ADR-B 对同一子系统使用直接函数调用
- **状态管理冲突**：两个 ADR 都定义了同一游戏状态的权威来源（例如 Combat ADR 和 Character ADR 都声称拥有 health）

每发现一个冲突：

```
## Conflict: [ADR-NNNN] vs [ADR-MMMM]
Type: [Data ownership / Integration / Performance / Dependency / Pattern / State]
ADR-NNNN claims: [...]
ADR-MMMM claims: [...]
Impact: [如果两者按原文实现，会破坏什么]
Resolution options:
  1. [Option A]
  2. [Option B]
```

### ADR 依赖排序

在冲突检测之后，分析所有 ADR 的依赖图：

1. **收集每个 ADR 的 ADR Dependencies 章节中的所有 `Depends On` 字段**
2. **拓扑排序**：确定正确实现顺序——没有依赖的 ADR 先（Foundation），依赖它们的随后，以此类推
3. **标记未解决依赖**：如果 ADR-A 的 `Depends On` 引用了一个仍为 `Proposed` 或不存在的 ADR，标记如下：
   ```
   ⚠️  ADR-0005 depends on ADR-0002 — but ADR-0002 is still Proposed.
       ADR-0005 cannot be safely implemented until ADR-0002 is Accepted.
   ```
4. **检测循环**：如果 ADR-A 依赖 ADR-B，而 ADR-B 又依赖 ADR-A（直接或传递），标记为 `DEPENDENCY CYCLE`：
   ```
   🔴 DEPENDENCY CYCLE: ADR-0003 → ADR-0006 → ADR-0003
      This cycle must be broken before either can be implemented.
   ```
5. **输出建议实现顺序**：
   ```
   ### Recommended ADR Implementation Order (topologically sorted)
   Foundation (no dependencies):
     1. ADR-0001: [title]
     2. ADR-0003: [title]
   Depends on Foundation:
     3. ADR-0002: [title] (requires ADR-0001)
     4. ADR-0005: [title] (requires ADR-0003)
   Feature layer:
     5. ADR-0004: [title] (requires ADR-0002, ADR-0005)
   ```

---

## 阶段 5：引擎兼容性交叉检查

在所有 ADR 中检查引擎一致性：

### 版本一致性
- 所有提到引擎版本的 ADR 是否都同意同一个版本？
- 若某 ADR 是为旧引擎版本写的，标记为可能过时

### 切后 API 一致性
- 收集所有 ADR 中的 "Post-Cutoff APIs Used" 字段
- 对每一项，结合相关模块参考文档验证
- 检查是否有两个 ADR 对同一切后 API 做出矛盾假设

### 弃用 API 检查
- 在所有 ADR 中 Grep `deprecated-apis.md` 里列出的 API 名称
- 标记任何引用了弃用 API 的 ADR

### 缺失的 Engine Compatibility 章节
- 列出所有完全缺少 Engine Compatibility 章节的 ADR
- 这些是盲点——它们的引擎假设未知

输出格式：
```
### Engine Audit Results
Engine: [name + version]
ADRs with Engine Compatibility section: X / Y total

Deprecated API References:
  - ADR-0002: uses [deprecated API] — deprecated since [version]

Stale Version References:
  - ADR-0001: written for [older version] — current project version is [version]

Post-Cutoff API Conflicts:
  - ADR-0004 and ADR-0007 both use [API] with incompatible assumptions
```

---

### 引擎专家咨询

完成上面的引擎审计后，通过 Task 生成**主引擎专家**进行一次领域专家二次审阅：
- 读取 `.claude/docs/technical-preferences.md` 的 `Engine Specialists` 章节，确定主专家是谁
- 如果没有配置引擎，则跳过此咨询
- 使用 `subagent_type: [primary specialist]`，并提供：所有包含引擎特定决策或 `Post-Cutoff APIs Used` 字段的 ADR、引擎参考文档、以及阶段 5 的审计发现。请他们：
  1. 确认或挑战每一条审计发现——专家可能了解参考文档未覆盖的引擎细节
  2. 识别 ADR 中可能遗漏的引擎特定反模式（例如 Godot 使用了错误的节点类型、Unity 组件耦合、Unreal 子系统误用）
  3. 标记对引擎行为的假设与当前钉定版本不一致的 ADR

将额外发现记录在阶段 5 输出的 `### Engine Specialist Findings` 下。这些发现会进入最终结论——专家标记的问题与审计标记的问题具有同等权重。

---

## 阶段 5b：设计修订标记（架构 → GDD 反馈）

对于阶段 5 中的每个**高风险引擎发现**，检查是否有任何 GDD 的假设与已验证的引擎事实相冲突。

需要检查的具体情况：

1. **切后 API 行为与训练数据假设不同**：如果某 ADR 记录的已验证 API 行为与默认 LLM 假设不同，检查所有引用相关系统的 GDD，看看是否有围绕旧行为写的规则。

2. **ADR 中记录了已知引擎限制**：如果 ADR 记录了已知限制（例如“Jolt ignores HingeJoint3D damp”、“D3D12 is now the default backend”），检查围绕受影响特性设计机制的 GDD。

3. **弃用 API 冲突**：如果阶段 5 标出了某 ADR 使用弃用 API，检查是否有 GDD 假设了该弃用 API 的行为。

对每个冲突，记录在 GDD Revision Flags 表中：

```
### GDD Revision Flags (Architecture → Design Feedback)
These GDD assumptions conflict with verified engine behaviour or accepted ADRs.
The GDD should be revised before its system enters implementation.

| GDD | Assumption | Reality (from ADR/engine-reference) | Action |
|-----|-----------|--------------------------------------|--------|
| combat.md | "Use HingeJoint3D damp for weapon recoil" | Jolt ignores damp — ADR-0003 | Revise GDD |
```

如果没有发现修订标记，写："No GDD revision flags — all GDD assumptions are consistent with verified engine behaviour."

询问："Should I flag these GDDs for revision in the systems index?"
- 如果是：把相关系统的 Status 字段更新为 `Needs Revision`
  并在相邻的 Notes/Description 列写一条简短内联说明解释冲突。
  写入前先请求批准。
  （不要使用像 `Needs Revision (Architecture Feedback)` 这样的括号——其他技能会精确匹配字符串 `Needs Revision`，括号会破坏匹配。）

---

## 阶段 6：架构文档覆盖

如果 `docs/architecture/architecture.md` 存在，验证其与 GDD 的一致性：

- `systems-index.md` 中的每个系统是否都出现在架构层中？
- 数据流章节是否覆盖了 GDD 中定义的所有跨系统通信？
- API 边界是否支持 GDD 中所有集成需求？
- 架构文档里是否存在没有对应 GDD 的系统（孤儿架构）？

---

## 阶段 7：输出审查报告

```
## Architecture Review Report
Date: [date]
Engine: [name + version]
GDDs Reviewed: [N]
ADRs Reviewed: [M]

---

### Traceability Summary
Total requirements: [N]
✅ Covered: [X]
⚠️ Partial: [Y]
❌ Gaps: [Z]

### Coverage Gaps (no ADR exists)
For each gap:
  ❌ TR-[id]: [GDD] → [system] → [requirement]
     Suggested ADR: "/architecture-decision [suggested title]"
     Domain: [Physics/Rendering/etc]
     Engine Risk: [LOW/MEDIUM/HIGH]

### Cross-ADR Conflicts
[列出阶段 4 的所有冲突]

### ADR Dependency Order
[来自阶段 4 的拓扑排序实现顺序——依赖排序部分]
[如有未解决依赖和循环，也写出]

### GDD Revision Flags
[与已验证引擎行为冲突的 GDD 假设——来自阶段 5b]
[或者："None — all GDD assumptions consistent with verified engine behaviour"]

### Engine Compatibility Issues
[列出阶段 5 的所有引擎问题]

### Architecture Document Coverage
[列出缺失系统和孤儿架构——来自阶段 6]

---

### Verdict: [PASS / CONCERNS / FAIL]

PASS: 所有需求都已覆盖，无冲突，引擎一致
CONCERNS: 存在一些缺口或部分覆盖，但没有阻断性冲突
FAIL: 存在关键缺口（Foundation/Core 层需求未覆盖），
      或检测到阻断性的跨 ADR 冲突

### Blocking Issues (must resolve before PASS)
[仅 FAIL 结论时列出必须解决的问题]

### Required ADRs
[按优先级排序、最基础优先的 ADR 创建清单]
```

---

## 阶段 8：写入并更新追踪索引

使用 `AskUserQuestion` 请求写入批准：
- "审查已完成。你希望我写入什么？"
  - [A] 写入全部三个文件（review report + traceability index + TR registry）
  - [B] 只写 review report —— `docs/architecture/architecture-review-[date].md`
  - [C] 暂时什么都不写——我想先查看发现结果

### RTM 输出（仅 rtm 模式）

对于 `rtm` 模式，还要额外询问："May I write the full Requirements Traceability Matrix to `docs/architecture/requirements-traceability.md`?"

RTM 文件格式：

```markdown
# Requirements Traceability Matrix (RTM)

> Last Updated: [date]
> Mode: /architecture-review rtm
> Coverage: [N]% full chain complete (GDD → ADR → Story → Test)

## How to read this matrix

| Column | Meaning |
|--------|---------|
| TR-ID | Stable requirement ID from tr-registry.yaml |
| GDD | Source design document |
| ADR | Architectural decision governing implementation |
| Story | Story file that implements this requirement |
| Test File | Automated test file path |
| Test Status | COVERED / MISSING / NONE / NO STORY |

## Full Traceability Matrix

| TR-ID | GDD | Requirement | ADR | Story | Test File | Status |
|-------|-----|-------------|-----|-------|-----------|--------|
[Full matrix rows from Phase 3b]

## Coverage Summary

| Status | Count | % |
|--------|-------|---|
| COVERED — full chain complete | [N] | [%] |
| MISSING test — story exists, no test | [N] | [%] |
| NO STORY — ADR exists, not yet implemented | [N] | [%] |
| NO ADR — architectural gap | [N] | [%] |
| **Total requirements** | **[N]** | **100%** |

## Uncovered Requirements (Priority Fix List)

Requirements where the full chain is broken, prioritized by layer:

### Foundation layer gaps
[list with suggested action per gap]

### Core layer gaps
[list]

### Feature / Presentation layer gaps
[list — lower priority]

## History

| Date | Full Chain % | Notes |
|------|-------------|-------|
| [date] | [%] | Initial RTM |
```

### TR Registry 更新

同时询问："May I update `docs/architecture/tr-registry.yaml` with new requirement IDs from this review?"

如果同意：
- **追加**本次审查之前未在 registry 中出现的新 TR-ID
- **更新** `requirement` 文本，以及因 GDD 文案变化而改动的条目的 `revised` 日期（ID 保持不变）
- **标记**那些对应 GDD 需求已不再存在的 registry 条目为 `status: deprecated`（标记前先与用户确认）
- **绝不**重编号或删除现有条目
- 更新顶部的 `last_updated` 和 `version` 字段

这样未来所有 story 文件都能引用在每次后续架构审查中保持不变的稳定 TR-ID。

### Reflexion Log 更新

在写完 review report 后，如果第 4 阶段发现了任何 🔴 CONFLICT 条目，就把它们追加到 `docs/consistency-failures.md`（如果该文件存在）：

```markdown
### [YYYY-MM-DD] — /architecture-review — 🔴 CONFLICT
**Domain**: Architecture / [specific domain e.g. State Ownership, Performance]
**Documents involved**: [ADR-NNNN] vs [ADR-MMMM]
**What happened**: [specific conflict — what each ADR claims]
**Resolution**: [how it was or should be resolved]
**Pattern**: [generalised lesson for future ADR authors in this domain]
```

只追加 CONFLICT 条目——不要记录 GAP 条目（架构尚未完成时缺少 ADR 是正常的）。如果文件不存在，不要创建——仅在它已经存在时追加。

### Session State 更新

在写完所有获批文件后，静默追加到 `production/session-state/active.md`：

    ## Session Extract — /architecture-review [date]
    - Verdict: [PASS / CONCERNS / FAIL]
    - Requirements: [N] total — [X] covered, [Y] partial, [Z] gaps
    - New TR-IDs registered: [N, or "None"]
    - GDD revision flags: [comma-separated GDD names, or "None"]
    - Top ADR gaps: [top 3 gap titles from the report, or "None"]
    - Report: docs/architecture/architecture-review-[date].md

如果 `active.md` 不存在，就以这段内容作为初始文件创建。
在对话中确认："Session state updated."

追踪索引格式：

```markdown
# Architecture Traceability Index
Last Updated: [date]
Engine: [name + version]

## Coverage Summary
- Total requirements: [N]
- Covered: [X] ([%])
- Partial: [Y]
- Gaps: [Z]

## Full Matrix
[Complete traceability matrix from Phase 3]

## Known Gaps
[All ❌ items with suggested ADRs]

## Superseded Requirements
[Requirements whose GDD was changed after the ADR was written]
```

---

## 阶段 9：交接

在完成审查并写入获批文件后，呈现：

1. **立即行动**：列出最优先的 3 个待创建 ADR（最高影响缺口优先，Foundation 层先于 Feature 层）
2. **门控指导**："当所有阻断问题都解决后，运行 `/gate-check pre-production` 以推进阶段"
3. **重新运行触发器**："每写完一个新的 ADR 后，再运行 `/architecture-review` 以确认覆盖率提升"

然后以 `AskUserQuestion` 收尾：
- "Architecture review complete. What would you like to do next?"
  - [A] 写一个缺失的 ADR —— 开一个新会话并运行 `/architecture-decision [system]`
  - [B] 运行 `/gate-check pre-production` —— 如果所有阻断缺口都已解决
  - [C] 本次会话到此结束

---

## 错误恢复协议

如果任何被派生的代理返回 BLOCKED、报错，或未能完成：

1. **立即上报**：在继续之前报告 `"[AgentName]: BLOCKED — [reason]"`
2. **评估依赖**：如果后续阶段需要该代理的输出，则在得到用户输入前不要越过该阶段
3. **通过 AskUserQuestion 提供选项**：
   - 跳过该代理，并在最终报告里注明缺口
   - 缩小范围后重试（更少的 GDD、单系统聚焦）
   - 先停在这里，先解决阻塞项
4. **始终产出部分报告**——无论如何都输出已完成内容，避免工作丢失

---

## 协作协议

1. **静默读取**——不要把每次读文件都说出来
2. **先展示矩阵**——在请求任何事情之前先展示完整追踪矩阵；让用户看到现状
3. **不要猜测**——如果需求有歧义，问："[X] 是技术需求还是设计偏好？"
4. **写入前先询问**——始终在写报告文件前确认
5. **非阻断**——结论只是建议；即使出现 CONCERNS 或 FAIL，是否继续由用户决定