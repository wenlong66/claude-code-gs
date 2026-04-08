---
name: sprint-status
description: "快速冲刺状态检查。读取当前冲刺计划，扫描故事文件中的状态，并输出简洁的进度快照、燃尽评估和新出现的风险。可在冲刺期间随时运行，以快速把握局势。用于用户询问‘冲刺进展如何’、‘冲刺更新’、‘显示冲刺进度’时。"
argument-hint: "[sprint-number or blank for current]"
user-invocable: true
allowed-tools: Read, Glob, Grep
model: haiku
---

# 冲刺状态

这是一次快速的态势感知检查，不是冲刺评审。它会读取当前冲刺计划和故事文件，扫描状态标记，并在 30 行以内给出简洁快照。若需更详细的冲刺管理，请使用 `/sprint-plan update` 或 `/milestone-review`。

**此技能为只读。** 它不会提出修改，不会要求写文件，并且最多只给出一条具体建议。

---

## 1. 查找冲刺

**参数：** `$ARGUMENTS[0]`（空白 = 使用当前冲刺）

- 如果提供了参数（例如 `/sprint-status 3`），就在 `production/sprints/` 中搜索匹配 `sprint-03.md`、`sprint-3.md` 或类似名称的文件。报告找到了哪个文件。
- 如果未提供参数，找到 `production/sprints/` 中最近修改的文件，并将其视为当前冲刺。
- 如果 `production/sprints/` 不存在或为空，报告："未找到任何冲刺文件。请使用 `/sprint-plan new` 开始一个冲刺。" 然后停止。

完整读取冲刺文件。提取：
- 冲刺编号与目标
- 开始日期与结束日期
- 所有故事或任务条目及其优先级（Must Have / Should Have / Nice to Have）、负责人和估算

---

## 2. 计算剩余天数

使用今天的日期和冲刺文件中的结束日期，计算：
- 冲刺总天数（结束日期减开始日期）
- 已经过天数
- 剩余天数
- 已消耗时间百分比

如果冲刺文件没有显式日期，请注明："未找到冲刺日期 — 跳过燃尽评估。"

---

## 3. 扫描故事状态

**首先：检查 `production/sprint-status.yaml`。**

如果存在，请直接读取——它是权威事实来源。
从 `status` 字段中提取每个故事的状态。无需扫描 Markdown。
使用其 `sprint`、`goal`、`start`、`end` 字段，而不是重新解析冲刺计划。

**如果 `sprint-status.yaml` 不存在**（旧式冲刺或首次设置），则回退到 Markdown 扫描：

1. 如果条目引用了故事文件路径，检查文件是否存在。
   读取文件并扫描状态标记：DONE、COMPLETE、IN PROGRESS、BLOCKED、NOT STARTED（不区分大小写）。
2. 如果条目没有文件路径（冲刺计划中的内联任务），则扫描冲刺计划本身中该条目旁的状态标记。
3. 如果找不到状态标记，归类为 NOT STARTED。
4. 如果引用了文件但文件不存在，归类为 MISSING 并注明。

使用回退模式时，在输出底部添加说明：
"⚠ 未找到 `sprint-status.yaml` — 状态由 Markdown 推断。运行 `/sprint-plan update` 生成它。"

可选地（仅快速检查——不要做深度扫描）：用 grep 扫描 `src/`，查找与故事系统 slug 匹配的目录或文件名，以作为实现证据的线索。这只是提示，不是最终状态。

### 过时故事检测

在收集完所有故事状态后，检查每个 IN PROGRESS 故事是否过时：

- 对于每个有引用文件的故事，读取该文件并查找 frontmatter 或头部中的 `Last Updated:` 字段（例如 `Last Updated: 2026-04-01` 或 `updated: 2026-04-01`）。接受任何合理的日期字段名：`Last Updated`、`Updated`、`last-updated`、`updated_at`。
- 使用今天的日期计算距该日期的天数。
- 如果日期超过 2 天前，将该故事标记为 **STALE**。
- 如果故事文件中没有日期字段，注明："没有时间戳 — 无法检查是否过时。"
- 如果故事没有引用文件（内联任务），注明："内联任务 — 无法检查是否过时。"

STALE 故事会包含在输出表中，并收集到一个 “Attention Needed” 部分（见第 5 阶段输出格式）。

**过时故事升级规则**：如果任何 IN PROGRESS 故事被标记为 STALE，则燃尽结论至少升级为 **At Risk** —— 即使完成百分比仍处于正常的 On Track 区间。记录升级原因："At Risk — [N] story(ies) with no progress in [N] days."

---

## 4. 燃尽评估

计算：
- 已完成任务（DONE 或 COMPLETE）
- 进行中任务（IN PROGRESS）
- 被阻塞任务（BLOCKED）
- 未开始任务（NOT STARTED 或 MISSING）
- 完成百分比： (complete / total) * 100

通过将完成百分比与已消耗时间百分比进行比较来评估燃尽：

- **On Track**：完成百分比与已消耗时间百分比相差不超过 10 个点，或领先
- **At Risk**：完成百分比落后已消耗时间百分比 10-25 个点
- **Behind**：完成百分比落后已消耗时间百分比超过 25 个点

如果日期不可用，则跳过燃尽评估并报告："On Track / At Risk / Behind：未知 — 未找到冲刺日期。"

---

## 5. 输出

将总输出控制在 30 行或更少。使用以下格式：

```markdown
## Sprint [N] Status — [Today's Date]
**Sprint Goal**: [from sprint plan]
**Days Remaining**: [N] of [total] ([% time consumed])

### Progress: [complete/total] tasks ([%])

| Story / Task         | Priority   | Status      | Owner   | Blocker        |
|----------------------|------------|-------------|---------|----------------|
| [title]              | Must Have  | DONE        | [owner] |                |
| [title]              | Must Have  | IN PROGRESS | [owner] |                |
| [title]              | Must Have  | BLOCKED     | [owner] | [brief reason] |
| [title]              | Should Have| NOT STARTED | [owner] |                |

### Attention Needed
| Story / Task         | Status      | Last Updated   | Days Stale | Note           |
|----------------------|-------------|----------------|------------|----------------|
| [title]              | IN PROGRESS | [date or N/A]  | [N days]   | [STALE / no timestamp — cannot check staleness / inline task — cannot check staleness] |

*(如果没有任何过时或存在时间戳疑虑的 IN PROGRESS 故事，则完全省略本节。)*

### Burndown: [On Track / At Risk / Behind]
[1-2 句。如果落后：指出哪些 Must Have 面临风险。如果进展正常：确认并注明团队可考虑拉入哪些 Should Have。]

### Must-Haves at Risk
[列出所有被 BLOCKED 或 NOT STARTED，且冲刺时间剩余不到 40% 的 Must Have 故事。如果没有，写 "None."]

### Emerging Risks
[从故事扫描中可见的任何风险：缺失文件、级联阻塞、没有负责人的故事。如果没有，写 "None identified."]

### Recommendation
[一条具体行动，或 "Sprint is on track — no action needed."]
```

---

## 6. 快速升级规则

在输出前应用这些规则；如果触发，则将标记放在输出顶部（状态表上方）：

**Critical flag** — 如果 Must Have 故事存在 BLOCKED 或 NOT STARTED，且冲刺时间剩余少于 40%：

```text
SPRINT AT RISK: [N] Must Have stories are not complete with [X]% of sprint time remaining. Recommend replanning with `/sprint-plan update`.
```

**Completion flag** — 如果所有 Must Have 故事都已完成：

```text
All Must Haves complete. Team can pull from Should Have backlog.
```

**Missing stories flag** — 如果任何引用的故事文件不存在：

```text
NOTE: [N] story files referenced in the sprint plan are missing.
Run `/story-readiness sprint` to validate story file coverage.
```

---

## 7. 协作协议

此技能为只读。它只报告磁盘上的观测事实。

- 不更新冲刺计划
- 不改变故事状态
- 不建议缩减范围（那是 `/sprint-plan update` 的职责）
- 每次运行最多只给出一条建议

如需查看某个具体故事的更多细节，用户可以直接读取故事文件，或运行 `/story-readiness [path]`。

如需重新规划冲刺，请使用 `/sprint-plan update`。
如需冲刺结束回顾，请使用 `/milestone-review`。