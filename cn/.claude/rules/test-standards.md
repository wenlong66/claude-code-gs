---
paths:
  - "tests/**"
---

# 测试标准

- 测试命名：`test_[system]_[scenario]_[expected_result]` 模式
- 每个测试必须有清晰的 arrange/act/assert 结构
- 单元测试不得依赖外部状态（文件系统、网络、数据库）
- 集成测试必须自我清理
- 性能测试必须指定可接受的阈值，超出则失败
- 测试数据必须在测试中或专用夹具中定义，永远不要共享可变状态
- 模拟外部依赖——测试应该快速且确定性
- 每个缺陷修复必须有回归测试，该测试本可以捕获原始缺陷

## 示例

**正确**（正确的命名 + Arrange/Act/Assert）：

```gdscript
func test_health_system_take_damage_reduces_health() -> void:
    # Arrange
    var health := HealthComponent.new()
    health.max_health = 100
    health.current_health = 100

    # Act
    health.take_damage(25)

    # Assert
    assert_eq(health.current_health, 75)
```

**错误**：

```gdscript
func test1() -> void:  # 违规：没有描述性名称
    var h := HealthComponent.new()
    h.take_damage(25)  # 违规：没有 arrange 步骤，没有清晰的 assert
    assert_true(h.current_health < 100)  # 违规：不精确的断言
```
