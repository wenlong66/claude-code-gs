---
name: help
description: "分析当前已完成的内容和用户的问题，并给出下一步建议。适用于用户说‘我接下来该做什么’、‘我现在该做什么’、‘我卡住了’或‘我不知道该做什么’时"
argument-hint: "[可选：你刚完成的内容，例如 'finished design-review' 或 'stuck on ADRs']"
user-invocable: true
allowed-tools: Read, Glob, Grep
context: |
  !echo "=== Live Project State ===" && echo "Stage: $(cat production/stage.txt 2>/dev/null | tr -d '[:space:]' || echo 'not set')" && echo "Latest sprint: $(ls -t production/sprints/*.md 2>/dev/null | head -1 || echo 'none')" && echo "Session state: $(head -5 production/session-state/active.md 2>/dev/null || echo 'none')"
model: haiku
---

# 工作室帮助 — 下一步做什么？

这个技能是只读的——它会报告结果，但不会写入任何文件。

它会准确判断你当前处于游戏开发流程的哪个位置，并告诉你下一步该做什么。它是**轻量级**的——不是完整审计。若需要完整缺口分析，请使用 `/project-stage-detect`。

---

## 第 1 步：读取目录

读取 `.claude/docs/workflow-catalog.yaml`。这是所有阶段的权威清单，定义了各步骤的顺序、每一步是必需还是可选，以及表示完成状态的 artifact glob。

---

## 第 1b 步：找出未收录的技能

读取目录后，再 Glob `.claude/skills/*/SKILL.md`，获取已安装技能的完整列表。
对每个文件，提取 frontmatter 中的 `name:` 字段。

将其与目录中的 `command:` 值进行对比。任何技能名称不出现在目录命令中的，都是**未收录技能**——它们仍然可用，但不属于阶段门控流程。

把这些内容收集到第 7 步的输出中——以页脚块形式展示：

```
### Also installed (not in workflow)
- `/skill-name` — [description from SKILL.md frontmatter]
- `/skill-name` — [description]
```

只有当至少存在一个未收录技能时才显示此块。根据用户当前阶段只保留最相关的 10 个：例如，生产期显示 QA 技能，生产/润色期显示团队技能等。

---

## 第 2 步：确定当前阶段

按以下顺序检查：

1. **读取 `production/stage.txt`**——如果存在且有内容，这就是权威阶段名称。将其映射到目录中的 phase key：
   - "Concept" → `concept`
   - "Systems Design" → `systems-design`
   - "Technical Setup" → `technical-setup`
   - "Pre-Production" → `pre-production`
   - "Production" → `production`
   - "Polish" → `polish`
   - "Release" → `release`

2. **如果 `stage.txt` 缺失**，根据产物推断阶段（以最先进的匹配为准）：
   - `src/` 中有 10+ 个源码文件 → `production`
   - 存在 `production/stories/*.md` → `pre-production`
   - 存在 `docs/architecture/adr-*.md` → `technical-setup`
   - 存在 `design/gdd/systems-index.md` → `systems-design`
   - 存在 `design/gdd/game-concept.md` → `concept`
   - 都没有 → `concept`（新项目）

---

## 第 3 步：读取会话上下文

读取 `production/session-state/active.md`（如果存在）。提取：
- 最近在做什么
- 任何进行中的任务或未决问题
- STATUS block 中的当前 epic/feature/task（如果有）

这能告诉你用户刚完成了什么，或者卡在哪里——用它来让输出更贴近当前情境。

---

## 第 4 步：检查当前阶段的步骤完成情况

对于当前阶段中的每一步（根据目录）：

### 基于 artifact 的检查

如果某一步有 `artifact.glob`：
- 用 Glob 检查是否存在匹配文件
- 如果指定了 `min_count`，确认至少匹配到那么多文件
- 如果指定了 `artifact.pattern`，用 Grep 验证匹配文件中是否存在该模式
- **Complete** = 满足 artifact 条件
- **Incomplete** = 缺少 artifact 或未找到 pattern

如果某一步有 `artifact.note`（没有 glob）：
- 标记为 **MANUAL**——无法自动检测，需要询问用户

如果某一步没有 `artifact` 字段：
- 标记为 **UNKNOWN**——完成情况不可跟踪（例如可重复执行的实现工作）

### 特殊情况：production 阶段——读取 `sprint-status.yaml`

当当前阶段是 `production` 时，在做任何基于 glob 的 story 检查前，先检查 `production/sprint-status.yaml`。如果存在，直接读取：

- `status: in-progress` 的故事 → 标记为“当前进行中”
- `status: ready-for-dev` 的故事 → 标记为“下一项”
- `status: done` 的故事 → 计为完成
- `status: blocked` 的故事 → 使用 `blocker` 字段标记阻塞原因

这样可以不依赖 markdown 扫描，直接获得精确的逐 story 状态。对于 `implement` 和 `story-done` 步骤，跳过 glob artifact 检查——YAML 是权威来源。

### 特殊情况：`repeatable: true`（非 production）

对于 production 之外的可重复步骤（例如“System GDDs”），artifact 检查只能说明**已有工作**，不能说明已经完成。
请区别展示——先显示检测到的内容，再说明它可能仍在进行中。

---

## 第 5 步：找出当前位置并识别下一步

根据完成数据，确定：

1. **最后确认完成的步骤**——最远的已完成必需步骤
2. **当前阻塞点**——第一个未完成的*必需*步骤（这就是用户下一步必须做的）
3. **可选机会**——可在阻塞点之前或同时完成的未完成*可选*步骤
4. **后续必需步骤**——当前阻塞点之后的必需步骤（以“coming up”方式展示，方便提前规划）

如果用户提供了参数（例如“刚完成 design-review”），即使 artifact 检查结果有歧义，也要用它来跳过用户提到的那一步。

---

## 第 6 步：检查进行中的工作

如果 `active.md` 显示有活跃任务或 epic：
- 在顶部突出显示：“看起来你正在做 [X]”
- 建议继续它，或者确认是否已经完成

---

## 第 7 步：展示输出

保持**简短直接**。这是快速导览，不是报告。

```
## 你现在在哪里：[阶段标签]

**进行中：** [来自 active.md，如果有]

### ✓ 已完成
- [已完成步骤名称]
- [已完成步骤名称]

### → 下一步（必需）
**[步骤名称]** — [描述]
Command: `[/command]`

### ~ 还可做（可选）
- **[步骤名称]** — [描述] → `/command`
- **[步骤名称]** — [描述] → `/command`

### 接下来还有
- [下一个必需步骤名称] (`/command`)
- [下一个必需步骤名称] (`/command`)

---
接近 **[下一个阶段]** gate → 准备好后运行 `/gate-check`。
```

**格式规则：**
- `✓` 表示已确认完成
- `→` 表示当前必需的下一步（只能有一个——第一个阻塞点）
- `~` 表示当前可选步骤
- 命令以内联反引号代码显示
- 如果某一步没有命令（例如“Implement Stories”），不要显示斜杠命令，而是解释应该做什么
- 对于 MANUAL 步骤，询问用户：“我无法判断 [步骤] 是否完成——它已经完成了吗？”

Verdict: **COMPLETE** — 已识别下一步。

---

## 第 8 步：门控提醒（如果接近）

在当前阶段步骤之后，检查用户是否可能接近门控：
- 如果当前阶段所有必需步骤都已完成（或几乎完成），就追加：
  "你已经接近 **[当前] → [下一]** gate。准备好后运行 `/gate-check`。"
- 如果还剩多个必需步骤，就不要显示门控提醒——还不相关。

---

## 第 9 步：升级路径

在给出推荐后，如果用户看起来卡住或困惑，再补充：

```
---
需要更多细节吗？
- `/project-stage-detect` — 全量缺口分析，列出所有缺失 artifact
- `/gate-check` — 针对下一阶段的正式就绪检查
- `/start` — 从头重新对齐
```

只有在用户输入暗示困惑时才显示（例如 “I don't know”, “stuck”, “lost”, “not sure”）。如果只是简单的“下一步是什么？”，不要显示这部分。

---

## 协作协议

- **不要自动运行下一个技能。** 只推荐，让用户自己调用。
- **对 MANUAL 步骤要提问**，不要假定完成或未完成。
- **匹配用户语气**——如果他们显得很焦虑（“我完全迷失了”），就给出安抚和一个行动，而不是六条列表。
- **只给一个首要建议**——用户离开时应该明确知道下一步只做一件事。可选步骤和“接下来还有”只是补充背景。
