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

---

## 3) 代理冲突矩阵（core 代理）

| Core Agent | `.claude` 重叠对象 | 主要重叠点 | 冲突级别 | 默认路由 | 单轮策略 |
|---|---|---|---|---|---|
| `planner` | `producer`, `technical-director`, `lead-programmer`（及规划类 skills） | 计划拆解、实施路径设计 | **HIGH** | 游戏生产流程优先 `.claude`；通用工程计划可用 `core/planner` | 同一轮只保留一个“主规划器” |
| `tdd-guide` | `qa-lead`, `qa-tester`（及 `qa-plan`/`story-done`/`regression-suite`） | 测试驱动、质量门禁、验收标准 | **HIGH** | Story/Gate 场景优先 `.claude`；纯工程 TDD 可用 `core/tdd-guide` | 禁止并行触发两个测试主流程 |
| `build-error-resolver` | `devops-engineer`, `lead-programmer`, 引擎专项程序员 | 构建失败、类型错误修复 | **MEDIUM** | 快速救火优先 `core/build-error-resolver` | 修复完成后再回到 `.claude` 流程 |
| `docs-lookup` | `godot-specialist`/`unity-specialist`/`unreal-specialist` | API/框架用法咨询 | **MEDIUM** | 通用库/API 文档优先 `core/docs-lookup`；引擎规则优先 `.claude` 引擎专家 | 若用户未说明，先问“通用库还是引擎问题” |
| `doc-updater` | `reverse-document`（skill） | 文档与实现同步 | **MEDIUM** | code→docs 同步优先 `core/doc-updater`；implementation→design 反推优先 `.claude/reverse-document` | 单轮只走一个文档主链路 |
| `refactor-cleaner` | `lead-programmer`, `technical-director`（及 `tech-debt`） | 重构、清理、技术债处理 | **MEDIUM** | 涉及游戏系统约束优先 `.claude`；纯代码清理可用 `core/refactor-cleaner` | 若影响多系统，升级到 `.claude` 评审链 |
| `harness-optimizer` | `skill-improve`, `skill-test`（间接） | 代理/工具链配置优化 | **LOW** | harness 级问题优先 `core/harness-optimizer` | 与业务实现任务分离执行 |
| `loop-operator` | `producer` + `team-*` 编排技能（间接） | 多任务循环与推进 | **LOW** | 生产协调用 `.claude` team skills；自动循环控制用 `core/loop-operator` | 不与主开发流混跑 |

---

## 4) 技能冲突矩阵（core 技能）

| Core Skill | `.claude` 重叠对象 | 主要重叠点 | 冲突级别 | 默认路由 | 单轮策略 |
|---|---|---|---|---|---|
| `codebase-onboarding` | `start`, `adopt`, `onboard`, `project-stage-detect` | 仓库上手、状态理解、初始引导 | **HIGH** | 本仓库默认 `.claude` 优先 | 不并行跑两套 onboarding |
| `blueprint` | `sprint-plan`, `create-epics`, `create-stories`, `dev-story` | 计划拆解、任务分层 | **HIGH** | 游戏开发拆解优先 `.claude` | 明确“按 Sprint/Story 还是通用工程蓝图” |
| `tdd-workflow` | `test-setup`, `qa-plan`, `regression-suite`, `smoke-check`, `story-done` | 测试流程、覆盖率、验收证据 | **HIGH** | 有 story/gate 时优先 `.claude` | 只保留一个测试总流程 |
| `verification-loop` | `gate-check`, `release-checklist`, `story-done`, `smoke-check` | 完工前验证、发布前检查 | **HIGH** | 阶段门禁优先 `.claude` | 验证口径只选一套 |
| `skill-stocktake` | `skill-test`, `skill-improve` | 技能质量审计与修复 | **HIGH** | 模板技能治理优先 `.claude` | 单轮仅一个技能治理入口 |
| `documentation-lookup` | `setup-engine`（部分） | 文档查询与依据引用 | **MEDIUM** | 外部库/API 查询优先 `core`；引擎配置决策优先 `.claude` | 二义时先询问用户目标 |
| `context-budget` | `project-stage-detect`（部分信息审计） | 诊断类审计（目标不同） | **MEDIUM** | 上下文窗口优化优先 `core/context-budget` | 不与阶段检测混为一次输出 |
| `strategic-compact` | `.claude/docs/context-management.md`（流程原则） | 上下文压缩建议 | **MEDIUM** | 会话压缩策略优先 `core/strategic-compact` | 与业务交付分步执行 |
| `agent-harness-construction` | `setup-engine`（均涉及配置但对象不同） | 配置设计（对象不同） | **MEDIUM** | 代理 action space 设计优先 `core`；引擎配置优先 `.claude` | 先定对象再选技能 |
| `ai-first-engineering` | （无明确等价） | 工程方法论 | **LOW/NONE** | 按需使用 `core` | 可独立执行 |
| `agentic-engineering` | （无明确等价） | 代理工程执行方法 | **LOW/NONE** | 按需使用 `core` | 可独立执行 |
| `bun-runtime` | （仅与 `test-setup` 有边缘关联） | runtime/tooling 选型 | **LOW/NONE** | 按需使用 `core` | 独立执行 |
| `cost-aware-llm-pipeline` | （无明确等价） | LLM 成本优化 | **LOW/NONE** | 按需使用 `core` | 独立执行 |
| `nutrient-document-processing` | （无明确等价） | 文档处理（OCR/脱敏/签名等） | **LOW/NONE** | 按需使用 `core` | 独立执行 |
| `prompt-optimizer` | （无明确等价） | Prompt 优化 | **LOW/NONE** | 按需使用 `core` | 独立执行 |
| `regex-vs-llm-structured-text` | （无明确等价） | 结构化文本解析策略 | **LOW/NONE** | 按需使用 `core` | 独立执行 |
| `search-first` | （与若干研究型 skills 仅弱重叠） | 先搜索后实现 | **LOW/NONE** | 按需使用 `core` | 独立执行 |

---

## 5) 路由策略（默认）

1. **Explicit command wins**：用户明确输入 `/xxx`，直接执行该 skill。
2. **Game workflow first (`.claude`)**：涉及 GDD/ADR/Epic/Story/Sprint/Gate/Release/QA Evidence 时，默认 `.claude`。
3. **General utility first (`core`)**：外部库 API 查询、build/type 错误救火、harness/context 优化，默认 `core`。
4. **One lane per turn**：同一轮避免并行触发两个同类主流程。
5. **Ambiguity ask-first**：二义场景先问“游戏流程版（.claude）还是通用工程版（core）”。
6. **Fallback**：首选链路失败后再切换到另一侧。

---

## 6) 常见意图路由

- “项目现在在哪个阶段” → `.claude/skills/project-stage-detect`
- “从零开始搭项目流程” → `.claude/skills/start`
- “旧项目迁移模板” → `.claude/skills/adopt`
- “某库 API 怎么用” → `core/skills/documentation-lookup`
- “先修 build/type 报错” → `core/agents/build-error-resolver`

---

## 7) 参考

- `core/agents/`
- `core/skills/`
- `.claude/agents/`
- `.claude/skills/`
- `.claude/docs/coordination-rules.md`
