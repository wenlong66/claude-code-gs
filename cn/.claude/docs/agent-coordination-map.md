# 智能体协调和委托地图

## 组织层级

```
                           [人类开发者]
                                 |
                 +---------------+---------------+
                 |               |               |
         creative-director  technical-director  producer
                 |               |               |
        +--------+--------+     |        (coordinates all)
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

  引擎专家（使用与你的引擎匹配的配置）：
    unreal-specialist  -- UE5 负责人：Blueprint/C++、GAS 概述、UE 子系统
      ue-gas-specialist         -- GAS：能力、效果、属性、标签、预测
      ue-blueprint-specialist   -- Blueprint：BP/C++ 边界、图表标准、优化
      ue-replication-specialist -- 网络：复制、RPC、预测、带宽
      ue-umg-specialist         -- UI：UMG、CommonUI、小部件层次结构、数据绑定

    unity-specialist   -- Unity 负责人：MonoBehaviour/DOTS、Addressables、URP/HDRP
      unity-dots-specialist         -- DOTS/ECS：Jobs、Burst、混合渲染器
      unity-shader-specialist       -- 着色器：Shader Graph、VFX Graph、SRP 定制
      unity-addressables-specialist -- 资源：异步加载、捆绑包、内存、CDN
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
| technical-director | lead-programmer、devops-engineer、performance-analyst、technical-artist（技术决策）|
| producer | 任何智能体（仅在其领域内的任务分配）|
| game-designer | systems-designer、level-designer、economy-designer |
| lead-programmer | gameplay-programmer、engine-programmer、ai-programmer、network-programmer、tools-programmer、ui-programmer |
| art-director | technical-artist、ux-designer |
| audio-director | sound-designer |
| narrative-director | writer、world-builder |
| qa-lead | qa-tester |
| release-manager | devops-engineer（发布构建）、qa-lead（发布测试）|
