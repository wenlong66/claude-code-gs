---
name: content-audit
description: "审核 GDD 中指定的内容数量与实际已实现内容是否一致。识别计划内容与已构建内容之间的差距。"
argument-hint: "[system-name | --summary | (no arg = full audit)]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
agent: producer
---

在调用此技能时：

解析参数：
- 无参数 → 对所有系统进行完整审计
- `[system-name]` → 只审计该单个系统
- `--summary` → 仅输出摘要表，不写文件

---

## 阶段 1 — 收集上下文

1. **读取 `design/gdd/systems-index.md`**，获取所有系统、类别，以及 MVP/priority tier。

2. **L0 预扫描**：在完整读取任何 GDD 之前，先 Grep 所有 GDD 文件，查找 `## Summary` 章节以及常见内容计数关键词：
   ```
   Grep pattern="(## Summary|N enemies|N levels|N items|N abilities|enemy types|item types)" glob="design/gdd/*.md" output_mode="files_with_matches"
   ```
   对于单系统审计：跳过此步骤，直接完整读取。
   对于完整审计：只完整读取匹配内容计数关键词的 GDD。
   没有内容计数语言的 GDD（纯机制 GDD）会被记录为“没有可审计的内容数量”，而不会做完整读取。

3. **完整读取范围内的 GDD 文件**（如果给出了系统名，则读取该系统的单个 GDD）。

4. **对每个 GDD，提取显式的内容数量或清单。** 查找如下模式：
   - "N enemies" / "enemy types:" / 命名敌人列表
   - "N levels" / "N areas" / "N maps" / "N stages"
   - "N items" / "N weapons" / "N equipment pieces"
   - "N abilities" / "N skills" / "N spells"
   - "N dialogue scenes" / "N conversations" / "N cutscenes"
   - "N quests" / "N missions" / "N objectives"
   - 任何显式枚举列表（命名内容项的 bullet list）

4. **根据提取结果构建内容清单表：**

   | System | Content Type | Specified Count/List | Source GDD |
   |--------|-------------|---------------------|------------|

   注意：如果 GDD 只是定性描述，没有数量，则记录为 "Unspecified" 并标记——未指定数量本身就是值得指出的设计缺口。

---

## 阶段 2 — 实现扫描

针对阶段 1 中发现的每一种内容类型，扫描相关目录统计已实现内容。使用 Glob 和 Grep 定位文件。

**Levels / Areas / Maps：**
- Glob `assets/**/*.tscn`, `assets/**/*.unity`, `assets/**/*.umap`
- Glob `src/**/*.tscn`, `src/**/*.unity`
- 查找子目录名包含 `levels/`、`areas/`、`maps/`、`worlds/`、`stages/` 的 scene 文件
- 统计看起来像 level/scene 定义的唯一文件（不含 UI scene）

**Enemies / Characters / NPCs：**
- Glob `assets/data/**/enemies/**`, `assets/data/**/characters/**`
- Glob `src/**/enemies/**`, `src/**/characters/**`
- 查找定义实体属性的 `.json`、`.tres`、`.asset`、`.yaml` 数据文件
- 查找 character 子目录中的 scene/prefab 文件

**Items / Equipment / Loot：**
- Glob `assets/data/**/items/**`, `assets/data/**/equipment/**`,
  `assets/data/**/loot/**`
- 查找 `.json`、`.tres`、`.asset` 数据文件

**Abilities / Skills / Spells：**
- Glob `assets/data/**/abilities/**`, `assets/data/**/skills/**`,
  `assets/data/**/spells/**`
- 查找 `.json`、`.tres`、`.asset` 数据文件

**Dialogue / Conversations / Cutscenes：**
- Glob `assets/**/*.dialogue`, `assets/**/*.csv`, `assets/**/*.ink`
- Grep `assets/data/` 中的对话数据文件

**Quests / Missions：**
- Glob `assets/data/**/quests/**`, `assets/data/**/missions/**`
- 查找 `.json`、`.yaml` 定义文件

**引擎相关说明（需在报告中注明）：**
- 计数只是近似值——该技能无法完美解析每种引擎格式，也无法始终区分 editor-only 文件和正式内容
- scene 文件可能同时包含 gameplay 内容和系统/UI scene；扫描会把所有匹配都计入，并注明此注意事项

---

## 阶段 3 — 缺口报告

生成缺口表：

```
| System | Content Type | Specified | Found | Gap | Status |
|--------|-------------|-----------|-------|-----|--------|
```

**状态类别：**
- `COMPLETE` —— Found ≥ Specified（100%+）
- `IN PROGRESS` —— Found 是 Specified 的 50–99%
- `EARLY` —— Found 是 Specified 的 1–49%
- `NOT STARTED` —— Found 为 0

**优先级标记：**
如果报告中的系统同时满足以下条件，则标为 `HIGH PRIORITY`：
- 状态为 `NOT STARTED` 或 `EARLY`，并且
- 系统在 systems index 中被标记为 MVP 或 Vertical Slice，或
- systems index 显示该系统阻塞下游系统

**摘要行：**
- 总指定内容项数（Specified 列所有值之和）
- 总已发现内容项数（Found 列所有值之和）
- 整体缺口百分比：`(Specified - Found) / Specified * 100`

---

## 阶段 4 — 输出

### 完整审计与单系统模式

把缺口表和摘要呈现给用户。询问："May I write the full report to `docs/content-audit-[YYYY-MM-DD].md`?"

如果同意，写入文件：

```markdown
# Content Audit — [Date]

## Summary
- **Total specified**: [N] content items across [M] systems
- **Total found**: [N]
- **Gap**: [N] items ([X%] unimplemented)
- **Scope**: [Full audit | System: name]

> Note: Counts are approximations based on file scanning.
> The audit cannot distinguish shipped content from editor/test assets.
> Manual verification is recommended for any HIGH PRIORITY gaps.

## Gap Table

| System | Content Type | Specified | Found | Gap | Status |
|--------|-------------|-----------|-------|-----|--------|

## HIGH PRIORITY Gaps

[列出所有被标记为 HIGH PRIORITY 的系统及其理由]

## Per-System Breakdown

### [System Name]
- **GDD**: `design/gdd/[file].md`
- **Content types audited**: [list]
- **Notes**: [与该系统扫描准确性相关的任何注意事项]

## Recommendation

把实施精力优先放在：
1. [最高缺口且为 HIGH PRIORITY 的系统]
2. [第二个系统]
3. [第三个系统]

## Unspecified Content Counts

下列 GDD 描述了内容，但没有给出明确数量。
若要提升可审计性，建议补充数量：
[带有 "Unspecified" 的 GDD 与内容类型列表]
```

写完报告后，询问：

> "Would you like to create backlog stories for any of the content gaps?"

如果用户同意：对用户选择的每个系统，建议一个 story 标题，并指引他们使用 `/create-stories [epic-slug]` 或 `/quick-design`，取决于缺口规模。

### --summary 模式

直接在对话中输出 Gap Table 和 Summary。不要写文件。
最后以："Run `/content-audit` without `--summary` to write the full report." 结束。

---

## 阶段 5 — 下一步

审计之后，推荐最有价值的后续动作：

- 如果某个系统是 `NOT STARTED` 且被标为 MVP → "Run `/design-system [name]` to add missing content counts to the GDD before implementation begins."
- 如果总缺口 >50% → "Run `/sprint-plan` to allocate content work across upcoming sprints."
- 如果需要 backlog stories → "Run `/create-stories [epic-slug]` for each HIGH PRIORITY gap."
- 如果使用了 `--summary` → "Run `/content-audit` (no flag) to write the full report to `docs/`."

结论：**COMPLETE** —— content audit 完成。