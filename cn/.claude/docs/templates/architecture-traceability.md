# 架构可追溯性索引

<!-- 活文档 — 由 /architecture-review 在每次审查运行后更新。
     除非修正错误，否则请勿手动编辑。 -->

## 文档状态

- **最后更新**: [YYYY-MM-DD]
- **引擎**: [例如 Godot 4.6]
- **已索引 GDD 数**: [N]
- **已索引 ADR 数**: [M]
- **最近审查**: [link to docs/architecture/architecture-review-[date].md]

## 覆盖摘要

| 状态 | 数量 | 百分比 |
|--------|-------|-----------|
| ✅ 已覆盖 | [X] | [%] |
| ⚠️ 部分 | [Y] | [%] |
| ❌ 缺口 | [Z] | [%] |
| **总计** | **[N]** | |

---

## 可追溯性矩阵

<!-- 每一行对应从 GDD 中提取的一项技术需求。
     “技术需求”指任何暗示特定架构决策的 GDD 语句：数据结构、性能约束、所需引擎能力、跨系统通信、状态持久化。 -->

| Req ID | GDD | System | Requirement Summary | ADR(s) | Status | Notes |
|--------|-----|--------|---------------------|--------|--------|-------|
| TR-[gdd]-001 | [filename] | [system name] | [one-line summary] | [ADR-NNNN] | ✅ | |
| TR-[gdd]-002 | [filename] | [system name] | [one-line summary] | — | ❌ GAP | 需要 `/architecture-decision [title]` |

---

## 已知缺口

按层级优先排序的、尚无 ADR 覆盖的需求（基础层优先）：

### 基础层缺口（阻塞 — 必须在编码前解决）
- [ ] TR-[id]: [requirement] — GDD: [file] — 建议 ADR: "[title]"

### 核心层缺口（必须在相关系统构建前解决）
- [ ] TR-[id]: [requirement] — GDD: [file] — 建议 ADR: "[title]"

### 功能层缺口（应在特性冲刺前解决）
- [ ] TR-[id]: [requirement] — GDD: [file] — 建议 ADR: "[title]"

### 表现层缺口（可推迟到实现阶段）
- [ ] TR-[id]: [requirement] — GDD: [file] — 建议 ADR: "[title]"

---

## 跨 ADR 冲突

<!-- 互相矛盾的 ADR 配对。必须解决。 -->

| Conflict ID | ADR A | ADR B | Type | Status |
|-------------|-------|-------|------|--------|
| CONFLICT-001 | ADR-NNNN | ADR-MMMM | Data ownership | 🔴 Unresolved |

---

## ADR → GDD 覆盖（反向索引）

<!-- 对于每个 ADR，它覆盖了哪些 GDD 需求？ -->

| ADR | Title | GDD Requirements Addressed | Engine Risk |
|-----|-------|---------------------------|-------------|
| ADR-0001 | [title] | TR-combat-001, TR-combat-002 | HIGH |

---

## 已废弃需求

<!-- 在编写 ADR 时存在于 GDD 中，但后来 GDD 已变更的需求。该 ADR 可能需要更新。 -->

| Req ID | GDD | Change | Affected ADR | Status |
|--------|-----|--------|-------------|--------|
| TR-[id] | [file] | [what changed] | ADR-NNNN | 🔴 ADR needs update |

---

## 如何使用本文档

**编写新的 ADR 时**：将其添加到“ADR → GDD 覆盖”表中，并在矩阵中将其满足的需求标记为 ✅。

**批准 GDD 变更时**：扫描该 GDD 的需求矩阵，并检查变更是否使任何现有 ADR 失效。如有需要，添加到“已废弃需求”中。

**运行 `/architecture-review` 时**：该技能会自动将当前状态更新到本文档中。

**门禁检查**：Pre-Production 门禁要求此文档存在，且基础层缺口为零。