# 示例会话：UX 流程 —— /ux-design → /ux-review → /team-ui

**上下文：** 单人独立开发者，处于预生产阶段。HUD 和库存界面是首批要设计的 UI。游戏已经有玩家旅程文档，以及库存和战斗的 GDD。

**起始状态：**
- `design/gdd/inventory-system.md` —— 完整
- `design/gdd/combat-system.md` —— 完整
- `design/player-journey.md` —— 完整（定义了 6 段情绪弧）
- 还没有任何 UX 规格
- `design/ux/` 目录还不存在

**会话时长：** 约 90 分钟，分两次会话完成（先 HUD 设计，再库存界面）
**轮数：** 16
**结果：** 创建并审查了 `design/ux/hud.md` 和 `design/ux/screens/inventory.md`，然后把 handoff 交给 `team-ui` 做视觉实现

---

## 第 1 部分：用 /ux-design 设计 HUD

### 第 1 轮：用户开始 HUD 设计

**User：**
> /ux-design hud

### 第 2 轮：智能体加载上下文并给出方法

**Agent（ux-designer，通过 /ux-design）：**
> 正在开始 HUD 设计。加载上下文……
>
> - 已读 `design/player-journey.md` —— 关键状态：平静探索、紧张（检测到威胁）、危机（低 HP/耐力）、战斗
> - 已读 `design/gdd/combat-system.md` —— HUD 需要：HP 条、耐力条、激活技能冷却（最多 3 个）、伤害数字
> - 已读 `design/gdd/inventory-system.md` —— HUD 需要：快捷栏（4 格）、当前物品指示器
>
> **HUD 哲学问题：** 玩家在实际游玩时主要关注什么？
>
> 这会决定 HUD 要有多强的存在感：
> - **选项 A：Diegetic（低存在感）** —— 只有在受伤时才显示 HP，耐力在消耗时才显示。以世界为先，HUD 只在紧急时出现。
> - **选项 B：Persistent minimal** —— HP 和耐力始终可见，但很小、很克制。能快速查阅，但不切换注意力模式。
> - **选项 C：Full tactical** —— 所有信息都始终可见（HP、耐力、冷却、地图、物品栏位）。玩家随时掌握完整信息。
>
> 考虑到你的 survival 游戏和“孤身幸存者”幻想，A 或 B 最符合这个类型。

**User：**
> B——我希望它一直在，但保持极简。玩家一直在管理资源。

### 第 3 轮：智能体起草 HUD 哲学部分

**Agent：**
> **HUD 哲学草稿：**
>
> > **方法：Persistent Minimal**
> > HUD 始终可见，但只占用很少的屏幕空间。玩家是一个资源管理型幸存者——如果隐藏 HP/耐力可视化，只会带来挫败感，而不是张力。所有关键状态都能一眼读懂，同时不会打断探索注意力。当元素变得紧急时，它们会增强视觉重量（HP 低于 30% 会脉冲，耐力为 0 会闪烁），然后恢复到极简状态。
>
> 我可以把这段写进 `design/ux/hud.md` 作为 Philosophy 部分吗？

**User：**
> Yes

**Agent** 创建 `design/ux/hud.md` 并写入 Philosophy 部分。

*(第 4–7 轮继续按章节编写 HUD：Info Architecture、Zones、Element Specs、State Machine、Visual Budget、Platform Adaptation —— 每节都经过起草、批准并写入文件。)*

---

**所有章节完成后的最终 HUD 结构：**

```text
design/ux/hud.md
  - Philosophy：Persistent Minimal
  - Info Architecture：HP（左上）、Stamina（左上 HP 下方）、Quick Slots（底部中央）、
    Ability Cooldowns（右下）、Damage Numbers（世界空间）
  - Zones：定义了 4 个区域（左上 vitals、底部中央交互、右下技能、世界空间）
  - Element Specs：6 个元素，包含尺寸、字体大小、不透明度规则
  - State Machine：Calm / Tension / Crisis / Combat（4 个状态，含状态切换触发器）
  - Visual Budget：最多占屏幕 8%，最多 3 个同时动画
  - Platform Adaptation：Controller（增加瞄准准星）、Mobile（v1 不在范围内）
```

---

## 第 2 部分：用 /ux-design 设计库存界面

### 第 8 轮：用户开始库存界面

**User：**
> /ux-design screen inventory

### 第 9 轮：智能体扫描 GDD 和玩家旅程

**Agent：**
> 正在加载库存界面上下文……
>
> 来自 `design/gdd/inventory-system.md`：
> - 网格库存，6×8 格
> - 物品有重量（影响移动）和堆叠上限
> - 玩家可以装备、丢弃、检查、拆分堆叠
>
> 来自 `design/player-journey.md`：
> - 库存会在平静探索中频繁打开
> - 玩家打开库存时应该感觉“井井有条、受控”
> - 焦虑时刻：“我需要决定丢什么”——应该清晰，而不是慌乱
>
> **玩家需求（来自旅程）：** *我需要快速判断自己携带了什么，决定保留什么、丢弃什么，然后回到世界里。*
>
> **关键设计问题：** 玩家如何执行库存操作？
> - **选项 A：右键上下文菜单** —— 悬停物品 → 右键 → 弹菜单（常见做法）
> - **选项 B：拖拽式** —— 拖到丢弃区就丢弃；拖到装备栏就装备（Stardew Valley）
> - **选项 C：检查面板** —— 点击物品 → 右侧出现详情面板和操作按钮

**User：**
> B——拖拽式。我想要手感更强。

*(第 10–12 轮继续为库存界面规格编写章节：Player Need、Layout Zones、States、Interaction Map、Data Requirements、Events Fired、Accessibility、Localization。)*

---

## 第 3 部分：/ux-review

### 第 13 轮：用户运行审查

**User：**
> /ux-review design/ux/

### 第 14 轮：智能体审查两份文档

**Agent（通过 /ux-review）：**
> 正在审查 `design/ux/` 中的所有 UX 规格……
>
> ---
> **HUD 审查（`hud.md`）：**
>
> | 检查项 | 状态 | 备注 |
> |-------|--------|-------|
> | 与 GDD 对齐 —— 所有必需元素都存在 | ✅ | HP、耐力、快捷栏、冷却都已编写 |
> | 状态机覆盖 | ✅ | 4 个游戏状态都涵盖了 |
> | 可访问性级别 | ⚠️ | 没有为 HP/耐力条指定色盲模式（红/黄惯例） |
> | 视觉预算 | ✅ | 占屏 8%，在预算内 |
> | 平台备注 | ✅ | 已记录 Controller 变体 |
>
> **库存界面审查（`screens/inventory.md`）：**
>
> | 检查项 | 状态 | 备注 |
> |-------|--------|-------|
> | 已写出 Player Need | ✅ | |
> | 涵盖所有 GDD 动作 | ✅ | 装备、丢弃、检查、拆分都在 interaction map 中 |
> | 拖放交互定义完整 | ⚠️ | 库存已满时的丢弃目标行为未定义——会发生什么？ |
> | 可访问性：拖拽的键盘替代方案 | ❌ | 缺失——只有拖拽，没有键盘路径，违反操作可访问性 |
> | 本地化：所有字符串都已标记 | ✅ | |
> | 数据事件触发 | ✅ | `item_equipped`、`item_dropped`、`stack_split` 都已映射 |
>
> ---
> **结论：NEEDS REVISION**
>
> 在交给 `/team-ui` 前，必须解决两个问题：
>
> 1. **BLOCKING（可访问性）：** 库存界面没有拖拽的键盘替代方案。操作可访问性要求必须有非拖拽路径。可以添加“按 X 拿起 / 再按一次放下”的切换，或者带有键盘可用按钮的详情面板。
>
> 2. **ADVISORY（HUD）：** HP/耐力条只靠颜色区分状态。给色盲用户加一个辅助指示（形状、图标或纹理）。可以在视觉打磨阶段修复。
>
> 3. **ADVISORY（Inventory）：** 库存已满时的丢弃行为没有定义。要么在 GDD 里解决，要么明确写成范围外。

### 第 15 轮：用户解决阻塞问题

**User：**
> 键盘方案：按 F 拾取光标下的物品，再按一次 F 放到目标格。把这个加到库存规格里。

**Agent：**
> 我会把这段加到 Interaction Map 的 “Keyboard / Controller Path” 下：
>
> > 按 F（或南键）拾取光标下的物品。物品进入“被持有”状态，并显示视觉指示。再按一次 F 放到目标格。按 Escape 取消并把物品放回。
>
> 我可以把它写进 `design/ux/screens/inventory.md`，然后重新跑一次可访问性检查吗？

**User：**
> Yes

**Agent** 写入更新。重新检查可访问性——现在通过。

---

## 第 4 部分：交给 /team-ui

### 第 16 轮：用户启动 team UI

**User：**
> /team-ui

**Agent（通过 /team-ui）：**
> 正在运行 UX 流程上下文检查……
>
> - `design/ux/hud.md` —— 已审查 ✅
> - `design/ux/screens/inventory.md` —— 已审查 ✅
> - `/ux-review` 结论：NEEDS REVISION 已解决 —— 当前状态：APPROVED ✅
>
> 现在进入 **阶段 2：视觉设计**
>
> 正在把交接给 `art-director`，让他们做视觉规格（调色板、字体、图标风格，与 art bible 对齐）……
>
> （team-ui 会继续执行：视觉设计 → 布局实现 → 可访问性审计 → 最终审查）

---

## 这个示例展示了什么

- **上下文驱动的设计**：智能体读取 player-journey.md，让 HUD 决策建立在玩家情绪状态上，而不是只看功能列表。
- **UX 审查是硬门禁**：`/team-ui` 在开始视觉设计前必须先通过 `/ux-review`。
- **可访问性尽早发现**：缺少键盘替代方案是由审查抓到的，而不是最终 QA 才发现。
- **阻塞 vs. 建议**：缺少键盘路径是 BLOCKING（会阻止交接）；色盲配色问题是 ADVISORY（可在视觉打磨阶段修）。
- **按章节写 UX**：和 `/design-system` 一样，都是增量写入——每一节都先写文件，再进入下一节。
- **HUD 和 screen 分文件**：`design/ux/hud.md` 是全局 HUD；每个屏幕的规格放在 `design/ux/screens/`。
- **/team-ui 强制模式库**：在这个会话之后，inventory 的拖拽式交互会被记录为 `design/ux/interaction-patterns.md` 里的一个模式，供以后所有屏幕引用。
