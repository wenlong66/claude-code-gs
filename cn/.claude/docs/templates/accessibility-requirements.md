# 无障碍需求： [Game Title]

> **状态**：Draft | Committed | Audited | Certified
> **作者**：[ux-designer / producer]
> **最后更新**：[Date]
> **无障碍层级目标**：[Basic / Standard / Comprehensive / Exemplary]
> **平台**：[PC / Xbox / PlayStation 5 / Nintendo Switch / iOS / Android]
> **目标外部标准**：
> - WCAG 2.1 Level [A / AA / AAA]
> - AbleGamers CVAA Guidelines
> - Xbox Accessibility Guidelines (XAG) [Yes / No / Partial]
> - PlayStation Accessibility (Sony Guidelines) [Yes / No / Partial]
> - Apple / Google Accessibility Guidelines [Yes / No / N/A — mobile only]
> **无障碍顾问**：[姓名和组织，或“None engaged”]
> **关联文档**：`design/gdd/systems-index.md`, `docs/ux/interaction-pattern-library.md`

> **本文档的存在原因**：单个界面的无障碍注释应放在 UX 规范中。本文档记录项目范围内的无障碍承诺、所有系统的功能矩阵、测试计划以及审计历史。它在 Technical Setup 期间由 UX designer 和 producer 创建一次，随后随着功能增加和审计完成持续更新。如果某项功能与本文档中的承诺冲突，则以本文档为准——应修改功能，而不是承诺，除非 producer 批准正式修订。
>
> **更新时机**：每次 `/gate-check` 通过后、每次无障碍审计后，以及每当 `systems-index.md` 中新增一个游戏系统时。

---

## 无障碍层级定义

> **为什么要定义层级**：无障碍不是二元的。定义四个层级能为团队提供共同语言，在制作开始时强制明确承诺，并防止双向范围蔓延（“以后再加”以及“我们必须支持一切”）。下面的层级是本项目的定义——业界使用相近但不完全相同的术语。请承诺具体功能目标的层级，而不只是层级名称。

### 层级定义

| 层级 | 核心承诺 | 典型工作量 |
|------|----------|------------|
| **Basic** | 关键玩家可见文本在标准分辨率下可读。没有任何功能只依赖颜色区分。音乐、SFX 和语音音量分别可调。游戏可完成且不存在光敏风险。 | 低——主要是设计约束 |
| **Standard** | 包含 Basic 的全部内容，再加上：所有平台上的完整输入重映射、带说话人标识的字幕、可调文字大小、至少一种色盲模式，以及所有无法延长或切换的定时输入都必须可调整。 | 中——需要专门实现工作 |
| **Comprehensive** | 包含 Standard 的全部内容，再加上：菜单屏幕阅读器支持、单声道音频选项、难度辅助模式、HUD 元素重新定位、降低运动模式，以及所有与玩法关键音频相关的视觉提示。 | 高——需要平台 API 集成和大量 UI 架构工作 |
| **Exemplary** | 包含 Comprehensive 的全部内容，再加上：完整字幕自定义（字体、大小、颜色、背景、位置）、高对比度模式、认知负荷辅助工具、所有仅音频提示的触觉 / 震动替代方案，以及外部第三方无障碍审计。 | 很高——需要专门无障碍预算和专家咨询 |

### 本项目的承诺

**目标层级**：[Standard]

**理由**：[写 3-5 句说明选择该层级的原因。不要只写层级名称——要解释理由。可考虑：游戏类型以及它如何对应常见无障碍障碍（例如，快节奏游戏更容易产生运动障碍；大量阅读的游戏更容易产生视觉障碍）？目标玩家是谁，该群体的残障流行率研究怎么说？平台要求是什么（Xbox 要求 ID@Xbox 的 XAG 合规）？团队能力如何？若降低一个层级，会以具体形式失去多少玩家群体？

示例：“这是一款面向 25-45 岁玩家的叙事 RPG，采用回合制战斗。回合制结构消除了动作游戏中最严重的运动障碍，但大量阅读的设计会产生显著的视觉和认知障碍。Standard 层级可覆盖这些需求。若要达到 Exemplary，需要专职无障碍工程师。Xbox ID@Xbox 项目对 Game Pass 考虑要求 XAG 合规，而 Standard 已满足。若降到 Basic，将排除依赖色盲模式或输入重映射的玩家，按 AbleGamers 数据估计约占目标受众的 8-12%。”]

**明确纳入范围的功能（超出层级基线）**：
- [例如，“完整字幕自定义——因为我们的游戏对白很多，字幕是主要信息通道”]
- [例如，“手柄单手模式——因为战斗中存在需要按住的输入”]

**明确排除在外的功能**：
- [例如，“游戏世界的屏幕阅读器（不含菜单）——需要超出当前能力范围的引擎工作。已记录在 Known Intentional Limitations 中。”]

---

## 视觉无障碍

> **为什么这一节排在最前**：视觉障碍影响使用无障碍功能的玩家比例最大。仅色觉缺陷就影响约 8% 的男性和 0.5% 的女性。在电视观看距离下的文字可读性常常是已发售游戏中最大的无障碍失败点。请在实现开始前记录每项视觉功能，因为在资源锁定后再补最小字号或颜色决策成本很高。

| 功能 | 目标层级 | 范围 | 状态 | 实现说明 |
|------|----------|------|------|---------|
| 最小文字大小——菜单 UI | Standard | 所有菜单界面 | Not Started | 1080p 下最小 24px。4K 时按比例缩放。参考：WCAG 2.1 SC 1.4.4 要求文本可放大到 200% 而不丢失内容。 |
| 最小文字大小——字幕 | Standard | 所有语音 / 字幕内容 | Not Started | 1080p 下最小 32px。3 米电视观看距离的玩家是约束条件。 |
| 最小文字大小——HUD | Standard | 游戏内 HUD | Not Started | 关键信息（生命值、弹药、目标）的最小字号为 20px。非关键 HUD 元素可更小。 |
| 文本对比度——UI 文本与背景 | Standard | 所有 UI 文本 | Not Started | 正文文字最低 4.5:1（WCAG AA）。大字号文字（18px+ 或 14px 加粗）为 3:1。使用自动对比度检查器在最终颜色值上测试。 |
| 文本对比度——字幕 | Standard | 字幕显示 | Not Started | 字幕最低 7:1 对比度（WCAG AAA）——玩家阅读速度快且无法控制背景。默认使用阴影或不透明背景框。 |
| 色盲模式——Protanopia | Standard | 所有颜色编码玩法内容 | Not Started | 红绿——影响约 6% 的男性。主要关注：生命条、敌人指示、地图标记。将红色信号改为橙 / 黄；将绿色信号改为青绿。 |
| 色盲模式——Deuteranopia | Standard | 所有颜色编码玩法内容 | Not Started | 绿红——影响约 1% 的男性。实际影响与 Protanopia 类似。常可由同一套调色方案覆盖。使用 Coblis 或 Colour Blindness Simulator 验证。 |
| 色盲模式——Tritanopia | Standard | 所有颜色编码玩法内容 | Not Started | 蓝黄——更少见（约 0.001%）。将蓝色 UI 元素改为紫色；将黄色改为橙色。 |
| 颜色是否唯一指示项审计 | Basic | 所有 UI 与玩法内容 | Not Started | 在下方表格中列出颜色是唯一差异点的所有位置。每一项在发售前都必须具备非颜色备份（图标、形状、纹理、文本标签）。 |
| UI 缩放 | Standard | 所有 UI 元素 | Not Started | 范围：75% 到 150%。默认：100%。缩放不得破坏布局——在最小和最大值下测试所有界面。HUD 缩放应与菜单缩放分离。 |
| 高对比度模式 | Comprehensive | 菜单（最低要求）；HUD（优先） | Not Started | 将所有半透明背景替换为完全不透明。将中间调 UI 颜色替换为黑 / 白 / 系统高对比度颜色。所有可交互元素都要加轮廓。 |
| 亮度 / gamma 控制 | Basic | 全局 | Not Started | 在图形设置中提供。包含参考校准图（在正确校准时几乎不可见的渐变或符号）。范围：相对默认值 -50% 到 +50%。 |
| 屏幕闪烁 / 频闪警告 | Basic | 所有过场动画、VFX | Not Started | (1) 开场前警告界面，提示光敏癫痫风险。 (2) 按 Harding FPA 标准审查所有强闪烁 VFX（高于亮度阈值时每秒不超过 3 次闪烁）。(3) 可选：闪烁减少模式，将闪烁幅度降低 80%。 |
| 运动 / 动画减弱模式 | Standard | 所有 UI 转场、镜头震动、VFX | Not Started | 减少或消除：屏幕震动、镜头晃动、运动模糊、菜单中的视差滚动、循环背景动画。无法完全消除：玩家移动动画（否则会破坏可读性）。在无障碍设置中切换。 |
| 字幕——开 / 关 | Basic | 所有语音内容 | Not Started | 默认：关闭（行业标准——很多玩家更偏好沉浸感）。首次启动时显著提供。 |
| 字幕——说话人识别 | Standard | 所有语音内容 | Not Started | 在对白前显示说话人姓名。如果颜色差异不只依赖色相（需通过色盲兼容性测试），可按说话人进行颜色编码。 |
| 字幕——样式自定义 | Comprehensive | 字幕显示 | Not Started | 字体大小（至少 4 档）、背景不透明度（0–100%）、文字颜色（白 / 黄 / 自定义）、位置（底部 / 顶部 / 相对玩家）。 |
| 字幕——音效说明 | Comprehensive | 玩法关键 SFX | Not Started | 哪些 SFX 归类见 Auditory Accessibility 部分。格式为方括号中的 [声音描述]，与对白区分开。 |

### 颜色是否唯一指示项审计

> 填写所有当前仅靠颜色区分的玩法或 UI 元素。在发售前逐项解决。已解决的条目必须有在上面三种色盲模式下都有效的非颜色备份。

| 位置 | 颜色信号 | 传达内容 | 非颜色备份 | 状态 |
|------|----------|----------|----------|------|
| [Health bar] | [Red = low health] | [Player is near death] | [Bar also shows numeric value and flashes] | [Not Started] |
| [Minimap markers] | [Red = enemy, green = ally] | [Unit allegiance] | [Enemy markers are triangles; ally markers are circles] | [Not Started] |
| [Inventory item rarity] | [Color-coded border (grey/blue/purple/gold)] | [Item quality tier] | [Rarity name shown on hover/focus; icon star count] | [Not Started] |
| [Add row for each color-coded element] | | | | |

---

## 运动无障碍

> **为什么运动无障碍对游戏很重要**：游戏对运动能力的要求通常高于大多数软件。网页表单只需要精确点击；游戏可能要求快速同时按键组合并持续特定时长。运动障碍范围很广——从震颤（影响精确度）到偏瘫（仅一只手可用）再到 RSI（影响持续按住能力）。AbleGamers 的 Able Assistance 项目估计，美国有 3500 万玩家存在影响游戏能力的残障。以下许多功能如果从一开始就规划，成本很低；若在发售后再补，代价极高。

| 功能 | 目标层级 | 范围 | 状态 | 实现说明 |
|------|----------|------|------|---------|
| 完整输入重映射 | Standard | 所有玩法输入，所有平台 | Not Started | 默认绑定的每个输入都必须可重绑。重映射对键盘、鼠标、手柄以及任何支持的外设分别生效。任何两个动作都不得同时绑定到同一输入（冲突时警告）。将重映射持久化到玩家档案。 |
| 输入方式切换 | Standard | PC | Not Started | 玩家必须能够在任意时刻在键鼠和手柄之间切换，无需重启。UI 必须动态更新提示（显示当前输入方式的正确按键图标）。 |
| 单手模式 | [Tier] | [Identify which features require two simultaneous hands] | Not Started | 审计所有多输入动作。对于每一项：能否用单手完成？如果不能，请提供切换替代方案或按住切换版本。在此明确哪些功能有单手路径，哪些没有。 |
| 按住替代方案 | Standard | 所有按住输入 | Not Started | 每个“按住 [button] 以 [action]”都必须提供切换替代方案。切换模式：第一次按下激活，第二次按下停用。示例：“按住冲刺”变为可选的“切换冲刺”模式。请在此列出游戏中的所有按住输入。 |
| 快速输入替代方案 | Standard | 任何按钮连按 / 快速输入序列 | Not Started | 任何要求持续每秒超过 3 次按键的输入，都必须提供单次按键的切换替代方案。示例：Hades 的“按住以持续冲刺”方案很优雅。 |
| 输入时序调整 | Standard | QTE、定时按键、节奏输入 | Not Started | 在无障碍设置中提供时序窗口倍率。最小范围：0.5x 到 3.0x。默认：1.0x。在 3.0x 下，500ms 窗口变为 1500ms。记录本游戏中的每个定时输入，并在所有倍率下测试。 |
| 瞄准辅助 | Standard | 所有远程战斗 / 锁定目标 | Not Started | 不只是开 / 关——要分别提供细粒度选项：辅助强度（0–100%）、辅助半径、瞄准吸附（snap-to-target）和瞄准减速（接近目标时减速）等滑块。默认值应调校为有帮助但不突兀。 |
| 自动冲刺 / 移动辅助 | Standard | 移动系统 | Not Started | “按住冲刺”切换（见上）。另外：自动跑步选项（按住方向，玩家无需继续按输入即可持续移动）。请明确所有在正常玩法中需要持续按住的移动输入。 |
| 跳台 / 穿越辅助 | [Tier] | [If game has platforming] | Not Started | 评估自动抓边（宽松边缘检测）、土狼时间延长和跳跃高度调整是否适合本游戏设计。如果没有平台跳跃系统，则标记为 N/A。 |
| HUD 元素重新定位 | Comprehensive | 所有 HUD 元素 | Not Started | 允许玩家将生命条、小地图和任务追踪器移动到更适合自己的屏幕位置。对于使用头部跟踪或眼动硬件、外围视野覆盖较弱的玩家尤其重要。 |

---

## 认知无障碍

> **为什么认知无障碍常常未被充分规格化**：认知无障碍会影响 ADHD、阅读障碍、自闭症谱系、获得性脑损伤以及焦虑障碍玩家——这一合计人群比许多工作室意识到的更大。它也能帮助高压时刻的所有玩家。最常见的失败点是：无法随时暂停、教程信息只能看一次，以及需要同时跟踪过多状态的系统。像 Hades 和 Celeste 这样的游戏已经证明，认知辅助选项（god mode、持久提醒、延长文本显示）不会损害不使用它们的玩家体验。

| 功能 | 目标层级 | 范围 | 状态 | 实现说明 |
|------|----------|------|------|---------|
| 难度选项 | Standard | 所有玩法难度参数 | Not Started | 尽量使用更细粒度的滑块（输出伤害、承受伤害、敌人 агression、敌人速度），而不是单一 Easy/Normal/Hard 标签。记录哪些参数可调，哪些固定。固定参数需要设计说明。 |
| 随时暂停 | Basic | 所有游戏状态 | Not Started | 玩家必须能在任何游戏状态下暂停，包括过场、对话和教程序列。记录当前哪些状态禁止暂停，以及该限制的设计理由。任何限制都属于风险。 |
| 教程持久化 | Standard | 所有教程和帮助文本 | Not Started | 在关闭教程提示后，玩家必须能在菜单的 Help 部分重新查看。不要依赖玩家第一次看到就能吸收教程——AbleGamers 研究显示，许多玩家会条件反射式地关闭提示。 |
| 任务 / 目标清晰度 | Standard | 任务与目标系统 | Not Started | 在游戏过程中，当前活动目标必须始终能在 2 次按键内访问到。按需显示完整目标文本，而不是仅显示截断标记。避免需要推断的目标（“调查北部区域”——具体是哪里？）。 |
| 音频信息的视觉指示 | Standard | 所有承载玩法信息的 SFX | Not Started | 审计所有传达玩法关键状态的音效。每一项都要问：是否有视觉对应？屏幕外敌人的方向音频需要屏幕边缘指示。关键警告（Boss 阶段转换、陷阱触发）需要视觉提示。完整列表见 Auditory Accessibility。 |
| UI 阅读时间 | Standard | 所有自动消失对话框 | Not Started | 任何包含可操作信息的对话、通知或提示，其自动消失时间不得少于 5 秒。优先方案：完全不要自动消失——改为要求玩家确认。在此记录所有自动消失元素及其当前时长。 |
| 认知负荷文档 | Comprehensive | 每个游戏系统 | Not Started | 对 `systems-index.md` 中的每个系统，记录它要求玩家同时跟踪的最大事项数量。若数量超过 4，则标记。该规则不是硬性限制，而是评审触发条件——高认知负荷系统需要额外的 UI 清晰度补偿。见下方 Per-Feature Accessibility Matrix。 |
| 导航辅助 | Standard | 世界导航 | Not Started | 快速旅行（到已访问地点）、当前目标的路标系统、始终可见的可选目标指示器。记录哪些适用于本游戏设计，哪些是有意省略的。 |

---

## 听觉无障碍

> **即使对听力正常的玩家，听觉无障碍也很重要的原因**：7% 的玩家是聋人或重听。此外，大量玩家经常在音频被降低或不可用的环境中游戏（通勤、共享家庭空间、婴儿睡觉）。在考虑无障碍之前，仅通过音频传达玩法关键内容本身就是设计失败。指导原则：任何会改变玩家下一步应做什么的声音，都必须有视觉对应。

| 功能 | 目标层级 | 范围 | 状态 | 实现说明 |
|------|----------|------|------|---------|
| 所有语音对白字幕 | Basic | 所有语音内容 | Not Started | 100% 覆盖——无例外。包括叙述、引擎内对白、远处听到的无线电 / 环境对白。测试字幕与语音节奏的同步。 |
| 玩法关键 SFX 的闭合字幕 | Comprehensive | 下方识别的 SFX 列表 | Not Started | 并非所有 SFX 都需要字幕——只有那些传达玩家无法通过视觉推断状态的音效才需要。见下方 SFX 审计表。 |
| 单声道音频选项 | Comprehensive | 全局音频输出 | Not Started | 将立体声 / 空间音频折叠为单声道。保留声道之间的音量平衡，而不是将两侧都加到满音量。对单侧耳聋玩家至关重要。 |
| 独立音量控制 | Basic | Music / SFX / Voice / UI 音频总线 | Not Started | 至少四个独立滑块。持久化到玩家档案。范围：0–100%，默认 80%。在主设置和暂停菜单中都提供。 |
| 定向音频的视觉表现 | Comprehensive | 所有屏幕外威胁和音频事件 | Not Started | 指向音源的屏幕边缘指示器。透明度随音量变化（越近越不透明）。两种变体：威胁指示器（红色）和信息指示器（中性）。例如：《The Last of Us Part II》使用了屏幕边缘指示器显示屏幕外敌人位置。 |
| 助听器兼容模式 | Standard | 高频音频提示 | Not Started | 审计所有音频提示的频率范围。任何仅通过 4kHz 以上高频声音传达关键信息的提示，都必须有低频或视觉对应方案。助听器通常会过滤高频。 |

### 玩法关键 SFX 审计

> 识别每个传达玩家需要采取行动状态的音效。
> 此表中的每一项都必须有已确认的视觉备份或字幕。

| 音效 | 传达内容 | 视觉备份 | 是否需要字幕 | 状态 |
|------|---------|---------|-------------|------|
| [Enemy attack windup sound] | [Incoming damage — player should dodge] | [Enemy animation telegraph visible from all camera angles] | [No — visual is sufficient] | [Not Started] |
| [Trap trigger click] | [Trap is about to fire] | [Not always visible depending on camera angle] | [Yes — "[CLICK]" caption with directional indicator] | [Not Started] |
| [Low health heartbeat] | [Player health critical] | [Health bar also shows critical state visually] | [No — visual is sufficient] | [Not Started] |
| [Quest completion chime] | [Objective completed] | [Quest tracker updates visually] | [No — visual is sufficient] | [Not Started] |
| [Add each SFX that changes what the player should do] | | | | |

---

## 平台无障碍 API 集成

> **为什么这一节存在**：每个平台都提供原生无障碍 API，使用这些 API 后，OS 级功能（系统屏幕阅读器、显示辅助、运动无障碍服务）才能与游戏协同工作。忽略这些 API 不会破坏游戏本身，但会让依赖 OS 级无障碍工具的玩家在游戏中得不到任何收益。尤其是 Xbox，认证需要 XAG 合规。在承诺某个层级之前，请先核对平台要求——平台要求决定最低门槛，而不是上限。

| 平台 | API / 标准 | 计划功能 | 状态 | 备注 |
|------|------------|---------|------|------|
| Xbox (GDK) | Xbox Game Core Accessibility / XAG | [通过 Xbox Ease of Access 的输入重映射、高对比度支持、菜单旁白集成] | Not Started | ID@Xbox Game Pass 考虑需要 XAG 合规。检查 XAG 清单：https://docs.microsoft.com/gaming/accessibility/guidelines |
| PlayStation 5 | Sony Accessibility Guidelines / AccessibilityNode API | [菜单屏幕阅读器透传、单声道音频、高对比度] | Not Started | 如果游戏通过 AccessibilityNode 数据暴露 UI 元素，PS5 可原生支持系统级音频描述和单声道音频。 |
| Steam (PC) | Steam Accessibility Features / SDL | [通过 Steam Input 实现手柄输入重映射、字幕支持] | Not Started | Steam Input 支持与游戏内重映射分离的系统级重映射。仍然需要游戏内的键鼠重映射。 |
| iOS | UIAccessibility / VoiceOver | [若计划移动端移植，则提供菜单 VoiceOver 支持] | N/A | 仅在移动版发行纳入范围时才需要。 |
| Android | AccessibilityService / TalkBack | [若计划移动端移植，则提供菜单 TalkBack 支持] | N/A | 仅在移动版发行纳入范围时才需要。 |
| PC (Screen Reader) | JAWS / NVDA / Windows Narrator | [菜单导航播报] | Not Started | 需要 UI 元素通过平台 UI 层暴露可访问名称和角色。Godot 4.5+ 的 AccessKit 集成可为受支持的控件类型提供此能力。请对照 engine-reference/godot/ 目录验证。 |

---

## 按功能划分的无障碍矩阵

> **为什么要有这张矩阵**：无障碍不是一个设置列表，而是每个游戏系统的属性。此矩阵创建了游戏的“无障碍影响”视图：哪些系统存在哪些障碍，以及这些障碍是否已被处理。当 `systems-index.md` 中新增系统时，必须在这里新增一行。若某系统存在未处理的无障碍问题，则不能在系统索引中标记为 Approved。

| 系统 | 视觉问题 | 运动问题 | 认知问题 | 听觉问题 | 已处理 | 备注 |
|------|----------|----------|----------|----------|------|------|
| [Combat System] | [Enemy health bars are color-coded; attack animations may cause motion sickness] | [Rapid input required for combos; hold inputs for guard] | [Track enemy patterns + cooldowns + player resources simultaneously] | [Audio cues for off-screen attacks; critical damage warning sounds] | [Partial] | [Colorblind palette applied; hold-to-block toggle needed] |
| [Inventory / Equipment] | [Item rarity conveyed by border color] | [No motor concerns — turn-based] | [Item stats comparison requires reading multiple values] | [None — no critical audio in this system] | [Partial] | [Non-color rarity indicators in progress] |
| [Dialogue System] | [Subtitle display depends on contrast settings] | [No motor concerns] | [Long dialogue trees with time pressure on dialogue choices] | [All dialogue must be subtitled] | [Not Started] | [Timed dialogue choices must support extended timer option] |
| [Navigation / World Map] | [Map marker colors] | [No motor concerns] | [Quest objective clarity; waypoint visibility] | [Audio pings for objectives have no visual equivalent] | [Not Started] | |
| [Add system from systems-index.md] | | | | | | |

---

## 无障碍测试计划

> **为什么要将无障碍测试与 QA 分开**：标准 QA 测试的是功能是否工作。无障碍测试检验的是这些功能是否能被使用它们的玩家正确使用。这是不同的测试。字幕系统可以通过 QA（显示文本），却在无障碍测试中失败（文本在电视观看距离对低视力玩家不可读）。请规划三种测试：自动化（对比度、文字大小）、内部手动（团队成员用无障碍模拟器模拟障碍），以及用户测试（实际使用这些功能的玩家）。

| 功能 | 测试方法 | 测试用例 | 通过标准 | 负责人 | 状态 |
|------|----------|----------|---------|--------|------|
| 文本对比度 | 自动化——对所有 UI 截图运行对比度分析工具 | 游戏所有状态下的所有文字 / 背景组合 | 所有正文文字 ≥ 4.5:1；所有大字号文字 ≥ 3:1；字幕背景 ≥ 7:1 | ux-designer | Not Started |
| 色盲模式 | 手动——在所有开启模式的游戏截图上使用 Coblis 模拟器 | 探索、战斗、背包的游戏截图，在每种模式下都测试 | 任何模式下都不会丢失关键信息；玩家无需依赖颜色区分即可完成所有目标 | ux-designer | Not Started |
| 输入重映射 | 手动——将所有输入重映射为非默认绑定，完成教程和第一关 | 所有默认输入都已重绑；玩法功能正常；不存在绑定冲突 | 重映射后所有动作都可访问；冲突防护有效；重启后绑定仍然保留 | qa-tester | Not Started |
| 字幕准确性 | 手动——与语音脚本核对，检查所有台词 | 所有语音内容；字幕时序；说话人识别 | 100% 语音台词都有字幕；多角色场景中所有角色都被识别；行结束后字幕显示不超过 3 秒 | qa-tester | Not Started |
| 按住输入切换 | 手动——启用所有切换替代方案，完成全部战斗与穿越序列 | 所有按住输入都处于切换模式 | 切换模式下所有按住动作都可完成；启用切换后没有任何玩法状态仍必须持续按住 | qa-tester | Not Started |
| 降低运动模式 | 手动——启用该模式，浏览所有菜单并完成游戏前一小时内容 | 所有菜单转场；所有 HUD 动画；所有镜头震动事件 | 菜单中无循环动画；镜头震动不超过阈值；所有屏幕转场均为淡入淡出或裁切 | ux-designer | Not Started |
| 平台屏幕阅读器（菜单） | 手动——启用 OS 屏幕阅读器，浏览所有菜单 | 主菜单、设置、暂停菜单、背包、地图 | 所有可交互菜单元素都有屏幕阅读器播报；导航顺序合理；没有元素无法通过键盘 / D-pad 到达 | ux-designer | Not Started |
| 用户测试——色盲 | 与色盲参与者进行用户测试 | 含每种色盲模式的完整游戏流程 | 参与者无需请求颜色说明即可完成所有内容；没有导致会话中断的困惑 | producer | Not Started |
| 用户测试——运动障碍 | 与使用单手或辅助控制器的参与者进行用户测试 | 启用切换和延长时序模式的完整游戏流程 | 参与者在可接受范围内完成所有 MVP 内容，完成时间接近健全玩家 | producer | Not Started |

---

## 已知的有意限制

> **为什么要记录未包含内容**：未记录的遗漏会在认证或社区反馈中变成惊喜。将限制及其理由写清楚，表明这是有意选择，而不是疏忽。它也能识别哪些玩家未被覆盖以及缓解方案是什么。这里每一项都是风险——请诚实评估。

| 功能 | 需要层级 | 为什么未包含 | 风险 / 影响 | 缓解措施 |
|------|----------|-------------|-----------|---------|
| [游戏世界（NPC、物体、环境文字）的屏幕阅读器支持] | Exemplary | 引擎（Godot 4.6）的 AccessKit 集成仅覆盖菜单；扩展到游戏世界需要自定义空间音频描述系统，超出当前范围 | 影响盲人和低视力玩家，他们可以操作菜单，但无法独立探索游戏世界 | 确保所有关键信息在可访问菜单系统（任务日志、地图）中有重复；评估是否作为发售后 DLC |
| [完整字幕自定义（字体 / 颜色 / 背景）] | Comprehensive | 范围缩减——本项目目标为 Standard 层级。Godot 中自定义字体渲染需要额外的资源管线工作 | 影响有特定可读性需求的聋人和重听玩家；尤其影响使用自定义字体的阅读障碍玩家 | 提供两种预设字幕样式（默认和高可读性）作为部分缓解；记录为发售后更新 |
| [所有音频提示的触觉 / 震动替代方案] | Exemplary | 非 Xbox 平台的手柄震动 API 集成超出 v1.0 范围 | 影响依赖触觉反馈的聋人玩家；使用非 Xbox 手柄的 PC 玩家没有震动反馈 | Xbox 手柄震动集成在范围内；评估 PlayStation DualSense 触觉 API 作为发售后补丁 |
| [Add any other intentionally excluded accessibility feature] | | | | |

---

## 审计历史

> **为什么要记录审计历史**：无障碍不是一次认证后就结束的。平台要求会变化。新功能可能引入新障碍。法律标准也会演进。审计历史能够证明尽职调查，并有助于识别审计之间的回归。

| 日期 | 审计人 | 类型 | 范围 | 发现摘要 | 状态 |
|------|-------|------|------|---------|------|
| [Date] | [Internal — ux-designer] | Internal review | [Pre-submission checklist against committed tier] | [e.g., "12 items verified, 3 open issues: subtitle contrast below target in 2 scenes, color-only indicator on minimap not resolved"] | [In Progress] |
| [Date] | [External — AbleGamers Player Panel] | User testing | [Motor accessibility — one-hand mode and timing adjustments] | [e.g., "Toggle modes functional. Timed QTE window at 3x still failed for one participant — recommend 5x option."] | [Findings addressed] |
| [Add row for each audit] | | | | | |

---

## 外部资源

| 资源 | URL | 相关性 |
|------|-----|--------|
| WCAG 2.1 (Web Content Accessibility Guidelines) | https://www.w3.org/TR/WCAG21/ | 基础无障碍标准——对比度、文字大小、输入要求 |
| Game Accessibility Guidelines | https://gameaccessibilityguidelines.com | 按类别和成本组织的综合游戏专用清单 |
| AbleGamers Player Panel | https://ablegamers.org/player-panel/ | 面向残障玩家的用户测试服务与咨询 |
| Xbox Accessibility Guidelines (XAG) | https://docs.microsoft.com/gaming/accessibility/guidelines | Xbox 认证必读；结构良好的功能清单 |
| PlayStation Accessibility Guidelines | https://www.playstation.com/en-us/accessibility/ | Sony 平台要求；同时包含写得很好的设计指导 |
| Colour Blindness Simulator (Coblis) | https://www.color-blindness.com/coblis-color-blindness-simulator/ | 用于在截图上模拟色盲模式的免费工具 |
| Accessible Games Database | https://accessible.games | 关于无障碍游戏设计决策的研究与示例 |
| CVAA (21st Century Communications and Video Accessibility Act) | https://www.fcc.gov/consumers/guides/21st-century-communications-and-video-accessibility-act-cvaa | 美国法律要求，适用于包含通信功能（语音聊天、消息）的游戏 |

---

## 待解决问题

| 问题 | 负责人 | 截止日期 | 解决方案 |
|------|-------|----------|---------|
| [Does Godot 4.6 AccessKit support dynamic accessibility node updates for HUD elements, or only static menus?] | [ux-designer] | [Before Technical Setup gate] | [Unresolved — check engine-reference/godot/ docs] |
| [What is the Xbox ID@Xbox minimum XAG compliance requirement for our release window?] | [producer] | [Before Pre-Production gate] | [Unresolved] |
| [Will the dialogue system support timed choice extensions without a full architecture change?] | [lead-programmer] | [During Technical Design] | [Unresolved] |
| [Add question] | [Owner] | [Deadline] | [Resolution] |