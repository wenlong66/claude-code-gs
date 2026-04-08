# 示例会话：/gate-check 阶段转换 —— 系统设计 → 技术准备

**上下文：** 单人独立开发者，项目第 5 周末。系统设计阶段看起来已经完成——6 个 MVP GDD 已写好，跨审查完成，引擎也已设置。用户想正式推进到技术准备阶段。

**起始状态：**
- `production/stage.txt` —— 当前为 `systems-design`
- `design/gdd/systems-index.md` —— 列出了 6 个 MVP 系统，全部标记为 `Status: GDD Complete`
- `design/gdd/` —— 6 个 GDD 文件都存在
- `design/gdd/gdd-cross-review-2026-03-10.md` —— 跨审查报告，结论：CONCERNS（1 条低优先级备注）
- 引擎已配置（Godot 4.6，已完成 `/setup-engine`）

**会话时长：** 约 20 分钟
**轮数：** 7
**结果：** 门禁通过，`stage.txt` 更新为 `technical-setup`，并给出下一步的清晰列表

---

## 第 1 轮：用户启动门禁检查

**User：**
> /gate-check

## 第 2 轮：智能体识别当前阶段并执行检查

**Agent（通过 /gate-check）：**
> 正在读取 `production/stage.txt` —— 当前阶段：**systems-design**
>
> 正在运行门禁：**Systems Design → Technical Setup**
>
> ---
> **必需工件清单：**
>
> | 工件 | 要求 | 状态 |
> |----------|-------------|--------|
> | `design/gdd/systems-index.md` | 存在，且列出所有 MVP 系统 | ✅ |
> | 各系统 GDD | 所有 MVP 系统都有 GDD | ✅（6/6） |
> | 每个 GDD 的 `/design-review` | 每个 GDD 都被审查过 | ✅（找到 6 份审查意见） |
> | 跨 GDD 审查报告 | 存在 `design/gdd/gdd-cross-review-*.md` | ✅ |
> | 跨审查结论 | PASS 或 CONCERNS（不能是 FAIL） | ✅ CONCERNS |
> | 引擎已配置 | `production/stage.txt` 或 CLAUDE.md 中有引擎条目 | ✅ Godot 4.6 |
>
> ---
> **内容扫描：**
>
> 检查 GDD 完整性（每个都必须有 8 个部分）……
>
> | GDD | 缺失部分 |
> |-----|-----------------|
> | movement-system.md | 无 ✅ |
> | stamina-system.md | 无 ✅ |
> | combat-system.md | 无 ✅ |
> | inventory-system.md | 无 ✅ |
> | crafting-system.md | 无 ✅ |
> | exploration-system.md | 无 ✅ |
>
> ---
> **跨审查备注（来自 `gdd-cross-review-2026-03-10.md`）：**
>
> 1. ⚠️ LOW —— Crafting 和 inventory 都独立定义了“item stack size”，但默认值不同（crafting: 99，inventory: 64）。应该由其中一个系统作为权威，另一个系统引用它。不是阻塞项——可以在 ADR 中解决。
>
> ---
> **结论：PASS**
>
> 所有必需工件都已存在。跨审查备注严重度很低，可以在技术准备阶段通过 ADR 解决。这在这个阶段是正常发现。
>
> **我可以把 `production/stage.txt` 推进到 `technical-setup` 吗？**

## 第 3 轮：用户确认

**User：**
> Yes, advance it.

## 第 4 轮：智能体更新阶段并给出下一步

**Agent：**
> 已将 `production/stage.txt` 更新为 `technical-setup`
>
> ---
> **你现在处于：技术准备**
>
> 这个阶段用于在开始生产编码前建立技术基础。目标是产出完整、已批准的架构，让预生产阶段写出的每个故事都有清晰、无歧义的技术指导。
>
> **本阶段必需步骤（按顺序）：**
>
> 1. **`/create-architecture`** —— 编写总架构文档。涵盖系统拆分、数据流、层边界和模块职责。
>
> 2. **`/architecture-decision`（每个重要技术选择都要做一次）** —— 至少包括：
>    - 渲染方式（2D 摄像机、viewport 等）
>    - 存档/读档策略
>    - 音频 bus 架构
>    - 跨审查里发现的“item stack size 权威来源”问题（crafting vs inventory）
>
> 3. **`/architecture-review`** —— 验证所有 ADR 是否完整、依赖顺序是否正确，以及是否能追溯到 GDD。会生成 TR 注册表。
>
> 4. **`/create-control-manifest`** —— 把已接受的 ADR 转成一份扁平的程序员规则表。实现型智能体会在编码时查它。
>
> 5. **`/gate-check`** —— 技术准备 → 预生产 门禁。要求：架构文档、所有 ADR 已 Accepted、控制清单、并解决依赖顺序问题。
>
> **可选但推荐：**
> - 如果你有计划带到正式项目中的原型代码，可以先跑 `/tech-debt`
> - 如果还没拉取 Godot 4.6 API 快照，可以重新运行 `/setup-engine`
>
> **提示：** 先对 item stack size 冲突跑 `/architecture-decision`，这是个很快的胜利，能在两个 ADR 里都写入前把悬而未决的问题收掉。

## 第 5 轮：用户询问跨审查备注

**User：**
> 那我到底要在 ADR 里怎么写这个 stack size 冲突？

## 第 6 轮：智能体建议

**Agent：**
> 这份 ADR 要决定的是：**哪个系统拥有 canonical 的 `max_stack_size` 值？**
>
> 有两个可考虑的方案：
>
> **选项 A：Inventory 拥有它**
> - `ItemData` 资源（由 inventory 拥有）新增 `max_stack_size: int = 64`
> - Crafting 系统从 `ItemData` 读取，绝不自己设置这个值
> - 优点：inventory 是所有物品属性的单一来源
> - 缺点：crafting 团队需要知道去 inventory 数据里找
>
> **选项 B：Item data 资源拥有它（共享资源）**
> - `ItemData.max_stack_size` 成为 crafting 和 inventory 的共同权威
> - 两个系统都从 `ItemData` 导入
> - 优点：单一来源，没有 crafting 和 inventory 模块之间的耦合
> - 缺点：共享数据层里又多了一项
>
> 对于一个单人项目，很多团队最终会选 B（共享资源），尤其是在已经有 2 个以上系统都碰 item data 时。不过这两种都有效。
>
> 运行 `/architecture-decision` 后，它会引导你填写 ADR 格式，包括 Dependencies 部分，把这项决策链接回两个 GDD。

## 第 7 轮：用户结束

**User：**
> 明白了。我先用 /architecture-decision 处理这个。

**Agent：**
> 这是个很好的起点。ADR 会记录这个决策、理由，以及它对应的 GDD 需求——这样几个月后你再写代码时，理由也不会丢。
>
> 你的阶段门禁已经记录。你在技术准备阶段的任何时候都可以运行 `/help`，查看自己相对于必需清单的当前进度。

---

## 这个示例展示了什么

- **门禁检查是自动的，不是手工表单**：智能体会自己读工件并检查——用户不用填一张表。
- **CONCERNS ≠ FAIL**：跨审查备注是 LOW 严重度，因此门禁通过。只有 FAIL 才需要先解决才能推进。
- **stage.txt 是权威**：状态行、`/help` 和所有技能都读取 `production/stage.txt`——这里更新后，后续所有技能看到的阶段都会变。
- **下一步是阶段专属的**：智能体不会给你一句泛泛的“祝你好运”——而是给出专门面向技术准备的顺序清单。
- **门禁会把后续工作具体化**：stack size 冲突原本是跨审查备注；门禁检查会确保它变成一条明确的 ADR，而不是被遗忘。
- **每次门禁只推进一次**：用户必须明确确认推进。门禁不会自动跳阶段；仍然需要人工确认。
