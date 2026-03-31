---
name: team-polish
description: "协调打磨团队：协调 performance-analyst、technical-artist、sound-designer 和 qa-tester 优化、打磨和强化功能或领域以达到发布质量。"
argument-hint: "[feature or area to polish]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---
当此技能被调用时，通过结构化管线协调打磨团队。

**决策点：** 在每个阶段转换时，使用 `AskUserQuestion` 向用户呈现子智能体的提议作为可选选项。在对话中写满智能体的完整分析，然后用简洁的标签捕获决策。在进入下一阶段之前，用户必须批准。

## 团队组成
- **performance-analyst** — 分析、优化、内存分析、帧预算
- **technical-artist** — VFX 打磨、着色器优化、视觉质量
- **sound-designer** — 音频打磨、混音、环境音层、反馈声音
- **qa-tester** — 边缘情况测试、回归测试、浸泡测试

## 如何委托

使用 Task 工具将每个团队成员作为子智能体生成：
- `subagent_type: performance-analyst` — 分析、优化、内存分析
- `subagent_type: technical-artist` — VFX 打磨、着色器优化、视觉质量
- `subagent_type: sound-designer` — 音频打磨、混音、环境音层
- `subagent_type: qa-tester` — 边缘情况测试、回归测试、浸泡测试

始终在每个智能体的提示中提供完整上下文（目标功能/领域、性能预算、已知问题）。在管线允许的地方并行启动独立智能体（例如，阶段 3 和 4 可以同时运行）。

## 管线

### 阶段 1：评估
委托给 **performance-analyst**：
- 使用 `/perf-profile` 分析目标功能/领域
- 识别性能瓶颈和帧预算违规
- 测量内存使用并检查泄漏
- 根据目标硬件规格进行基准测试
- 输出：带优先优化列表的性能报告

### 阶段 2：优化
委托给 **performance-analyst**（根据需要使用相关程序员）：
- 修复阶段 1 识别的性能热点
- 优化绘制调用，减少过度绘制
- 修复内存泄漏并减少分配压力
- 验证优化不会改变游戏玩法行为
- 输出：优化代码与前后指标

### 阶段 3：视觉打磨（与阶段 2 并行）
委托给 **technical-artist**：
- 根据艺术圣经审查 VFX 质量和一致性
- 优化粒子系统和着色器效果
- 在适当的地方添加屏幕震动、相机效果和视觉 juice
- 确保效果在较低设置下优雅降级
- 输出：打磨的视觉效果

### 阶段 4：音频打磨（与阶段 2 并行）
委托给 **sound-designer**：
- 审查音频事件的完整性（是否有任何动作缺少声音反馈？）
- 检查音频混音电平——相对于混音没有太大或太小
- 添加环境音层以营造氛围
- 验证音频在空间定位中正确播放
- 输出：音频打磨列表和混音备注

### 阶段 5：强化
委托给 **qa-tester**：
- 测试所有边缘情况：边界条件、快速输入、不寻常序列
- 浸泡测试：长时间运行功能检查退化
- 压力测试：最大实体、最坏情况场景
- 回归测试：验证打磨变更没有破坏现有功能
- 在最低规格硬件上测试（如果有）
- 输出：测试结果与任何剩余问题

### 阶段 6：签字
- 收集所有团队成员的结果
- 将性能指标与预算进行比较
- 报告：发布就绪 / 需要更多工作
- 列出任何剩余问题及其严重性和建议

## 输出
