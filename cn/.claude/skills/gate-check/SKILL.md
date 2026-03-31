---
name: gate-check
description: "验证开发阶段之间推进的就绪状态。生成 PASS/CONCERNS/FAIL 裁定以及具体的阻塞因素和所需产物。"
argument-hint: "[target-phase: systems-design | technical-setup | pre-production | production | polish | release]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write
---

# 阶段门验证

此技能验证项目是否准备好进入下一个开发阶段。它检查所需产物、质量标准和阻塞因素。

**与 `/project-stage-detect` 的区别**：该技能是诊断性的（"我们在哪里？"）。此技能是规定性的（"我们准备好推进了吗？"并带有正式裁定）。

## 生产阶段（7 个）

项目通过这些阶段进展：

1. **概念** — 构思、游戏概念文档
2. **系统设计** — 映射系统、编写 GDD
3. **技术设置** — 引擎配置、架构决策
4. **预生产** — 原型制作、垂直切片验证
5. **生产** — 功能开发（Epic/Feature/Task 跟踪活动）
6. **打磨** — 性能、游玩测试、缺陷修复
7. **发布** — 发布准备、认证

**当一个门通过时**，将新阶段名称写入 `production/stage.txt`（单行，例如 `Production`）。这会立即更新状态行。

---

## 1. 解析参数

- **带参数**：`/gate-check production` — 验证该特定阶段的就绪状态
- **无参数**：使用与 `/project-stage-detect` 相同的启发式方法自动检测当前阶段，然后验证下一个阶段转换

---

## 2. 阶段门定义

### 门：概念 → 系统设计

**所需产物：**
- [ ] `design/gdd/game-concept.md` 存在且有内容
- [ ] 游戏支柱已定义（在概念文档或 `design/gdd/game-pillars.md` 中）

**质量检查：**
- [ ] 游戏概念已审查（`/design-review` 裁定不是 MAJOR REVISION NEEDED）
- [ ] 核心循环已描述并被理解
- [ ] 已确定目标受众

---

### 门：系统设计 → 技术设置

**所需产物：**
- [ ] 系统索引存在于 `design/gdd/systems-index.md`，至少枚举了 MVP 系统
