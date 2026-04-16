# Agent / Skill Routing Matrix

> Updated: 2026-04-09  
> Scope: 明确 `core/` 与 `.claude/` 的功能重叠，避免重复触发

---

## 1) 清单概览

- `core/agents`: 8
- `core/skills`: 17
- `.claude/agents`: 49
- `.claude/skills`: 72
- 完全同名冲突: **0**

结论：**无同名冲突，有功能重叠**。

---

## 2) 重叠可见性（按代理 / 技能分开展示）

### 2.1 代理重叠热度（以 core 代理为基准）

- **HIGH (2/8)**: `planner`, `tdd-guide`
- **MEDIUM (4/8)**: `build-error-resolver`, `docs-lookup`, `doc-updater`, `refactor-cleaner`
- **LOW (2/8)**: `harness-optimizer`, `loop-operator`

### 2.2 技能重叠热度（以 core 技能为基准）

- **HIGH (5/17)**: `codebase-onboarding`, `blueprint`, `tdd-workflow`, `verification-loop`, `skill-stocktake`
- **MEDIUM (4/17)**: `documentation-lookup`, `context-budget`, `strategic-compact`, `agent-harness-construction`
- **LOW / NONE (8/17)**: `ai-first-engineering`, `agentic-engineering`, `bun-runtime`, `cost-aware-llm-pipeline`, `nutrient-document-processing`, `prompt-optimizer`, `regex-vs-llm-structured-text`, `search-first`

### 2.3 命令高冲突速查（core/commands）

| 命令 | 冲突对象 | 触发方式 | 默认路由 |
|---|---|---|---|
| `code-review` | `.claude/skills/code-review` | 主动（显式 `/code-review`） | 默认走 `.claude`（避免双审查） |
| `app-plan` | `sprint-plan` / `create-epics` / `create-stories` | 主动（显式 `/plan`） | 游戏流程走 `.claude` |
| `verify` | `gate-check` / `story-done` / `release-checklist` | 主动（显式 `/verify`） | 阶段门禁走 `.claude` |
| `quality-gate` | `gate-check` / `story-done` | 主动（显式 `/quality-gate`） | `.claude` 为主，`quality-gate` 作为补充 |
| `build-fix` | `hotfix`（部分场景） | 主动（显式 `/build-fix`） | 构建错误走 `build-fix`；线上紧急走 `.claude/hotfix` |

> 规则：命令冲突多数是“主动触发”，优先级低于被动冲突；同一轮只跑一条主链路，避免 `verify + gate-check`、`app-plan + sprint-plan` 同时触发。

### 2.4 被动触发冲突重点（优先治理）

以下项在未显式输入命令时也可能被语义触发，应优先标注和治理：

- **Agent（PROACTIVELY）**
  - `planner` ↔ `.claude` 规划链（`sprint-plan` / `create-epics` / `create-stories`）
  - `tdd-guide` ↔ `.claude` 测试验收链（`qa-plan` / `story-done` / `regression-suite`）
  - `build-error-resolver` ↔ `.claude` 故障修复流程（含 `hotfix` 场景）
  - `refactor-cleaner` ↔ `.claude` 技术债/重构流程（`tech-debt`）
  - `doc-updater` ↔ `.claude` 文档反推流程（`reverse-document`）

- **Skill（TRIGGER when）**
  - `blueprint` ↔ `.claude` 计划拆解链（`sprint-plan` / `create-epics` / `create-stories`）
  - `prompt-optimizer` ↔ 任务执行类请求（易与“直接执行”意图冲突）

- **Command（显式调用）**
  - 主要为主动冲突，默认降级处理（仅保留路由规则即可）。
---

## 3) 代理冲突矩阵（core 代理）

| Core Agent | `.claude` 重叠对象 | 主要重叠点 | 触发方式 | 处理优先级 | 冲突级别 | 默认路由 | 单轮策略 |
|---|---|---|---|---|---|---|---|
| `planner` | `producer`, `technical-director`, `lead-programmer`（及规划类 skills） | 计划拆解、实施路径设计 | **被动**（PROACTIVELY） | **P0 ⚠** | **HIGH** | 游戏生产流程优先 `.claude`；通用工程计划可用 `core/planner` | 同一轮只保留一个“主规划器” |
| `tdd-guide` | `qa-lead`, `qa-tester`（及 `qa-plan`/`story-done`/`regression-suite`） | 测试驱动、质量门禁、验收标准 | **被动**（PROACTIVELY） | **P0 ⚠** | **HIGH** | Story/Gate 场景优先 `.claude`；纯工程 TDD 可用 `core/tdd-guide` | 禁止并行触发两个测试主流程 |
| `build-error-resolver` | `devops-engineer`, `lead-programmer`, 引擎专项程序员 | 构建失败、类型错误修复 | **被动**（PROACTIVELY） | **P1 ⚠** | **MEDIUM** | 快速救火优先 `core/build-error-resolver` | 修复完成后再回到 `.claude` 流程 |
| `docs-lookup` | `godot-specialist`/`unity-specialist`/`unreal-specialist` | API/框架用法咨询 | 主动（按需调用） | P2 | **MEDIUM** | 通用库/API 文档优先 `core/docs-lookup`；引擎规则优先 `.claude` 引擎专家 | 若用户未说明，先问“通用库还是引擎问题” |
| `doc-updater` | `reverse-document`（skill） | 文档与实现同步 | **被动**（PROACTIVELY） | **P1 ⚠** | **MEDIUM** | code→docs 同步优先 `core/doc-updater`；implementation→design 反推优先 `.claude/reverse-document` | 单轮只走一个文档主链路 |
| `refactor-cleaner` | `lead-programmer`, `technical-director`（及 `tech-debt`） | 重构、清理、技术债处理 | **被动**（PROACTIVELY） | **P1 ⚠** | **MEDIUM** | 涉及游戏系统约束优先 `.claude`；纯代码清理可用 `core/refactor-cleaner` | 若影响多系统，升级到 `.claude` 评审链 |
| `harness-optimizer` | `skill-improve`, `skill-test`（间接） | 代理/工具链配置优化 | 主动（按需调用） | P3 | **LOW** | harness 级问题优先 `core/harness-optimizer` | 与业务实现任务分离执行 |
| `loop-operator` | `producer` + `team-*` 编排技能（间接） | 多任务循环与推进 | 主动（按需调用） | P3 | **LOW** | 生产协调用 `.claude` team skills；自动循环控制用 `core/loop-operator` | 不与主开发流混跑 |

---

## 4) 技能冲突矩阵（core 技能）

| Core Skill | `.claude` 重叠对象 | 主要重叠点 | 触发方式 | 处理优先级 | 冲突级别 | 默认路由 | 单轮策略 |
|---|---|---|---|---|---|---|---|
| `codebase-onboarding` | `start`, `adopt`, `onboard`, `project-stage-detect` | 仓库上手、状态理解、初始引导 | 主动（按需调用） | P2 | **HIGH** | 本仓库默认 `.claude` 优先 | 不并行跑两套 onboarding |
| `blueprint` | `sprint-plan`, `create-epics`, `create-stories`, `dev-story` | 计划拆解、任务分层 | **被动**（TRIGGER when） | **P0 ⚠** | **HIGH** | 游戏开发拆解优先 `.claude` | 明确“按 Sprint/Story 还是通用工程蓝图” |
| `tdd-workflow` | `test-setup`, `qa-plan`, `regression-suite`, `smoke-check`, `story-done` | 测试流程、覆盖率、验收证据 | 主动（按需调用） | P2 | **HIGH** | 有 story/gate 时优先 `.claude` | 只保留一个测试总流程 |
| `verification-loop` | `gate-check`, `release-checklist`, `story-done`, `smoke-check` | 完工前验证、发布前检查 | 主动（按需调用） | P2 | **HIGH** | 阶段门禁优先 `.claude` | 验证口径只选一套 |
| `skill-stocktake` | `skill-test`, `skill-improve` | 技能质量审计与修复 | 主动（按需调用） | P2 | **HIGH** | 模板技能治理优先 `.claude` | 单轮仅一个技能治理入口 |
| `documentation-lookup` | `setup-engine`（部分） | 文档查询与依据引用 | 主动（按需调用） | P2 | **MEDIUM** | 外部库/API 查询优先 `core`；引擎配置决策优先 `.claude` | 二义时先询问用户目标 |
| `context-budget` | `project-stage-detect`（部分信息审计） | 诊断类审计（目标不同） | 主动（按需调用） | P3 | **MEDIUM** | 上下文窗口优化优先 `core/context-budget` | 不与阶段检测混为一次输出 |
| `strategic-compact` | `.claude/docs/context-management.md`（流程原则） | 上下文压缩建议 | 主动（按需调用） | P3 | **MEDIUM** | 会话压缩策略优先 `core/strategic-compact` | 与业务交付分步执行 |
| `agent-harness-construction` | `setup-engine`（均涉及配置但对象不同） | 配置设计（对象不同） | 主动（按需调用） | P3 | **MEDIUM** | 代理 action space 设计优先 `core`；引擎配置优先 `.claude` | 先定对象再选技能 |
| `ai-first-engineering` | （无明确等价） | 工程方法论 | 主动（按需调用） | P3 | **LOW/NONE** | 按需使用 `core` | 可独立执行 |
| `agentic-engineering` | （无明确等价） | 代理工程执行方法 | 主动（按需调用） | P3 | **LOW/NONE** | 按需使用 `core` | 可独立执行 |
| `bun-runtime` | （仅与 `test-setup` 有边缘关联） | runtime/tooling 选型 | 主动（按需调用） | P3 | **LOW/NONE** | 按需使用 `core` | 独立执行 |
| `cost-aware-llm-pipeline` | （无明确等价） | LLM 成本优化 | 主动（按需调用） | P3 | **LOW/NONE** | 按需使用 `core` | 独立执行 |
| `nutrient-document-processing` | （无明确等价） | 文档处理（OCR/脱敏/签名等） | 主动（按需调用） | P3 | **LOW/NONE** | 按需使用 `core` | 独立执行 |
| `prompt-optimizer` | （无明确等价） | Prompt 优化 | **被动**（TRIGGER when） | **P1 ⚠** | **LOW/NONE** | 按需使用 `core` | 独立执行 |
| `regex-vs-llm-structured-text` | （无明确等价） | 结构化文本解析策略 | 主动（按需调用） | P3 | **LOW/NONE** | 按需使用 `core` | 独立执行 |
| `search-first` | （与若干研究型 skills 仅弱重叠） | 先搜索后实现 | 主动（按需调用） | P3 | **LOW/NONE** | 按需使用 `core` | 独立执行 |

---

## 5) 路由策略（默认）

1. **先看触发方式与优先级**：`被动触发 + P0/P1` 冲突先处理；`主动触发 + P2/P3` 可按需处理。
2. **Explicit command wins**：用户明确输入 `/xxx`，直接执行该 skill/command。
3. **Game workflow first (`.claude`)**：涉及 GDD/ADR/Epic/Story/Sprint/Gate/Release/QA Evidence 时，默认 `.claude`。
4. **General utility first (`core`)**：外部库 API 查询、build/type 错误救火、harness/context 优化，默认 `core`。
5. **One lane per turn**：同一轮避免并行触发两个同类主流程。
6. **Ambiguity ask-first**：二义场景先问“游戏流程版（.claude）还是通用工程版（core）”。
7. **Fallback**：首选链路失败后再切换到另一侧。

---

## 6) 常见意图路由

- “项目现在在哪个阶段” → `.claude/skills/project-stage-detect`
- “从零开始搭项目流程” → `.claude/skills/start`
- “旧项目迁移模板” → `.claude/skills/adopt`
- “某库 API 怎么用” → `core/skills/documentation-lookup`
- “先修 build/type 报错” → `core/agents/build-error-resolver`

---

## 7) Commands 冲突矩阵（core/commands vs .claude/skills）

### 7.1 盘点结论

- `core/commands`: 22
- `.claude/commands`: 0（目录不存在）
- 与 `.claude/skills` 的**同名冲突**: 1（`code-review`）

### 7.2 Commands 冲突清单

| core command | `.claude` 重叠对象 | 重叠点 | 触发方式 | 处理优先级 | 冲突级别 | 默认路由 | 策略 |
|---|---|---|---|---|---|---|---|
| `code-review` | `code-review` | 代码审查（同名同域） | 主动（显式 `/code-review`） | P2 | **HIGH** | `.claude/skills/code-review` | 固定优先 `.claude`，避免双审查 |
| `app-plan` | `sprint-plan`, `create-epics`, `create-stories` | 规划拆解、执行计划 | 主动（显式 `/plan`） | P2 | **HIGH** | 游戏开发用 `.claude` | 若是通用工程计划再用 `app-plan` |
| `verify` | `gate-check`, `story-done`, `release-checklist` | 验证与放行 | 主动（显式 `/verify`） | P2 | **HIGH** | 阶段门禁走 `.claude` | 不同时运行两套验收口径 |
| `quality-gate` | `gate-check`, `story-done` | 质量门禁 | 主动（显式 `/quality-gate`） | P2 | **HIGH** | `.claude` 为主 | `quality-gate` 作为快速补充检查 |
| `build-fix` | `hotfix`（部分场景） | 故障修复/恢复可用 | 主动（显式 `/build-fix`） | P2 | **HIGH** | 纯构建报错用 `build-fix`；线上紧急流程用 `.claude/hotfix` | 先定场景再选链路 |
| `docs` | `help`, `setup-engine`（部分） | 文档查询/指导 | 主动（显式 `/docs`） | P3 | **MEDIUM** | 通用库文档用 `docs` | 引擎配置或阶段指导走 `.claude` |
| `test-coverage` | `qa-plan`, `regression-suite`, `test-setup` | 测试覆盖与测试计划 | 主动（显式 `/test-coverage`） | P3 | **MEDIUM** | 测试治理用 `.claude` | 覆盖率专项可单独用 `test-coverage` |
| `update-docs` | `reverse-document` | 文档产出 | 主动（显式 `/update-docs`） | P3 | **MEDIUM** | code→docs 用 `update-docs` | implementation→design 用 `reverse-document` |
| `update-codemaps` | `reverse-document`（部分） | 结构文档/映射产出 | 主动（显式 `/update-codemaps`） | P3 | **MEDIUM** | codemap 用 `update-codemaps` | 设计反推仍走 `.claude` |
| `context-budget` | `scope-check`（弱重叠） | 诊断分析 | 主动（显式 `/context-budget`） | P3 | **LOW** | 上下文优化用 `context-budget` | 与范围审计分离执行 |

### 7.3 Commands 路由补充规则

1. **同名命令冲突固定路由**：`code-review` 默认走 `.claude/skills/code-review`。
2. **流程型指令优先 `.claude`**：计划、门禁、发布、故事验收。
3. **工具型指令优先 `core/commands`**：会话管理、包管理、构建救火、prompt/harness 工具。
4. **一轮只走一个主链路**：避免同轮同时跑 `verify` + `gate-check`、`app-plan` + `sprint-plan`。

---

## 8) 参考

- `core/agents/`
- `core/skills/`
- `core/commands/`
- `.claude/agents/`
- `.claude/skills/`
- `.claude/docs/coordination-rules.md`
