# Docs 目录

在编写或编辑此目录下的文件时，请遵循这些标准。

## 架构决策记录（`docs/architecture/`）

使用 ADR 模板：`.claude/docs/templates/architecture-decision-record.md`

**必需部分：** 标题、状态、上下文、决策、后果、ADR 依赖、引擎兼容性、GDD 需求对应项

**状态生命周期：** `Proposed` → `Accepted` → `Superseded`
- 绝不要跳过 `Accepted` —— 引用仍为 `Proposed` 的 ADR 的故事会被自动阻塞
- 使用 `/architecture-decision` 通过引导流程创建 ADR

**TR Registry：** `docs/architecture/tr-registry.yaml`
- 稳定的需求 ID（例如 `TR-MOV-001`），用于把 GDD 需求连接到故事
- 不要重编号既有 ID —— 只追加新 ID
- 由 `/architecture-review` 第 8 阶段更新

**Control Manifest：** `docs/architecture/control-manifest.md`
- 面向程序员的扁平规则清单：按层级列出 Required / Forbidden / Guardrails
- 头部包含带日期的 `Manifest Version:`
- 故事会嵌入这个版本；`/story-done` 会检查是否过期

**验证：** 在完成一组 ADR 后运行 `/architecture-review`。

## 引擎参考（`docs/engine-reference/`）

带版本固定的引擎 API 快照。**在使用任何引擎 API 之前都要先检查这里**——LLM 的训练数据早于固定的引擎版本。

当前引擎：见 `docs/engine-reference/godot/VERSION.md`