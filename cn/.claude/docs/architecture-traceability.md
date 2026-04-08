# 架构可追溯性索引

<!-- 活文档 —— 由 /architecture-review 在每次审查后更新。
     除非是修正错误，否则不要手动编辑。 -->

## 文档状态

- **最后更新**：[YYYY-MM-DD]
- **引擎**：[例如 Godot 4.6]
- **已索引 GDD 数量**：[N]
- **已索引 ADR 数量**：[M]
- **最近审查**：[docs/architecture/architecture-review-[date].md 的链接]

## 覆盖摘要

| 状态 | 数量 | 百分比 |
|------|------|--------|
| ✅ 已覆盖 | [X] | [%] |
| ⚠️ 部分覆盖 | [Y] | [%] |
| ❌ 存在缺口 | [Z] | [%] |
| **总计** | **[N]** | |

---

## 可追溯性矩阵

<!-- 每一行对应从 GDD 中提取出的一个技术需求。
     “技术需求”指任何暗示了具体架构决策的 GDD 语句：数据结构、性能约束、所需引擎能力、跨系统通信、状态持久化。 -->

| Req ID | GDD | 系统 | 需求摘要 | ADR(s) | 状态 | 备注 |
|--------|-----|------|----------|--------|------|------|
| TR-[gdd]-001 | [filename] | [system name] | [one-line summary] | [ADR-NNNN] | ✅ | |
| TR-[gdd]-002 | [filename] | [system name] | [one-line summary] | — | ❌ GAP | 需要 `/architecture-decision [title]` |

---

## 已知缺口

按层级排列、尚无 ADR 覆盖的需求（Foundation 最高优先）。

### Foundation 层缺口（BLOCKING — 编码前必须解决）
- [ ] TR-[id]：[requirement] — GDD：[file] — 建议 ADR："[title]"

### Core 层缺口（在相关系统构建前必须解决）
- [ ] TR-[id]：[requirement] — GDD：[file] — 建议 ADR："[title]"

### Feature 层缺口（在功能冲刺前应解决）
- [ ] TR-[id]：[requirement] — GDD：[file] — 建议 ADR："[title]"

### Presentation 层缺口（可延后到实现阶段）
- [ ] TR-[id]：[requirement] — GDD：[file] — 建议 ADR："[title]"

---

## 跨 ADR 冲突

<!-- 彼此矛盾的 ADR 配对。必须解决。 -->

| Conflict ID | ADR A | ADR B | 类型 | 状态 |
|-------------|-------|-------|------|------|
| CONFLICT-001 | ADR-NNNN | ADR-MMMM | 数据所有权 | 🔴 未解决 |

---

## ADR → GDD 覆盖（反向索引）

<!-- 每个 ADR 对应它解决了哪些 GDD 需求。 -->

| ADR | 标题 | 覆盖的 GDD 需求 | 引擎风险 |
|-----|------|----------------|---------|
| ADR-0001 | [title] | TR-combat-001, TR-combat-002 | HIGH |

---

## 已被取代的需求

<!-- 某个 ADR 编写后，GDD 中原本存在的需求后来发生了变化。该 ADR 可能需要更新。 -->

| Req ID | GDD | 变更内容 | 受影响 ADR | 状态 |
|--------|-----|----------|-----------|------|
| TR-[id] | [file] | [what changed] | ADR-NNNN | 🔴 需要更新 |

---

## 如何使用本文件

**编写新 ADR 时**：将其加入“ADR → GDD 覆盖”表，并在矩阵中把它满足的需求标记为 ✅。

**批准 GDD 修改时**：检查该 GDD 的相关需求，并确认变更是否使已有 ADR 失效。如果失效，则添加到“已被取代的需求”。

**运行 `/architecture-review` 时**：该技能会自动用当前状态更新本文件。

**门禁检查**：Pre-Production 门禁要求此文件存在，并且 Foundation 层缺口必须为 0。