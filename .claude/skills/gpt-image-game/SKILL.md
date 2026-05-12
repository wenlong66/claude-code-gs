---
name: gpt-image-game
description: Use this skill whenever the user wants game-focused image generation with OpenAI gpt-image-2, including game characters, character portraits, monsters, NPCs, game UI, HUD, buttons, icons, popups, cards, green-screen assets, or says 游戏角色、立绘、游戏UI、HUD、按钮、图标、绿底图、游戏素材、生图、出图. This skill is for game image generation only.
user-invocable: true
allowed-tools: Bash, Read, Write, Glob
---

# gpt-image-game —— 游戏角色 / 游戏 UI 绿底生图与透明切片

这个 skill 只负责两件事：
1. 把游戏美术需求转成默认绿底的 `gpt-image-2` 图片文件
2. 在需要拆分素材时，按绿底抠图并导出透明散图 PNG

## 何时使用

当用户要生成游戏角色素材或游戏 UI 素材，并且希望：
- 按某个游戏画面设计尺寸来构图或设计 UI
- UI 素材图生成后自动切成多个散图
- 使用绿底图方便后续自动抠图切分

典型场景：
- 角色立绘、怪物、NPC、道具拟人
- 游戏卡面、头像裁切素材
- HUD、按钮、图标、弹窗、面板、状态条
- 一张 UI 素材图生成后，按绿底抠图切出多个独立 PNG
- 用户明确提到 `gpt-image-2`
- 用户用中文说“游戏角色 / 立绘 / 游戏 UI / HUD / 绿底图 / 游戏素材 / 生图 / 出图”

## 先确认六件事

如果用户没有一次性讲清楚，先补齐：
1. **主题**：画什么角色或什么 UI
2. **类型**：`character` 还是 `ui`
3. **设计尺寸**：例如 `1080x1920`、`1920x1080`、`2048x2048`
4. **背景策略**：默认绿底；如果要切图，会再自动转成透明散图
5. **是否切散图**：是否要在生成后自动切分
6. **数量**：先出 1 张还是多张变体

如果用户没有把画面描述清楚，先给出一版精炼 prompt 再生成。

## 设计尺寸说明

`--design-size` 表示的是**游戏画面设计尺寸**，不是 API 的真实生图像素尺寸。

例如：
- `--design-size 1920x1080` 的意思是“按 1920x1080 的游戏画面来设计 UI 布局、比例和安全区域”
- 实际请求给生图接口的尺寸，仍会按内部比例档位映射，例如 `1536x1024`

兼容旧用法时也支持 `--size`，但它只是 `--design-size` 的别名，后续应优先使用 `--design-size`。

## 后端选择规则

按下面顺序选择生成方式：

1. **如果 skill 目录下存在可用 `.env`，且其中可提供 `OPENAI_BASE_URL` 和 `OPENAI_API_KEY`**
   - 走 `scripts/generate_images.py`
   - 使用 `.env` / 进程环境变量中的配置调用 `gpt-image-2`
   - 这是默认的脚本化路径，适合稳定复现、批量生成和保存 manifest

2. **如果没有可用 `.env`，或缺少 `OPENAI_BASE_URL` / `OPENAI_API_KEY`**
   - 直接使用当前运行环境自带的内置生图能力
   - 先整理出最终 prompt，再直接出图

3. **如果既没有可用 `.env`，当前环境也没有内置生图能力**
   - 再提示用户补充 `.env` 或提供 API 配置

## 工作流

### 1. 默认先出 1 张样图

除非用户明确要求批量，否则先生成 1 张，让用户确认方向。

### 2. 生成方式

#### 方式 A：有 `.env` 时，走脚本

角色素材示例：

```bash
python ".claude/skills/gpt-image-game/scripts/generate_images.py" \
  --prompt "一个科幻女战士角色立绘，蓝白能量装甲，适合手游卡面与头像裁切" \
  --game-type character \
  --design-size 1080x1920 \
  --count 1
```

UI 素材并自动切散图示例：

```bash
python ".claude/skills/gpt-image-game/scripts/generate_images.py" \
  --prompt "赛博风任务面板 UI，包含多个独立按钮、图标、标签和弹窗组件" \
  --game-type ui \
  --design-size 1920x1080 \
  --slice-mode chroma-key-components \
  --count 1
```

如果 prompt 很长，用 heredoc：

```bash
python ".claude/skills/gpt-image-game/scripts/generate_images.py" \
  --prompt "$(cat <<'EOF'
<完整 prompt>
EOF
)" \
  --game-type ui \
  --design-size 1920x1080 \
  --slice-mode chroma-key-components \
  --count 1
```

#### 方式 B：没有 `.env` 时，走内置生图

- 先整理出最终 prompt
- 直接使用当前环境自带的 image generation / image tool 出图
- 同样默认先生成 1 张，不要一开始就批量生成

### 3. 结果回报

如果走脚本，默认输出到：

```text
outputs/<timestamp>/
```

其中可能包含：
- `image-01.png`, `image-02.png`, ...
- `slices/<image-name>/sprite-01.png`, `sprite-02.png`, ...
- `manifest.json`

`manifest.json` 会记录：
- 设计尺寸
- 真实生成尺寸档位
- 背景模式
- 切图模式与色键参数
- 每张原图路径
- 每个切片的 box、尺寸与输出路径

## 切图规则

生成工作流默认使用 `chroma-key-components`：

### 默认：`chroma-key-components`

含义：
- 先生成绿底图
- 根据绿底颜色做色键抠图
- 把绿底转成透明 alpha
- 对半透明边缘默认做去绿边处理
- 把前景的按钮、图标、面板等独立元素切成透明散图 PNG

适合：
- UI 按钮
- 图标
- 标签
- 面板块
- 明显分开的 UI 组件

使用要求：
- 背景尽量纯绿
- 元素之间尽量不要粘连
- 前景不要大面积使用接近绿底的颜色
- 如边缘仍有轻微绿边，可调 `--despill-strength`

### 高级调参（通常不用改）

只有在切片效果不理想时，再按需调整这些参数：

- `--key-color`：更换绿底色值，默认 `#00FF00`
- `--key-threshold`：控制多大范围被视为背景
- `--edge-softness`：控制透明边缘的过渡宽度
- `--despill-strength`：控制去绿边强度，默认 `1.2`
- `--slice-min-width` / `--slice-min-height` / `--slice-min-area`：过滤太小的碎片
- `--slice-padding`：给切出来的散图额外留边

### 兼容：`alpha-components`

仅保留给独立切图脚本处理已有透明 PNG；生成工作流不再走这条路径。

## 限制说明

- 默认生成策略就是绿底，不再走透明生图
- 如果前景自身含大量接近绿底的颜色，可能被误抠或被去绿边处理削弱
- 如果背景不是足够纯的绿底，切图效果会下降
- 透明散图来自绿底抠图结果，不是模型直接返回 alpha
- 这不是通用海报/KV/社媒技能

## 环境要求

- **有可用 `.env`，且包含 `OPENAI_BASE_URL` 与 `OPENAI_API_KEY`**：
  - 走脚本路径
  - 可额外读取：
    - `GPT_IMAGE_MODEL_NAME`（默认 `gpt-image-2`）
    - `GPT_IMAGE_QUALITY`（默认 `high`）
    - `GPT_IMAGE_ENDPOINT`（默认 `auto`）

- **依赖**：
  - `requests`
  - `python-dotenv`
  - `Pillow`

脚本只从 skill 自己目录附近的受限 `.env` 位置读取，不会向上递归扫描项目目录。

## 禁止事项

- 不要把它当成通用海报/KV/社媒技能来用
- 不要在用户没确认方向时直接批量生很多张
- 不要承诺所有 UI 图都能自动切出理想散图；元素粘连或颜色太接近绿底时仍需重新生成或人工调整 prompt
