---
name: test-flakiness
description: "通过读取 CI 运行日志或测试结果历史来检测非确定性（flaky）测试。汇总每个测试的通过率，识别间歇性失败，建议隔离或修复，并维护 flaky test 登记表。最好在 Polish 阶段或多次 CI 运行后执行。"
argument-hint: "[ci-log-path | scan | registry]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# 测试不稳定性检测

Flaky test 是指在没有代码变更的情况下，有时通过、有时失败的测试。某些方面上，flaky test 比没有测试更糟——它会训练团队忽略红色 CI 运行，从而掩盖真正的失败。此技能会识别这些测试，解释可能原因，并建议是隔离还是修复。

**输出：** 更新后的 `tests/regression-suite.md` 隔离部分 + 可选的 `production/qa/flakiness-report-[date].md`

**运行时机：**
- Polish 阶段（测试已经运行多次；统计信号较可靠）
- 当开发者开始把 CI 失败说成“可能只是 flaky”时
- 在 `/regression-suite` 标识出需要诊断的隔离测试之后

---

## 1. 解析参数

**模式：**
- `/test-flakiness [ci-log-path]` — 分析一个特定的 CI 运行日志文件
- `/test-flakiness scan` — 扫描 `.github/` 或标准日志输出目录中所有可用的 CI 日志
- `/test-flakiness registry` — 读取 `regression-suite.md` 中现有的 quarantine 部分，并为已经知道的 flaky tests 提供修复建议
- 无参数 — 自动检测：如果 CI 日志可访问则运行 `scan`，否则运行 `registry`

---

## 2. 定位 CI 日志数据

### 选项 A — GitHub Actions（优先）

检查测试结果 artifact：
```bash
ls -t .github/ 2>/dev/null
ls -t test-results/ 2>/dev/null
```

对于 Godot 项目：GdUnit4 输出与 JUnit 格式兼容的 XML 结果。
检查 `test-results/` 中的 `.xml` 文件。

对于 Unity 项目：game-ci test runner 默认输出 NUnit XML 到 `test-results/`。

对于 Unreal 项目：自动化日志输出到 `Saved/Logs/`。用 Grep 查找 `Result: Success` 和 `Result: Fail` 模式。

### 选项 B — 本地日志文件

如果提供了路径参数，则直接读取该文件。

### 选项 C — 没有可用日志数据

如果找不到日志：
> "No CI log data found. To detect flaky tests, this skill needs test result history from multiple runs. Options:
> 1. Run the test suite at least 3 times and collect the output logs
> 2. Check CI pipeline output and save a log to `test-results/`
> 3. Run `/test-flakiness registry` to review tests already flagged as flaky
>    in `tests/regression-suite.md`"

停止并询问用户想采用哪个选项。

---

## 3. 解析测试结果

对找到的每个 CI 日志或结果文件，解析：

**JUnit XML 格式**（GdUnit4 / Unity）：
- Grep `<testcase name=` 获取测试名
- Grep `<failure` 或 `<error` 识别失败
- 解析 `classname` 和 `name` 属性，获得完整测试标识符

**纯文本日志**：
- Grep 通过/失败模式：
  - Godot：测试名旁的 `PASSED` / `FAILED`
  - Unreal：`Result: Success` / `Result: Fail`
  - Unity：`Test passed` / `Test failed`

建立表：`test_id → [run1_result, run2_result, run3_result, ...]`

---

## 4. 识别 Flaky Tests

如果某个测试在多个运行的结果历史中同时出现 PASS 和 FAIL，且中间没有代码变更，则它是 **flaky**。

Flakiness 阈值：
- **High flakiness**：在超过 25% 的运行中失败 — 立即 quarantine
- **Moderate flakiness**：在 5–25% 的运行中失败 — 尽快调查并修复
- **Low/suspected flakiness**：在 1–5% 的运行中失败 — 持续观察；可能只是罕见故障

对每个 flaky test，分类可能原因：

### 原因分类

| Cause | 症状 | 修复方向 |
|-------|------|----------|
| **Timing / async** | 在等待信号或计时器后失败；通过率与系统负载相关 | 添加显式 await/同步；避免基于时间的延迟 |
| **Order dependency** | 在特定其他测试之后运行时失败；单独运行时通过 | 添加正确的 setup/teardown；确保测试隔离 |
| **Random seed** | 无规律地间歇失败；涉及 RNG | 提供显式 seed；不要在测试中使用 `randf()` |
| **Resource leak** | 在测试运行后期更容易失败 | 修复 teardown 清理；检查孤立节点（Godot）或对象释放（Unity） |
| **External state** | 当某个文件、场景或全局状态来自前一个测试时失败 | 将测试与文件系统隔离；使用内存 mock |
| **Floating point** | 在 `== 0.5` 之类的比较上失败 | 使用 epsilon 比较（`is_equal_approx`、`Assert.AreApproximately`） |
| **Scene/prefab load race** | 场景尚未 ready 时失败 | 实例化后等待一帧；使用 `await get_tree().process_frame` |

用 Grep 检查测试文件中的计时调用、randf、全局状态访问或浮点相等比较，以缩小原因范围。

---

## 5. 建议动作

对于每个 flaky test：

**隔离（High flakiness）：**
> "Quarantine this test immediately. Disable it in CI by adding
> `@pytest.mark.skip` / `[Ignore]` / `GdUnitSkip` annotation. Log it in
> `tests/regression-suite.md` quarantine section. The test is now opt-in only.
> Fix the root cause before removing quarantine."

**调查并尽快修复（Moderate）：**
> "This test is intermittently unreliable. Root cause appears to be [cause].
> Suggested fix: [specific fix based on cause classification]. Do not quarantine
> yet — fix the test directly."

**观察（Low/suspected）：**
> "This test shows suspected flakiness. Collect more run data before
> quarantining. Note it as 'suspected' in the regression suite."

---

## 6. 生成报告

### 对话内摘要

```text
## Flakiness Detection Results

**Runs analysed**: [N]
**Tests tracked**: [N]

### Flaky Tests Found

| Test | System | Fail Rate | Likely Cause | Recommendation |
|------|--------|-----------|--------------|----------------|
| [test_name] | [system] | [N]% | Timing | Quarantine + fix async |
| [test_name] | [system] | [N]% | Float comparison | Fix: use epsilon compare |
| [test_name] | [system] | [N]% | Order dependency | Investigate teardown |

### Clean Tests (no flakiness detected)

[N] tests ran across [N] runs with consistent results — no flakiness detected.

### Data Limitations

[如果可用运行次数少于 5 次，注明——运行次数越少，统计置信度越低]
```

---

## 7. 更新 Regression Suite + 可选报告文件

询问："May I update the quarantine section of `tests/regression-suite.md` with the flaky tests found?"

如果同意：使用 `Edit` 将条目追加到 Quarantined Tests 表中。
绝不要删除现有 quarantine 条目——只新增。

另行询问："May I write a full flakiness report to `production/qa/flakiness-report-[date].md`?"

完整报告包括每个测试的分析、原因细节和引擎特定的修复片段。

写入后：

- 对于每个被 quarantine 的测试："Add the engine-specific skip annotation to disable this test in CI. Re-enable after the root cause is fixed."
- 对于可直接修复的测试："The fix for [test] is straightforward — change the equality comparison on line [N] to use `is_equal_approx`."
- 摘要："Once all quarantine annotations are applied, CI should run green. Schedule fix work for the [N] quarantined tests before the release gate."

---

## 协作协议

- **永远不要删除测试文件**——quarantine 的意思是注释 + 列表，不是移除
- **统计置信度很重要**——少于 3 次运行时，将发现标记为 "suspected" 而不是 "confirmed"；询问是否有更多运行数据
- **目标始终是修复**——即使建议 quarantine，也要给出修复方向
- **写入前先询问**——更新 regression-suite 和报告文件都需要明确批准。写入时：Verdict: **COMPLETE** — flakiness report written. 如果用户拒绝：Verdict: **BLOCKED** — user declined write.
- **CI 中的 flakiness 是团队问题**——清楚呈现列表和建议动作；不要在团队不知情的情况下悄悄 quarantine