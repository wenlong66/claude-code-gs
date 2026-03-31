---
paths:
  - "src/gameplay/**"
---

# 游戏玩法代码规则

- 所有游戏玩法值必须来自外部配置/数据文件，永远不要硬编码
- 所有时间相关计算使用增量时间（帧率独立性）
- 禁止直接引用 UI 代码——使用事件/信号进行跨系统通信
- 每个游戏玩法系统必须实现清晰的接口
- 状态机必须具有带文档化状态的明确转换表
- 为所有游戏玩法逻辑编写单元测试——将逻辑与表现分离
- 在代码注释中记录每个功能实现的设计文档
- 禁止使用静态单例管理游戏状态——使用依赖注入

## 示例

**正确**（数据驱动）：

```gdscript
var damage: float = config.get_value("combat", "base_damage", 10.0)
var speed: float = stats_resource.movement_speed * delta
```

**错误**（硬编码）：

```gdscript
var damage: float = 25.0   # 违规：硬编码的游戏玩法值
var speed: float = 5.0      # 违规：不是来自配置，没有使用 delta
```
