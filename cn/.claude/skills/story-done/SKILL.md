---
name: story-done
description: "故事完成收尾审查。读取故事文件，核对每条验收标准与实现是否一致，检查是否偏离 GDD/ADR，提示代码审查，更新故事状态为 Complete，并从冲刺中找出下一个可接手的故事。"
argument-hint: "[story-file-path] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Edit, AskUserQuestion, Task
---

# 故事完成

此技能用于打通设计与实现之间的闭环。请在完成任何故事的实现后运行它。它会确保在将故事标记为完成之前，每条验收标准都已验证，GDD 和 ADR 的偏差都被明确记录而不是悄悄引入，代码审查会被提醒而不是被遗忘，并且故事文件会反映真实完成状态。

**输出：** 已更新的故事文件（Status: Complete）+ 显示下一个故事。

---

## 第 1 阶段：查找故事

解析审查模式（只解析一次，本次运行中的所有 gate spawn 都复用）：
1. 如果传入了 `--review [full|lean|solo]` → 使用该值
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认 `lean`

完整检查模式见 `.claude/docs/director-gates.md`。

**如果提供了文件路径**（例如 `/story-done production/epics/core/story-damage-calculator.md`）：
直接读取该文件。

**如果没有提供参数：**

1. 检查 `production/session-state/active.md`，查找当前活动故事。
2. 若未找到，则读取 `production/sprints/` 中最近的文件，并查找标记为 IN PROGRESS 的故事。
3. 如果找到多个进行中的故事，使用 `AskUserQuestion`：
   - "我们要完成哪个故事？"
   - 选项：列出进行中的故事文件名。
4. 如果找不到任何故事，请用户提供路径。

---

## 第 2 阶段：读取故事

完整读取故事文件，并在上下文中提取并保留：

- **故事名称和 ID**
- 参考的 **GDD Requirement TR-ID(s)**（例如 `TR-combat-001`）
- 故事头部中嵌入的 **Manifest Version**（例如 `2026-03-10`）
- 参考的 **ADR**
- **Acceptance Criteria** — 完整列表（每个复选项）
- **Implementation files** — “files to create/modify” 下列出的文件
- **Story Type** — 故事头部中的 `Type:` 字段（Logic / Integration / Visual/Feel / UI / Config/Data）
- **Engine notes** — 任何注明的引擎特定约束
- **Definition of Done** — 如果存在，则读取故事级 DoD
- **Estimated vs actual scope** — 如果有记录估算

同时还要读取：
- `docs/architecture/tr-registry.yaml` — 查找故事中的每个 TR-ID。
  读取注册表条目中当前的 `requirement` 文本。这个文本才是 GDD 现行需求的权威来源——不要使用故事中可能内联引用的任何 requirement 文本（它可能已经过时）。
- 被引用的 GDD 章节 — 只读验收标准和关键规则，不要读整篇文档。用来交叉核对注册表文本是否仍然准确。
- 被引用的 ADR — 只读 Decision 和 Consequences 章节
- `docs/architecture/control-manifest.md` 头部 — 提取当前 `Manifest Version:` 日期（用于第 4 阶段的陈旧性检查）

---

## 第 3 阶段：验证验收标准

对故事中的每一条验收标准，尝试使用以下三种方式之一进行验证：

### 自动验证（无需询问即可运行）

- **文件存在检查**：对故事声明会创建的文件执行 `Glob`。
- **测试通过检查**：如果提到了测试文件路径，通过 `Bash` 运行它。
- **无硬编码值检查**：在应当放在配置文件中的 gameplay code 路径中用 `Grep` 查找数字字面量。
- **无硬编码字符串检查**：在应当放入本地化文件的 `src/` 中，用 `Grep` 查找面向玩家的字符串。
- **依赖检查**：如果某条标准写着“depends on X”，检查 X 是否存在。

### 需要确认的人工验证（使用 `AskUserQuestion`）

- 关于主观品质的标准（“手感响应良好”、“动画播放正确”）
- 关于玩法行为的标准（“当……时玩家受到伤害”、“敌人对……作出响应”）
- 性能标准（“在 Xms 内完成”）——询问是否已 profiling，或是否可按假定处理

将最多 4 个人工验证问题打包到一次 `AskUserQuestion` 调用中：

```text
question: "Does [criterion]?"
options: "Yes — passes", "No — fails", "Not tested yet"
```

### 无法验证的内容（标记但不阻塞）

- 需要完整游戏构建才能测试的标准（端到端玩法场景）
- 标记为：`DEFERRED — requires playtest session`

### 测试-标准可追踪性

完成上面的通过/失败/延后检查后，将每条验收标准映射到覆盖它的测试：

对于故事中的每一条验收标准：

1. 判断是否存在一个测试——单元、集成，或已确认的人工 playtest——直接验证这条标准？
   - **单元测试**：在 `tests/unit/` 中查找文件或函数名与该标准主题相匹配的测试（用 `Glob` 和 `Grep`）
   - **集成测试**：同样检查 `tests/integration/`
   - **人工确认**：如果上面通过 `AskUserQuestion` 验证且答案为 "Yes — passes"，则计为人工测试

2. 生成可追踪性表：

```text
| Criterion | Test | Status |
|-----------|------|--------|
| AC-1: [criterion text] | tests/unit/test_foo.gd::test_bar | COVERED |
| AC-2: [criterion text] | Manual playtest confirmation | COVERED |
| AC-3: [criterion text] | — | UNTESTED |
```

3. 应用以下升级规则：

   - 如果 **超过 50% 的标准是 UNTESTED**：升级为 **BLOCKING** — 覆盖率不足以确认故事确实完成。第 6 阶段的 verdict 不能是 COMPLETE，直到覆盖率改善。
   - 如果 **部分（≤50%）标准是 UNTESTED**：保持 ADVISORY — 不阻止完成，但必须出现在 Completion Notes 中。
   - 如果 **所有标准都被 COVERED**：除了在报告中包含该表之外，无需额外操作。

4. 对于任何 ADVISORY 的未测试标准，在第 7 阶段的 Completion Notes 中添加：
   `"Untested criteria: [AC-N list]. Recommend adding tests in a follow-up story."`

### 测试证据要求

根据第 2 阶段提取的 Story Type，检查所需证据：

| Story Type | Required Evidence | Gate Level |
|---|---|---|
| **Logic** | `tests/unit/[system]/` 中的自动化单元测试 — 必须存在且通过 | BLOCKING |
| **Integration** | `tests/integration/[system]/` 中的集成测试，或 playtest 文档 | BLOCKING |
| **Visual/Feel** | `production/qa/evidence/` 中的截图 + 签字确认 | ADVISORY |
| **UI** | `production/qa/evidence/` 中的人工走查文档或交互测试 | ADVISORY |
| **Config/Data** | `production/qa/smoke-*.md` 中的 smoke check 通过报告 | ADVISORY |

**对于 Logic stories**：先读取故事的 **Test Evidence** 小节，提取精确要求的文件路径。使用 `Glob` 检查该精确路径。如果找不到精确路径，再广泛搜索 `tests/unit/[system]/`（该文件可能放在稍微不同的位置）。如果在任一位置都找不到测试文件：
- 标记为 **BLOCKING**："Logic story has no unit test file. Story requires it at `[exact-path-from-Test-Evidence-section]`. Create and run the test before marking this story Complete."

**对于 Integration stories**：读取故事的 **Test Evidence** 小节，先查找精确要求的路径。首先用 `Glob` 检查该精确路径，然后广泛搜索 `tests/integration/[system]/`，再检查 `production/session-logs/` 中是否有引用该故事的 playtest 记录。
如果都找不到：标记为 **BLOCKING**（规则同 Logic）。

**对于 Visual/Feel 和 UI stories**：在 `production/qa/evidence/` 中 glob 查找引用该故事的文件。如果没有：标记为 **ADVISORY** —
"No manual test evidence found. Create `production/qa/evidence/[story-slug]-evidence.md` using the test-evidence template and obtain sign-off before final closure."

**对于 Config/Data stories**：检查是否存在任何 `production/qa/smoke-*.md` 文件。
如果没有：标记为 **ADVISORY** — "No smoke check report found. Run `/smoke-check`."

**如果没有设置 Story Type**：标记为 **ADVISORY** —
"Story Type not declared. Add `Type: [Logic|Integration|Visual/Feel|UI|Config/Data]` to the story header to enable test evidence gate enforcement in future stories."

任何 BLOCKING 的测试证据缺口都会阻止第 6 阶段给出 COMPLETE verdict。

---

## 第 4 阶段：检查偏差

将实现与设计文档进行对比。

自动运行这些检查：

1. **GDD 规则检查**：使用 `tr-registry.yaml` 中当前的 requirement 文本（通过故事的 TR-ID 查到），检查实现是否反映了 GDD 当前的实际需求——而不是故事编写时的需求。
   对实现文件执行 `Grep`，查找当前 GDD 章节中提到的关键函数名、数据结构或类名。

2. **Manifest 版本陈旧性检查**：将故事头部嵌入的 `Manifest Version:` 日期与当前 `docs/architecture/control-manifest.md` 头部中的 `Manifest Version:` 日期进行比较。
   - 如果一致 → 静默通过。
   - 如果故事版本更旧 → 标记为 ADVISORY：
     `ADVISORY: Story was written against manifest v[story-date]; current manifest is v[current-date]. New rules may apply. Run /story-readiness to check.`
   - 如果 `control-manifest.md` 不存在 → 跳过此检查。

3. **ADR 约束检查**：读取被引用 ADR 的 Decision 章节。检查 `docs/architecture/control-manifest.md` 中的禁止模式（如果存在）。对 ADR 明确禁止的模式执行 `Grep`。

4. **硬编码值检查**：对实现文件中的 gameplay logic 数字字面量执行 `Grep`，这些值应当放在数据文件中。

5. **范围检查**：实现是否触及了故事声明范围之外的文件？（不在 “files to create/modify” 中列出的文件）

对发现的每一项偏差，归类为：

- **BLOCKING** — 实现与 GDD 或 ADR 相冲突（在标记完成前必须修复）
- **ADVISORY** — 实现与规格存在轻微偏离，但功能等价（记录下来，由用户决定）
- **OUT OF SCOPE** — 触及了故事声明边界之外的额外文件（标记供知晓——可能是有效变更，也可能是范围蔓延）

---

## 第 4b 阶段：QA 覆盖门禁

**审查模式检查** — 在 spawn QL-TEST-COVERAGE 之前应用：
- `solo` → 跳过。说明："QL-TEST-COVERAGE skipped — Solo mode." 继续到第 5 阶段。
- `lean` → 跳过（不是 PHASE-GATE）。说明："QL-TEST-COVERAGE skipped — Lean mode." 继续到第 5 阶段。
- `full` → 正常 spawn。

完成第 4 阶段的偏差检查后，使用 gate **QL-TEST-COVERAGE**（`.claude/docs/director-gates.md`）通过 Task spawn `qa-lead`。

传入：
- 故事文件路径和故事类型
- 第 3 阶段找到的测试文件路径（精确路径，或 "none found"）
- 故事的 `## QA Test Cases` 小节（在故事创建时预写的测试规格）
- 故事的 `## Acceptance Criteria` 列表

qa-lead 会审查测试是否真正覆盖了规格内容——不仅仅是文件是否存在。

应用 verdict：
- **ADEQUATE** → 继续到第 5 阶段
- **GAPS** → 标记为 **ADVISORY**："QA lead identified coverage gaps: [list]. Story can complete but gaps should be addressed in a follow-up story."
- **INADEQUATE** → 标记为 **BLOCKING**："QA lead: critical logic is untested. Verdict cannot be COMPLETE until coverage improves. Specific gaps: [list]."

Config/Data 故事跳过此阶段（不需要代码测试）。

---

## 第 5 阶段：首席程序员代码审查门禁

**审查模式检查** — 在 spawn LP-CODE-REVIEW 之前应用：
- `solo` → 跳过。说明："LP-CODE-REVIEW skipped — Solo mode." 继续到第 6 阶段（完成报告）。
- `lean` → 跳过（不是 PHASE-GATE）。说明："LP-CODE-REVIEW skipped — Lean mode." 继续到第 6 阶段（完成报告）。
- `full` → 正常 spawn。

通过 Task 使用 gate **LP-CODE-REVIEW**（`.claude/docs/director-gates.md`）spawn `lead-programmer`。

传入：实现文件路径、故事文件路径、相关 GDD 章节、主导 ADR。

把 verdict 呈现给用户。如果是 CONCERNS，通过 `AskUserQuestion` 提示：
- 选项：`Revise flagged issues` / `Accept and proceed` / `Discuss further`
如果是 REJECT，在问题解决之前，不要进入第 6 阶段 verdict。

如果故事还没有任何实现文件（即在编码完成前运行此 verdict），则跳过此阶段并注明："LP-CODE-REVIEW skipped — no implementation files found. Run after implementation is complete."

---

## 第 6 阶段：呈现完成报告

在更新任何文件之前，先呈现完整报告：

```markdown
## Story Done: [Story Name]
**Story**: [file path]
**Date**: [today]

### Acceptance Criteria: [X/Y passing]
- [x] [Criterion 1] — auto-verified (test passes)
- [x] [Criterion 2] — confirmed
- [ ] [Criterion 3] — FAILS: [reason]
- [?] [Criterion 4] — DEFERRED: requires playtest

### Test-Criterion Traceability
| Criterion | Test | Status |
|-----------|------|--------|
| AC-1: [text] | [test file::test name] | COVERED |
| AC-2: [text] | Manual confirmation | COVERED |
| AC-3: [text] | — | UNTESTED |

### Test Evidence
**Story Type**: [Logic | Integration | Visual/Feel | UI | Config/Data | Not declared]
**Required evidence**: [unit test file | integration test or playtest | screenshot + sign-off | walkthrough doc | smoke check pass]
**Evidence found**: [YES — `[path]` | NO — BLOCKING | NO — ADVISORY]

### Deviations
[NONE] OR:
- BLOCKING: [description] — [GDD/ADR reference]
- ADVISORY: [description] — user accepted / flagged for tech debt

### Scope
[All changes within stated scope] OR:
- Extra files touched: [list] — [note whether valid or scope creep]

### Verdict: COMPLETE / COMPLETE WITH NOTES / BLOCKED
```

**Verdict definitions：**
- **COMPLETE**：所有标准通过，没有阻塞性偏差
- **COMPLETE WITH NOTES**：所有标准通过，记录了 advisory 偏差
- **BLOCKED**：存在失败标准或阻塞性偏差，必须先解决

如果 verdict 是 **BLOCKED**：不要进入第 7 阶段。列出必须修复的内容。提供帮助修复阻塞项。

---

## 第 7 阶段：更新故事状态

写入前先询问："May I update the story file to mark it Complete and log the completion notes?"

如果用户同意，编辑故事文件：

1. 更新 status 字段：`Status: Complete`
2. 在底部添加 `## Completion Notes` 小节：

```markdown
## Completion Notes
**Completed**: [date]
**Criteria**: [X/Y passing] ([any deferred items listed])
**Deviations**: [None] or [list of advisory deviations]
**Test Evidence**: [Logic: test file at path | Visual/Feel: evidence doc at path | None required (Config/Data)]
**Code Review**: [Pending / Complete / Skipped]
```

3. 如果存在 advisory 偏差，询问："Should I log these as tech debt in `docs/tech-debt-register.md`?"

4. **更新 `production/sprint-status.yaml`**（如果存在）：
   - 找到与该故事文件路径或 ID 匹配的条目
   - 设置 `status: done` 和 `completed: [today's date]`
   - 更新顶层 `updated` 字段
   - 这是静默更新——不需要额外批准（上一步已经批准）

### 会话状态更新

在更新故事文件后，静默追加到 `production/session-state/active.md`：

    ## Session Extract — /story-done [date]
    - Verdict: [COMPLETE / COMPLETE WITH NOTES / BLOCKED]
    - Story: [story file path] — [story title]
    - Tech debt logged: [N items, or "None"]
    - Next recommended: [next ready story title and path, or "None identified"]

如果 `active.md` 不存在，则用这个 block 作为初始内容创建它。
在对话中确认："Session state updated."

---

## 第 8 阶段：显示下一个故事

完成后，帮助开发者保持推进：

1. 从 `production/sprints/` 读取当前冲刺计划。
2. 找出以下故事：
   - 状态：READY 或 NOT STARTED
   - 未被其他未完成故事阻塞
   - 处于 Must Have 或 Should Have 级别

呈现：

```text
### Next Up
The following stories are ready to pick up:
1. [Story name] — [1-line description] — Est: [X hrs]
2. [Story name] — [1-line description] — Est: [X hrs]

Run `/story-readiness [path]` to confirm a story is implementation-ready
before starting.
```

如果本冲刺中已没有更多 Must Have 故事（全部都 Complete 或 Blocked）：

```text
### Sprint Close-Out Sequence

All Must Have stories are complete. QA sign-off is required before advancing.
Run these in order:

1. `/smoke-check sprint` — verify the critical path still works end-to-end
2. `/team-qa sprint` — full QA cycle: test case execution, bug triage, sign-off report
3. `/gate-check` — advance to the next phase once QA approves

Do not run `/gate-check` until `/team-qa` returns APPROVED or APPROVED WITH CONDITIONS.
```

如果还有 Should Have 故事尚未开始，则在 close-out 序列旁同时展示它们，方便用户选择：现在关闭冲刺，或先拉入更多工作。

如果没有更多 ready 的故事，但 Must Have 故事仍在进行中（尚未 Complete）：
"No more stories ready to start — [N] Must Have stories still in progress. Continue implementing those before sprint close-out."

---

## 协作协议

- **未经用户批准，绝不把故事标记为完成** — 第 7 阶段要求在编辑任何文件前获得明确的“yes”。
- **绝不自动修复失败的标准** — 报告它们，并询问如何处理。
- **偏差是事实，不是判断** — 中性地呈现；由用户决定它们是否可接受。
- **BLOCKED verdict 只是建议** — 用户可以覆盖并仍然标记完成；如果这样做，请明确记录风险。
- 对代码审查提示和批量确认人工标准时，使用 `AskUserQuestion`。

---

## 推荐下一步

- 运行 `/story-readiness [next-story-path]`，在开始前验证下一个故事是否已具备实施条件
- 如果所有 Must Have 故事都已完成：运行 `/smoke-check sprint` → `/team-qa sprint` → `/gate-check`
- 如果已记录 tech debt：通过 `/tech-debt` 持续维护登记表