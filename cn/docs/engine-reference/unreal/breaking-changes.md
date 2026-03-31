# Unreal Engine 5.7 — 破坏性变更

**最后验证：** 2026-02-13

本文档跟踪 Unreal Engine 5.3（可能在模型训练中）和 Unreal Engine 5.7（当前版本）之间的破坏性 API 变更和行为差异。按风险级别组织。

## 高风险 — 将破坏现有代码

### Substrate 材质系统（5.7 生产就绪）
**版本：** UE 5.5+（实验性），5.7（生产就绪）

Substrate 用模块化、物理准确的框架替换了旧材质系统。

```cpp
// ❌ 旧的：旧材质节点（仍可用但已弃用）
// 具有 Base Color、Metallic、Roughness 等的标准材质图

// ✅ 新的：Substrate 材质层
// 使用 Substrate 节点：Substrate Slab、Substrate Blend 等
// 真正的物理准确的模块化材质创作
```

**迁移：** 在 `Project Settings > Engine > Substrate` 中启用 Substrate 并使用 Substrate 节点重建材质。

---

### PCG（程序内容生成）API 大修
**版本：** UE 5.7（生产就绪）

PCG 框架达到生产就绪状态，API 有重大变更。

```cpp
// ❌ 旧的：实验性 PCG API（5.7 之前）
// 旧的节点类型，不稳定的 API

// ✅ 新的：生产 PCG API（5.7+）
// 使用 FPCGContext、IPCGElement、新的节点类型
// 稳定的 API、生产就绪的工作流程
```

**迁移：** 遵循 5.7 文档中的 PCG 迁移指南。实验性 PCG 代码需要大量重构。

---

### Megalights 渲染系统
**版本：** UE 5.5+

新照明系统支持数百万动态灯光。

```cpp
// ❌ 旧的：有限的动态灯光（分组前向着色）
// 性能下降前最多约 100-200 个动态灯光

// ✅ 新的：Megalights（5.5+）
// 以极低的性能成本支持数百万动态灯光
// 启用：Project Settings > Engine > Rendering > Megalights
```

**迁移：** 不需要代码变更，但照明行为可能不同。启用后测试场景。
