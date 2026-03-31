# Unity 6.3 LTS — 破坏性变更

**最后验证：** 2026-02-13

本文档跟踪 Unity 2022 LTS（可能在模型训练中）和 Unity 6.3 LTS（当前版本）之间的破坏性 API 变更和行为差异。按风险级别组织。

## 高风险 — 将破坏现有代码

### Entities/DOTS API 完全大修
**版本：** Entities 1.0+（Unity 6.0+）

```csharp
// ❌ 旧的（Unity 6 之前，GameObjectEntity 模式）
public class HealthComponent : ComponentData {
    public float Value;
}

// ✅ 新的（Unity 6+，IComponentData）
public struct HealthComponent : IComponentData {
    public float Value;
}

// ❌ 旧的：ComponentSystem
public class DamageSystem : ComponentSystem { }

// ✅ 新的：ISystem（非托管，Burst 兼容）
public partial struct DamageSystem : ISystem {
    public void OnCreate(ref SystemState state) { }
    public void OnUpdate(ref SystemState state) { }
}
```

**迁移：** 遵循 Unity 的 ECS 迁移指南。需要重大的架构变更。

---

### 输入系统 — 旧输入已弃用
**版本：** Unity 6.0+

```csharp
// ❌ 旧的：Input 类（已弃用）
if (Input.GetKeyDown(KeyCode.Space)) { }

// ✅ 新的：输入系统包
using UnityEngine.InputSystem;
if (Keyboard.current.spaceKey.wasPressedThisFrame) { }
```

**迁移：** 安装输入系统包，用新 API 替换所有 `Input.*` 调用。

---

### URP/HDRP 渲染器功能 API 变更
**版本：** Unity 6.0+

```csharp
// ❌ 旧的：ScriptableRenderPass.Execute 签名
public override void Execute(ScriptableRenderContext context, ref RenderingData data)
