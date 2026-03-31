# Unreal Engine — 版本参考

| 字段 | 值 |
|-------|-------|
| **引擎版本** | Unreal Engine 5.7 |
| **发布日期** | 2025 年 11 月 |
| **项目固定** | 2026-02-13 |
| **最后验证文档** | 2026-02-13 |
| **LLM 知识截止** | 2025 年 5 月 |

## 知识差距警告

LLM 的训练数据可能覆盖 Unreal Engine 直至约 5.3。版本 5.4、5.5、5.6 和 5.7 引入了模型不知道的重大变更。在建议 Unreal API 调用之前务必交叉参考此目录。

## 截止后版本时间线

| 版本 | 发布 | 风险级别 | 关键主题 |
|---------|---------|------------|-----------|
| 5.4 | 约 2025 年中期 | 高 | Motion Design 工具、动画改进、PCG 增强 |
| 5.5 | 约 2025 年 9 月 | 高 | Megalights（数百万灯光）、动画创作、MegaCity 演示 |
| 5.6 | 约 2025 年 10 月 | 中等 | 性能优化、缺陷修复 |
| 5.7 | 2025 年 11 月 | 高 | PCG 生产就绪、Substrate 生产就绪、AI 助手 |

## 自 UE 5.3 到 UE 5.7 的主要变更

### 破坏性变更
- **Substrate 材质系统**：新材质框架（替换旧材质）
- **PCG（程序内容生成）**：生产就绪，重大 API 变更
- **Megalights**：新照明系统（数百万动态灯光）
- **动画创作**：新绑 定和动画工具
- **AI 助手**：编辑器内 AI 指导（实验性）

### 新功能（截止后）
- **Megalights**：大规模动态照明（数百万灯光）
- **Substrate Materials**：生产就绪的模块化材质系统
- **PCG Framework**：程序世界生成（5.7+ 生产就绪）
- **增强的虚拟制作**：MetaHuman 集成、更深的 VP workflow
- **动画改进**：更好的绑定、混合、程序动画
- **AI 助手**：编辑器内 AI 帮助（实验性）

### 弃用系统
- **旧材质系统**：新项目迁移到 Substrate
- **旧 PCG API**：使用新的生产就绪 PCG API（5.7+）

## 验证来源

- 官方文档：https://docs.unrealengine.com/5.7/
- UE 5.7 发布说明：https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-7-release-notes
- 5.7 新功能：https://dev.epicgames.com/documentation/en-us/unreal-engine/whats-new
- UE 5.7 公告：https://www.unrealengine.com/en-US/news/unreal-engine-5-7-is-now-available
- UE 5.5 博客：https://www.unrealengine.com/en-US/blog/unreal-engine-5-5-is-now-available
- 迁移指南：https://docs.unrealengine.com/5.7/en-US/upgrading-projects/
