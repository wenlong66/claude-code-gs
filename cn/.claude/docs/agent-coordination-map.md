# 智能体协调与委托图

## 组织层级

```
                           [人类开发者]
                                 |
                 +---------------+---------------+
                 |               |               |
         creative-director  technical-director  producer
                 |               |               |
        +--------+--------+     |        (协调全部)
        |        |        |     |
  game-designer art-dir  narr-dir  lead-programmer  qa-lead  audio-dir
        |        |        |         |                |        |
     +--+--+     |     +--+--+  +--+--+--+--+--+   |        |
     |  |  |     |     |     |  |  |  |  |  |  |   |        |
    sys lvl eco  ta   wrt  wrld gp ep  ai net tl ui qa-t    snd
                                 |
                             +---+---+
                             |       |
                          perf-a   devops   analytics

  额外负责人（向 producer/directors 汇报）：
    release-manager         -- 发布管线、版本控制、部署
    localization-lead       -- i18n、字符串表、翻译管线
    prototyper              -- 快速可丢弃原型、概念验证
    security-engineer       -- 反作弊、利用、数据隐私、网络安全
    accessibility-specialist -- WCAG、色盲、重映射、文本缩放
    live-ops-designer       -- 赛季、活动、战斗通行证、留存、实时经济
    community-manager       -- 补丁说明、玩家反馈、危机沟通

  引擎专家（使用与你的引擎匹配的集合）：
    unreal-specialist  -- UE5 负责人：Blueprint/C++、GAS 概述、UE 子系统
      ue-gas-specialist         -- GAS：能力、效果、属性、标签、预测
      ue-blueprint-specialist   -- Blueprint：BP/C++ 边界、图表标准、优化
      ue-replication-specialist -- 网络：复制、RPC、预测、带宽
      ue-umg-specialist         -- UI：UMG、CommonUI、小部件层次、数据绑定

    unity-specialist   -- Unity 负责人：MonoBehaviour/DOTS、Addressables、URP/HDRP
      unity-dots-specialist         -- DOTS/ECS：Jobs、Burst、混合渲染器
      unity-shader-specialist       -- 着色器：Shader Graph、VFX Graph、SRP 定制
      unity-addressables-specialist -- 资源：异步加载、捆绑、内存、CDN
      unity-ui-specialist           -- UI：UI Toolkit、UGUI、UXML/USS、数据绑定

    godot-specialist   -- Godot 4 负责人：GDScript、节点/场景、信号、资源
      godot-gdscript-specialist    -- GDScript：静态类型、模式、信号、性能
      godot-shader-specialist      -- 着色器：Godot 着色语言、可视化着色器、VFX
      godot-gdextension-specialist -- 原生：C++/Rust 绑定、GDExtension、构建系统
```

### 图例
```
sys  = systems-designer       gp  = gameplay-programmer
lvl  = level-designer         ep  = engine-programmer
eco  = economy-designer       ai  = ai-programmer
ta   = technical-artist       net = network-programmer
wrt  = writer                 tl  = tools-programmer
wrld = world-builder          ui  = ui-programmer
snd  = sound-designer         qa-t = qa-tester
narr-dir = narrative-director perf-a = performance-analyst
art-dir = art-director
```

## 委托规则

### 谁可以委托给谁

| 从 | 可以委托给 |
|------|----------------|
| creative-director | game-designer、art-director、audio-director、narrative-director |
| technical-director | lead-programmer、devops-engineer、performance-analyst、technical-artist（技术决策） |
| producer | 任何智能体（仅限其领域内的任务分配） |
| game-designer | systems-designer、level-designer、economy-designer |
| lead-programmer | gameplay-programmer、engine-programmer、ai-programmer、network-programmer、tools-programmer、ui-programmer |
| art-director | technical-artist、ux-designer |
| audio-director | sound-designer |
| narrative-director | writer、world-builder |
| qa-lead | qa-tester |
| release-manager | devops-engineer（发布构建）、qa-lead（发布测试） |
| localization-lead | writer（字符串审查）、ui-programmer（文本适配） |
| prototyper | （独立工作，将发现报告给 producer 和相关负责人） |
| security-engineer | network-programmer（安全审查）、lead-programmer（安全模式） |
| accessibility-specialist | ux-designer（无障碍模式）、ui-programmer（实现）、qa-tester（无障碍测试） |
| [engine]-specialist | 引擎子专业人员 |
| [engine] 子专业人员 | （就引擎子系统模式和优化向所有程序员提供建议） |
| live-ops-designer | economy-designer（实时经济）、community-manager（活动沟通）、analytics-engineer（参与度指标） |
| community-manager | （与 producer 协作批准，并与 release-manager 确认补丁说明时机） |

### 升级路径

| 情况 | 升级到 |
|-----------|------------|
| 两位设计师对某个机制意见不一致 | game-designer |
| 游戏设计与叙事冲突 | creative-director |
| 游戏设计与技术可行性冲突 | producer（协调），然后 creative-director + technical-director |
| 美术与音频在基调上冲突 | creative-director |
| 代码架构争议 | technical-director |
| 跨系统代码冲突 | lead-programmer，然后 technical-director |
| 跨部门排期冲突 | producer |
| 范围超出容量 | producer，然后 creative-director 决定削减 |
| 质量门禁争议 | qa-lead，然后 technical-director |
| 性能预算违规 | performance-analyst 提示，technical-director 决定 |

## 常见工作流模式

### 模式 1：新功能（完整流程）

```
1. creative-director  -- 批准与愿景一致的功能概念
2. game-designer      -- 创建包含完整规格的设计文档
3. producer           -- 安排工作并识别依赖
4. lead-programmer    -- 设计代码架构，创建接口草图
5. [specialist-programmer] -- 实现功能
6. technical-artist   -- 实现视觉效果（如需要）
7. writer             -- 创建文字内容（如需要）
8. sound-designer     -- 创建音频事件列表（如需要）
9. qa-tester          -- 编写测试用例
10. qa-lead           -- 审查并批准测试覆盖
11. lead-programmer   -- 代码审查
12. qa-tester         -- 执行测试
13. producer          -- 标记任务完成
```

### 模式 2：Bug 修复

```
1. qa-tester          -- 使用 /bug-report 提交缺陷报告
2. qa-lead            -- 分类严重性和优先级
3. producer           -- 分配到 sprint（若不是 S1）
4. lead-programmer    -- 识别根因，分配给程序员
5. [specialist-programmer] -- 修复 bug
6. lead-programmer    -- 代码审查
7. qa-tester          -- 验证修复并运行回归
8. qa-lead            -- 关闭 bug
```

### 模式 3：平衡调整

```
1. analytics-engineer -- 从数据（或玩家反馈）识别失衡
2. game-designer      -- 依据设计意图评估问题
3. economy-designer   -- 建模调整
4. game-designer      -- 批准新数值
5. [数据文件更新]     -- 修改配置值
6. qa-tester          -- 回归测试受影响系统
7. analytics-engineer -- 监控变更后的指标
```

### 模式 4：新区域/关卡

```
1. narrative-director -- 定义该区域的叙事目的与节拍
2. world-builder      -- 创建 lore 与环境背景
3. level-designer     -- 设计布局、遭遇、节奏
4. game-designer      -- 审查遭遇的机制设计
5. art-director       -- 定义该区域的视觉方向
6. audio-director     -- 定义该区域的音频方向
7. [由相关程序员和美术实现]
8. writer             -- 创建区域专属文字内容
9. qa-tester          -- 测试完整区域
```

### 模式 5：Sprint 周期

```
1. producer           -- 使用 /sprint-plan new 制定 sprint
2. [所有智能体]       -- 执行分配的任务
3. producer           -- 使用 /sprint-plan status 进行每日状态更新
4. qa-lead            -- 在 sprint 期间持续测试
5. lead-programmer    -- 在 sprint 期间持续进行代码审查
6. producer           -- 通过 post-sprint hook 进行回顾
7. producer           -- 基于经验教训规划下一个 sprint
```

### 模式 6：里程碑检查点

```
1. producer           -- 运行 /milestone-review
2. creative-director  -- 审查创意进展
3. technical-director -- 审查技术健康状况
4. qa-lead            -- 审查质量指标
5. producer           -- 协调 go/no-go 讨论
6. [所有总监]        -- 如有需要，同意范围调整
7. producer           -- 记录决定并更新计划
```

### 模式 7：发布管线

```text
1. producer             -- 宣布发布候选版本，确认里程碑标准已满足
2. release-manager      -- 切发布分支，生成 /release-checklist
3. qa-lead              -- 运行完整回归，并对质量签字
4. localization-lead    -- 验证所有字符串已翻译，文本适配通过
5. performance-analyst  -- 确认性能基准满足目标
6. devops-engineer      -- 构建发布产物，运行部署管线
7. release-manager      -- 生成 /changelog，打标签并创建发布说明
8. technical-director   -- 重大版本最终签字
9. release-manager      -- 部署并监控 48 小时
10. producer            -- 标记发布完成
```

### 模式 8：快速原型

```text
1. game-designer        -- 定义假设和成功标准
2. prototyper           -- 使用 /prototype 搭建原型
3. prototyper           -- 用最小实现构建（按小时而不是按天）
4. game-designer        -- 根据标准评估原型
5. prototyper           -- 记录发现报告
6. creative-director    -- 决定是否进入生产
7. producer             -- 如获批准则安排生产工作
```

### 模式 9：实时活动 / 赛季发布

```text
1. live-ops-designer     -- 设计活动/赛季内容、奖励、时间表
2. game-designer         -- 验证该活动的玩法机制
3. economy-designer      -- 平衡活动经济与奖励数值
4. narrative-director    -- 提供赛季叙事主题
5. writer                -- 创建活动说明和 lore
6. producer              -- 安排实现工作
7. [由相关程序员实现]
8. qa-lead               -- 端到端测试活动流程
9. community-manager     -- 起草活动公告和补丁说明
10. release-manager      -- 发布活动内容
11. analytics-engineer   -- 监控活动参与度与指标
12. live-ops-designer    -- 活动后分析与经验总结
```

## 跨域沟通协议

### 设计变更通知

当设计文档发生变化时，game-designer 必须通知：
- lead-programmer（实现影响）
- qa-lead（需要更新测试计划）
- producer（评估排期影响）
- 根据变更影响到的相关专业智能体

### 架构变更通知

当创建或修改 ADR 时，technical-director 必须通知：
- lead-programmer（需要代码变更）
- 所有受影响的专业程序员
- qa-lead（测试策略可能变化）
- producer（排期影响）

### 资源标准变更通知

当 art bible 或资源标准发生变化时，art-director 必须通知：
- technical-artist（管线变化）
- 使用受影响资源的所有内容创作者
- devops-engineer（如果构建管线受影响）

## 需要避免的反模式

1. **绕过层级**：专业智能体绝不应在未咨询负责人的情况下做出超出其职责的决策。
2. **跨域实现**：未经相关所有者明确委托，智能体绝不应修改其指定区域之外的文件。
3. **影子决策**：所有决策都必须记录。没有书面记录的口头约定会导致冲突。
4. **单体任务**：分配给智能体的每个任务都应能在 1-3 天内完成。如果更大，必须先拆分。
5. **假设驱动实现**：如果规范有歧义，实现者必须先询问编写者，而不是猜测。错误猜测的代价比提问更高。