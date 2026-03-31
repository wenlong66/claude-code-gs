---
name: retrospective
description: "通过分析已完成的工作、速度、阻碍者和模式生成冲刺或里程碑回顾。为下一次迭代生成可操作的见解。"
argument-hint: "[sprint-N|milestone-name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
context: |
  !git log --oneline --since="2 weeks ago" 2>/dev/null
---

当此技能被调用时：

1. **读取参数** 以确定这是冲刺回顾（`sprint-N`）还是里程碑回顾（`milestone-name`）。

2. **从适当的位置读取冲刺或里程碑计划**：
   - 冲刺计划：`production/sprints/`
   - 里程碑定义：`production/milestones/`

   提取：计划的任务、估计工作量、负责人和目标。

3. **读取冲刺或里程碑所涵盖时期的 git log** 以了解实际提交了什么以及何时提交。

4. **通过将计划与实际交付物进行比较来扫描已完成和未完成的任务**。检查：
   - 按计划完成的任务
   - 完成但有修改的任务
   - 结转的任务（未完成）
   - 冲刺中途添加的任务（计划外工作）
   - 已删除或缩小范围的任务

5. **扫描 TODO/FIXME 趋势**：
   - 统计当前 TODO/FIXME/HACK 注释
   - 如果有，与上一个冲刺计数进行比较（检查上一个回顾）
   - 注意技术债务是在增长还是减少

6. **读取之前的回顾**（如果有）从 `production/sprints/` 或 `production/milestones/` 以检查：
   - 之前的行动项目是否已处理？
   - 相同的问题是否重复出现？
   - 速度趋势如何？

7. **生成回顾**：

```markdown
## 回顾：[冲刺 N / 里程碑名称]
时期：[开始日期] -- [结束日期]
生成日期：[日期]

### 指标

| 指标 | 计划 | 实际 | 差异 |
|--------|---------|--------|-------|
| 任务 | [X] | [Y] | [+/- Z] |
| 完成率 | -- | [Z%] | -- |
| 故事点/工作天数 | [X] | [Y] | [+/- Z] |
| 发现缺陷 | -- | [N] | -- |
| 修复缺陷 | -- | [N] | -- |
```
