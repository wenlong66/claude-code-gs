---
name: regression-suite
description: "将测试覆盖映射到 GDD 关键路径，识别没有回归测试的已修复 bug，标记新功能带来的覆盖漂移，并维护 tests/regression-suite.md。修复 bug 后或在 release gate 前运行。"
argument-hint: "[update | audit | report]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Regression Suite

这个技能确保每个 bug 修复都伴随一个本应能抓到原始 bug 的测试——并且随着游戏演进，回归测试套件保持最新。它也能检测是否有新功能被加入，但没有对应的回归覆盖。

回归测试套件不是新的测试类别——它是 `tests/` 中**已存在测试的精选清单**，这些测试共同覆盖游戏关键路径和已知故障点。这个技能负责维护那份清单。

**输出：** `tests/regression-suite.md`

**何时运行：**
- 修复 bug 之后（确认是否写了回归测试，或识别缺口）
- 在 release gate 之前（`/gate-check polish` 需要存在 regression suite）
- 作为 sprint 收尾的一部分，检测覆盖漂移

---

## 1. 解析参数

**模式：**
- `/regression-suite update` —— 扫描本 sprint 中新的 bug 修复，并检查是否有回归测试；把新测试加入 suite manifest
- `/regression-suite audit` —— 对所有 GDD 关键路径与现有测试覆盖做完整审计；标记没有回归测试的路径
- `/regression-suite report` —— 只读状态报告（不写入）；适合 sprint review
- 无参数 —— 如果有活跃 sprint，则运行 `update`；否则运行 `audit`

---

## 2. 加载上下文

### Step 2a —— 加载现有 regression suite

如果存在，读取 `tests/regression-suite.md`。提取：
- 已注册的 regression tests 总数
- 最后更新日期
- 任何标记为 `STALE` 或 `QUARANTINED` 的测试

如果不存在：记录 "No regression suite found — will create one."

### Step 2b —— 加载测试库存

Glob 所有测试文件：
```
tests/unit/**/*_test.*
tests/integration/**/*_test.*
tests/regression/**/*
```

对每个文件，记录系统（来自目录路径）和文件名。
除非需要用于名字到测试的映射，否则不要读取测试文件内容。

### Step 2c —— 加载 GDD 关键路径

对于 `audit` 模式：读取 `design/gdd/systems-index.md` 获取所有系统。
对每个 MVP-tier 系统，读取其 GDD 并提取：
- Acceptance Criteria（它们定义关键路径）
- Formulas 章节（公式必须有回归测试）
- Edge Cases 章节（已知边界情况应该有回归测试）

对于 `update` 模式：跳过完整 GDD 扫描。改为读取当前 sprint plan 和 story 文件，找出本 sprint 中 `Status: Complete` 的 stories。

### Step 2d —— 加载已关闭 bug

Glob `production/qa/bugs/*.md`，筛选带有 `Status: Closed` 或 `Status: Fixed` 字段的 bugs。记录：
- 该 bug 属于哪个 story 或系统
- 修复说明中是否提到了回归测试

---

## 3. 映射覆盖 —— 关键路径

仅在 `audit` 模式下：

对每条 GDD acceptance criterion，判断是否存在测试：

1. Grep `tests/unit/[system]/` 和 `tests/integration/[system]/` 中与该 criterion 关键名词/动词相关的文件名和函数名
2. 指定覆盖状态：

| Status | Meaning |
|--------|---------|
| **COVERED** | 存在一个测试文件，针对该 criterion 的逻辑 |
| **PARTIAL** | 存在测试，但没有覆盖所有情况（例如只有 happy path） |
| **MISSING** | 没有找到该关键路径的测试 |
| **EXEMPT** | Visual/Feel 或 UI criterion —— 按设计不可自动化 |

3. 将与公式或状态机对应的 MISSING 项提升为 **HIGH PRIORITY** gap——这是最容易产生回归的地方。

---

## 4. 映射覆盖 —— 已修复 bug

对每个已关闭的 bug：

1. 从 bug metadata 中提取 system slug
2. 在 `tests/unit/[system]/` 和 `tests/integration/[system]/` 中 Grep 一个引用了 bug ID 或特定失败场景的测试
3. 指定：
   - **HAS REGRESSION TEST** —— 找到了能抓住该 bug 的测试
   - **MISSING REGRESSION TEST** —— bug 已修复，但没有测试防止其再次出现

对于 MISSING REGRESSION TEST 项：
- 将其标记为 regression gap
- 建议测试文件路径：`tests/unit/[system]/[bug-slug]_regression_test.[ext]`
- 注明："Without this test, this bug can silently return in a future sprint."

---

## 5. 检测覆盖漂移

覆盖漂移是指游戏在增长，但 regression suite 没有同步增长。

检查漂移指标：
- 本 sprint 完成的 stories 没有对应的测试文件出现在 `tests/`
- `systems-index.md` 中自上次 regression-suite 更新以来新增的系统
- regression suite 上次更新后新增或修订的 GDD 章节（如果有文件修改提示，则用 Grep；否则询问用户）
- `tests/regression-suite.md` 的 last-updated 日期与当前日期相比——如果间隔 > 2 个 sprint，则标记为可能过时

---

## 6. 生成报告和 suite manifest

### 报告格式（在对话中）

```
## Regression Suite Status

**Mode**: [update | audit | report]
**Existing registered tests**: [N]
**Test files scanned**: [N]

### Critical Path Coverage (audit mode only)
| System | Total ACs | Covered | Partial | Missing | Exempt |
|--------|-----------|---------|---------|---------|--------|
| [name] | [N] | [N] | [N] | [N] | [N] |

**Coverage rate (non-exempt)**: [N]%

### Bug Regression Coverage
| Bug ID | System | Severity | Has Regression Test? |
|--------|--------|----------|----------------------|
| BUG-NNN | [system] | S[N] | YES / NO ⚠ |

**Bugs without regression tests**: [N]

### Coverage Drift Indicators
[List new systems or stories with no test coverage, or "None detected."]

### Recommended New Regression Tests
| Priority | System | Suggested Test File | Covers |
|----------|--------|---------------------|--------|
| HIGH | [system] | `tests/unit/[system]/[slug]_regression_test.[ext]` | BUG-NNN / AC-[N] |
| MEDIUM | [system] | `tests/unit/[system]/[slug]_test.[ext]` | [criterion] |
```

### Suite manifest 格式（`tests/regression-suite.md`）

该 manifest 是精选索引——不是测试本身，而是一个注册表，列出哪些测试在 release 前必须始终通过：

```markdown
# Regression Suite Manifest

> Last Updated: [date]
> Total registered tests: [N]
> Coverage: [N]% of GDD critical paths

## How to run

[Engine-specific command to run all regression tests]

## Registered Regression Tests

### [System Name]

| Test File | Test Function (if known) | Covers | Added |
|-----------|--------------------------|--------|-------|
| `tests/unit/[system]/[file]_test.[ext]` | `test_[scenario]` | AC-N / BUG-NNN | [date] |

## Known Gaps

Tests that should exist but don't yet:

| Priority | System | Suggested Path | Covers | Reason Not Yet Written |
|----------|--------|----------------|--------|------------------------|
| HIGH | [system] | `tests/unit/[system]/[path]` | BUG-NNN | Bug fixed without test |

## Quarantined Tests

Tests that are flaky or disabled (do not run in CI):

| Test File | Function | Reason | Quarantined Since |
|-----------|----------|--------|-------------------|
| (none) | | | |
```

---

## 7. 写出输出

询问："May I write/update `tests/regression-suite.md` with the current regression suite manifest?"

对于 `update` 模式：追加新条目；永远不要删除已有条目（使用带定点插入的 `Edit`）。
对于 `audit` 模式：用更新后的覆盖数据重写完整 manifest。
对于 `report` 模式：不要写任何内容。

写入后（如果获批）：

- 对每个 HIGH priority gap："Consider creating the missing regression test before the next sprint. Run `/test-helpers` to scaffold the test file."
- 如果 bug regression gaps > 0："These bugs can silently return without regression tests. The next sprint should include a story to write the missing tests."
- 如果检测到覆盖漂移："Regression suite may be drifting. Consider running `/regression-suite audit` at the next sprint boundary."

Verdict: **COMPLETE** — regression suite updated.（如果用户拒绝写入：Verdict: **BLOCKED**。）

---

## 协作协议

- **不要在未获明确批准时移除 manifest 中已有的 regression tests**——删除一个本来有意写下的测试本身就是回归风险
- **Gap 只是建议，不是阻断**——清晰展示，但不要阻止其他工作继续（release gate 需要 regression suite 的情况除外）
- **Quarantine 不是删除**——间歇性失败的测试应该 quarantine（写入 manifest），但不要移除；应由 `/test-flakiness` 修复
- **写入前先询问**——创建或更新 manifest 前始终确认
