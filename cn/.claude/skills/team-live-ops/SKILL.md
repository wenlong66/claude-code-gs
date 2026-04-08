---
name: team-live-ops
description: "编排上线后内容规划的 live-ops 团队：协调 live-ops-designer、economy-designer、analytics-engineer、community-manager、writer 和 narrative-director 来设计和规划赛季、活动或 live 内容更新。"
argument-hint: "[season name or event description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---
**参数检查：** 如果没有提供赛季名称或活动描述，则输出：
> "Usage: `/team-live-ops [season name or event description]` — Provide the name or description of the season or live event to plan."
然后立即停止，不要 spawn 任何 subagent，也不要读取任何文件。

当该技能带着有效参数被调用时，按结构化规划流程编排 live-ops 团队。

**决策点：** 在每个阶段切换时，使用 `AskUserQuestion` 呈现 subagent 的提案作为可选项。先在对话中写出 agent 的完整分析，再用简洁标签记录用户决策。
用户必须批准后才能进入下一阶段。

## 团队构成
- **live-ops-designer** — 赛季结构、活动节奏、留存机制、battle pass
- **economy-designer** — Live economy 平衡、商店轮换、货币定价、保底计时器
- **analytics-engineer** — 成功指标、A/B 测试设计、活动追踪、仪表盘规格
- **community-manager** — 面向玩家的公告、活动描述、赛季信息传达
- **narrative-director** — 赛季叙事主题、故事弧线、世界事件包装
- **writer** — 活动描述、奖励物品名称、赛季文案、公告文案

## 如何委派

使用 Task 工具为每个团队成员 spawn 一个 subagent：
- `subagent_type: live-ops-designer` — 赛季/活动结构与留存机制
- `subagent_type: economy-designer` — Live economy 平衡与奖励定价
- `subagent_type: analytics-engineer` — 成功指标、A/B 测试、活动埋点
- `subagent_type: community-manager` — 面向玩家的沟通与信息传达
- `subagent_type: narrative-director` — 赛季主题与叙事包装
- `subagent_type: writer` — 所有面向玩家的文本：活动描述、物品名、文案

始终在每个 agent 的提示中提供完整上下文（游戏概念路径、现有赛季文档、伦理政策路径、当前经济状态）。在流程允许时并行启动独立 agent（第 3 和第 4 阶段可以同时运行）。

## 流程

### 第 1 阶段：赛季/活动范围界定
委派给 **live-ops-designer**：
- 定义赛季或活动：类型（赛季型、限时活动、挑战）、持续时间、主题方向
- 概述内容列表：新增内容（模式、物品、挑战、故事节点）
- 定义留存钩子：赛季期间让玩家每天/每周回来的原因
- 识别资源预算：需要创建多少新内容，多少可以复用
- 输出：赛季简报，包含范围、内容列表和留存机制概览

### 第 2 阶段：叙事主题
委派给 **narrative-director**：
- 读取第 1 阶段的赛季简报
- 设计赛季叙事主题：这个活动如何与游戏世界连接？
- 定义玩家在活动中会发现的核心故事钩子
- 识别本赛季可以推进哪些现有 lore 线索
- 输出：叙事包装文档（主题、故事钩子、lore 关联）

### 第 3 阶段：经济设计（如果主题清晰，可与第 2 阶段并行）
委派给 **economy-designer**：
- 读取赛季简报和 `design/live-ops/economy-rules.md` 中的现有经济规则
- 设计奖励轨道：免费层进度、付费层价值主张
- 规划赛季内 economy：赛季货币、商店轮换、定价
- 为任何随机元素定义保底计时器和坏运保护机制
- 验证高级奖励轨道中没有 pay-to-win 物品
- 输出：经济设计文档，包含奖励表、定价与货币流转

### 第 4 阶段：分析与成功指标（与第 3 阶段并行）
委派给 **analytics-engineer**：
- 读取赛季简报
- 定义成功指标：参与率目标、留存提升目标、battle pass 完成率
- 设计赛季期间要运行的 A/B 测试（例如不同奖励节奏）
- 指定本赛季内容所需的新 telemetry events
- 输出：包含成功标准和埋点需求的分析计划

### 第 5 阶段：内容撰写（并行）
并行委派：
- **narrative-director**（如有需要）：撰写本赛季的游戏内叙事文本（过场脚本、NPC 对白、世界事件描述）
- **writer**：撰写所有面向玩家的文本——活动名称、奖励物品描述、挑战目标文本、赛季风味文案
- 两者都应阅读第 2 阶段的叙事包装文档

### 第 6 阶段：玩家沟通计划
委派给 **community-manager**：
- 阅读赛季简报、经济设计和叙事包装
- 起草赛季发布公告（语气、重点、平台特定版本）
- 规划沟通节奏：预热公告、上线日帖子、中期提醒、最后一周 FOMO 推送
- 起草 day-1 patch notes 的已知问题占位段落
- 输出：包含各触点草案文案的沟通日历

### 第 7 阶段：审阅与签收
汇总所有阶段的输出，呈现一份统一的赛季计划：
- 赛季简报（第 1 阶段）
- 叙事包装（第 2 阶段）
- 经济设计与奖励表（第 3 阶段）
- 分析计划与成功指标（第 4 阶段）
- 已撰写内容清单（第 5 阶段）
- 沟通日历（第 6 阶段）

向用户呈现摘要，包括：
- **内容范围**：将创建什么
- **经济健康检查**：奖励轨道是否公平且不具剥削性？
- **分析就绪度**：成功标准是否已定义并埋点？
- **伦理审查**：将第 3 阶段的经济设计与 `design/live-ops/ethics-policy.md` 对照
  - 如果该文件不存在：标记 "ETHICS REVIEW SKIPPED: `design/live-ops/ethics-policy.md` not found. Economy design was not reviewed against an ethics policy. Recommend creating one before production begins." 将此标记包含在赛季设计输出文档中。并在下一步中添加：创建 `design/live-ops/ethics-policy.md`。
  - 如果该文件存在且发现违反：标记 "ETHICS FLAG: [element] in Phase 3 economy design violates [policy rule]. Approval is blocked until this is resolved." 不要发出 COMPLETE verdict，也不要写输出文档。使用 `AskUserQuestion`，选项：修改经济设计 / 使用记录在案的理由覆盖 / 取消。如果用户选择修改：重新 spawn economy-designer 产出修正版，然后回到第 7 阶段审查。
- **未决问题**：在生产开始前仍需做出的决定

在委派给生产团队之前，请用户批准赛季计划。只有用户批准且不存在未解决的伦理违规时，才发出 COMPLETE verdict。如果伦理违规尚未解决，则以 Verdict: **BLOCKED** 结束。

## 输出文档

所有文档保存到 `design/live-ops/`：
- `seasons/S[N]_[name].md` — 赛季设计文档（来自第 1-3 阶段）
- `seasons/S[N]_[name]_analytics.md` — 分析计划（来自第 4 阶段）
- `seasons/S[N]_[name]_comms.md` — 沟通日历（来自第 6 阶段）

## 错误恢复协议

如果任何通过 Task spawn 的 agent 返回 BLOCKED、出错或无法完成：

1. **立即呈现**：在继续后续阶段之前，向用户报告 "[AgentName]: BLOCKED — [reason]"
2. **评估依赖**：检查被阻塞 agent 的输出是否是后续阶段所必需。如果是，则在没有用户输入前不要继续到该依赖点之后。
3. **提供选项** 通过 AskUserQuestion：
   - 跳过该 agent，并在最终报告中注明缺口
   - 用更窄的范围重试
   - 先停止并解决该阻塞
4. **始终产出部分报告** —— 输出已完成的内容。绝不要因为一个 agent 阻塞就丢弃工作。

如果 BLOCKED 状态无法解决，则以 Verdict: **BLOCKED** 结束，而不是 COMPLETE。

## 文件写入协议

所有文件写入（赛季设计文档、分析计划、沟通日历）都通过 Task 委派给 subagent。每个 subagent 都会执行“May I write to [path]?” 协议。这个编排器不会直接写文件。

## 输出

总结应覆盖：赛季主题与范围、经济设计要点、成功指标、内容列表、沟通计划，以及在生产前需要用户输入的任何未决决定。

Verdict: **COMPLETE** — 赛季计划已产出并交接给生产。

## 下一步

- 在赛季设计文档上运行 `/design-review` 以验证一致性。
- 运行 `/sprint-plan` 来安排该赛季的内容制作工作。
- 当赛季内容准备好部署时，运行 `/team-release`。