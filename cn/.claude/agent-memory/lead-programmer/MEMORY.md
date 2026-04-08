# 首席程序员 — 代理记忆

## 技能编写约定

### Frontmatter
- 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- 以只读分析为主、并在隔离环境中运行的技能，还会带有 `context: fork` 和 `agent:`
- 交互式技能（写文件、提问）不使用 `context: fork`
- `AskUserQuestion` 是技能正文中的使用模式——它不会列在 frontmatter 的 `allowed-tools` 中（现有技能里没有这样做）

### 文件布局
- 技能位于 `.claude/skills/<name>/SKILL.md`（每个技能一个子目录，不使用扁平的 .md 文件）
- 章节标题用 `##` 表示阶段，用 `###` 表示子小节
- 阶段名称遵循“Phase N: Verb Noun”模式（例如，“Phase 1: Find the Story”）
- 输出格式模板放在 fenced code blocks 中

### 已知规范路径（在新技能中引用前先验证）
- 技术债务登记：`docs/tech-debt-register.md`（不是 `production/tech-debt.md`）
- Sprint 文件：`production/sprints/`
- Epic 故事文件：`production/epics/[epic-slug]/story-[NNN]-[slug].md`
- 控制清单：`docs/architecture/control-manifest.md`
- 会话状态：`production/session-state/active.md`
- 系统索引：`design/gdd/systems-index.md`
- 引擎参考：`docs/engine-reference/[engine]/VERSION.md`

### 已完成的技能
- `story-done` — 故事结束完成握手（Phase 1-8，写入故事文件）