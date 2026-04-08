---
name: quick-design
description: "适用于小改动的轻量设计规范——数值调优、小机制、平衡微调。当系统 GDD 已存在，或变更太小不足以单独写完整 GDD 时，跳过完整 GDD authoring。生成可直接嵌入 story 文件的 Quick Design Spec。"
argument-hint: "[对变更的简要描述]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Quick Design

这是针对**轻量级设计路径**的技能，适用于不需要完整 GDD 的改动。通过 `/design-system` 进行完整 GDD authoring 是重量级路径。对于大约 4 小时以内的实现工作使用这个技能——数值调优、小行为调整、小型功能追加，或者太小不足以单独出文档的独立特性。

**输出：** `design/quick-specs/[name]-[date].md`

**何时运行：** 任何时候只要改动太小，不适合 `/design-system`，但又足够重要，值得写下理由时。

---

## 1. 给变更分类

首先读取参数，判断这个变更属于哪一类：

- **Tuning** —— 在现有系统中改数字或平衡值，没有行为变化（最小路径）。示例："increase jump height from 5 to 6 units"、"reduce enemy patrol speed by 10%"。
- **Tweak** —— 对现有系统做小的行为改动，不引入新的状态、分支或系统。示例："make dash invincible on frame 1"、"allow combo to cancel into roll"。
- **Addition** —— 给现有系统增加一个小机制，可能引入 1–2 个新状态或交互。示例："add a parry window to the block mechanic"、"add a charge variant to the basic attack"。
- **New Small System** —— 一个独立特性，规模足够小，因此没有现有 GDD，且实现工作量约在一周以内。示例："achievement popup system"、"simple day/night visual cycle"。

如果变更**不**符合这些类别——它引入了一个新系统，且存在显著跨系统依赖、实现超过一周，或从根本上改变了现有系统的核心规则——就停止，并改用 `/design-system`。

先把分类展示给用户并确认无误，再继续。如果没有参数，就询问用户要改什么。

---

## 2. 上下文扫描

在起草之前，读取相关上下文：

- 搜索 `design/gdd/`，找到与这次变更最相关的 GDD。读取会受影响的章节。
- 检查 `design/gdd/systems-index.md` 是否存在。如果存在，读取它，了解该系统在依赖图中的位置及其层级。如果不存在，记录 "No systems index found — skipping dependency tier check." 并继续。
- 检查 `design/quick-specs/` 中是否有先前触及该系统的 quick spec——避免与它们冲突。
- 如果这是 Tuning 变更，还要检查 `assets/data/`，找到承载相关数值的数据文件。

报告你找到的内容："Found GDD at [path]. Relevant section: [section name]. No conflicting quick specs found."（如果有冲突也要说明。）

---

## 3. 起草 Quick Design Spec

按变更类别使用相应的 spec 格式。

### 对 Tuning 变更

生成单个表格：

```markdown
# Quick Design Spec: [Title]

**Type**: Tuning
**System**: [System name]
**GDD Reference**: `design/gdd/[filename].md` — Tuning Knobs section
**Date**: [today]

## Change

| Parameter | Old Value | New Value | Rationale |
|-----------|-----------|-----------|-----------|
| [param]   | [old]     | [new]     | [why]     |

## Tuning Knob Mapping

Maps to GDD Tuning Knob: [knob name and its documented range].
New value is [within / at the edge of / outside] the documented range.
[If outside: explain why the range should be extended.]

## Acceptance Criteria

- [ ] [Parameter] reads [new value] from `assets/data/[file]`
- [ ] Behavior difference is observable in [specific context]
- [ ] No regression in [related behavior]
```

### 对 Tweak 和 Addition 变更

```markdown
# Quick Design Spec: [Title]

**Type**: [Tweak / Addition]
**System**: [System name]
**GDD Reference**: `design/gdd/[filename].md`
**Date**: [today]

## Change Summary

[1-2 句话说明什么变化以及为什么。]

## Motivation

[为什么需要这个变更？它解决了什么玩家体验问题？如适用，请引用相关 MDA aesthetic 或玩家反馈。]

## Design Delta

Current GDD says (quoting `design/gdd/[filename].md`, [section]):

> [exact quote of the relevant rule or description]

This spec changes that to:

[New rule or description, written with the same precision as a GDD Detailed Rules section. A programmer should be able to implement from this text alone.]

## New Rules / Values

[完整、无歧义地说明替换内容。如果引入新状态，请列出来。如果引入新参数，请定义范围。]

## Affected Systems

| System | Impact | Action Required |
|--------|--------|-----------------|
| [system] | [how it is affected] | [update GDD / update data file / no action] |

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]
- [ ] No regression: [the original behavior this must not break]

## GDD Update Required?

[Yes / No]
[If yes: which file, which section, and what the update should say.]
```

### 对 New Small System 变更

使用裁剪版 GDD 结构。只包含直接必要的章节——除非系统确实需要，否则跳过 Player Fantasy、完整 Formulas 和 Edge Cases。

```markdown
# Quick Design Spec: [Title]

**Type**: New Small System
**Scope**: [1-2 sentence description of what this system does and doesn't do]
**Date**: [today]
**Estimated Implementation**: [hours]

## Overview

[一段话，新团队成员也能理解。这个系统做什么、何时激活、会产出什么？]

## Core Rules

[系统的无歧义规则。顺序行为使用编号列表，条件使用项目列表。精确到程序员无需追问即可实现。]

## Tuning Knobs

| Knob | Default | Range | Category | Rationale |
|------|---------|-------|----------|-----------|
| [name] | [value] | [min–max] | [feel/curve/gate] | [why this default] |

All values must live in `assets/data/[appropriate-file].json`, not hardcoded.

## Acceptance Criteria

- [ ] [Functional criterion: does the right thing]
- [ ] [Functional criterion: handles the edge case]
- [ ] [Experiential criterion: feels right — what a playtest validates]
- [ ] [Regression criterion: does not break adjacent system]

## Systems Index

This system is not currently in `design/gdd/systems-index.md`.
[If it should be added: suggest which layer and priority tier.]
[If it is too small to track: state "This system is below systems-index tracking threshold — quick spec is sufficient."]
```

---

## 4. 批准与归档

完整向用户展示草稿。然后询问：

"May I write this Quick Design Spec to
`design/quick-specs/[kebab-case-title]-[YYYY-MM-DD].md`?"

文件名使用今天的日期。标题应为该变更的 kebab-case 描述（例如 `jump-height-tuning-2026-03-10`、`parry-window-addition-2026-03-10`）。

如果同意，先在不存在时创建 `design/quick-specs/` 目录，然后写入文件。

如果 spec 中标记需要 GDD 更新，在写完 quick spec 后再单独询问：

"This spec modifies rules in [System Name]. May I update
`design/gdd/[filename].md` — specifically the [section name] section?"

在询问前显示准确的变更文本（旧 vs. 新）。没有明确批准，不要修改 GDD。

---

## 5. 交接

写入文件后输出：

```
Quick Design Spec written to: design/quick-specs/[filename].md
Type: [Tuning / Tweak / Addition / New Small System]
System: [system name]
GDD update: [Required — pending approval / Applied / Not required]

Next step: This spec is ready for `/story-readiness` validation before
implementation. Reference this spec in the story's GDD Reference field.
```

### Pipeline Notes

Verdict: **COMPLETE** — quick design spec written and ready for implementation.

Quick Design Specs **bypass** `/design-review` and `/review-all-gdds` by design。它们适用于小型、低风险、范围明确的变更，此时完整审查流水线的成本高于变更本身的风险。

如果满足以下任意条件，就转回完整流水线：
- 变更增加了应进入 systems index 的新系统
- 变更显著改变了跨系统行为或系统与其他系统之间的契约
- 变更引入了影响游戏 MDA aesthetic 平衡的新玩家可见机制
- 实现工作预计超过一周

在这些情况下："This change has grown beyond quick-spec scope. I recommend using `/design-system` to author a full GDD for this."

---

## 推荐下一步

- 运行 `/story-readiness [story-path]`，在实现开始前验证 story——在 story 的 GDD Reference 字段中引用这份 spec
- 运行 `/dev-story [story-path]`，在 story 通过 readiness checks 后实施
- 如果变更比预期更大，运行 `/design-system [system-name]` 来改写完整 GDD
