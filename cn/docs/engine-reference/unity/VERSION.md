# Unity 引擎 — 版本参考

| 字段 | 值 |
|-------|-------|
| **引擎版本** | Unity 6.3 LTS |
| **发布日期** | 2025 年 12 月 |
| **项目固定** | 2026-02-13 |
| **最后验证文档** | 2026-02-13 |
| **LLM 知识截止** | 2025 年 5 月 |

## 知识差距警告

LLM 的训练数据可能覆盖 Unity 直至约 2022 LTS（2022.3）。整个 Unity 6 发布系列（以前的 Unity 2023 Tech Stream）引入了模型不知道的重大变更。在建议 Unity API 调用之前务必交叉参考此目录。

## 截止后版本时间线

| 版本 | 发布 | 风险级别 | 关键主题 |
|---------|---------|------------|-----------|
| 6.0 | 2024 年 10 月 | 高 | Unity 6 品牌重塑、新渲染功能、Entities 1.3、DOTS 改进 |
| 6.1 | 2024 年 11 月 | 中等 | 缺陷修复、稳定性改进 |
| 6.2 | 2024 年 12 月 | 中等 | 性能优化、新输入系统改进 |
| 6.3 LTS | 2025 年 12 月 | 高 | 首个 LTS，自 6.0 起，生产就绪的 DOTS、增强的图形功能 |

## 自 2022 LTS 到 Unity 6.3 LTS 的主要变更

### 破坏性变更
- **Entities/DOTS**：Entities 1.0+ 中的重大 API 大修，ECS 模式完全重新设计
- **输入系统**：旧输入管理器弃用，新输入系统为默认
- **渲染**：URP/HDRP 重大升级，SRP Batcher 改进
- **Addressables**：资产管理 workflow 变更
- **脚本**：C# 9 支持、新 API 模式

### 新功能（截止后）
- **DOTS**：生产就绪的实体组件系统（Entities 1.3+）
- **图形**：增强的 URP/HDRP 管线、GPU Resident Drawer
- **多人游戏**：Netcode for GameObjects 改进
- **UI Toolkit**：运行时 UI 生产就绪（新项目推荐替换 UGUI）
- **异步资源加载**：改进的 Addressables 性能
- **Web**：WebGPU 支持

### 弃用系统
- **旧输入管理器**：使用新输入系统包
- **旧粒子系统**：使用 Visual Effect Graph
- **UGUI**：仍支持，但新项目推荐 UI Toolkit
- **旧 ECS (GameObjectEntity)**：被现代 DOTS/Entities 取代

## 验证来源

- 官方文档：https://docs.unity3d.com/6000.0/Documentation/Manual/index.html
- Unity 6 发布：https://unity.com/releases/unity-6
- Unity 6.3 LTS 公告：https://unity.com/blog/unity-6-3-lts-is-now-available
- 迁移指南：https://docs.unity3d.com/6000.0/Documentation/Manual/upgrade-guides.html
- Unity 6 支持：https://unity.com/releases/unity-6/support
- C# API 参考：https://docs.unity3d.com/6000.0/Documentation/ScriptReference/index.html
