---
name: story-readiness
description: "验证故事文件是否已具备实施条件。检查嵌入的 GDD 要求、ADR 引用、引擎说明、清晰的验收标准以及是否存在未解决的设计问题。输出 READY / NEEDS WORK / BLOCKED verdict，并列出具体缺口。用于用户询问‘这个故事准备好了吗’、‘我可以开始这个故事吗’、‘故事 X 可以实施了吗’。"
argument-hint: "[story-file-path or 'all' or 'sprint']"
user-invocable: true
allowed-tools: Read, Glob, Grep, AskUserQuestion, Task
model: haiku
---

# 故事就绪度

此技能用于验证故事文件是否包含开发者开始实施所需的一切——不在冲刺中途打断设计，不靠猜测，不留下含糊的验收标准。请在分配故事前运行它。

**此技能为只读。** 它不会编辑故事文件。它只报告发现，并询问用户是否希望帮助补齐缺口。

**输出：** 每个故事的 verdict（READY / NEEDS WORK / BLOCKED），并为每个未就绪的故事列出具体缺口。

---

## 第 0 阶段：解析审查模式

在启动时一次性解析审查模式（本次运行中的所有 gate spawn 共用该模式）：

1. 如果技能调用时带了 `--review [full|lean|solo]` → 使用该值
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认 `lean`

完整检查模式和模式定义见 `.claude/docs/director-gates.md`。

---

## 1. 解析参数

**范围：** `$ARGUMENTS[0]`（空白 = 通过 AskUserQuestion 询问）

- **特定路径**（例如 `/story-readiness production/epics/combat/story-001-basic-attack.md`）：验证该单个故事文件。
- **`sprint`**：读取 `production/sprints/` 中最近修改的当前冲刺计划，提取其中引用的所有故事路径，逐个验证。
- **`all`**：glob `production/epics/**/*.md`，排除 `EPIC.md` 索引文件，验证找到的每个故事文件。
- **无参数**：询问用户要验证哪个范围。

如果没有参数，使用 `AskUserQuestion`：
- "你想验证什么？"
  - 选项："一个具体的故事文件"、"当前冲刺中的所有故事"、"production/epics/ 中的所有故事"、"某个特定 epic 的故事"

继续前先报告范围："正在验证 [N] 个故事文件。"

---

## 2. 载入支持上下文

在检查任何故事之前，先一次性加载参考文档（不要对每个故事重复加载）：

- `design/gdd/systems-index.md` —— 了解哪些系统有已批准的 GDD
- `docs/architecture/control-manifest.md` —— 了解有哪些 manifest 规则（如果文件不存在，只记录一次缺失；不要对每个故事重复提示）
  同时如果文件存在，提取头部块中的 `Manifest Version:` 日期。
- `docs/architecture/tr-registry.yaml` —— 按 `id` 索引所有条目。用于验证故事中的 TR-ID。如果文件不存在，只记录一次；TR-ID 检查将对所有故事自动通过（registry 早于故事出现，所以缺失 registry 意味着故事创建于 TR tracking 引入之前）。
- 所有 ADR 的 status 字段 —— 对于被检查的故事里引用到的每个唯一 ADR，读取 ADR 文件并记录其 `Status:` 字段。缓存这些结果，避免对每个故事重复读取同一个 ADR。
- 当前冲刺文件（如果范围是 `sprint`）—— 用于判断 Must Have / Should Have 优先级，供升级规则使用

---

## 3. 故事就绪检查清单

对每个故事文件，评估以下每一项。只有所有项都通过，或者明确标记为 N/A 且给出原因时，故事才算 READY。

### 设计完整性

- [ ] **引用了 GDD 要求**：故事包含一个 `design/gdd/` 路径，并引用或链接了该 GDD 中的具体 requirement、acceptance criterion 或 rule —— 不能只是 GDD 文件名。仅仅链接文档而没有追踪到具体 requirement 不算通过。
- [ ] **要求是自包含的**：故事中的验收标准无需打开 GDD 也能理解。开发者不应需要阅读另一份文档才能理解 DONE 的含义。
- [ ] **验收标准可测试**：每条标准都是具体、可观察的条件——不是“实现 X”或“系统正常工作”。
  不好的例子："实现跳跃机制。" 好的例子："按住跳跃时，跳跃在 0.3 秒内达到 5 单位的最大高度。"
- [ ] **没有需要主观判断的验收标准**：像“手感响应良好”或“看起来不错”这样的标准，如果没有明确基准，就不可测试。它们必须替换为具体的可观察条件或 playtest 协议。

### 架构完整性

- [ ] **引用了 ADR 或明确写了 N/A**：故事至少引用一份 ADR，或者明确写出 "No ADR applies" 并附简短原因。
  如果既没有 ADR 引用，也没有显式 N/A 注记，则不通过。
- [ ] **ADR 已被接受（不是 Proposed）**：对每个被引用的 ADR，使用第 2 节加载的缓存 ADR 状态检查其 `Status:` 字段。
  - 如果 `Status: Accepted` → 通过。
  - 如果 `Status: Proposed` → **BLOCKED**：ADR 在被接受前可能还会更改，故事的实施指导可能出错。
    修复方式：`BLOCKED: ADR-NNNN is Proposed — wait for acceptance before implementing.`
  - 如果 ADR 文件不存在 → **BLOCKED**：引用的 ADR 缺失。
  - 如果故事有显式的 “No ADR applies” N/A 注记，则自动通过。
- [ ] **TR-ID 有效且处于 active**：如果故事包含 `TR-[system]-NNN` 引用，则在第 2 节加载的 TR registry 中查找。
  - 如果 ID 存在且 `status: active` → 通过。
  - 如果 ID 存在且 `status: deprecated` 或 `status: superseded-by: ...` → NEEDS WORK：该需求已被移除或替换。
    修复：更新故事以引用当前 requirement ID，或如果不再适用则移除。
  - 如果 ID 在 registry 中不存在 → NEEDS WORK：该 ID 尚未注册（故事可能早于 registry，或 registry 需要运行一次 `/architecture-review`）。
  - 如果故事没有 TR-ID 引用，或 registry 不存在 → 自动通过。
- [ ] **Manifest 版本是最新的**：如果故事头部有 `Manifest Version:` 日期，并且 `docs/architecture/control-manifest.md` 存在：
  - 如果故事版本与当前 manifest 的 `Manifest Version:` 一致 → 通过。
  - 如果故事版本早于当前 manifest → NEEDS WORK：可能有新规则。
    修复：查看变更后的 manifest 规则，若任何禁止项或必需项有变化则更新故事，然后将故事的 `Manifest Version:` 更新为当前版本。
  - 如果故事没有 `Manifest Version:` 字段，或 manifest 不存在 → 自动通过。
- [ ] **有引擎说明**：对于这条故事很可能会触及的任何 post-cutoff 引擎 API，实施说明或验证要求已写入。
  如果故事显然不会触及引擎 API（例如纯数据/配置变更），则写明 “N/A — no engine API involved” 即可。
- [ ] **已注明控制 manifest 规则**：引用了 control manifest 中相关的层级规则，或者写明 “N/A — manifest not yet created”。
  如果 `docs/architecture/control-manifest.md` 尚不存在，则这一项自动通过（不要处罚写在 manifest 创建前的故事）。

### 范围清晰度

- [ ] **有估算**：故事包含大小估算（小时、点数或 T-shirt size）。没有估算的故事无法排期。
- [ ] **写明范围边界**：故事明确说明它不包含什么，可以是显式的 Out of Scope 小节，也可以是足够清晰的语言。
  如果没有这个内容，实施时很容易出现范围蔓延。
- [ ] **列出了故事依赖**：如果这个故事依赖其他故事先完成，则列出这些故事 ID。如果没有依赖，必须显式写明 “None”，不能留空。

### 未解决的问题

- [ ] **没有未解决的设计问题**：故事中没有任何被标记为 “UNRESOLVED”、“TBD”、“TODO”、“?” 或类似标记的文本，出现在任何验收标准、实施说明或规则陈述中。
- [ ] **依赖故事不是 DRAFT**：对于每个列为依赖的故事，检查文件是否存在且不是 DRAFT 状态。依赖于 DRAFT 或缺失故事的故事应标记为 BLOCKED，而不只是 NEEDS WORK。

### 资源引用检查

- [ ] **引用的资源存在**：扫描故事文本中的资源路径模式（包含 `assets/` 的路径，或扩展名 `.png`、`.jpg`、`.svg`、`.wav`、`.ogg`、`.mp3`、`.glb`、`.gltf`、`.tres`、`.tscn`、`.res`）。
  - 对每个找到的资源路径：使用 Glob 检查文件是否存在。
  - 如果任一引用资源不存在：**NEEDS WORK** —— 标注缺失路径。
    （故事引用了尚未创建的资源。要么移除引用，要么创建占位资源，要么将其标记为明确依赖于资源创建故事。）
  - 如果所有引用资源都存在：注明 "Referenced assets verified: [count] found."。
  - 如果故事中没有引用任何资源路径：注明 "No asset references found in story — skipping asset check."。这一项自动通过。
  - 这是仅检查存在性的规则。不要验证文件格式或内容。

### Definition of Done

- [ ] **至少有 3 条可测试的验收标准**：少于 3 条说明故事要么过于微小（是否真的该作为一个故事？），要么规格不足。
- [ ] **如适用则注明性能预算**：如果这条故事涉及 gameplay loop、渲染或物理的任何部分，必须有性能预算，或写明 “no performance impact expected — [reason]”。
- [ ] **声明了 Story Type**：故事在头部包含 `Type:` 字段，标明测试类别（Logic / Integration / Visual/Feel / UI / Config/Data）。
  没有这个字段，就无法在故事结束时强制执行测试证据要求。
  修复：在故事头部添加 `Type: [Logic|Integration|Visual/Feel|UI|Config/Data]`。
- [ ] **测试证据要求清晰**：如果设置了 Story Type，故事必须包含 `## Test Evidence` 小节，说明证据将存放在哪里（Logic/Integration 的测试文件路径，或 Visual/Feel/UI 的证据文档路径）。
  修复：添加 `## Test Evidence`，并写明该故事类型对应的预期证据位置。

---

## 4. Verdict 赋值

为每个故事分配三种 verdict 之一：

**READY** —— 所有清单项都通过，或有明确的 N/A 理由。
故事可以立即分配。

**NEEDS WORK** —— 一项或多项检查失败，但所有依赖故事都存在且不是 DRAFT。
故事可以先修复再分配。

**BLOCKED** —— 一个或多个依赖故事缺失或处于 DRAFT，
或者某个关键设计问题（在标准或规则中标记为 UNRESOLVED）没有负责人。
在阻塞解除前，故事不能分配。注意：BLOCKED 的故事也可能有 NEEDS WORK 项——两者都要列出。

---

## 5. 输出格式

### 单故事输出

```text
## Story Readiness: [story title]
File: [path]
Verdict: [READY / NEEDS WORK / BLOCKED]

### Passing Checks (N/[total])
[list passing items briefly]

### Gaps
- [Checklist item]: [exact description of what is missing or wrong]
  Fix: [specific text needed to resolve this gap]

### Blockers (if BLOCKED)
- [What is blocking]: [story ID or design question that must resolve first]
```

### 多故事汇总输出

```text
## Story Readiness Summary — [scope] — [date]

Ready:      [N] stories
Needs Work: [N] stories
Blocked:    [N] stories

### Ready Stories
- [story title] ([path])

### Needs Work
- [story title]: [primary gap — one line]
- [story title]: [primary gap — one line]

### Blocked Stories
- [story title]: Blocked by [story ID / design question]

---
[每个非就绪故事的完整细节，沿用单故事格式]
```

### 冲刺升级

如果范围是 `sprint`，且有任何 Must Have 故事是 NEEDS WORK 或 BLOCKED，则在输出顶部添加醒目警告：

```text
WARNING: [N] Must Have stories are not implementation-ready.
[List them with their primary gap or blocker.]
Resolve these before the sprint begins or replan with `/sprint-plan update`.
```

---

## 6. 协作协议

此技能为只读。它不会提议编辑，也不会要求写文件。

在报告完发现后，提供：

"Would you like help filling in the gaps for any of these stories? I can draft the missing sections for your approval."

如果用户对某个特定故事说可以，则只在对话中起草缺失部分。不要使用 Write 或 Edit 工具——写入由用户或 `/create-stories` 负责。

**重定向规则：**
- 如果故事文件完全不存在："这个故事文件完全缺失。请运行 `/create-epics [layer]` 然后运行 `/create-stories [epic-slug]`，从 GDD 和 ADR 生成故事。"
- 如果故事没有 GDD 引用，而且工作看起来很小："这个故事没有 GDD 引用。如果变更很小（约 4 小时以内），请运行 `/quick-design [description]` 创建 Quick Design Spec，然后在故事中引用它。"
- 如果故事范围已经超出原始估算："这个故事看起来范围扩大了。建议在实施前将其拆分，或升级给 producer。"

---

## 7. 下一个故事交接

在完成单个故事的就绪性检查后（不是 `all` 或 `sprint` 范围）：

1. 从 `production/sprints/` 读取当前冲刺文件（最近修改的那个）。
2. 找出以下故事：
   - 状态：READY 或 NOT STARTED
   - 不是刚刚检查过的故事
   - 不会被未完成依赖阻塞
   - 位于 Must Have 或 Should Have 级别

如果找到，最多显示 3 个：

```text
### Other Ready Stories in This Sprint

1. [Story name] — [1-line description] — Est: [X hrs]
2. [Story name] — [1-line description] — Est: [X hrs]

Run `/story-readiness [path]` to validate before starting.
```

如果没有冲刺文件，或者没有找到其他 ready 的故事，则静默跳过这一节。

---

## 第 8 阶段：Director Gate — Story Readiness Review

在 spawn QL-STORY-READY 前应用第 0 阶段解析出的审查模式：

- `solo` → 跳过。说明："QL-STORY-READY skipped — Solo mode." 继续关闭。
- `lean` → 跳过。说明："QL-STORY-READY skipped — Lean mode." 继续关闭。
- `full` → 正常 spawn。

通过 Task 使用 gate **QL-STORY-READY**（`.claude/docs/director-gates.md`）spawn `qa-lead`。

传入以下上下文：
- 故事标题
- 验收标准列表（故事验收标准小节中的所有条目）
- 依赖状态（列出的所有依赖及其当前状态：exist / DRAFT / missing）
- 第 4 阶段得出的整体 verdict（READY / NEEDS WORK / BLOCKED）

按 `director-gates.md` 中的标准规则处理 verdict：
- **ADEQUATE** → 故事通过。继续关闭。
- **GAPS [list]** → 通过 `AskUserQuestion` 将具体缺口呈现给用户：
  选项：`Update story with suggested gaps` / `Accept and proceed anyway` / `Discuss further`。
- **INADEQUATE** → 呈现具体缺口；询问用户是否更新故事或仍然继续。

---

## 推荐下一步

- 运行 `/dev-story [story-path]`，在故事 READY 后开始实施
- 运行 `/story-readiness sprint`，一次性检查当前冲刺中的所有故事
- 如果故事文件完全缺失，运行 `/create-stories [epic-slug]`