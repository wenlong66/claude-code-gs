---
name: review-all-gdds
description: "进行全局跨 GDD 一致性与游戏设计审查。一次性读取所有系统 GDD，检查它们之间是否存在矛盾、过时引用、ownership 冲突、公式不兼容，以及游戏设计理论问题（dominant strategies、经济失衡、认知负荷、pillar drift）。在所有 MVP GDD 写完后、architecture 开始前运行。"
argument-hint: "[focus: full | consistency | design-theory | since-last-review]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash, AskUserQuestion, Task
model: opus
---

# Review All GDDs

这个技能会一次性读取每份系统 GDD，并执行两类单独的审查，这两类审查都无法在单份 GDD 内孤立完成：

1. **Cross-GDD Consistency** —— 文档之间的矛盾、过时引用和 ownership 冲突
2. **Game Design Holism** —— 只有把所有系统放在一起看时才会显现的问题：dominant strategies、失衡的经济、认知过载、pillar drift、相互竞争的 progression loop

**这与 `/design-review` 不同**，后者只审查单个 GDD 的内部完整性。这个技能审查的是所有 GDD 之间的*关系*。

**何时运行：**
- 所有 MVP-tier GDD 都分别获批之后
- 任何 GDD 在 production 中期发生重大修订后
- 在 `/create-architecture` 开始之前（基于不一致 GDD 构建的架构也会继承这些不一致）

**参数模式：**

**Focus:** `$ARGUMENTS[0]`（空 = `full`）

- **无参数 / `full`**：同时执行 consistency 和 design theory 两个检查
- **`consistency`**：仅做跨 GDD 一致性检查（更快）
- **`design-theory`**：仅做游戏设计整体性检查
- **`since-last-review`**：仅审查自上次 review 报告以来修改过的 GDD（基于 git）

---

## 第 1 阶段：加载全部内容

### Phase 1a — L0：摘要扫描（快速、低 token）

在读取任何完整文档之前，先用 Grep 从所有 GDD 文件中提取 `## Summary` 章节：

```
Grep pattern="## Summary" glob="design/gdd/*.md" output_mode="content" -A 5
```

向用户展示清单：
```
Found [N] GDDs. Summaries:
  • combat.md — [summary text]
  • inventory.md — [summary text]
  ...
```

对于 `since-last-review` 模式：运行 `git log --name-only`，找出自上次 review 报告文件写入以来被修改的 GDD。在做任何完整读取前，先通过摘要告诉用户哪些 GDD 在范围内。只对这些 GDD 以及它们在 “Key deps” 中列出的依赖进行 L1。

### Phase 1b — Registry 预加载（快速基线）

在完整读取任何 GDD 之前，先检查 entity registry：

```
Read path="design/registry/entities.yaml"
```

如果 registry 存在且有条目，将其作为**预构建冲突基线**：其中包含已知实体、物品、公式和常量，以及它们的权威值和来源 GDD。在 Phase 2 中，先 grep 已注册名称——这比在不确定要找什么之前就完整读取所有 GDD 更快。

如果 registry 为空或不存在：继续不使用它。在报告中注明：
"Entity registry is empty — consistency checks rely on full GDD reads only.
Run `/consistency-check` after this review to populate the registry."

### Phase 1c — L1/L2：完整文档加载

完整读取范围内的文档：

1. `design/gdd/game-concept.md` —— 游戏愿景、核心循环、MVP 定义
2. `design/gdd/game-pillars.md`（如果存在）—— 设计支柱与反支柱
3. `design/gdd/systems-index.md` —— 权威系统列表、层级、依赖、状态
4. `design/gdd/` 中**所有在范围内的系统 GDD** —— 完整读取（跳过 game-concept.md 和 systems-index.md——它们已在上面读取）

报告："Loaded [N] system GDDs covering [M] systems. Pillars: [list]. Anti-pillars: [list]."

如果系统 GDD 少于 2 个，停止：
> "Cross-GDD review requires at least 2 system GDDs. Write more GDDs first,
> then re-run `/review-all-gdds`."

---

### 并行执行

Phase 2（Consistency）和 Phase 3（Design Theory）是独立的——它们读取相同的 GDD 输入，但生成不同的报告。应同时并行 spawn 两个 Task agent，而不是等 Phase 2 结束后再开始 Phase 3。收齐两个结果后，再写合并报告。

---

## 第 2 阶段：跨 GDD 一致性

按文档对之间和文档组之间逐一检查矛盾与缺口。

### 2a：依赖双向性

对每个 GDD 的 Dependencies 章节，检查其中列出的每个依赖是否互相对应：
- 如果 GDD-A 写着 "depends on GDD-B"，检查 GDD-B 是否把 GDD-A 列为 dependent
- 如果 GDD-A 写着 "depended on by GDD-C"，检查 GDD-C 是否把 GDD-A 列为 dependency
- 任何单向依赖都标记为一致性问题

```
⚠️  Dependency Asymmetry
[system-a].md lists: Depends On → [system-b].md
[system-b].md does NOT list [system-a].md as a dependent
→ One of these documents has a stale dependency section
```

### 2b：规则矛盾

对于任一 GDD 中定义的游戏规则、机制或约束，检查其他 GDD 是否对同一情况定义了冲突规则：

扫描类别：
- **Floor/ceiling rules**：某 GDD 是否定义了输出的最小值？另一 GDD 是否说某系统能绕过这个 floor？这就是冲突。
- **Resource ownership**：如果两个 GDD 都定义共享资源如何积累或消耗，它们是否一致？
- **State transitions**：如果 GDD-A 描述角色死亡会发生什么，GDD-B 对同一事件的描述是否一致？
- **Timing**：如果 GDD-A 说 "X happens on the same frame"，GDD-B 是否假设它是异步的？
- **Stacking rules**：如果 GDD-A 说状态效果会叠加，GDD-B 是否假设不会叠加？

```
🔴 Rule Contradiction
[system-a].md: "Minimum [output] after reduction is [floor_value]"
[system-b].md: "[mechanic] bypasses [system-a]'s rules and can reduce [output] to 0"
→ These rules directly contradict. Which GDD is authoritative?
```

### 2c：过时引用

对每个跨文档引用（GDD-A 提到 GDD-B 中的某个机制、数值或系统名），验证被引用元素是否仍以同名且同等行为存在于 GDD-B：

- 如果 GDD-A 说 "combo multiplier from the combat system feeds into score"，检查 combat GDD 是否确实定义了一个输出到 score 的 combo multiplier
- 如果 GDD-A 引用 "the progression curve defined in [system].md"，检查 [system].md 是否真的有那条曲线，而不是不同的 progression model
- 如果 GDD-A 早于 GDD-B 写成，并假设了后来被 GDD-B 重新设计过的机制，则把 GDD-A 标记为包含过时引用

```
⚠️  Stale Reference
inventory.md (written first): "Item weight uses the encumbrance formula
  from movement.md"
movement.md (written later): Defines no encumbrance formula — uses a flat
  carry limit instead
→ inventory.md references a formula that doesn't exist
```

### 2d：数据和 tuning knob ownership 冲突

两个 GDD 不应同时宣称拥有同一个数据或 tuning knob。扫描所有 GDD 的 Tuning Knobs 章节并标记重复项：

```
⚠️  Ownership Conflict
[system-a].md Tuning Knobs: "[multiplier_name] — controls [output] scaling"
[system-b].md Tuning Knobs: "[multiplier_name] — scales [output] with [factor]"
→ Two GDDs define multipliers on the same output. Which owns the final value?
  This will produce either a double-application bug or a design conflict.
```

### 2e：公式兼容性

对于公式相互连接的 GDD（一个系统的输出作为另一个系统的输入），检查上游公式的输出范围是否落在下游公式期望的输入范围内：

- 如果 [system-a].md 输出在 [min]–[max] 之间，而 [system-b].md 设计接收 [min2]–[max2]，这种不匹配是故意的吗？
- 如果 economy GDD 期望 resource acquisition 处于范围 X，而 progression GDD 在范围 Y 产生它，经济会变得过于简单或根本无法获得——这是预期的吗？

把不兼容标记为 CONCERNS（需要设计判断，不一定就是错）：

```
⚠️  Formula Range Mismatch
[system-a].md: Max [output] = [value_a] (at max [condition])
[system-b].md: Base [input] = [value_b], max [input] = [value_c]
→ Late-[stage] [scenario] can resolve in a single [event].
  Is this intentional? If not, either [system-a]'s ceiling or [system-b]'s ceiling needs adjustment.
```

### 2f：Acceptance Criteria 交叉检查

扫描所有 GDD 的 Acceptance Criteria，检查是否互相矛盾：

- GDD-A criteria: "Player cannot die from a single hit"
- GDD-B criteria: "Boss attack deals 150% of player max health"

这两个 acceptance criteria 不可能同时通过。

---

## 第 3 阶段：游戏设计整体性

从游戏设计理论和玩家心理的角度，把所有 GDD 放在一起审视。这些问题单独看某个 GDD 时可能发现不了，因为必须看到所有系统才能看出来。

### 3a：进度循环竞争

游戏应该有一个占主导地位的 progression loop，让玩家感觉它才是游戏“真正的核心”，同时其他辅助循环为它服务。当多个系统都同样竞争成为主要进度驱动时，玩家就不知道这个游戏到底是关于什么的。

扫描所有 GDD，找出那些：
- 授予玩家主要资源（XP、等级、prestige、unlocks）
- 自称为 “core” 或 “main” loop
- 在深度和时间投入上与其他做同类事情的系统相当

```
⚠️  Competing Progression Loops
combat.md: Awards XP, unlocks abilities, is described as "the core loop"
crafting.md: Awards XP, unlocks recipes, is described as "the primary activity"
exploration.md: Awards XP, unlocks map areas, described as "the main driver"
→ Three systems all claim to be the primary progression loop and all award
  the same primary currency. Players will optimise one and ignore the others.
  Consider: one primary loop with the others as support systems.
```

### 3b：玩家注意力预算

统计一次典型 session 中，有多少系统需要玩家同时保持主动关注。每个 actively-managed 系统都会消耗注意力：

- Active = 玩家需要在游玩时持续对这个系统做决策
- Passive = 系统自动运行，玩家看结果但无需管理

同时 active 的系统超过 3–4 个，会让大多数玩家产生认知过载。给出数量，并在超过 4 个并发 active 系统时标记：

```
⚠️  Cognitive Load Risk
Simultaneously active systems during [core loop moment]:
  1. [system-a].md — [decision type] (active)
  2. [system-b].md — [resource management] (active)
  3. [system-c].md — [tracking] (active)
  4. [system-d].md — [item/action use] (active)
  5. [system-e].md — [cooldown/timer management] (active)
  6. [system-f].md — [coordination decisions] (active)
→ 6 simultaneously active systems during the core loop.
  Research suggests 3-4 is the comfortable limit for most players.
  Consider: which of these can be made passive or simplified?
```

### 3c：主导策略检测

主导策略会让其他策略失去意义——玩家会发现它，只用它，最后觉得整个游戏没意思。重点找：

- **Resource monopolies**：某种策略产生某个资源的速度显著快于其他所有策略
- **Risk-free power**：一种既高收益又低风险的策略（如果有高风险策略，它们就需要成比例更高的奖励）
- **No trade-offs**：某个选项在所有维度上都优于其他选项
- **Obvious optimal path**：如果任何进度选择“显然正确”，那其他就不是真选择

```
⚠️  Potential Dominant Strategy
combat.md: Ranged attacks deal 80% of melee damage with no risk
combat.md: Melee attacks deal 100% damage but require close range
→ Unless melee has a significant compensating advantage (AOE, stagger,
  resource regeneration), ranged is dominant — higher safety, only 20% less
  damage. Consider what melee offers that ranged cannot.
```

### 3d：经济循环分析

识别所有 GDD 中的资源（gold、XP、crafting materials、stamina、health、mana 等）。对每种资源，映射它的**sources**（玩家如何获得）和**sinks**（玩家如何消耗）。

标记危险的经济状态：

| Condition | Sign | Risk |
|-----------|------|------|
| **Infinite source, no sink** | Resource accumulates indefinitely | Late game becomes trivially easy |
| **Sink, no source** | Resource drains to zero | System becomes unavailable |
| **Source >> Sink** | Surplus accumulates | Resource becomes meaningless |
| **Sink >> Source** | Constant scarcity | Frustration and gatekeeping |
| **Positive feedback loop** | More resource → easier to earn more | Runaway leader, snowball |
| **No catch-up** | Falling behind accelerates deficit | Unrecoverable states |

```
🔴 Economic Imbalance: Unbounded Positive Feedback
gold economy:
  Sources: monster drops (scales with player power), merchant selling (unlimited)
  Sinks: equipment purchase (one-time), ability upgrades (finite count)
→ After equipment and abilities are purchased, gold has no sink.
  Infinite surplus. Gold becomes meaningless mid-game.
  Add ongoing gold sinks (upkeep, consumables, cosmetics, gambling).
```

### 3e：难度曲线一致性

当多个系统会随着玩家进度而缩放时，它们必须以兼容的方向和兼容的速率缩放。不匹配的 scaling 曲线会产生意外的难度尖峰或被过度简化。

对于每个随时间缩放的系统，提取：
- 什么在缩放（enemy health、player damage、resource cost、area size）
- 如何缩放（linear、exponential、stepped）
- 何时缩放（level、time、area）

对比所有 scaling 曲线。标记不匹配：

```
⚠️  Difficulty Curve Mismatch
combat.md: Enemy health scales exponentially with area (×2 per area)
progression.md: Player damage scales linearly with level (+10% per level)
→ By area 5, enemies have 32× base health; player deals ~1.5× base damage.
  The gap widens indefinitely. Late areas will become inaccessibly difficult
  unless the curves are reconciled.
```

### 3f：支柱对齐

每个系统都应该清楚地服务于至少一个设计支柱。没有服务任何支柱的系统属于“设计上的 scope creep”——它进入了游戏，但并不服务于游戏想成为的东西。

对每个 GDD 系统，检查它的 Player Fantasy 章节是否与设计支柱相对应。标记任何其宣称 fantasy 没有映射到任何支柱的系统：

```
⚠️  Pillar Drift
fishing-system.md: Player Fantasy — "peaceful, meditative activity"
Pillars: "Brutal Combat", "Tense Survival", "Emergent Stories"
→ The fishing system serves none of the three pillars. Either add a pillar
  that covers it, redesign it to serve an existing pillar, or cut it.
```

也要检查 anti-pillars——如果某个系统做了游戏明确说“不会做”的事情，就标记出来：

```
🔴 Anti-Pillar Violation
Anti-Pillar: "We will NOT have linear story progression — player defines their path"
main-quest.md: Defines a 12-chapter linear story with mandatory sequence
→ This system directly violates the defined anti-pillar.
```

### 3g：玩家幻想一致性

所有系统中的 player fantasies 应该彼此兼容——它们应共同强化一个统一的玩家身份。互相冲突的 player fantasies 会让玩家不知道自己在游戏里“是什么”。

```
⚠️  Player Fantasy Conflict
combat.md: "You are a ruthless, precise warrior — every kill is earned"
dialogue.md: "You are a charismatic diplomat — violence is always avoidable"
exploration.md: "You are a reckless adventurer — diving in without a plan"
→ Three systems present incompatible identities. Players will feel the game
  doesn't know what it wants them to be. Consider: do these fantasies serve
  the same core identity from different angles, or do they genuinely conflict?
```

---

## 第 4 阶段：跨系统场景演练

从玩家视角走一遍游戏，找出只有在多个系统交互边界才会出现的问题——单独分析各个 GDD 看不到这些问题。

### 4a：识别关键多系统时刻

扫描所有 GDD，找出 3–5 个最重要的玩家面对时刻，在这些时刻多个系统会同时激活。重点看：

- **Combat + Economy overlap**：击杀敌人掉资源、战斗中消耗资源、死亡/复活与经济状态交互
- **Progression + Difficulty overlap**：升级在战斗中触发、能力解锁改变战斗可行性、难度在进度节点上变化
- **Narrative + Gameplay overlap**：对话选择锁定/解锁机制、剧情节点打断资源循环、任务完成触发系统状态变化
- **3+ system chains**：任何会触发 System A，再传到 System B，再触发 System C 的玩家动作（这些是最高风险的交互路径）

在继续之前，先列出每个识别出的场景，并用一句话描述。

### 4b：逐个演练场景

对每个场景，明确逐步展开：

1. **Trigger** —— 由什么玩家动作或游戏事件开始？
2. **Activation order** —— 哪些系统激活，按什么顺序？
3. **Data flow** —— 每个系统输出什么，这个输出是否是下一个系统的有效输入？
4. **Player experience** —— 玩家在每一步看到、听到或感受到什么？
5. **Failure modes** —— 是否存在以下任一种？
   - **Race conditions**：两个系统同时修改同一状态
   - **Feedback loops**：System A 放大 System B，而 System B 又反过来放大 System A，且没有上限或缓冲
   - **Broken state transitions**：某系统假设了前一个系统可能已改变的状态（例如 combat 步骤后“玩家仍然活着”的假设）
   - **Contradictory messaging**：两个系统对同一事件给出相互矛盾的反馈（例如“成功”音效 + “失败” UI）
   - **Compounding difficulty spikes**：两个系统在同一进度点同时上调，叠加成预期外的难度增幅
   - **Reward conflicts**：两个系统都对同一触发作出奖励，合起来超过预期价值（double-dipping）
   - **Undefined behavior**：GDD 没有说明这种组合状态该怎么处理（两个系统的规则都没有覆盖）

```
Example walkthrough:
Scenario: Player kills elite enemy at level-up threshold during active quest

Trigger: Player lands killing blow on elite enemy
→ combat.md: awards kill XP (100 pts)
→ progression.md: XP total crosses level threshold → triggers level-up
  Output: new level, stat increases, ability unlock popup
→ quest.md: kill-count criterion met → triggers quest completion event
  Output: quest reward XP (500 pts), completion fanfare
→ progression.md (again): quest XP added → triggers SECOND level-up in same frame
  ⚠️  Data flow issue: quest.md awards XP without checking if a level-up
  is already in progress. progression.md has no guard against concurrent
  level-up events. Undefined behavior: does the player level up once or twice?
  Does the ability popup fire twice? Does the second level use the updated or
  pre-update stat baseline?
```

### 4c：标记场景问题

对演练中发现的每个问题，按严重程度分类：

- **BLOCKER**：undefined behavior、broken state transition 或矛盾的玩家信息——在这个场景里体验已经破坏或不连贯
- **WARNING**：compounding spikes、无上限 feedback loop、reward conflicts——体验还能运行，但会产生非预期结果
- **INFO**：轻微的顺序歧义或信息重叠——值得记录，但不太可能造成玩家可见问题

把所有发现加入输出报告的 **"Cross-System Scenario Issues"**。
每条发现必须引用：场景名称、涉及的具体系统、问题发生在哪一步，以及 failure mode 的性质。

---

## 第 5 阶段：输出审查报告

```
## Cross-GDD Review Report
Date: [date]
GDDs Reviewed: [N]
Systems Covered: [list]

---

### Consistency Issues

#### Blocking (must resolve before architecture begins)
🔴 [Issue title]
[What GDDs are involved, what the contradiction is, what needs to change]

#### Warnings (should resolve, but won't block)
⚠️  [Issue title]
[What GDDs are involved, what the concern is]

---

### Game Design Issues

#### Blocking
🔴 [Issue title]
[What the problem is, which GDDs are involved, design recommendation]

#### Warnings
⚠️  [Issue title]
[What the concern is, which GDDs are affected, recommendation]

---

### Cross-System Scenario Issues

Scenarios walked: [N]
[List scenario names]

#### Blockers
🔴 [Scenario name] — [Systems involved]
[Step where failure occurs, nature of the failure mode, what must be resolved]

#### Warnings
⚠️  [Scenario name] — [Systems involved]
[What the unintended outcome is, recommendation]

#### Info
ℹ️  [Scenario name] — [Systems involved]
[Minor ordering ambiguity or note]

---

### GDDs Flagged for Revision

| GDD | Reason | Type | Priority |
|-----|--------|------|----------|
| [system-a].md | Rule contradiction with [system-b].md | Consistency | Blocking |
| [system-c].md | Stale reference to nonexistent mechanic | Consistency | Blocking |
| [system-d].md | No pillar alignment | Design Theory | Warning |

---

### Verdict: [PASS / CONCERNS / FAIL]

PASS: No blocking issues. Warnings present but don't prevent architecture.
CONCERNS: Warnings present that should be resolved but are not blocking.
FAIL: One or more blocking issues must be resolved before architecture begins.

### If FAIL — required actions before re-running:
[Specific list of what must change in which GDD]
```

---

## 第 6 阶段：写报告并标记 GDD

使用 `AskUserQuestion` 请求写入权限：
- 提示："May I write this review to `design/gdd/gdd-cross-review-[date].md`?"
- 选项：`[A] Yes — write the report` / `[B] No — skip`

如果有任何 GDD 被标记为需要修订，再发起第二个 `AskUserQuestion`：
- 提示："Should I update the systems index to mark these GDDs as needing revision? ([list of flagged GDDs])"
- 选项：`[A] Yes — update systems index` / `[B] No — leave as-is`
- 如果同意：把每个被标记 GDD 在 systems-index.md 中的 Status 字段更新为 "Needs Revision"。
  （不要在 status 值后追加括号——其他技能会按精确字符串匹配 "Needs Revision"，括号会破坏匹配。）

### 会话状态更新

在写完报告（以及如果批准则更新 systems index）后，静默追加到 `production/session-state/active.md`：

    ## Session Extract — /review-all-gdds [date]
    - Verdict: [PASS / CONCERNS / FAIL]
    - GDDs reviewed: [N]
    - Flagged for revision: [comma-separated list, or "None"]
    - Blocking issues: [N — brief one-line descriptions, or "None"]
    - Recommended next: [the Phase 7 handoff action, condensed to one line]
    - Report: design/gdd/gdd-cross-review-[date].md

如果 `active.md` 不存在，就用这个 block 作为初始内容创建它。
在对话中确认："Session state updated."

---

## 第 7 阶段：交接

在所有文件写入完成后，使用 `AskUserQuestion` 打开一个收尾 widget。

在构建选项前，先检查项目状态：
- 有没有 Warning-level 且属于简单编辑的项（带有 "30-second edit"、"brief addition" 等标记）？→ 提供 inline quick-fix 选项
- 有没有 GDD 出现在 “Flagged for Revision” 表里？→ 为每个这样的 GDD 提供 /design-review 选项
- 读取 systems-index.md，找到下一个 Status: Not Started 的系统 → 提供 /design-system 选项
- 裁定是 PASS 还是 CONCERNS？→ 提供 /gate-check 或 /create-architecture

动态构建选项列表——只包含适用项：

**Option pool:**
- `[_] Apply quick fix: [W-XX description] in [gdd-name].md — [effort estimate]`（每个简单编辑 warning 一个选项；只适用于 Warning-level，不适用于 Blocking）
- `[_] Run /design-review [flagged-gdd-path] — address flagged warnings`（每个 flagged GDD 一个选项，如果有）
- `[_] Run /design-system [next-system] — next in design order`（始终包含，使用实际系统名）
- `[_] Run /create-architecture — begin architecture (verdict is PASS/CONCERNS)`（如果 verdict 不是 FAIL，则包含）
- `[_] Run /gate-check — validate Systems Design phase gate`（如果 verdict 是 PASS，则包含）
- `[_] Stop here`

只给包含的选项分配 A、B、C… 字母。把最能推进流程的选项标记为 `(recommended)`。

绝不要以纯文本结束这个技能。始终用这个 widget 收尾。

---

## 错误恢复协议

如果任何 spawned agent 返回 BLOCKED、报错，或无法完成：

1. **立即上报**：在继续之前报告 "[AgentName]: BLOCKED — [reason]"
2. **评估依赖**：如果被阻塞 agent 的输出是后续阶段所需，不要在没有用户输入前越过那个阶段
3. **通过 AskUserQuestion 提供选项**：
   - 跳过该 agent，并在最终报告中注明缺口
   - 用更窄的范围重试（更少的 GDD、单系统聚焦）
   - 停在这里，先解决阻塞
4. **始终产出部分报告** —— 输出已完成的内容，避免工作丢失

---

## 协作协议

1. **静默读取** —— 在展示任何内容前加载所有 GDD
2. **展示全部内容** —— 在请求任何操作前先展示完整的一致性和设计理论分析
3. **区分阻断与建议** —— 不是每个问题都要阻止 architecture；要清楚标明哪些会阻断
4. **不要替用户做设计决定** —— 只标记矛盾和选项，不要单方面判断哪个 GDD “正确”
5. **写入前先询问** —— 在写报告或更新 systems index 前确认
6. **要具体** —— 每个问题都必须引用准确的 GDD、章节和文本；不要给模糊警告
