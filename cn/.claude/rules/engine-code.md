---
paths:
  - "src/core/**"
---

# 引擎代码规则

- 热路径中零分配（更新循环、渲染、物理）——预分配、池化、重用
- 所有引擎 API 必须线程安全，或明确文档化为单线程专用
- 每次优化前后都要分析——记录测量的数字
- 引擎代码绝对不能依赖游戏玩法代码（严格的依赖方向：引擎 <- 游戏玩法）
- 每个公共 API 必须在其文档注释中包含使用示例
- 更改公共接口需要弃用期和迁移指南
- 对所有资源使用 RAII / 确定性清理
- 所有引擎系统必须支持优雅降级
- 编写引擎 API 代码之前，请查阅 `docs/engine-reference/` 了解当前引擎版本并根据参考文档验证 API

## 示例

**正确**（热路径零分配）：

```gdscript
# 预分配的数组每帧重用
var _nearby_cache: Array[Node3D] = []

func _physics_process(delta: float) -> void:
    _nearby_cache.clear()  # 重用，不要重新分配
    _spatial_grid.query_radius(position, radius, _nearby_cache)
```

**错误**（热路径中分配）：

```gdscript
func _physics_process(delta: float) -> void:
    var nearby: Array[Node3D] = []  # 违规：每帧分配
    nearby = get_tree().get_nodes_in_group("enemies")  # 违规：每帧树查询
```
