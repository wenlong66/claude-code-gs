# Agent / Skill Routing Matrix

> Updated: 2026-04-08
> Scope: resolve functional overlap between `core/` and `.claude/`

## 1) Inventory Snapshot

- `core/agents`: 8
- `core/skills`: 17
- `.claude/agents`: 49
- `.claude/skills`: 72
- Exact name collision: **0**

结论：当前不存在“同名冲突”，但存在多处“功能重叠/职责相邻”。

---

## 2) Conflict Matrix (Functional Overlap)

| Capability Area | core (general) | .claude (game workflow) | Conflict Level | Default Route |
|---|---|---|---|---|
| Onboarding / 项目理解 | `codebase-onboarding` | `start`, `adopt`, `onboard`, `project-stage-detect` | High | **.claude first** |
| Planning / 拆解 | `blueprint`, `planner` | `sprint-plan`, `create-epics`, `create-stories`, `dev-story` | High | **.claude first** |
| TDD / QA / 验收 | `tdd-workflow`, `verification-loop`, `tdd-guide` | `test-setup`, `qa-plan`, `regression-suite`, `smoke-check`, `story-done` | High | **.claude first** |
| Docs/API 查询 | `documentation-lookup`, `docs-lookup` | （无同等外部库 API 查询主技能） | Medium | **core first** |
| Build/Type Error 修复 | `build-error-resolver` | （流程类技能为主） | Medium-Low | **core first** |
| 文档同步与结构图 | `doc-updater` | `reverse-document` | Medium | code→docs 用 core；impl→design 用 .claude |
| Harness/Context 优化 | `harness-optimizer`, `context-budget` | `skill-improve`, `skill-test` | Low | 按目标分流 |

---

## 3) Routing Rules (Default Policy)

1. **Explicit command wins**: 用户明确输入 `/xxx` 时，直接执行该 skill。
2. **Game production workflow => `.claude`**:
   - GDD / ADR / Epic / Story / Sprint / Stage Gate / Release / QA Evidence
3. **General engineering utility => `core`**:
   - 外部库/API 文档查询、构建报错救火、Harness 优化、上下文预算审计
4. **Single path per turn**:
   - 同一轮不要并行触发两个同类技能（避免互相覆盖）。
5. **Ask on ambiguity**:
   - 二义场景先问：走“游戏流程版（.claude）”还是“通用工程版（core）”。
6. **Fallback policy**:
   - 首选链路失败后，再切换到另一侧等价能力。
7. **Naming guardrail**:
   - 新增 skill/agent 命名避免与另一侧形成同义重复（尤其 onboarding/planning/tdd）。

---

## 4) Quick Intent Mapping

- “项目现在处于哪个阶段” → `.claude/skills/project-stage-detect`
- “从零开始搭流程” → `.claude/skills/start`
- “旧项目迁移到模板” → `.claude/skills/adopt`
- “某库 API 怎么用” → `core/skills/documentation-lookup`
- “先把 build/type error 修好” → `core/agents/build-error-resolver`

---

## 5) Operational Guidance

- 本仓库为 Game Studios 模板，默认策略：
  - **主流程用 `.claude`**
  - **工具能力补充用 `core`**
- 若后续新增技能导致新重叠，优先更新本文件后再启用。

---

## 6) File References

- `core/agents/`
- `core/skills/`
- `.claude/agents/`
- `.claude/skills/`
- `.claude/docs/coordination-rules.md`
