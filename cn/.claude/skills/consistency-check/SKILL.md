---
name: consistency-check
description: "将所有 GDD 与实体 registry 对照，检测跨文档不一致：同一实体的数值不同、同一物品的数值不同、同一公式的变量不同。采用 grep-first 方法——先读 registry，再只定位冲突的 GDD 章节，而不是完整读取文档。"
argument-hint: "[full | since-last-review | entity:<name> | item:<name>]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Consistency Check

通过把所有 GDD 与实体 registry（`design/registry/entities.yaml`）进行比较来检测跨文档不一致。采用 grep-first 方法：先读取一次 registry，再只定位提到已登记名称的 GDD 章节——除非需要调查冲突，否则不做整份文档读取。

**这个技能是写入时的安全网。** 它能捕捉 `/design-system` 的分章节检查可能遗漏的内容，也能捕捉 `/review-all-gdds` 的整体审查发现得太晚的问题。

**何时运行：**
- 每写完一个新的 GDD 之后（在转到下一个系统之前）
- 在 `/review-all-gdds` 之前（让该技能从干净基线开始）
- 在 `/create-architecture` 之前（一致性问题会污染下游 ADR）
- 按需运行：`/consistency-check entity:[name]`，只检查某个实体

**输出：**冲突报告 + 可选 registry 修正

---

## 阶段 1：解析参数并加载 registry

**模式：**
- 无参数 / `full` —— 检查所有登记条目与所有 GDD
- `since-last-review` —— 仅检查自上一份 review 报告以来修改过的 GDD
- `entity:<name>` —— 跨所有 GDD 检查一个特定实体
- `item:<name>` —— 跨所有 GDD 检查一个特定物品

**加载 registry：**

```
Read path="design/registry/entities.yaml"
```

如果文件不存在或没有条目：
> "Entity registry is empty. Run `/design-system` to write GDDs — the registry is populated automatically after each GDD is completed. Nothing to check yet."

停止并退出。

从 registry 构建四个查找表：
- **entity_map**：`{ name → { source, attributes, referenced_by } }`
- **item_map**：`{ name → { source, value_gold, weight, ... } }`
- **formula_map**：`{ name → { source, variables, output_range } }`
- **constant_map**：`{ name → { source, value, unit } }`

统计登记条目总数。报告：
```
Registry loaded: [N] entities, [N] items, [N] formulas, [N] constants
Scope: [full | since-last-review | entity:name]
```

---

## 阶段 2：定位范围内的 GDD

```
Glob pattern="design/gdd/*.md"
```

排除：`game-concept.md`、`systems-index.md`、`game-pillars.md`——这些不是系统 GDD。

对于 `since-last-review` 模式：
```bash
git log --name-only --pretty=format: -- design/gdd/ | grep "\.md$" | sort -u
```

将范围限制为自最近一个 `design/gdd/gdd-cross-review-*.md` 文件创建时间之后修改的 GDD。

在扫描前先报告范围内的 GDD 列表。

---

## 阶段 3：Grep-first 冲突扫描

对每个 registry 条目，在所有范围内 GDD 中 Grep 该条目名称。
不要做完整读取——只提取匹配行及其上下文（`-C 3` 行）。

这是核心优化：不是读 10 份 GDD × 每份 400 行（4,000 行），而是 grep 50 个实体名 × 10 份 GDD（50 次定向搜索，每次命中返回约 10 行）。

### 3a：实体扫描

对 entity_map 中的每个实体：

```
Grep pattern="[entity_name]" glob="design/gdd/*.md" output_mode="content" -C 3
```

对每个 GDD 命中，提取实体附近提到的值：
- 任何数值属性（数量、成本、持续时间、范围、速率）
- 任何分类属性（类型、等级、类别）
- 任何派生值（总量、输出、结果）
- entity_map 中登记的任何其他属性

把提取值与 registry 条目比较。

**冲突检测：**
- Registry 说 `[entity_name].[attribute] = [value_A]`。GDD 说 `[entity_name] has [value_B]`。→ **CONFLICT**
- Registry 说 `[item_name].[attribute] = [value_A]`。GDD 说 `[item_name] is [value_B]`。→ **CONFLICT**
- GDD 提到了 `[entity_name]`，但没有说明该属性。→ **NOTE**（不是冲突，只是不可验证）

### 3b：物品扫描

对 item_map 中的每个物品，grep 所有 GDD 里的物品名。提取：
- 出售价格 / 价值 / gold value
- 重量
- 堆叠规则（stackable / non-stackable）
- 类别

与 registry 条目值比较。

### 3c：公式扫描

对 formula_map 中的每个公式，grep 所有 GDD 里的公式名。提取：
- 公式附近提到的变量名
- 输出范围或上限值

与 registry 条目比较：
- 变量名不同 → **CONFLICT**
- 输出范围不同 → **CONFLICT**

### 3d：常量扫描

对 constant_map 中的每个常量，grep 所有 GDD 里的常量名。提取：
- 常量名附近提到的任何数值

与 registry 值比较：
- 数值不同 → **CONFLICT**

---

## 阶段 4：深度调查（仅限冲突）

对阶段 3 中发现的每个冲突，做一次针对性的完整章节读取，以获得精确上下文：

```
Read path="design/gdd/[conflicting_gdd].md"
```
（如果文件很大，也可以用 Grep 配合更宽的上下文）

用完整上下文确认冲突。判断：
1. **哪个 GDD 是正确的？** 查看 registry 中的 `source:` 字段——source GDD 才是权威所有者。任何与其冲突的其他 GDD 都需要更新。
2. **registry 本身是否过时？** 如果 source GDD 在 registry 条目写入之后被更新（检查 git log），registry 可能已经陈旧。
3. **这是否真的是设计变更？** 如果冲突代表有意的设计决策，解决方案是：更新 source GDD，更新 registry，然后修复其他所有 GDD。

对每个冲突，分类为：
- **🔴 CONFLICT** —— 不同 GDD 中同名实体/物品/公式/常量的值不同。必须在 architecture 开始前解决。
- **⚠️ STALE REGISTRY** —— source GDD 的值变了，但 registry 没更新。需要更新 registry；其他 GDD 可能已经正确。
- **ℹ️ UNVERIFIABLE** —— 提到了实体，但没有可比较的属性。不是冲突，只是记录引用。

---

## 阶段 5：输出报告

```
## Consistency Check Report
Date: [date]
Registry entries checked: [N entities, N items, N formulas, N constants]
GDDs scanned: [N] ([list names])

---

### Conflicts Found (must resolve before architecture)

🔴 [Entity/Item/Formula/Constant Name]
   Registry (source: [gdd]): [attribute] = [value]
   Conflict in [other_gdd].md: [attribute] = [different_value]
   → Resolution needed: [which doc to change and to what]

---

### Stale Registry Entries (registry behind the GDD)

⚠️ [Entry Name]
   Registry says: [value] (written [date])
   Source GDD now says: [new value]
   → Update registry entry to match source GDD, then check referenced_by docs.

---

### Unverifiable References (no conflict, informational)

ℹ️ [gdd].md mentions [entity_name] but states no comparable attributes.
   No conflict detected. No action required.

---

### Clean Entries (no issues found)

✅ [N] registry entries verified across all GDDs with no conflicts.

---

Verdict: PASS | CONFLICTS FOUND
```

**结论：**
- **PASS** —— 无冲突。registry 与 GDD 在所有检查值上保持一致。
- **CONFLICTS FOUND** —— 检测到一个或多个冲突。列出解决步骤。

---

## 阶段 6：registry 修正

如果发现 stale registry 条目，询问：
> "May I update `design/registry/entities.yaml` to fix the [N] stale entries?"

对每个 stale 条目：
- 更新 `value` / attribute 字段
- 将 `revised:` 设为今天日期
- 用 YAML 注释记录旧值：`# was: [old_value] before [date]`

如果在 GDD 中发现了 registry 里没有的新条目，询问：
> "Found [N] entities/items mentioned in GDDs that aren't in the registry yet.
> May I add them to `design/registry/entities.yaml`?"

只添加那些出现在多个 GDD 中的条目（真正的跨系统事实）。

**绝不要删除 registry 条目。** 如果某条目已从所有 GDD 中移除，则设为 `status: deprecated`。

写入后：结论：**COMPLETE** —— consistency check 完成。
如果仍有未解决冲突：结论：**BLOCKED** —— 在 architecture 开始前，需要人工解决 [N] 个冲突。

### 6b. 追加到 Reflexion Log

如果发现了任何 🔴 CONFLICT 条目（无论是否已解决），为每个冲突向 `docs/consistency-failures.md` 追加一条记录：

```markdown
### [YYYY-MM-DD] — /consistency-check — 🔴 CONFLICT
**Domain**: [system domain(s) involved]
**Documents involved**: [source GDD] vs [conflicting GDD]
**What happened**: [specific conflict — entity name, attribute, differing values]
**Resolution**: [how it was fixed, or "Unresolved — manual action needed"]
**Pattern**: [generalised lesson, e.g. "Item values defined in combat GDD were not
referenced in economy GDD before authoring — always check entities.yaml first"]
```

只有在 `docs/consistency-failures.md` 已存在时才追加。如果文件缺失，静默跳过此步骤——不要在这个技能里创建该文件。

---

## 下一步

- **如果 PASS**：运行 `/review-all-gdds` 做整体设计理论审查，或者如果所有 MVP GDD 都完成了，就运行 `/create-architecture`。
- **如果 CONFLICTS FOUND**：修复被标记的 GDD，然后重新运行 `/consistency-check` 确认已解决。
- **如果 STALE REGISTRY**：先更新 registry（阶段 6），再重新运行以验证。
- 每写完一个新的 GDD 后都运行 `/consistency-check`，把问题尽早抓出来，而不是等到 architecture 阶段。