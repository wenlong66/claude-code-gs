# 设置要求

此模板需要安装一些工具以获得完整功能。所有钩子在工具缺失时都会优雅地失败——不会破坏任何东西，但你将失去验证功能。

## 必需

| 工具 | 用途 | 安装 |
| ---- | ---- | ---- |
| **Git** | 版本控制、分支管理 | [git-scm.com](https://git-scm.com/) |
| **Claude Code** | AI 智能体 CLI | `npm install -g @anthropic-ai/claude-code` |

## 推荐

| 工具 | 使用者 | 用途 | 安装 |
| ---- | ---- | ---- | ---- |
| **jq** | 钩子（4/8） | 在 commit/push/asset/agent 钩子中进行 JSON 解析 | 见下文 |
| **Python 3** | 钩子（2/8） | 数据文件的 JSON 验证 | [python.org](https://www.python.org/) |
| **Bash** | 所有钩子 | Shell 脚本执行 | Git for Windows 包含 |

### 安装 jq

**Windows**（任选其一）：
```
winget install jqlang.jq
choco install jq
scoop install jq
```

**macOS**：
```
brew install jq
```

**Linux**：
```
sudo apt install jq     # Debian/Ubuntu
sudo dnf install jq     # Fedora
sudo pacman -S jq       # Arch
```

## 平台说明

### Windows
- Git for Windows 包含 **Git Bash**，它提供了所有钩子在 `settings.json` 中使用的 `bash` 命令
- 确保 Git Bash 在你的 PATH 上（如果通过 Git 安装程序安装则是默认设置）
- 钩子使用 `bash .claude/hooks/[name].sh` —— 这在 Windows 上有效，因为 Claude Code 通过可以找到 `bash.exe` 的 shell 调用命令

### macOS / Linux
- Bash 原生可用
- 通过你的包管理器安装 `jq` 以获得完整的钩子支持

## 验证你的设置

运行这些命令检查前提条件：

```bash
git --version          # 应该显示 git 版本
bash --version         # 应该显示 bash 版本
jq --version           # 应该显示 jq 版本（可选）
python3 --version      # 应该显示 python 版本（可选）
```

## 没有可选工具会发生什么

| 缺失工具 | 影响 |
| ---- | ---- |
| **jq** | Commit 验证、推送保护、资源验证和智能体审计钩子静默跳过其检查。提交和推送仍然有效。 |
| **Python 3** | 跳过 commit 和资源钩子中的 JSON 数据文件验证。无效 JSON 可以在没有警告的情况下提交。 |
| **两者都有** | 所有钩子仍然执行而不出错（exit 0），但不提供验证。你在没有任何安全网的情况下飞行。 |

## 推荐 IDE

Claude Code 可与任何编辑器配合使用，但模板针对以下进行了优化：
- **VS Code** 搭配 Claude Code 扩展
- **Cursor**（Claude Code 兼容）
- 基于终端的 Claude Code CLI