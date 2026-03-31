# 引擎参考文档

此目录包含该项目所用游戏引擎的精选、版本固定的文档快照。这些文件存在是因为 **LLM 知识有截止日期**，而游戏引擎频繁更新。

## 为什么这存在

Claude 的训练数据有知识截止日期（目前是 2025 年 5 月）。像 Godot、Unity 和 Unreal 这样的游戏引擎发布的更新会引入破坏性 API 变更、新功能和新弃用模式。如果没有这些参考文件，智能体会建议过时的代码。

## 结构

每个引擎都有自己的目录：

```
<engine>/
├── VERSION.md              # 固定版本、验证日期、知识差距窗口
├── breaking-changes.md     # 版本之间的 API 变更，按风险级别组织
├── deprecated-apis.md      # "不要用 X → 用 Y" 查找表
├── current-best-practices.md  # 模型训练数据中没有的新实践
└── modules/                # 每个子系统快速参考（每个最多约 150 行）
    ├── rendering.md
    ├── physics.md
    └── ...
```

## 智能体如何使用这些文件

引擎专家智能体被指示：

1. 读取 `VERSION.md` 确认当前引擎版本
2. 在建议任何引擎 API 之前检查 `deprecated-apis.md`
3. 查阅 `breaking-changes.md` 了解特定版本问题
4. 读取相关的 `modules/*.md` 了解子系统特定工作

## 维护

### 何时更新

- 升级引擎版本后
- LLM 模型更新时（新的知识截止日期）
- 运行 `/refresh-docs` 后（如果有）
- 当你发现模型错误的 API 时

### 如何更新

1. 用新引擎版本和日期更新 `VERSION.md`
2. 为版本过渡在 `breaking-changes.md` 添加新条目
3. 将新弃用的 API 移入 `deprecated-apis.md`
4. 用新模式更新 `current-best-practices.md`
5. 用 API 变更更新相关的 `modules/*.md`
6. 在所有修改的文件上设置"最后验证"日期

### 质量规则

- 每个文件必须有"最后验证：YYYY-MM-DD"日期
- 保持模块文件在 150 行以内（上下文预算）
- 包含显示正确/错误模式的代码示例
- 链接到官方文档 URL 以便验证
- 只记录与模型训练数据不同的内容
