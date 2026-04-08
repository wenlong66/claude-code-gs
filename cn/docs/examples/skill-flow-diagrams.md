# 技能流程图

这些图展示了 7 个开发阶段中，技能是如何串联的。它们说明每个技能前后会运行什么，以及工件如何在流程中流转。

---

## 完整流水线概览（从零到发布）

```text
阶段 1：概念
  /start ──────────────────────────────────────────────────────► 路由到 A/B/C/D
  /brainstorm ────────────────────────────────────────────────► design/gdd/game-concept.md
  /setup-engine ───────────────────────────────────────────────► CLAUDE.md + technical-preferences.md
  /design-review [game-concept.md] ────────────────────────────► 概念已验证
  /gate-check ────────────────────────────────────────────────► PASS → 进入 systems-design
        │
        ▼
阶段 2：系统设计
  /map-systems ────────────────────────────────────────────────► design/gdd/systems-index.md
        │
        ▼（按依赖顺序，对每个系统执行）
  /design-system [名称] ───────────────────────────────────────► design/gdd/[system].md
  /design-review [system].md ──────────────────────────────────► 单个 GDD 审查意见
        │
        ▼（所有 MVP GDD 完成后）
  /review-all-gdds ────────────────────────────────────────────► design/gdd/gdd-cross-review-[date].md
  /gate-check ────────────────────────────────────────────────► PASS → 进入 technical-setup
        │
        ▼
阶段 3：技术准备
  /create-architecture ────────────────────────────────────────► docs/architecture/master.md
  /architecture-decision (×N) ─────────────────────────────────► docs/architecture/[adr-nnn].md
  /architecture-review ────────────────────────────────────────► 审查报告 + docs/architecture/tr-registry.yaml
  /create-control-manifest ────────────────────────────────────► docs/architecture/control-manifest.md
  /gate-check ────────────────────────────────────────────────► PASS → 进入 pre-production
        │
        ▼
阶段 4：预生产
  [UX —— 先于 epics 编写，确保写故事时规格已存在]
  /ux-design [screen/hud/patterns] ────────────────────────────► design/ux/*.md
  /ux-review ──────────────────────────────────────────────────► UX 规格已批准（/team-ui 的硬门禁）

  [测试基础设施 —— 在故事引用测试之前先搭架子]
  /test-setup ─────────────────────────────────────────────────► 测试框架 + CI/CD 流水线
  /test-helpers ───────────────────────────────────────────────► tests/helpers/[engine-specific].gd

  [故事 + 原型]
  /create-epics [layer] ───────────────────────────────────────► production/epics/*/EPIC.md
  /create-stories [epic-slug] ─────────────────────────────────► production/epics/*/story-*.md
  /prototype [core-mechanic] ──────────────────────────────────► prototypes/[name]/
  /playtest-report ────────────────────────────────────────────► tests/playtest/vertical-slice.md
  /sprint-plan new ────────────────────────────────────────────► production/sprints/sprint-01.md
  /gate-check ────────────────────────────────────────────────► PASS → 进入 production
        │
        ▼
阶段 5：生产（重复的冲刺循环）
  /sprint-status ──────────────────────────────────────────────► 冲刺快照
  /story-readiness [story] ────────────────────────────────────► story 验证为 READY
        │
        ▼（接手并实现）
  /dev-story [story] ──────────────────────────────────────────► 路由到正确的程序员智能体
        │
        ▼（实现期间按需使用）
  /code-review ────────────────────────────────────────────────► 代码审查报告
  /scope-check ────────────────────────────────────────────────► 范围膨胀检测 / 清理
  /content-audit ──────────────────────────────────────────────► GDD 内容缺口识别
  /bug-report ─────────────────────────────────────────────────► production/qa/bugs/bug-NNN.md
  /bug-triage ─────────────────────────────────────────────────► 缺陷重新排序 + 分派

  [用于完整功能的团队技能 —— 需要时启动]
  /team-combat / /team-narrative / /team-ui / /team-level / /team-audio

  [每个冲刺的 QA 流程]
  /qa-plan ────────────────────────────────────────────────────► production/qa/qa-plan-sprint-NN.md
  /smoke-check ────────────────────────────────────────────────► 冒烟测试门禁（PASS/FAIL）
  /regression-suite ───────────────────────────────────────────► 覆盖缺口 + 缺少回归测试的项目
  /test-evidence-review ───────────────────────────────────────► 证据质量报告
  /test-flakiness ─────────────────────────────────────────────► 不稳定测试报告
        │
        ▼
  /story-done [story] ─────────────────────────────────────────► 故事关闭 + 下一个故事浮现
  /sprint-plan [next] ─────────────────────────────────────────► 下一轮冲刺
        │
        ▼（Production 里程碑后）
  /milestone-review ───────────────────────────────────────────► 里程碑报告
  /gate-check ─────────────────────────────────────────────────► PASS → 进入 polish
        │
        ▼
阶段 6：打磨
  /perf-profile ───────────────────────────────────────────────► 性能报告 + 修复
  /balance-check ──────────────────────────────────────────────► 平衡报告 + 修复
  /asset-audit ────────────────────────────────────────────────► 资源合规报告
  /tech-debt ──────────────────────────────────────────────────► docs/tech-debt-register.md
  /soak-test ──────────────────────────────────────────────────► 浸泡测试流程 + 结果
  /localize ───────────────────────────────────────────────────► 本地化准备度报告
  /team-polish ────────────────────────────────────────────────► 协同打磨冲刺
  /team-qa ────────────────────────────────────────────────────► 完整 QA 流程签字
  /gate-check ─────────────────────────────────────────────────► PASS → 进入 release
        │
        ▼
阶段 7：发布
  /launch-checklist ───────────────────────────────────────────► 上线准备报告
  /release-checklist ──────────────────────────────────────────► 平台特定检查清单
  /changelog ──────────────────────────────────────────────────► CHANGELOG.md
  /patch-notes ────────────────────────────────────────────────► 面向玩家的说明
  /team-release ───────────────────────────────────────────────► 发布流水线编排
        │
        ▼（上线后，持续进行）
  /hotfix ─────────────────────────────────────────────────────► 带审计轨迹的紧急修复
  /team-live-ops ──────────────────────────────────────────────► Live Ops 内容计划
```

---

## 技能链：/design-system 细节

一个 GDD 是如何被编写、审查并交给架构阶段的：

```text
systems-index.md（输入）
game-concept.md（输入）
上游 GDD（输入，如果有）
        │
        ▼
/design-system [名称]
        │
        ├── 预检：可行性表 + 引擎风险标记
        │
        ├── 章节循环 × 8：
        │     问题 → 选项 → 决策 → 草案 → 批准 → 写入
        │     [每节在批准后立即写盘]
        │
        └── 输出：design/gdd/[system].md（完整，含全部 8 部分）
                │
                ▼
        /design-review design/gdd/[system].md
                │
                ├── APPROVED → 在 systems-index 中标记完成，继续下一个系统
                ├── NEEDS REVISION → 智能体展示具体问题，回到章节循环
                └── MAJOR REVISION → 在下一个系统前需要重大重做
                        │
                        ▼（所有 MVP GDD + 跨审查完成后）
                /review-all-gdds
                        │
                        └── 输出：gdd-cross-review-[date].md
```

---

## 技能链：UX / UI 流程细节

UX 规格在阶段 4（预生产）编写，且要早于 epic，以便故事验收标准可以引用具体 UX 工件。

```text
design/gdd/*.md（提取出的 UI/UX 要求）
design/player-journey.md（情绪弧，如果有）
        │
        ▼
/ux-design hud              → design/ux/hud.md
/ux-design screen [name]    → design/ux/screens/[name].md
/ux-design patterns         → design/ux/interaction-patterns.md
        │
        ▼
/ux-review design/ux/
        │
        ├── APPROVED → UX 规格可用，进入 /create-epics
        ├── NEEDS REVISION → 列出阻塞项 → 修复 → 重新审查
        └── MAJOR REVISION → 根本性的 UX 问题 → 在写 epic 前先重做
                │
                ▼（APPROVED 后 —— 在阶段 5 实现 UI 功能时）
        /team-ui
                │
                ├── 阶段 1：/ux-design（如果仍有缺失规格）+ /ux-review
                ├── 阶段 2：视觉设计（art-director）
                ├── 阶段 3：布局实现（ui-programmer）
                ├── 阶段 4：可访问性审计（accessibility-specialist）
                └── 阶段 5：最终审查

注意：/ux-design 和 /ux-review 属于阶段 4（预生产）。
      /team-ui 属于阶段 5（生产），用于构建某个 UI 功能。
```

---

## 技能链：开发故事流程细节

一个故事如何从待办进入关闭：

```text
/story-readiness [story]
        │
        ├── READY → Status: ready-for-dev → 可接手实现
        ├── NEEDS WORK → 智能体指出具体缺口 → 修复 → 重新检查
        └── BLOCKED → ADR 仍为 Proposed，或上游故事未完成
                │
                ▼（READY 后）
        /dev-story [story]
                │
                ├── 读取：故事文件、关联的 GDD 需求、ADR 决策、控制清单
                ├── 路由到：gameplay-programmer / engine-programmer / ui-programmer / 等
                │
                └── 开始实现
                        │
                        ▼（实现期间/之后按需）
                /code-review          → 变更集的架构审查
                /scope-check          → 验证是否相对原故事标准发生范围膨胀
                /test-evidence-review → 验证测试文件和人工证据质量
                        │
                        ▼
                /story-done [story]
                        │
                        ├── COMPLETE → Status: Complete，更新 sprint-status.yaml，并浮现下一个故事
                        ├── COMPLETE WITH NOTES → 已完成，但部分标准延期（记录下来）
                        └── BLOCKED → 验收标准无法验证 → 先调查阻塞项
```

---

## 技能链：故事生命周期（从待办到关闭）

故事如何从待办进入关闭（摘要视图）：

```text
/create-epics [layer]
        │
        └── 输出：production/epics/[slug]/EPIC.md
                │
                ▼
        /create-stories [epic-slug]
                │
                └── 输出：production/epics/[slug]/story-NNN-[slug].md
                            （Status: Ready；如果 ADR 是 Proposed 则为 Blocked）
                │
                ▼
        /story-readiness [story]
                │
                ├── READY → /dev-story → implement → /story-done
                ├── NEEDS WORK → 解决缺口 → 重新运行
                └── BLOCKED → 先修上游依赖
```

---

## 技能链：QA 流程细节

```text
[阶段 4 —— 一次性基础设施搭建]
/test-setup ────────────────────────────────────────────────────► 测试框架已搭建 + CI/CD 已连接
/test-helpers ──────────────────────────────────────────────────► tests/helpers/[engine].gd（GDUnit4、NUnit 等）

[阶段 5 —— 每个冲刺的 QA 循环]
/qa-plan [sprint 或 feature]
        │
        ├── 读取：故事文件、GDD、验收标准
        ├── 按测试类型分类每个故事：
        │     Logic → 自动化单元测试（BLOCKING）
        │     Integration → 集成测试或文档化游玩测试（BLOCKING）
        │     Visual/Feel → 截图 + lead 签字（ADVISORY）
        │     UI → 手工 walkthrough 或交互测试（ADVISORY）
        │     Config/Data → 冒烟检查（ADVISORY）
        └── 输出：production/qa/qa-plan-sprint-NN.md
                │
                ▼
        /smoke-check
                │
                ├── PASS → QA 交接完成
                └── FAIL → 阻止冲刺关闭 → 先修关键路径
                        │
                        ▼
                /regression-suite
                        │
                        └── 覆盖缺口 + 缺少回归测试的已修复 bug 列表
                                │
                                ▼
                        /test-evidence-review
                                │
                                └── 验证证据质量，而不只是是否存在
                                        │
                                        ▼（如果有 CI 运行历史）
                        /test-flakiness
                                │
                                └── 不稳定测试报告 + 修复建议

[阶段 6 —— 扩展稳定性测试]
/soak-test ─────────────────────────────────────────────────────► 浸泡测试流程 + 观察结果
/team-qa ───────────────────────────────────────────────────────► 发布门禁的完整 QA 签字

[持续进行 —— 缺陷管理]
/bug-report ────────────────────────────────────────────────────► production/qa/bugs/bug-NNN.md
/bug-triage ────────────────────────────────────────────────────► 开放缺陷重新排序 + 分派

[元能力 —— harness 验证]
/skill-test [lint|spec|catalog] ────────────────────────────────► 技能文件结构 + 行为检查
```

---

## 技能链：UX 流程细节（历史参考）

```text
design/gdd/*.md（提取出的 UX 要求）
design/player-journey.md（情绪弧）
        │
        ▼
/ux-design hud              → design/ux/hud.md
/ux-design screen [name]    → design/ux/screens/[name].md
/ux-design patterns         → design/ux/interaction-patterns.md
        │
        ▼
/ux-review design/ux/
        │
        ├── APPROVED → 所有规格可供 /team-ui 使用
        ├── NEEDS REVISION → 列出阻塞项 → 修复 → 重新审查
        └── MAJOR REVISION → 根本性 UX 问题 → 大幅重做
                │
                ▼（APPROVED 后）
        /team-ui
                │
                ├── 阶段 1：上下文加载 + /ux-design（如果规格缺失）
                ├── 阶段 2：视觉设计（art-director）
                ├── 阶段 3：布局实现（ui-programmer）
                ├── 阶段 4：可访问性审计（accessibility-specialist）
                └── 阶段 5：最终审查
```

---

## 棕地入门流程

针对已有工作的项目（使用 `/start` 的 D 选项，或直接运行）：

```text
/project-stage-detect    → 阶段检测报告
        │
        ▼
/adopt
        │
        ├── 阶段 1：检测已存在内容
        ├── 阶段 2：FORMAT 审计（不是只看是否存在）
        ├── 阶段 3：分类缺口（BLOCKING / HIGH / MEDIUM / LOW）
        ├── 阶段 4：有顺序的迁移计划
        ├── 阶段 5：写入 docs/adoption-plan-[date].md
        └── 阶段 6：在内联中修复最紧急的缺口（可选）
                │
                ▼
        /design-system retrofit [path]      → 补齐缺失的 GDD 部分
        /architecture-decision retrofit [path] → 补齐缺失的 ADR 部分
        /gate-check                         → 检查你当前处于流水线的哪一段
```

---

## 如何阅读这些图

| 符号 | 含义 |
|------|------|
| `──►` | 产出这个工件 |
| `│ ▼` | 流向下一步 |
| `├──` | 分支（多个可能结果） |
| `×N` | 运行 N 次（每个系统、故事等一次） |
| `(input)` | 由技能读取，但不是这里产出 |
| `[optional]` | 不是门禁通过所必需 |
| `WRITE`（全大写） | 立即写入磁盘的文件 |

---

## 常见入口点

| 你现在在哪 | 运行这个 |
|-----------|---------|
| 刚开始，还没有点子 | `/start` → `/brainstorm` |
| 有概念，但没选引擎 | `/setup-engine` |
| 有概念和引擎 | `/map-systems` |
| 系统设计进行中 | `/design-system [下一个系统]` 或 `/map-systems next` |
| 所有 GDD 都完成了 | `/review-all-gdds` → `/gate-check` |
| 正在技术准备 | `/create-architecture` → `/architecture-decision` |
| 正在开始 UX 设计 | `/ux-design screen [name]` 或 `/ux-design hud` |
| 正在搭建测试框架 | `/test-setup` → `/test-helpers` |
| 有故事，准备写代码 | `/story-readiness [story]` → `/dev-story [story]` |
| 故事已完成 | `/story-done [story]` |
| 正在为冲刺做 QA | `/qa-plan` → `/smoke-check` → `/regression-suite` |
| 缺陷待排序 | `/bug-triage` |
| 需要长期稳定性测试 | `/soak-test` |
| 不知道下一步 | `/help` |
| 现有项目 | `/adopt` |
```