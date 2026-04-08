---
name: art-bible
description: "分章节引导式编写 Art Bible。它创建视觉识别规范，作为所有资产生产的门禁。请在 /brainstorm 获批之后、且在 /map-systems 或任何 GDD 编写开始之前运行。"
argument-hint: "[--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
---

## 阶段 0：解析参数并检查上下文

先解析 review 模式（只做一次，并在本次运行所有 gate spawn 中复用）：
1. 如果传入了 `--review [full|lean|solo]` → 使用它
2. 否则读取 `production/review-mode.txt` → 使用其值
3. 否则 → 默认 `lean`

完整检查模式见 `.claude/docs/director-gates.md`。

读取 `design/gdd/game-concept.md`。如果不存在，则失败并提示：
> "未找到 game concept。请先运行 `/brainstorm`——Art Bible 是在 game concept 获批之后编写的。"

从 game-concept.md 提取：
- 游戏标题（临时标题）
- 核心幻想与电梯陈述
- 所有游戏支柱
- 如果存在，提取 **Visual Identity Anchor** 章节（来自 brainstorm 第 4 阶段 art-director 输出）
- 目标平台（如果已注明）

**回填模式检测**：Glob `design/art/art-bible.md`。如果文件存在：
- 完整读取
- 对 9 个章节逐一检查正文是否包含真实内容（不仅是 `[To be designed]` 之类占位符）
- 建立章节状态表：

```
Section | Status
--------|--------
1. Visual Identity Statement | [Complete / Empty / Placeholder]
2. Color Palette | ...
3. Lighting & Atmosphere | ...
4. Character Art Direction | ...
5. Environment & Level Art | ...
6. UI Visual Language | ...
7. VFX & Particle Style | ...
8. Asset Standards | ...
9. Style Prohibitions | ...
```

- 把此表呈现给用户：
  > "在 `design/art/art-bible.md` 找到了现有 art bible。已有 [N] 个章节完成，[M] 个章节需要内容。我只会处理未完成的章节——现有内容不会被触碰。"
- 只处理状态为 Empty 或 Placeholder 的章节。不要重新撰写已经完成的章节。

如果文件不存在，则视为全新编写会话——正常继续。

读取 `.claude/docs/technical-preferences.md`（如果存在）——提取性能预算和引擎信息，供资产标准约束使用。

---

## 阶段 1：定界

在写任何内容之前，先呈现会话上下文并问两个问题：

使用 `AskUserQuestion`，分两个 Tab：
- Tab **"Scope"** —— "今天需要编写哪些章节？"
  选项：`Full bible — all 9 sections` / `Visual identity core (sections 1–4 only)` / `Asset standards only (section 8)` / `Resume — fill in missing sections`
- Tab **"References"** —— "你是否有定义视觉方向的参考游戏、电影或艺术风格？"
  （自由文本——让用户直接输入具体标题。此处不要预设选项。）

如果 game-concept.md 中有 Visual Identity Anchor 章节，提示：
> "在 brainstorm 中找到了视觉识别锚点：'[anchor name] — [one-line rule]'。我会以它作为 art bible 的基础。"

---

## 阶段 2：视觉识别基础（第 1–4 章）

这四个章节定义核心视觉语言。**其他所有章节都由它们派生。** 逐章编写并写入文件后，再进入下一章。

### 第 1 章：Visual Identity Statement

**目标**：一句视觉规则 + 2–3 条支持性原则，用于消除视觉歧义。

如果存在来自 game-concept.md 的视觉锚点：先展示它并询问：
- "直接基于这个锚点展开？"
- "先修订它再扩展？"
- "从头开始提出新方向？"

**代理委派（强制）**：通过 Task 生成 `art-director`：
- 提供：game concept（elevator pitch、core fantasy）、完整的 pillars 集合、平台目标、Phase 1 定界中提到的任何参考游戏/艺术、如果存在的视觉锚点
- 询问："为这个游戏起草一个 Visual Identity Statement。请提供：(1) 一条可以消除任何视觉决策歧义的视觉规则；(2) 2–3 条支持性视觉原则，每条都要有一句设计测试（'当 X 不明确时，此原则要求选择 Y'）。所有原则都必须直接锚定在既定 pillars 上——每条原则都必须服务于某个具体 pillar。"

把 art-director 的草案展示给用户。使用 `AskUserQuestion`：
- 选项：`[A] Lock this in` / `[B] Revise the one-liner` / `[C] Revise a supporting principle` / `[D] Describe my own direction`

获批后立即写入文件。

### 第 2 章：Mood & Atmosphere

**目标**：按游戏状态定义情绪目标——要具体到足以让灯光美术直接执行。

对每个主要游戏状态（例如探索、战斗、胜利、失败、菜单——需按本游戏状态调整），定义：
- 主要情绪/氛围目标
- 灯光特征（时间、色温、对比度）
- 氛围描述词（3–5 个形容词）
- 能量等级（frenetic / measured / contemplative / 等）

**代理委派**：通过 Task 生成 `art-director`，输入 Visual Identity Statement 和 pillars 集合。询问："为这个游戏的每个主要状态定义 mood 和 atmosphere 目标。不要只写 'dark and foreboding' 这种泛词。要明确命名情绪目标、灯光特征（暖/冷、高/低对比、时间方向），以及至少一个承载情绪的视觉元素。每个状态都必须在视觉上彼此区分。"

获批后立即写入文件。

### 第 3 章：Shape Language

**目标**：定义让这个世界在视觉上自洽且易于辨识的几何词汇。

覆盖：
- 角色轮廓哲学（缩略图大小是否可读？每个 archetype 有何区分特征？）
- 环境几何（angular/curved/organic/geometric——哪个占主导，为什么？）
- UI 形状语法（UI 是否回响世界美术，还是保持独立 HUD 语言？）
- Hero shapes 与 supporting shapes（什么吸引视线，什么退后？）

**代理委派**：通过 Task 生成 `art-director`，输入 Visual Identity Statement 和 mood 目标。询问："为这个游戏定义 shape language。把每条形状原则都和视觉识别声明、以及某个具体 pillar 联系起来。解释这些形状选择在情绪层面向玩家传达了什么。"

获批后立即写入文件。

### 第 4 章：Color System

**目标**：一个完整、可生产的调色系统，同时服务审美与信息传达。

覆盖：
- 主色板（5–7 个颜色及其职责——不只是 hex 值，而是每种颜色在这个世界里代表什么）
- 语义颜色用法（红色代表什么？金色？蓝色？白色？建立颜色词汇表）
- 按生物群系/区域划分的色温规则（如果游戏有不同区域）
- UI 调色板（可与世界调色板不同——必须明确说明差异）
- 色盲安全：哪些语义颜色需要形状/图标/声音作为备份

**代理委派**：通过 Task 生成 `art-director`，输入 Visual Identity Statement 和 mood 目标。询问："为这个游戏设计 color system。每个语义颜色分配都必须解释清楚——为什么这个颜色在这个世界里代表危险/安全/奖励？指出哪些颜色组合可能对色盲玩家失效，并说明需要什么备份提示。"

获批后立即写入文件。

---

## 阶段 3：生产指南（第 5–8 章）

这些章节把视觉识别转化为具体生产规则。它们要具体到外包团队无需额外说明即可执行。

### 第 5 章：Character Design Direction

**代理委派**：通过 Task 生成 `art-director`，输入第 1–4 章。询问："为这个游戏定义角色设计方向。覆盖：玩家角色（如果有）的视觉 archetype、每种角色类型的区分特征规则（玩家如何一眼区分敌人/NPC/盟友？）、表情/姿态风格目标（stiff/expressive/realistic/exaggerated）、以及 LOD 哲学（在游戏镜头距离下保留多少细节？）。"

写入获批章节。

### 第 6 章：Environment Design Language

**代理委派**：通过 Task 生成 `art-director`，输入第 1–4 章。询问："为这个游戏定义环境设计语言。覆盖：建筑风格及其与世界文化/历史的关系、材质哲学（painted vs. PBR vs. stylized——为什么这个游戏选择它？）、道具密度规则（sparse/dense——每种区域类型为何如此选择？）、以及环境叙事指南（哪些视觉细节应在没有文字的情况下讲故事？）。"

写入获批章节。

### 第 7 章：UI/HUD Visual Direction

**代理委派**：并行生成：
- **`art-director`**：UI 的视觉风格——diegetic vs. screen-space HUD、排版方向（字体个性、字重、层级尺寸）、图标风格（flat/outlined/illustrated/photorealistic）、UI 元素的动效手感
- **`ux-designer`**：UX 一致性检查——这个视觉方向是否支持本游戏所需的交互模式？标记任何与可读性/可访问性需求冲突的地方。

收集两者结果。如果它们冲突（例如 art-director 想要复杂的 diegetic UI，但 ux-designer 认为会降低战斗可读性），要明确展示冲突和双方立场。不要擅自解决——用 `AskUserQuestion` 让用户决定。

写入获批章节。

### 第 8 章：Asset Standards

**代理委派**：并行生成：
- **`art-director`**：文件格式偏好、命名惯例方向、纹理分辨率层级、LOD 级别预期、导出设置哲学
- **`technical-artist`**：引擎级硬约束——每类资产的多边形预算、纹理内存限制、材质槽数量、导入器约束，以及 `.claude/docs/technical-preferences.md` 中性能预算要求的任何内容

如果任何美术偏好与技术约束冲突（例如 art-director 想要 4K 纹理，但性能预算要求移动端只能用 2K），要明确解决冲突——同时记录理想标准与受限标准，并解释取舍。资产标准的含糊之处会直接变成生产成本。

写入获批章节。

---

## 阶段 4：参考方向（第 9 章）

**目标**：一组经过筛选的参考来源，并明确说明每个来源该借鉴什么、又该避免什么。

**代理委派**：通过 Task 生成 `art-director`，输入已完成的第 1–8 章。询问："为这个游戏整理参考方向。请提供 3–5 个参考来源（游戏、电影、艺术风格或具体艺术家）。对每个来源：命名、明确指出要借鉴的具体视觉元素（不要只写 '整体美学'——要写具体技巧、颜色选择或构图规则），并明确指出要刻意避免或偏离的点（避免被看成抄袭 X）。参考应当是增量式的——不要有两个参考在朝完全相同的方向。"

写入获批章节。

---

## 阶段 5：Art Director 签署

**review mode 检查**——在 spawn AD-ART-BIBLE 前执行：
- `solo` → 跳过。注："AD-ART-BIBLE skipped — Solo mode." 进入阶段 6。
- `lean` → 跳过（不是 PHASE-GATE）。注："AD-ART-BIBLE skipped — Lean mode." 进入阶段 6。
- `full` → 正常 spawn。

当所有章节完成（或 Phase 1 选定的范围完成）后，通过 Task 使用 gate **AD-ART-BIBLE**（见 `.claude/docs/director-gates.md`）spawn `creative-director`。

传入：art bible 文件路径、游戏 pillars、visual identity anchor。

按 `director-gates.md` 的标准规则处理 verdict。在 art bible 的状态头中记录 verdict：
`> **Art Director Sign-Off (AD-ART-BIBLE)**: APPROVED [date] / CONCERNS (accepted) [date] / REVISED [date]`

---

## 阶段 6：结束

在展示下一步之前，检查项目状态：
- `design/gdd/systems-index.md` 是否存在？→ map-systems 已完成，跳过该选项
- `.claude/docs/technical-preferences.md` 是否已配置引擎（不是 `[TO BE CONFIGURED]`）？→ setup-engine 已完成，跳过该选项
- `design/gdd/` 中是否存在任何 `*.md` 文件？→ design-system 已运行，跳过该选项
- 是否存在 `design/gdd/gdd-cross-review-*.md`？→ review-all-gdds 已完成
- 上面检查若确认存在 GDD？→ 包含 `/consistency-check` 选项

使用 `AskUserQuestion` 询问下一步。只包含确实基于上述状态检查后仍然适用的选项：

**选项池——只在尚未完成时包含：**
- `[_] Run /map-systems — 在编写 GDD 前先把概念拆成系统`（如果 systems-index.md 已存在则跳过）
- `[_] Run /setup-engine — 配置引擎（引擎设定后，资产标准可能需要重看）`（如果引擎已配置则跳过）
- `[_] Run /design-system — 开始第一个 GDD`（如果已有任何 GDD 则跳过）
- `[_] Run /review-all-gdds — 跨 GDD 一致性检查（Technical Setup gate 前必需）`（如果 gdd-cross-review-*.md 已存在则跳过）
- `[_] Run /asset-spec — 基于已批准的 GDD 生成逐资产视觉规格和 AI 生成提示词`（如果已有 GDD 则包含）
- `[_] Run /consistency-check — 以 art bible 的视觉方向规则扫描现有 GDD 冲突`（如果已有 GDD 则包含）
- `[_] Run /create-architecture — 编写主架构文档（下一步 Technical Setup）`
- `[_] Stop here`

只给实际包含的选项分配 A、B、C… 编号。把最合理、能推进流水线的选项标为 `(recommended)`。

> **始终包含** `/create-architecture` 和 Stop here 作为选项——一旦 art bible 完成，它们总是有效的下一步。

---

## 协作协议

每个章节都遵循：**Question → Options → Decision → Draft (from art-director agent) → Approval → Write to file**

- 绝不要在先 spawn 相关代理之前起草章节
- 每个章节一旦获批，立刻写入文件——不要批量写
- 将所有代理分歧展示给用户——不要在 art-director 与 technical-artist 之间静默裁决冲突
- art bible 是约束文档：它通过限制未来决策来换取视觉一致性。每个章节都应当有助于收紧解空间。

---

## 推荐下一步

在 art bible 获批后：
- 运行 `/map-systems`，在编写 GDD 之前把概念拆解为游戏系统
- 若引擎尚未配置，运行 `/setup-engine`（引擎选择后，资产标准可能需要重审）
- 运行 `/design-system [first-system]`，开始按系统编写 GDD
- 一旦 GDD 存在，运行 `/consistency-check` 以验证它们是否符合 art bible 的视觉规则
- 运行 `/create-architecture` 以产出主架构文档