# Godot 渲染 — 快速参考

最后验证：2026-02-12 | 引擎：Godot 4.6

## 自 ~4.3（LLM 截止）以来的变更

### 4.6 变更
- **D3D12 是 Windows 上默认的渲染后端**（原为 Vulkan）
- **Glow 在 tone mapping 之前处理**（原为之后）— 使用 screen 混合模式
- **AgX tonemapper**：新的白点和对比度控制
- **SSR 大修**：更好的真实感、视觉稳定性和性能

### 4.5 变更
- **Shader Baker**：预编译着色器以减少启动时间
- **SMAA 1x**：新的抗锯齿选项（比 FXAA 更锐利，比 TAA 更便宜）
- **模板缓冲区支持**：启用选择性几何遮蔽/传送门效果
- **弯曲法线贴图**：编码在法线贴图纹理中的方向遮蔽
- **镜面反射遮蔽**：环境光遮蔽现在正确影响反射

### 4.4 变更
- **`RenderingDevice.draw_list_begin`**：移除许多参数；添加了可选的 `breadcrumb`
- **着色器纹理类型**：从 `Texture2D` 改为 `Texture` 基类型
- **粒子 `.restart()`**：添加了可选的 `keep_seed` 参数

### 4.3 变更（在训练数据中）
- **Compositor 节点**：`Compositor` + `CompositorEffect` 用于后处理链

## 当前 API 模式

### 后处理 (4.3+)
```gdscript
# 使用 Compositor 节点 — 而不是手动视口着色器链
# 将 Compositor 添加为 WorldEnvironment 或 Camera3D 的子节点
# 为每个后处理步骤创建 CompositorEffect 资源
```

### 抗锯齿选项 (4.6)
```
项目设置 → 渲染 → 抗锯齿：
- MSAA 2D/3D：硬件 MSAA（质量好但昂贵）
- 屏幕空间 AA：FXAA（快速、模糊）或 SMAA（锐利、中等成本）  # SMAA 4.5 新增
- TAA：时域（最佳质量，快速运动时重影）
```

### 渲染后端选择 (4.6)
```
项目设置 → 渲染 → 渲染器：
- Forward+（默认）：功能齐全，专注于桌面
- 移动端：为移动端/低端优化，功能有限
- 兼容性：OpenGL 3.3 / WebGL 2，最广泛的硬件支持

Windows 默认后端：D3D12（4.6 之前是 Vulkan）
```

## 常见错误
- 假设 Windows 上默认后端是 Vulkan（4.6 起是 D3D12）
- 使用手动视口链而不是 Compositor 进行后处理
- 在着色器统一类型中使用 `Texture2D`（4.4 起使用 `Texture`）
- 对于有许多着色器变体的项目不使用 Shader Baker
