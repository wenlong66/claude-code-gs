# 交互模式库: [Game Title]

> **状态**: Draft | Stable | Under Revision
> **作者**: [ux-designer]
> **最后更新**: [Date]
> **版本**: [1.0]
> **引擎**: [Godot 4.6 / Unity 6 / Unreal Engine 5]
> **UI 框架**: [Godot Control nodes / Unity UI Toolkit / Unreal UMG]
> **相关文档**:
> - `docs/art-bible.md` — 视觉标准（颜色、排版、图标）
> - `docs/accessibility-requirements.md` — 各功能的无障碍承诺
> - `docs/ux/ux-spec-[screen].md` — 引用这些模式的单独界面规格

> **为什么存在这份文档**：每一份 UI 界面规格都应该能写“使用 Button (Primary) 模式”，而不是从头重新规定悬停状态、按压动画、焦点行为、键盘处理和屏幕阅读器播报。本库是可复用交互行为的唯一事实来源。当某个界面规格引用了模式名称，程序员就来这里查找。当行为发生变化时，它只在这里变更，并应用到所有使用处。
>
> 这是一份持续维护的文档。随着新界面的设计，会不断添加新模式——在设计新交互之前，务必先检查这里。如果确实需要新模式，请先把它添加到这里（或提交给 ux-designer）再去编写第一个使用它的界面规格。
>
> **状态定义**：
> - **Draft**：交互已定义，但尚未实现或验证
> - **Stable**：已实现、测试并在至少一个已发售界面中验证
> - **Deprecated**：正在淘汰——现有用法会迁移，新界面不要再使用

---

## 如何使用本库

**如果你在设计一个界面**：在发明新交互之前，先浏览下面的模式目录索引。当某个标准模式适用时，在界面规格中直接引用它的名称（例如：“确认按钮使用 Button (Primary) 模式”）。如果没有现成模式适用，就提议一个新模式——在这里记录它，或者在引入它的界面规格之前/同时记录。

**如果你在实现一个界面**：当界面规格写着“使用 [PatternName] 模式”时，到本文档查找完整规范。实现说明部分包含引擎相关指导。无障碍部分包含不可妥协的要求。

**如果你在审查一个界面规格**：检查所有交互元素是否都引用了本库中的某个模式，或者是否提供了自己的完整交互规范。“标准按钮”或“通常那样”都不是有效引用。

**如果你在更新某个模式**：更改一个 Stable 模式会影响所有使用它的界面。在修改之前，先审计所有用法（在界面规格中搜索该模式名），评估影响，获得 ux-designer 的批准，并在实现改动之前或同时更新本文档。

---

## 模式目录索引

> 每次向本文档添加新模式时，都要在这里新增一行。
> “Used In” 列是用法审计记录——当新界面采用该模式时要更新它。

| Pattern Name | Category | Description | Used In (Screens) | Status |
|-------------|----------|-------------|------------------|--------|
| Button (Primary) | Input | 主要行动号召。视觉权重最高。每个界面最多一个。 | [Main Menu, Pause Menu, Settings] | Draft |
| Button (Secondary) | Input | 备用或取消动作。视觉权重低于 Primary。 | [All modal dialogs, settings screens] | Draft |
| Button (Destructive) | Input | 不可逆动作。执行前必须确认。 | [Delete Save, Reset Settings] | Draft |
| Toggle | Input | 二元开/关状态选择。 | [Accessibility settings, audio settings] | Draft |
| Slider | Input | 连续值选择。 | [Volume controls, brightness, text size] | Draft |
| Dropdown / Select | Input | 从离散选项列表中进行选择。 | [Resolution, language, key binding] | Draft |
| List Item | Layout / Input | 可滚动垂直列表中的可选行。 | [Achievements, quest log, settings list] | Draft |
| Grid Item | Layout / Input | 二维网格中的可选单元格。 | [Inventory, ability select, item shop] | Draft |
| Modal Dialog | Feedback / Layout | 需要明确决策的阻塞式覆盖层。 | [Confirmation dialogs, error prompts] | Draft |
| Confirmation Dialog | Feedback / Layout | 用于危险动作确认的特定模态框。 | [Delete Save, Leave Match, Reset] | Draft |
| Toast / Notification | Feedback | 屏幕角落里非阻塞的临时消息。 | [Achievement unlock, autosave notification] | Draft |
| Tooltip | Feedback | 悬停或聚焦时出现的上下文信息。 | [Inventory items, ability descriptions, settings] | Draft |
| Progress Bar | Feedback / Layout | 线性进度指示器。 | [Loading screen, XP bar, quest progress] | Draft |
| Input Field | Input | 文本输入控件。 | [Player name, search, key binding entry] | Draft |
| Tab Bar | Navigation | 单个界面内的标签页导航。 | [Character sheet, settings, crafting] | Draft |
| Scroll Container | Layout | 带可见滚动指示器的可滚动内容区域。 | [Inventory, lore entries, credits] | Draft |
| Inventory Slot | Game-Specific | 物品栏中的物品容器（空、已填充、已装备、已锁定）。 | [Inventory screen, equipment screen] | Draft |
| Ability / Skill Icon | Game-Specific | 带冷却、层数和锁定状态的技能按钮。 | [HUD ability bar, skill tree] | Draft |
| Health / Resource Bar | Game-Specific | 带阈值状态和受击闪烁的数值条。 | [HUD] | Draft |
| Minimap | Game-Specific | 带玩家标记和兴趣点的概览地图。 | [HUD] | Draft |
| Quest / Objective Tracker | Game-Specific | 带接近度和完成状态的当前目标显示。 | [HUD] | Draft |
| Dialogue Box | Game-Specific | 带说话者标识的 NPC 对话 UI。 | [All dialogue sequences] | Draft |
| Context Action Prompt | Game-Specific | 靠近可交互对象时出现的上下文“按 X 执行[action]”提示。 | [World interaction] | Draft |
| Damage Number | Game-Specific | 悬浮的战斗反馈数字。 | [Combat HUD] | Draft |
| Status Effect Icon | Game-Specific | 带持续时间的增益/减益指示器。 | [HUD status bar, enemy health display] | Draft |
| Notification Banner | Game-Specific | 成就、升级、获得物品的通知。 | [Global overlay] | Draft |
| Screen Push | Navigation | 向前导航并带方向动画。 | [All menu navigation] | Draft |
| Screen Pop (Back) | Navigation | 反向动画的返回导航。 | [All menu navigation] | Draft |
| Screen Replace | Navigation | 不堆叠历史记录地替换当前界面。 | [Main Menu to Loading Screen] | Draft |
| Modal Open / Close | Navigation | 使背景界面变暗的覆盖层。 | [All modal dialogs] | Draft |
| Tab Switch | Navigation | 同一界面内的标签切换。 | [All tabbed screens] | Draft |
| Focus Management | Navigation | 界面打开、关闭或变更时焦点的去向规则。 | [All screens] | Draft |
| Escape / Cancel | Navigation | 跨平台与输入方式通用的返回行为。 | [All screens] | Draft |
| Loading State | Feedback | 界面和组件在加载中的表现方式。 | [All loading states] | Draft |
| Empty State | Feedback | 空列表和空网格的呈现方式。 | [Empty inventory, no quests, no saves] | Draft |
| Error State | Feedback | 错误如何传达。 | [Save failed, network error, invalid input] | Draft |
| Success Confirmation | Feedback | 完成动作如何被确认。 | [Settings saved, item crafted, quest turned in] | Draft |
| Optimistic UI | Feedback | 在系统确认前先展示假定成功。 | [If online features are present] | Draft |

---

## 标准控件模式

---

#### Button (Primary)

**Category**: Input  
**Status**: Draft  
**When to Use**: 一个界面上最重要的单一动作。“Start Game,” “Confirm,” “Accept,” “Buy.” 屏幕上同时出现的 Primary 按钮最多一个。它回答的是“玩家在这里最可能想做什么？”  
**When NOT to Use**: 替代动作或次要动作；需要确认的危险动作；任何不是该界面主要意图的动作。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Default | 满不透明填充，使用 art-bible 中的主色。标签居中。 | — | — | — | — |
| Hovered (mouse) | 亮度 +15%，轻微缩放 1.03x，光标变为指针 | 鼠标移入元素 | 从 Default 过渡 | 80ms ease-out | [UI hover sound — see Sound Standards] |
| Focused (keyboard/gamepad) | 显示焦点环（2px，偏移 3px，高对比度颜色）。与 Hovered 相同亮度。 | Tab / 方向键导航 | 从 Default 过渡 | 80ms ease-out | [UI focus sound — same as hover] |
| Pressed | 缩放 0.97x，亮度 -10% | Click / Enter / A (Xbox) / Cross (PS) | 动作在释放按键时触发，而不是按下时。按下时开始缩放。 | 按下 60ms ease-in；释放 80ms ease-out | [UI confirm sound] |
| Disabled | 40% 透明度，无指针光标，无悬停状态 | — | 无响应 | — | — |
| Loading (post-press) | 用加载转圈替换标签。按钮保持在按下后的缩放状态，并处于禁用状态。 | — | 防止重复提交 | 异步操作持续时间 | — |

**Accessibility**:
- Keyboard：Tab 聚焦，Enter 或 Space 激活。必须能通过 Tab 序列从屏幕上的任何其他可交互元素到达。
- Gamepad：使用方向键或左摇杆在焦点间移动到按钮。A (Xbox) / Cross (PS) 激活。屏幕打开时，焦点必须默认放在 Primary 按钮上。
- Screen reader：按钮必须暴露与可见标签一致的可访问名称。Role: “button.” 禁用时状态为 “dimmed.” 激活播报：“[Label] button — [result of action, if known].”
- Colorblind：不要只靠颜色区分 Primary 与 Secondary。Primary 还应通过更高视觉权重（实心填充 vs. 描边，或更大尺寸）来区分。
- Minimum touch target：44x44pt（iOS HIG）/ 48x48dp（Android）。即使在 PC 上，如果可能支持触控，也应应用该标准。

**Implementation Notes**:
[Godot: 继承 `Button` 控件。针对自定义状态覆盖 `_draw()`，而不要在状态之间修改主题。使用 `focus_mode = FOCUS_ALL` 确保可通过键盘聚焦。设置 `mouse_default_cursor_shape = CURSOR_POINTING_HAND`。缩放动画建议作用于按钮父级 `Control` 的 `scale` 属性——直接缩放 `Button` 自身可能会裁切子节点。]

---

#### Button (Secondary)

**Category**: Input  
**Status**: Draft  
**When to Use**: 备用或取消动作。“Back,” “Cancel,” “Skip,” “Maybe Later.” 视觉权重要低于 Primary——它应当视觉上退后，而不是竞争注意力。  
**When NOT to Use**: 危险动作（使用 Button (Destructive)）。屏幕上最重要的动作（使用 Button (Primary)）。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Default | 描边样式（仅边框、透明填充），次要颜色。比 Primary 稍小或更低权重。 | — | — | — | — |
| Hovered | 背景填充出现 15% 不透明度。边框变亮。缩放 1.02x。 | 鼠标移入 | 从 Default 过渡 | 80ms ease-out | [UI hover sound — softer variant than Primary] |
| Focused | 焦点环，与 Primary 规范相同。 | Tab / 方向键 | 从 Default 过渡 | 80ms ease-out | [UI focus sound] |
| Pressed | 缩放 0.97x，填充不透明度提升到 30% | Click / Enter / B (Xbox) / Circle (PS) 在焦点状态下 | 动作在释放时触发 | 60ms ease-in | [UI cancel/back sound] |
| Disabled | 40% 透明度 | — | 无响应 | — | — |

**Accessibility**：与 Button (Primary) 相同。可访问名称必须与可见标签一致。在带 Primary 和 Secondary 按钮的对话框中，Secondary 按钮通常映射到平台的“cancel”输入（B / Circle / Escape），也可以通过直接焦点激活。

**Implementation Notes**：[与 Button (Primary) 相同。若 Primary 与 Secondary 同时出现，确保 Secondary 始终以一致方式摆放——横向布局中位于 Primary 的右侧/下方，纵向布局中位于 Primary 的下方。跨界面的一致性比每个界面的美学偏好更重要。]

---

#### Button (Destructive)

**Category**: Input  
**Status**: Draft  
**When to Use**: 任何不可逆并会导致玩家数据或重大进度损失的动作：“Delete Save File,” “Reset All Settings,” “Leave Match,” “Discard Changes.” 视觉处理在玩家按下之前就先传达危险。  
**When NOT to Use**: 可撤销动作，或只是有后果但仍可回退的动作。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Default | 使用危险色（通常为低饱和红色——请在 accessibility-requirements 中确认色盲兼容性）的描边或填充。标签可包含警告图标。 | — | — | — | — |
| Hovered / Focused | 与 Button (Primary) 的 hover/focus 行为相同，但采用危险色。 | — | — | 80ms | [UI hover sound] |
| Pressed (first press) | 不直接执行动作。相反，打开 Confirmation Dialog 模式（见下）。按钮本身显示短暂脉冲动画。 | Click / Enter | 触发 Confirmation Dialog | 100ms pulse | [UI warning sound — distinct from standard confirm] |
| — | Confirmation Dialog 负责实际执行 | — | — | — | — |
| Disabled | 40% 透明度 | — | 无响应 | — | — |

> **关键规则**：Button (Destructive) 绝不会直接执行其动作。  
> 它始终会触发 Confirmation Dialog。没有例外。玩家误触时必须始终还有一步撤回机会。  
> 跳过破坏性动作确认的游戏，会比任何其他 UX 失败类型更容易产生最显眼的社区负面情绪。参见：任何论坛上“我不小心删了存档”的投诉。

**Accessibility**：屏幕阅读器必须播报其危险性质：“[Label] button — this action cannot be undone.” 除了可访问名称外，如有 `description` 属性可用，请加入警告文本。

**Implementation Notes**：[Destructive button 触发独立的 Confirmation Dialog 场景。将动作回调传递给对话框——按钮本身不持有执行逻辑。这种分离可防止确认对话框出现 bug 时误执行。]

---

#### Toggle

**Category**: Input  
**Status**: Draft  
**When to Use**: 二元开/关设置，且两种状态同等有效，并且当前状态需要一眼可见。“Subtitles: On/Off,” “Aim Assist: On/Off,” “Notifications: On/Off.”  
**When NOT to Use**: 超过两个选项的选择（使用 Dropdown）。只发生一次的动作，而不是持续状态的表示（使用 Button）。切换后果复杂到需要解释的情况（旁边加一个描述字段）。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Off / Default | 轨道：低调填充。滑块：最左侧位置。标签：“Off”或状态标签。 | — | — | — | — |
| Hovered | 轨道亮度提升 10%。光标：指针。 | 鼠标移入 | 过渡 | 60ms | [UI hover sound] |
| Focused | 围绕整个 toggle 元素（轨道 + 滑块）的焦点环。 | Tab / 方向键 | — | 60ms | [UI focus sound] |
| Pressed / Activated | 滑块滑到右侧。轨道填充变为激活色。标签变为 “On” 或激活状态标签。状态保持。 | Click / Enter / A / Cross | 切换状态变化。触发 onChange 事件。持久化数值。 | 150ms ease-in-out for slide | [Toggle ON sound] |
| Pressed / Deactivated | 滑块滑回左侧。轨道恢复为低调填充。 | Same inputs | 切换状态变化 | 150ms ease-in-out | [Toggle OFF sound — subtly different from ON] |
| Disabled | 40% 透明度。不可交互。当前状态仍可见。 | — | 无响应 | — | — |

**Accessibility**:
- Keyboard/Gamepad：Space 或 Enter 切换。不要要求使用方向输入（left/right）来切换——有些用户无法预判这种行为。
- Screen reader：Role: “switch.” State: “on” 或 “off”——可访问名称不应包含状态（屏幕阅读器会单独播报状态）。正确示例：可访问名称 “Subtitles,” 状态 “on.” 错误示例：可访问名称 “Subtitles On.”
- toggle 标签（而不仅是视觉滑块位置）必须变化，以便无法可靠分辨左右位置的玩家识别当前状态。

**Implementation Notes**：[Godot：使用自定义 Control 或 CheckButton。内置 CheckButton 提供无障碍角色，但使用的是复选框式视觉；若目标美术风格需要，可能要自定义滑动开关动画。确保在启用运动减弱模式时跳过滑动动画——此时应立即跳到最终状态。]

---

#### Slider

**Category**: Input  
**Status**: Draft  
**When to Use**: 在连续范围内选择数值，允许近似值，且范围和相对位置本身有信息价值。音量（0–100%）、亮度、文字大小。数值位置的视觉表示本身就是有用信息。  
**When NOT to Use**: 精确数值输入（使用 Input Field）。从少量离散列表中选择（使用 Dropdown）。二元状态（使用 Toggle）。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Default | 轨道（全宽）。填充（滑块左侧，表示当前值）。滑块（可拖拽把手）。当前数值标签（轨道右侧或滑块上方）。 | — | — | — | — |
| Hovered | 滑块略微放大（1.2x）。轨道变亮。 | 鼠标移入 | — | 60ms | — |
| Focused | 滑块上的焦点环。轨道变亮。 | Tab / 方向键 | — | 60ms | [UI focus sound] |
| Dragging (mouse) | 滑块跟随光标。填充实时更新。数值标签实时更新。 | 在滑块上单击并拖拽 | 持续数值更新。连续触发 onChange。 | 实时 | [Slider adjust sound — subtle, loops while dragging] |
| Keyboard / D-pad adjust | 每次按键滑块移动一个步长（范围的 5% 或 1 个离散单位）。 | 聚焦时按 Left/Right 箭头或 Left/Right D-pad | 单步数值变化。每步触发 onChange。 | 立即 | [Slider step sound — one click per step] |
| Keyboard fast adjust | 更大的步长（范围的 25%）。 | 聚焦时按 Page Up / Page Down | 大步数值变化 | 立即 | [Same step sound] |
| Released | 数值锁定。onChange 触发最终值。 | 鼠标释放 | — | — | — |
| Disabled | 40% 透明度。不可交互。值仍可见。 | — | 无响应 | — | — |

**Accessibility**:
- Keyboard：Left/Right 箭头按小步调整。Page Up/Page Down 按大步调整。Home/End 跳到最小/最大值。
- Screen reader：Role: “slider.” 可访问名称为标签（例如 “Music Volume”）。每次变化都播报当前值：“Music Volume, 80 percent.” 首次聚焦时播报最小/最大值。
- 所有 slider 都必须在视觉位置之外再显示一个数值。只依赖轨道填充位置会排除那些无法感知相对位置的玩家。

**Implementation Notes**：[Godot `HSlider`：将 `step` 设为合适的增量。通过 `_input()` 覆盖键盘输入以支持 Page Up/Down。绑定 `value_changed` 信号来更新显示的数值标签。启用运动减弱模式时，确保数值标签更新是唯一反馈——不要把它们也抑制掉。游戏手柄滑块调整时加入震动反馈是对无障碍有益的增强。]

---

#### Dropdown / Select

**Category**: Input  
**Status**: Draft  
**When to Use**: 从 3-15 个离散选项中选择，且静止时只需要显示当前值。显示分辨率、语言、窗口模式、输入预设。关闭状态只显示当前选择。  
**When NOT to Use**: 二元选择（使用 Toggle）。超过约 15 个选项（使用完整 List 模式或可滚动 Select）。当比较选项与选择同样重要时（改为可见选项，例如水平选择器或列表）。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Closed / Default | 标签（左）。当前值（右）。下拉箭头图标（最右）。 | — | — | — | — |
| Hovered | 行背景以 10% 不透明度填充 | 鼠标移入 | — | 60ms | — |
| Focused (closed) | 整行焦点环。 | Tab / D-pad | — | 60ms | [UI focus sound] |
| Opening | 下拉列表在下方展开（如果靠近屏幕底部则在上方）。显示所有列表项。此前选中的条目高亮。焦点移到列表中当前选中项。 | Click / Enter / A / Cross | 打开列表 | 100ms ease-out (expand) | [UI expand sound] |
| List item hovered/focused | 列表项高亮 | 鼠标 / D-pad | — | 60ms | [UI hover sound] |
| List item selected | 列表关闭。关闭状态显示新值。触发 onChange 事件。 | 在列表项上 Click / Enter / A / Cross | 选择值，关闭列表 | 80ms ease-in (collapse) | [UI confirm sound] |
| Dismissed without selecting | 列表关闭。值不变。 | Escape / B / Circle / 点击外部 | Dismiss | 80ms | [UI cancel sound] |
| Disabled | 40% 透明度。不可交互。 | — | — | — | — |

**Accessibility**:
- Keyboard：列表打开时用 Up/Down 箭头在列表项之间移动。Enter 选择。Escape 关闭。按下某个选项的首字母会跳到第一个匹配项。
- Screen reader：Role: “combobox.” 可访问名称为字段标签。会播报展开/折叠状态。聚焦时播报当前值。每个列表项会播报其值和位置：“English, 1 of 12.”
- 下拉列表绝不能遮住当前项或打开它的控件——这在小屏幕上是常见失败。

**Implementation Notes**：[Godot：使用 `Button`（关闭状态）加 `PopupMenu` 或通过动画显现的 `VBoxContainer` 自定义实现。原生 `OptionButton` 提供无障碍，但视觉定制能力有限。若列表会被屏幕底部裁切，确保弹出层在控件上方显示。通过 `_input` 检测点击外部时关闭弹出层。]

---

#### List Item

**Category**: Layout / Input  
**Status**: Draft  
**When to Use**: 垂直可滚动列表中的单个可选行。成就、任务日志条目、设置分类、存档槽位。列表是容器；这里是其中的一行。  
**When NOT to Use**: 二维网格布局（使用 Grid Item）。不可选的内容行（移除 hover/focus 和 pressed 状态）。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Default | 全宽行。图标（可选，左侧）。主标签。次级标签 / 元数据（右侧或在主标签下方）。箭头（右侧，如需进入更深层）。 | — | — | — | — |
| Hovered | 行背景 12% 不透明度高亮。 | 鼠标移入 | — | 60ms | — |
| Focused | 行上的焦点环，或行背景 20% 不透明度高亮（与平台惯例一致）。 | D-pad / Tab | — | 60ms | [UI focus sound] |
| Selected (persistent) | 行背景 25% 不透明度高亮。可显示选择指示器（左边框、对勾）。与焦点状态不同——一行可以已选中但未聚焦。 | — | 渲染状态 | — | — |
| Pressed / Activated | 短暂亮度闪烁，然后跳转或执行动作 | Click / Enter / A / Cross | 导航或动作 | 80ms flash | [UI confirm sound] |
| Disabled | 40% 透明度。不可交互。 | — | — | — | — |

**Accessibility**:
- Keyboard/Gamepad：使用 Up/Down 箭头或 D-pad 在列表项之间移动。列表必须处理焦点循环——到达底部应停止（而不是环绕），除非明确设计了环绕。
- Screen reader：Role: “listitem.” 父级列表 role: “list.” 可访问名称为主标签内容。元数据（次级标签）可选择性包含在描述中。位置会被播报：“Quest Log, 3 of 12.”
- Minimum row height：44pt / 48dp for touch。对于以手柄为主的平台，56px 行高会更舒适。

**Implementation Notes**：[Godot：在 `ScrollContainer` 中使用 `VBoxContainer`。每一行是一个自定义 `Control` 或 `PanelContainer`，并重写 `_gui_input`。对于滚动容器内的键盘导航，实现自定义焦点遍历——Godot 默认的 Tab 导航不会在焦点项移出视野时自动滚动容器。使用滚动容器的 `ensure_control_visible()`。]

---

#### Grid Item

**Category**: Layout / Input  
**Status**: Draft  
**When to Use**: 二维网格中的可选单元格。物品栏格子、技能选择、制作材料选择、角色头像选择。网格是容器；这里是其中的格子。  
**When NOT to Use**: 单列内容（使用 List Item）。不可选的展示单元（移除交互状态）。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Empty | 空槽视觉（低调边框或虚线轮廓）。与 disabled 不同。 | — | — | — | — |
| Populated | 物品图标填满单元格。堆叠数量（右下角，如适用）。品质指示器（边框颜色或图标覆盖层）。 | — | — | — | — |
| Hovered | 亮度 +15%。400ms 延迟后显示工具提示。 | 鼠标移入 | — | 60ms | — |
| Focused | 焦点环（2px，偏移 2px）。与 hovered 相同亮度。400ms 后显示工具提示，或在手柄上立即显示。 | D-pad 导航 | — | 60ms | [UI focus sound] |
| Selected (persistent) | 明显边框（更粗、更有对比度的颜色）。可显示选中对勾。 | Click / Enter / A / Cross | 选择物品。可与不同单元格上的焦点状态共存。 | 立即 | [UI select sound] |
| Pressed | 短暂缩放 0.95x，然后执行动作 | Double-click / Enter / A / Cross | 动作（装备、使用、查看——由上下文定义） | 80ms | [UI confirm sound] |
| Locked | 已填充内容上叠加锁头图标。无 hover/focus 状态。 | — | 不可交互 | — | — |
| Drag source | 单元格变暗（50% 不透明度），拖拽预览出现在光标处。 | Click + drag (mouse only) | 开始拖拽操作 | 立即 | [UI grab sound] |
| Drop target (valid) | 单元格变亮，显示接受颜色指示 | 物品拖到上方 | — | 60ms | — |
| Drop target (invalid) | 红色染色或抖动动画 | 物品拖到无效槽位 | — | 60ms | [UI error sound] |

**Accessibility**:
- Keyboard/Gamepad：使用 D-pad 或方向键在单元格间导航。网格必须向屏幕阅读器传达其维度。需要播报行/列位置。
- Screen reader：Role: “gridcell.” 父级 role: “grid.” 可访问名称为物品名称（空单元格则为 “empty slot”）。已选中时状态为 “selected”，已锁定时为 “dimmed”。位置：“row 2, column 3.”
- 工具提示必须可通过键盘到达——它们必须在单元格获得焦点时出现，而不只是悬停时。

**Implementation Notes**：[Godot：使用固定列数的 `GridContainer`。每个单元格都是一个自定义 `Control`。通过重写 `_gui_input` 并基于索引和列数计算左右上下相邻单元格来实现自定义 D-pad 导航。`GridContainer` 原生不提供这一点。]

---

#### Modal Dialog

**Category**: Feedback / Layout  
**Status**: Draft  
**When to Use**: 需要在玩家继续之前解决的决策或确认。该对话框是阻塞式的——背景内容会变暗并不可交互。“Are you sure?”, “Your progress will be saved.”, 错误状态。  
**When NOT to Use**: 非阻塞通知（使用 Toast / Notification）。可以等到玩家准备好再看的信息（将其加入持续性帮助系统）。应允许玩家在其背后继续游玩的对话框。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Opening | 背景覆盖层从 0% 动画到 60% 不透明度。对话框面板从 0.9 缩放到 1.0。从中心进入（不是从边缘）。 | 由代码触发 | 焦点移动到对话框中的第一个可交互元素（或 Primary 按钮） | 200ms ease-out | [UI modal open sound] |
| Active | 背景不可交互。对话框拥有全部输入焦点。玩家无法与背景交互。 | 键盘 / 手柄仅在对话框内导航 | — | — | — |
| Dismissing (confirmed) | 对话框面板缩放到 1.1 后淡出。覆盖层淡出到 0%。 | Primary button pressed | 执行动作，焦点返回到触发元素 | 180ms | [UI confirm sound] |
| Dismissing (cancelled) | 对话框面板缩放到 0.9 后淡出。覆盖层淡出到 0%。 | Secondary button / Escape / B / Circle | 无动作，焦点返回到触发元素 | 150ms | [UI cancel sound] |
| Cannot dismiss | 如果对话框表示阻塞式错误，则不要提供取消路径。只提供解决选项。 | — | — | — | — |

> **焦点陷阱规则**：当模态对话框打开时，Tab 和 D-pad 导航必须只在该对话框的可交互元素中循环。绝不能让焦点导航到对话框外的背景内容。这既是无障碍要求（WCAG 2.1 SC 2.1.2），也是 UX 完整性要求。对话框关闭时，焦点必须返回到触发它的元素，而不是页面顶部。

**Accessibility**:
- Screen reader：对话框容器 role: “dialog.” 可访问名称为对话框标题（必需——每个对话框都必须有标题，即使它在视觉上隐藏）。打开时，屏幕阅读器播报标题和第一个可聚焦元素。焦点陷阱启用。
- Keyboard：Escape 键始终映射到取消/关闭动作（与 Secondary 按钮或关闭按钮一致）。Enter 始终映射到 primary/confirm 动作。
- Motion reduction：缩放动画改为即时显示/隐藏。覆盖层淡出保留，但时长缩短为 100ms。

**Implementation Notes**：[Godot：作为 `CanvasLayer` 实现，使用较高 layer 值（100+）确保它渲染在所有游戏内容之上。背景覆盖层为全屏 `ColorRect`，60% 黑色不透明度。打开动画完成后对话框的 Primary 按钮调用 `grab_focus()`。重写 `_input()` 实现焦点陷阱——拦截 Tab 导航并重定向到对话框内可聚焦元素。]

---

#### Confirmation Dialog

**Category**: Feedback / Layout  
**Status**: Draft  
**When to Use**: 确认破坏性动作的特定情况。始终由 Button (Destructive) 触发。始终只有两个选项：确认（使用具体动作命名，而不是 “OK”）和取消。  
**When NOT to Use**: 非破坏性确认。无需玩家做决定的错误或通知。任何超过两个动作的对话框。

> **标签规则**：确认按钮必须以具体动作命名，而不是泛泛的 “OK” 或 “Yes.” “Delete Save File” 而不是 “OK.” “Leave Match” 而不是 “Yes.” 这能减少那些无法快速阅读对话框内容的玩家出错。该模式来自 Apple HIG，并得到数十年可用性研究验证。

**Structure**:
- Title：简短、描述动作。“Delete save file?” 而不是 “Are you sure?”
- Body：用一句话说明后果。“This cannot be undone.”
- Confirm button：Button (Primary)——使用具体动作命名。“Delete Save File.”
- Cancel button：Button (Secondary)——“Cancel.”
- Default focus：Cancel（更安全的默认值——减少误触破坏性动作）。

**Accessibility**：继承 Modal Dialog 的全部无障碍要求。此外：屏幕阅读器会播报 “Alert dialog, [title]” 以表明这是破坏性上下文。默认聚焦 Cancel 是硬性要求，而不是偏好。

**Implementation Notes**：[Confirmation Dialog 是 Modal Dialog 的特例——可以作为子类实现，也可以作为参数化场景实现。默认聚焦 Cancel 很关键：在打开动画完成后对 Cancel 按钮调用 `grab_focus()`，而不是对 Confirm 按钮。]

---

#### Toast / Notification

**Category**: Feedback  
**Status**: Draft  
**When to Use**: 简短、非阻塞、无需玩家决策的信息。“Game saved.” “Achievement unlocked.” “Your inventory is full.” 玩家可以继续游玩；通知会自行消失。  
**When NOT to Use**: 需要玩家做决定的信息（使用 Modal Dialog）。需要玩家采取行动的错误。玩家绝不能错过的关键消息。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Entering | 从屏幕边缘滑入（通常为右下角，远离主要操作区域）。从 0 淡入到 100% 不透明度。 | 由代码触发 | — | 200ms ease-out | [Sound matching notification type — see Sound Standards] |
| Displayed | 完全不透明。可选：图标（左侧）、标题、正文（可选）、关闭按钮（X，可选）。 | 鼠标悬停会暂停自动消失计时器 | 暂停自动消失 | — | — |
| Auto-dismiss | 从 100% 淡出到 0%，并滑出 | 计时器到期（单行默认 5 秒；双行 8 秒） | 从队列移除 | 200ms ease-in | — |
| Manual dismiss | 立即淡出并滑出 | 点击/轻触 X 按钮或在触摸设备上滑动 | 移除 | 150ms | [UI cancel sound, quiet] |
| Queue overflow | 新通知会把最旧的通知提前挤出 | 在前一个通知显示时触发新通知 | FIFO 队列，最多同时 3 个 | — | — |

**Accessibility**:
- Screen reader：Toast 必须在不要求焦点的情况下朗读。在 HTML 中，这使用 `role="status"` 或 `role="alert"`。在游戏 UI 中，这需要引擎的无障碍通知系统。请在 engine-reference 文档中核实引擎支持。
- Motion reduction：滑动动画改为仅淡入淡出。
- Toast 绝不能成为玩家需要采取行动的信息的唯一沟通渠道。如果信息需要行动，除了 toast 之外，还必须提供持久 UI 元素。
- 自动消失计时器：5 秒是最短值。认知处理差异的玩家可能需要更久。考虑提供将其延长到 10 或 15 秒的设置。

**Implementation Notes**：[Godot：在锚定到屏幕角落的 `VBoxContainer` 中管理一组 `PanelContainer` 场景队列。每个 toast 被实例化后添加到容器中，然后在计时器结束后自动移除。该容器应位于较高的 `CanvasLayer`（50+），但低于模态对话框（100+）。用 `Tween` 作用于 `modulate.a` 和 `position.x` 来制作动画。启用运动减弱时，跳过位置动画。]

---

#### Tooltip

**Category**: Feedback  
**Status**: Draft  
**When to Use**: 对可见标签进行补充的上下文信息。物品栏中的物品说明。角色面板中的属性解释。无障碍选项里的设置说明。玩家必须能够访问这些信息，或者可以不依赖它们继续进行。  
**When NOT to Use**: 玩家必须阅读才能完成操作的信息——应放在标签或正文里，而不是 tooltip 中。移动端触屏上无法通过 hover 轻易发现 tooltip。对于纯触控平台，请改用信息按钮打开说明模态框。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Hidden | — | — | — | — | — |
| Hover trigger | — | 鼠标进入元素 | 开始 400ms 延迟计时器 | — | — |
| Gamepad/keyboard trigger | — | 元素获得焦点 | 开始 300ms 延迟计时器（更短，因为导航是有意图的） | — | — |
| Appearing | Tooltip 面板淡入，并从 0.95 缩放到 1.0。放置在元素附近（优先上方，靠近屏幕边缘时再调整）。 | 计时器到期 | 显示 tooltip | 120ms ease-out | — |
| Displayed | Tooltip 可见。标题（可选）。正文。最大宽度：300px。允许多行。 | — | — | — | — |
| Hiding | Tooltip 淡出 | 鼠标离开元素 / 焦点移开 | 隐藏 tooltip | 80ms ease-in | — |

**Accessibility**:
- Screen reader：Tooltip 内容必须在无 hover 的情况下也可访问。父元素的可访问名称应包含最关键的 tooltip 信息。完整 tooltip 文本可选放在 `description` 属性中。元素获得焦点时，屏幕阅读器会读取 tooltip 内容。
- 300-400ms 的延迟可防止误触发 tooltip，这是游戏手柄导航的必需条件——即时 tooltip 会造成干扰。
- Tooltip 文本必须与正文相同的对比度要求（最低 4.5:1）。

**Implementation Notes**：[Godot：将自定义 `TooltipControl` 场景作为触发元素的子节点附加。使用 `Timer` 节点控制显示/隐藏。通过 `CanvasLayer` 定位 tooltip，确保它出现在所有其他 UI 之上。靠近屏幕边缘时，检测 tooltip rect 是否超出 `get_viewport_rect()`，并翻转到另一侧。]

---

#### Progress Bar

**Category**: Feedback / Layout  
**Status**: Draft  
**When to Use**: 指向明确终点的线性进度。加载屏幕（完成时间）、经验条填充到下一等级、带可计数进度的任务目标（“3 of 10 enemies defeated”）、下载进度。  
**When NOT to Use**: 圆形或径向进度（如需要请使用单独的 Radial Progress 模式）。快速上下波动的数值（使用 Health/Resource Bar 模式）。没有明确终点的数值。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Default | 轨道（全宽，背景色）。填充（从左到右，数值色）。数值标签（百分比或 N/M，位于填充内或外）。 | — | — | — | — |
| Value increasing | 填充宽度动画到新值 | 数值变化 | 平滑填充动画 | 300ms ease-out | [Context-dependent — XP gain has a sound; loading has none] |
| Value at maximum | 填充达到全宽。可选：完成动画（脉冲、发光）。 | 值达到 100% | 触发完成事件 | 200ms | [Completion sound if appropriate] |
| Value at zero | 填充隐藏（零宽度）。轨道仍可见。 | — | — | — | — |
| Indeterminate (unknown duration) | 循环动画（填充段从左到右移动，重复）。用于未知时长的加载。 | — | — | 无限循环 | — |

**Accessibility**:
- Screen reader：Role: “progressbar.” 可访问名称为正在进展的内容（例如 “Experience Points,” “Loading”）。数值必须播报当前数值、百分比和最大值。“Experience Points, 450 of 1000, 45 percent.” 仅在明显变化时更新（不是每个像素）。
- 不要只依赖填充颜色来传达数值。要包含数值标签。
- 不确定时长的进度条：播报 “Loading, in progress”——不要播报变化，因为数值未知。
- Motion reduction：不确定动画改为静态 “loading” 指示器。平滑填充动画改为立即跳到新值。

**Implementation Notes**：[Godot：使用带自定义主题的内置 `ProgressBar`。对于不确定模式，Godot 4.x 的 `ProgressBar` 没有原生不确定状态——请通过在填充元素位置上循环 `Tween` 来实现。确保启用运动减弱模式时暂停该 Tween，并改为显示静态指示器。]

---

#### Input Field

**Category**: Input  
**Status**: Draft  
**When to Use**: 文本输入。新存档的玩家名、列表内搜索、重映射按键（特殊情况——显示按键输入而不是文本）、精确输入数值。  
**When NOT to Use**: 从已知选项中选择（使用 Dropdown 或 List）。在主机优先平台上，尽量减少文本输入——它需要虚拟键盘，摩擦成本很高。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Default | 字段边框、占位文本（标签风格、低调颜色）、空输入区域。 | — | — | — | — |
| Hovered | 边框稍微变亮 | 鼠标移入 | — | 60ms | — |
| Focused | 边框完全变亮。光标（闪烁，530ms on / 530ms off）。占位文本隐藏。 | Tab / click | 在主机/移动设备上打开虚拟键盘 | 立即 | [UI focus sound] |
| Typing | 字符出现。光标前进。 | Keyboard input | 更新字段值 | 立即 | [Subtle keystroke sound, optional] |
| Value present | 字段显示输入值。占位文本隐藏。若值非空，清除按钮（X，位于字段右侧）出现。 | — | — | — | — |
| Character limit reached | 不再接受额外输入。可选：短暂抖动动画，且限制指示器变色。 | 达到限制时输入 | 拒绝后续字符 | 200ms shake | [UI error sound, subtle] |
| Clear | 字段清空。光标回到原位。清除按钮消失。 | Click X / gamepad clear input | 清除值 | 立即 | [UI cancel sound, subtle] |
| Validation error | 边框变为错误色（红色——确保色盲安全）。错误消息显示在字段下方。 | 提交时或失焦时 | 显示错误 | 立即 | [UI error sound] |
| Validated / correct | 边框变为成功色（绿色——确保色盲安全）。可选成功图标。 | 验证通过时 | — | 立即 | — |
| Disabled | 40% 透明度，不可交互。值仍可见。 | — | — | — | — |

**Accessibility**:
- Keyboard：所有标准文本编辑快捷键（Home、End、Ctrl+A、Ctrl+C、Ctrl+V、Ctrl+Z）。
- Screen reader：Role: “textbox.” 可访问名称为字段标签（而不是占位文本）。会播报当前值。达到字符上限时会播报。验证错误会在发生时立即播报。
- 占位文本绝不能作为唯一标签——字段上方或旁边必须有可见标签。占位文本在玩家输入后会消失，这会让认知或记忆障碍玩家感到困惑。

**Implementation Notes**：[Godot `LineEdit`：将 `placeholder_text` 作为提示，但始终包含一个可见 `Label` 节点作为字段的可访问名称。绑定 `text_changed` 信号以进行实时验证。绑定 `text_submitted` 以在按 Enter 时提交表单。在控制台上，使用 `LineEdit.call("_popup_keyboard")` 或 OS 虚拟键盘 API——请在 engine-reference/godot/ 中核实 Godot 4.6 控制台键盘 API 的具体细节。]

---

#### Tab Bar

**Category**: Navigation  
**Status**: Draft  
**When to Use**: 将单个界面的内容分成多个离散部分，每次只显示一个部分。角色面板标签（Stats / Equipment / Skills）、设置标签（Gameplay / Graphics / Audio / Accessibility）。最多 5-6 个标签，再多就不适合该模式，应考虑侧边栏导航。  
**When NOT to Use**: 超过 6 个标签。适合同时可见的内容（使用布局模式）。不同屏幕之间的导航（使用 Screen Push）。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Default (inactive tab) | 标签文字。无激活指示器。 | — | — | — | — |
| Active tab | 标签文字。激活指示器（下划线、填充或对比背景）。内容区显示该标签内容。 | — | — | — | — |
| Hovered (inactive) | 标签背景轻微填充 | 鼠标移入 | — | 60ms | — |
| Focused (keyboard/gamepad) | 标签文字上的焦点环。 | 标签栏内的 Tab 键或 D-pad 左/右切换 | — | 60ms | [UI focus sound] |
| Activated | 激活指示器切换到此标签。内容区过渡（淡入或滑动）。 | Click / Enter / A / Cross | 切换活动标签。更新内容。 | 150ms ease | [UI tab switch sound] |
| Gamepad shoulder button | — | L1/R1 (PS) 或 LB/RB (Xbox) | 切换到前一个/后一个标签（标准平台惯例） | 150ms | [UI tab switch sound] |

**Accessibility**:
- Keyboard：标签栏内使用箭头键在标签之间导航（左/右）。Tab 键将焦点移入下方内容区。这遵循 ARIA tab panel 模式。
- Screen reader：单个标签角色为 “tab.” 容器角色为 “tablist.” 内容区角色为 “tabpanel.” 活动标签状态为 “selected.” 可访问名称为标签文本。tabpanel 会由对应标签命名。
- 活动标签必须通过不止颜色一种方式来区分（下划线、填充样式或权重变化，除了颜色之外还要有其他变化）。

**Implementation Notes**：[Godot：内置 `TabContainer`。若要自定义视觉样式，手动实现为 `HBoxContainer` 的标签按钮和 `MarginContainer` 的内容区域。肩键快捷方式（LB/RB）必须在界面的 `_input()` 覆盖中实现——Godot 的标签系统不自带它。注意平台惯例：Xbox 使用 LB/RB；PlayStation 使用 L1/R1；它们本质上是同一个物理按钮，因此一个绑定即可。]

---

#### Scroll Container

**Category**: Layout  
**Status**: Draft  
**When to Use**: 超出容器可视区域的内容。物品列表、文本传说条目、制作人员名单、较长的设置列表。滚动指示器让玩家知道还有更多内容。  
**When NOT to Use**: 可以分页替代的内容（对于密集的列表导航，分页可能更清晰）。无限滚动（始终提供加载状态和结束状态）。

**Interaction Specification**:

| State | Visual | Input | Response | Duration | Audio |
|-------|--------|-------|----------|----------|-------|
| Content fits | 不显示滚动条（或根据美术风格显示始终可见但满高的滚动条）。 | — | — | — | — |
| Scrollable | 显示滚动条（右边缘）。滚动条滑块大小表示视口与内容的比例。 | — | — | — | — |
| Scrolling (mouse) | 内容移动。滚动条滑块按比例移动。 | Mouse wheel | 每次滚轮 tick 滚动 3 行（可由 OS 配置） | Smooth | — |
| Scrollbar drag | 内容移动。滑块跟随指针。 | 点击并拖拽滚动条滑块 | 按比例滚动 | 实时 | — |
| Keyboard scroll | 每次按键内容移动一个条目高度。 | 容器获得焦点且没有子项聚焦时按 Up/Down 箭头 | 滚动一个单位 | 立即 | — |
| Gamepad scroll | 内容移动以保持当前焦点项可见。 | D-pad 导航到可视区域外的条目 | 自动滚动以保持焦点项可见 | Smooth 150ms | — |
| Scroll top / bottom | 内容停止。滚动条滑块位于末端。 | 到达内容边界 | 停止滚动 | — | — |
| Focus follows scroll | 当某个子元素获得焦点时，滚动容器确保它完全可见。 | 任何子元素获得焦点 | 滚动以显示焦点元素 | 200ms ease | — |

**Accessibility**:
- Keyboard/Gamepad：滚动容器本身不应要求显式操作滚动条——在它内部导航列表项时应自动滚动以保持焦点项可见。
- Screen reader：滚动容器应播报“scrollable”和滚动位置（“showing items 5 through 15 of 30”）。这需要引擎无障碍支持——请在 engine-reference/godot/ 中核实。
- 内容边缘淡出（在滚动边界处让内容渐隐以表示还有更多内容）是有用的视觉辅助，但不能成为唯一指示内容超过可见区域的手段。必须包含滚动条。

**Implementation Notes**：[Godot `ScrollContainer`：当容器内部的 `gui_focus_changed` 触发时，对获得焦点的子控件调用 `ensure_control_visible()`。通过在容器的 `gui_focus_changed` 信号上递归 `connect` 来绑定。平滑滚动动画应通过作用于 `scroll_vertical` 的 `Tween` 来实现，而不是直接赋值。]

---

## 游戏特定 UI 模式

---

#### Inventory Slot

**Category**: Game-Specific  
**Status**: Draft  
**When to Use**: 物品栏网格中的每一个物品容器。空槽、已填充槽、已装备槽、已锁定槽。槽位是框架；物品图标是内容。

**States**:

| State | Visual | Notes |
|-------|--------|-------|
| Empty | 低调的槽位边框，无内容。与 disabled 不同。空槽是可交互的（可接收物品）。 | 不要让空槽完全不可见——玩家会失去对网格尺寸的感知 |
| Populated | 物品图标占据槽位面积的 80%。堆叠数在右下角（如适用）。品质边框（色盲安全——图标 + 颜色）。已装备徽章（右上角，如已装备）。 | |
| Focused | 焦点环。300ms 后出现工具提示。 | |
| Selected | 更粗或更有对比度的边框。用于支持多选时。 | |
| Drag source | 槽位变暗，拖拽幽灵跟随指针。 | 完整拖拽规范见 Grid Item |
| Locked | 叠加锁头图标。不可交互。可在锁后以 50% 不透明度显示物品。 | 用于锁定的预设槽、DLC 内容等 |
| Highlighted | 动画边框发光（脉冲）。用于任务相关物品或新获得物品。 | 遵守运动减弱——将脉冲替换为静态徽章 |
| Cooldown overlay | 从 12 点钟方向开始的径向填充遮罩，顺时针递减，随冷却结束而消失。 | 仅适用于槽位代表带冷却的主动物品时 |

**Accessibility**：堆叠数量和品质等级必须有文本或图标替代方案，不能只靠颜色。Tooltips 是主要无障碍机制——确保它们可通过键盘和屏幕阅读器访问。锁定槽必须向屏幕阅读器播报 “locked.”

**Implementation Notes**：[Godot：自定义 `Control` 节点。品质边框根据稀有度通过 `StyleBoxFlat` 切换——不要用 `modulate` 颜色表示品质，因为它会影响图标颜色。拖放通过 `get_drag_data()` 以及 `can_drop_data()` / `drop_data()` 覆写方法实现。]

---

#### Ability / Skill Icon

**Category**: Game-Specific  
**Status**: Draft  
**When to Use**: HUD 技能栏中的能力按钮、技能树节点，以及任何需要显示可用状态的能力场景。

**States**:

| State | Visual | Notes |
|-------|--------|-------|
| Available | 全不透明图标。下方显示按键绑定标签。 | |
| On cooldown | 从 12 点钟方向开始顺时针递减的径向遮罩。剩余时间在剩余大于 2 秒时以数字显示在中央。 | |
| Charges remaining | 图标下方显示层数指示点（例如 3 个填充圆点 = 3 层）。屏幕阅读器使用数字替代。 | |
| Out of resource | 图标去饱和到约 20%。边框变暗。按键标签变暗。与冷却不同——是资源门槛，而不是时间门槛。 | |
| Locked / not unlocked | 仅显示图标轮廓（不显示完整插画）。锁头徽章。工具提示中可显示解锁条件。 | |
| Active / channeling | 边框脉冲。径向填充显示引导剩余时间。 | |
| Just activated | 短暂缩放到 0.9x，再弹回到 1.0x（过冲到 1.05x）。 | 示例：Guild Wars 2 和 Path of Exile 都在能力使用时使用按下-弹起动画来确认激活。遵守运动减弱。 |

**Accessibility**：所有冷却/层数信息都必须有数值（屏幕阅读器无法解析径向遮罩）。冷却计时数字满足这一要求。能力名称和说明必须通过 tooltip 暴露给屏幕阅读器。

**Implementation Notes**：[Godot：自定义 `TextureButton` 子类，并为冷却径向与层数点使用覆盖 `Control` 节点。冷却径向可用作用于 `ColorRect` 的自定义 shader，通过旋转遮罩实现——或者如果引擎支持，也可用被样式化为圆形的 `ProgressBar`。请在 engine-reference/godot/ 中核实 Godot 4.6 对该模式的 shader 支持。]

---

#### Health / Resource Bar

**Category**: Game-Specific  
**Status**: Draft  
**When to Use**: HUD 中任何持续变化、代表关键玩家资源的数值。生命、法力、耐力、护盾、燃料。

**States and behaviors**:

| Event | Visual | Audio | Duration |
|-------|--------|-------|---------|
| Value decrease (damage) | 填充缩小。填充上出现短暂“damage flash”（白色或红色闪光）。幽灵条保留在之前数值并在 0.5s 内下落到新值（“damage indicator”）。 | [Damage taken sound — varies by amount] | 立即下降，500ms 幽灵条下落 |
| Value increase (heal) | 填充增长。短暂治疗色闪烁（绿色——确保通过图标/光效备份满足色盲安全）。 | [Heal sound] | 300ms ease-in |
| Below 25% threshold | 填充变为警告状态颜色。边框脉冲（或在运动减弱模式下使用静态徽章）。可选：心跳音效（若音频是唯一信号，需与视觉配对）。 | [Low health sound — loops until above threshold] | Continuous |
| At zero | 条为空。可选：短暂抖动。触发死亡/耗尽事件。 | [Death/depletion sound] | 200ms shake |
| Maximum | 填充到 100%，短暂发光。 | — | 200ms |
| Overflow (shield) | 在自然填充区域之外出现独立条段，使用护盾颜色。 | [Shield gain sound] | 200ms |

**Accessibility**：当前数值必须以数字形式可访问（tooltip 或持续显示，或两者兼有）。颜色编码的阈值状态必须有非颜色备份（图标、闪烁或音频视觉警告）。25% 警告状态必须有独立于颜色变化之外的视觉信号。

**Implementation Notes**：[Godot：用两个重叠的 `ProgressBar` 节点实现幽灵条效果——后层条保存前一个值（通过 Tween 下落），前层条保存当前值（立即更新）。阈值状态在前层条上触发 `StyleBoxFlat` 切换。幽灵条 Tween 持续时间是可由设计师调节的参数。]

---

#### Dialogue Box

**Category**: Game-Specific  
**Status**: Draft  
**When to Use**: NPC 对话、配音叙事对话、通过角色传递的教程文本。所有带说话者的对话。

**Structure**: 说话者头像或名字标签（盒子顶部或左侧）。对话文本正文。继续/推进提示（右下角）。可选：全跳过按钮、配音指示器、字幕指示器。

**States and behaviors**:

| State | Visual | Input | Response | Duration |
|-------|--------|-------|----------|---------|
| Line entering | 文本逐字符显示（打字机效果）。或者：若启用无障碍选项，则以完整速度淡入。 | — | — | 速度：可在无障碍设置中配置 |
| Revealing | 文本正在出现。继续提示隐藏或以低速透明度脉冲。 | [Any advance input] | 立刻跳到当前行末尾（显示完整行，停止打字机） | 立即 |
| Line complete | 显示完整句子。继续提示可见并带动画。 | — | — | — |
| Advancing to next line | 继续提示隐藏。文本淡出或擦除。新行开始。 | [Any advance input] — Enter / A / Cross / Space / mouse click | 前进 | 100ms transition |
| Choices appearing | 选项按钮显示在对话文本下方。继续提示隐藏。焦点移动到第一个选项。 | D-pad / keyboard to select, Enter / A / Cross to confirm | 选择选项 | 150ms enter animation |
| Closing | 对话框淡出 | 最后一行推进后 | 将控制权返回给玩家 | 200ms |
| Skipping all (if supported) | 短暂确认提示：“Skip dialogue?” | Dedicated skip button | 跳到对话后状态 | — |

**Accessibility**：所有配音对话默认都开启字幕。打字机动画速度是用户设置（见 accessibility-requirements.md）。对话框不能自动推进——玩家必须控制节奏。说话者名字始终显示。所有选项按钮都必须能通过键盘和手柄导航。选项必须对屏幕阅读器可访问，并播报位置。

**Implementation Notes**：[Godot：使用启用 `bbcode_enabled` 的 `RichTextLabel` 进行格式化。通过 `Timer` 属性动画化 `visible_characters` 来实现打字机效果。将 advance 输入绑定到一个函数：要么跳过打字机（设置 `visible_characters = -1`），要么推进对话状态。说话者名字显示在盒子上方或旁边的独立 `Label` 中。对话数据从 JSON 或专用对话格式加载（例如 Dialogic、Yarn Spinner for Godot）。]

---

#### Context Action Prompt

**Category**: Game-Specific  
**Status**: Draft  
**When to Use**: 出现在可交互游戏对象附近的提示，用来说明玩家可以做什么。“Press [A] to open chest.” “Hold [E] to pick up.” 当玩家进入交互范围时出现，离开时消失。

**States**:

| State | Visual | Notes |
|-------|--------|-------|
| Appearing | 从对象锚点淡入并上移 8px。 | 遵守运动减弱——仅淡入，不上移 |
| Idle | 平台正确的按键图标 + 动作标签。图标匹配当前输入方式（若玩家切换会更新）。 | 始终显示平台正确图标——不要在所有平台上都硬编码 “Press A” |
| Holding (for hold inputs) | 按键图标上的径向填充显示按住进度。标签改为主动动词（“Opening...”）。 | |
| Cannot interact (blocked) | 图标变暗。若已知原因则显示原因（“Too heavy”, “Need key”）。 | 可选——只有在原因对玩家有意义时才显示阻塞状态 |
| Disappearing | 淡出。 | 玩家离开交互范围时触发 |

**Accessibility**：按键图标必须配合文本标签——不要只依赖图标（有些玩家使用自定义按键标签或带非标准图标的辅助控制器）。提示必须定位到不会覆盖角色生命值或关键 HUD 信息的位置。

**Implementation Notes**：[Godot：作为 `Node3D` 子节点（2D 游戏中则为 `Node2D`）附加到可交互对象上。3D 游戏可使用 `BillboardMesh` 或 `SubViewport` 配合 UI 场景——这样可以无需代码让提示始终面向摄像机。根据 `Input.get_joy_name()` 或通过 `InputEventKey` 与 `InputEventJoypadButton` 的输入类型来更新按键图标纹理。按住进度可通过 `AnimationPlayer` 或作用于径向遮罩 shader 的 `Tween` 实现。]

---

#### Damage Number

**Category**: Game-Specific  
**Status**: Draft  
**When to Use**: 悬浮在战斗参与者上方的反馈数字。普通伤害、暴击、治疗、未命中。

**Variants**:

| Variant | Visual | Notes |
|---------|--------|-------|
| Normal damage | 白色数字，常规字重，中等大小。 | |
| Critical hit | 更大尺寸（1.5x）、粗体、橙色或黄色——请验证色盲安全。出现时有短暂放大冲击（1.3x → 1.0x）。 | 示例：Path of Exile 和 Diablo IV 都使用暴击时的 scale-pop，使其可以仅通过尺寸而非颜色立即识别。 |
| Healing | 绿色（请验证色盲安全——使用 “+” 前缀和向上轨迹作为非颜色备份）。 | |
| Miss / Evade | “MISS” 文本，灰色，斜体。以较小尺寸浮动。 | |
| Status damage (DoT) | 更小尺寸，与状态效果一致的不同颜色。 | |

**Behavior**：数字从命中位置向上浮动 1.0 秒。数字在最后 0.4 秒从 100% 淡出到 0%。来自快速连击的多个数字在水平方向错开，以避免重叠。屏幕上同时显示的伤害数字上限：[按游戏定义——通常每个角色 8-12 个]。

**Accessibility**：伤害数字只是辅助反馈——绝不能成为理解战斗状态的唯一方式。生命条才是权威来源。提供关闭伤害数字的选项（有些玩家会觉得它们过于视觉干扰）。关闭后，游戏必须仍然完全可玩。

**Implementation Notes**：[Godot：使用 `Label3D`（3D 游戏）或 `Label`（2D 游戏）的对象池进行回收复用。每个实例生成时赋予随机的小水平偏移（±20px）以减少重叠。通过 `Tween` 作用于 `position.y` 和 `modulate.a` 来实现浮动动画。暴击 scale-pop 使用带 `EASE_OUT` 的 Tween 放大后再线性回落。]

---

## 导航模式

---

#### Screen Push / Pop / Replace

**Category**: Navigation  
**Status**: Draft

这三个模式定义了界面如何进入和退出导航栈。

| Pattern | Trigger | Animation | Stack Behavior | Focus Behavior |
|---------|---------|-----------|---------------|----------------|
| Push | 向更深层导航（打开子菜单、打开详情视图） | 新屏幕从右侧滑入。前一屏向左滑并变暗。 | 前一屏保留在栈中 | 焦点移到新屏幕上的第一个可交互元素 |
| Pop (Back) | 返回按钮 / Escape / B / Circle | 当前屏幕向右滑出。前一屏从左侧滑入并变亮。 | 当前屏幕从栈中移除 | 焦点返回到触发 Push 的元素 |
| Replace | 导航到同级屏幕（不是子级，也不是父级）。加载屏幕。 | 当前屏幕淡出，新屏幕淡入。没有方向偏向。 | 当前屏幕移除。新屏幕加入。 | 焦点移到新屏幕上的第一个可交互元素 |

**Animation durations**：Push/Pop：250ms ease-in-out。Replace：200ms fade out + 200ms fade in。

**Motion reduction**：所有滑动动画都改为淡入淡出。时长缩短为 100ms。

**Implementation Notes**：[Godot：作为管理 `Control` 场景栈的 `ScreenManager` 单例实现。`push(screen_scene)` 会实例化并动画进入。`pop()` 动画退出并释放。`replace(screen_scene)` 先 pop 再 push，中间不保留栈状态。为每个屏幕使用 `CanvasLayer` 以隔离输入处理。push 前保存“return focus”元素引用，以便 pop 时恢复。]

---

#### Focus Management

**Category**: Navigation  
**Status**: Draft

> 焦点管理是游戏 UI 中最常见的键盘和手柄无障碍失败点。这些规则必须一致地实现。玩家绝不应处于看不到哪个元素被聚焦，或 Tab/D-pad 没有可见反馈的状态。

| Rule | Description |
|------|-------------|
| Screen open | 焦点应放在最合理的可交互元素上——通常是 Primary 按钮、第一个列表项，或如果该屏幕此前访问过则放在上一次最后聚焦的元素上。绝不能放在非交互元素上。 |
| Screen close / pop | 焦点返回到触发导航的元素（打开该屏幕的按钮、被选中的列表项）。如果该元素不再存在，则焦点转到顺序上最接近的前一个可交互元素。 |
| Modal open | 焦点被困在模态框内。见 Modal Dialog 模式。 |
| Modal close | 焦点返回到触发模态框的元素。 |
| Element disabled | 如果被聚焦元素变为禁用，焦点移到 Tab 顺序中的下一个可用可交互元素。 |
| Element destroyed | 如果被聚焦元素从场景中移除，焦点移到 Tab 顺序中最接近的前一个元素。 |
| Screen without interactive elements | 焦点管理为空操作。确保返回/取消输入仍然可用。 |
| Tab key (keyboard) | 按文档顺序在可交互元素间前进焦点（从左到右，从上到下）。Shift+Tab 反向移动。 |
| D-pad (gamepad) | 按下的方向进行空间导航。对于手柄，优先空间导航而不是严格的 Tab 顺序。不要在无关区域之间环绕焦点（例如 Tab bar 和内容区应是独立导航区域）。 |
| Focus is always visible | 通过键盘或手柄聚焦时，焦点环或等效焦点指示器必须始终可见。绝不隐藏焦点指示。 |

---

#### Escape / Cancel

**Category**: Navigation  
**Status**: Draft

> “返回”动作是所有菜单系统中使用最多的导航输入。  
> 它必须在每个界面中保持一致，且没有例外。

| Platform | Input | Behavior |
|----------|-------|---------|
| PC (keyboard) | Escape | 关闭最上层模态框 / 返回上一个栈界面 / 如果在根界面（主菜单），打开“quit?”确认 |
| PC (gamepad) | B (Xbox layout) / Circle (PS layout) | 与 Escape 相同 |
| Xbox | B button | 与 Escape 相同 |
| PlayStation | Circle button | 与 Escape 相同 |
| Nintendo Switch | B button | 与 Escape 相同（注意：Nintendo 在某些第一方游戏中用 B 确认为主；请为本次发布核实平台惯例并记录决定） |

**Rules**：此输入绝不能被改作“返回/取消”之外的事情。如果某个界面没有返回动作（例如游戏暂停且玩家必须做出选择），Escape 要么无操作，要么显示“you must choose”提示——绝不能导航离开。每个界面都必须在其 UX 规格中明确其 Escape 行为。

---

## 反馈与加载模式

---

#### Loading State

**Category**: Feedback  
**Status**: Draft

| Scope | Pattern | Notes |
|-------|---------|-------|
| Full screen (initial load) | 带游戏美术、进度条（若可能则使用确定进度）、提示文本（可选）的全屏加载界面。 | 绝不要用空黑屏。给玩家一些可读或可看的内容。 |
| Full screen (level transition) | 淡出到黑屏，加载界面，再从黑屏淡入到新场景。 | 这种淡出可消除上一场景突然消失的突兀感。 |
| Component / inline | 加载中的组件用 spinner 或 skeleton 占位符替换。内容加载后组件布局不应跳动。 | 对布局密集的内容来说，skeleton 占位符（近似内容形状的灰盒）优于 spinner——它能防止加载时的布局偏移。 |
| Background / async | 除非操作超过 2 秒，否则不显示任何视觉提示。2 秒后，显示一个小 spinner 或 toast。 | 对于 2 秒内完成的操作，不要显示加载指示器——指示器一闪而过比等待更扰人。 |

**Accessibility**：加载状态必须向屏幕阅读器播报：“[Context] loading, please wait.” 完成时必须播报：“[Context] loaded.” 对于全屏加载，确保加载界面本身可被屏幕阅读器导航——提示文本和任何 UI 元素都必须暴露出来。

---

#### Empty State

**Category**: Feedback  
**Status**: Draft

> 空状态通常是游戏 UI 中设计得最少的部分。它决定玩家感受到的是“这是我存放物品的地方”，还是“这里为什么什么都没有？是不是坏了？” 每个空列表和空网格都必须有一个设计过的空状态。空状态不是错误——它是起点。

| Location | Empty State Content | Notes |
|----------|--------------------|----|
| Inventory (no items) | 图标（低调、大号、居中）。消息：“Your inventory is empty.” 子消息：“Items you find on your journey will appear here.” | 不要说 “No items found”——“found” 暗示搜索失败。 |
| Quest Log (no active quests) | 图标。消息：“No active quests.” 子消息：“Talk to characters marked with [quest marker icon] to start a quest.” | 给玩家一个明确行动。 |
| Achievements (none earned) | 图标。消息：“No achievements yet.” 提示成就列表：“Try [Action] to earn your first achievement.” | 游戏化激励，而不只是空白。 |
| Search results (no matches) | 图标。消息：“No results for '[search term]'.” 子消息：“Try a different search or [browse all].” | 把搜索词原样反馈给玩家。给出替代动作。 |

**Rule**：每个空状态都必须包含图标、消息，以及子消息或操作按钮。没有解释的空容器绝不可接受。

---

#### Error State

**Category**: Feedback  
**Status**: Draft

| Error Type | Pattern | Tone |
|-----------|---------|------|
| Input validation (form field) | 字段下方显示内联错误消息。错误消息左侧显示错误图标。字段红色边框（通过图标确保色盲安全）。 | 中性且具体——“Username must be 3-20 characters.” 不是 “Invalid input.” |
| Operation failed (save error, network error) | 非关键失败使用 toast 通知。关键失败（存档无法写入）使用 Modal Dialog。 | 平静且可执行——“Save failed. Check storage space.” 不是 “FATAL ERROR.” |
| System error (crash, data corruption) | 全屏错误界面，包含错误代码、恢复选项（“Restart Game,” “Load last save”）和支持联系信息。 | 令人安心——承认问题，给玩家掌控感。绝不责怪玩家。 |
| Soft error (action cannot be performed) | Toast 或内联消息。 | 解释性——“Not enough gold” 而不是 “Action unavailable.” |

**Principle**：错误信息永远不是玩家的错。它们是游戏在告诉玩家发生了什么以及下一步该做什么。从所有错误消息中移除“invalid”这个词——用具体说明替代。

---

## 动画标准

> 这些时间值适用于本库中的所有模式。当某个模式写着 “150ms ease-out” 时，其 easing function 就定义在这里。统一的时序会让 UI 像一个经过设计的系统，而不是一堆孤立的决定。

| Animation Type | Duration (ms) | Easing Function | Notes |
|---------------|--------------|----------------|-------|
| Button hover / focus enter | 80 | ease-out | 快速——利落，不拖沓 |
| Button hover / focus exit | 60 | ease-in | 比进入稍快的退出 |
| Button press scale down | 60 | ease-in | 立即反馈 |
| Button press scale up (release) | 80 | ease-out | 稍微有点弹性 |
| Screen push (enter) | 250 | ease-in-out | 屏幕从右侧滑入 |
| Screen pop (exit) | 250 | ease-in-out | 屏幕向右滑出 |
| Modal open | 200 | ease-out | 从中心展开 |
| Modal close | 150 | ease-in | 比打开更快收起 |
| Toast enter | 200 | ease-out | 从屏幕边缘滑入 |
| Toast exit | 200 | ease-in | |
| Tab switch | 150 | ease-in-out | 内容交叉淡入或滑动 |
| Tooltip appear | 120 | ease-out | 在 300-400ms 延迟之后 |
| Tooltip disappear | 80 | ease-in | |
| Progress bar fill | 300 | ease-out | 数值变化平滑动画 |
| Value flash (damage, gain) | 100ms on + 100ms off | linear | 短促、吸引注意 |
| Dialogue text reveal (per character) | 30ms per character | linear | 可在无障碍设置中配置 |
| HUD damage flash | 80 | linear | 白色或红色覆盖层，立即反馈 |

**Motion reduction overrides**：当启用运动减弱模式时（见 accessibility-requirements.md），所有滑动和缩放动画都改为淡入淡出。淡入淡出时长缩短 50%。循环动画（不确定 spinner、脉冲指示器）改为静态等效物。

---

## 声音标准

> 每个交互事件都应该有音频反馈。声音是主要反馈通道，而不是装饰。这里定义的声音是事件类别——具体音频资产定义在 `docs/sound-bible.md` 中。该表将交互事件映射到声音类别，以便音频设计师和 UI 程序员使用相同词汇。

| Interaction Event | Sound Category | Notes |
|------------------|---------------|-------|
| Button hover / focus | UI Hover | 低调、短促（< 80ms）、在快速导航中不会让人疲劳。Hades 使用的是一个非常安静的高频点击声，在快速导航时几乎融入背景。 |
| Button (Primary) confirm | UI Confirm — Primary | 比 secondary confirm 更突出一点。“yes, let's go”的声音。 |
| Button (Secondary) cancel / back | UI Cancel | 轻微向下的音高。“正在返回”的声音。Mass Effect 用的是干净、明确的 swoosh 来表达返回导航。 |
| Button (Destructive) — opening confirmation | UI Warning | 与标准 confirm 区分开。短促、吸引注意的声音。 |
| Confirmation dialog — confirm destructive | UI Confirm — Destructive | 最终、稍有重量感。动作正在被执行。 |
| Toggle ON | UI Toggle On | 短促、利落、略明亮。Celeste 的无障碍切换有令人满意的 click-on 声。 |
| Toggle OFF | UI Toggle Off | 同一 click 家族，但更平一些。 |
| Slider adjust | UI Slider | 拖动时有低调连续声。D-pad 每次移动只出一个 click。绝不能让人疲劳。 |
| Dropdown open | UI Expand | 短促、带方向感（打开感）。 |
| Dropdown close / select | UI Select | 确认感。 |
| Tab switch | UI Tab | 横向移动感。与纵向导航不同。 |
| Modal open | UI Modal Open | 比标准导航更突出——用来吸引注意。 |
| Modal close (cancel) | UI Modal Close | 回到先前上下文。 |
| Toast — informational | UI Notification | 背景级、非侵入式。 |
| Toast — achievement | UI Achievement | 有庆祝感，但不要太长。玩家应感到被奖励，而不是被打断。 |
| Toast — warning | UI Warning — Toast | 与 error 区分开。是提醒，不是惊吓。 |
| Error state | UI Error | 友好但明确。不是刺耳警报。Dark Souls 用的是轻微、低沉的敲击声来表达失败动作——传达“no”，但不苛刻。 |
| Success confirmation | UI Success | 干净、令人满足。 |
| Ability activate | Gameplay — Ability Activate | 游戏内感觉，与纯 UI 区分开。属于 game feel，而非菜单 feel。 |
| Damage received | Gameplay — Damage | 完整规范见 sound-bible.md。 |
| Item pickup | Gameplay — Item Acquire | 短促、令人愉悦。 |
| Level up / rank up | Gameplay — Progression | 庆祝性、适度突出。 |
| Dialogue advance | UI Dialogue | 低调，若启用打字机效果则与其节奏一致。 |

---

## 未决问题

| Question | Owner | Deadline | Resolution |
|----------|-------|----------|-----------|
| [Does the engine's accessibility node system support screen reader announcements for toast notifications without requiring focus? Verify against engine-reference/godot/ for Godot 4.6.] | [ux-designer] | [Before first menu implementation] | [Unresolved] |
| [What is the platform-correct confirm/cancel button mapping for Nintendo Switch release? Nintendo first-party convention differs from Xbox/PlayStation.] | [producer] | [Before platform certification submission] | [Unresolved] |
| [Should damage numbers be pooled as Label3D nodes or rendered in a SubViewport? Verify performance budget in coordination with technical-director.] | [lead-programmer, ux-designer] | [Before combat HUD implementation] | [Unresolved] |
| [What is the maximum number of simultaneous toast notifications before the queue becomes visually overwhelming? Needs playtesting.] | [ux-designer] | [First playtesting session] | [Unresolved] |
| [Add question] | [Owner] | [Deadline] | [Resolution] |