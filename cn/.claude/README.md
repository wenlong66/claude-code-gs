<p align="center">
  <h1 align="center">Claude Code 游戏工作室</h1>
  <p align="center">
    将单一的 Claude Code 会话转变为完整的游戏开发工作室。
    <br />
    48 个智能体。37 个工作流程。一个协调的 AI 团队。
  </p>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href=".claude/agents"><img src="https://img.shields.io/badge/agents-48-blueviolet" alt="48 Agents"></a>
  <a href=".claude/skills"><img src="https://img.shields.io/badge/skills-37-green" alt="37 Skills"></a>
  <a href=".claude/hooks"><img src="https://img.shields.io/badge/hooks-8-orange" alt="8 Hooks"></a>
  <a href=".claude/rules"><img src="https://img.shields.io/badge/rules-11-red" alt="11 Rules"></a>
  <a href="https://docs.anthropic.com/en/docs/claude-code"><img src="https://img.shields.io/badge/built%20for-Claude%20Code-f5f5f5?logo=anthropic" alt="Built for Claude Code"></a>
  <a href="https://ko-fi.com/donchitos"><img src="https://img.shields.io/badge/Ko--fi-Support%20this%20project-ff5e5b?logo=ko-fi&logoColor=white" alt="Ko-fi"></a>
</p>

---

## 为什么存在这个项目

用 AI 独立开发游戏很强大——但单一的聊天会话没有结构。没有人会阻止你硬编码魔法数字、跳过设计文档或编写意大利面条式代码。没有 QA 审查，没有设计评审，没有人会问"这真的符合游戏的愿景吗？"

**Claude Code 游戏工作室**通过给你的 AI 会话一个真实工作室的结构来解决这个问题。你不再只有一个通用助手，而是获得 48 个专业智能体组织成工作室层级——守护愿景的总监、掌控各自领域部门的负责人，以及进行实际工作的专家。每个智能体都有明确的职责、升级路径和质量门控。

结果是：你仍然做出每一个决定，但现在你有了一个能提出正确问题、早期发现错误、并使你的项目从第一次头脑风暴到发布都保持有序的团队。

---

## 目录

- [包含内容](#包含内容)
- [工作室层级](#工作室层级)
- [斜杠命令](#斜杠命令)
- [开始使用](#开始使用)
- [升级](#升级)
- [项目结构](#项目结构)
- [工作原理](#工作原理)
- [设计理念](#设计理念)
- [自定义](#自定义)
- [平台支持](#平台支持)
- [社区](#社区)
- [许可证](#许可证)

---

## 包含内容

| 类别 | 数量 | 描述 |
|----------|-------|-------------|
| **智能体** | 48 | 跨设计、编程、美术、音频、叙事、QA 和制作的专业子智能体 |
| **技能** | 37 | 常用工作流程的斜杠命令（`/start`、`/sprint-plan`、`/code-review`、`/brainstorm` 等）|
| **钩子** | 8 | 在提交、推送、资产变更、会话生命周期、智能体审计和差距检测时的自动化验证 |
| **规则** | 11 | 编辑游戏玩法、引擎、AI、UI、网络代码等时强制执行的路径作用域编码标准 |
| **模板** | 29 | 用于 GDD、ADR、冲刺计划、经济模型、派系设计等文档模板 |

## 工作室层级

智能体被组织成三个层级，与真实工作室的运作方式相匹配：

```
第一层 — 总监 (Opus)
  creative-director    technical-director    producer

第二层 — 部门负责人 (Sonnet)
  game-designer        lead-programmer       art-director
  audio-director       narrative-director    qa-lead
  release-manager      localization-lead

第三层 — 专家 (Sonnet/Haiku)
  gameplay-programmer  engine-programmer     ai-programmer
  network-programmer   tools-programmer      ui-programmer
  systems-designer     level-designer        economy-designer
  technical-artist     sound-designer        writer
  world-builder        ux-designer           prototyper
  performance-analyst  devops-engineer       analytics-engineer
  security-engineer    qa-tester             accessibility-specialist
  live-ops-designer    community-manager
```

### 引擎专家

该模板包含所有三大引擎的智能体集。使用与你的项目匹配的集合：

| 引擎 | 主导智能体 | 子专家 |
|--------|-----------|-----------------|
| **Godot 4** | `godot-specialist` | GDScript、Shaders、GDExtension |
| **Unity** | `unity-specialist` | DOTS/ECS、Shaders/VFX、Addressables、UI Toolkit |
| **Unreal Engine 5** | `unreal-specialist` | GAS、Blueprints、Replication、UMG/CommonUI |

## 斜杠命令

在 Claude Code 中输入 `/` 访问所有 37 个技能：

**评审与分析**
`/design-review` `/code-review` `/balance-check` `/asset-audit` `/scope-check` `/perf-profile` `/tech-debt`

**生产**
`/sprint-plan` `/milestone-review` `/estimate` `/retrospective` `/bug-report`

**项目管理**
`/start` `/project-stage-detect` `/reverse-document` `/gate-check` `/map-systems` `/design-system`

**发布**
`/release-checklist` `/launch-checklist` `/changelog` `/patch-notes` `/hotfix`

**创意**
`/brainstorm` `/playtest-report` `/prototype` `/onboard` `/localize`

**团队编排**（协调多个智能体完成单一功能）
`/team-combat` `/team-narrative` `/team-ui` `/team-release` `/team-polish` `/team-audio` `/team-level`

## 开始使用

### 前置要求

- [Git](https://git-scm.com/)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)（`npm install -g @anthropic-ai/claude-code`）
- **推荐**：[jq](https://jqlang.github.io/jq/)（用于钩子验证）和 Python 3（用于 JSON 验证）

所有钩子在可选工具缺失时会优雅地失败——不会破坏任何东西，只是失去验证功能。

### 设置

1. **克隆或用作模板**：
   ```bash
   git clone https://github.com/Donchitos/Claude-Code-Game-Studios.git my-game
   cd my-game
   ```

2. **打开 Claude Code** 并启动会话：
   ```bash
   claude
   ```

3. **运行 `/start`** — 系统会询问你当前的状态（不知道、模糊概念、清晰设计、现有工作）并引导你到正确的工作流程。不做任何假设。

   或者如果你已经知道需要什么，可以直接跳转到特定技能：
   - `/brainstorm` — 从头开始探索游戏创意
   - `/setup-engine godot 4.6` — 如果你已经知道引擎，配置它
   - `/project-stage-detect` — 分析现有项目

## 升级

已经在使用旧版本的这个模板了？参见 [UPGRADING.md](UPGRADING.md) 获取逐步迁移说明、版本间变化的详细说明，以及哪些文件可以安全覆盖 vs. 需要手动合并。

## 项目结构

```
CLAUDE.md                           # 主配置
.claude/
  settings.json                     # 钩子、权限、安全规则
  agents/                           # 48 个智能体定义（markdown + YAML frontmatter）
  skills/                           # 37 个斜杠命令（每个技能一个子目录）
  hooks/                            # 8 个钩子脚本（bash，跨平台）
  rules/                            # 11 个路径作用域编码标准
  docs/
    quick-start.md                  # 详细使用指南
    agent-roster.md                 # 带领域的完整智能体表
    agent-coordination-map.md       # 委托和升级路径
    setup-requirements.md           # 前置要求和平台说明
    templates/                      # 28 个文档模板
src/                                # 游戏源代码
assets/                             # 美术、音频、VFX、着色器、数据文件
design/                             # GDD、叙事文档、关卡设计
docs/                               # 技术文档和 ADR
tests/                              # 测试套件
tools/                              # 构建和管道工具
prototypes/                         # 一次性原型（与 src/ 隔离）
production/                         # 冲刺计划、里程碑、发布跟踪
```

## 工作原理

### 智能体协调

智能体遵循结构化的委托模型：

1. **垂直委托** — 总监委托给负责人，负责人委托给专家
2. **水平咨询** — 同层智能体可以相互咨询，但不能做出跨领域的约束性决策
3. **冲突解决** — 分歧升级到共同的父级（设计的 `creative-director`，技术的 `technical-director`）
4. **变更传播** — 跨部门变更由 `producer` 协调
5. **领域边界** — 智能体不会在未明确委托的情况下修改其领域外的文件

### 协作而非自主

这不是一个自动驾驶系统。每个智能体都遵循严格的协作协议：

1. **提问** — 智能体在提出解决方案之前先提问
2. **展示选项** — 智能体展示 2-4 个带优缺点的选项
3. **你决定** — 用户始终做出选择
4. **草案** — 智能体在定稿前展示工作
5. **批准** — 未经你的签字什么都不会被写入

你保持控制。智能体提供结构和专业知识，而不是自主权。
</p>
