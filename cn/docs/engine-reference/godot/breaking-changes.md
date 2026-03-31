# Godot — 破坏性变更

最后验证：2026-02-12

Godot 版本之间的变更，专注于模型训练数据截止后（4.4+）的变更。

## 4.5 → 4.6（2026 年 1 月 — 截止后，高风险）

| 子系统 | 变更 | 详情 |
|-----------|---------|---------|
| 物理 | Jolt 现在是默认的 3D 物理引擎 | 新项目自动使用 Jolt。现有项目保持其设置。一些 HingeJoint3D 属性（如 `damp`）仅适用于 GodotPhysics。 |
| 渲染 | Glow 在 tone mapping **之前**处理 | 原先在之后。具有 glow 的场景看起来会不同。在 WorldEnvironment 中调整 intensity/blend。 |
| 渲染 | Windows 上 D3D12 默认 | 原先是 Vulkan。为了更好的驱动兼容性。 |
| 渲染 | AgX tonemapper 新增控制 | 添加了白点和对比度参数。 |
| 核心 | Quaternion 初始化为单位元 | 原先是零。不太可能影响大多数代码，但技术上是破坏性的。 |
| UI | 双焦点系统 | 鼠标/触摸焦点现在与键盘/游戏手柄焦点分离。不同输入方式的视觉反馈不同。 |
| 动画 | IK 系统完全恢复 | 通过 SkeletonModifier3D 节点实现 CCDIK、FABRIK、Jacobian IK、Spline IK、TwoBoneIK。 |
| 编辑器 | 新的"现代"主题默认 | 灰度替换蓝色调。恢复：编辑器设置 → 界面 → 主题 → 风格：经典 |
| 编辑器 | "选择模式"快捷键变更 | 新的"选择模式"（v 键）防止意外变换。旧模式改名为"变换模式"（q 键）。 |
| 2D | TileMapLayer 场景瓦片旋转 | 场景瓦片现在可以像图集瓦片一样旋转。 |
| 本地化 | CSV 复数形式支持 | 不再需要 Gettext 进行复数。添加了上下文列。 |
| C# | 自动字符串提取 | 翻译字符串从 C# 代码自动提取。 |
| 插件 | 新的 EditorDock 类 | 带布局控制的插件停靠栏专用容器。 |

## 4.4 → 4.5（2025 年晚期 — 截止后，高风险）

| 子系统 | 变更 | 详情 |
|-----------|---------|---------|
| GDScript | 添加了可变参数 | 函数可以接受 `...` 任意参数 — 新语言特性 |
| GDScript | `@abstract` 装饰器 | 抽象类和方法现在可强制执行 |
| GDScript | 脚本回溯 | 即使在 Release 构建中也可用的详细调用栈 |
| 渲染 | 模板缓冲区支持 | 高级视觉效果的新能力 |
| 渲染 | SMAA 1x 抗锯齿 | 新的后处理 AA 选项 |
| 渲染 | Shader Baker | 预编译着色器 — 据报道某些演示启动速度提高 20 倍 |
| 渲染 | 弯曲法线贴图、镜面反射遮蔽 | 新材质特性 |
| 可访问性 | 屏幕阅读器支持 | Control 节点可通过 AccessKit 与可访问性工具配合使用 |
| 编辑器 | 实时翻译预览 | 在编辑器中测试不同语言的 GUI 布局 |
| 物理 | 3D 插值重构 | 从 RenderingServer 移至 SceneTree。API 未变但内部不同。 |
| 动画 | BoneConstraint3D | 新增：AimModifier3D、CopyTransformModifier3D、ConvertTransformModifier3D |
| 资源 | 添加了 `duplicate_deep()` | 用于嵌套资源深度复制的新显式方法 |
| 导航 | 专用的 2D 导航服务器 | 不再是 3D 导航的代理；2D 游戏导出更小 |
| UI | FoldableContainer 节点 | 用于可折叠 UI 部分的新手风琴风格容器 |
| UI | 递归 Control 行为 | 在整个节点层次结构中禁用鼠标/焦点交互 |
| 平台 | visionOS 导出支持 | 新平台目标 |
| 平台 | SDL3 游戏手柄驱动 | 将游戏手柄处理委托给 SDL 库 |
| 平台 | Android 16KB 页面支持 | Google Play 目标 Android 15+ 所需 |

## 4.3 → 4.4（2025 年中期 — 接近截止，验证）

| 子系统 | 变更 | 详情 |
