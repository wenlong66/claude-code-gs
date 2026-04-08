---
name: ux-design
description: "为某个屏幕、流程或 HUD 进行按章节引导的 UX 规格撰写。读取游戏概念、玩家旅程和相关 GDD，以提供上下文感知的设计指导。输出 ux-spec.md（单屏/流程）或 hud-design.md，使用工作室模板。"
argument-hint: "[screen/flow name] or 'hud' or 'patterns'"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, Task
agent: ux-designer
---

当该技能被调用时：

## 1. 解析参数并确定模式

根据参数存在三种撰写模式：

| Argument | Mode | Output file |
|----------|------|-------------|
| `hud` | HUD design | `design/ux/hud.md` |
| `patterns` | Interaction pattern library | `design/ux/interaction-patterns.md` |
| 任何其他值（例如 `main-menu`、`inventory`） | 某个屏幕或流程的 UX spec | `design/ux/[argument].md` |
| 无参数 | 询问用户 | (见下文) |

**如果没有提供参数**，不要失败——改为询问。使用 `AskUserQuestion`：
- "我们今天要设计什么？"
  - 选项："一个具体的屏幕或流程（我来命名）"、"游戏 HUD"、"交互模式库"、"我不确定——帮我弄清楚"

如果用户选择“我来命名”或输入屏幕名称，将其规范化为文件名的 kebab-case（例如 "Main Menu" 变成 `main-menu`）。

---

## 2. 收集上下文（读取阶段）

在向用户提任何问题之前，先读取所有相关上下文。这个技能的价值在于带着信息进入。

### 2a：必读内容

- **Game concept**：读取 `design/gdd/game-concept.md` —— 如果缺失，提示：
  > "No game concept found. Run `/brainstorm` first to establish the game's
  > foundation before designing UX."
  > 如果用户要求，可以继续。

### 2b：玩家旅程

如果存在，读取 `design/player-journey.md`。对每个相关部分，提取：
- 这个屏幕出现在哪个 journey phase（或哪些 phases）？
- 玩家到达该屏幕时的情绪状态是什么？
- 该屏幕在旅程中服务了什么玩家需求？
- 这个屏幕承载了哪些关键时刻（来自 journey map）？

如果玩家旅程文件不存在，记录缺口并继续：
> "No player journey map found at `design/player-journey.md`. Designing without it
> means we'll be making assumptions about player context. Consider running a player
> journey session after this spec is drafted."

### 2c：GDD UI Requirements

Glob `design/gdd/*.md` 并 Grep `UI Requirements` 小节。读取任何在 UI Requirements 中按名称或类别引用了该屏幕的 GDD。

这些 GDD UI Requirements 是本规格的**需求输入**。将它们整理成一份必须满足的约束列表。

如果设计的是 HUD，则读取所有 GDD 的 UI Requirements 小节——HUD 会聚合每个系统的要求。

### 2d：现有 UX Specs

Glob `design/ux/*.md`，记录哪些屏幕已经有规格。对于会链接到当前屏幕或从当前屏幕跳转的屏幕，读取它们的 navigation/flow 小节，以找到本规格必须匹配的入口和出口点。

### 2e：交互模式库

如果 `design/ux/interaction-patterns.md` 存在，读取 pattern catalog index（模式名称及其一句话描述的列表）。不要读取完整 pattern 细节——只看目录。这能告诉你哪些模式已经存在，以便引用而不是重造轮子。

### 2f：Art Bible

检查 `design/art/art-bible.md`。如果找到，读取视觉方向小节。UX 布局必须与已经确立的美术承诺一致。

### 2g：无障碍要求

检查 `design/accessibility-requirements.md`。如果存在，则读取。规格必须满足那里承诺的无障碍层级。

### 2h：输入方式（来自项目配置）

读取 `.claude/docs/technical-preferences.md` 并提取 `## Input & Platform` 小节。将这些值保留在整个技能中使用——它们会驱动 Interaction Map，并影响无障碍要求：

- **Input Methods** — 例如 Keyboard/Mouse、Gamepad、Touch、Mixed
- **Primary Input** — 该游戏的主要输入方式
- **Gamepad Support** — Full / Partial / None
- **Touch Support** — Full / Partial / None
- **Target Platforms** — 用于安全区和宽高比决策

如果该小节未配置（`[TO BE CONFIGURED]`），询问一次：
> "Input methods aren't configured yet. What does this game target?"
> 选项："Keyboard/Mouse only"、"Gamepad only"、"Both (PC + Console)"、"Touch (mobile)"、"All of the above"
>
> （运行 `/setup-engine` 可将其永久保存，这样以后就不会再问。）

在本次会话剩余部分中记住该答案。不要在每个 section 或每个屏幕重复询问。

### 2i：呈现上下文摘要

在开始任何设计工作前，先向用户简要总结：

> **Designing: [Screen/Flow Name]**
> - Mode: [UX Spec / HUD Design / Pattern Library]
> - Journey phase(s): [来自 player-journey.md，或 "unknown — no journey map"]
> - GDD requirements feeding this spec: [数量和名称，或 "none found"]
> - Related screens already specced: [列表，或 "none yet"]
> - Known patterns available: [数量，或 "no pattern library yet"]
> - Accessibility tier: [来自 requirements doc，或 "not yet defined"]
> - Input methods: [来自 technical-preferences.md，或 "asked above"]

然后问："Anything else I should read before we start, or shall we proceed?"

---

## 2b. 改造模式检测

在创建 skeleton 之前，检查目标输出文件是否已存在。

Glob `design/ux/[filename].md`（其中 `[filename]` 是第 1 阶段解析后的输出路径）。

**如果文件已存在 —— 进入改造模式：**
- 完整读取该文件
- 对每个预期 section，检查内容是否有真实内容（不仅仅是 `[To be designed]` 占位符）或是否为空/占位
- 向用户呈现 section 状态摘要：

> "Found existing UX spec at `design/ux/[filename].md`. Here's what's already done:
>
> | Section | Status |
> |---------|--------|
> | Overview & Context | [Complete / Empty / Placeholder] |
> | Player Journey Integration | ... |
> | Screen Layout & Information Architecture | ... |
> | Interaction Model | ... |
> | Feedback & State Communication | ... |
> | Accessibility | ... |
> | Edge Cases & Error States | ... |
> | Open Questions | ... |
> |
> > I'll work on the [N] incomplete sections only — existing content will not be overwritten."

- 跳过第 3 节（创建 skeleton）——文件已经存在
- 在第 4 阶段（Section Authoring）中，只处理状态为 Empty 或 Placeholder 的 section
- 使用 `Edit` 原地填充占位符，而不是创建新的 skeleton

**如果文件不存在 —— 新建撰写模式：**
正常进入第 3 阶段（创建文件 skeleton）。

---

## 3. 创建文件 Skeleton

在用户确认后，**立即**创建输出文件，并写入空的 section 标题。这能确保增量写入有目标，且工作能在中断后继续。

询问："May I create the skeleton file at `design/ux/[filename].md`?"

---

### UX Spec Skeleton（屏幕或流程）

```markdown
# UX Spec: [Screen/Flow Name]

> **Status**: In Design
> **Author**: [user + ux-designer]
> **Last Updated**: [today's date]
> **Journey Phase(s)**: [from context]
> **Template**: UX Spec

---

## Purpose & Player Need

[To be designed]

---

## Player Context on Arrival

[To be designed]

---

## Navigation Position

[To be designed]

---

## Entry & Exit Points

[To be designed]

---

## Layout Specification

### Information Hierarchy

[To be designed]

### Layout Zones

[To be designed]

### Component Inventory

[To be designed]

### ASCII Wireframe

[To be designed]

---

## States & Variants

[To be designed]

---

## Interaction Map

[To be designed]

---

## Events Fired

[To be designed]

---

## Transitions & Animations

[To be designed]

---

## Data Requirements

[To be designed]

---

## Accessibility

[To be designed]

---

## Localization Considerations

[To be designed]

---

## Acceptance Criteria

[To be designed]

---

## Open Questions

[To be designed]
```

---

### HUD Design Skeleton

```markdown
# HUD Design

> **Status**: In Design
> **Author**: [user + ux-designer]
> **Last Updated**: [today's date]
> **Template**: HUD Design

---

## HUD Philosophy

[To be designed]

---

## Information Architecture

### Full Information Inventory

[To be designed]

### Categorization

[To be designed]

---

## Layout Zones

[To be designed]

---

## HUD Elements

[To be designed]

---

## Dynamic Behaviors

[To be designed]

---

## Platform & Input Variants

[To be designed]

---

## Accessibility

[To be designed]

---

## Open Questions

[To be designed]
```

---

### 交互模式库 Skeleton

```markdown
# Interaction Pattern Library

> **Status**: In Design
> **Author**: [user + ux-designer]
> **Last Updated**: [today's date]
> **Template**: Interaction Pattern Library

---

## Overview

[To be designed]

---

## Pattern Catalog

[To be designed]

---

## Patterns

[Individual pattern entries added here as they are defined]

---

## Gaps & Patterns Needed

[To be designed]

---

## Open Questions

[To be designed]
```

---

写完 skeleton 后，用以下内容更新 `production/session-state/active.md`：
- Task: Designing [screen/flow name] UX spec
- Current section: Starting (skeleton created)
- File: design/ux/[filename].md

---

## 4. 按章节撰写

按顺序逐个 section 处理。对于**每个 section**，都遵循以下循环：

```text
Context  ->  Questions  ->  Options  ->  Decision  ->  Draft  ->  Approval  ->  Write
```

1. **Context**：说明本 section 需要包含什么，并指出从第 2 阶段收集到的相关约束。
2. **Questions**：询问起草本 section 所需的信息。对受限选项使用 `AskUserQuestion`，对开放式探索使用对话文本。
3. **Options**：在存在设计选择时，给出 2-4 个方案及其利弊。在对话中解释原因，然后用 `AskUserQuestion` 记录决定。
4. **Decision**：用户选择一个方案或提供自定义方向。
5. **Draft**：在对话中写出 section 内容供审阅。显式标出任何暂定假设。
6. **Approval**："Does this capture it? Any changes before I write it to the file?"
7. **Write**：使用 `Edit` 将 `[To be designed]` 占位符替换为已批准内容。确认写入。

每写完一个 section，就更新 `production/session-state/active.md`。

---

### Section Guidance: UX Spec Mode

#### Section A: Purpose & Player Need

这是基础。其余所有决策都从这里展开。

**要问的问题**：
- "What player goal does this screen serve? What is the player trying to DO here?"
- "What would go wrong if this screen didn't exist or was hard to use?"
- "Complete this sentence: 'The player arrives at this screen wanting to ___. '"

交叉参考第 2 阶段收集到的玩家旅程上下文。陈述的目的必须与旅程阶段和情绪状态一致。

---

#### Section B: Player Context on Arrival

**要问的问题**：
- "When in the game does a player first encounter this screen?"
- "What were they just doing immediately before reaching this screen?"
- "What emotional state should the design assume? (calm, stressed, curious, time-pressured)"
- "Do players arrive at this screen voluntarily, or are they sent here by the game?"

如果玩家旅程文档存在，则提供将此内容映射到旅程阶段的帮助。

---

#### Section B2: Navigation Position

该屏幕位于游戏导航层级的哪里？这是一个一段式的定位地图——不是完整流程图。

**要问的问题**：
- "Is this screen accessed from the main menu, from pause, from within gameplay, or from another screen?"
- "Is it a top-level destination (always reachable) or a context-dependent one (only accessible in certain states)?"
- "Can the player reach this screen from more than one place in the game?"

呈现为："This screen lives at: [root] → [parent] → [this screen]"，并加上任何替代入口路径。

---

#### Section B3: Entry & Exit Points

绘制玩家进入和离开该屏幕的每一种方式。

**要问的问题**：
- "What are all the ways a player can reach this screen?"（列出每个触发：按钮、游戏事件、从其他屏幕重定向等）
- "What can the player do to exit? What happens when they do?"（返回键、确认动作、超时、游戏事件）
- "Are there any exits that are one-way — where the player cannot return to this screen without starting over?"

呈现为两张表：

| Entry Source | Trigger | Player carries this context |
|---|---|---|
| [screen/event] | [how] | [state/data they arrive with] |

| Exit Destination | Trigger | Notes |
|---|---|---|
| [screen/event] | [how] | [any irreversible state changes] |

---

#### Section C: Layout Specification

这是最大、交互最强的 section。按以下子部分推进：

**子部分 1 — Information Hierarchy**（在任何布局前先建立）：
- 让用户列出该屏幕必须传达的每一条信息。
- 然后让他们排序："玩家第一眼最需要看到的是什么？第二重要的是什么？哪些内容可以通过探索发现，而不是立即可见？"
- 在进入 zones 之前，先将形成的信息层级呈现给用户确认。

**子部分 2 — Layout Zones**：
- 基于信息层级，提出大致的屏幕区域（header、content area、action bar、sidebar 等）。
- 提供 2-3 种区域布局方案，并为每种方案给出理由。参考第 2 阶段收集到的平台和输入上下文。
- 问："Do any of these match your mental image, or shall we build a custom arrangement?"

**子部分 3 — Component Inventory**：
- 对于每个 zone，列出其中的 UI 组件。对每个组件注明：
  - 组件类型（button、list、card、stat display、input field 等）
  - 它显示的内容
  - 是否可交互
  - 是否使用了库中已有模式（按 pattern 名引用）
  - 是否引入了新模式（标记以后加入库）

**子部分 4 — ASCII Wireframe**：
- 提议根据区域布局和组件列表生成 ASCII wireframe。
- 使用 `AskUserQuestion`："Want an ASCII wireframe as part of this spec?"
  - 选项："Yes, include one"、"No, I'll attach a separate file"
- 如果是，则先在对话中生成 wireframe。写入文件前先请求反馈。

---

#### Section D: States & Variants

引导用户考虑 happy path 之外的内容。

**要问的问题**（一次只问一个）：
- "What does this screen look like the very first time a player sees it, when there is no data yet? (empty state)"
- "What happens when something goes wrong — an error, a failed action, a missing resource? (error state)"
- "Is there ever a loading wait on this screen? If so, what does it show? (loading state)"
- "Are there any player progression states that change what this screen shows? For example, locked content, premium content, or tutorial-mode overlays?"
- "Does this screen behave differently on any supported platform? (platform variant)"

将收集到的状态整理成表，供批准：

| State / Variant | Trigger | What Changes |
|-----------------|---------|--------------|
| Default | Normal load | — |
| Empty | No data available | [content area description] |
| [etc.] | [trigger] | [changes] |

---

#### Section E: Interaction Map

对于在 Layout Specification 中识别出的每个可交互组件，定义：
- 动作（tap、click、press、hold、scroll、drag）
- 触发它的平台输入（mouse click、gamepad A、keyboard Enter）
- 立即反馈（visual、audio、haptic）
- 结果（navigation target、state change、data write）

使用第 2h 阶段从 `technical-preferences.md` 载入的输入方式——不要再次询问用户。先明确说明："Mapping interactions for: [Input Methods from tech-prefs]. Covering [Gamepad Support] gamepad support."

一次只处理一个组件，不要一次性问完所有组件。
对于导航动作（去往其他屏幕），确认目标与现有 UX spec 匹配，或者将其标为 spec dependency。

---

#### Section E2: Events Fired

对于 Interaction Map 中的每个玩家动作，记录游戏或分析系统应触发的对应事件——如果不适用，则明确写 "no event"。

**要问的问题**：
- "For each action, should the game fire an analytics event, trigger a game-state change, or both?"
- "Are there any actions that should NOT fire an event — and is that a deliberate choice?"

将其与 Interaction Map 并列表格呈现：

| Player Action | Event Fired | Payload / Data |
|---|---|---|
| [action] | [EventName] or none | [data passed with event] |

标记任何会修改持久游戏状态的动作（存档、进度、经济）——这些需要架构团队显式关注。

---

#### Section E3: Transitions & Animations

指定屏幕如何进入和退出，以及如何响应状态变化。

**要问的问题**：
- "How does this screen appear? (fade in, slide from right, instant pop, scale from button)"
- "How does it dismiss? (fade out, slide back, cut)"
- "Are there any in-screen state transitions that need animation? (loading spinner, success state, error flash)"
- "Is there any animation that could cause motion sickness — and does the game have a reduced-motion option?"

最低要求：
- 屏幕进入过渡
- 屏幕退出过渡
- 如果屏幕有多个状态，至少一项状态变化动画

---

#### Section F: Data Requirements

交叉参考第 2 阶段收集到的 GDD UI Requirements 小节。

对屏幕显示的每一项信息，询问：
- "Where does this data come from? Which system owns it?"
- "Does this screen need to write data back, or is it read-only?"
- "Is any of this data time-sensitive or real-time? (health bars, cooldown timers)"

如果 UI 需要拥有或管理游戏状态，则标记为架构层面的关注点。UX spec 定义 UI 需要什么，不规定数据如何传递。那是架构决策。

将数据需求整理成表：

| Data | Source System | Read / Write | Notes |
|------|--------------|--------------|-------|
| [item] | [system] | Read | — |
| [item] | [system] | Write | [concern if any] |

---

#### Section G: Accessibility

交叉参考 `design/accessibility-requirements.md`（如果存在）。

引导 ux-designer agent 针对此屏幕使用标准检查清单：
- Keyboard-only navigation path through all interactive elements
- Gamepad navigation order（如适用）
- Text contrast 和最小可读字号
- 不依赖颜色的沟通（不能只用颜色传达信息）
- 对任何非文本元素的屏幕阅读器考虑
- 任何需要 reduced-motion 替代方案的 motion 或 animation

使用 `AskUserQuestion` 处理无障碍层级的任何开放问题：
- "Has the accessibility tier been committed to for this project?"
  - 选项："Yes, read from requirements doc"、"Not yet — let's flag it as a question"、"Skip accessibility section for now"

---

#### Section H: Localization Considerations

记录会影响该屏幕在文本翻译后如何表现的约束。

**要问的问题**：
- "Which text elements on this screen are the longest? What is the maximum character count that fits the layout?"
- "Are there any elements where text length is layout-critical — e.g., a button label that must stay on one line?"
- "Are there any elements that display numbers, dates, or currencies that need locale-specific formatting?"

注意：目标是标记任何在本地化后出现 40% 文本扩展（例如英语到德语或法语）就会破坏布局的元素。将这些标为本地化工程师的 HIGH PRIORITY。

---

#### Section I: Acceptance Criteria

至少写 5 条具体、可测试的标准，QA tester 无需阅读其他设计文档就能验证。这些会成为 `/story-done` 的通过/失败条件。

**格式**：使用复选框。每条标准都必须能被人工测试者验证：

```text
- [ ] Screen opens within [X]ms from [trigger]
- [ ] [Element] displays correctly at [minimum] and [maximum] values
- [ ] [Navigation action] correctly routes to [destination screen]
- [ ] Error state appears when [condition] and shows [specific message or icon]
- [ ] Keyboard/gamepad navigation reaches all interactive elements in logical order
- [ ] [Accessibility requirement] is met — e.g., "all interactive elements have focus indicators"
```

**最低要求**：
- 1 条性能标准（打开/加载时间）
- 1 条导航标准（验证至少一条入口或出口路径）
- 1 条错误/空状态标准
- 1 条无障碍标准（按承诺的层级）
- 1 条针对该屏幕核心目的的标准

请用户确认："Do these criteria cover what would actually make this screen 'done' for your QA process?"

---

### Section Guidance: HUD Design Mode

HUD 设计遵循与 UX spec 不同的顺序。先从 philosophy 开始；在信息架构完成前不要碰布局。

#### Section A: HUD Philosophy

请用户用 1-2 句话描述游戏与屏幕信息之间的关系。

提供一些 framing 示例帮助他们：
- "Nearly HUD-free — atmosphere requires unobstructed immersion (e.g., Hollow Knight, Firewatch)"
- "Minimal but present — only critical information visible, everything else contextual (e.g., Dark Souls)"
- "Information-dense — all decision-relevant data always visible (e.g., Diablo IV, StarCraft II)"
- "Adaptive — HUD density responds to combat state, exploration mode, menus (e.g., God of War)"

这个 philosophy 会成为后续每个 HUD 决策的设计约束。
如果拟议元素与该哲学冲突，请把冲突指出来。

---

#### Section B: Information Architecture

在任何布局工作前都要先完成这一部分。不要跳过。

**步骤 1 — Full information inventory**：
收集第 2 阶段中 GDD UI Requirements 所有信息。
展示完整列表："These are all the things your game systems say they need to communicate to the player on screen."

**步骤 2 — Categorization**：
让用户对每一项进行分类：

| Category | Description |
|----------|-------------|
| **Must Show** | 始终可见，玩家做核心决策所必需 |
| **Contextual** | 只有在相关时可见（战斗中、靠近可交互物时等） |
| **On Demand** | 玩家必须主动请求（切换、按住按钮） |
| **Hidden** | 通过世界/音频传达，从不以屏幕文本显示 |

使用 `AskUserQuestion` 分组处理每次 3-4 个条目，不要一次性全部处理。
这是 HUD 中最关键的设计决策——不要着急。

**冲突检查**：如果信息哲学（Section A）写的是“nearly HUD-free”，但 Must Show 列表越来越长，请显式指出冲突：
> "The current Must Show list has [N] items. That may conflict with the HUD-free
> philosophy. Options: reduce the Must Show list, revise the philosophy, or define
> a hybrid approach where HUD is absent in exploration and present in combat."

---

#### Section C: Layout Zones

只有在信息架构批准之后，才设计 layout zones。

布局应基于：
- 哪些条目是 Must Show（它们决定永久区域）
- 玩家在游戏中自然会把注意力放在哪里（动作游戏看屏幕中央，策略游戏看角落）
- 平台和宽高比目标

提供 2-3 种区域布局方案。依据 HUD philosophy 和第 B 节的分类给出理由。

---

#### Section D: HUD Elements

对布局中的每个元素，指定：
- 元素名称和类别（Must Show / Contextual / On Demand）
- 显示内容
- 视觉形式（bar、number、icon、counter、map）
- 更新行为（real-time、event-driven、player-queried）
- 上下文触发（如果不是始终可见）
- 动画行为（低值时是否闪烁？淡入？猛地弹出？）

逐个元素推进。若存在适用模式，则引用交互模式库，用于状态显示、资源条或冷却指示器。

---

#### Sections E, F, G: Dynamic Behaviors, Platform Variants, Accessibility

这三部分与 UX spec 对应部分结构相同。详见 UX Spec 中 D（States/Variants）、E（Interactions）和 G（Accessibility）的指导。

对于 HUD，特别强调：
- Dynamic Behaviors：什么会在游戏过程中改变 HUD 密度？
- Platform Variants：mobile/console 是否需要不同的元素尺寸或位置？

---

### Section Guidance: Interaction Pattern Library Mode

Pattern library 撰写是增量式、目录驱动的，不是线性的。

#### 第 1 阶段：整理现有模式目录

Glob `design/ux/*.md`（排除 `interaction-patterns.md`），读取每个 spec 的 Component Inventory 和 Interaction Map 小节。提取其中使用的每一个 interaction pattern。

呈现提取列表："Based on existing UX specs, these patterns are already in use in the game:"
- [Pattern name]: used in [screen], [screen]
- [etc.]

询问："Are there patterns you know exist but aren't in existing specs yet? List any additional ones now."

---

#### 第 2 阶段：将每个模式形式化

对每个 pattern（已有或新增），记录：

```markdown
### [Pattern Name]

**Category**: Navigation / Input / Feedback / Data Display / Modal / Overlay / [other]
**Used In**: [list of screens]

**Description**: [One paragraph explaining what this pattern is and when to use it]

**Specification**:
- [Component behavior]
- [Input mapping]
- [Visual/audio feedback]
- [Accessibility requirements for this pattern]

**When to Use**: [Conditions where this pattern is appropriate]
**When NOT to Use**: [Conditions where another pattern is more appropriate]

**Reference**: [Screenshot path or ASCII example, if available]
```

按批次处理模式。可以提出："Shall I draft the first batch based on what I've found in the existing specs, or do you want to define them one by one?"

---

#### 第 3 阶段：识别缺口

在整理完已知模式后，询问：
- "Are there screens or interactions planned that would need patterns not yet in this library?"
- "Are there any patterns in existing specs that feel inconsistent with each other and should be consolidated?"

将缺口记录在 Gaps 小节中，留待后续处理。

---

## 5. 交叉引用检查

在将 spec 标记为可审查前，运行以下检查：

**1. GDD requirement coverage**：引用该屏幕的每条 GDD UI Requirement 是否在本 spec 中有对应元素？列出任何缺口。

**2. Pattern library alignment**：本 spec 使用的所有 interaction pattern 是否都按名称引用了？如果在本次 spec 会话中发明了新模式，请将其标记为加入 pattern library：
> "This spec uses [pattern name], which isn't in the pattern library yet.
> Want to add it now, or flag it as a gap?"

**3. Navigation consistency**：本 spec 的入口/出口点是否与任何相关 spec 中的 navigation map 一致？标记不匹配。

**4. Accessibility coverage**：本 spec 是否满足 `design/accessibility-requirements.md` 中承诺的无障碍层级？如果没有，标记开放问题。

**5. Empty states**：每个依赖数据的元素是否都定义了空状态？标记任何没有的。

呈现检查结果：
> **Cross-Reference Check: [Screen Name]**
> - GDD requirements: [N of M covered / all covered]
> - New patterns to add to library: [list or "none"]
> - Navigation mismatches: [list or "none"]
> - Accessibility gaps: [list or "none"]
> - Missing empty states: [list or "none"]

---

## 6. 交接

当所有 section 都已批准并写入后：

### 6a：更新会话状态

更新 `production/session-state/active.md`，包含：
- Task: [screen-name] UX spec
- Status: Complete（或 In Review）
- File: design/ux/[filename].md
- Sections: All written
- Next: [suggestion]

### 6b：建议下一步

在给出选项之前，先清楚说明：

> "This spec should be validated with `/ux-review` before it enters the
> implementation pipeline. The Pre-Production gate requires all key screen specs
> to have a review verdict."

然后使用 `AskUserQuestion`：
- "Run `/ux-review [filename]` now, or do something else first?"
  - 选项：
    - "Run `/ux-review` now — validate this spec"
    - "Design another screen first, then review all specs together"
    - "Update the interaction pattern library with new patterns from this spec"
    - "Stop here for this session"

如果用户选择“Design another screen first”，添加备注："Reminder: run `/ux-review` on all completed specs before running `/gate-check pre-production`."

### 6c：为相关 spec 建立交叉链接

如果其他 UX spec 会链接到该屏幕或从该屏幕链接出去，注明哪些文件应引用本 spec。不要在未询问的情况下编辑那些文件——只需要指出它们。

---

## 7. 恢复与继续

如果会话中断（压缩、崩溃、新会话）：

1. 读取 `production/session-state/active.md` —— 它记录了当前屏幕以及哪些 section 已完成。
2. 读取 `design/ux/[filename].md` —— 真实内容已写入的 section 视为完成；仍是 `[To be designed]` 的 section 需要继续工作。
3. 从下一个未完成的 section 继续——无需重新讨论已完成的部分。

这就是增量写入重要的原因：每个已批准的 section 都能在任何中断后保留下来。

---

## 8. 专业代理路由

此技能以 `ux-designer` 作为主 agent（已在 frontmatter 中设置）。针对某些子主题，可能需要额外上下文或协调：

| Topic | Coordinate with |
|-------|----------------|
| Visual aesthetics, color, layout feel | `art-director` — UX spec 定义区域；art 决定它们的视觉呈现 |
| Implementation feasibility（引擎约束） | `ui-programmer` — 在最终确定组件清单前 |
| Gameplay data requirements | `game-designer` — 当数据所有权不清晰时 |
| Narrative/lore visible in the UI | `narrative-director` — 用于风味文本、物品名、lore 面板 |
| Accessibility tier decisions | 由本会话处理——归 ux-designer 所有 |

当通过 Task 工具委派给其他 agent 时：
- 提供：屏幕名称、游戏概念摘要、需要专家输入的具体问题
- agent 将分析返回给本会话
- 本会话将 agent 的输出呈现给用户
- 用户决定；本会话写入文件
- agent 不会直接写文件——本会话负责所有文件写入

---

## 协作协议

此技能始终遵循协作式设计原则：

1. **Question -> Options -> Decision -> Draft -> Approval**，适用于每个 section
2. 在每个决策点使用 `AskUserQuestion`（Explain -> Capture 模式）：
   - 第 2 阶段："Ready to start, or need more context?"
   - 第 3 阶段："May I create the skeleton?"
   - 第 4 阶段（每个 section）：设计问题、方案选项、草稿审批
   - 第 5 阶段："Run cross-reference check? What's next?"
3. 在 skeleton 和每次 section 写入前，都要先说 **"May I write to [filepath]?"**
4. **增量写入**：每个 section 一旦批准，立即写入文件
5. **会话状态更新**：每次 section 写入后都要更新

**审美让权**：当布局或视觉选择最终取决于个人品味时，呈现选项并询问。不要因为它“标准”就自行选择某种布局——始终要确认。用户是创意总监。

**冲突显化**：当某条 GDD 要求与可用屏幕空间发生冲突时，要显式呈现冲突并给出解决方案。绝不要悄悄丢掉某项要求。也不要在没有标记的情况下默默扩大布局。

**绝不**一次性自动生成整份 spec 并当作既成事实呈现。
**绝不**未经用户批准就写入任何 section。
**绝不**在未标记冲突的情况下与已批准的 UX spec 相矛盾。
**始终**说明每个决策的来源（GDD 要求、玩家旅程、用户选择）。

Verdict: **COMPLETE** — UX spec 已按章节写入并批准。

---

## 推荐下一步

- 运行 `/ux-review [filename]`，在进入实施流程前验证该 spec
- 运行 `/ux-design [next-screen]`，继续设计剩余的屏幕或流程
- 当所有关键屏幕都拥有已批准的 UX spec 后，运行 `/gate-check pre-production`