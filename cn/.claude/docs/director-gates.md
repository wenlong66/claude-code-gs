# 总监门禁 — 共享评审模式

本文档定义了适用于所有总监和负责人评审的标准门禁提示，覆盖每个工作流阶段。各技能应引用本文档中的门禁 ID，而不是将完整提示直接内联——这样在提示更新时可以避免漂移。

**范围**：全部 7 个生产阶段（概念 → 发布）、全部 3 位 Tier 1 总监、所有关键 Tier 2 负责人。任何技能、团队编排器或工作流都可以调用这些门禁。

---

## 如何使用本文档

在任何技能中，用引用替换内联的总监提示：

```
通过 Task 生成 `creative-director`，使用门禁 **CD-PILLARS**，来源为
`.claude/docs/director-gates.md`。
```

传入该门禁 **Context to pass** 字段下列出的上下文，然后按照下方的 **Verdict handling** 规则处理裁定结果。

---

## 审查模式

审查强度决定是否运行总监门禁。它可以全局设置（跨会话持久化），也可以在单次技能运行时覆盖。

**全局配置**：`production/review-mode.txt` — 单个词：`full`、`lean` 或 `solo`。请在 `/start` 时设置一次。之后可随时直接编辑该文件更改。

**单次运行覆盖**：任何使用门禁的技能都可以接受参数 `--review [full|lean|solo]`。这只会覆盖该次运行的全局配置。

示例：
```
/brainstorm space horror           → 使用全局模式
/brainstorm space horror --review full   → 本次强制 full 模式
/architecture-decision --review solo     → 本次跳过所有门禁
```

| 模式 | 运行内容 | 最适合 |
|------|-----------|--------|
| `full` | 所有门禁都激活 — 每个工作流步骤都会被审查 | 团队、学习型用户，或当你希望每一步都获得完整的总监反馈时 |
| `lean` | 仅运行 PHASE-GATE（`/gate-check`）— 跳过单技能门禁 | **默认** — 适合独立开发者和小团队；总监只在里程碑时审查 |
| `solo` | 任何地方都不运行总监门禁 | Game jam、原型、追求最快速度 |

**检查模式——在每次门禁生成前应用：**

```
在生成门禁 [GATE-ID] 前：
1. 如果技能以 --review [mode] 调用，则使用该模式
2. 否则读取 production/review-mode.txt
3. 否则默认 full

应用解析后的模式：
- solo → 跳过所有门禁。备注："[GATE-ID] skipped — Solo mode"
- lean → 跳过，除非这是 PHASE-GATE（CD-PHASE-GATE、TD-PHASE-GATE、PR-PHASE-GATE）
         备注："[GATE-ID] skipped — Lean mode"
- full → 正常生成
```

---

## 调用模式（可复制到任何技能中）

**强制要求：在每次门禁生成前都要先解析审查模式。** 绝不要在未检查的情况下生成门禁。解析后的模式在每次技能运行时只确定一次：
1. 如果技能以 `--review [mode]` 调用，则使用该模式
2. 否则读取 `production/review-mode.txt`
3. 否则默认 `lean`

应用解析后的模式：
- `solo` → **跳过所有门禁**。在输出中注明：`[GATE-ID] skipped — Solo mode`
- `lean` → **跳过，除非这是 PHASE-GATE**（CD-PHASE-GATE、TD-PHASE-GATE、PR-PHASE-GATE、AD-PHASE-GATE）。注明：`[GATE-ID] skipped — Lean mode`
- `full` → 正常生成

```
# 先应用模式检查，然后：
通过 Task 生成 `[agent-name]`：
- Gate: [GATE-ID]（见 .claude/docs/director-gates.md）
- Context: [该门禁下列出的字段]
- 在继续之前等待裁定结果。
```

用于并行生成（同一门禁点需要多个总监时）：

```
# 先对每个门禁应用模式检查，然后生成所有保留下来的：
通过 Task 同时生成全部 [N] 个智能体——必须在等待任何结果前发出所有 Task 调用。收集全部裁定后再继续。
```

---

## 标准裁定格式

所有门禁返回以下三种裁定之一。技能必须处理全部三种：

| 裁定 | 含义 | 默认动作 |
|------|------|---------|
| **APPROVE / READY** | 没有问题。继续。 | 继续工作流 |
| **CONCERNS [list]** | 存在问题，但不阻塞。 | 通过 `AskUserQuestion` 向用户呈现选项：`Revise flagged items` / `Accept and proceed` / `Discuss further` |
| **REJECT / NOT READY [blockers]** | 存在阻塞问题。不要继续。 | 将阻塞项呈现给用户。在问题解决前不要写文件或推进阶段。 |

**升级规则**：当多个总监并行生成时，采用最严格的裁定——只要有一个 NOT READY，就会覆盖所有 READY 裁定。

---

## 记录门禁结果

门禁解析完成后，将裁定记录到相关文档的状态标题中：

```markdown
> **[Director] Review ([GATE-ID])**: APPROVED [date] / CONCERNS (accepted) [date] / REVISED [date]
```

对于阶段门禁，按需要记录在 `docs/architecture/architecture.md` 或 `production/session-state/active.md` 中。

---

## Tier 1 — 创意总监门禁

Agent: `creative-director` | Model tier: Opus | Domain: Vision, pillars, player experience

---

### CD-PILLARS — 支柱压力测试

**Trigger**：在游戏支柱和反支柱定义之后（brainstorm 第 4 阶段，或任何支柱被修订的时候）

**Context to pass**：
- 完整的支柱集合，包含名称、定义和设计测试
- 反支柱列表
- 核心幻想陈述
- 独特卖点（"Like X, AND ALSO Y"）

**Prompt**：
> "Review these game pillars. Are they falsifiable — could a real design decision
> actually fail this pillar? Do they create meaningful tension with each other? Do
> they differentiate this game from its closest comparables? Would they help resolve
> a design disagreement in practice, or are they too vague to be useful? Return
> specific feedback for each pillar and an overall verdict: APPROVE (strong), CONCERNS
> [list] (needs sharpening), or REJECT (weak — pillars do not carry weight)."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

### CD-GDD-ALIGN — GDD 支柱一致性检查

**Trigger**：在系统 GDD 完成后（design-system、quick-design，或任何产出 GDD 的工作流）

**Context to pass**：
- GDD 文件路径
- 游戏支柱（来自 `design/gdd/game-concept.md` 或 `design/gdd/game-pillars.md`）
- 本游戏的 MDA 美学目标
- 系统中陈述的 Player Fantasy 章节

**Prompt**：
> "Review this system GDD for pillar alignment. Does every section serve the stated
> pillars? Are there mechanics or rules that contradict or weaken a pillar? Does
> the Player Fantasy section match the game's core fantasy? Return APPROVE, CONCERNS
> [specific sections with issues], or REJECT [pillar violations that must be
> redesigned before this system is implementable]."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

### CD-SYSTEMS — 系统拆分愿景检查

**Trigger**：在 `/map-systems` 写入系统索引之后——在开始编写 GDD 前验证完整系统集

**Context to pass**：
- 系统索引路径（`design/gdd/systems-index.md`）
- 游戏支柱与核心幻想（来自 `design/gdd/game-concept.md`）
- 优先级层级分配（MVP / Vertical Slice / Alpha / Full Vision）
- 依赖图中识别出的任何高风险或瓶颈系统

**Prompt**：
> "Review this systems decomposition against the game's design pillars. Does the
> full set of MVP-tier systems collectively deliver the core fantasy? Are there
> systems whose mechanics don't serve any stated pillar — indicating they may be
> scope creep? Are there pillar-critical player experiences that have no system
> assigned to deliver them? Are any systems missing that the core loop requires?
> Return APPROVE (systems serve the vision), CONCERNS [specific gaps or
> misalignments with their pillar implications], or REJECT [fundamental gaps —
> the decomposition misses critical design intent and must be revised before GDD
> authoring begins]."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

### CD-NARRATIVE — 叙事一致性检查

**Trigger**：在叙事 GDD、世界观文档、对话规格或世界构建文档完成后（team-narrative、用于故事系统的 design-system、writer 交付物）

**Context to pass**：
- 文档文件路径
- 游戏支柱
- 叙事方向简报或语气指南（如果存在于 `design/narrative/`）
- 新文档所引用的任何现有 lore

**Prompt**：
> "Review this narrative content for consistency with the game's pillars and
> established world rules. Does the tone match the game's established voice? Are
> there contradictions with existing lore or world-building? Does the content serve
> the player experience pillar? Return APPROVE, CONCERNS [specific inconsistencies],
> or REJECT [contradictions that break world coherence]."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

### CD-PLAYTEST — 玩家体验验证

**Trigger**：在游玩测试报告生成后（`/playtest-report`），或在任何产出玩家反馈的会话之后

**Context to pass**：
- 游玩测试报告文件路径
- 游戏支柱与核心幻想陈述
- 正在验证的具体假设

**Prompt**：
> "Review this playtest report against the game's design pillars and core fantasy.
> Is the player experience matching the intended fantasy? Are there systematic issues
> that represent pillar drift — mechanics that feel fine in isolation but undermine
> the intended experience? Return APPROVE (core fantasy is landing), CONCERNS [gaps
> between intended and actual experience], or REJECT [core fantasy is not present —
> redesign needed before further playtesting]."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

### CD-PHASE-GATE — 阶段切换时的创意就绪性

**Trigger**：始终在 `/gate-check` 时触发——与 TD-PHASE-GATE 和 PR-PHASE-GATE 并行生成

**Context to pass**：
- 目标阶段名称
- 所有现有工件列表（文件路径）
- 游戏支柱与核心幻想

**Prompt**：
> "Review the current project state for [target phase] gate readiness from a
> creative direction perspective. Are the game pillars faithfully represented in
> all design artifacts? Does the current state preserve the core fantasy? Are there
> any design decisions across GDDs or architecture that compromise the intended
> player experience? Return READY, CONCERNS [list], or NOT READY [blockers]."

**Verdicts**：READY / CONCERNS / NOT READY

---

## Tier 1 — 技术总监门禁

Agent: `technical-director` | Model tier: Opus | Domain: Architecture, engine risk, performance

---

### TD-SYSTEM-BOUNDARY — 系统边界架构审查

**Trigger**：在 `/map-systems` 第 3 阶段依赖映射达成一致之后、但在开始编写 GDD 之前——在团队投入编写 GDD 前验证系统结构在架构上是否合理

**Context to pass**：
- 系统索引路径（如果索引尚未写入，则使用依赖图摘要）
- 层级分配（Foundation / Core / Feature / Presentation / Polish）
- 完整依赖图（每个系统依赖什么）
- 标记出的任何瓶颈系统（依赖者很多）
- 找到的任何循环依赖及其拟议解决方案

**Prompt**：
> "Review this systems decomposition from an architectural perspective before GDD
> authoring begins. Are the system boundaries clean — does each system own a
> distinct concern with minimal overlap? Are there God Object risks (systems doing
> too much)? Does the dependency ordering create implementation-sequencing problems?
> Are there implicit shared-state problems in the proposed boundaries that will
> cause tight coupling when implemented? Are any Foundation-layer systems actually
> dependent on Feature-layer systems (inverted dependency)? Return APPROVE
> (boundaries are architecturally sound — proceed to GDD authoring), CONCERNS
> [specific boundary issues to address in the GDDs themselves], or REJECT
> [fundamental boundary problems — the system structure will cause architectural
> issues and must be restructured before any GDD is written]."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

### TD-FEASIBILITY — 技术可行性评估

**Trigger**：在范围/可行性阶段识别出最大的技术风险之后（brainstorm 第 6 阶段、quick-design，或任何带有技术未知数的早期概念）

**Context to pass**：
- 概念的核心循环描述
- 目标平台
- 引擎选择（或 "undecided"）
- 已识别的技术风险列表

**Prompt**：
> "Review these technical risks for a [genre] game targeting [platform] using
> [engine or 'undecided engine']. Flag any HIGH risk items that could invalidate
> the concept as described, any risks that are engine-specific and should influence
> the engine choice, and any risks that are commonly underestimated by solo
> developers. Return VIABLE (risks are manageable), CONCERNS [list with mitigation
> suggestions], or HIGH RISK [blockers that require concept or scope revision]."

**Verdicts**：VIABLE / CONCERNS / HIGH RISK

---

### TD-ARCHITECTURE — 架构签核

**Trigger**：在主架构文档草拟完成后（`/create-architecture` 第 7 阶段），以及在任何重大架构修订之后

**Context to pass**：
- 架构文档路径（`docs/architecture/architecture.md`）
- 技术需求基线（TR-IDs 及数量）
- 带状态的 ADR 列表
- 引擎知识缺口清单

**Prompt**：
> "Review this master architecture document for technical soundness. Check: (1) Is
> every technical requirement from the baseline covered by an architectural decision?
> (2) Are all HIGH risk engine domains explicitly addressed or flagged as open
> questions? (3) Are the API boundaries clean, minimal, and implementable? (4) Are
> Foundation layer ADR gaps resolved before implementation begins? Return APPROVE,
> CONCERNS [list], or REJECT [blockers that must be resolved before coding starts]."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

### TD-ADR — 架构决策审查

**Trigger**：在单个 ADR 编写完成后（`/architecture-decision`），在其标记为 Accepted 之前

**Context to pass**：
- ADR 文件路径
- 该领域的引擎版本和知识缺口风险等级
- 相关 ADR（如果有）

**Prompt**：
> "Review this Architecture Decision Record. Does it have a clear problem statement
> and rationale? Are the rejected alternatives genuinely considered? Does the
> Consequences section acknowledge the trade-offs honestly? Is the engine version
> stamped? Are post-cutoff API risks flagged? Does it link to the GDD requirements
> it covers? Return APPROVE, CONCERNS [specific gaps], or REJECT [the decision is
> underspecified or makes unsound technical assumptions]."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

### TD-ENGINE-RISK — 引擎版本风险审查

**Trigger**：在做出涉及引擎 API 截止点之后的架构决策时，或在最终确定任何引擎特定实现方案之前

**Context to pass**：
- 正在使用的具体 API 或功能
- 引擎版本与 LLM 知识截止点（来自 `docs/engine-reference/[engine]/VERSION.md`）
- 破坏性变更或废弃 API 文档中的相关摘录

**Prompt**：
> "Review this engine API usage against the version reference. Is this API present
> in [engine version]? Has its signature, behaviour, or namespace changed since the
> LLM knowledge cutoff? Are there known deprecations or post-cutoff alternatives?
> Return APPROVE (safe to use as described), CONCERNS [verify before implementing],
> or REJECT [API has changed — provide corrected approach]."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

### TD-PHASE-GATE — 阶段切换时的技术就绪性

**Trigger**：始终在 `/gate-check` 时触发——与 CD-PHASE-GATE 和 PR-PHASE-GATE 并行生成

**Context to pass**：
- 目标阶段名称
- 架构文档路径（如果存在）
- 引擎参考路径
- ADR 列表

**Prompt**：
> "Review the current project state for [target phase] gate readiness from a
> technical direction perspective. Is the architecture sound for this phase? Are
> all high-risk engine domains addressed? Are performance budgets realistic and
> documented? Are Foundation-layer decisions complete enough to begin implementation?
> Return READY, CONCERNS [list], or NOT READY [blockers]."

**Verdicts**：READY / CONCERNS / NOT READY

---

## Tier 1 — 制作总监门禁

Agent: `producer` | Model tier: Opus | Domain: Scope, timeline, dependencies, production risk

---

### PR-SCOPE — 范围与时间线验证

**Trigger**：在范围层级定义之后（brainstorm 第 6 阶段、quick-design，或任何产出 MVP 定义和时间估算的工作流）

**Context to pass**：
- 完整的愿景范围描述
- MVP 定义
- 时间线估算
- 团队规模（solo / small team / 等）
- 范围层级（如果时间耗尽会交付什么）

**Prompt**：
> "Review this scope estimate. Is the MVP achievable in the stated timeline for
> the stated team size? Are the scope tiers correctly ordered by risk — does each
> tier deliver a shippable product if work stops there? What is the most likely
> cut point under time pressure, and is it a graceful fallback or a broken product?
> Return REALISTIC (scope matches capacity), OPTIMISTIC [specific adjustments
> recommended], or UNREALISTIC [blockers — timeline or MVP must be revised]."

**Verdicts**：REALISTIC / OPTIMISTIC / UNREALISTIC

---

### PR-SPRINT — 冲刺可行性审查

**Trigger**：在最终确定冲刺计划（`/sprint-plan`）之前，以及在任何冲刺中期范围变更之后

**Context to pass**：
- 拟定的冲刺故事列表（标题、估算、依赖）
- 团队容量（可用小时数）
- 当前冲刺待办债务（如果有）
- 里程碑约束

**Prompt**：
> "Review this sprint plan for feasibility. Is the story load realistic for the
> available capacity? Are stories correctly ordered by dependency? Are there hidden
> dependencies between stories that could block the sprint mid-way? Are any stories
> underestimated given their technical complexity? Return REALISTIC (plan is
> achievable), CONCERNS [specific risks], or UNREALISTIC [sprint must be
> descoped — identify which stories to defer]."

**Verdicts**：REALISTIC / CONCERNS / UNREALISTIC

---

### PR-MILESTONE — 里程碑风险评估

**Trigger**：在里程碑审查（`/milestone-review`）、冲刺中期回顾，或当提出的范围变更会影响里程碑时

**Context to pass**：
- 里程碑定义与目标日期
- 当前完成百分比
- 被阻塞故事数量
- 冲刺速度数据（如果可用）

**Prompt**：
> "Review this milestone status. Based on current velocity and blocked story count,
> will this milestone hit its target date? What are the top 3 production risks
> between now and the milestone? Are there scope items that should be cut to protect
> the milestone date vs. items that are non-negotiable? Return ON TRACK, AT RISK
> [specific mitigations], or OFF TRACK [date must slip or scope must cut — provide
> both options]."

**Verdicts**：ON TRACK / AT RISK / OFF TRACK

---

### PR-EPIC — Epic 结构可行性审查

**Trigger**：在 `/create-epics` 定义完 epics 之后、拆分 stories 之前——在调用 `/create-stories` 前验证 epic 结构是否可生产

**Context to pass**：
- Epic 定义文件路径（刚创建的所有 epics）
- Epic 索引路径（`production/epics/index.md`）
- 里程碑时间线与目标日期
- 团队容量（solo / small team / size）
- 被拆分 epic 的层级（Foundation / Core / Feature / etc.）

**Prompt**：
> "Review this epic structure for production feasibility before story breakdown
> begins. Are the epic boundaries scoped appropriately — could each epic realistically
> complete before a milestone deadline? Are epics correctly ordered by system
> dependency — does any epic require another epic's output before it can start?
> Are any epics underscoped (too small, should merge) or overscoped (too large,
> should split into 2-3 focused epics)? Are the Foundation-layer epics scoped to
> allow Core-layer epics to begin at the start of the next sprint after Foundation
> completes? Return REALISTIC (epic structure is producible), CONCERNS [specific
> structural adjustments before stories are written], or UNREALISTIC [epics must
> be split, merged, or reordered — story breakdown cannot begin until resolved]."

**Verdicts**：REALISTIC / CONCERNS / UNREALISTIC

---

### PR-PHASE-GATE — 阶段切换时的制作就绪性

**Trigger**：始终在 `/gate-check` 时触发——与 CD-PHASE-GATE 和 TD-PHASE-GATE 并行生成

**Context to pass**：
- 目标阶段名称
- 当前存在的冲刺与里程碑工件
- 团队规模与容量
- 当前被阻塞的故事数量

**Prompt**：
> "Review the current project state for [target phase] gate readiness from a
> production perspective. Is the scope realistic for the stated timeline and team
> size? Are dependencies properly ordered so the team can actually execute in
> sequence? Are there milestone or sprint risks that could derail the phase within
> the first two sprints? Return READY, CONCERNS [list], or NOT READY [blockers]."

**Verdicts**：READY / CONCERNS / NOT READY

---

## Tier 1 — 美术总监门禁

Agent: `art-director` | Model tier: Sonnet | Domain: Visual identity, art bible, visual production readiness

---

### AD-CONCEPT-VISUAL — 视觉识别锚点

**Trigger**：在游戏支柱锁定后（brainstorm 第 4 阶段），与 CD-PILLARS 并行

**Context to pass**：
- 游戏概念（电梯陈述、核心幻想、独特卖点）
- 完整的支柱集合，包含名称、定义和设计测试
- 目标平台（如果已知）
- 用户提到的任何参考游戏或视觉基准

**Prompt**：
> "Based on these game pillars and core concept, propose 2-3 distinct visual identity
> directions. For each direction provide: (1) a one-line visual rule that could guide
> all visual decisions (e.g., 'everything must move', 'beauty is in the decay'), (2)
> mood and atmosphere targets, (3) shape language (sharp/rounded/organic/geometric
> emphasis), (4) color philosophy (palette direction, what colors mean in this world).
> Be specific — avoid generic descriptions. One direction should directly serve the
> primary design pillar. Name each direction. Recommend which best serves the stated
> pillars and explain why."

**Verdicts**：CONCEPTS（多个有效选项——由用户选择） / STRONG（某个方向明显占优） / CONCERNS（支柱还不足以支持区分视觉识别方向）

---

### AD-ART-BIBLE — 美术圣经签核

**Trigger**：在美术圣经草拟完成后（`/art-bible`），在资源生产开始之前

**Context to pass**：
- 美术圣经路径（`design/art/art-bible.md`）
- 游戏支柱与核心幻想
- 平台与性能约束（如果已配置，则来自 `.claude/docs/technical-preferences.md`）
- brainstorm 中选定的视觉识别锚点（来自 `design/gdd/game-concept.md`）

**Prompt**：
> "Review this art bible for completeness and internal consistency. Does the color
> system match the mood targets? Does the shape language follow from the visual
> identity statement? Are the asset standards achievable within the platform
> constraints? Does the character design direction give artists enough to work from
> without over-specifying? Are there contradictions between sections? Would an
> outsourcing team be able to produce assets from this document without additional
> briefing? Return APPROVE (art bible is production-ready), CONCERNS [specific
> sections needing clarification], or REJECT [fundamental inconsistencies that must
> be resolved before asset production begins]."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

### AD-PHASE-GATE — 阶段切换时的视觉就绪性

**Trigger**：始终在 `/gate-check` 时触发——与 CD-PHASE-GATE、TD-PHASE-GATE 和 PR-PHASE-GATE 并行生成

**Context to pass**：
- 目标阶段名称
- 所有现有美术/视觉工件列表（文件路径）
- 来自 `design/gdd/game-concept.md` 的视觉识别锚点（如果存在）
- 美术圣经路径（如果存在：`design/art/art-bible.md`）

**Prompt**：
> "Review the current project state for [target phase] gate readiness from a visual
> direction perspective. Is the visual identity established and documented at the
> level this phase requires? Are the right visual artifacts in place? Would visual
> teams be able to begin their work without visual direction gaps that cause costly
> rework later? Are there visual decisions that are being deferred past their latest
> responsible moment? Return READY, CONCERNS [specific visual direction gaps that
> could cause production rework], or NOT READY [visual blockers that must exist
> before this phase can succeed — specify what artifact is missing and why it
> matters at this stage]."

**Verdicts**：READY / CONCERNS / NOT READY

---

## Tier 2 — 负责人门禁

这些门禁由编排技能和高级技能在需要某领域专家进行可行性签核时调用。Tier 2 负责人使用 Sonnet（默认）。

---

### LP-FEASIBILITY — 主程序员实现可行性

**Trigger**：在主架构文档写完后（`/create-architecture` 第 7b 阶段），或提出新的架构模式时

**Context to pass**：
- 架构文档路径
- 技术需求基线摘要
- 带状态的 ADR 列表

**Prompt**：
> "Review this architecture for implementation feasibility. Flag: (a) any decisions
> that would be difficult or impossible to implement with the stated engine and
> language, (b) any missing interface definitions that programmers would need to
> invent themselves, (c) any patterns that create avoidable technical debt or
> that contradict standard [engine] idioms. Return FEASIBLE, CONCERNS [list], or
> INFEASIBLE [blockers that make this architecture unimplementable as written]."

**Verdicts**：FEASIBLE / CONCERNS / INFEASIBLE

---

### LP-CODE-REVIEW — 主程序员代码审查

**Trigger**：在开发故事实现完成后（`/dev-story`、`/story-done`），或作为 `/code-review` 的一部分

**Context to pass**：
- 实现文件路径
- 故事文件路径（用于验收标准）
- 相关 GDD 章节
- 约束该系统的 ADR

**Prompt**：
> "Review this implementation against the story acceptance criteria and governing
> ADR. Does the code match the architecture boundary definitions? Are there
> violations of the coding standards or forbidden patterns? Is the public API
> testable and documented? Are there any correctness issues against the GDD rules?
> Return APPROVE, CONCERNS [specific issues], or REJECT [must be revised before merge]."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

### QL-STORY-READY — QA 负责人故事就绪检查

**Trigger**：在故事被接受进冲刺之前——由 `/create-stories`、`/story-readiness` 和 `/sprint-plan` 在故事选择期间调用

**Context to pass**：
- 故事文件路径
- 故事类型（Logic / Integration / Visual/Feel / UI / Config/Data）
- 验收标准列表（逐字取自故事）
- 该故事覆盖的 GDD 需求（TR-ID 和文本）

**Prompt**：
> "Review this story's acceptance criteria for testability before it enters the
> sprint. Are all criteria specific enough that a developer would know unambiguously
> when they are done? For Logic-type stories: can every criterion be verified with
> an automated test? For Integration stories: is each criterion observable in a
> controlled test environment? Flag criteria that are too vague to implement
> against, and flag criteria that require a full game build to test (mark these
> DEFERRED, not BLOCKED). Return ADEQUATE (criteria are implementable as written),
> GAPS [specific criteria needing refinement], or INADEQUATE [criteria are too
> vague — story must be revised before sprint inclusion]."

**Verdicts**：ADEQUATE / GAPS / INADEQUATE

---

### QL-TEST-COVERAGE — QA 负责人测试覆盖审查

**Trigger**：在实现故事完成后、在标记 epic 完成之前，或在 `/gate-check` 的 Production → Polish 时

**Context to pass**：
- 已实现故事及其故事类型列表（Logic / Integration / Visual / UI / Config）
- `tests/` 中的测试文件路径
- 该系统的 GDD 验收标准

**Prompt**：
> "Review the test coverage for these implementation stories. Are all Logic stories
> covered by passing unit tests? Are Integration stories covered by integration
> tests or documented playtests? Are the GDD acceptance criteria each mapped to at
> least one test? Are there untested edge cases from the GDD Edge Cases section?
> Return ADEQUATE (coverage meets standards), GAPS [specific missing tests], or
> INADEQUATE [critical logic is untested — do not advance]."

**Verdicts**：ADEQUATE / GAPS / INADEQUATE

---

### ND-CONSISTENCY — 叙事总监一致性检查

**Trigger**：在撰写完作者交付物（对话、lore、物品描述）后，或当设计决策产生叙事影响时

**Context to pass**：
- 文档或内容文件路径
- 叙事圣经或语气指南路径（如果存在）
- 相关世界构建规则
- 受影响的角色或派系资料

**Prompt**：
> "Review this narrative content for internal consistency and adherence to
> established world rules. Are character voices consistent with their established
> profiles? Does the lore contradict any established facts? Is the tone consistent
> with the game's narrative direction? Return APPROVE, CONCERNS [specific
> inconsistencies to fix], or REJECT [contradictions that break the narrative
> foundation]."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

### AD-VISUAL — 美术总监视觉一致性审查

**Trigger**：在美术方向决策完成后、引入新的资源类型时，或当技术美术决策影响视觉风格时

**Context to pass**：
- 美术圣经路径（如果存在于 `design/art-bible.md`）
- 正在审查的具体资源类型、风格决策或视觉方向
- 参考图片或风格描述
- 平台与性能约束

**Prompt**：
> "Review this visual direction decision for consistency with the established art
> style and production constraints. Does it match the art bible? Is it achievable
> within the platform's performance budget? Are there asset pipeline implications
> that create technical risk? Return APPROVE, CONCERNS [specific adjustments], or
> REJECT [style violation or production risk that must be resolved first]."

**Verdicts**：APPROVE / CONCERNS / REJECT

---

## 并行门禁协议

当某个工作流在同一检查点需要多个总监时（最常见于 `/gate-check`），应同时生成所有智能体：

```
并行生成（在等待任何结果之前发出全部 Task 调用）：
1. creative-director  → gate CD-PHASE-GATE
2. technical-director → gate TD-PHASE-GATE
3. producer           → gate PR-PHASE-GATE
4. art-director       → gate AD-PHASE-GATE

收集全部四个裁定，然后应用升级规则：
- 任何 NOT READY / REJECT → 整体裁定最低为 FAIL
- 任何 CONCERNS → 整体裁定最低为 CONCERNS
- 所有 READY / APPROVE → 可判定为 PASS（仍需通过工件检查）
```

---

## 添加新门禁

当为新技能或新工作流需要一个新门禁时：

1. 分配一个门禁 ID：`[DIRECTOR-PREFIX]-[DESCRIPTIVE-SLUG]`
   - 前缀：`CD-` `TD-` `PR-` `LP-` `QL-` `ND-` `AD-`
   - 为新智能体添加新前缀：`AudioDirector` → `AU-`，`UX` → `UX-`
2. 在相应总监章节下添加该门禁，并包含全部五个字段：
   Trigger、Context to pass、Prompt、Verdicts，以及任何特殊处理说明
3. 在技能中只按 ID 引用——不要把提示文本复制进技能

---

## 各阶段门禁覆盖

| 阶段 | 必需门禁 | 可选门禁 |
|-------|---------|---------|
| **Concept** | CD-PILLARS, AD-CONCEPT-VISUAL | TD-FEASIBILITY, PR-SCOPE |
| **Systems Design** | TD-SYSTEM-BOUNDARY, CD-SYSTEMS, PR-SCOPE, CD-GDD-ALIGN（每个 GDD） | ND-CONSISTENCY, AD-VISUAL |
| **Technical Setup** | TD-ARCHITECTURE, TD-ADR（每个 ADR）, LP-FEASIBILITY, AD-ART-BIBLE | TD-ENGINE-RISK |
| **Pre-Production** | PR-EPIC, QL-STORY-READY（每个 story）, PR-SPRINT, 所有四个 PHASE-GATE（通过 gate-check） | CD-PLAYTEST |
| **Production** | LP-CODE-REVIEW（每个 story）, QL-STORY-READY, PR-SPRINT（每个 sprint） | PR-MILESTONE, QL-TEST-COVERAGE, AD-VISUAL |
| **Polish** | QL-TEST-COVERAGE, CD-PLAYTEST, PR-MILESTONE | AD-VISUAL |
| **Release** | 所有四个 PHASE-GATE（通过 gate-check） | QL-TEST-COVERAGE |
