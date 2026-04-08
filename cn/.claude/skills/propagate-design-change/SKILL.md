---
name: propagate-design-change
description: "当 GDD 被修订时，扫描所有 ADR 和 traceability index，找出哪些架构决策可能已经过时。生成变更影响报告，并引导用户完成处理。"
argument-hint: "[path/to/changed-gdd.md]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash, Task
agent: technical-director
---

# Propagate Design Change

当 GDD 发生变化时，基于它写下的架构决策可能不再有效。这个技能会找出所有受影响的 ADR，对比 ADR 当时的假设与 GDD 的当前内容，并引导用户完成处理。

**用法：** `/propagate-design-change design/gdd/combat-system.md`

---

## 1. 验证参数

必须提供 GDD 路径参数。如果缺失，直接失败并输出：
> "Usage: `/propagate-design-change design/gdd/[system].md`
> Provide the path to the GDD that was changed."

验证该文件存在。如果不存在，失败并输出：
> "[path] not found. Check the path and try again."

---

## 2. 读取变更后的 GDD

完整读取当前 GDD。

---

## 3. 读取前一版本

使用 git 获取前一次提交版本：

```bash
git show HEAD:design/gdd/[filename].md
```

如果该文件没有 git 历史（新文件），报告：
> "No previous version in git — this appears to be a new GDD, not a revision.
> Nothing to propagate."

如果 git 返回了前一个版本，则进行概念性 diff：
- 识别发生变化的章节（新规则、删除规则、修改公式、变更 acceptance criteria、变更 tuning knobs）
- 识别未变化的章节
- 生成变更摘要：

```
## Change Summary: [GDD filename]
Date of revision: [today]

Changed sections:
- [Section name]: [what changed — new rule, removed rule, formula modified, etc.]

Unchanged sections:
- [Section name]

Key changes affecting architecture:
- [Change 1 — likely to affect ADRs]
- [Change 2]
```

---

## 4. 读取架构输入

读取 `docs/architecture/` 中所有 ADR：
- 对每个 ADR，完整读取文件
- 提取 "GDD Requirements Addressed" 表
- 记录每个 ADR 引用的 GDD 文档和 requirement ID

如果存在，则读取 `docs/architecture/architecture-traceability.md`。

报告："Loaded [N] ADRs. [M] reference [gdd filename]."

---

## 5. 影响分析

对每个引用了变更后 GDD 的 ADR：

将 ADR 的 "GDD Requirements Addressed" 条目与 GDD 中变更的章节进行对比。针对每个被引用的 requirement：

1. **定位 requirement** 在当前 GDD 中是否仍然存在？
2. **对比**：ADR 写成时 GDD 怎么说 vs. 现在怎么说？
3. **评估 ADR 决策**：该架构决策是否仍然有效？

将每个受影响 ADR 分类为以下之一：

| Status | Meaning |
|--------|---------|
| ✅ **Still Valid** | GDD 变化并不影响该 ADR 的决策 |
| ⚠️ **Needs Review** | GDD 变化可能影响该 ADR —— 需要人工判断 |
| 🔴 **Likely Superseded** | GDD 变化直接与该 ADR 的假设相矛盾 |

为每个受影响 ADR 生成一条影响项：

```
### ADR-NNNN: [title]
Status: [Still Valid / Needs Review / Likely Superseded]

What the ADR assumed about this GDD:
  "[relevant quote from the ADR's GDD Requirements Addressed section]"

What the GDD now says:
  "[relevant quote from the current GDD]"

Assessment:
  [Explanation of whether the ADR decision is still valid, and why]

Recommended action:
  [Keep as-is | Review and update | Mark Superseded and write new ADR]
```

---

## 6. 展示影响报告

在请求任何操作之前，先把完整影响报告展示给用户。格式：

```
## Design Change Impact Report
GDD: [filename]
Date: [today]
Changes detected: [N sections changed]
ADRs referencing this GDD: [M]

### Not Affected
[ADRs referencing this GDD whose decisions remain valid]

### Needs Review ([count])
[ADRs that may need updating]

### Likely Superseded ([count])
[ADRs whose assumptions are now contradicted]
```

---

## 6b. Director Gate — Technical Impact Review

**Review mode check**——在 spawn TD-CHANGE-IMPACT 之前应用：
- `solo` → 跳过。Note: "TD-CHANGE-IMPACT skipped — Solo mode." 继续进入 Phase 7。
- `lean` → 跳过。Note: "TD-CHANGE-IMPACT skipped — Lean mode." 继续进入 Phase 7。
- `full` → 正常 spawn。

使用 gate **TD-CHANGE-IMPACT**（`.claude/docs/director-gates.md`）spawn `technical-director`。

传入：Phase 6 的完整 Design Change Impact Report（变更摘要、所有受影响 ADR 及其 Still Valid / Needs Review / Likely Superseded 分类，以及推荐操作）。

technical-director 评审以下内容：
- 影响分类是否正确（没有把 ADR 低估风险）
- 推荐操作在架构上是否合理
- 是否遗漏了对其他 ADR 或系统的连锁影响

应用裁定：
- **APPROVE** → 进入 Phase 7 resolution workflow
- **CONCERNS** → 上报具体被标记的 ADR 或建议；使用 `AskUserQuestion`，选项：`Revise the impact assessment` / `Accept with noted concerns` / `Discuss further`
- **REJECT** → 不进入 resolution；先重新分析影响，再继续

---

## 7. 解决流程

对于每个标为 "Needs Review" 或 "Likely Superseded" 的 ADR，逐个询问用户处理方式：

逐个问：
> "ADR-NNNN ([title]) — [status]. What would you like to do?"
> Options:
> - "Mark Superseded (I'll write a new ADR)" — 将 ADR 状态行更新为 `Superseded by: [pending]`
> - "Update in place (minor revision)" — 打开 ADR 进行编辑；注明需要修订什么
> - "Keep as-is (the change doesn't actually affect this decision)"
> - "Skip for now (revisit later)"

对于标为 **Superseded** 的 ADR：
- 将 ADR 的 Status 字段更新为：`Superseded by ADR-[next number] (pending — see change-impact-[date]-[system].md)`
- 询问："May I update the status in [ADR filename]?"

---

## 8. 更新 Traceability Index

如果 `docs/architecture/architecture-traceability.md` 存在：
- 将变更后的 GDD requirements 添加到 "Superseded Requirements" 表：

```markdown
## Superseded Requirements
| Date | GDD | Requirement | Changed To | ADRs Affected | Resolution |
|------|-----|-------------|------------|---------------|------------|
| [date] | [gdd] | [old requirement text] | [new requirement text] | ADR-NNNN | [Superseded/Updated/Valid] |
```

询问："May I update the traceability index?"

---

## 9. 输出变更影响文档

询问："May I write the change impact report to `docs/architecture/change-impact-[date]-[system-slug].md`?"

该文档包含：
- 第 3 步的变更摘要
- 第 5 步的完整影响分析
- 第 7 步中做出的解决决定
- 需要新建或更新的 ADR 列表

如果用户同意：Verdict: **COMPLETE** — change impact report saved.
如果用户拒绝：Verdict: **BLOCKED** — user declined write.

---

## 10. 后续操作

根据解决决定，建议：

- **ADRs marked Superseded**："Run `/architecture-decision [title]` to write the replacement ADR. Then re-run `/propagate-design-change` to verify coverage."
- **ADRs to update in place**：列出每个 ADR 需要更新的具体字段
- **If many ADRs affected**："Run `/architecture-review` after all ADRs are updated to verify the full traceability matrix is still coherent."

---

## 协作协议

1. **静默读取** —— 在展示任何内容前先计算完整影响
2. **先展示完整报告** —— 让用户先看到范围，再请求操作
3. **逐个 ADR 询问** —— 不要批量决定；每个受影响 ADR 可能需要不同处理
4. **写入前先询问** —— 修改任何文件前都必须确认
5. **非破坏性** —— 永远不要删除 ADR 内容；只添加 "Superseded by" 说明
