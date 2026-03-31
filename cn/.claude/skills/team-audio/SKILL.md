---
name: team-audio
description: "协调音频团队：audio-director + sound-designer + technical-artist + gameplay-programmer 完成从方向到实现的完整音频管线。"
argument-hint: "[feature or area to design audio for]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---

当此技能被调用时，通过结构化管线协调音频团队。

**决策点：** 在每个步骤转换时，使用 `AskUserQuestion` 向用户呈现子智能体的提议作为可选选项。在对话中写满智能体的完整分析，然后用简洁的标签捕获决策。在进入下一步之前，用户必须批准。

1. **读取参数** 获取目标功能或区域（例如 `combat`、`main menu`、`forest biome`、`boss encounter`）。

2. **收集上下文**：
   - 阅读 `design/gdd/` 中该功能的相关设计文档
   - 如果存在，阅读 `design/gdd/sound-bible.md` 中的声音圣经
   - 阅读 `assets/audio/` 中的现有音频资源列表
   - 阅读该区域的任何现有声音设计文档

## 如何委托

使用 Task 工具将每个团队成员作为子智能体生成：
- `subagent_type: audio-director` — 声音身份、情感基调、音频调色板
- `subagent_type: sound-designer` — SFX 规格、音频事件、混音组
- `subagent_type: technical-artist` — 音频中间件、总线结构、内存预算
- `subagent_type: gameplay-programmer` — 音频管理器、游戏玩法触发器、适应性音乐

始终在每个智能体的提示中提供完整上下文（功能描述、现有音频资源、设计文档引用）。

3. **按顺序协调音频团队**：

### 步骤 1：音频方向（audio-director）
生成 `audio-director` 智能体以：
- 定义此功能/区域的声音身份
- 指定情感基调和音频调色板
- 设置音乐方向（适应性层、分离音轨、过渡）
- 定义音频优先级和混音目标
- 建立任何适应性音频规则（战斗强度、探索、紧张）

### 步骤 2：声音设计（sound-designer）
生成 `sound-designer` 智能体以：
- 为每个音频事件创建详细的 SFX 规格
- 定义声音类别（环境音、UI、游戏玩法、音乐、对话）
- 指定每个声音的参数（音量范围、音高变化、衰减）
- 规划带触发条件的音频事件列表
- 定义混音组和闪避规则

### 步骤 3：技术实现（technical-artist）
生成 `technical-artist` 智能体以：
- 设计音频中间件集成（Wwise/FMOD/native）
- 定义音频总线结构和路由
- 指定每个平台的音频资源内存预算
- 规划流式传输与预加载资源策略
- 设计任何音频响应视觉效果
