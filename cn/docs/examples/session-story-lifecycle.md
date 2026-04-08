# 示例会话：完整故事生命周期 —— /story-readiness → 实现 → /story-done

**上下文：** 单人独立开发者，处于生产中期冲刺。移动系统的 GDD 和架构都已经完成。`/create-stories` 已经生成了一个关于移动核心实现的故事。

**起始状态：**
- `design/gdd/movement-system.md` —— 完整，8 个部分全部齐全
- `docs/architecture/movement-adr-001.md` —— 状态：Accepted
- `production/sprints/sprint-03.md` —— 待办中列出了 STORY-MOV-001
- `production/stories/STORY-MOV-001.md` —— 已存在，但还没验证
- 还没有实现代码

**会话时长：** 约 50 分钟
**轮数：** 13
**结果：** 故事验证为可做，实现完成，并通过 `/story-done` 验收关闭

---

## 第 1 阶段：故事就绪检查

### 第 1 轮：用户运行就绪检查

**User：**
> /story-readiness production/stories/STORY-MOV-001.md

### 第 2 轮：智能体验证故事

**Agent（通过 /story-readiness）：**
> 正在读取 `production/stories/STORY-MOV-001.md`……
>
> **STORY-MOV-001：实现带地形修正的 CharacterBody2D 移动**
>
> 正在运行 4 项验证：
>
> **1. 设计完整性**
> - 引用的 GDD：`design/gdd/movement-system.md` ✅
> - GDD 部分覆盖：Detailed Rules ✅、Formulas ✅、Edge Cases ✅
> - 已嵌入 TR-ID：TR-MOV-001 到 TR-MOV-008 ✅
>
> **2. 架构完整性**
> - 引用的 ADR：`docs/architecture/movement-adr-001.md` ✅
> - ADR 状态：**Accepted** ✅ *（如果还是 Proposed，这里会被 BLOCKED）*
> - 故事中的控制清单版本：`2026-03-10` —— 当前清单也是 `2026-03-10` ✅
>
> **3. 范围清晰度**
> - 验收标准：9 条，全部可度量 ✅
> - 列出的范围外项：游泳、攀爬 ✅
> - 发现 1 个歧义：
>   - ⚠️ 故事写的是“翻滚方向跟随最后输入方向”，但 GDD 写的是“沿移动方向翻滚”——当玩家停住后立刻翻滚时这两者会冲突。接手前需要澄清。
>
> **4. 完成定义**
> - 需要测试：公式函数的单元测试 ✅
> - 集成信号：`on_stamina_event` 必须正确触发 ✅
>
> ---
> **结论：NEEDS WORK**
>
> 需要先解决这个歧义，才能开始实现。你要现在就把它修掉，让我把故事标成 ready 吗？

### 第 3 轮：用户解决歧义

**User：**
> 翻滚使用最后的移动方向。如果玩家站着不动，翻滚则使用当前面朝方向。

### 第 4 轮：智能体更新故事

**Agent：**
> 正在更新故事里的 Detailed Rules：
>
> > 翻滚方向：最后的移动方向。如果在翻滚输入时速度为 0，则使用当前面朝方向。
>
> 我可以把它写进 `production/stories/STORY-MOV-001.md`，并把 Status 设为 `ready-for-dev` 吗？

**User：**
> Yes

**Agent 写入更新。故事状态：`ready-for-dev`。**

> **结论：READY**
>
> 故事已经可以实现了。你准备好就可以接手。

---

## 第 2 阶段：实现

### 第 5 轮：用户开始实现

**User：**
> 我们来实现 STORY-MOV-001。我准备开始写代码了。

### 第 6 轮：智能体读取故事和 ADR

**Agent（gameplay-programmer）：**
> 正在读取 `production/stories/STORY-MOV-001.md`、`design/gdd/movement-system.md` 和 `docs/architecture/movement-adr-001.md`……
>
> **架构（来自 ADR-001）：**
> - `MovementComponent.gd` —— 挂在玩家场景上，不做单例
> - 地形修正查询通过 `TerrainLayer.get_modifier(tile_position)` 辅助函数完成
> - 耐力事件通过 signal 发出（不是直接调用 StaminaSystem）
>
> **我建议的文件结构：**
> ```text
> src/gameplay/movement/
>   movement_component.gd       # CharacterBody2D 逻辑、状态机
>   terrain_modifier_table.gd   # 常量表：terrain_type -> {speed_mod, drain_mod}
> tests/unit/
>   test_movement_formulas.gd   # 速度/消耗公式的单元测试
> ```
>
> 我可以按这个结构继续吗？

**User：**
> Yes

### 第 7 轮：智能体实现并展示关键代码

**Agent：**
> 我正在实现 `movement_component.gd`。下面是你在我写文件前先看一眼的关键片段：
>
> ```gdscript
> class_name MovementComponent
> extends Node
>
> signal stamina_event(type: String, amount: float)
>
> @export var base_walk_speed: float = 120.0
> @export var run_multiplier: float = 1.7
> @export var stamina_drain_walk: float = 2.0
> @export var stamina_drain_run: float = 6.0
> @export var stamina_cost_roll: float = 15.0
>
> var _is_carrying_heavy: bool = false
>
> func _physics_process(delta: float) -> void:
>     var terrain_mod := _get_terrain_modifier()
>     var effective_speed := _calculate_speed(terrain_mod)
>     # ...
> ```
>
> 所有数值都来自 `@export` —— 没有硬编码。这个方向符合你的想法吗？

**User：**
> 看起来不错。写吧。

### 第 8–9 轮：智能体写文件和测试

**Agent 写入：**
- `src/gameplay/movement/movement_component.gd`
- `src/gameplay/movement/terrain_modifier_table.gd`
- `tests/unit/test_movement_formulas.gd`

**Agent：**
> 文件已写入。正在运行可用的 lint 检查……
>
> 没有错误。测试文件已创建，包含 6 个单元测试，覆盖：
> - 步行速度公式（3 种地形）
> - 奔跑速度公式
> - 耐力消耗计算
> - 翻滚耐力消耗（含零速度边缘情况）
>
> 还需要手工测试的部分：无敌帧、坡度阻挡、地形集成（需要跑场景）。

---

## 第 3 阶段：故事完成

### 第 10 轮：用户手动测试并运行 /story-done

**User：**
> 我已经在场景里测试过了——一切正常。/story-done production/stories/STORY-MOV-001.md

### 第 11 轮：智能体运行完成审查

**Agent（通过 /story-done）：**
> 正在读取故事、GDD、ADR……
>
> **阶段 1：找到故事** ✅ `production/stories/STORY-MOV-001.md`
>
> **阶段 2：验收标准验证**
>
> | # | 标准 | 验证方式 | 状态 |
> |---|-----------|--------------|--------|
> | 1 | 普通地面上的步行速度正确 | 自动：公式单元测试通过 | ✅ AUTO |
> | 2 | 奔跑速度正确 | 自动：公式单元测试通过 | ✅ AUTO |
> | 3 | 耐力为 0 时会取消奔跑 | 手工：用户确认 | ✅ MANUAL |
> | 4 | 翻滚无敌帧正确 | 手工：用户确认 | ✅ MANUAL |
> | 5 | 地形修正正确应用 | 手工：用户确认 | ✅ MANUAL |
> | 6 | 搬运重物会禁用奔跑 | 自动：尚不可测（库存未集成） | ⏳ DEFERRED |
> | 7 | 耐力信号正确触发 | 自动：集成测试待做 | ⏳ DEFERRED |
> | 8 | 没有硬编码值 | 自动：grep 查 magic number → 0 个 | ✅ AUTO |
> | 9 | 斜率 >45° 会阻挡移动 | 手工：用户确认 | ✅ MANUAL |
>
> **阶段 3：GDD/ADR 偏差**
>
> 扫描实现与 TR-ID 的一致性……
>
> - TR-MOV-001 到 TR-MOV-007：✅ 按规范实现
> - TR-MOV-008（heavy carry signal）：⚠️ ADVISORY —— 延期到 inventory 集成故事。不是偏差，只是当前还无法验证。
>
> **阶段 4：清单过期检查**
>
> 故事控制清单版本 `2026-03-10` 与当前清单 `2026-03-10` 一致。✅
>
> **阶段 5：代码审查提示**
>
> 建议在标记完成前先运行 `/code-review src/gameplay/movement/`。不是阻塞项。
>
> ---
> **完成报告：COMPLETE WITH NOTES**
>
> 故事已完成。两项标准延期到 inventory 集成——记录为延期，不是阻塞。
>
> 我可以把故事状态更新为 `Status: Complete`，添加完成备注，并更新 `production/sprint-status.yaml` 吗？

**User：**
> Yes

### 第 12 轮：智能体关闭故事

**Agent 写入：**
- 故事 `Status: Complete` + 完成备注（注明延期标准）
- `production/sprint-status.yaml` —— 将 STORY-MOV-001 标记为 `done`

**Agent：**
> STORY-MOV-001 已关闭。
>
> **延期标准已记录**（会在 inventory 集成故事中自动浮现）：
> - 搬运重物会禁用奔跑（需要 inventory 信号）
> - 耐力信号集成测试（需要 stamina 系统）
>
> **冲刺里下一个就绪故事：**
> - STORY-MOV-002：Stamina 系统 —— 这是逻辑上的下一个故事（下游依赖现在已经解锁）
> - STORY-HUD-001：移动 HUD 指示器 —— 也已解锁
>
> 下一步运行 `/story-readiness`，看看你想先接哪一个。

---

## 这个示例展示了什么

- **就绪门禁能抓到真实问题**：如果没有 `/story-readiness`，翻滚方向歧义会变成一个很晚才暴露的实现决策。
- **ADR 状态是硬门禁**：如果 `movement-adr-001.md` 还是 `Proposed` 而不是 `Accepted`，故事会被标成 `BLOCKED`，实现不会开始。
- **延期标准**：不是每个验收标准都能在故事结束时验证；`/story-done` 会追踪延期项，而不是把完成卡住。
- **TR-ID 引用**：故事存的是 `TR-MOV-001` 这类 ID，而不是照抄 GDD 文本——这样以后 GDD 文字清理时不会产生假偏差。
- **sprint-status.yaml**：冲刺状态的单一事实来源，由 `/story-done` 更新，由 `/sprint-status` 读取。
- **清单版本检查**：确保故事的实现指导没有偏离当前架构决策。
