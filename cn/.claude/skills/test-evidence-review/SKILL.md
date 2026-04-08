---
name: test-evidence-review
description: "对测试文件和人工证据文档进行质量审查。不只是检查是否存在——还会评估断言覆盖、边界情况处理、命名规范和证据完整性。为每个故事产出 ADEQUATE/INCOMPLETE/MISSING verdict。可在 QA 签收前或按需运行。"
argument-hint: "[story-path | sprint | system-name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
---

# 测试证据审查

`/smoke-check` 只验证测试文件**存在**且**通过**。此技能更进一步——它审查这些测试和证据文档的**质量**。即使测试文件存在并通过，也可能仍然遗漏关键行为。人工证据文档即使存在，也可能缺少关闭所需的签字确认。

**输出：** 口头摘要报告 + 可选的 `production/qa/evidence-review-[date].md`

**运行时机：**
- 在 QA 交接签收前（`/team-qa` 第 5 阶段）
- 任何测试质量存疑的故事上
- 作为里程碑评审的一部分，用于 Logic 和 Integration 故事质量审计

---

## 1. 解析参数

**模式：**
- `/test-evidence-review [story-path]` — 审查单个故事的证据
- `/test-evidence-review sprint` — 审查当前冲刺中的所有故事
- `/test-evidence-review [system-name]` — 审查某个 epic/system 下的所有故事
- 无参数 — 询问范围："Single story"、"Current sprint"、"A system"

---

## 2. 载入范围内故事

根据参数：

**单故事**：直接读取故事文件。提取：Story Type、Test Evidence 小节、story slug、system name。

**冲刺**：读取 `production/sprints/` 中最近修改的文件。提取冲刺计划中的故事文件路径列表。读取每个故事文件。

**系统**：glob `production/epics/[system-name]/story-*.md`。逐个读取。

对每个故事，收集：
- `Type:` 字段（Logic / Integration / Visual/Feel / UI / Config/Data）
- `## Test Evidence` 小节——声明的预期测试文件路径或证据文档
- Story slug（来自文件名）
- System name（来自目录路径）
- Acceptance Criteria 列表（所有复选项）

---

## 3. 定位证据文件

对每个故事，找到对应证据：

**Logic stories**：Glob `tests/unit/[system]/[story-slug]_test.*`
  - 如果没找到，也尝试：在 `tests/unit/[system]/` 中 Grep 包含该 story slug 的文件

**Integration stories**：Glob `tests/integration/[system]/[story-slug]_test.*`
  - 也检查 `production/session-logs/` 中是否有提到该故事的 playtest 记录

**Visual/Feel 和 UI stories**：Glob `production/qa/evidence/[story-slug]-evidence.*`

**Config/Data stories**：Glob `production/qa/smoke-*.md`（任意 smoke check 报告）

记录每个故事找到的内容（路径）或未找到的内容（缺口）。

---

## 4. 评审自动化测试质量（Logic / Integration）

对找到的每个测试文件进行读取并评估：

### 断言覆盖

统计不同断言的数量（包含 assert、expect、check、verify 或引擎特定断言模式的行）。断言数量过少是质量信号——一个测试函数如果只做 1 次断言，可能无法覆盖预期行为的范围。

阈值：
- **每个测试函数 3+ 个断言** → 正常
- **每个测试函数 1-2 个断言** → 记为可能偏薄
- **0 个断言**（测试存在但没有 asserts）→ 标记为 BLOCKING —— 这个测试空洞通过，不能证明任何内容

### 边界情况覆盖

对于故事中任何包含数字、阈值或 “when X happens” 条件的验收标准：检查测试函数名或测试内容是否引用了该具体场景。

启发式：
- 在测试文件中 Grep “zero”、“max”、“null”、“empty”、“min”、“invalid”、“boundary”、“edge”——出现任一项都是积极信号
- 如果故事有 Formulas 小节且有具体边界：检查测试是否覆盖最小/最大值

### 命名质量

测试函数名应描述：场景 + 期望结果。
模式：`test_[scenario]_[expected_outcome]`

将泛泛命名（如 `test_1`、`test_run`、`testBasic`）标记为 **naming issues** —— 它们会让故障排查更困难。

### 公式可追踪性

对于带有 Formulas 小节的 Logic 故事：检查测试文件中至少有一个测试，其名称或注释引用了公式名称或公式值。测试若验证了公式却没有点名，会在公式变更时更难维护。

---

## 5. 评审人工证据质量（Visual/Feel / UI）

对找到的每份证据文档进行读取并评估：

### 标准关联

证据文档应引用故事中的每条验收标准。
检查：证据文档是否包含每条标准（或清晰改写）。缺失标准意味着某条标准从未被验证。

### 签字完整性

检查是否存在三条签字线（或等效字段）：
- Developer sign-off
- Designer / art-lead sign-off（用于 Visual/Feel）
- QA lead sign-off

如果任意一项缺失或为空：标记为 INCOMPLETE —— 没有全部必需签字，故事不能完全关闭。

### 截图 / 产物完整性

对于 Visual/Feel 故事：检查证据文档中是否引用了截图文件路径。如果有引用，再用 Glob 确认这些文件存在。

对于 UI 故事：检查是否存在走查序列（逐步交互日志）。

### 日期覆盖

证据文档应有日期。如果日期早于故事的最近一次重大变更（启发式：与冲刺开始日期比较），标记为 POTENTIALLY STALE —— 证据可能没有覆盖最终实现。

---

## 6. 构建审查报告

为每个故事分配一个 verdict：

| Verdict | 含义 |
|---------|------|
| **ADEQUATE** | 测试/证据存在，通过质量检查，覆盖了所有标准 |
| **INCOMPLETE** | 测试/证据存在，但有质量缺口（断言太少、缺少签字等） |
| **MISSING** | 对需要证据的故事类型，没有找到任何测试或证据 |

整体冲刺/系统 verdict 取所有故事 verdict 中最差的那个。

```markdown
## Test Evidence Review

> **Date**: [date]
> **Scope**: [single story path | Sprint [N] | [system name]]
> **Stories reviewed**: [N]
> **Overall verdict**: ADEQUATE / INCOMPLETE / MISSING

---

### Story-by-Story Results

#### [Story Title] — [Type] — [ADEQUATE/INCOMPLETE/MISSING]

**Test/evidence path**: `[path]` (found) / (not found)

**Automated test quality** *(Logic/Integration only)*:
- Assertion coverage: [N per function on average] — [adequate / thin / none]
- Edge cases: [covered / partial / not found]
- Naming: [consistent / [N] generic names flagged]
- Formula traceability: [yes / no — formula names not referenced in tests]

**Manual evidence quality** *(Visual/Feel/UI only)*:
- Criterion linkage: [N/M criteria referenced]
- Sign-offs: [Developer ✓ | Designer ✗ | QA Lead ✗]
- Artefacts: [screenshots present / missing / N/A]
- Freshness: [dated [date] — current / potentially stale]

**Issues**:
- BLOCKING: [description] *(prevents story-done)*
- ADVISORY: [description] *(should fix before release)*

---

### Summary

| Story | Type | Verdict | Issues |
|-------|------|---------|--------|
| [title] | Logic | ADEQUATE | None |
| [title] | Integration | INCOMPLETE | Thin assertions (avg 1.2/function) |
| [title] | Visual/Feel | INCOMPLETE | QA lead sign-off missing |
| [title] | Logic | MISSING | No test file found |

**BLOCKING items** (must resolve before story can be closed): [N]
**ADVISORY items** (should address before release): [N]
```

---

## 7. 写出输出（可选）

在对话中呈现报告。

询问："May I write this test evidence review to `production/qa/evidence-review-[date].md`?"

这是可选的——报告本身已经足够单独使用。只有用户希望保留记录时才写入。

报告之后：

- 对于 BLOCKING 项："These must be resolved before `/story-done` can mark the story Complete. Would you like to address any of them now?"
- 对于断言偏薄："Consider running `/test-helpers [system]` to see scaffolded assertion patterns for common cases."
- 对于缺少签字："Manual sign-off is required from [role]. Share `[evidence-path]` with them to complete sign-off."

Verdict: **COMPLETE** — evidence review finished. If found BLOCKING items, use CONCERNS。

---

## 协作协议

- **报告质量问题，不修复它们**——此技能只负责读取和评估，不修改测试文件或证据文档
- **ADEQUATE 意味着足以发布，不是完美**——避免对已能正常工作、且足够全面的测试吹毛求疵
- **BLOCKING 与 ADVISORY 的区分很重要**——只有当缺口让故事某条标准确实未被验证时，才标记 BLOCKING
- **写入前先询问**——报告文件是可选的；写入前必须先确认