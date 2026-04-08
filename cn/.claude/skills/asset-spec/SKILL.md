---
name: asset-spec
description: "根据 GDD、关卡文档或角色档案生成逐资产的视觉规格与 AI 生成提示词。会产出结构化规格文件并更新主资产清单。请在 art bible 与 GDD/关卡设计获批后、正式生产开始前运行。"
argument-hint: "[system:<name> | level:<name> | character:<name>] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
---

如果没有提供参数，先检查 `design/assets/asset-manifest.md` 是否存在：
- 如果存在：读取它，找出第一个状态为 "Needed" 但还没有写入 spec 文件的上下文（system/level/character），然后用 `AskUserQuestion`：
  - 提示："下一个尚未规格化的上下文是 **[target]**。要为它生成 asset specs 吗？"
  - 选项：`[A] Yes — spec [target]` / `[B] Pick a different target` / `[C] Stop here`
- 如果不存在 manifest：失败并提示：
  > "Usage: `/asset-spec system:<name>` — 例如 `/asset-spec system:tower-defense`
  > 或：`/asset-spec level:iron-gate-fortress` / `/asset-spec character:frost-warden`
  > 请在 art bible 与 GDD 获批后运行。"

---

## 阶段 0：解析参数

提取：
- **Target type**：`system`、`level` 或 `character`
- **Target name**：冒号后的名称（规范化为 kebab-case）
- **Review mode**：如果存在，则为 `--review [full|lean|solo]`

**模式行为：**
- `full`（默认）：并行 spawn `art-director` 和 `technical-artist`
- `lean`：只 spawn `art-director`——更快，跳过技术约束检查
- `solo`：不 spawn 代理——由主会话仅基于 art bible 规则编写规格。适合简单资产类别，或速度比深度更重要时使用。

---

## 阶段 1：收集上下文

在询问用户任何事情之前，先读取所有源材料。

### 必需读取：
- **Art bible**：读取 `design/art/art-bible.md`——若缺失则失败：
  > "未找到 art bible。请先运行 `/art-bible`——asset specs 以 art bible 的视觉规则和资产标准为锚点。"
  提取：Visual Identity Statement、Color System（语义颜色）、Shape Language、Asset Standards（第 8 章——尺寸、格式、多边形预算、纹理分辨率层级）。

- **技术偏好**：读取 `.claude/docs/technical-preferences.md`——提取性能预算和命名约定。

### 按目标类型读取源文档：
- **system**：读取 `design/gdd/[target-name].md`。提取 **Visual/Audio Requirements** 章节。如果不存在或内容为 `[To be designed]`：
  > "`design/gdd/[target-name].md` 的 Visual/Audio 章节是空的。要么运行 `/design-system [target-name]` 完成 GDD，要么手动描述视觉需求。"
  使用 `AskUserQuestion`：`[A] Describe needs manually` / `[B] Stop — complete the GDD first`
- **level**：读取 `design/levels/[target-name].md`。提取美术需求、资产列表、VFX 需求，以及第 4 步中 art-director 的生产概念规格。
- **character**：读取 `design/narrative/characters/[target-name].md`，或在 `design/narrative/` 中搜索该角色档案。提取视觉描述、角色定位、以及任何指定的区分特征。

### 可选读取：
- **现有 manifest**：如果存在，读取 `design/assets/asset-manifest.md`——提取该目标已规格化的资产，避免重复。
- **相关 specs**：Glob `design/assets/specs/*.md`——扫描是否存在可共享的资产（例如，一个系统中规格化的通用 UI 元素可能也适用于此处）。

### 呈现上下文摘要：
> **Asset Spec: [Target Type] — [Target Name]**
> - Source doc: [path] — 已识别 [N] 类资产
> - Art bible: 已找到 —— 第 8 章是 Asset Standards
> - 该目标已有的 specs： [N already specced / none]
> - 在其他 specs 中找到的共享资产： [list or "none"]

---

## 阶段 2：资产识别

从源文档中提取所有提到的资产类型——显式和隐式都算。

**针对 systems**：查找 VFX 事件、sprite 引用、UI 元素、音频触发、粒子效果、图标需求，以及任何“视觉反馈”相关描述。

**针对 levels**：查找独特环境道具、氛围 VFX、灯光设置、环境音、天空盒/背景，以及任何区域专属材质。

**针对 characters**：查找 sprite sheet（idle、walk、attack、death）、portrait/avatar、附着于能力的 VFX、UI 表示（icon、health bar skin）。

将资产分组为以下类别：
- **Sprite / 2D Art** —— 角色 sprite、UI icon、tile sheet
- **VFX / Particles** —— 命中特效、环境粒子、屏幕特效
- **Environment** —— 道具、地砖、背景、天空盒
- **UI** —— HUD 元素、菜单美术、字体（如为自定义）
- **Audio** —— SFX、音乐曲目、环境循环音 *(注意：音频规格只写描述——不生成提示词)*
- **3D Assets** —— 网格、材质（如引擎适用）

将完整识别列表呈现给用户。使用 `AskUserQuestion`：
- 提示："我为 **[target]** 识别出 [N] 个资产，分布在 [N] 个类别中。请在规格化前先审阅："
- 先在对话文本中展示分组列表
- 选项：`[A] Proceed — spec all of these` / `[B] Remove some assets` / `[C] Add assets I didn't catch` / `[D] Adjust categories`

在用户确认资产列表之前，不要进入阶段 3。

---

## 阶段 3：规格生成

根据 review mode spawn 专家代理。**所有 Task 调用必须同时发出——不要等一个完成后再发下一个。**

### Full mode — 并行 spawn：

**`art-director`** via Task：
- 提供：阶段 2 的完整资产列表、art bible 的 Visual Identity Statement、Color System、Shape Language、源文档中的视觉需求，以及 art bible 第 9 章提到的任何参考游戏/艺术
- 询问："针对列表中的每个资产，分别提供：(1) 2–3 句视觉描述，锚定到 art bible 的 shape language 和 color system —— 要具体到不同艺术家也能产出一致结果；(2) 一个可用于 AI 图像工具的生成提示词（Midjourney/Stable Diffusion 风格——包含风格关键词、构图、颜色锚点、负面提示）；(3) 哪些 art bible 规则直接约束这个资产（按章节引用）。对于音频资产，请描述声音特征而不是生成提示词。"

**`technical-artist`** via Task：
- 提供：完整资产列表、art bible 的 Asset Standards（第 8 章）、technical-preferences.md 中的性能预算、引擎名称与版本
- 询问："针对列表中的每个资产，指定：(1) 精确尺寸或多边形数（匹配 art bible Asset Standards 的层级——不要发明新尺寸）；(2) 文件格式与导出设置；(3) 命名约定（来自 technical-preferences.md）；(4) 该资产类型必须遵守的引擎特定约束；(5) 如适用的 LOD 要求。标记任何 art bible 偏好与引擎约束冲突的资产类型。"

### Lean mode —— 仅 spawn art-director（跳过 technical-artist）。

### Solo mode —— 跳过两者。仅根据 art bible 规则推导规格，并注明未验证技术约束。

**在进入阶段 4 之前要收齐两个响应。**如果 art-director 与 technical-artist 之间存在冲突（例如 art-director 指定 4K 纹理，但 technical-artist 发现引擎预算要求 512px），要明确展示——不要静默解决。

---

## 阶段 4：汇编并审阅

将代理输出合并为每个资产的草案规格。用以下格式在对话文本中展示所有规格：

```
## ASSET-[NNN] — [Asset Name]

| Field | Value |
|-------|-------|
| Category | [Sprite / VFX / Environment / UI / Audio / 3D] |
| Dimensions | [e.g. 256×256px, 4-frame sprite sheet] |
| Format | [PNG / SVG / WAV / etc.] |
| Naming | [e.g. vfx_frost_hit_01.png] |
| Polycount | [if 3D — e.g. <800 tris] |
| Texture Res | [e.g. 512px — matches Art Bible §8 Tier 2] |

**Visual Description:**
[2–3 sentences. Specific enough for two artists to produce consistent results.]

**Art Bible Anchors:**
- §3 Shape Language: [relevant rule applied]
- §4 Color System: [color role — e.g. "uses Threat Blue per semantic color rules"]

**Generation Prompt:**
[Ready-to-use prompt. Include: style keywords, composition notes, color palette anchors, lighting direction, negative prompts.]

**Status:** Needed
```

展示完所有规格后，使用 `AskUserQuestion`：
- 提示："Asset specs for **[target]** — [N] assets. Review complete?"
- 选项：`[A] Approve all — write to file` / `[B] Revise a specific asset` / `[C] Regenerate with different direction`

如果选 [B]：询问要改哪个资产、改什么。就地修订并重新展示。不要为小的文本修订重新 spawn 代理——只有视觉方向本身需要变化时才重新 spawn。

如果选 [C]：询问要如何改方向。用更新后的 brief 重新 spawn 相关代理。

---

## 阶段 5：写入规格文件

获批后，询问："May I write the spec to `design/assets/specs/[target-name]-assets.md`?"

写入文件，内容如下：

```markdown
# Asset Specs — [Target Type]: [Target Name]

> **Source**: [path to source GDD/level/character doc]
> **Art Bible**: design/art/art-bible.md
> **Generated**: [date]
> **Status**: [N] assets specced / [N] approved / [N] in production / [N] done

[all asset specs in ASSET-NNN format]
```

然后更新 `design/assets/asset-manifest.md`。如果不存在则创建：

```markdown
# Asset Manifest

> Last updated: [date]

## Progress Summary

| Total | Needed | In Progress | Done | Approved |
|-------|--------|-------------|------|----------|
| [N] | [N] | [N] | [N] | [N] |

## Assets by Context

### [Target Type]: [Target Name]
| Asset ID | Name | Category | Status | Spec File |
|----------|------|----------|--------|-----------|
| ASSET-001 | [name] | [category] | Needed | design/assets/specs/[target]-assets.md |
```

如果 manifest 已存在，追加新的上下文块并更新 Progress Summary 数值。

询问："May I update `design/assets/asset-manifest.md`?"

---

## 阶段 6：结束

使用 `AskUserQuestion`：
- 提示："Asset specs complete for **[target]**. What's next?"
- 选项：
  - `[A] Spec another system — /asset-spec system:[next-system]`
  - `[B] Spec a level — /asset-spec level:[level-name]`
  - `[C] Spec a character — /asset-spec character:[character-name]`
  - `[D] Run /asset-audit — validate delivered assets against specs`
  - `[E] Stop here`

---

## Asset ID 分配

Asset ID 在整个项目范围内按顺序分配——不是按上下文分别编号。分配前先读 manifest 找到当前最大编号：

```
Grep pattern="ASSET-" path="design/assets/asset-manifest.md"
```

新资产从 `ASSET-[highest + 1]` 开始。这样 ID 在整个项目里稳定且唯一。

如果还没有 manifest，则从 `ASSET-001` 开始。

---

## Shared Asset Protocol

在为资产编写规格之前，先检查其他上下文的 spec 中是否已经存在等价资产：

- 通用 UI 元素（health bar、score display）通常跨系统共享
- 通用环境道具可能出现在多个关卡
- 角色 VFX（hit spark、death effect）可复用基础规格，只变更颜色

如果找到匹配项：引用现有 ASSET-ID，而不是重复创建。在 manifest 的 referenced-by 列中注明共享用途。

> "ASSET-012 (Generic Hit Spark) already specced for Combat system. Reusing for Tower Defense — adding tower-defense to referenced-by."

---

## 错误恢复协议

如果任何被 spawn 的代理返回 BLOCKED 或无法完成：

1. 立即上报：`"[AgentName]: BLOCKED — [reason]"`
2. 在 `lean` 模式中，或如果 `technical-artist` 阻塞：仅使用 art-director 输出继续——注明未验证技术约束
3. 在 `solo` 模式中，或如果 `art-director` 阻塞：根据 art bible 规则推导描述——标记为 "Art director not consulted — verify against art bible before production"
4. 始终产出部分规格——不要因为一个代理阻塞就丢弃工作

---

## 协作协议

每个阶段都遵循：**Identify → Confirm → Generate → Review → Approve → Write**

- 绝不要在未先与用户确认资产列表前就编写资产规格
- 始终将规格锚定在 art bible 上——与 art bible 冲突的规格就是错误的
- 展示所有代理分歧——不要静默选择其中一个
- 只有在明确获批后才写入 spec 文件
- 写完 spec 后立即更新 manifest

---

## 推荐下一步

- 运行 `/asset-spec [next-context]`，继续为剩余系统、关卡或角色编写规格
- 运行 `/asset-audit`，将交付资产与书面规格对照，识别缺口或不匹配