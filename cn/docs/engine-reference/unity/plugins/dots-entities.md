# Unity 6.3 — DOTS / Entities (ECS)

**最后验证：** 2026-02-13
**状态：** 生产就绪（Entities 1.3+，Unity 6.3 LTS）
**包：** `com.unity.entities`（包管理器）

---

## 概述

**DOTS（数据导向技术堆栈）** 是 Unity 的高性能 ECS（实体组件系统）框架。专为大规模游戏设计（1000-10000 个实体）。

**使用 DOTS 用于：**
- RTS 游戏（1000 个单位）
- 模拟（人群、交通、物理）
- 程序内容生成
- 性能关键系统

**不要使用 DOTS 用于：**
- 小游戏（开销不值得）
- 需要频繁结构变更的游戏
- 大量使用 UnityEngine API（MonoBehaviour 更容易）

**⚠️ 知识差距：** Entities 1.0+（Unity 6）是从 0.x 完全重写。许多 Entities 0.x 教程现已过时。

---

## 安装

### 通过包管理器安装

1. `窗口 > 包管理器`
2. Unity 注册表 > 搜索 "Entities"
3. 安装：
   - `Entities`（ECS 核心）
   - `Burst`（LLVM 编译器）
   - `Jobs`（自动安装）
   - `Mathematics`（SIMD 数学）

---

## 核心概念

### 1. **实体**
- 轻量级 ID（int）
- 无行为，只是一个标识符

### 2. **组件**
- 仅数据（无方法）
- 实现 `IComponentData` 的结构体

### 3. **系统**
- 对组件进行操作的逻辑
- 实现 `ISystem` 的结构体

### 4. **原型**
- 组件类型的唯一组合
- 具有相同组件的实体共享原型
