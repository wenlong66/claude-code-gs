---
name: team-qa
description: "编排 QA 团队完成一整套测试流程。协调 qa-lead（策略 + 测试计划）与 qa-tester（测试用例编写 + bug 报告），为冲刺或功能产出完整的 QA 套件。涵盖：测试计划生成、测试用例编写、smoke check 门禁、人工 QA 执行以及签字确认报告。"
argument-hint: "[sprint | feature: system-name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
agent: qa-lead
---

当该技能被调用时，按结构化测试流程编排 QA 团队。

**决策点：** 在每个阶段切换时，使用 `AskUserQuestion` 呈现 subagent 的提案作为可选项。先在对话中写出 agent 的完整分析，再用简洁标签记录用户决策。
用户必须批准后才能进入下一阶段。

## 团队构成

- **qa-lead** — QA 策略、测试计划生成、故事分类、签字报告
- **qa-tester** — 测试用例编写、bug 报告编写、人工 QA 文档

## 如何委派

使用 Task 工具为每个团队成员 spawn 一个 subagent：
- `subagent_type: qa-lead` — 策略、规划、分类、签收
- `subagent_type: qa-tester` — 测试用例编写和 bug 报告编写

始终在每个 agent 的提示中提供完整上下文（故事文件路径、QA 计划路径、范围约束）。在可能的情况下，并行启动相互独立的 qa-tester 任务（例如，第 5 阶段中的多个故事可以同时搭建）。

## 流程

### 第 1 阶段：加载上下文

在做任何事之前，先收集完整范围：

1. 从参数检测当前冲刺或功能范围：
   - 如果参数是一个冲刺标识（例如 `sprint-03`）：读取 `production/sprints/[sprint]/` 中所有故事文件
   - 如果参数是 `feature: [system-name]`：glob 该系统标记下的故事文件
   - 如果没有参数：读取 `production/session-state/active.md` 和 `production/sprint-status.yaml`（如果存在）以推断当前活跃冲刺

2. 读取 `production/stage.txt` 以确认当前项目阶段。

3. 统计找到的故事数量并向用户报告：
   > "QA cycle starting for [sprint/feature]. Found [N] stories. Current stage: [stage]. Ready to begin QA strategy?"

### 第 2 阶段：QA 策略（qa-lead）

通过 Task spawn `qa-lead`，审阅所有范围内故事并产出 QA 策略。

指示 qa-lead：
- 读取每个故事文件
- 按类型分类每个故事：**Logic** / **Integration** / **Visual/Feel** / **UI** / **Config/Data**
- 识别哪些故事需要自动化测试证据，哪些需要人工 QA
- 标记任何缺少验收标准或测试证据、会阻塞 QA 的故事
- 估算人工 QA 工作量（需要多少次测试会话）
- 检查 `tests/smoke/` 中的 smoke test 场景；对每个场景，评估是否可基于当前 build 进行验证。产出 smoke check verdict：**PASS** / **PASS WITH WARNINGS [list]** / **FAIL [list of failures]**
- 产出策略摘要表和 smoke check 结果：

  | Story | Type | Automated Required | Manual Required | Blocker? |
  |-------|------|--------------------|-----------------|----------|

  **Smoke Check**: [PASS / PASS WITH WARNINGS / FAIL] — [details if not PASS]

如果 smoke check 结果是 **FAIL**，qa-lead 必须显著列出失败项。smoke check 失败时，QA 不能继续到策略阶段之后。

先向用户呈现 qa-lead 的完整策略，然后使用 `AskUserQuestion`：

```text
question: "QA Strategy Review"
options:
  - "Looks good — proceed to test plan"
  - "Adjust story types before proceeding"
  - "Skip blocked stories and proceed with the rest"
  - "Smoke check failed — fix issues and re-run /team-qa"
  - "Cancel — resolve blockers first"
```

如果 smoke check **FAIL**：不要继续到第 3 阶段。将失败项呈现出来并停止。用户必须修复后重新运行 `/team-qa`。
如果 smoke check 是 **PASS WITH WARNINGS**：在签字报告中注明这些警告，然后继续。
如果存在阻塞项：明确列出。用户可以选择跳过被阻塞的故事，或者取消本次流程。

### 第 3 阶段：生成测试计划

基于第 2 阶段的策略，生成结构化测试计划文档。

测试计划应覆盖：
- **Scope**：冲刺/功能名称、故事数量、日期
- **Story Classification Table**：来自第 2 阶段策略
- **Automated Test Requirements**：哪些故事需要测试文件，`tests/` 中的预期路径
- **Manual QA Scope**：哪些故事需要人工走查，以及要验证什么
- **Out of Scope**：本轮明确不测什么，以及原因
- **Entry Criteria**：QA 开始前必须满足什么（smoke check 通过、build 稳定）
- **Exit Criteria**：什么算完成了 QA 周期（所有故事 PASS，或 FAIL 但已提交 bug）

询问："May I write the QA plan to `production/qa/qa-plan-[sprint]-[date].md`?"

只有收到批准后才写入。

### 第 4 阶段：测试用例编写（qa-tester）

> **Smoke check** 在第 2 阶段（QA Strategy）中执行。如果第 2 阶段的 smoke check 返回 FAIL，则流程在那里就已停止。此阶段仅在第 2 阶段 smoke check 为 PASS 或 PASS WITH WARNINGS 时运行。

对每个需要人工 QA 的故事（Visual/Feel、UI、没有自动化测试的 Integration）：

通过 Task 为每个故事 spawn `qa-tester`（在可能的情况下并行），并提供：
- 故事文件路径
- QA 计划中与该故事相关的部分
- 被测试系统的 GDD 验收标准（如果可用）
- 要求编写覆盖所有验收标准的详细测试用例

每组测试用例都应包含：
- **Preconditions**：测试开始前所需的游戏状态
- **Steps**：编号、无歧义的操作步骤
- **Expected Result**：应该发生什么
- **Actual Result**：留空给测试者填写
- **Pass/Fail**：留空

在人工执行前，先将测试用例提供给用户审阅。按故事分组展示。

对每个故事组（每次批量 3-4 个）使用 `AskUserQuestion`：

```text
question: "Test cases ready for [Story Group]. Review before manual QA begins?"
options:
  - "Approved — begin manual QA for these stories"
  - "Revise test cases for [story name]"
  - "Skip manual QA for [story name] — not ready"
```

### 第 6 阶段：人工 QA 执行

逐个走查已批准的人工 QA 列表中的故事。

将故事按 3-4 个为一组，并对每组使用 `AskUserQuestion`：

```text
question: "Manual QA — [Story Title]\n[brief description of what to test]"
options:
  - "PASS — all acceptance criteria verified"
  - "PASS WITH NOTES — minor issues found (describe after)"
  - "FAIL — criteria not met (describe after)"
  - "BLOCKED — cannot test yet (reason)"
```

每次得到 FAIL 后：使用 `AskUserQuestion` 收集失败说明，然后通过 Task spawn `qa-tester`，在 `production/qa/bugs/` 中撰写正式 bug 报告。

Bug report 命名：`BUG-[NNN]-[short-slug].md`（从目录中现有 bug 递增 NNN）。

收集完所有结果后，总结：
- Stories PASS: [count]
- Stories PASS WITH NOTES: [count]
- Stories FAIL: [count] — bugs filed: [IDs]
- Stories BLOCKED: [count]

### 第 7 阶段：QA 签收报告

通过 Task spawn `qa-lead`，使用第 4-6 阶段的所有结果生成签收报告。

签收报告格式：

```markdown
## QA Sign-Off Report: [Sprint/Feature]
**Date**: [date]
**QA Lead sign-off**: [pending]

### Test Coverage Summary
| Story | Type | Auto Test | Manual QA | Result |
|-------|------|-----------|-----------|--------|
| [title] | Logic | PASS | — | PASS |
| [title] | Visual | — | PASS | PASS |

### Bugs Found
| ID | Story | Severity | Status |
|----|-------|----------|--------|
| BUG-001 | [story] | S2 | Open |

### Verdict: APPROVED / APPROVED WITH CONDITIONS / NOT APPROVED

**Conditions** (if any): [list what must be fixed before the build advances]

### Next Step
[guidance based on verdict]
```

Verdict 规则：
- **APPROVED**：所有故事 PASS 或 PASS WITH NOTES；没有打开的 S1/S2 bug
- **APPROVED WITH CONDITIONS**：有打开的 S3/S4 bug，或记录了 PASS WITH NOTES 问题；没有 S1/S2 bug
- **NOT APPROVED**：有任何打开的 S1/S2 bug；或者故事 FAIL 但没有记录的临时方案

按 verdict 给出下一步指引：
- APPROVED: "Build is ready for the next phase. Run `/gate-check` to validate advancement."
- APPROVED WITH CONDITIONS: "Resolve conditions before advancing. S3/S4 bugs may be deferred to polish."
- NOT APPROVED: "Resolve S1/S2 bugs and re-run `/team-qa` or targeted manual QA before advancing."

询问："May I write this QA sign-off report to `production/qa/qa-signoff-[sprint]-[date].md`?"

只有收到批准后才写入。

## 错误恢复协议

如果任何通过 Task spawn 的 agent 返回 BLOCKED、出错或无法完成：

1. **立即呈现**：在继续后续阶段之前，向用户报告 "[AgentName]: BLOCKED — [reason]"
2. **评估依赖**：检查被阻塞 agent 的输出是否是后续阶段所必需。如果是，则在没有用户输入前不要继续到该依赖点之后。
3. **提供选项** 通过 AskUserQuestion：
   - 跳过该 agent，并在最终报告中注明缺口
   - 用更窄的范围重试
   - 先停止并解决该阻塞
4. **始终产出部分报告** —— 输出已完成的内容。绝不要因为一个 agent 阻塞就丢弃工作。

常见阻塞：
- 输入文件缺失（故事找不到、GDD 缺失）→ 重定向到创建它的技能
- ADR 状态为 Proposed → 不要实现；先运行 `/architecture-decision`
- 范围过大 → 通过 `/create-stories` 拆成两个故事
- ADR 与故事之间有冲突指令 → 呈现冲突，不要猜测

## 输出

总结应覆盖：范围内的故事、smoke check 结果、人工 QA 结果、提交的 bug（含 ID 和严重性），以及最终 APPROVED / APPROVED WITH CONDITIONS / NOT APPROVED verdict。

Verdict: **COMPLETE** — QA 周期完成。
Verdict: **BLOCKED** — smoke check 失败，或关键阻塞导致流程无法完成；已产出部分报告。