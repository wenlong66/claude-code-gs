---
name: skill-improve
description: "使用 test-fix-retest 循环改进一个 skill。运行静态检查，提出有针对性的修复，重写 skill，重新测试，并根据分数变化保留或回滚。"
argument-hint: "[skill-name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash
---

# Skill Improve

对单个 skill 运行改进循环：
test → fix → retest → keep or revert.

---

## 第 1 阶段：解析参数

从第一个参数读取 skill 名称。如果缺失，输出用法并停止：

```
Usage: /skill-improve [skill-name]
Example: /skill-improve tech-debt
```

验证 `.claude/skills/[name]/SKILL.md` 是否存在。如果不存在，停止并输出：
"Skill '[name]' not found."

---

## 第 2 阶段：基线测试

运行 `/skill-test static [name]` 并记录基线分数：
- FAIL 的数量
- WARN 的数量
- 具体失败的是哪些检查（Check 1–7）

向用户展示：
```
Static baseline:   [N] failures, [M] warnings
Failing: Check 4 (no ask-before-write), Check 5 (no handoff)
```

如果基线是 0 FAIL、0 WARN，就记录这一点并继续到 Phase 2b。

### 第 2b 阶段：分类基线

在 `CCGS Skill Testing Framework/catalog.yaml` 中查找 skill 的 `category:` 字段。

如果没有找到 `category:` 字段，显示：
"Category: not yet assigned — skipping category checks."
然后跳到 Phase 3。

如果找到了 category，运行 `/skill-test category [name]` 并记录分类基线：
- FAIL 的数量
- WARN 的数量
- 具体哪些 category rubric 指标失败

向用户展示：
```
Category baseline: [N] failures, [M] warnings  ([category] rubric)
```

如果 static 和 category 两个基线都为 0 FAIL、0 WARN，则停止：
"This skill already passes all static and category checks. No improvements needed."

---

## 第 3 阶段：诊断

完整读取 `.claude/skills/[name]/SKILL.md`。

对于每个失败或警告的 **static** 检查，找出精确缺口：

- **Check 1 fail** → 缺少哪个 frontmatter 字段
- **Check 2 fail** → 找到了多少个 phase vs. 最少要求
- **Check 3 fail** → skill 正文里完全没有 verdict 关键词
- **Check 4 fail** → allowed-tools 里有 Write 或 Edit，但没有先询问后写入语言
- **Check 5 warn** → 末尾没有跟进或下一步章节
- **Check 6 warn** → 设置了 `context: fork`，但找到的 phase 少于 5 个
- **Check 7 warn** → argument-hint 为空，或与文档中的模式不匹配

对于每个失败或警告的 **category** 检查（如果在 Phase 2b 中分配了 category），找出 skill 文本中的精确缺口。例如：
- 如果 G2 失败（gate mode，未 spawn 全部 directors）：skill 正文从未提到所有 4 个 PHASE-GATE director prompts
- 如果 A2 失败（authoring，没有每段前先 May-I-write）：skill 在最后才统一询问，而不是在每次 section 写入前
- 如果 T3 失败（team，没有上报 BLOCKED）：skill 在 agent 阻塞时没有停止后续工作

在提出任何改动前，先把完整诊断展示给用户。

---

## 第 4 阶段：提出修复

针对每个失败和警告写出定点修复。以清晰标记的 before/after 块展示拟议变更。只改失败的部分——不要重写通过的章节。

询问："May I write this improved version to `.claude/skills/[name]/SKILL.md`?"

如果用户拒绝，停止于此。

---

## 第 5 阶段：写入并重测

记录 skill 文件的当前内容（以便需要回滚）。

把改进后的 skill 写回 `.claude/skills/[name]/SKILL.md`。

重新运行 `/skill-test static [name]` 并记录新的 static 分数。
如果分配了 category，也重新运行 `/skill-test category [name]` 并记录新的分类分数。

展示对比：
```
Static:   Before [N] failures, [M] warnings  →  After [N'] failures, [M'] warnings
Category: Before [N] failures, [M] warnings  →  After [N'] failures, [M'] warnings  (if applicable)
Combined change: improved / no change / worse
```

---

## 第 6 阶段：裁定

计算 combined failure total：static FAILs + category FAILs + static WARNs + category WARNs。

**如果 combined score 有改善（combined failure count 比基线更低）：**
报告："Score improved. Changes kept."
展示每个维度修复了什么的摘要。

**如果 combined score 相同或更差：**
报告："Combined score did not improve."
展示改了什么，以及为什么可能没有帮助。
询问："May I revert `.claude/skills/[name]/SKILL.md` using git checkout?"
如果同意：运行 `git checkout -- .claude/skills/[name]/SKILL.md`

---

## 第 7 阶段：下一步

- 运行 `/skill-test static all`，找出下一个有失败的 skill。
- 运行 `/skill-improve [next-name]`，在另一个 skill 上继续这个循环。
- 运行 `/skill-test audit`，查看整体覆盖率进展。
