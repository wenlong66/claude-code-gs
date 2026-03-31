# Godot — 当前最佳实践

最后验证：2026-02-12 | 引擎：Godot 4.6

自模型训练数据（~4.3）以来**新或变更**的实践。这补充（不替换）智能体的内置知识。

## GDScript (4.5+)

- **可变参数**：函数可以接受任意数量的参数
  ```gdscript
  func log_values(prefix: String, values: Variant...) -> void:
      for v in values:
          print(prefix, ": ", v)
  ```

- **抽象类和方法**：使用 `@abstract` 强制继承
  ```gdscript
  @abstract
  class_name BaseEnemy extends CharacterBody3D

  @abstract
  func get_attack_pattern() -> Array[Attack]:
      pass  # 子类必须覆盖
  ```

- **脚本回溯**：即使在 Release 构建中也可用的详细调用栈

## 物理 (4.6)

- **Jolt Physics 是新项目的默认 3D 引擎**
  - 比 GodotPhysics3D 更好的确定性和稳定性
  - 一些 HingeJoint3D 属性（`damp`）仅适用于 GodotPhysics
  - 切换：项目设置 → 物理 → 3D → 物理引擎
  - 2D 物理不变（仍然是 Godot Physics 2D）

## 渲染 (4.6)

- **D3D12 是 Windows 上的默认后端**（原为 Vulkan）— 为了更好的驱动兼容性
- **Glow 现在在 tone mapping 之前处理**，screen 混合模式 — 现有 glow 设置看起来可能不同
- **SSR 大修** — 真实感、稳定性和性能的重大改进
- **AgX tonemapper** — 新的白点和对比度控制

## 渲染 (4.5)

- **Shader Baker**：预编译着色器以消除启动卡顿
- **SMAA 1x**：新 AA 选项 — 比 FXAA 更锐利，比 TAA 更便宜
- **模板缓冲区**：可用于高级遮蔽/传送门效果
- **弯曲法线贴图**：法线贴图纹理中的方向遮蔽
- **镜面反射遮蔽**：环境光遮蔽现在影响反射
