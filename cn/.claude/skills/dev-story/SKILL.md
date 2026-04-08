---
name: dev-story
description: "读取故事文件并实现它。加载完整上下文（story、GDD requirement、ADR 指南、control manifest），路由到正确的程序员专精 agent，完成代码与测试实现，并确认每条验收标准。核心实现技能——在 /story-readiness 之后、/code-review 和 /story-done 之前运行。"
argument-hint: "[story-path]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash, Task, AskUserQuestion
---

# Dev Story

此技能连接规划与代码。它会完整读取 story 文件，组装程序员所需的全部上下文，路由到正确的专精 agent，并推动实现直到完成——包括编写测试。

**每个 story 的流程：**
```
/qa-plan sprint           ← 在 sprint 开始前定义测试需求
/story-readiness [path]   ← 开始前验证
/dev-story [path]         ← 实现它（本技能）
/code-review [files]      ← 审查它
/story-done [path]        ← 验证并关闭它
```

**当所有 sprint stories 完成后：**运行 `/team-qa sprint` 执行完整 QA 流程，并在推进项目阶段前获得签收裁定。

**输出：** 项目 `src/` 与 `tests/` 目录中的源代码 + 测试文件。

---

## 第 1 阶段：找到 Story

**如果提供了路径**：直接读取该文件。

**如果没有参数**：检查 `production/session-state/active.md` 中的活跃 story。若找到，确认：“继续处理 [story title] ——对吗？”
如果没找到，询问：“我们要实现哪个 story？”Glob `production/epics/**/*.md` 并列出 Status: Ready 的 stories。

---

## 第 2 阶段：加载完整上下文

**在加载任何上下文之前，先验证所需文件是否存在。** 从 story 的 `ADR Governing Implementation` 字段提取 ADR 路径，然后检查：

| 文件 | 路径 | 若缺失 |
|------|------|--------|
| TR registry | `docs/architecture/tr-registry.yaml` | **停止** ——“未找到 TR registry。运行 `/create-epics` 生成它。” |
| Governing ADR | story ADR 字段中的路径 | **停止** ——“未找到 ADR 文件 [path]。运行 `/architecture-decision` 创建它，或修正 story 中 ADR 字段的文件名。” |
| Control manifest | `docs/architecture/control-manifest.md` | **警告并继续** ——“未找到 Control manifest——无法检查层级规则。运行 `/create-control-manifest`。” |

如果 TR registry 或 Governing ADR 缺失，把 story 状态设为会话状态中的 **BLOCKED**，并且不要 spawn 任何 programmer agent。

同时读取以下内容——这些是彼此独立的读取。所有上下文加载完之前，不要开始实现：

### Story 文件
提取并保留：
- **Story title、ID、layer、type**（Logic / Integration / Visual/Feel / UI / Config/Data）
- **TR-ID** —— GDD requirement 标识符
- **Governing ADR** 引用
- Story header 中嵌入的 **Manifest Version**
- **Acceptance Criteria** —— 每个复选项，逐字保留
- **Implementation Notes** —— story 中的 ADR 指导部分
- **Out of Scope** 边界
- **Test Evidence** —— 需要创建的测试文件路径
- **Dependencies** —— 在此 story 之前必须完成的内容

### TR registry
读取 `docs/architecture/tr-registry.yaml`。查找 story 的 TR-ID。
读取当前的 `requirement` 文本——这是对 GDD 当前要求的唯一真相来源。不要依赖 story 文件中的任何内联文本（可能已过时）。

### Governing ADR
读取 `docs/architecture/[adr-file].md`。提取：
- 完整的 Decision 章节
- Implementation Guidelines 章节（程序员实际遵循的内容）
- Engine Compatibility 章节（后截止日期 API、已知风险）
- ADR Dependencies 章节

### Control manifest
读取 `docs/architecture/control-manifest.md`。提取与该 story 层级相关的规则：
- 必需模式
- 禁止模式
- 性能护栏

检查：story 内嵌的 Manifest Version 是否与当前 manifest 标头日期一致？
如果不一致，在继续前先用 `AskUserQuestion`：
- 提示：“该 story 是按 manifest v[story-date] 编写的。当前 manifest 是 v[current-date]。新规则可能适用。你想如何继续？”
- 选项：
  - `[A] 更新 story 的 manifest version，并使用当前规则实现（推荐）`
  - `[B] 按旧规则实现——我接受不符合新规则的风险`
  - `[C] 先停在这里——我想先查看 manifest diff`

如果选 [A]：在 spawn 程序员之前，把 story 文件里的 `Manifest Version:` 字段改为当前 manifest 日期。然后仔细阅读 manifest 中的新规则。
如果选 [B]：仍然要仔细阅读 manifest 中的新规则，并在 Phase 6 总结的“Deviations”下记录版本不一致。
如果选 [C]：停止。不要 spawn 任何 agent。让用户先查看并重新运行 `/dev-story`。

### 依赖验证

在从 story 文件中提取 **Dependencies** 列表后，逐项验证：

1. Glob `production/epics/**/*.md` 找到每个依赖 story 文件。
2. 读取其 `Status:` 字段。
3. 如果任一依赖的 Status 不是 `Complete` 或 `Done`：
   - 使用 `AskUserQuestion`：
     - 提示：“Story '[current story]' 依赖 '[dependency title]'，而它当前是 [status]，不是 Complete。你想如何继续？”
     - 选项：
       - `[A] 继续——我接受依赖风险`
       - `[B] 停止——我先完成依赖`
       - `[C] 依赖其实已经完成，只是状态没更新——把它标为 Complete 并继续`
   - 如果选 [B]：把 story 状态设为会话状态中的 **BLOCKED**，并停止。不要 spawn 任何 programmer agent。
   - 如果选 [C]：先问“我可以把 [dependency path] 的 Status 更新为 Complete 吗？”再继续。
   - 如果选 [A]：在 Phase 6 总结的“Deviations”下记录：“以未完成依赖实现：[dependency title] —— [status].”

如果找不到依赖文件：警告“未找到依赖 story：[path]。请核对路径或创建该 story 文件。”

---

### 引擎参考
读取 `.claude/docs/technical-preferences.md`：
- `Engine:` 值——决定要使用哪些 programmer agent
- 命名约定（类名、文件名、signal/event 名称）
- 性能预算（帧预算、内存上限）
- 禁止模式

---

## 第 3 阶段：路由到正确的 Programmer

根据 story 的 **Layer**、**Type** 和 **system name**，确定要通过 Task spawn 哪个专精 agent。

**Config/Data stories——完全跳过 agent spawn：**
如果 story 的 Type 是 `Config/Data`，则不需要 programmer agent 或 engine specialist。直接进入 Phase 4（Config/Data note）。实现是编辑数据文件——不需要路由表评估，也不需要 engine specialist。

### 主 agent 路由表

| Story context | Primary agent |
|---|---|
| Foundation layer — any type | `engine-programmer` |
| Any layer — Type: UI | `ui-programmer` |
| Any layer — Type: Visual/Feel | `gameplay-programmer`（实施） |
| Core or Feature — gameplay mechanics | `gameplay-programmer` |
| Core or Feature — AI behaviour, pathfinding | `ai-programmer` |
| Core or Feature — networking, replication | `network-programmer` |
| Config/Data — no code | No agent needed（见 Phase 4 Config note） |

### 引擎专精——代码类 stories 一律作为 secondary spawn

读取 `.claude/docs/technical-preferences.md` 的 `Engine Specialists` 章节，获取已配置的 primary specialist。当 story 涉及引擎特定 API、模式，或者 ADR 具有 HIGH 引擎风险时，把它们和 primary agent 一起 spawn。

| Engine | 可用 specialist agents |
|--------|------------------------|
| Godot 4 | `godot-specialist`, `godot-gdscript-specialist`, `godot-shader-specialist` |
| Unity | `unity-specialist`, `unity-ui-specialist`, `unity-shader-specialist` |
| Unreal Engine | `unreal-specialist`, `ue-gas-specialist`, `ue-blueprint-specialist`, `ue-umg-specialist`, `ue-replication-specialist` |

**当引擎风险为 HIGH**（来自 ADR 或 VERSION.md）时：即使是非引擎面对的 story，也始终要 spawn engine specialist。High risk 意味着 ADR 中记录了后截止日期引擎 API 假设，需要专家校验。

---

## 第 4 阶段：实现

通过 Task 用完整上下文包 spawn 选定的 programmer agent：

向 agent 提供：
1. 完整 story 文件内容
2. 当前 GDD requirement 文本（来自 TR registry）
3. ADR Decision + Implementation Guidelines（逐字——不要总结）
4. 该层级的 control manifest 规则
5. 引擎命名约定与性能预算
6. ADR Engine Compatibility 章节中的任何引擎特定备注
7. 必须创建的测试文件路径
8. 明确指令：**实现这个 story 并写测试**

agent 应该：
- 按照 ADR 指南在 `src/` 中创建或修改文件
- 遵守 control manifest 中所有必需与禁止模式
- 保持在 story 的 Out of Scope 边界内（不要碰无关文件）
- 编写干净、带文档注释的公共 API

### Config/Data stories（无需 agent）

对于 Type: Config/Data 的 story，不需要 programmer agent。实现就是直接编辑一个数据文件。读取 story 的 acceptance criteria，并直接对数据文件做指定修改。记录修改了哪些值，以及从什么改成了什么。

### Visual/Feel stories

Spawn `gameplay-programmer` 来实现代码/动画调用。注意 Visual/Feel 的 acceptance criteria 不能自动验证——“感觉是否合适？”这一步会在 `/story-done` 中通过人工确认完成。

---

## 第 5 阶段：写测试

对于 **Logic** 和 **Integration** stories，测试必须作为实现的一部分写出来——不能留到后面。

提醒 programmer agent：

> "该 story 的测试文件必须位于：`[path from Test Evidence section]`。
> 没有它，story 就不能通过 `/story-done` 关闭。请把测试和实现一起写，而不是事后补。"

测试要求（来自 coding-standards.md）：
- 文件名：`[system]_[feature]_test.[ext]`
- 函数名：`test_[scenario]_[expected_outcome]`
- 每条 acceptance criterion 至少要有一个测试函数覆盖
- 不要随机种子、不要依赖时间的断言、不要外部 I/O
- 测试 GDD Formulas 章节中的公式边界

对于 **Visual/Feel** 和 **UI** stories：不需要自动测试。提醒 agent 在实现总结中注明需要什么手工证据：
"Evidence doc required at `production/qa/evidence/[slug]-evidence.md`."

对于 **Config/Data** stories：不需要测试文件。smoke check 将作为证据。

---

## 第 6 阶段：收集并总结

在 programmer agent(s) 完成后，收集：

- 创建或修改的文件（含路径）
- 已创建的测试文件（路径和测试函数数量）
- 任何超出 story Out of Scope 边界的偏离（标记出来）
- agent 提出的任何问题或阻塞
- specialist 标记的任何引擎特定风险

给出简洁的实现总结：

```
## 实现完成：[Story Title]

**变更文件**：
- `src/[path]` — 创建 / 修改（[简述]）
- `tests/[path]` — 测试文件（[N] 个测试函数）

**已覆盖的验收标准**：
- [x] [criterion] — 已在 [file:function] 中实现
- [x] [criterion] — 已由测试 [test_name] 覆盖
- [ ] [criterion] — 延后：需要 playtest（Visual/Feel）

**超出范围的偏离**： [None] 或 [列出触及 story 边界之外的文件]
**引擎风险**： [None] 或 [specialist 发现]
**阻塞**： [None] 或 [描述]

可进行：`/code-review [file1] [file2]` 然后 `/story-done [story-path]`
```

---

## 第 7 阶段：更新会话状态

悄悄追加到 `production/session-state/active.md`：

```
## Session Extract — /dev-story [date]
- Story: [story-path] — [story title]
- Files changed: [comma-separated list]
- Test written: [path, or "None — Visual/Feel/Config story"]
- Blockers: [None, or description]
- Next: /code-review [files] then /story-done [story-path]
```

如果 `active.md` 不存在，则创建它。确认：“Session state updated.”

---

## 错误恢复协议

如果任何已 spawn 的 agent（通过 Task）返回 BLOCKED、报错，或无法完成：

1. **立即上报**：在继续后续阶段之前，向用户报告 “[AgentName]: BLOCKED — [reason]”
2. **评估依赖**：检查被阻塞的 agent 输出是否是后续阶段所需。若是，不要在没有用户输入前继续越过该依赖点。
3. **通过 AskUserQuestion 提供选项**：
   - 跳过该 agent，并在最终报告中注明缺口
   - 用更窄的范围重试
   - 停在这里，先解决阻塞
4. **始终产出部分报告** —— 输出已完成的内容。不要因为一个 agent 被阻塞就丢弃成果。

常见阻塞：
- 输入文件缺失（story 找不到、GDD 缺失）→ 转到创建它的技能
- ADR 状态为 Proposed → 不要实现；先运行 `/architecture-decision`
- 范围过大 → 用 `/create-stories` 拆成两个 stories
- ADR 与 story 之间的指令冲突 → 上报冲突，不要猜
- Manifest 版本不匹配 → 向用户展示 diff，询问是否按旧规则继续还是先更新 story

## 协作协议

- **文件写入由下游代理负责** —— 所有源代码、测试文件和证据文档都由通过 Task spawn 的 sub-agents 编写。每个 sub-agent 都要单独执行“May I write to [path]?” 协议。本 orchestrator 不直接写文件。
- **先加载，再实现** —— 不要在所有上下文都加载完成前开始编码（story、TR-ID、ADR、manifest、engine prefs）。上下文不完整会导致实现偏离设计。
- **ADR 是法律** —— 实现必须遵循 ADR 的 Implementation Guidelines。如果指南和你觉得“更好”的做法冲突，请在总结中指出，而不是悄悄偏离。
- **保持在范围内** —— Out of Scope 章节是合同。如果实现某条标准需要改动一个 out-of-scope 文件，就停下来并上报：
  "实现 [criterion] 需要修改 [file]，这超出了范围。我可以继续吗，还是要创建一个单独的 story？"
- **Logic/Integration 的测试不是可选项** —— 没有测试文件就不要把实现标记为完成
- **Visual/Feel 标准是延后而不是跳过** —— 在总结中把它们标为 DEFERRED；它们会在 `/story-done` 中人工验证
- **大型结构性决策前先询问** —— 如果 story 需要 ADR 未覆盖的架构模式，在实现前先上报：
  "ADR 没有说明如何处理 [case]。我的计划是 [X]。要继续吗？"

---

## 推荐下一步

- 运行 `/code-review [file1] [file2]`，在关闭 story 前审查实现
- 运行 `/story-done [story-path]`，验证 acceptance criteria 并标记 story 完成
- 所有 sprint stories 完成后：在推进项目阶段前运行 `/team-qa sprint` 执行完整 QA 流程
