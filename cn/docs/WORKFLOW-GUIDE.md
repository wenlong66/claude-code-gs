# Claude Code Game Studios -- 完整工作流程指南

> **如何使用智能体架构从零到发布一款游戏。**
>
> 本指南会带你走完游戏开发的每个阶段，使用 48 个智能体、68 个斜杠命令和 12 个自动化钩子。它假设你已经安装了 Claude Code，并且正在项目根目录下工作。
>
> 流水线共有 7 个阶段。每个阶段都有正式门禁（`/gate-check`），在进入下一阶段前必须通过。权威的阶段顺序定义在 `.claude/docs/workflow-catalog.yaml` 中，并由 `/help` 读取。

---

## 目录

1. [快速开始](#快速开始)
2. [阶段 1：概念](#阶段-1概念)
3. [阶段 2：系统设计](#阶段-2系统设计)
4. [阶段 3：技术准备](#阶段-3技术准备)
5. [阶段 4：预生产](#阶段-4预生产)
6. [阶段 5：生产](#阶段-5生产)
7. [阶段 6：打磨](#阶段-6打磨)
8. [阶段 7：发布](#阶段-7发布)
9. [横切关注点](#横切关注点)
10. [附录 A：智能体快速参考](#附录-a智能体快速参考)
11. [附录 B：斜杠命令快速参考](#附录-b斜杠命令快速参考)
12. [附录 C：常见工作流](#附录-c常见工作流)

---

## 快速开始

### 你需要什么

开始前请确认你已安装并可用：

- **Claude Code**
- **Git**，Windows 使用 Git Bash，Mac/Linux 使用标准终端
- **jq**（可选但推荐——缺少时钩子会回退到 `grep`）
- **Python 3**（可选——部分钩子会用它做 JSON 验证）

### 步骤 1：克隆并打开

```bash
git clone <repo-url> my-game
cd my-game
```

### 步骤 2：运行 /start

如果这是你的第一次会话：

```
/start
```

这个引导式入门会问你当前处于哪个阶段，并把你路由到正确的流程：

- **路径 A** —— 还没有想法：路由到 `/brainstorm`
- **路径 B** —— 想法模糊：带种子信息路由到 `/brainstorm`
- **路径 C** —— 概念清晰：路由到 `/setup-engine` 和 `/map-systems`
- **路径 D1** —— 现有项目，工件很少：走正常流程
- **路径 D2** —— 现有项目，已有 GDD/ADR：运行 `/project-stage-detect`，然后 `/adopt` 做棕地迁移

### 步骤 3：检查钩子是否工作

启动新的 Claude Code 会话。你应该会看到 `session-start.sh` 钩子的输出：

```text
=== Claude Code Game Studios -- Session Context ===
Branch: main
Recent commits:
  abc1234 Initial commit
===================================
```

如果看到了，说明钩子正常工作。如果没有，请检查 `.claude/settings.json`，确认钩子路径对你的操作系统是正确的。

### 步骤 4：随时求助

任何时候都可以运行：

```
/help
```

它会读取 `production/stage.txt` 中的当前阶段，检查有哪些工件存在，并准确告诉你下一步要做什么。它会区分 **必须执行** 的下一步和 **可选** 机会。

### 步骤 5：创建目录结构

目录会按需创建。系统期望如下布局：

```text
src/                  # 游戏源代码
  core/               # 引擎/框架代码
  gameplay/           # 游戏玩法系统
  ai/                 # AI 系统
  networking/         # 多人游戏代码
  ui/                 # UI 代码
  tools/              # 开发工具
assets/               # 游戏资源
  art/                # 精灵、模型、纹理
  audio/              # 音乐、音效
  vfx/                # 粒子效果
  shaders/            # 着色器文件
  data/               # JSON 配置/平衡数据
design/               # 设计文档
  gdd/                # 游戏设计文档
  narrative/          # 故事、世界观、对白
  levels/             # 关卡设计文档
  balance/            # 平衡表格和数据
docs/                 # 技术文档
  architecture/       # 架构决策记录
  api/                # API 文档
  postmortems/        # 事后分析
tests/                # 测试套件
prototypes/           # 一次性原型
production/           # 冲刺计划、里程碑、发布
  sprints/
  milestones/
  releases/
  epics/              # Epic 与故事文件（来自 /create-epics + /create-stories）
  playtests/          # 游玩测试报告
  session-state/      # 临时会话状态（gitignored）
  session-logs/       # 会话审计日志（gitignored）
```

> **提示：** 你不需要第一天就创建这些目录。到对应阶段再创建即可。关键是创建时要遵守这个结构，因为**规则系统**会按文件路径强制标准。`src/gameplay/` 下的代码使用游戏玩法规则，`src/ai/` 下的代码使用 AI 规则，依此类推。

---

## 阶段 1：概念

### 本阶段会发生什么

你会从“没有想法”或“想法模糊”变成一个结构化的游戏概念文档，并明确支柱和玩家旅程。这是你弄清楚**在做什么**以及**为什么做**的地方。

### 阶段 1 流水线

```text
/brainstorm  -->  game-concept.md  -->  /design-review  -->  /setup-engine
     |                                        |                    |
     v                                        v                    v
  10 个概念     概念文档包含支柱、       概念文档验证         引擎固定到
  MDA 分析      MDA、核心循环、USP      technical-preferences.md
  玩家动机                                                      |
                                                                 v
                                                            /map-systems
                                                                 |
                                                                 v
                                                           systems-index.md
                                                           （所有系统、依赖、
                                                            优先级层级）
```

### 步骤 1.1：使用 /brainstorm 头脑风暴

这是起点。运行头脑风暴技能：

```
/brainstorm
```

或者加上类型提示：

```
/brainstorm roguelike deckbuilder
```

**会发生什么：** 头脑风暴技能使用专业工作室技术，引导你完成一个协作式 6 阶段构思过程：

1. 询问你的兴趣、主题和约束
2. 生成 10 个概念种子，并附上 MDA（Mechanics、Dynamics、Aesthetics）分析
3. 你挑选 2-3 个最喜欢的进行深度分析
4. 做玩家动机映射和受众定位
5. 你选择最终概念
6. 将其正式化为 `design/gdd/game-concept.md`

概念文档包括：

- 电梯推介（一句话）
- 核心幻想（玩家想象自己在做什么）
- MDA 分解
- 目标受众（Bartle 类型、人口统计）
- 核心循环图
- 独特卖点
- 可比较作品与差异化
- 游戏支柱（3-5 个不可妥协的设计价值）
- 反支柱（游戏刻意避免的内容）

### 步骤 1.2：审查概念（可选但推荐）

```
/design-review design/gdd/game-concept.md
```

在继续之前验证结构和完整性。

### 步骤 1.3：选择引擎

```
/setup-engine
```

或者指定引擎：

```
/setup-engine godot 4.6
```

**/setup-engine 的作用：**

- 在 `.claude/docs/technical-preferences.md` 中填充命名约定、性能预算和引擎特定默认值
- 检测知识缺口（引擎版本比 LLM 训练数据更新），并建议交叉参考 `docs/engine-reference/`
- 在 `docs/engine-reference/` 中创建版本固定的参考文档

**为什么这很重要：** 一旦你设置了引擎，系统就知道该使用哪些引擎专长智能体。如果你选择 Godot，像 `godot-specialist`、`godot-gdscript-specialist` 和 `godot-shader-specialist` 这样的智能体会成为首选专家。

### 步骤 1.4：把概念拆成系统

在编写单独的 GDD 之前，先枚举你的游戏需要哪些系统：

```
/map-systems
```

这会创建 `design/gdd/systems-index.md` —— 一个主追踪文档，它：

- 列出游戏需要的每个系统（战斗、移动、UI 等）
- 映射系统之间的依赖关系
- 分配优先级层级（MVP、垂直切片、Alpha、完整愿景）
- 决定设计顺序（基础 > 核心 > 功能 > 呈现 > 打磨）

在进入阶段 2 之前，这一步是**必需**的。来自 155 份游戏复盘的研究表明，跳过系统枚举会让生产成本增加 5-10 倍。

### 阶段 1 门禁

```
/gate-check concept
```

**通过要求：**

- `technical-preferences.md` 中已配置引擎
- `design/gdd/game-concept.md` 存在且包含支柱
- `design/gdd/systems-index.md` 存在且包含依赖顺序

**结论：** PASS / CONCERNS / FAIL。CONCERNS 仍可通过，但需要承认风险。FAIL 会阻止继续推进。

---

## 阶段 2：系统设计

### 本阶段会发生什么

你会创建定义游戏如何运作的所有设计文档。此时还不会写代码——这是纯设计。系统索引中列出的每个系统都会有自己的 GDD，按章节逐步撰写、逐个审查，然后所有 GDD 会一起做一致性检查。

### 阶段 2 流水线

```text
/map-systems next  -->  /design-system  -->  /design-review
       |                     |                     |
       v                     v                     v
  选择下一个系统      按章节撰写 GDD        验证 8 个必需部分
  来自 systems-index   （增量写入）         APPROVED/NEEDS REVISION
       |
       |  （对每个 MVP 系统重复）
       v
/review-all-gdds
       |
       v
  跨 GDD 一致性 + 设计理论审查
  PASS / CONCERNS / FAIL
```

### 步骤 2.1：编写系统 GDD

按依赖顺序使用引导流程设计每个系统：

```
/map-systems next
```

这会选出最高优先级、尚未设计的系统，并交给 `/design-system`，由它引导你按章节创建 GDD。

你也可以直接设计特定系统：

```
/design-system combat-system
```

**/design-system 的作用：**

1. 读取游戏概念、系统索引，以及任何上游/下游 GDD
2. 运行技术可行性预检（领域映射 + 可行性简报）
3. 一次只引导你填写 8 个必需 GDD 部分中的一个
4. 每个部分都遵循：上下文 > 问题 > 选项 > 决策 > 草案 > 批准 > 写入
5. 每个部分在批准后立刻写入文件（即使会话崩溃也能保留）
6. 标记与已批准 GDD 的冲突
7. 按类别路由到专长智能体（数学给 systems-designer，经济给 economy-designer，故事系统给 narrative-director）

**8 个必需 GDD 部分：**

| # | 部分 | 写什么 |
|---|------|--------|
| 1 | **概述** | 系统的一段式摘要 |
| 2 | **玩家幻想** | 玩家使用此系统时会想象/感受到什么 |
| 3 | **详细规则** | 无歧义的机械规则 |
| 4 | **公式** | 每个计算，包含变量定义和范围 |
| 5 | **边缘情况** | 奇怪情况下会发生什么？明确解决 |
| 6 | **依赖关系** | 这个系统连接了哪些其他系统（双向） |
| 7 | **调优旋钮** | 设计师可以安全修改的值，以及安全范围 |
| 8 | **验收标准** | 如何测试是否有效？具体、可测量 |

另外还有一个 **游戏手感** 部分：参考感受、输入响应时间（毫秒/帧）、动画手感目标（起始/活跃/恢复）、打击瞬间、重量感配置。

### 步骤 2.2：审查每个 GDD

在进入下一个系统前，先验证当前系统：

```
/design-review design/gdd/combat-system.md
```

检查这 8 个部分是否完整、公式是否清晰、边缘情况是否已解决、依赖关系是否双向、验收标准是否可测试。

**结论：** APPROVED / NEEDS REVISION / MAJOR REVISION。只有 APPROVED 的 GDD 才能继续推进。

### 步骤 2.3：无需完整 GDD 的小改动

对于调参、小增量或不值得写完整 GDD 的微调：

```
/quick-design "为侧后攻击增加 10% 伤害加成"
```

这会在 `design/quick-specs/` 中创建轻量级规格，而不是完整的 8 章节 GDD。它适合调优、数值调整和小功能。

### 步骤 2.4：跨 GDD 一致性审查

当所有 MVP 系统 GDD 都各自通过审查后：

```
/review-all-gdds
```

它会同时读取所有 GDD，并运行两个分析阶段：

**阶段 1 —— 跨 GDD 一致性：**
- 依赖双向性（A 引用 B，B 是否也引用 A？）
- 系统之间的规则冲突
- 对已重命名或删除系统的过期引用
- 职责归属冲突（两个系统争同一职责）
- 公式范围兼容性（系统 A 的输出是否适合系统 B 的输入？）
- 验收标准交叉检查

**阶段 2 —— 设计理论（整体游戏设计）：**
- 竞争性的进度循环（两个系统是否争夺同一奖励空间？）
- 认知负荷（一次是否有超过 4 个活跃系统？）
- 退化策略（是否有一种策略让其他策略失效？）
- 经济循环分析（来源和消耗是否平衡？）
- 跨系统难度曲线一致性
- 支柱对齐与反支柱违规
- 玩家幻想一致性

**输出：** `design/gdd/gdd-cross-review-[date].md`，包含一个结论。

### 步骤 2.5：叙事设计（如适用）

如果你的游戏有故事、世界观或对白，现在就是构建它的时候：

1. **世界构建** —— 使用 `world-builder` 定义派系、历史、地理和世界规则
2. **故事结构** —— 使用 `narrative-director` 设计故事弧、角色弧和叙事节拍
3. **角色表** —— 使用 `narrative-character-sheet.md` 模板

### 阶段 2 门禁

```
/gate-check systems-design
```

**通过要求：**

- `systems-index.md` 中所有 MVP 系统的 `Status` 都是 `Approved`
- 每个 MVP 系统都有审查过的 GDD
- 跨 GDD 审查报告存在（`design/gdd/gdd-cross-review-*.md`），且结论为 PASS 或 CONCERNS（不是 FAIL）

---

## 阶段 3：技术准备

### 本阶段会发生什么

你会做出关键技术决策，将其记录为架构决策记录（ADR），通过审查验证，并生成一份控制清单，让程序员拿到的是扁平、可执行的规则。你还会建立 UX 基础。

### 阶段 3 流水线

```text
/create-architecture  -->  /architecture-decision (x N)  -->  /architecture-review
        |                          |                                   |
        v                          v                                   v
  总体架构文档            每个决策对应 ADR             验证完整性、
  覆盖所有系统            docs/architecture/           依赖顺序、
                          adr-*.md                    引擎兼容性
                                                                      |
                                                                      v
                                                         /create-control-manifest
                                                                      |
                                                                      v
                                                         扁平程序员规则
                                                         docs/architecture/
                                                         control-manifest.md
        本阶段还包括：
        -------------------
        /ux-design  -->  /ux-review
        可访问性需求文档
        交互模式库
```

### 步骤 3.1：总体架构文档

```
/create-architecture
```

在 `docs/architecture/architecture.md` 中创建总架构文档，涵盖系统边界、数据流和集成点。

### 步骤 3.2：架构决策记录（ADR）

对每个重要技术决策：

```
/architecture-decision "NPC AI 使用状态机还是行为树"
```

**会发生什么：** 技能会引导你创建一份 ADR，其中包含：
- 上下文和决策驱动因素
- 所有选项及其优缺点和引擎兼容性
- 选定方案及其理由
- 后果（正面、负面、风险）
- 依赖关系（Depends On、Enables、Blocks、Ordering Note）
- GDD 需求对应项（通过 TR-ID 关联）

ADR 有一个生命周期：Proposed > Accepted > Superseded/Deprecated。

**在门禁检查前，至少需要 3 份基础层 ADR。**

**回填现有 ADR：** 如果你是棕地项目，已经有 ADR：

```
/architecture-decision retrofit docs/architecture/adr-005.md
```

它会检测模板中缺少哪些部分，只补缺口，绝不会覆盖已有内容。

### 步骤 3.3：架构审查

```
/architecture-review
```

会一起验证所有 ADR：
- ADR 依赖的拓扑排序（检测循环）
- 引擎兼容性验证
- GDD 修订标记（根据 ADR 选择标记需要更新的 GDD 部分）
- TR-ID 注册表维护（`docs/architecture/tr-registry.yaml`）

### 步骤 3.4：控制清单

```
/create-control-manifest
```

把所有已接受的 ADR 转换为一份扁平的程序员规则表：

```
docs/architecture/control-manifest.md
```

它按代码层级列出 Required、Forbidden 和 Guardrails。后续创建的故事会嵌入清单版本日期，以便检测过期。

### 步骤 3.5：可访问性需求

使用模板创建 `design/accessibility-requirements.md`。选择一个级别（Basic / Standard / Comprehensive / Exemplary），并填完 4 轴功能矩阵（视觉、操作、认知、听觉）。

这个文档在阶段 3 中是必需的，因为 UX 规格（阶段 4 编写）会引用这个级别——它是设计前置条件，不是 UX 交付物。

### 阶段 3 门禁

```
/gate-check technical-setup
```

**通过要求：**

- `docs/architecture/architecture.md` 存在
- 至少 3 份 ADR 存在且已被 Accepted
- 架构审查报告存在
- `docs/architecture/control-manifest.md` 存在
- `design/accessibility-requirements.md` 存在

---

## 阶段 4：预生产

### 本阶段会发生什么

你会为关键界面创建 UX 规格，原型化高风险机制，把设计文档转成可实施故事，规划第一轮冲刺，并建立一个能证明核心循环好玩的垂直切片。

### 阶段 4 流水线

```text
/ux-design  -->  /prototype  -->  /create-epics  -->  /create-stories  -->  /sprint-plan
    |                |                  |                   |                       |
    v                v                  v                   v                       v
  UX 规格       一次性原型       production/epics/*/    production/epics/*/      第一轮冲刺与
  design/ux/    位于 prototypes/   EPIC.md              story-*.md             优先级故事
                                                                                production/sprints/
                                                                                sprint-*.md
    |                                                      |
    v                                                      v
 /ux-review                                          /story-readiness
（验证规格）                                           （在接手前验证每个故事）
                                                           |
                                                           v
                                                       /dev-story
                                                     （实现故事，自动路由
                                                      到正确的智能体）
                         |
                         v
                   垂直切片
                   （可游玩构建，
                    3 次无引导会话）
```

### 步骤 4.1：关键界面的 UX 规格

在写 Epic 之前，先创建 UX 规格，让故事作者知道有哪些界面，以及这些界面必须支持哪些交互。

**UX 规格：**

```
/ux-design main-menu
/ux-design core-gameplay-hud
```

三种模式：屏幕/流程、HUD、交互模式。输出到 `design/ux/`。每份规格都包含：玩家需求、布局区域、状态、交互图、数据需求、触发事件、可访问性、本地化。

它会读取你在阶段 3 写的 `accessibility-requirements.md`，以及 `technical-preferences.md` 中的输入方式配置，来驱动可访问性和输入覆盖检查——每个界面不需要重复说明这些内容。

> **提示：** `/design-system` 会为每个有 UI 要求的系统输出一个 📌 UX Flag。把这些标记当作需要编写规格的界面清单。

**交互模式库：**

```
/ux-design interaction-patterns
```

创建 `design/ux/interaction-patterns.md` —— 16 个标准控件，再加上游戏特定模式（背包槽、技能图标、HUD 条、对话框等），并附带动画和音效标准。

**UX 审查：**

```
/ux-review all
```

验证 UX 规格是否与 GDD 对齐，以及是否满足可访问性级别。输出 `APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED` 结论。

### 步骤 4.2：原型化高风险机制

不是所有内容都需要原型。以下情况适合原型化：
- 机制新颖，你不确定它好不好玩
- 技术方案有风险，你不确定它是否可行
- 两个设计方案都可行，你想亲手感受差异

```
/prototype "带动量的抓钩移动"
```

**会发生什么：** 技能会和你协作定义假设、成功标准和最小范围。`prototyper` 智能体会在隔离的 git worktree 中运行（`isolation: worktree`），所以一次性代码不会污染 `src/`。

**关键规则：** `prototype-code` 规则会有意放宽编码标准——硬编码值可以、测试不是必需的，但必须有一份 README 记录假设和发现。

### 步骤 4.3：从设计工件创建 Epic 和故事

```
/create-epics layer: foundation
/create-stories [epic-slug]   # 对每个 epic 重复
/create-epics layer: core
/create-stories [epic-slug]   # 对每个核心 epic 重复
```

`/create-epics` 会读取你的 GDD、ADR 和架构来定义 Epic 范围——每个架构模块一个 Epic。然后 `/create-stories` 会把每个 Epic 拆成可实施的故事文件，放在 `production/epics/[slug]/` 中。每个故事会嵌入：
- GDD 需求引用（TR-ID，而不是引用原文——这样更稳定）
- ADR 引用（只来自 Accepted ADR；Proposed ADR 会导致 `Status: Blocked`）
- Control Manifest 版本日期（用于检测过期）
- 引擎特定实现说明
- GDD 中的验收标准

故事创建完成后，运行 `/dev-story [story-path]` 实现其中一个——它会自动路由到正确的程序员智能体。

### 步骤 4.4：接手前验证故事

```
/story-readiness production/stories/combat-damage-calc.md
```

检查：设计完整性、架构覆盖、范围清晰度、完成定义。结论：READY / NEEDS WORK / BLOCKED。

### 步骤 4.5：工作量估算

```
/estimate production/stories/combat-damage-calc.md
```

提供带风险评估的工作量估算。

### 步骤 4.6：规划第一轮冲刺

```
/sprint-plan new
```

**会发生什么：** `producer` 智能体协作做冲刺规划：
- 询问冲刺目标和可用时间
- 将目标拆成 Must Have / Should Have / Nice to Have 任务
- 识别风险和阻塞项
- 创建 `production/sprints/sprint-01.md`
- 填充 `production/sprint-status.yaml`（机器可读的故事追踪）

### 步骤 4.7：垂直切片（硬门禁）

在进入生产之前，必须构建并游玩测试一个垂直切片：

- 一条完整端到端的核心循环，可从开始玩到结束
- 代表性质量（不是所有内容都用占位符）
- 在至少 3 次会话中无引导地游玩
- 写出游玩测试报告（`/playtest-report`）

这是一个**硬门禁**——如果没有人无引导地玩过构建，`/gate-check` 会自动 FAIL。

### 阶段 4 门禁

```
/gate-check pre-production
```

**通过要求：**

- `design/ux/` 中至少有 1 份已审查的 UX 规格
- UX 审查已完成（APPROVED 或 NEEDS REVISION，且风险已记录）
- 至少有 1 个带 README 的原型
- `production/stories/` 中存在故事文件
- 至少有 1 份冲刺计划
- 至少有 1 份游玩测试报告（垂直切片已玩 3 次以上）

---

## 阶段 5：生产

### 本阶段会发生什么

这是核心生产循环。你会在冲刺中工作（通常 1-2 周），按故事实现功能，跟踪进度，并通过结构化完成审查关闭故事。这个阶段会重复，直到内容完成。

### 阶段 5 流水线（每个冲刺）

```text
/sprint-plan new  -->  /story-readiness  -->  implement  -->  /story-done
       |                     |                    |                |
       v                     v                    v                v
  创建冲刺              故事验证通过          编写代码          8 阶段完成审查：
  sprint-status.yaml   READY 结论           测试通过          验证标准、
  被填充                                                      检查偏差、
                                                             更新故事状态
       |
       |  （每个故事重复，直到冲刺完成）
       v
  /sprint-status  （随时查看 30 行快照）
  /scope-check    （如果范围在增长）
  /retrospective  （冲刺结束时）
```

### 步骤 5.1：故事生命周期

生产阶段的核心是**故事生命周期**：

```text
/story-readiness  -->  implement  -->  /story-done  -->  next story
```

**1. 故事就绪：** 在接手故事前先验证它：

```
/story-readiness production/stories/combat-damage-calc.md
```

它会检查设计完整性、架构覆盖、ADR 状态（如果 ADR 仍是 Proposed 就阻塞）、控制清单版本（如果过期则警告）以及范围清晰度。结论：READY / NEEDS WORK / BLOCKED。

**2. 实现：** 与合适的智能体协作：

- `gameplay-programmer` 负责游戏玩法系统
- `engine-programmer` 负责核心引擎工作
- `ai-programmer` 负责 AI 行为
- `network-programmer` 负责多人功能
- `ui-programmer` 负责 UI 代码
- `tools-programmer` 负责开发工具

所有智能体都遵循协作协议：先读设计文档，提出澄清问题，展示架构选项，获得你的批准，然后再实现。

**3. 故事完成：** 当故事完成时：

```
/story-done production/stories/combat-damage-calc.md
```

它会运行一个 8 阶段完成审查：
1. 找到并读取故事文件
2. 加载引用的 GDD、ADR 和控制清单
3. 验证验收标准（可自动检查、人工检查、延期）
4. 检查 GDD/ADR 偏差（BLOCKING / ADVISORY / OUT OF SCOPE）
5. 提示进行代码审查
6. 生成完成报告（COMPLETE / COMPLETE WITH NOTES / BLOCKED）
7. 更新故事的 `Status: Complete` 和完成说明
8. 找出下一个就绪故事

审查时发现的技术债会记录到 `docs/tech-debt-register.md`。

### 步骤 5.2：冲刺追踪

随时检查进度：

```
/sprint-status
```

它会读取 `production/sprint-status.yaml`，给出一个 30 行的快速快照。

如果范围在增长：

```
/scope-check production/sprints/sprint-03.md
```

它会把当前范围与原计划比较，并标记范围增长，提出削减建议。

### 步骤 5.3：内容追踪

```
/content-audit
```

比较 GDD 规定的内容与已实现内容，尽早发现内容缺口。

### 步骤 5.4：设计变更传播

当 GDD 在故事创建之后发生变化时：

```
/propagate-design-change design/gdd/combat-system.md
```

它会对 GDD 做 git diff，找到受影响的 ADR，生成影响报告，并引导你决定 Superseded / update / keep。

### 步骤 5.5：多系统功能（团队编排）

对于跨多个领域的功能，使用团队技能：

```
/team-combat "带 HoT 和净化的治疗技能"
/team-narrative "第二幕剧情内容"
/team-ui "背包界面重做"
/team-level "森林地牢关卡"
/team-audio "战斗音频打磨"
```

每个团队技能都协调一个 6 阶段协作流程：
1. **设计** —— game-designer 提问并给出选项
2. **架构** —— lead-programmer 提出代码结构
3. **并行实现** —— 专长智能体同时工作
4. **集成** —— gameplay-programmer 统一接入
5. **验证** —— qa-tester 按验收标准测试
6. **报告** —— 协调者汇总状态

编排是自动化的，但**决策点仍然由你掌控**。

### 步骤 5.6：冲刺回顾与下一轮冲刺

在冲刺结束时：

```
/retrospective
```

它会分析计划 vs 完成、速度、阻碍和可执行改进。

然后规划下一轮冲刺：

```
/sprint-plan new
```

### 步骤 5.7：里程碑审查

在里程碑检查点：

```
/milestone-review "alpha"
```

它会产出功能完成度、质量指标、风险评估以及是否推进的建议。

### 阶段 5 门禁

```
/gate-check production
```

**通过要求：**

- 所有 MVP 故事完成
- 已进行 3 次游玩测试，覆盖新玩家、中期和难度曲线
- 已验证“好玩”假设
- 游玩测试数据中没有困惑循环

---

## 阶段 6：打磨

### 本阶段会发生什么

你的游戏功能完整了。现在要把它做得更好。这个阶段聚焦性能、平衡、可访问性、音频、视觉打磨和游玩测试。

### 阶段 6 流水线

```text
/perf-profile  -->  /balance-check  -->  /asset-audit  -->  /playtest-report (x3)
       |                  |                    |                    |
       v                  v                    v                    v
  分析 CPU/GPU        分析公式与数据         验证命名、          覆盖：新玩家、
  内存并优化瓶颈      是否导致进度异常       格式、大小           中期、难度曲线

  /tech-debt  -->  /team-polish
       |                |
       v                v
  跟踪并优先级化      协调式打磨：
  技术债条目          性能 + 美术 + 音频 + UX + QA
```

### 步骤 6.1：性能分析

```
/perf-profile
```

引导你完成结构化的性能分析：
- 建立目标（FPS、内存、平台）
- 按影响排序识别瓶颈
- 生成带代码位置和预期收益的可执行优化任务

### 步骤 6.2：平衡分析

```
/balance-check assets/data/combat_damage.json
```

分析平衡数据，检查统计异常值、破坏性的进度曲线、退化策略，以及经济不平衡。

### 步骤 6.3：资源审计

```
/asset-audit
```

验证所有资源的命名约定、文件格式标准和大小预算。

### 步骤 6.4：游玩测试（必需：3 次会话）

```
/playtest-report
```

生成结构化的游玩测试报告。必须覆盖三次会话：
- 新玩家体验
- 中期系统
- 难度曲线

### 步骤 6.5：技术债评估

```
/tech-debt
```

扫描 TODO/FIXME/HACK 注释、代码重复、过度复杂函数、缺失测试和过时依赖。每一项都会被分类并排序。

### 步骤 6.6：协同打磨

```
/team-polish "combat system"
```

并行协调 4 个专长：
1. 性能优化（performance-analyst）
2. 视觉打磨（technical-artist）
3. 音频打磨（sound-designer）
4. 手感/juice（gameplay-programmer + technical-artist）

由你设定优先级；团队会在每一步获得你的批准后执行。

### 步骤 6.7：本地化与可访问性

```
/localize src/
```

扫描硬编码字符串、会破坏翻译的字符串拼接、未考虑文本扩展的 UI 文本，以及缺失的语言文件。

可访问性会按照阶段 3 的可访问性需求文档中承诺的级别进行审计。

### 阶段 6 门禁

```
/gate-check polish
```

**通过要求：**

- 至少存在 3 份游玩测试报告
- 已完成协同打磨（`/team-polish`）
- 没有阻塞性的性能问题
- 满足可访问性级别要求

---

## 阶段 7：发布

### 本阶段会发生什么

你的游戏已经打磨好、测试过、准备就绪。现在就发出去。

### 阶段 7 流水线

```text
/release-checklist  -->  /launch-checklist  -->  /team-release
        |                       |                      |
        v                       v                      v
  发布前验证            全跨部门验证           协调：
  覆盖代码、内容、      （每个部门 Go/No-Go）    构建、QA 签字、
  商店、法务                                     部署、上线
                    另外还有：/changelog、/patch-notes、/hotfix
```

### 步骤 7.1：发布清单

```
/release-checklist v1.0.0
```

生成全面的发布前检查清单，覆盖：
- 构建验证（所有平台都能编译并运行）
- 认证要求（平台特定）
- 商店元数据（描述、截图、预告片）
- 法律合规（EULA、隐私政策、分级）
- 存档兼容性
- 分析验证

### 步骤 7.2：上线准备度（全面验证）

```
/launch-checklist
```

跨部门完整验证：

| 部门 | 检查什么 |
|------|---------|
| **工程** | 构建稳定性、崩溃率、内存泄漏、加载时间 |
| **设计** | 功能完整性、教程流程、难度曲线 |
| **美术** | 资源质量、缺失纹理、LOD 层级 |
| **音频** | 缺失音效、混音音量、空间音频 |
| **QA** | 按严重级别统计的未解决缺陷、回归套件通过率 |
| **叙事** | 对白完整性、世界观一致性、错别字 |
| **本地化** | 所有字符串已翻译、没有截断、完成语言测试 |
| **可访问性** | 合规清单、辅助功能测试 |
| **商店** | 元数据完整、截图已批准、定价已设置 |
| **市场** | 新闻包就绪、预告片、社媒排期 |
| **社区** | 补丁说明草稿、FAQ、支持渠道就绪 |
| **基础设施** | 服务器扩容、CDN 配置、监控开启 |
| **法务** | EULA 定稿、隐私政策、COPPA/GDPR 合规 |

每一项都会被标记为 **Go / No-Go**。全部为 Go 才能发布。

### 步骤 7.3：生成面向玩家的内容

```
/patch-notes v1.0.0
```

根据 git 历史和冲刺数据生成玩家友好的补丁说明，把开发语言翻译成玩家语言。

```
/changelog v1.0.0
```

生成内部变更日志（更技术化，供团队使用）。

### 步骤 7.4：协调发布

```
/team-release
```

协调 release-manager、QA 和 DevOps 完成：
1. 发布前验证
2. 构建管理
3. 最终 QA 签字
4. 部署准备
5. Go/No-Go 决策

### 步骤 7.5：发布

`validate-push` 钩子在你向 `main` 或 `develop` 推送时会发出警告。这是刻意设计的——发布推送应该是经过深思熟虑的：

```bash
git tag v1.0.0
git push origin main --tags
```

### 步骤 7.6：上线后

**热修复流程** 适用于严重生产缺陷：

```
/hotfix "当背包超过 99 个物品时玩家丢失存档"
```

它会绕过正常冲刺流程，但保留完整审计轨迹：
1. 创建热修复分支
2. 实现修复
3. 确保回灌到开发分支
4. 记录事件

**上线后复盘**：当游戏稳定后：

```
Ask Claude to create a post-mortem using the template at
.claude/docs/templates/post-mortem.md
```

---

## 横切关注点

这些主题贯穿所有阶段。

### 主管审查模式

主管门禁是专门的智能体，会在工作流关键步骤审查你的工作。默认情况下它们会在每个检查点运行。你可以控制审查强度。

**在 `/start` 时一次性设置审查强度。** 保存到 `production/review-mode.txt`。

| 模式 | 运行什么 | 适合谁 |
|------|----------|--------|
| `full` | 每一步都运行所有主管门禁 | 新项目、学习系统 |
| `lean` | 只在阶段转换（`/gate-check`）时运行主管 | 有经验的开发者 |
| `solo` | 不运行主管审查 | game jam、原型、追求速度 |

**临时覆盖** 不会改变全局设置：

```
/brainstorm space horror --review full
/architecture-decision --review solo
```

`--review` 标志适用于所有使用门禁的技能。你可以随时直接编辑 `production/review-mode.txt`，或者重新运行 `/start` 来修改全局模式。

完整的门禁定义与检查模式见：`.claude/docs/director-gates.md`

---

### 协作协议

这个系统是**用户驱动的协作式**，不是自主执行式。

**模式：** Question > Options > Decision > Draft > Approval

每次智能体交互都遵循这个模式：
1. 智能体提出澄清问题
2. 智能体给出 2-4 个选项，并附上权衡和理由
3. 由你来决定
4. 智能体根据你的决定起草
5. 你审阅并修订
6. 智能体在写入前先问“我可以把它写到 [filepath] 吗？”

完整协议和示例见 `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`。

### AskUserQuestion 工具

智能体会使用 `AskUserQuestion` 工具来结构化呈现选项。模式是先解释，再捕获：先在对话文本中完整分析，再用干净的 UI 选择器做决定。它适用于设计选择、架构决策和战略问题。不要把它用于开放式探索问题或简单的是/否确认。

### 智能体协调（3 层层级）

```text
Tier 1（主管）：creative-director、technical-director、producer
                                          |
Tier 2（负责人）：game-designer、lead-programmer、art-director、
                  audio-director、narrative-director、qa-lead、
                  release-manager、localization-lead
                                          |
Tier 3（专长）： gameplay-programmer、engine-programmer、
                  ai-programmer、network-programmer、ui-programmer、
                  tools-programmer、systems-designer、level-designer、
                  economy-designer、world-builder、writer、
                  technical-artist、sound-designer、ux-designer、
                  qa-tester、performance-analyst、devops-engineer、
                  analytics-engineer、accessibility-specialist、
                  live-ops-designer、prototyper、security-engineer、
                  community-manager、godot-specialist、
                  godot-gdscript-specialist、godot-shader-specialist、
                  unity-specialist、unity-csharp-specialist、
                  unreal-specialist、unreal-blueprint-specialist、
                  unreal-cpp-specialist
```

**协调规则：**
- 垂直委托：主管 > 负责人 > 专长。复杂决策不要跳级。
- 横向协商：同层级智能体可以互相咨询，但不能在其领域外做出约束性决策。
- 冲突解决：设计冲突交给 `creative-director`。技术冲突交给 `technical-director`。范围冲突交给 `producer`。
- 不允许跨域单方面修改。

### 自动化钩子（安全网）

系统有 12 个会自动运行的钩子：

| 钩子 | 触发时机 | 做什么 |
|------|---------|--------|
| `session-start.sh` | 会话开始 | 显示分支、最近提交，检测 active.md 以便恢复 |
| `detect-gaps.sh` | 会话开始 | 检测新项目（无引擎、无概念），建议运行 `/start` |
| `pre-compact.sh` | 压缩前 | 将会话状态写回对话，便于自动恢复 |
| `post-compact.sh` | 压缩后 | 提醒 Claude 从 `active.md` 恢复会话状态 |
| `notify.sh` | 通知事件 | 通过 PowerShell 显示 Windows 弹窗 |
| `validate-commit.sh` | 提交前 | 检查是否引用设计文档、JSON 是否有效、是否存在硬编码值 |
| `validate-push.sh` | 推送前 | 警告推送到 main/develop |
| `validate-assets.sh` | 提交前 | 检查资源命名和大小 |
| `validate-skill-change.sh` | 技能文件写入后 | 提醒在 `.claude/skills/` 变更后运行 `/skill-test` |
| `log-agent.sh` | 智能体启动 | 记录智能体调用以留审计轨迹 |
| `log-agent-stop.sh` | 智能体停止 | 完成智能体审计轨迹（启动 + 停止） |
| `session-stop.sh` | 会话结束 | 最终会话记录 |

### 上下文韧性

**会话状态文件：** `production/session-state/active.md` 是一个活跃检查点。每完成一个重要里程碑就更新它。在任何中断（压缩、崩溃、`/clear`）后，先读取这个文件。

**增量写入：** 创建多部分文档时，每批准一个部分就立即写入文件。这意味着已完成的部分在崩溃和上下文压缩后仍然存在。关于已写入部分的旧讨论可以安全压缩。

**自动恢复：** `session-start.sh` 钩子会自动检测并预览 `active.md`。`pre-compact.sh` 钩子会在压缩前把状态导入对话。

**冲刺状态追踪：** `production/sprint-status.yaml` 是机器可读的故事追踪器，由 `/sprint-plan`（初始化）和 `/story-done`（状态更新）写入，由 `/sprint-status`、`/help` 和 `/story-done`（下一个故事）读取。这样就不需要脆弱的 Markdown 扫描了。

### 棕地迁移

对于已经有部分工件的现有项目：

```
/adopt
```

或针对性使用：

```
/adopt gdds
/adopt adrs
/adopt stories
/adopt infra
```

它会审计已有工件的**格式**（不是存在性），把缺口分为 BLOCKING/HIGH/MEDIUM/LOW，构建有顺序的迁移计划，并写入 `docs/adoption-plan-[date].md`。核心原则：MIGRATION 而不是 REPLACEMENT——它不会重生成已有工作，只补缺口。

单个技能也支持回填模式：

```
/design-system retrofit design/gdd/combat-system.md
/architecture-decision retrofit docs/architecture/adr-005.md
```

这些模式会检测哪些部分已经存在、哪些缺失，只填补缺口。

### 门禁系统

阶段门禁是正式检查点。用对应的转换名称运行 `/gate-check`：

```
/gate-check concept              # 概念 -> 系统设计
/gate-check systems-design       # 系统设计 -> 技术准备
/gate-check technical-setup      # 技术准备 -> 预生产
/gate-check pre-production       # 预生产 -> 生产
/gate-check production           # 生产 -> 打磨
/gate-check polish               # 打磨 -> 发布
```

**结论：**
- **PASS** —— 所有要求都满足，可以进入下一阶段
- **CONCERNS** —— 要求满足但存在已知风险，可以通过
- **FAIL** —— 要求未满足，阻止推进并给出明确修复方案

门禁通过时，`production/stage.txt` 会被更新（只有这时），它控制状态行和 `/help` 的行为。

### 逆向文档化

适用于已有代码但缺少设计文档的情况（棕地迁移后很常见）：

```
/reverse-document src/gameplay/combat/
```

读取已有代码，并从中生成 GDD 格式的设计文档。

---

## 附录 A：智能体快速参考

### “我需要做 X —— 应该用哪个智能体？”

| 我需要…… | 智能体 | 层级 |
|-----------|--------|------|
| 想出一个游戏点子 | `/brainstorm` 技能 | -- |
| 设计游戏机制 | `game-designer` | 2 |
| 设计具体公式/数值 | `systems-designer` | 3 |
| 设计关卡 | `level-designer` | 3 |
| 设计掉落/经济 | `economy-designer` | 3 |
| 构建世界观 | `world-builder` | 3 |
| 写对白 | `writer` | 3 |
| 规划故事 | `narrative-director` | 2 |
| 规划冲刺 | `producer` | 1 |
| 做创意决策 | `creative-director` | 1 |
| 做技术决策 | `technical-director` | 1 |
| 实现游戏代码 | `gameplay-programmer` | 3 |
| 实现核心引擎系统 | `engine-programmer` | 3 |
| 实现 AI 行为 | `ai-programmer` | 3 |
| 实现多人功能 | `network-programmer` | 3 |
| 实现 UI | `ui-programmer` | 3 |
| 构建开发工具 | `tools-programmer` | 3 |
| 审查代码架构 | `lead-programmer` | 2 |
| 创建着色器 / VFX | `technical-artist` | 3 |
| 定义视觉风格 | `art-director` | 2 |
| 定义音频风格 | `audio-director` | 2 |
| 设计音效 | `sound-designer` | 3 |
| 设计 UX 流程 | `ux-designer` | 3 |
| 编写测试用例 | `qa-tester` | 3 |
| 规划测试策略 | `qa-lead` | 2 |
| 分析性能 | `performance-analyst` | 3 |
| 配置 CI/CD | `devops-engineer` | 3 |
| 设计分析埋点 | `analytics-engineer` | 3 |
| 检查可访问性 | `accessibility-specialist` | 3 |
| 规划 Live Ops | `live-ops-designer` | 3 |
| 管理发布 | `release-manager` | 2 |
| 管理本地化 | `localization-lead` | 2 |
| 快速原型 | `prototyper` | 3 |
| 审计安全 | `security-engineer` | 3 |
| 与玩家沟通 | `community-manager` | 3 |
| Godot 专项帮助 | `godot-specialist` | 3 |
| GDScript 专项帮助 | `godot-gdscript-specialist` | 3 |
| Godot 着色器帮助 | `godot-shader-specialist` | 3 |
| GDExtension 模块 | `godot-gdextension-specialist` | 3 |
| Unity 专项帮助 | `unity-specialist` | 3 |
| Unity DOTS/ECS | `unity-dots-specialist` | 3 |
| Unity 着色器/VFX | `unity-shader-specialist` | 3 |
| Unity Addressables | `unity-addressables-specialist` | 3 |
| Unity UI Toolkit | `unity-ui-specialist` | 3 |
| Unreal 专项帮助 | `unreal-specialist` | 3 |
| Unreal GAS | `ue-gas-specialist` | 3 |
| Unreal 蓝图 | `ue-blueprint-specialist` | 3 |
| Unreal 复制系统 | `ue-replication-specialist` | 3 |
| Unreal UMG/CommonUI | `ue-umg-specialist` | 3 |

### 智能体层级

```text
                    creative-director / technical-director / producer
                                         |
          ---------------------------------------------------------------
          |            |           |           |          |        |       |
    game-designer  lead-prog  art-dir  audio-dir  narr-dir  qa-lead  release-mgr
          |            |           |           |          |        |        |
     specialists  programmers  tech-art  snd-design  writer   qa-tester  devops
     (systems,    (gameplay,             (sound)     (world-  (perf,     (analytics,
      economy,     engine,                           builder)  access.)   security)
      level)       ai, net,
                   ui, tools)
```

**升级规则：** 如果两个智能体意见不一致，就往上升级。设计冲突交给 `creative-director`。技术冲突交给 `technical-director`。范围冲突交给 `producer`。

---

## 附录 B：斜杠命令快速参考

### 按类别分组的全部 66 条命令

#### 入门与导航（5）

| 命令 | 作用 | 阶段 |
|------|------|------|
| `/start` | 引导式入门，路由到正确工作流 | 任意（首次会话） |
| `/help` | 根据上下文告诉你“下一步做什么” | 任意 |
| `/project-stage-detect` | 全项目审计，判断当前阶段 | 任意 |
| `/setup-engine` | 配置引擎、固定版本、设置偏好 | 1 |
| `/adopt` | 棕地审计与迁移计划 | 任意（已有项目） |

#### 游戏设计（6）

| 命令 | 作用 | 阶段 |
|------|------|------|
| `/brainstorm` | 结合 MDA 的协作式创意发散 | 1 |
| `/map-systems` | 把概念拆成系统索引 | 1-2 |
| `/design-system` | 引导式、按章节撰写 GDD | 2 |
| `/quick-design` | 小改动的轻量规格 | 2+ |
| `/review-all-gdds` | 跨 GDD 一致性与设计理论审查 | 2 |
| `/propagate-design-change` | 找出受 GDD 变更影响的 ADR/故事 | 5 |

#### UX 与界面（2）

| 命令 | 作用 | 阶段 |
|------|------|------|
| `/ux-design` | 编写 UX 规格（屏幕/流程、HUD、模式） | 4 |
| `/ux-review` | 验证 UX 规格的可访问性和 GDD 对齐 | 4 |

#### 架构（4）

| 命令 | 作用 | 阶段 |
|------|------|------|
| `/create-architecture` | 总体架构文档 | 3 |
| `/architecture-decision` | 创建或回填 ADR | 3 |
| `/architecture-review` | 验证所有 ADR 和依赖顺序 | 3 |
| `/create-control-manifest` | 从已接受 ADR 生成扁平程序员规则 | 3 |

#### 故事与冲刺（8）

| 命令 | 作用 | 阶段 |
|------|------|------|
| `/create-epics` | 将 GDD + ADR 转成 Epic（每个模块一个） | 4 |
| `/create-stories` | 把单个 Epic 拆成故事文件 | 4 |
| `/dev-story` | 实现一个故事——自动路由到正确程序员智能体 | 5 |
| `/sprint-plan` | 创建或管理冲刺计划 | 4-5 |
| `/sprint-status` | 30 行的快速冲刺快照 | 5 |
| `/story-readiness` | 验证故事可否接手实现 | 4-5 |
| `/story-done` | 8 阶段故事完成审查 | 5 |
| `/estimate` | 工作量估算与风险评估 | 4-5 |

#### 审查与分析（10）

| 命令 | 作用 | 阶段 |
|------|------|------|
| `/design-review` | 按 8 部分标准验证 GDD | 1-2 |
| `/code-review` | 架构代码审查 | 5+ |
| `/balance-check` | 游戏平衡公式分析 | 5-6 |
| `/asset-audit` | 资源命名、格式、大小校验 | 6 |
| `/content-audit` | 比对 GDD 指定内容与已实现内容 | 5 |
| `/scope-check` | 检测范围膨胀 | 5 |
| `/perf-profile` | 性能分析流程 | 6 |
| `/tech-debt` | 技术债扫描与优先级排序 | 6 |
| `/gate-check` | 带 PASS/CONCERNS/FAIL 的正式阶段门禁 | 所有转换 |
| `/reverse-document` | 从已有代码生成设计文档 | 任意 |

#### QA 与测试（9）

| 命令 | 作用 | 阶段 |
|------|------|------|
| `/qa-plan` | 为冲刺或功能生成 QA 计划 | 5 |
| `/smoke-check` | QA 交接前的关键路径冒烟测试门禁 | 5-6 |
| `/soak-test` | 长时间游玩会话的浸泡测试流程 | 6 |
| `/regression-suite` | 映射测试覆盖、找出缺少回归测试的已修复 bug | 5-6 |
| `/test-setup` | 搭建测试框架和 CI/CD 流水线 | 4 |
| `/test-helpers` | 生成引擎专用测试辅助库 | 4-5 |
| `/test-evidence-review` | 测试文件与人工证据质量审查 | 5 |
| `/test-flakiness` | 从 CI 日志中检测不稳定测试 | 5-6 |
| `/skill-test` | 验证技能文件的结构和行为正确性 | 任意 |

#### 生产管理（6）

| 命令 | 作用 | 阶段 |
|------|------|------|
| `/milestone-review` | 里程碑进度和是否继续推进 | 5 |
| `/retrospective` | 冲刺回顾分析 | 5 |
| `/bug-report` | 结构化 bug 报告创建 | 5+ |
| `/bug-triage` | 重新评估开放 bug 的优先级、严重性和负责人 | 5+ |
| `/playtest-report` | 结构化游玩测试报告 | 4-6 |
| `/onboard` | 新团队成员入职 | 任意 |

#### 发布（5）

| 命令 | 作用 | 阶段 |
|------|------|------|
| `/release-checklist` | 发布前验证 | 7 |
| `/launch-checklist` | 完整跨部门上线准备度检查 | 7 |
| `/changelog` | 自动生成内部变更日志 | 7 |
| `/patch-notes` | 面向玩家的补丁说明 | 7 |
| `/hotfix` | 紧急修复流程 | 7+ |

#### 创意（2）

| 命令 | 作用 | 阶段 |
|------|------|------|
| `/prototype` | 在隔离 worktree 中做一次性原型 | 4 |
| `/localize` | 字符串提取与校验 | 6-7 |

#### 团队编排（9）

| 命令 | 作用 | 阶段 |
|------|------|------|
| `/team-combat` | 战斗功能：从设计到实现 | 5 |
| `/team-narrative` | 叙事内容：从结构到对白 | 5 |
| `/team-ui` | UI 功能：从 UX 规格到打磨完成的实现 | 5 |
| `/team-level` | 关卡：从布局到完整遭遇 | 5 |
| `/team-audio` | 音频：从方向到已实现事件 | 5-6 |
| `/team-polish` | 协同打磨：性能 + 美术 + 音频 + QA | 6 |
| `/team-release` | 发布协同：构建 + QA + 部署 | 7 |
| `/team-live-ops` | Live Ops 规划：赛季活动、战斗通行证、留存 | 7+ |
| `/team-qa` | 完整 QA 流程：策略、执行、覆盖、签字 | 6-7 |

---

## 附录 C：常见工作流

### 工作流 1：“我刚开始，还没有游戏点子”

```text
1. /start（根据你所在情况路由）
2. /brainstorm（协作式创意发散，选一个概念）
3. /setup-engine（固定引擎和版本）
4. 对概念文档做 /design-review（可选，推荐）
5. /map-systems（把概念拆成带依赖和优先级的系统）
6. /gate-check concept（确认你已经准备好进入系统设计）
7. 每个系统跑 /design-system（引导式 GDD 编写）
```

### 工作流 2：“我已经有设计，想开始写代码”

```text
1. 对每个 GDD 做 /design-review（确保足够扎实）
2. /review-all-gdds（跨 GDD 一致性）
3. /gate-check systems-design
4. /create-architecture + /architecture-decision（每个重大决策）
5. /architecture-review
6. /create-control-manifest
7. /gate-check technical-setup
8. /create-epics layer: foundation + /create-stories [slug]（定义 Epic，拆成故事）
9. /sprint-plan new
10. /story-readiness -> implement -> /story-done（故事生命周期）
```

### 工作流 3：“我需要在生产中加入一个复杂功能”

```text
1. /design-system 或 /quick-design（取决于范围）
2. /design-review 验证
3. 如果在修改现有 GDD，运行 /propagate-design-change
4. /estimate 评估工作量和风险
5. 用合适的团队技能（/team-combat、/team-narrative、/team-ui 等）
6. 完成后运行 /story-done
7. 如果影响游戏平衡，再跑 /balance-check
```

### 工作流 4：“生产中出了问题”

```text
1. /hotfix "问题描述"
2. 在 hotfix 分支上实现修复
3. 对修复做 /code-review
4. 运行测试
5. 对 hotfix 构建跑 /release-checklist
6. 部署并回灌
```

### 工作流 5：“我有一个现有项目，想用这个系统”

```text
1. /start（选择路径 D —— 现有工作）
2. /project-stage-detect（判断当前阶段）
3. /adopt（审计现有工件，制定迁移计划）
4. /design-system retrofit [path]（补 GDD 缺口）
5. /architecture-decision retrofit [path]（补 ADR 缺口）
6. 在合适的阶段转换处运行 /gate-check
```

### 工作流 6：“开始新的冲刺”

```text
1. /retrospective（回顾上一个冲刺）
2. /sprint-plan new（创建下一轮冲刺）
3. /scope-check（确认范围可控）
4. 每个故事接手前跑 /story-readiness
5. 实现故事
6. 每完成一个故事跑 /story-done
7. 用 /sprint-status 查看快速进度
```

### 工作流 7：“发布游戏”

```text
1. /gate-check polish（确认打磨阶段完成）
2. /tech-debt（决定哪些技术债可接受）
3. /localize（最终本地化）
4. /release-checklist v1.0.0
5. /launch-checklist（完整跨部门验证）
6. /team-release（协调发布）
7. /patch-notes 和 /changelog
8. 发布！
9. 如果上线后出问题，用 /hotfix
10. 稳定后做 post-mortem
```

### 工作流 8：“我迷路了 / 不知道下一步”

```text
1. /help（读取当前阶段、检查工件、告诉你下一步）
2. 如果 /help 还不够：/project-stage-detect（全量审计）
3. 如果阶段看起来不对：对你认为所在的阶段运行 /gate-check
```

---

## 使用系统的小贴士

1. **永远先设计，再实现。** 这个智能体系统默认设计文档先于代码存在。智能体会持续引用 GDD。
2. **跨领域功能用团队技能。** 不要手动协调 4 个智能体——让 `/team-combat`、`/team-narrative` 等去做编排。
3. **相信规则系统。** 规则指出代码问题时就修复它。规则承载了独立游戏开发的经验教训（数据驱动值、delta time、可访问性等）。
4. **主动压缩。** 当上下文使用率达到约 65-70% 时，执行 compact 或 `/clear`。预压缩钩子会保存你的进度。不要等到上限。
5. **用对层级的智能体。** 不要让 `creative-director` 写着色器，也不要让 `qa-tester` 做设计决策。层级有其原因。
6. **不确定时运行 /help。** 它会读取你真实的项目状态，并告诉你唯一最重要的下一步。
7. **在把设计交给程序员前先跑 /design-review。** 这可以尽早发现不完整规格，减少返工。
8. **每个重大功能后运行 /code-review。** 在架构问题扩散前先捕捉它们。
9. **先原型高风险机制。** 一天的原型，可能省掉一周的生产时间。
10. **让冲刺计划保持真实。** 定期使用 /scope-check。范围膨胀是独立游戏最常见的杀手。
11. **用 ADR 记录决策。** 未来的你会感谢现在的你把“为什么”记录下来。
12. **严格使用故事生命周期。** 接手前跑 `/story-readiness`，完成后跑 `/story-done`。这能尽早捕捉偏差并保持流水线诚实。
13. **尽早且经常写入文件。** 增量章节写入能让设计决策在崩溃和压缩后仍然存在。文件是记忆，不是对话。