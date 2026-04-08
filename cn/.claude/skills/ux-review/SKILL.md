---
name: ux-review
description: "验证 UX 规格、HUD 设计或交互模式库是否完整、符合无障碍要求、与 GDD 对齐并已具备实施条件。产出 APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED verdict，并列出具体缺口。"
argument-hint: "[file-path or 'all' or 'hud' or 'patterns']"
user-invocable: true
allowed-tools: Read, Glob, Grep
agent: ux-designer
---

## 概述

在 UX 设计文档进入实施流程之前对其进行验证。
它在 `/team-ui` 流程中充当 UX Design 与 Visual Design/Implementation 之间的质量门禁。

**运行此技能：**
- 在通过 `/ux-design` 完成 UX spec 后
- 在交给 `ui-programmer` 或 `art-director` 之前
- 在 Pre-Production 到 Production 的 gate check 之前（该 gate 要求关键屏幕拥有已审阅的 UX specs）
- 在 UX spec 进行重大修订后

**Verdict 等级：**
- **APPROVED** — spec 完整、一致且可实施
- **NEEDS REVISION** — 找到具体缺口；在交接前修复，但不需要全面重做
- **MAJOR REVISION NEEDED** — 范围、玩家需求或完整性存在根本问题；需要大幅返工

---

## 第 1 阶段：解析参数

- **特定文件路径**（例如 `/ux-review design/ux/inventory.md`）：验证该单个文档
- **`all`**：查找 `design/ux/` 中所有文件并逐个验证
- **`hud`**：专门验证 `design/ux/hud.md`
- **`patterns`**：专门验证 `design/ux/interaction-patterns.md`
- **无参数**：询问用户要验证哪个 spec

对于 `all`，先输出摘要表（file | verdict | primary issue），然后再给出每个文件的完整细节。

---

## 第 2 阶段：载入交叉引用上下文

在验证任何 spec 之前，先加载：

1. **输入与平台配置**：读取 `.claude/docs/technical-preferences.md` 并提取 `## Input & Platform`。这是关于游戏支持哪些输入方式的权威来源——用它来驱动第 3A 阶段的 Input Method Coverage 检查，而不是使用 spec 自己的头部。如果未配置，则退回使用 spec 头部。
2. `design/accessibility-requirements.md` 中承诺的无障碍层级（如果存在）
3. `design/ux/interaction-patterns.md` 中的交互模式库（如果存在）
4. spec 头部中引用的 GDD（读取其 UI Requirements 小节）
5. `design/player-journey.md`（如果存在），用于验证 arrival context

---

## 第 3A 阶段：UX Spec 验证清单

对基于 `ux-spec.md` 的文档运行所有检查。

### 完整性（必需章节）

- [ ] 文档头部存在，且包含 Status、Author、Platform Target
- [ ] Purpose & Player Need —— 包含站在玩家角度的需求陈述（而不是开发者视角）
- [ ] Player Context on Arrival —— 描述玩家到达时的状态和先前活动
- [ ] Navigation Position —— 显示该屏幕在层级中的位置
- [ ] Entry & Exit Points —— 文档化所有进入来源和退出目的地
- [ ] Layout Specification —— 定义了 zones，并且存在 component inventory 表
- [ ] States & Variants —— 至少记录 loading、empty/populated 和 error 状态
- [ ] Interaction Map —— 覆盖所有目标输入方式（检查头部中的平台目标）
- [ ] Data Requirements —— 每个显示的数据元素都有来源系统和 owner
- [ ] Events Fired —— 每个玩家动作都有对应事件或明确的无事件说明
- [ ] Transitions & Animations —— 至少定义进入/退出过渡
- [ ] Accessibility Requirements —— 存在屏幕级要求
- [ ] Localization Considerations —— 文本元素的最大字符数
- [ ] Acceptance Criteria —— 至少 5 条具体且可测试的标准

### 质量检查

**Player Need 清晰度**
- [ ] Purpose 是从玩家视角撰写的，而不是系统/开发者视角
- [ ] 到达时的玩家目标清晰明确（"The player arrives wanting to ___"）
- [ ] 玩家到达时的上下文是具体的（不只是“他们打开了 inventory”）

**状态完整性**
- [ ] 文档了 error state（不是只有 happy path）
- [ ] 文档了 empty state（没有数据时的情况）
- [ ] 如果屏幕会异步拉取数据，则文档了 loading state
- [ ] 任何带计时器或自动消失的状态都写明了持续时间

**输入方式覆盖**
- [ ] 如果平台包含 PC：完整说明仅键盘导航
- [ ] 如果平台包含 console/gamepad：文档了 d-pad 导航和 face button 映射
- [ ] 没有任何交互要求在 gamepad 上做出鼠标式精确操作
- [ ] 定义了焦点顺序（键盘的 Tab 顺序、gamepad 的 d-pad 顺序）

**数据架构**
- [ ] 没有数据元素把 "UI" 列为 owner（UI 不应拥有游戏状态）
- [ ] 所有实时数据都说明了更新频率（不只是写“realtime”——是由什么触发更新？）
- [ ] 所有数据元素都说明了 null 处理（数据不可用时显示什么？）

**无障碍**
- [ ] 与 `accessibility-requirements.md` 中承诺的无障碍层级匹配或超出
- [ ] 如果是 Basic tier：没有仅靠颜色传达信息的指示器
- [ ] 如果是 Standard tier+：记录了焦点顺序，并指定了文本对比度比值
- [ ] 如果是 Comprehensive tier+：针对关键状态变化提供屏幕阅读器播报
- [ ] 色盲检查：任何使用颜色编码的元素都有非颜色替代方案

**GDD 对齐**
- [ ] 头部引用的每条 GDD UI Requirement 都在本 spec 中得到处理
- [ ] 没有任何 UI 元素在没有对应 GDD requirement 的情况下显示或修改游戏状态
- [ ] 没有 GDD UI Requirement 从本 spec 中缺失（交叉检查被引用的 GDD 小节）

**模式库一致性**
- [ ] 所有交互组件都引用了模式库（或注明它们是新模式）
- [ ] 如果模式库中已经存在某种行为，则不从头重写该行为
- [ ] 本 spec 中发明的新模式都被标记为应加入模式库

**本地化**
- [ ] 所有文字较多的元素都存在字符限制警告
- [ ] 任何对布局关键的文本都标记了 40% 扩展兼容

**Acceptance Criteria 质量**
- [ ] 标准足够具体，以至于未读过其他设计文档的 QA tester 也能验证
- [ ] 存在性能标准（屏幕在 Xms 内打开）
- [ ] 存在分辨率标准
- [ ] 没有任何标准需要阅读其他文档才能评估

---

## 第 3B 阶段：HUD 验证清单

对基于 `hud-design.md` 的文档运行所有检查。

### 完整性

- [ ] 定义了 HUD Philosophy
- [ ] Information Architecture 表覆盖了所有在 GDD 中具有 UI Requirements 的系统
- [ ] Layout Zones 为所有目标平台定义了安全区边距
- [ ] 每个 HUD 元素都有完整规格（zone、visibility trigger、data source、priority）
- [ ] HUD States by Gameplay Context 至少覆盖：exploration、combat、dialogue/cutscene、paused
- [ ] 定义了 Visual Budget（最大同时元素数、最大屏幕占比）
- [ ] Platform Adaptation 覆盖所有目标平台
- [ ] 为玩家可调元素提供了 Tuning Knobs

### 质量检查

- [ ] 没有 HUD 元素在没有可见性规则的情况下覆盖中心游玩区域
- [ ] 任何 GDD 中存在的信息项都要么在 HUD 中，要么被显式归类为 "hidden/demand"
- [ ] 所有使用颜色编码的 HUD 元素都有色盲变体
- [ ] Feedback & Notification 小节中的 HUD 元素定义了队列/优先级行为
- [ ] Visual Budget 符合：总同时元素数量在预算内

### GDD 对齐

- [ ] `design/gdd/systems-index.md` 中所有具有 UI 类别的系统，都在 HUD 中有表现（或有合理缺失说明）

---

## 第 3C 阶段：模式库验证清单

- [ ] 模式目录索引是最新的（与文档中的实际模式一致）
- [ ] 所有标准控制模式都已定义：button variants、toggle、slider、dropdown、list、grid、modal、dialog、toast、tooltip、progress bar、input field、tab bar、scroll
- [ ] 所有当前 UX specs 需要的游戏特定模式都已存在
- [ ] 每个模式都包含：When to Use、When NOT to Use、完整状态规格、无障碍规格、实现说明
- [ ] 存在 Animation Standards 表
- [ ] 存在 Sound Standards 表
- [ ] 模式之间没有冲突行为（例如，所有导航模式中的 “Back” 行为一致）

---

## 第 4 阶段：输出 verdict

```markdown
## UX Review: [Document Name]
**Date**: [date]
**Reviewer**: ux-review skill
**Document**: [file path]
**Platform Target**: [from header]
**Accessibility Tier**: [from header or accessibility-requirements.md]

### Completeness: [X/Y sections present]
- [x] Purpose & Player Need
- [ ] States & Variants — MISSING: error state not documented

### Quality Issues: [N found]
1. **[Issue title]** [BLOCKING / ADVISORY]
   - What's wrong: [specific description]
   - Where: [section name]
   - Fix: [specific action to take]

### GDD Alignment: [ALIGNED / GAPS FOUND]
- GDD [name] UI Requirements — [X/Y requirements covered]
- Missing: [list any uncovered GDD requirements]

### Accessibility: [COMPLIANT / GAPS / NON-COMPLIANT]
- Target tier: [tier]
- [list specific accessibility findings]

### Pattern Library: [CONSISTENT / INCONSISTENCIES FOUND]
- [findings]

### Verdict: APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED
**Blocking issues**: [N] — must be resolved before implementation
**Advisory issues**: [N] — recommended but not blocking

[如果是 APPROVED]：This spec is ready for handoff to `/team-ui` Phase 2 (Visual Design).

[如果是 NEEDS REVISION]：Address the [N] blocking issues above, then re-run `/ux-review`.

[如果是 MAJOR REVISION NEEDED]：The spec has fundamental gaps in [areas].
Recommend returning to `/ux-design` to rework [sections].
```

---

## 第 5 阶段：协作协议

此技能是只读的——它绝不编辑或写入文件。它只报告发现。

在给出 verdict 后：
- 对于 **APPROVED**：建议运行 `/team-ui` 来开始实施协调
- 对于 **NEEDS REVISION**：提出帮助修复具体缺口（"Would you like me to help draft the missing error state?"）——但不要自动修复；等用户指示
- 对于 **MAJOR REVISION NEEDED**：建议返回 `/ux-design`，并重做具体 section

不要阻止用户继续前进——verdict 是建议性的。记录风险，呈现发现，让用户决定是否在有顾虑的情况下继续。若用户选择在 NEEDS REVISION spec 上继续，则其承担文档中记录的风险。