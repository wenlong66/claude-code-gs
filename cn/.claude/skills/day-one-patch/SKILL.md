---
name: day-one-patch
description: "为游戏发售准备 day-one patch。对 gold master 之后但在公开发售前后发现的问题进行范围控制、优先级排序、实现与 QA 门禁，并确保在任何内容发布前都有回滚计划。把它当成一个带独立 QA gate 和回滚计划的迷你 sprint。"
argument-hint: "[scope: known-bugs | cert-feedback | all]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion
---

# Day-One Patch

每款已发售的游戏都会有 day-one patch。提前在发售日前规划它，可以避免混乱。此技能会把补丁范围限制在安全且必要的内容上，通过一个轻量 QA 流程，并确保在任何内容发布前都有回滚计划。它是一个迷你 sprint——不是 hotfix，也不是完整 sprint。

**何时运行：**
- 在 gold master build 锁定之后（cert 已批准或 launch candidate 已打标签）
- 当存在一些知道但在 gold master 中修复风险过高的 bug 时
- 当 cert feedback 要求在提交后做轻微修复时
- 当发售前 playtest 在 release gate 通过后暴露出必须修复的问题时

**Day-one patch 范围规则：**
- 只包含可安全快速修复的 P1/P2 bug
- 不新增功能——这是纯修复
- 不重构——只做最小可行改动
- 任何需要超过 4 小时开发时间的修复都应放到 patch 1.1，而不是 day-one

**输出：**`production/releases/day-one-patch-[version].md`

---

## 阶段 1：加载发售上下文

读取：
- `production/stage.txt` —— 确认项目处于 Release 阶段
- `production/gate-checks/` 下最新的文件 —— 读取 release gate verdict
- `production/qa/bugs/*.md` —— 加载所有 Status 为 Open 或 Fixed — Pending Verification 的 bug
- `production/sprints/` 最近的文件 —— 理解已发售内容
- `production/security/security-audit-*.md` 最近的文件 —— 检查是否有未解决的安全项

如果 `production/stage.txt` 不是 `Release` 或 `Polish`：
> "Day-one patch prep is for Release-stage projects. Current stage: [stage]. This skill is not appropriate until you are approaching launch."

---

## 阶段 2：为补丁范围做定界

### 步骤 2a — 将开放 bug 分类，判断是否纳入补丁

对每个开放 bug 评估：

| Criteria | Include in day-one? |
|-----------|-------------------|
| S1 or S2 severity | Yes — must include if safe to fix |
| P1 priority | Yes |
| Fix estimated < 4 hours | Yes |
| Fix requires architecture change | No — defer to 1.1 |
| Fix introduces new code paths | No — too risky |
| Fix is data/config only (no code change) | Yes — very low risk |
| Cert feedback requirement | Yes — required for platform approval |
| S3/S4 severity | Only if trivial config fix; otherwise defer |

### 步骤 2b — 向用户展示补丁范围

使用 `AskUserQuestion`：
- 提示："Based on open bugs and cert feedback, here is the proposed day-one patch scope. Does this look right?"
- 展示：纳入的 bug 表格（ID、严重度、描述、预估工作量）
- 展示：延后的 bug 表格（ID、严重度、延后原因）
- 选项：`[A] Approve this scope` / `[B] Adjust — I want to add or remove items` / `[C] No day-one patch needed`

如果选 [C]：输出 "No day-one patch required. Proceed to `/launch-checklist`." 然后停止。

### 步骤 2c — 检查总范围

汇总预估工作量。如果总量超过 1 天：
> "⚠️ Patch scope is [N hours] — this exceeds a safe day-one window. Consider deferring lower-priority items to patch 1.1. A bloated day-one patch introduces more risk than it removes."

使用 `AskUserQuestion` 确认是否继续，或缩减范围。

---

## 阶段 3：回滚计划

在写任何代码之前，先定义回滚流程。这是不可妥协的。

通过 Task spawn `release-manager`。要求他们提供一份回滚计划，覆盖：
- 如何在每个目标平台回滚到 gold master build
- 平台特定的回滚限制（某些平台不能回滚 cert builds）
- 谁负责触发回滚
- 如果发生回滚，需要什么玩家沟通

展示回滚计划。询问："May I write this rollback plan to `production/releases/rollback-plan-[version].md`?"

在回滚计划写入之前，不要进入阶段 4。

---

## 阶段 4：实施修复

对批准范围内的每个 bug，启动一个聚焦的实现循环：

1. 通过 Task spawn `lead-programmer`，传入：
   - bug 报告（精确复现步骤与已知根因）
   - 约束：只做最小可行修复，不做清理
   - 受影响文件（来自 bug 报告的 Technical Context 章节）

2. lead-programmer 实施并运行目标测试。

3. 通过 Task spawn `qa-tester` 验证：修复后 bug 还能复现吗？

对于仅 config/data 的修复：直接修改（不需要 programmer agent）。确认值已变更，并重新运行相关 smoke test。

---

## 阶段 5：补丁 QA 门禁

这是一次轻量 QA——不是完整的 `/team-qa`。补丁已经在 release gate 时做过 QA；现在只是重新验证被修改的区域。

通过 Task spawn `qa-lead`，传入：
- 所有变更文件列表
- 已修复 bug 列表（含阶段 4 的验证状态）
- 受影响系统的 smoke check 范围

请 qa-lead 判断：**是只做 targeted smoke check 就够了，还是某些修复触及了需要更广泛回归的系统？**

运行所需 QA 范围：
- **Targeted smoke check** —— 运行 `/smoke-check [affected-systems]`
- **更广泛回归** —— 对受影响系统运行 `tests/unit/` 和 `tests/integration/` 中的 targeted tests

在继续之前，QA verdict 必须是 PASS 或 PASS WITH WARNINGS。如果 FAIL：把失败的修复从 day-one patch 中剔除并延后到 1.1。

---

## 阶段 6：生成补丁记录

```markdown
# Day-One Patch: [Game Name] v[version]

**Date prepared**: [date]
**Target release**: [launch date or "day of launch"]
**Base build**: [gold master tag or commit]
**Patch build**: [patch tag or commit]

---

## Patch Notes (Internal)

### Bugs Fixed
| BUG-ID | Severity | Description | Fix summary |
|--------|----------|-------------|-------------|
| BUG-NNN | S[1-4] | [description] | [one-line fix] |

### Deferred to 1.1
| BUG-ID | Severity | Description | Reason deferred |
|--------|----------|-------------|-----------------|
| BUG-NNN | S[1-4] | [description] | [reason] |

---

## QA Sign-Off

**QA scope**: [Targeted smoke / Broader regression]
**Verdict**: [PASS / PASS WITH WARNINGS]
**QA lead**: qa-lead agent
**Date**: [date]
**Warnings (if any)**: [list or "None"]

---

## Rollback Plan

See: `production/releases/rollback-plan-[version].md`

**Trigger condition**: If [N] or more S1 bugs are reported within [X] hours of launch, execute rollback.
**Rollback owner**: [user / producer]

---

## Approvals Required Before Deploy

- [ ] lead-programmer: all fixes reviewed
- [ ] qa-lead: QA gate PASS confirmed
- [ ] producer: deployment timing approved
- [ ] release-manager: platform submission confirmed

---

## Player-Facing Patch Notes

[Draft for community-manager to review before publishing]

[list player-facing changes in plain language]
```

询问："May I write this patch record to `production/releases/day-one-patch-[version].md`?"

---

## 阶段 7：下一步

补丁记录写入后：

1. 运行 `/patch-notes` 生成玩家可见的版本说明
2. 对每个已修复 bug，在补丁上线后运行 `/bug-report verify [BUG-ID]`
3. 对每个已验证修复运行 `/bug-report close [BUG-ID]`
4. 使用 `/retrospective launch` 安排在发售后 48–72 小时的复盘

**如果补丁后仍有 S1 bug 未关闭：**
> "⚠️ S1 bugs remain open and were not patched. These are accepted risks. Document them in the rollback plan trigger conditions — if they occur at scale, rollback may be preferable to a follow-up patch."

---

## 协作协议

- **范围纪律最重要**——抵制范围蔓延；每增加一项都会增加风险
- **先回滚计划，永远如此**——没有回滚计划的补丁是不负责任的
- **延后不等于遗忘**——每个延后的 bug 都会自动生成 1.1 ticket
- **玩家沟通是补丁的一部分**——`/patch-notes` 是必需输出，而不是可选项