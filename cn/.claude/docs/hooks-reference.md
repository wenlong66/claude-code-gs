# 活动钩子

钩子配置在 `.claude/settings.json` 中并自动触发：

| 钩子 | 事件 | 触发条件 | 动作 |
| ---- | ----- | ------- | ------ |
| `validate-commit.sh` | PreToolUse (Bash) | `git commit` 命令 | 验证设计文档章节、JSON 数据文件、硬编码值、TODO 格式 |
| `validate-push.sh` | PreToolUse (Bash) | `git push` 命令 | 对推送到受保护分支（develop/main）发出警告 |
| `validate-assets.sh` | PostToolUse (Write/Edit) | 资源文件变更 | 检查 `assets/` 中文件的命名约定和 JSON 有效性 |
| `session-start.sh` | SessionStart | 会话开始 | 加载冲刺上下文、里程碑、git 活动；检测并预览活动会话状态文件以便恢复 |
| `detect-gaps.sh` | SessionStart | 会话开始 | 检测新项目（建议 /start）以及代码/原型存在时缺少文档的情况，建议 /reverse-document 或 /project-stage-detect |
| `pre-compact.sh` | PreCompact | 上下文压缩前 | 在压缩前将会话状态（active.md、修改的文件、WIP 设计文档）输出到对话中，以便压缩后仍能恢复 |
| `post-compact.sh` | PostCompact | 压缩后 | 提醒 Claude 从 `active.md` 检查点恢复会话状态 |
| `notify.sh` | Notification | 通知事件 | 通过 PowerShell 显示 Windows Toast 通知 |
| `session-stop.sh` | Stop | 会话结束 | 总结已完成内容并更新会话日志 |
| `log-agent.sh` | SubagentStart | 智能体启动 | 审计轨迹开始 -- 记录子智能体调用与时间戳 |
| `log-agent-stop.sh` | SubagentStop | 智能体停止 | 审计轨迹结束 -- 完成子智能体记录 |
| `validate-skill-change.sh` | PostToolUse (Write/Edit) | 技能文件变更 | 建议在任何 `.claude/skills/` 文件被写入或编辑后运行 `/skill-test` |

钩子参考文档：`.claude/docs/hooks-reference/`
钩子输入模式文档：`.claude/docs/hooks-reference/hook-input-schemas.md`