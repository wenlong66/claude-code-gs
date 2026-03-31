---
paths:
  - "assets/shaders/**"
---

# 着色器代码标准

`assets/shaders/` 中的所有着色器文件必须遵循这些标准以保持视觉质量、性能和跨平台兼容性。

## 命名约定
- 文件命名：`[type]_[category]_[name].[ext]`
  - `spatial_env_water.gdshader` (Godot)
  - `SG_Env_Water` (Unity Shader Graph)
  - `M_Env_Water` (Unreal Material)
- 使用描述性名称指示材质用途
- 使用着色器类型前缀：`spatial_`、`canvas_`、`particles_`、`post_`

## 代码质量
- 所有 uniform/参数必须有描述性名称和适当的提示
- 分组相关参数（Godot：`group_uniforms`、Unity：`[Header]`、Unreal：Category）
- 注释不明显计算（特别是数学密集部分）
- 没有魔法数字——使用命名常量或文档化的 uniform 值
- 在每个着色器文件顶部包含作者和用途注释

## 性能要求
- 为每个着色器记录目标平台和复杂度预算
- 使用适当精度：在不需要全精度的地方使用 `half`/`mediump`（移动端）
- 最小化片段着色器中的纹理采样
- 避免片段着色器中的动态分支——使用 `step()`、`mix()`、`smoothstep()`
- 循环内不要纹理读取
- 模糊效果使用两遍方法（先水平后垂直）

## 跨平台
- 在最低规格目标硬件上测试着色器
- 为较低质量层级提供备用/简化版本
- 记录着色器针对的渲染管线（Forward/Deferred、URP/HDRP、Forward+/Mobile/Compatibility）
- 不要在同一目录中混合来自不同渲染管线的着色器

## 变体管理
- 最小化着色器变体——每个变体是一个单独的编译着色器
- 记录所有关键字/变体及其用途
- 尽可能使用功能剥离以减少构建大小
- 记录并监控每个着色器的总变体数量
