# 游戏工作室智能体架构 -- 快速入门指南

## 这是什么？

这是一套完整的 Claude Code 游戏开发智能体架构。它将 48 个专业 AI 智能体组织成一个工作室层级，模拟真实游戏团队的分工、委托规则和协作协议。它包含 Godot、Unity 和 Unreal 的引擎专家智能体——每个引擎都有针对主要子系统的专门子智能体。所有设计智能体和模板都基于成熟的游戏设计理论（MDA 框架、自我决定理论、心流、Bartle 玩家类型）。请使用与你项目匹配的引擎集合。

## 如何使用

### 1. 了解层级结构

智能体分为三个层级：

- **Tier 1（Opus）**：负责高层决策的总监
  - `creative-director` -- 愿景与创意冲突解决
  - `technical-director` -- 架构与技术决策
  - `producer` -- 进度、协调与风险管理

- **Tier 2（Sonnet）**：拥有各自领域的部门负责人
  - `game-designer`、`lead-programmer`、`art-director`、`audio-director`、
    `narrative-director`、`qa-lead`、`release-manager`、`localization-lead`

- **Tier 3（Sonnet/Haiku）**：在各自领域内执行工作的专家
  - 设计师、程序员、艺术家、撰稿人、测试员、工程师

### 2. 为任务选择合适的智能体

问自己：“在真实工作室里，哪个部门会处理这个？”

| 我需要... | 使用这个智能体 |
|-------------|---------------|
| 设计新机制 | `game-designer` |
| 编写战斗代码 | `gameplay-programmer` |
| 创建着色器 | `technical-artist` |
| 编写对话 | `writer` |
| 规划下一个冲刺 | `producer` |
| 审查代码质量 | `lead-programmer` |
| 编写测试用例 | `qa-tester` |
| 设计关卡 | `level-designer` |
| 修复性能问题 | `performance-analyst` |
| 配置 CI/CD | `devops-engineer` |
| 设计战利品表 | `economy-designer` |
| 解决创意冲突 | `creative-director` |
| 做架构决策 | `technical-director` |
| 管理发布 | `release-manager` |
| 准备翻译字符串 | `localization-lead` |
| 快速验证机制想法 | `prototyper` |
| 审查安全问题 | `security-engineer` |
| 检查可访问性合规 | `accessibility-specialist` |
| 获取 Unreal Engine 建议 | `unreal-specialist` |
| 获取 Unity 建议 | `unity-specialist` |
| 获取 Godot 建议 | `godot-specialist` |
| 设计 GAS 能力/效果 | `ue-gas-specialist` |
| 定义 BP/C++ 边界 | `ue-blueprint-specialist` |
| 实现 UE 复制 | `ue-replication-specialist` |
| 构建 UMG/CommonUI 界面 | `ue-umg-specialist` |
| 设计 DOTS/ECS 架构 | `unity-dots-specialist` |
| 编写 Unity 着色器/VFX | `unity-shader-specialist` |
| 管理 Addressables 资源 | `unity-addressables-specialist` |
| 构建 UI Toolkit/UGUI 界面 | `unity-ui-specialist` |
| 编写惯用 GDScript | `godot-gdscript-specialist` |
| 创建 Godot 着色器 | `godot-shader-specialist` |
| 构建 GDExtension 模块 | `godot-gdextension-specialist` |
| 规划直播活动和赛季 | `live-ops-designer` |
| 撰写玩家补丁说明 | `community-manager` |
| 头脑风暴新游戏点子 | 使用 `/brainstorm` 技能 |

### 3. 使用斜杠命令处理常见任务

| 命令 | 功能 |
|---------|-------------|
| `/start` | 首次入门 -- 询问你当前处于什么阶段，并引导到正确流程 |
| `/design-review` | 审查设计文档 |
| `/code-review` | 审查代码质量与架构 |
| `/playtest-report` | 生成结构化游玩测试报告模板 |
| `/balance-check` | 分析游戏平衡数据并标记异常值 |
| `/sprint-plan` | 生成或更新冲刺计划 |
| `/bug-report` | 创建结构化缺陷报告 |
| `/architecture-decision` | 创建架构决策记录（ADR） |
| `/asset-audit` | 审计资源命名、大小和管线合规性 |
| `/milestone-review` | 审查里程碑进度并生成状态报告 |
| `/onboard` | 为新贡献者或智能体生成入职上下文 |
| `/prototype` | 搭建可丢弃原型以验证机制或技术方案 |
| `/release-checklist` | 为当前构建生成并验证预发布清单 |
| `/changelog` | 从 git 提交和冲刺数据自动生成变更日志 |
| `/retrospective` | 运行结构化冲刺或里程碑回顾 |
| `/estimate` | 生成带复杂性与风险分解的结构化工作评估 |
| `/hotfix` | 紧急修复流程，带审计跟踪，绕过正常冲刺流程 |
| `/tech-debt` | 扫描、跟踪、优先级排序并报告技术债务 |
| `/scope-check` | 分析功能或冲刺范围与原始计划的差异，标记范围蔓延 |
| `/localize` | 本地化工作流：提取字符串、验证、准备翻译 |
| `/perf-profile` | 结构化性能分析与瓶颈识别 |
| `/project-stage-detect` | 自动分析项目状态、检测阶段、识别缺口并推荐下一步 |
| `/reverse-document` | 从现有实现反向生成设计或架构文档 |
| `/team-combat` | 协调战斗团队：game-designer + gameplay-programmer + ai-programmer + technical-artist + sound-designer + qa-tester |
| `/team-narrative` | 协调叙事团队：narrative-director + writer + world-builder + level-designer |
| `/team-ui` | 协调 UI 团队：ux-designer + ui-programmer + art-director |
| `/team-release` | 协调发布团队：release-manager + qa-lead + devops-engineer + producer |
| `/team-polish` | 协调打磨团队：performance-analyst + technical-artist + sound-designer + qa-tester |
| `/team-audio` | 协调音频团队：audio-director + sound-designer + technical-artist + gameplay-programmer |
| `/team-level` | 协调关卡团队：level-designer + narrative-director + world-builder + art-director + systems-designer + qa-tester |
| `/launch-checklist` | 跨所有部门进行完整的发布准备验证 |
| `/patch-notes` | 从 git 历史和内部数据生成面向玩家的补丁说明 |
| `/brainstorm` | 使用专业工作室方法（MDA、SDT、Bartle、动词优先）进行引导式构思 |
| `/gate-check` | 验证开发阶段之间推进的就绪性（通过/关注/失败） |
| `/map-systems` | 将游戏概念分解为系统，映射依赖关系，优先排序设计顺序，并指导每个系统的 GDD |
| `/design-system` | 针对单个游戏系统的引导式、分节 GDD 创作，支持交叉引用与增量写作 |
| `/setup-engine` | 配置引擎 + 版本，检测知识缺口，填充版本感知参考文档 |

### 4. 使用模板创建新文档

模板位于 `.claude/docs/templates/`：

- `game-design-document.md` -- 用于新机制与系统
- `architecture-decision-record.md` -- 用于技术决策
- `architecture-traceability.md` -- 将 GDD 需求映射到 ADR 再到故事 ID
- `risk-register-entry.md` -- 用于新增风险
- `narrative-character-sheet.md` -- 用于新角色
- `test-plan.md` -- 用于功能测试计划
- `sprint-plan.md` -- 用于冲刺规划
- `milestone-definition.md` -- 用于新里程碑
- `level-design-document.md` -- 用于新关卡
- `game-pillars.md` -- 用于核心设计支柱
- `art-bible.md` -- 用于视觉风格参考
- `technical-design-document.md` -- 用于单系统技术设计
- `post-mortem.md` -- 用于项目/里程碑复盘
- `sound-bible.md` -- 用于音频风格参考
- `release-checklist-template.md` -- 用于平台发布清单
- `changelog-template.md` -- 用于面向玩家的补丁说明
- `release-notes.md` -- 用于面向玩家的发布说明
- `incident-response.md` -- 用于线上事故响应手册
- `game-concept.md` -- 用于初始游戏概念（MDA、SDT、Flow、Bartle）
- `pitch-document.md` -- 用于向利益相关者提案
- `economy-model.md` -- 用于虚拟经济设计（sink/faucet 模型）
- `faction-design.md` -- 用于派系身份、背景与玩法定位
- `systems-index.md` -- 用于系统拆分与依赖映射
- `project-stage-report.md` -- 用于项目阶段检测输出
- `design-doc-from-implementation.md` -- 用于从实现反向整理成 GDD
- `architecture-doc-from-code.md` -- 用于从代码反向整理成架构文档
- `concept-doc-from-prototype.md` -- 用于从原型反向整理成概念文档
- `ux-spec.md` -- 用于单屏 UX 规格（布局区域、状态、事件）
- `hud-design.md` -- 用于整体 HUD 理念、区域与元素规格
- `accessibility-requirements.md` -- 用于项目级可访问性等级与功能矩阵
- `interaction-pattern-library.md` -- 用于标准 UI 控件与游戏专用模式
- `player-journey.md` -- 用于按时间尺度划分的 6 阶段情绪曲线与留存钩子
- `difficulty-curve.md` -- 用于难度轴、引导曲线与跨系统交互
- `test-evidence.md` -- 用于记录手动测试证据（截图、走查笔记）

另外在 `.claude/docs/templates/collaborative-protocols/` 中（供智能体使用，通常不直接编辑）：

- `design-agent-protocol.md` -- 设计智能体的“提问 -> 选项 -> 草案 -> 批准”循环
- `implementation-agent-protocol.md` -- 程序智能体的故事接取到 `/story-done` 流程
- `leadership-agent-protocol.md` -- 总监层的跨部门委托与升级流程

### 5. 遵循协调规则

1. 工作自上而下流转：总监 -> 负责人 -> 专家
2. 冲突向上升级
3. 跨部门工作由 `producer` 协调
4. 智能体未经委托不得修改其领域之外的文件
5. 所有决策都要记录

## 新项目的第一步

**不知道从哪里开始？** 运行 `/start`。它会询问你当前所处阶段，并将你路由到正确流程。不会对你的游戏、引擎或经验水平做任何假设。

如果你已经知道自己需要什么，可以直接进入对应路径：

### 路径 A：“我完全不知道要做什么”

1. **运行 `/start`**（或 `/brainstorm open`）——引导式创意探索：
   你喜欢什么、你玩过什么、你的约束
   - 生成 3 个概念，帮助你选择其中一个，定义核心循环和支柱
   - 产出游戏概念文档并推荐引擎
2. **设置引擎** —— 运行 `/setup-engine`（使用 brainstorm 的推荐）
   - 配置 CLAUDE.md，检测知识缺口，填充参考文档
   - 创建 `.claude/docs/technical-preferences.md`，包含命名约定、
     性能预算和引擎特定默认值
   - 如果引擎版本新于 LLM 的训练数据，它会从网络获取当前文档，以便智能体建议正确的 API
3. **验证概念** —— 运行 `/design-review design/gdd/game-concept.md`
4. **拆分系统** —— 运行 `/map-systems` 列出所有系统与依赖
5. **逐个设计系统** —— 运行 `/design-system [system-name]`（或 `/map-systems next`）
   按依赖顺序编写 GDD
6. **测试核心循环** —— 运行 `/prototype [core-mechanic]`
7. **进行游玩测试** —— 运行 `/playtest-report` 验证假设
8. **规划第一轮冲刺** —— 运行 `/sprint-plan new`
9. 开始构建

### 路径 B：“我知道自己想做什么”

如果你已经有游戏概念和引擎选择：

1. **设置引擎** —— 运行 `/setup-engine [engine] [version]`
   （例如：`/setup-engine godot 4.6`）——同时创建技术偏好
2. **编写游戏支柱** —— 委托给 `creative-director`
3. **拆分系统** —— 运行 `/map-systems` 枚举系统与依赖
4. **逐个设计系统** —— 运行 `/design-system [system-name]` 编写按依赖顺序排列的 GDD
5. **创建首个 ADR** —— 运行 `/architecture-decision`
6. **创建第一个里程碑** 到 `production/milestones/`
7. **规划第一轮冲刺** —— 运行 `/sprint-plan new`
8. 开始构建

### 路径 C：“我知道游戏，但不知道引擎”

如果你有概念但不知道哪个引擎合适：

1. **运行 `/setup-engine`** 并且不带参数——它会询问你的游戏需求
   （2D/3D、平台、团队规模、语言偏好），然后根据你的回答推荐引擎
2. 从第 2 步开始沿用路径 B

### 路径 D：“我已经有现成项目”

如果你已经有设计文档、原型或代码：

1. **运行 `/start`**（或 `/project-stage-detect`）——分析现状、
   识别缺口并推荐下一步
2. **运行 `/adopt`** 如果你已有 GDD、ADR 或故事——审计内部格式合规性并生成编号迁移计划，填补缺口而不覆盖现有工作
3. **如有需要先配置引擎** —— 如果尚未配置则运行 `/setup-engine`
4. **验证阶段就绪性** —— 运行 `/gate-check` 查看当前所处阶段
5. **规划下一轮冲刺** —— 运行 `/sprint-plan new`

## 文件结构参考

```text
CLAUDE.md                          -- 主配置（先读它，约 60 行）
.claude/
  settings.json                    -- Claude Code 钩子与项目设置
  agents/                          -- 48 个智能体定义（YAML frontmatter）
  skills/                          -- 68 个斜杠命令定义（YAML frontmatter）
  hooks/                           -- 12 个钩子脚本（.sh），由 settings.json 连接
  rules/                           -- 11 个路径专属规则文件
  docs/
    quick-start.md                 -- 本文件
    technical-preferences.md       -- 项目专属标准（由 /setup-engine 填充）
    coding-standards.md            -- 编码与设计文档标准
    coordination-rules.md          -- 智能体协调规则
    context-management.md          -- 上下文预算与压缩说明
    directory-structure.md         -- 项目目录布局
    workflow-catalog.yaml          -- 7 阶段流水线定义（由 /help 读取）
    setup-requirements.md          -- 系统先决条件（Git Bash、jq、Python）
    settings-local-template.md     -- 个人 settings.local.json 指南
    templates/                     -- 37 个文档模板
```