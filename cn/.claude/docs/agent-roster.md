# 智能体名册

以下智能体可用。每个都在 `.claude/agents/` 中有专门的定义文件。使用最适合当前任务的智能体。当任务跨越多个领域时，协调智能体（通常是 `producer` 或领域负责人）应委托给专业人员。

## 层级 1 -- 领导智能体（Opus）
| 智能体 | 领域 | 何时使用 |
|-------|--------|-------------|
| `creative-director` | 高层愿景 | 主要创意决策、支柱冲突、基调/方向 |
| `technical-director` | 技术愿景 | 架构决策、技术栈选择、性能策略 |
| `producer` | 生产管理 | 冲刺计划、里程碑跟踪、风险管理、协调 |

## 层级 2 -- 部门负责人智能体（Sonnet）
| 智能体 | 领域 | 何时使用 |
|-------|--------|-------------|
| `game-designer` | 游戏设计 | 机制、系统、进度、经济、平衡 |
| `lead-programmer` | 代码架构 | 系统设计、代码审查、API 设计、重构 |
| `art-director` | 视觉方向 | 风格指南、艺术圣经、资源标准、UI/UX 方向 |
| `audio-director` | 音频方向 | 音乐方向、音效调色板、音频实现策略 |
| `narrative-director` | 故事和写作 | 故事弧线、世界构建、角色设计、对话策略 |
| `qa-lead` | 质量保证 | 测试策略、缺陷分类、发布就绪、回归规划 |
| `release-manager` | 发布管线 | 构建管理、版本控制、变更日志、部署、回滚 |
| `localization-lead` | 国际化 | 字符串外部化、翻译管线、区域测试 |

## 层级 3 -- 专业智能体（Sonnet 或 Haiku）
| 智能体 | 领域 | 模型 | 何时使用 |
|-------|--------|-------|-------------|
| `systems-designer` | 系统设计 | Sonnet | 特定机制实现、公式设计、循环 |
| `level-designer` | 关卡设计 | Sonnet | 关卡布局、节奏、遭遇设计、流程 |
| `economy-designer` | 经济/平衡 | Sonnet | 资源经济、战利品表、进度曲线 |
| `gameplay-programmer` | 游戏玩法代码 | Sonnet | 功能实现、游戏系统代码 |
| `engine-programmer` | 引擎系统 | Sonnet | 核心引擎、渲染、物理、内存管理 |
| `ai-programmer` | AI 系统 | Sonnet | 行为树、寻路、NPC 逻辑、状态机 |
| `network-programmer` | 网络 | Sonnet | 网络代码、复制、延迟补偿、配对 |
| `tools-programmer` | 开发工具 | Sonnet | 编辑器扩展、管线工具、调试实用程序 |
| `ui-programmer` | UI 实现 | Sonnet | UI 框架、屏幕、小部件、数据绑定 |
| `technical-artist` | 技术美术 | Sonnet | 着色器、VFX、优化、艺术管线工具 |
| `sound-designer` | 音效设计 | Haiku | SFX 设计文档、音频事件列表、混音笔记 |
| `writer` | 对话/lore | Sonnet | 对话写作、lore 条目、物品描述 |
| `world-builder` | 世界/lore 设计 | Sonnet | 世界规则、派系设计、历史、地理 |
| `qa-tester` | 测试执行 | Haiku | 编写测试用例、缺陷报告、测试清单 |
| `performance-analyst` | 性能 | Sonnet | 分析、优化建议、内存分析 |
| `devops-engineer` | 构建/部署 | Haiku | CI/CD、构建脚本、版本控制工作流程 |
| `analytics-engineer` | 遥测 | Sonnet | 事件跟踪、仪表板、A/B 测试设计 |
| `ux-designer` | UX 流程 | Sonnet | 用户流程、线框图、可访问性、输入处理 |
| `prototyper` | 快速原型 | Sonnet | 可丢弃原型、机制测试、可行性验证 |
| `security-engineer` | 安全 | Sonnet | 反作弊、利用预防、存档加密、网络安全 |
| `accessibility-specialist` | 可访问性 | Haiku | WCAG 合规、色盲模式、按键重映射、文本缩放 |
| `live-ops-designer` | 实时运营 | Sonnet | 赛季、活动、战斗通行证、留存、实时经济 |
| `community-manager` | 社区 | Haiku | 补丁说明、玩家反馈、危机沟通、社区健康 |

## 引擎特定智能体（使用与你的引擎匹配的配置）

### 引擎负责人

| 智能体 | 引擎 | 模型 | 何时使用 |
| ---- | ---- | ---- | ---- |
| `unreal-specialist` | Unreal Engine 5 | Sonnet | Blueprint vs C++、GAS 概述、UE 子系统、Unreal 优化 |
| `unity-specialist` | Unity | Sonnet | MonoBehaviour vs DOTS、Addressables、URP/HDRP、Unity 优化 |
| `godot-specialist` | Godot 4 | Sonnet | GDScript 模式、节点/场景架构、信号、Godot 优化 |

### Unreal Engine 子专业人员

| 智能体 | 子系统 | 模型 | 何时使用 |
| ---- | ---- | ---- | ---- |
| `ue-gas-specialist` | Gameplay Ability System | Sonnet | 能力、游戏效果、属性集、标签、预测 |
| `ue-blueprint-specialist` | Blueprint 架构 | Sonnet | BP/C++ 边界、图表标准、命名、BP 优化 |
| `ue-replication-specialist` | 网络/复制 | Sonnet | 属性复制、RPC、预测、相关性、带宽 |
| `ue-umg-specialist` | UMG/CommonUI | Sonnet | 小部件层次结构、数据绑定、CommonUI 输入、UI 性能 |

### Unity 子专业人员

| 智能体 | 子系统 | 模型 | 何时使用 |
| ---- | ---- | ---- | ---- |
| `unity-dots-specialist` | DOTS/ECS | Sonnet | 实体组件系统、Jobs、Burst 编译器、混合渲染器 |
| `unity-shader-specialist` | 着色器/VFX | Sonnet | Shader Graph、VFX Graph、SRP 定制、后处理 |
| `unity-addressables-specialist` | 资产管理 | Sonnet | Addressable 组、异步加载、捆绑包、内存、CDN |
| `unity-ui-specialist` | UI Toolkit/UGUI | Sonnet | UI Toolkit、UGUI Canvas、UXML/USS、数据绑定、跨平台输入 |
