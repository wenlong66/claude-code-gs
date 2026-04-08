<p align="center">
  <h1 align="center">Claude Code 游戏工作室</h1>
  <p align="center">
    将单个 Claude Code 会话变成完整的游戏开发工作室。
    <br />
    49 个智能体。72 个技能。一个协调一致的 AI 团队。
  </p>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT 许可证"></a>
  <a href=".claude/agents"><img src="https://img.shields.io/badge/agents-49-blueviolet" alt="49 个智能体"></a>
  <a href=".claude/skills"><img src="https://img.shields.io/badge/skills-72-green" alt="72 个技能"></a>
  <a href=".claude/hooks"><img src="https://img.shields.io/badge/hooks-12-orange" alt="12 个钩子"></a>
  <a href=".claude/rules"><img src="https://img.shields.io/badge/rules-11-red" alt="11 条规则"></a>
  <a href="https://docs.anthropic.com/en/docs/claude-code"><img src="https://img.shields.io/badge/built%20for-Claude%20Code-f5f5f5?logo=anthropic" alt="为 Claude Code 构建"></a>
  <a href="https://www.buymeacoffee.com/donchitos3"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20this%20project-FFDD00?logo=buymeacoffee&logoColor=black" alt="Buy Me a Coffee"></a>
  <a href="https://github.com/sponsors/Donchitos"><img src="https://img.shields.io/badge/GitHub%20Sponsors-Support%20this%20project-ea4aaa?logo=githubsponsors&logoColor=white" alt="GitHub Sponsors"></a>
</p>

---

## 为什么存在这个项目

用 AI 独立开发游戏很强大，但单个聊天会话缺少结构。没人会阻止你硬编码魔法数字、跳过设计文档，或者写出意大利面式代码。没有 QA 审查，没有设计评审，也没人会问：“这真的符合游戏愿景吗？”

**Claude Code 游戏工作室**通过为你的 AI 会话提供一个真实工作室的结构来解决这个问题。你不再只有一个通用助手，而是拥有 49 个专业智能体，按工作室层级组织——守护愿景的总监、负责各自领域的部门负责人，以及执行具体工作的专家。每个智能体都有明确职责、升级路径和质量关卡。

结果是：你仍然做出每一个决定，但现在你拥有一支会提出正确问题、及早发现错误，并能让项目从第一次头脑风暴一直保持有序直到发布的团队。

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
- [支持本项目](#支持本项目)
- [许可证](#许可证)

---

## 包含内容

| 类别 | 数量 | 描述 |
|------|------|------|
| **智能体** | 49 | 覆盖设计、编程、美术、音频、叙事、QA 和制作的专业子智能体 |
| **技能** | 72 | 覆盖每个工作流阶段的斜杠命令（`/start`、`/design-system`、`/create-epics`、`/create-stories`、`/dev-story`、`/story-done` 等） |
| **钩子** | 12 | 提交、推送、资产变更、会话生命周期、智能体审计轨迹和缺口检测的自动验证 |
| **规则** | 11 | 在编辑玩法、引擎、AI、UI、网络代码等时自动执行的路径作用域编码标准 |
| **模板** | 39 | 用于 GDD、UX 规格、ADR、冲刺计划、HUD 设计、可访问性等的文档模板 |

## 工作室层级

智能体按三个层级组织，对应真实工作室的运作方式：

```
第一层 — 总监（Opus）
  creative-director    technical-director    producer

第二层 — 部门负责人（Sonnet）
  game-designer        lead-programmer       art-director
  audio-director       narrative-director     qa-lead
  release-manager      localization-lead

第三层 — 专家（Sonnet/Haiku）
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

模板包含三大引擎的智能体集合。请选择与你项目匹配的那一组：

| 引擎 | 主导智能体 | 子专家 |
|------|-----------|--------|
| **Godot 4** | `godot-specialist` | GDScript、着色器、GDExtension |
| **Unity** | `unity-specialist` | DOTS/ECS、着色器/VFX、Addressables、UI Toolkit |
| **Unreal Engine 5** | `unreal-specialist` | GAS、蓝图、复制、UMG/CommonUI |

## 斜杠命令

在 Claude Code 中输入 `/` 可访问全部 72 个技能：

**入门与导航**
`/start` `/help` `/project-stage-detect` `/setup-engine` `/adopt`

**游戏设计**
`/brainstorm` `/map-systems` `/design-system` `/quick-design` `/review-all-gdds` `/propagate-design-change`

**美术与资源**
`/art-bible` `/asset-spec` `/asset-audit`

**UX 与界面设计**
`/ux-design` `/ux-review`

**架构**
`/create-architecture` `/architecture-decision` `/architecture-review` `/create-control-manifest`

**故事与冲刺**
`/create-epics` `/create-stories` `/dev-story` `/sprint-plan` `/sprint-status` `/story-readiness` `/story-done` `/estimate`

**评审与分析**
`/design-review` `/code-review` `/balance-check` `/content-audit` `/scope-check` `/perf-profile` `/tech-debt` `/gate-check` `/consistency-check`

**QA 与测试**
`/qa-plan` `/smoke-check` `/soak-test` `/regression-suite` `/test-setup` `/test-helpers` `/test-evidence-review` `/test-flakiness` `/skill-test` `/skill-improve`

**制作**
`/milestone-review` `/retrospective` `/bug-report` `/bug-triage` `/reverse-document` `/playtest-report`

**发布**
`/release-checklist` `/launch-checklist` `/changelog` `/patch-notes` `/hotfix`

**创意与内容**
`/prototype` `/onboard` `/localize`

**团队编排**（协调多个智能体完成单一功能）
`/team-combat` `/team-narrative` `/team-ui` `/team-release` `/team-polish` `/team-audio` `/team-level` `/team-live-ops` `/team-qa`

## 开始使用

### 前置条件

- [Git](https://git-scm.com/)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)（`npm install -g @anthropic-ai/claude-code`）
- **推荐**：[jq](https://jqlang.github.io/jq/)（用于钩子验证）和 Python 3（用于 JSON 验证）

如果可选工具缺失，所有钩子都会优雅失败——不会破坏任何东西，只是少了一层验证。

### 设置

1. **克隆或作为模板使用**：
   ```bash
   git clone https://github.com/Donchitos/Claude-Code-Game-Studios.git my-game
   cd my-game
   ```

2. **打开 Claude Code** 并启动会话：
   ```bash
   claude
   ```

3. **运行 `/start`** —— 系统会询问你当前处于什么状态（完全没概念、模糊概念、清晰设计、已有工程），然后引导你进入正确流程。不会做任何假设。

   如果你已经知道自己要什么，也可以直接跳到特定技能：
   - `/brainstorm` —— 从零开始探索游戏创意
   - `/setup-engine godot 4.6` —— 如果你已经确定引擎，就先配置它
   - `/project-stage-detect` —— 分析现有项目

## 升级

如果你已经在使用旧版本模板，请查看 [UPGRADING.md](UPGRADING.md)，其中包含逐步迁移说明、版本变化说明，以及哪些文件可以安全覆盖、哪些需要手动合并。

## 项目结构

```
CLAUDE.md                           # 主配置
.claude/
  settings.json                     # 钩子、权限、安全规则
  agents/                           # 49 个智能体定义（Markdown + YAML frontmatter）
  skills/                           # 72 个斜杠命令（每个技能一个子目录）
  hooks/                            # 12 个钩子脚本（bash，跨平台）
  rules/                            # 11 条路径作用域编码标准
  statusline.sh                     # 状态行脚本（context%、模型、阶段、epic 面包屑）
  docs/
    workflow-catalog.yaml           # 7 阶段流水线定义（由 /help 读取）
    templates/                      # 39 个文档模板
src/                                # 游戏源代码
assets/                             # 美术、音频、VFX、着色器、数据文件
design/                             # GDD、叙事文档、关卡设计
docs/                               # 技术文档和 ADR
tests/                              # 测试套件（单元、集成、性能、游玩测试）
tools/                              # 构建与管线工具
prototypes/                         # 一次性原型（与 src/ 隔离）
production/                         # 冲刺计划、里程碑、发布跟踪
```

## 工作原理

### 智能体协调

智能体遵循结构化的委托模型：

1. **垂直委托** —— 总监委托给负责人，负责人再委托给专家
2. **横向协商** —— 同层智能体可以相互咨询，但不能做出跨领域的约束性决定
3. **冲突解决** —— 分歧会升级到共同上级（设计问题交给 `creative-director`，技术问题交给 `technical-director`）
4. **变更传播** —— 跨部门变更由 `producer` 协调
5. **领域边界** —— 智能体不会在未明确委托的情况下修改其领域之外的文件

### 协作，而非自动驾驶

这不是一个自动接管系统。每个智能体都遵循严格的协作协议：

1. **提问** —— 智能体在提出方案前先提问
2. **展示选项** —— 智能体给出 2-4 个带优缺点的选项
3. **你决定** —— 由用户做最终选择
4. **草案** —— 智能体在定稿前展示工作内容
5. **批准** —— 未经你的同意，不会写入任何内容

你始终掌握控制权。智能体提供结构和专业能力，而不是自主权。

### 自动化安全

**钩子**会在每次会话中自动运行：

| 钩子 | 触发时机 | 作用 |
|------|---------|------|
| `validate-commit.sh` | PreToolUse (Bash) | 检查硬编码值、TODO 格式、JSON 有效性、设计文档章节——如果命令不是 `git commit` 会立即退出 |
| `validate-push.sh` | PreToolUse (Bash) | 在受保护分支上推送时发出警告——如果命令不是 `git push` 会立即退出 |
| `validate-assets.sh` | PostToolUse (Write/Edit) | 验证命名约定和 JSON 结构——如果文件不在 `assets/` 下会立即退出 |
| `session-start.sh` | 会话打开 | 显示当前分支和最近提交，帮助定位 |
| `detect-gaps.sh` | 会话打开 | 检测新项目（建议 `/start`）以及有原型/代码但缺少设计文档的情况 |
| `pre-compact.sh` | 压缩前 | 保留会话进度笔记 |
| `post-compact.sh` | 压缩后 | 提醒 Claude 从 `active.md` 恢复会话状态 |
| `notify.sh` | 通知事件 | 通过 PowerShell 显示 Windows 弹窗通知 |
| `session-stop.sh` | 会话关闭 | 归档 `active.md` 到会话日志并记录 git 活动 |
| `log-agent.sh` | 智能体启动 | 审计轨迹开始——记录子智能体调用 |
| `log-agent-stop.sh` | 智能体停止 | 审计轨迹结束——完成子智能体记录 |
| `validate-skill-change.sh` | PostToolUse (Write/Edit) | 建议在任何 `.claude/skills/` 变更后运行 `/skill-test` |

> **说明**：`validate-commit.sh`、`validate-assets.sh` 和 `validate-skill-change.sh` 会在每次 Bash/Write 工具调用时触发，并在命令或文件路径无关时立刻退出（exit 0）。这是正常行为，不是性能问题。

**`settings.json` 中的权限规则**会自动允许安全操作（git status、测试运行），并阻止危险操作（强推、`rm -rf`、读取 `.env` 文件）。

### 路径作用域规则

编码标准会根据文件位置自动生效：

| 路径 | 强制执行 |
|------|----------|
| `src/gameplay/**` | 数据驱动数值、使用 delta time、禁止 UI 引用 |
| `src/core/**` | 热路径零分配、线程安全、API 稳定性 |
| `src/ai/**` | 性能预算、可调试性、数据驱动参数 |
| `src/networking/**` | 服务器权威、版本化消息、安全性 |
| `src/ui/**` | 不拥有游戏状态、支持本地化、支持可访问性 |
| `design/gdd/**` | 必需的 8 个章节、公式格式、边缘情况 |
| `tests/**` | 测试命名、覆盖要求、夹具模式 |
| `prototypes/**` | 放宽标准，需 README，并记录假设 |

## 设计理念

这个模板建立在专业游戏开发实践之上：

- **MDA 框架** —— 机制（Mechanics）、动态（Dynamics）、审美（Aesthetics）分析
- **自我决定理论** —— 自主、胜任、联结三种动机
- **心流设计** —— 难度与技能的平衡，维持玩家投入
- **Bartle 玩家类型** —— 面向目标受众并进行验证
- **验证驱动开发** —— 先写测试，再实现

## 自定义

这是一个**模板**，不是锁死的框架。一切都可以自定义：

- **增删智能体** —— 删除不需要的智能体文件，新增适合你项目领域的智能体
- **编辑智能体提示词** —— 调整智能体行为，加入项目专属知识
- **修改技能** —— 让工作流符合团队流程
- **添加规则** —— 创建新的路径作用域规则，匹配你的目录结构
- **调整钩子** —— 修改验证严格度，增加新检查
- **选择引擎** —— 使用 Godot、Unity 或 Unreal 的智能体集合（也可以不用）
- **设置评审强度** —— `full`（所有总监关卡）、`lean`（仅阶段关卡）、`solo`（关闭）. 可在 `/start` 时设置，或编辑 `production/review-mode.txt`。也可在任意技能上用 `--review solo` 覆盖一次。

## 平台支持

已在 **Windows 10** 的 Git Bash 上测试。所有钩子都使用 POSIX 兼容模式（`grep -E`，不是 `grep -P`），并为缺失工具提供回退。无需修改即可在 macOS 和 Linux 上运行。

## 社区

- **讨论** —— [GitHub Discussions](https://github.com/Donchitos/Claude-Code-Game-Studios/discussions)，用于提问、交流想法以及展示你的作品
- **Issues** —— [Bug 报告与功能请求](https://github.com/Donchitos/Claude-Code-Game-Studios/issues)

---

## 支持本项目

Claude Code 游戏工作室是免费开源的。如果它帮你节省了时间，或帮助你把游戏做出来，可以考虑支持后续开发：

<p>
  <a href="https://www.buymeacoffee.com/donchitos3"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"></a>
  &nbsp;
  <a href="https://github.com/sponsors/Donchitos"><img src="https://img.shields.io/badge/GitHub%20Sponsors-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white" alt="GitHub Sponsors"></a>
</p>

- **[Buy Me a Coffee](https://www.buymeacoffee.com/donchitos3)** —— 一次性支持
- **[GitHub Sponsors](https://github.com/sponsors/Donchitos)** —— 通过 GitHub 持续支持

赞助有助于资助维护技能、添加新智能体、跟进 Claude Code 和引擎 API 变化，以及响应社区问题的时间。

---

*为 Claude Code 而构建。持续维护与扩展——欢迎通过 [GitHub Discussions](https://github.com/Donchitos/Claude-Code-Game-Studios/discussions) 贡献。*

## 许可证

MIT 许可证，详见 [LICENSE](LICENSE)。
