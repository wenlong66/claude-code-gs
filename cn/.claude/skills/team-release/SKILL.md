---
name: team-release
description: "协调发布团队：协调 release-manager、qa-lead、devops-engineer 和 producer 执行从候选版本到部署的发布。"
argument-hint: "[version number or 'next']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---
当此技能被调用时，通过结构化管线协调发布团队。

**决策点：** 在每个阶段转换时，使用 `AskUserQuestion` 向用户呈现子智能体的提议作为可选选项。在对话中写满智能体的完整分析，然后用简洁的标签捕获决策。在进入下一阶段之前，用户必须批准。

## 团队组成
- **release-manager** — 发布分支、版本控制、变更日志、部署
- **qa-lead** — 测试签字、回归套件、发布质量门
- **devops-engineer** — 构建管道、产物、部署自动化
- **producer** — go/no-go 决策、利益相关者沟通、调度

## 如何委托

使用 Task 工具将每个团队成员作为子智能体生成：
- `subagent_type: release-manager` — 发布分支、版本控制、变更日志、部署
- `subagent_type: qa-lead` — 测试签字、回归套件、发布质量门
- `subagent_type: devops-engineer` — 构建管道、产物、部署自动化
- `subagent_type: producer` — go/no-go 决策、利益相关者沟通

始终在每个智能体的提示中提供完整上下文（版本号、里程碑状态、已知问题）。在管线允许的地方并行启动独立智能体（例如，阶段 3 智能体可以同时运行）。

## 管线

### 阶段 1：发布计划
委托给 **producer**：
- 确认所有里程碑验收标准已满足
- 识别从此版本推迟的任何范围项目
- 设置目标发布日期并传达给团队
- 输出：带范围确认的发布授权

### 阶段 2：发布候选
委托给 **release-manager**：
- 从约定的提交中切出发布分支
- 在所有相关文件中增加版本号
- 使用 `/release-checklist` 生成发布清单
- 冻结分支——无功能变更，仅缺陷修复
- 输出：发布分支名称和清单

### 阶段 3：质量门（并行）
并行委托：
- **qa-lead**：执行完整回归测试套件。测试所有关键路径。验证无 S1/S2 缺陷。签署质量。
- **devops-engineer**：为所有目标平台构建发布产物。验证构建是干净且可复现的。在 CI 中运行自动化测试。

### 阶段 4：本地化和性能
委托（如果有资源可与阶段 3 并行运行）：
- 验证所有字符串已翻译（如果有本地化负责人则委托）
- 根据目标运行性能基准测试（如果有性能分析师则委托）
- 输出：本地化和性能签字

### 阶段 5：Go/No-Go
委托给 **producer**：
