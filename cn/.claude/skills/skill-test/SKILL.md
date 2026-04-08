---
name: skill-test
description: "验证技能文件的结构合规性与行为正确性。三种模式：static（linter）、spec（行为测试）、audit（覆盖率报告）。"
argument-hint: "static [skill-name | all] | spec [skill-name] | category [skill-name | all] | audit"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
---

# 技能测试

验证 `.claude/skills/*/SKILL.md` 文件的结构合规性与行为正确性。无需外部依赖——完全在现有的 skill/hook/template 架构中运行。

**四种模式：**

| 模式 | 命令 | 目的 | Token 成本 |
|------|------|------|-----------|
| `static` | `/skill-test static [name\|all]` | 结构 linter —— 每个 skill 进行 7 项合规检查 | Low (~1k/skill) |
| `spec` | `/skill-test spec [name]` | 行为验证器 —— 评估测试规范中的断言 | Medium (~5k/skill) |
| `category` | `/skill-test category [name\|all]` | 分类 rubric —— 按 skill 的分类指标检查 | Low (~2k/skill) |
| `audit` | `/skill-test audit` | 覆盖率报告 —— skills、agent 规范、最近测试日期 | Low (~3k total) |

---

## 阶段 1：解析参数

根据第一个参数确定模式：

- `static [name]` → 对单个 skill 执行 7 项结构检查
- `static all` → 对所有 skills 执行 7 项结构检查（Glob `.claude/skills/*/SKILL.md`）
- `spec [name]` → 读取 skill + 测试规范，评估断言
- `category [name]` → 从 `CCGS Skill Testing Framework/quality-rubric.md` 运行分类特定 rubric
- `category all` → 对 catalog 中每个带有 `category:` 的 skill 运行分类 rubric
- `audit`（或无参数）→ 读取 catalog，列出所有 skills 和 agents，显示覆盖情况

如果参数缺失或无法识别，输出用法并停止。

---

## 阶段 2A：Static 模式——结构 linter

对每个被测试的 skill，完整读取其 `SKILL.md` 并运行全部 7 项检查：

### 检查 1 —— 必需 frontmatter 字段
文件必须在 YAML frontmatter 块中包含以下所有字段：
- `name:`
- `description:`
- `argument-hint:`
- `user-invocable:`
- `allowed-tools:`

**FAIL** 如果有任何缺失。

### 检查 2 —— 多阶段
skill 必须至少有 2 个编号的阶段标题。查找如下模式：
- `## Phase N` 或 `## Phase N:`
- `## N.`（编号顶级章节）
- 如果没有显式编号的 phase，至少要有 2 个不同的 `##` 标题

**FAIL** 如果发现的 phase-like 标题少于 2 个。

### 检查 3 —— Verdict 关键词
skill 必须至少包含以下关键词之一：`PASS`, `FAIL`, `CONCERNS`, `APPROVED`,
`BLOCKED`, `COMPLETE`, `READY`, `COMPLIANT`, `NON-COMPLIANT`

**FAIL** 如果都没有。

### 检查 4 —— 协作协议语言
skill 必须包含先询问后写入的语言。查找：
- `"May I write"`（标准形式）
- `"before writing"` 或靠近文件写入说明的 `"approval"`
- `"ask"` 与 `"write"` 在同一段落附近出现

**WARN** 如果缺失（某些只读技能可以合理跳过）。
**FAIL** 如果 `allowed-tools` 包含 `Write` 或 `Edit`，但没有发现先询问后写入语言。

### 检查 5 —— 下一步交接
skill 必须以推荐的后续行动或跟进路径结束。查找：
- 最后一个部分提到另一个 skill（例如 `/story-done`、`/gate-check`）
- “Recommended next” 或 “next step” 之类的措辞
- “Follow-Up” 或 “After this” 章节

**WARN** 如果缺失。

### 检查 6 —— fork context 复杂度
如果 frontmatter 包含 `context: fork`，skill 应该至少有 5 个 phase 标题（`##` 级别或编号的 Phase N 标题）。fork context 适合复杂的多阶段 skill；简单 skill 不应该使用它。

**WARN** 如果设置了 `context: fork`，但找到的 phase 少于 5 个。

### 检查 7 —— argument hint 合理性
`argument-hint` 必须非空。如果 skill 正文提到多个模式（例如 “Mode A | Mode B”），hint 应该反映这些模式。将 hint 与第一阶段的 “Parse Arguments” 章节交叉比对。

**WARN** 如果 hint 是 `""`，或文档中的模式与 hint 不匹配。

---

### Static 模式输出格式

对于单个 skill：
```
=== Skill Static Check: /[name] ===

Check 1 — Frontmatter Fields:    PASS
Check 2 — Multiple Phases:       PASS (7 phases found)
Check 3 — Verdict Keywords:      PASS (PASS, FAIL, CONCERNS)
Check 4 — Collaborative Protocol: PASS ("May I write" found)
Check 5 — Next-Step Handoff:     WARN (no follow-up section found)
Check 6 — Fork Context Complexity: PASS (8 phases, context: fork set)
Check 7 — Argument Hint:         PASS

Verdict: WARNINGS (1 warning, 0 failures)
Recommended: Add a "Follow-Up Actions" section at the end of the skill.
```

对于 `static all`，先给出汇总表，然后列出任何不合规的 skills：
```
=== Skill Static Check: All 52 Skills ===

Skill                  | Result       | Issues
-----------------------|--------------|-------
gate-check             | COMPLIANT    |
design-review          | COMPLIANT    |
story-readiness        | WARNINGS     | Check 5: no handoff
...

Summary: 48 COMPLIANT, 3 WARNINGS, 1 NON-COMPLIANT
Aggregate Verdict: N WARNINGS / N FAILURES
```

---

## 阶段 2B：Spec 模式——行为验证器

### 步骤 1 —— 定位文件

在 `.claude/skills/[name]/SKILL.md` 找到 skill。
从 `CCGS Skill Testing Framework/catalog.yaml` 中查找 spec 路径——使用对应 skill 条目的 `spec:` 字段。

如果任一项缺失：
- 缺失 skill："Skill '[name]' not found in `.claude/skills/`."
- catalog 中缺少 spec path："No spec path set for '[name]' in catalog.yaml."
- 对应路径下找不到 spec 文件："Spec file missing at [path]. Run `/skill-test audit` to see coverage gaps."

### 步骤 2 —— 读取两个文件

完整读取 skill 文件和测试 spec 文件。

### 步骤 3 —— 评估断言

对 spec 中每个 **Test Case**：

1. 读取 **Fixture** 描述（对项目文件状态的假定）
2. 读取 **Expected behavior** 步骤
3. 读取每个 **Assertion** 复选框

对每个 assertion，评估如果正确遵循 skill 的书面指令，且以 fixture 状态为前提，是否能满足它。这是一个由 Claude 执行的推理检查，不是代码执行。

给每个 assertion 标记：
- **PASS** —— skill 指令清楚满足该断言
- **PARTIAL** —— skill 指令部分满足，但存在歧义
- **FAIL** —— 在该 fixture 下，skill 指令无法满足该断言

对 **Protocol Compliance** 断言（始终存在）：
- 检查 skill 是否要求在写文件前先说 “May I write”
- 检查 skill 是否在请求批准前先展示发现
- 检查 skill 是否以推荐下一步结束
- 检查 skill 是否避免在未获批准时自动创建文件

### 步骤 4 —— 生成报告

```
=== Skill Spec Test: /[name] ===
Date: [date]
Spec: CCGS Skill Testing Framework/skills/[category]/[name].md

Case 1: [Happy Path — name]
  Fixture: [summary]
  Assertions:
    [PASS] [assertion text]
    [FAIL] [assertion text]
       Reason: The skill's Phase 3 says "..." but the fixture state means "..."
  Case Verdict: FAIL

Case 2: [Edge Case — name]
  ...
  Case Verdict: PASS

Protocol Compliance:
  [PASS] Uses "May I write" before file writes
  [PASS] Presents findings before asking approval
  [WARN] No explicit next-step handoff at end

Overall Verdict: FAIL (1 case failed, 1 warning)
```

### 步骤 5 —— 提议写入结果

"May I write these results to `CCGS Skill Testing Framework/results/skill-test-spec-[name]-[date].md`
and update `CCGS Skill Testing Framework/catalog.yaml`?"

如果用户同意：
- 把结果文件写入 `CCGS Skill Testing Framework/results/`
- 更新 `CCGS Skill Testing Framework/catalog.yaml` 中该 skill 的条目：
  - `last_spec: [date]`
  - `last_spec_result: PASS|PARTIAL|FAIL`

---

## 阶段 2D：Category 模式——Rubric 评估

### 步骤 1 —— 定位 skill 和 category

在 `.claude/skills/[name]/SKILL.md` 找到 skill。
在 `CCGS Skill Testing Framework/catalog.yaml` 中查找 `category:` 字段。

如果找不到 skill："Skill '[name]' not found."
如果没有 `category:` 字段："No category assigned for '[name]' in catalog.yaml.
Add `category: [name]` to the skill entry first."

对于 `category all`：收集所有带有 `category:` 字段的 skills 并逐个处理。
`category: utility` 的 skills 只按 U1（static checks 通过）和 U2（如果适用，gate mode 正确）评估——先跳到 static mode 处理 U1。

### 步骤 2 —— 读取 Rubric 章节

读取 `CCGS Skill Testing Framework/quality-rubric.md`。
提取与 skill 分类对应的章节（例如 `### gate`、`### team`）。

### 步骤 3 —— 读取 skill

完整读取该 skill 的 `SKILL.md`。

### 步骤 4 —— 评估 rubric 指标

针对该分类 rubric 表中的每个指标：
1. 检查 skill 的书面指令是否清楚满足该标准
2. 标记 PASS、FAIL 或 WARN
3. 对 FAIL/WARN，找出 skill 文本中准确的缺口（引用相关部分或说明其缺失）

### 步骤 5 —— 输出报告

```
=== Skill Category Check: /[name] ([category]) ===

Metric G1 — Review mode read:      PASS
Metric G2 — Full mode directors:   FAIL
  Gap: Phase 3 spawns only CD-PHASE-GATE; TD-PHASE-GATE, PR-PHASE-GATE, AD-PHASE-GATE absent
Metric G3 — Lean mode: PHASE-GATE only: PASS
Metric G4 — Solo mode: no directors:    PASS
Metric G5 — No auto-advance:       PASS

Verdict: FAIL (1 failure, 0 warnings)
Fix: Add TD-PHASE-GATE, PR-PHASE-GATE, and AD-PHASE-GATE to the full-mode director
     panel in Phase 3.
```

### 步骤 6 —— 提议更新 catalog

"May I update `CCGS Skill Testing Framework/catalog.yaml` to record this category check
(`last_category`, `last_category_result`) for [name]?"

---

## 阶段 2C：Audit 模式——覆盖率报告

### 步骤 1 —— 读取 catalog

读取 `CCGS Skill Testing Framework/catalog.yaml`。如果缺失，说明 catalog 尚不存在（首次运行状态）。

### 步骤 2 —— 枚举所有 skills 和 agents

Glob `.claude/skills/*/SKILL.md` 获取完整 skill 列表。
从每个路径中提取 skill 名称（目录名）。

同时读取 `CCGS Skill Testing Framework/catalog.yaml` 中的 `agents:` 部分，获取完整的 agent 列表。

### 步骤 3 —— 构建 Skill 覆盖表

对每个 skill：
- 检查是否存在 spec 文件（使用 catalog 中的 `spec:` 路径，或 glob `CCGS Skill Testing Framework/skills/*/[name].md`）
- 从 catalog 中查找 `last_static`、`last_static_result`、`last_spec`、`last_spec_result`、
  `last_category`、`last_category_result`、`category`（若 catalog 中没有，则标为 “never” / “—”）
- Priority 来自 catalog 的 `priority:` 字段（critical/high/medium/low）

### 步骤 3b —— 构建 Agent 覆盖表

对 catalog `agents:` 部分中的每个 agent：
- 检查是否存在 spec 文件（使用 catalog 中的 `spec:` 路径，或 glob `CCGS Skill Testing Framework/agents/*/[name].md`）
- 从 catalog 中查找 `last_spec`、`last_spec_result`、`category`

### 步骤 4 —— 输出报告

```
=== Skill Test Coverage Audit ===
Date: [date]

SKILLS (72 total)
Specs written: 72 (100%) | Never static tested: 72 | Never category tested: 72

Skill                  | Cat      | Has Spec | Last Static | S.Result | Last Cat | C.Result | Priority
-----------------------|----------|----------|-------------|----------|----------|----------|----------
gate-check             | gate     | YES      | never       | —        | never    | —        | critical
design-review          | review   | YES      | never       | —        | never    | —        | critical
...

AGENTS (49 total)
Agent specs written: 49 (100%)

Agent                  | Category   | Has Spec | Last Spec   | Result
-----------------------|------------|----------|-------------|--------
creative-director      | director   | YES      | never       | —
technical-director     | director   | YES      | never       | —
...

Top 5 Priority Gaps (skills with no spec, critical/high priority):
(none if all specs are written)

Skill coverage:  72/72 specs (100%)
Agent coverage:  49/49 specs (100%)
```

Audit 模式不写任何文件。

提议：“你想运行 `/skill-test static all` 检查所有 skills 的结构合规性吗？想运行 `/skill-test category all` 执行分类 rubric 检查吗？还是想运行 `/skill-test spec [name]` 做特定行为测试？”

---

## 阶段 3：推荐下一步

任何模式完成后，提供上下文相关的后续建议：

- After `static [name]`: “如果存在测试 spec，运行 `/skill-test spec [name]` 来验证行为正确性。”
- After `static all` with failures: “先处理 NON-COMPLIANT skills。可逐个运行 `/skill-test static [name]` 获取详细修复建议。”
- After `spec [name]` PASS: “更新 `CCGS Skill Testing Framework/catalog.yaml` 记录这次通过日期。也可以运行 `/skill-test audit` 找出下一个 spec 缺口。”
- After `spec [name]` FAIL: “查看失败断言，并更新 skill 或测试 spec 以修正不匹配。”
- After `audit`: “先处理 critical-priority 的缺口。使用 `CCGS Skill Testing Framework/templates/skill-test-spec.md` 模板创建新 spec。”
