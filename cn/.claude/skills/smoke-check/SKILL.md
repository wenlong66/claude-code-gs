---
name: smoke-check
description: "在交给 QA 前运行关键路径 smoke test gate。执行自动化测试套件，验证核心功能，并输出 PASS/FAIL 报告。应在 sprint 的 stories 实现完成后、人工 QA 开始前运行。smoke check 失败意味着构建还不适合交给 QA。"
argument-hint: "[sprint | quick | --platform pc|console|mobile|all]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, AskUserQuestion
---

# Smoke Check

这个技能是“实现完成”和“准备交给 QA”之间的 gate。它会运行自动化测试套件，检查测试覆盖缺口，与开发者一起批量验证关键路径，并输出 PASS/FAIL 报告。

规则很简单：**smoke check 失败的构建不能交给 QA。** 把坏构建交给 QA 会浪费他们的时间，也会打击团队士气。

**输出：** `production/qa/smoke-[date].md`

---

## 解析参数

参数可以组合：`/smoke-check sprint --platform console`

**基础模式**（第一个参数，默认：`sprint`）：
- `sprint` —— 针对当前 sprint 的 stories 做完整 smoke check
- `quick` —— 跳过覆盖扫描（Phase 3）和 Batch 3；适合快速复查

**平台标志**（`--platform`，默认：无）：
- `--platform pc` —— 增加 PC 专属检查（键盘、鼠标、窗口模式）
- `--platform console` —— 增加主机专属检查（手柄、TV safe zones、平台认证要求）
- `--platform mobile` —— 增加移动端专属检查（触控、竖屏/横屏、电池/温度行为）
- `--platform all` —— 增加所有平台变体；输出按平台的 verdict 表

如果提供了 `--platform`，Phase 4 会增加平台特定的 batches，Phase 5 会在总体裁定之外再输出按平台的 verdict 表。

---

## 第 1 阶段：检测测试设置

在运行任何东西之前，先了解环境：

1. **测试框架检查**：确认 `tests/` 目录存在。
   如果不存在：“No test directory found at `tests/`. Run `/test-setup`
   to scaffold the testing infrastructure, or create the directory manually
   if tests live elsewhere.” 然后停止。

2. **CI 检查**：检查 `.github/workflows/` 是否包含引用测试的 workflow 文件。
   在报告中注明是否已配置 CI。

3. **引擎检测**：读取 `.claude/docs/technical-preferences.md`，提取 `Engine:` 值。
   把它存起来，用于 Phase 2 的测试命令选择。

4. **Smoke test 列表**：检查是否存在 `production/qa/smoke-tests.md` 或 `tests/smoke/`。
   如果找到了 smoke test 列表，在 Phase 4 中使用它。如果两者都不存在，smoke tests 将从当前 QA plan 中提取（Phase 4 fallback）。

5. **QA plan 检查**：glob `production/qa/qa-plan-*.md`，取最近修改的文件。如果找到，记录路径——它会在 Phase 3 和 Phase 4 中使用。如果没找到，记录："No QA plan found. Run `/qa-plan sprint` before smoke-checking for best results."

先报告这些发现，再继续：“Environment: [engine]. Test directory: [found / not found]. CI configured: [yes / no]. QA plan: [path / not found].”

---

## 第 2 阶段：运行自动化测试

尝试通过 Bash 运行测试套件。根据 Phase 1 中检测到的引擎选择命令：

**Godot 4：**
```bash
godot --headless --script tests/gdunit4_runner.gd 2>&1
```
如果该路径下没有 GDUnit4 runner script，尝试：
```bash
godot --headless -s addons/gdunit4/GdUnitRunner.gd 2>&1
```
如果两个路径都不存在，记录：“GDUnit4 runner not found — confirm the runner path for your test framework.”

**Unity：**
Unity tests 需要编辑器，在大多数环境下不能通过 shell 头less 运行。检查最近的测试结果工件：
```bash
ls -t test-results/ 2>/dev/null | head -5
```
如果存在测试结果文件（XML 或 JSON），读取最新的一份并解析 PASS/FAIL 数量。如果没有工件："Unity tests must be run from the editor or CI pipeline. Please confirm test status manually before proceeding."

**Unreal Engine：**
```bash
ls -t Saved/Logs/ 2>/dev/null | grep -i "test\|automation" | head -5
```
如果没有匹配日志："UE automation tests must be run via the Session Frontend or CI pipeline. Please confirm test status manually."

**未知引擎 / 未配置：**
"Engine not configured in `.claude/docs/technical-preferences.md`. Run
`/setup-engine` to specify the engine, then re-run `/smoke-check`."

**如果本环境无法运行测试 runner**（引擎 binary 不在 PATH、runner script 找不到等），请清楚报告：

"Automated tests could not be executed — engine binary not found on PATH.
Status will be recorded as NOT RUN. Confirm test results from your local IDE
or CI pipeline. Unconfirmed NOT RUN is treated as PASS WITH WARNINGS, not
FAIL — the developer must manually confirm results."

不要把 NOT RUN 当作自动 FAIL。把它记录为 warning。开发者在 Phase 4 的人工确认可以消除它。

解析 runner 输出并提取：
- 总测试数
- 通过数
- 失败数
- 任何失败测试的名称（最多 10 个；如果更多，记数量）
- runner 本身输出的任何 crash 或 error 信息

---

## 第 3 阶段：检查测试覆盖

按以下优先级获取 story 列表：
1. Phase 1 找到的 QA plan（其 Test Summary 表列出每个 story 的预期测试文件路径）
2. 来自 `production/sprints/` 的当前 sprint plan（最近修改的文件）
3. 如果传入了 `quick` 参数，跳过本阶段并记录：
   "Coverage scan skipped — run `/smoke-check sprint` for full coverage analysis."

对范围内每个 story：

1. 从 story 文件路径提取 system slug
   （例如 `production/epics/combat/story-001.md` → `combat`）
2. Glob `tests/unit/[system]/` 和 `tests/integration/[system]/`，找文件名中包含该 story slug 或近似相关术语的测试文件
3. 检查 story 文件本身是否有 `Test file:` header field 或 “Test Evidence” 章节

为每个 story 分配 coverage 状态：

| Status | Meaning |
|--------|---------|
| **COVERED** | 找到了匹配该 story system 和 scope 的测试文件 |
| **MANUAL** | Story 类型是 Visual/Feel 或 UI；找到了测试证据文档 |
| **MISSING** | Logic 或 Integration story 没有匹配的测试文件 |
| **EXPECTED** | Config/Data story —— 不需要测试文件；抽查即可 |
| **UNKNOWN** | Story 文件缺失或不可读 |

MISSING 条目是建议性缺口。它们不会导致 FAIL verdict，但必须在报告中显著显示，并且在 `/story-done` 能完全关闭这些 stories 之前必须解决。

---

## 第 4 阶段：运行人工 smoke checks

按以下优先级提取 smoke test checklist：
1. QA plan 的 “Smoke Test Scope” 章节（如果 Phase 1 找到了 QA plan）
2. `production/qa/smoke-tests.md`（如果存在）
3. `tests/smoke/` 目录内容（如果存在）
4. 下面的标准 fallback list（仅当以上都不存在时使用）

根据 sprint 或 QA plan 中实际识别出的系统来调整 batch 2 和 batch 3。把方括号中的占位符替换成当前 sprint stories 中真实的机制名称。

使用 `AskUserQuestion` 批量验证。最多调用 3 次。

**Batch 1 — Core stability（始终运行）：**
```
question: "Smoke check — Batch 1: Core stability. Please verify each:"
options:
  - "Game launches to main menu without crash — PASS"
  - "Game launches to main menu without crash — FAIL"
  - "New game / session starts successfully — PASS"
  - "New game / session starts successfully — FAIL"
  - "Main menu responds to all inputs — PASS"
  - "Main menu responds to all inputs — FAIL"
```

**Batch 2 — Sprint mechanic and regression（始终运行）：**
```
question: "Smoke check — Batch 2: This sprint's changes and regression check:"
options:
  - "[Primary mechanic this sprint] — PASS"
  - "[Primary mechanic this sprint] — FAIL: [describe what broke]"
  - "[Second notable change this sprint, if any] — PASS"
  - "[Second notable change this sprint] — FAIL"
  - "Previous sprint's features still work (no regressions) — PASS"
  - "Previous sprint's features — regression found: [brief description]"
```

**Batch 3 — Data integrity and performance（除非使用 `quick` 参数，否则运行）：**
```
question: "Smoke check — Batch 3: Data integrity and performance:"
options:
  - "Save / load completes without data loss — PASS"
  - "Save / load — FAIL: [describe what broke]"
  - "Save / load — N/A (save system not yet implemented)"
  - "No new frame rate drops or hitches observed — PASS"
  - "Frame rate drops or hitches found — FAIL: [where]"
  - "Performance — not checked in this session"
```

逐字记录每个回应，供 Phase 5 报告使用。

**平台批次**（仅在提供了 `--platform` 参数时运行）：

**PC platform**（`--platform pc` 或 `--platform all`）：
```
question: "Smoke check — PC Platform: Verify platform-specific behaviour:"
options:
  - "Keyboard controls work correctly across all menus and gameplay — PASS"
  - "Keyboard controls — FAIL: [describe issue]"
  - "Mouse input and cursor visibility correct in all states — PASS"
  - "Mouse input — FAIL: [describe issue]"
  - "Windowed and fullscreen modes function without graphical issues — PASS"
  - "Windowed/fullscreen — FAIL: [describe issue]"
  - "Resolution changes apply correctly — PASS"
  - "Resolution changes — FAIL: [describe issue]"
```

**Console platform**（`--platform console` 或 `--platform all`）：
```
question: "Smoke check — Console Platform: Verify platform-specific behaviour:"
options:
  - "Gamepad input works correctly for all actions — PASS"
  - "Gamepad input — FAIL: [describe issue]"
  - "UI fits within TV safe zone margins (no text clipped) — PASS"
  - "TV safe zone — FAIL: [describe what is clipped]"
  - "No keyboard/mouse-only fallbacks shown to gamepad user — PASS"
  - "Input prompt inconsistency — FAIL: [describe]"
  - "Game boots correctly from cold start (no prior save) — PASS"
  - "Cold start — FAIL: [describe issue]"
```

**Mobile platform**（`--platform mobile` 或 `--platform all`）：
```
question: "Smoke check — Mobile Platform: Verify platform-specific behaviour:"
options:
  - "Touch controls work correctly for all primary actions — PASS"
  - "Touch controls — FAIL: [describe issue]"
  - "Game handles orientation change (portrait ↔ landscape) correctly — PASS"
  - "Orientation change — FAIL: [describe what breaks]"
  - "Background / foreground transitions (home button) handled gracefully — PASS"
  - "Background/foreground — FAIL: [describe issue]"
  - "No visible performance issues on target device (no thermal throttling signs) — PASS"
  - "Mobile performance — FAIL: [describe issue]"
```

---

## 第 5 阶段：生成报告

组装完整 smoke check 报告：

````markdown
## Smoke Check Report
**Date**: [date]
**Sprint**: [sprint name / number, or "Not identified"]
**Engine**: [engine]
**QA Plan**: [path, or "Not found — run /qa-plan first"]
**Argument**: [sprint | quick | blank]

---

### Automated Tests

**Status**: [PASS ([N] tests, [N] passing) | FAIL ([N] failures) |
NOT RUN ([reason])]

[If FAIL, list failing tests:]
- `[test name]` — [brief failure description from runner output]

[If NOT RUN:]
"Manual confirmation required: did tests pass in your local IDE or CI? This
will determine whether the automated test row contributes to a FAIL verdict."

---

### Test Coverage

| Story | Type | Test File | Coverage Status |
|-------|------|-----------|----------------|
| [title] | Logic | `tests/unit/[system]/[slug]_test.[ext]` | COVERED |
| [title] | Visual/Feel | `tests/evidence/[slug]-screenshots.md` | MANUAL |
| [title] | Logic | — | MISSING ⚠ |
| [title] | Config/Data | — | EXPECTED |

**Summary**: [N] covered, [N] manual, [N] missing, [N] expected.

---

### Manual Smoke Checks

- [x] Game launches without crash — PASS
- [x] New game starts — PASS
- [x] [Core mechanic] — PASS
- [ ] [Other check] — FAIL: [user's description]
- [x] Save / load — PASS
- [-] Performance — not checked this session

---

### Missing Test Evidence

Stories that must have test evidence before they can be marked COMPLETE via
`/story-done`:

- **[story title]** (`[path]`) — Logic story has no test file.
  Expected location: `tests/unit/[system]/[story-slug]_test.[ext]`

[If none:] "All Logic and Integration stories have test coverage."

---

### Platform-Specific Results *(only if `--platform` was provided)*

| Platform | Checks Run | Passed | Failed | Platform Verdict |
|----------|-----------|--------|--------|-----------------|
| PC | [N] | [N] | [N] | PASS / FAIL |
| Console | [N] | [N] | [N] | PASS / FAIL |
| Mobile | [N] | [N] | [N] | PASS / FAIL |

**Platform notes**: [any platform-specific observations not captured in pass/fail]

Any platform with one or more FAIL checks contributes to the overall FAIL verdict.

---

### Verdict: [PASS | PASS WITH WARNINGS | FAIL]

[Verdict rules — first matching rule wins:]

**FAIL** if ANY of:
- Automated test suite ran and reported one or more test failures
- Any Batch 1 (core stability) check returned FAIL
- Any Batch 2 (primary sprint mechanic or regression check) returned FAIL

**PASS WITH WARNINGS** if ALL of:
- Automated tests PASS or NOT RUN (developer has not yet confirmed)
- All Batch 1 and Batch 2 smoke checks PASS
- One or more Logic/Integration stories have MISSING test evidence

**PASS** if ALL of:
- Automated tests PASS
- All smoke checks in all batches PASS or N/A
- No MISSING test evidence entries
````

---

## 第 6 阶段：写入并门控

先在对话中展示完整报告，然后询问：

"May I write this smoke check report to `production/qa/smoke-[date].md`?"

只有在获得批准后才写入。

写入后，给出 gate 裁定：

**如果 verdict 是 FAIL：**

"The smoke check failed. Do not hand off to QA until these failures are
resolved:

[List each failing automated test or smoke check with a one-line description]

Fix the failures and run `/smoke-check` again to re-gate before QA hand-off."

**如果 verdict 是 PASS WITH WARNINGS：**

"Smoke check passed with warnings. The build is ready for manual QA.

Advisory items to resolve before running `/story-done` on affected stories:
[list MISSING test evidence entries]

QA hand-off: share `production/qa/qa-plan-[sprint].md` with the qa-tester
agent to begin manual verification."

**如果 verdict 是 PASS：**

"Smoke check passed cleanly. The build is ready for manual QA.

QA hand-off: share `production/qa/qa-plan-[sprint].md` with the qa-tester
agent to begin manual verification."

---

## 协作协议

- **永远不要把 NOT RUN 当成自动 FAIL**——记录为 NOT RUN，并让开发者手动确认状态。未确认的 NOT RUN 会计入 PASS WITH WARNINGS，而不是 FAIL。
- **永远不要自动修复失败**——只报告并说明需要解决什么。不要尝试编辑源代码或测试文件。
- **PASS WITH WARNINGS 不会阻止 QA hand-off**——它只是记录 `/story-done` 需要跟进的建议性缺口。
- **`quick` 参数** 会跳过 Phase 3（覆盖扫描）和 Phase 4 Batch 3。修复某个具体失败后快速复查时使用它。
- 所有人工 smoke check 验证都使用 `AskUserQuestion`。
- **写报告前绝不自动写入**——Phase 6 在任何文件创建前都需要显式批准。
