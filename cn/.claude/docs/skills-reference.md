# 可用技能（斜杠命令）

68 个斜杠命令，按阶段组织。输入 Claude Code 中的 `/` 即可访问。

## 入门与导航

| 命令 | 用途 |
|---------|---------|
| `/start` | 首次入门 -- 询问你当前所处阶段，然后引导你到正确的工作流程 |
| `/help` | 上下文感知的“下一步做什么？”-- 读取当前阶段并给出所需下一步 |
| `/project-stage-detect` | 完整项目审计 -- 检测阶段、识别存在性缺口、推荐下一步 |
| `/setup-engine` | 配置引擎 + 版本，检测知识缺口，填充版本感知参考文档 |
| `/adopt` | 旧项目格式审计 -- 检查现有 GDD/ADR/故事的内部结构，生成迁移计划 |

## 游戏设计

| 命令 | 用途 |
|---------|---------|
| `/brainstorm` | 使用专业工作室方法进行引导式构思（MDA、SDT、Bartle、动词优先） |
| `/map-systems` | 将游戏概念拆分为系统，映射依赖关系，优先排序设计顺序 |
| `/design-system` | 针对单个游戏系统进行引导式、分节 GDD 编写 |
| `/quick-design` | 适用于小改动的轻量设计规范 -- 调数、微调、小幅新增 |
| `/review-all-gdds` | 跨 GDD 的一致性与整体性审查 |
| `/propagate-design-change` | 当 GDD 变更时，查找受影响的 ADR 并生成影响报告 |

## UX 与界面设计

| 命令 | 用途 |
|---------|---------|
| `/ux-design` | 引导式分节 UX 规格编写（界面/流程、HUD 或模式库） |
| `/ux-review` | 验证 UX 规格是否符合 GDD、可访问性和模式规范 |

## 架构

| 命令 | 用途 |
|---------|---------|
| `/create-architecture` | 主架构文档的引导式编写 |
| `/architecture-decision` | 创建架构决策记录（ADR） |
| `/architecture-review` | 验证所有 ADR 的完整性、依赖顺序和 GDD 覆盖 |
| `/create-control-manifest` | 根据已接受的 ADR 生成扁平程序员规则表 |

## 故事与冲刺

| 命令 | 用途 |
|---------|---------|
| `/create-epics` | 将 GDD + ADR 转换为 epics -- 每个架构模块一个 |
| `/create-stories` | 将单个 epic 拆分成可实施的 story 文件 |
| `/dev-story` | 读取 story 并实现 -- 路由到正确的程序员智能体 |
| `/sprint-plan` | 生成或更新冲刺计划；初始化 sprint-status.yaml |
| `/sprint-status` | 快速 30 行冲刺快照（读取 sprint-status.yaml） |
| `/story-readiness` | 在拾取前验证 story 是否可实施（READY/NEEDS WORK/BLOCKED） |
| `/story-done` | 实现后的 8 阶段完成审查；更新 story 文件并给出下一条 story |
| `/estimate` | 结构化工作量评估，包含复杂性、依赖和风险分解 |

## 评审与分析

| 命令 | 用途 |
|---------|---------|
| `/design-review` | 审查游戏设计文档的完整性和一致性 |
| `/code-review` | 对文件或变更集进行架构代码审查 |
| `/balance-check` | 分析游戏平衡数据、公式和配置 -- 标记异常 |
| `/asset-audit` | 审计资源的命名约定、文件大小预算和管线合规性 |
| `/content-audit` | 审计 GDD 规定的内容数量与已实现内容的差距 |
| `/scope-check` | 分析功能或冲刺范围与原始计划的偏差，标记范围蔓延 |
| `/perf-profile` | 结构化性能分析与瓶颈识别 |
| `/tech-debt` | 扫描、跟踪、优先级排序并报告技术债务 |
| `/gate-check` | 验证跨开发阶段推进的就绪性（PASS/CONCERNS/FAIL） |
| `/consistency-check` | 扫描所有 GDD 与实体注册表，检测跨文档不一致（数值、名称、规则冲突） |

## QA 与测试

| 命令 | 用途 |
|---------|---------|
| `/qa-plan` | 为冲刺或功能生成 QA 测试计划 |
| `/smoke-check` | 在 QA 移交前运行关键路径冒烟测试门禁 |
| `/soak-test` | 为长时间游玩会话生成浸泡测试流程 |
| `/regression-suite` | 将测试覆盖映射到 GDD 关键路径，识别已有缺陷但缺少回归测试的项目 |
| `/test-setup` | 为项目引擎搭建测试框架和 CI/CD 管线 |
| `/test-helpers` | 为测试套件生成引擎专属测试辅助库 |
| `/test-evidence-review` | 对测试文件和手动证据文档进行质量审查 |
| `/test-flakiness` | 从 CI 运行日志中检测非确定性（易波动）测试 |
| `/skill-test` | 验证技能文件的结构合规性与行为正确性 |

## 生产管理

| 命令 | 用途 |
|---------|---------|
| `/milestone-review` | 审查里程碑进度并生成状态报告 |
| `/retrospective` | 运行结构化冲刺或里程碑回顾 |
| `/bug-report` | 创建结构化缺陷报告 |
| `/bug-triage` | 读取所有开放缺陷，重新评估优先级与严重性，分配负责人和标签 |
| `/reverse-document` | 从现有实现生成设计或架构文档 |
| `/playtest-report` | 生成结构化游玩测试报告或分析现有测试笔记 |

## 发布

| 命令 | 用途 |
|---------|---------|
| `/release-checklist` | 生成并验证当前构建的预发布清单 |
| `/launch-checklist` | 对所有部门进行完整发布就绪验证 |
| `/changelog` | 从 git 提交和冲刺数据自动生成变更日志 |
| `/patch-notes` | 从 git 历史和内部数据生成面向玩家的补丁说明 |
| `/hotfix` | 紧急修复流程，带审计跟踪，绕过正常冲刺流程 |

## 创意与内容

| 命令 | 用途 |
|---------|---------|
| `/prototype` | 快速搭建一次性原型以验证机制（标准较宽松，隔离工作树） |
| `/onboard` | 为新贡献者或智能体生成上下文化入门文档 |
| `/localize` | 本地化流程：字符串提取、验证、翻译准备 |

## 团队编排

在单一功能区域中协调多个智能体：

| 命令 | 协调对象 |
|---------|-------------|
| `/team-combat` | game-designer + gameplay-programmer + ai-programmer + technical-artist + sound-designer + qa-tester |
| `/team-narrative` | narrative-director + writer + world-builder + level-designer |
| `/team-ui` | ux-designer + ui-programmer + art-director + accessibility-specialist |
| `/team-release` | release-manager + qa-lead + devops-engineer + producer |
| `/team-polish` | performance-analyst + technical-artist + sound-designer + qa-tester |
| `/team-audio` | audio-director + sound-designer + technical-artist + gameplay-programmer |
| `/team-level` | level-designer + narrative-director + world-builder + art-director + systems-designer + qa-tester |
| `/team-live-ops` | live-ops-designer + economy-designer + community-manager + analytics-engineer |
| `/team-qa` | qa-lead + qa-tester + gameplay-programmer + producer |