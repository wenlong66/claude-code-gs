---
name: create-stories
description: "把单个 epic 拆分为可实施的 story 文件。读取 epic、其 GDD、主管 ADR 与 control manifest。每个 story 都嵌入对应的 GDD requirement TR-ID、ADR 指导、验收标准、story 类型和测试证据路径。每个 epic 完成后运行。"
argument-hint: "[epic-slug | epic-path] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
agent: lead-programmer
---

# Create Stories

Story 是一个单一、可实施的行为——足够小，可在一次聚焦的会话中完成，独立、完整，并且能与一个 GDD requirement 和一个 ADR 决策完全追踪。开发者接手的是 stories。Architect 定义的是 epics。

**按 epic 运行此技能**，不要按层级。先为 Foundation epics 运行，再到 Core，以此类推——遵循依赖顺序。

**输出：**`production/epics/[epic-slug]/story-NNN-[slug].md` 文件

**上一步：**`/create-epics [system]`
**stories 存在后的下一步：**先 `/story-readiness [story-path]`，再 `/dev-story [story-path]`

---

## 1. 解析参数

如果存在，提取 `--review [full|lean|solo]` 并将其作为本次运行的 review mode 覆盖值。如果未提供，则读取 `production/review-mode.txt`（缺失时默认 `full`）。此解析后的模式适用于本技能中的所有 gate spawn——在每次 gate 调用前都按 `.claude/docs/director-gates.md` 中的检查模式执行。

- `/create-stories [epic-slug]` —— 例如 `/create-stories combat`
- `/create-stories production/epics/combat/EPIC.md` —— 也接受完整路径
- 无参数 —— 询问："Which epic would you like to break into stories?"
  Glob `production/epics/*/EPIC.md` 并列出可用 epics 及其状态。

---

## 2. 为该 Epic 加载全部上下文

完整读取：

- `production/epics/[epic-slug]/EPIC.md` —— epic 概览、主管 ADR、GDD requirements 表
- 该 epic 对应的 GDD（`design/gdd/[filename].md`）——读取全部 8 个章节，尤其是 Acceptance Criteria、Formulas 和 Edge Cases
- epic 中列出的所有主管 ADR —— 读取 Decision、Implementation Guidelines、Engine Compatibility 和 Engine Notes 章节
- `docs/architecture/control-manifest.md` —— 提取此 epic 所属层的规则；注意头部的 Manifest Version 日期
- `docs/architecture/tr-registry.yaml` —— 为此系统加载所有 TR-ID

**ADR 存在性验证**：读取 epic 中的主管 ADR 列表后，确认每个 ADR 文件在磁盘上都真实存在。如果有任何 ADR 文件找不到，**立刻停止**，不要开始分解任何 story：

> "Epic references [ADR-NNNN: title] but `docs/architecture/[adr-file].md` was not found.
> Check the filename in the epic's Governing ADRs list, or run `/architecture-decision`
> to create it. Cannot create stories until all referenced ADR files are present."

在确认所有被引用 ADR 文件都存在之前，不要进入步骤 3。

报告：`"Loaded epic [name], GDD [filename], [N] governing ADRs (all confirmed present), control manifest v[date]."`

---

## 3. 按类型对 stories 分类

**Story Type Classification**——根据验收标准为每个 story 分配类型：

| Story Type | 在哪些 criteria 下分配 |
|---|---|
| **Logic** | 公式、数值阈值、状态转换、AI 决策、计算 |
| **Integration** | 两个或更多系统交互、跨边界信号、save/load 往返 |
| **Visual/Feel** | 动画行为、VFX、"feels responsive"、时序、screen shake、音频同步 |
| **UI** | 菜单、HUD 元素、按钮、屏幕、对话框、tooltip |
| **Config/Data** | 仅平衡数值调整、纯数据文件更改——没有新增代码逻辑 |

混合 story：按风险最高的实现类型分配。
类型决定在 `/story-done` 关闭 story 之前需要什么测试证据。

---

## 4. 将 GDD 拆分为 stories

针对每条 GDD 验收标准：

1. 将需要相同核心实现的相关标准分组
2. 每个分组 = 一个 story
3. story 排序：先基础行为，再边界情况，最后 UI

**story 尺寸规则：**一个 story = 一个聚焦会话（约 2–4 小时）。如果一组标准需要更久，就拆成两个 story。

对每个 story，确定：
- **GDD requirement**：它满足哪些 acceptance criterion？
- **TR-ID**：在 `tr-registry.yaml` 中查找稳定 ID。如果没有匹配，使用 `TR-[system]-???` 并警告。
- **Governing ADR**：该 story 由哪个 ADR 决定如何实现？
  - `Status: Accepted` → 正常嵌入
  - `Status: Proposed` → 将 story 的 `Status` 设为 `Blocked`，并注明："BLOCKED: ADR-NNNN is Proposed — run `/architecture-decision` to advance it"
- **Story Type**：来自步骤 3 分类
- **Engine risk**：来自 ADR 的 Knowledge Risk 字段

---

## 4b. QA Lead Story Readiness Gate

**review mode 检查**——在 spawn QL-STORY-READY 前执行：
- `solo` → 跳过。注："QL-STORY-READY skipped — Solo mode." 进入步骤 5（展示 stories 供审阅）。
- `lean` → 跳过（不是 PHASE-GATE）。注："QL-STORY-READY skipped — Lean mode." 进入步骤 5（展示 stories 供审阅）。
- `full` → 正常 spawn。

在分解完所有 stories（步骤 4 完成）但在提交写入批准之前，通过 Task 使用 gate **QL-STORY-READY**（`.claude/docs/director-gates.md`）spawn `qa-lead`。

传入：完整的 story 列表（含验收标准、story 类型与 TR-ID）；以及该 epic 的 GDD 验收标准供参考。

展示 QA lead 的评估。对于每个被标记为 GAPS 或 INADEQUATE 的 story，在继续前先修订验收标准——验收标准不可测试的 story 不能正确实施。所有 stories 都达到 ADEQUATE 之后再继续。

**在达到 ADEQUATE 后**：对每个 Logic 与 Integration story，请 qa-lead 为每条验收标准生成具体的测试用例规格——每条标准一条，格式如下：

```
Test: [criterion text]
  Given: [precondition]
  When: [action]
  Then: [expected result / assertion]
  Edge cases: [boundary values or failure states to test]
```

对于 Visual/Feel 与 UI stories，则生成手动验证步骤：
```
Manual check: [criterion text]
  Setup: [how to reach the state]
  Verify: [what to look for]
  Pass condition: [unambiguous pass description]
```

这些测试用例会直接嵌入每个 story 的 `## QA Test Cases` 章节。开发者就是依据这些用例实现。程序员不会从零编写测试——QA 已经定义好了 “done” 的样子。

---

## 5. 展示 stories 供审阅

在写任何文件之前，先展示完整 story 列表：

```
## Stories for Epic: [name]

Story 001: [title] — Logic — ADR-NNNN
  Covers: TR-[system]-001 ([1-line summary of requirement])
  Test required: tests/unit/[system]/[slug]_test.[ext]

Story 002: [title] — Integration — ADR-MMMM
  Covers: TR-[system]-002, TR-[system]-003
  Test required: tests/integration/[system]/[slug]_test.[ext]

Story 003: [title] — Visual/Feel — ADR-NNNN
  Covers: TR-[system]-004
  Evidence required: production/qa/evidence/[slug]-evidence.md

[N stories total: N Logic, N Integration, N Visual/Feel, N UI, N Config/Data]
```

使用 `AskUserQuestion`：
- 提示："May I write these [N] stories to `production/epics/[epic-slug]/`?"
- 选项：`[A] Yes — write all [N] stories` / `[B] Not yet — I want to review or adjust first`

---

## 6. 写入 Story 文件

对每个 story，写入 `production/epics/[epic-slug]/story-[NNN]-[slug].md`：

```markdown
# Story [NNN]: [title]

> **Epic**: [epic name]
> **Status**: Ready
> **Layer**: [Foundation / Core / Feature / Presentation]
> **Type**: [Logic | Integration | Visual/Feel | UI | Config/Data]
> **Manifest Version**: [date from control-manifest.md header]

## Context

**GDD**: `design/gdd/[filename].md`
**Requirement**: `TR-[system]-NNN`
*(Requirement text lives in `docs/architecture/tr-registry.yaml` — read fresh at review time)*

**ADR Governing Implementation**: [ADR-NNNN: title]
**ADR Decision Summary**: [1-2 sentence summary of what the ADR decided]

**Engine**: [name + version] | **Risk**: [LOW / MEDIUM / HIGH]
**Engine Notes**: [from ADR Engine Compatibility section — post-cutoff APIs, verification required]

**Control Manifest Rules (this layer)**:
- Required: [relevant required pattern]
- Forbidden: [relevant forbidden pattern]
- Guardrail: [relevant performance guardrail]

---

## Acceptance Criteria

*From GDD `design/gdd/[filename].md`, scoped to this story:*

- [ ] [criterion 1 — directly from GDD]
- [ ] [criterion 2]
- [ ] [performance criterion if applicable]

---

## Implementation Notes

*Derived from ADR-NNNN Implementation Guidelines:*

[Specific, actionable guidance from the ADR. Do not paraphrase in ways that
change meaning. This is what the programmer reads instead of the ADR.]

---

## Out of Scope

*Handled by neighbouring stories — do not implement here:*

- [Story NNN+1]: [what it handles]

---

## QA Test Cases

*Written by qa-lead at story creation. The developer implements against these — do not invent new test cases during implementation.*

**[For Logic / Integration stories — automated test specs]:**

- **AC-1**: [criterion text]
  - Given: [precondition]
  - When: [action]
  - Then: [assertion]
  - Edge cases: [boundary values / failure states]

**[For Visual/Feel / UI stories — manual verification steps]:**

- **AC-1**: [criterion text]
  - Setup: [how to reach the state]
  - Verify: [what to look for]
  - Pass condition: [unambiguous pass description]

---

## Test Evidence

**Story Type**: [type]
**Required evidence**:
- Logic: `tests/unit/[system]/[story-slug]_test.[ext]` — must exist and pass
- Integration: `tests/integration/[system]/[story-slug]_test.[ext]` OR playtest doc
- Visual/Feel: `production/qa/evidence/[story-slug]-evidence.md` + sign-off
- UI: `production/qa/evidence/[story-slug]-evidence.md` or interaction test
- Config/Data: smoke check pass (`production/qa/smoke-*.md`)

**Status**: [ ] Not yet created

---

## Dependencies

- Depends on: [Story NNN-1 must be DONE, or "None"]
- Unlocks: [Story NNN+1, or "None"]
```

### 同时更新 `production/epics/[epic-slug]/EPIC.md`

把 “Stories: Not yet created” 那一行替换为填充好的表格：

```markdown
## Stories

| # | Story | Type | Status | ADR |
|---|-------|------|--------|-----|
| 001 | [title] | Logic | Ready | ADR-NNNN |
| 002 | [title] | Integration | Ready | ADR-MMMM |
```

---

## 7. 写完之后

使用 `AskUserQuestion`，并带上上下文相关的下一步：

检查：
- `production/epics/` 里是否还有尚未生成 stories 的 epics？列出来。
- 这是否是最后一个 epic？如果是，就把 `/sprint-plan` 作为选项之一。

Widget：
- 提示："[N] stories written to `production/epics/[epic-slug]/`. What next?"
- 选项（按需包含全部适用项）：
  - `[A] Start implementing — run /story-readiness [first-story-path]` (Recommended)
  - `[B] Create stories for [next-epic-slug] — run /create-stories [slug]`（仅当还有其他 epic 没有 stories 时）
  - `[C] Plan the sprint — run /sprint-plan`（仅当所有 epics 都已有 stories 时）
  - `[D] Stop here for this session`

输出中注明："Work through stories in order — each story's `Depends on:` field tells you what must be DONE before you can start it."

---

## 协作协议

1. **先读再展示**——在展示 story 列表前，先静默加载所有输入
2. **一次问清**——把该 epic 的所有 stories 一次性展示，而不是一个一个问
3. **对阻塞 story 发出警告**——在写文件前标记任何带 Proposed ADR 的 story
4. **写入前先问**——在写任何文件前，先获得全套 story 的批准
5. **不凭空发明**——验收标准来自 GDD，实现说明来自 ADR，规则来自 manifest
6. **绝不开始实现**——此技能止步于 story 文件层级

写入后（或用户拒绝后）：

- **Verdict: COMPLETE** —— 已将 [N] 个 stories 写入 `production/epics/[epic-slug]/`。运行 `/story-readiness` → `/dev-story` 开始实现。
- **Verdict: BLOCKED** —— 用户拒绝。未写入任何 story 文件。