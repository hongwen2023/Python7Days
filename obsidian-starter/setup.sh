#!/usr/bin/env bash
# Obsidian × Claude 阶段 0+1 一键安装脚本
# 用法：bash setup.sh /path/to/你的Obsidian库
# 作用：1) 建标准文件夹结构  2) 安装官方 obsidian-skills  3) 安装 /inbox 命令和学习打卡笔记
# 幂等：重复运行安全，绝不覆盖你已有的文件。

set -euo pipefail

VAULT="${1:-}"
if [[ -z "$VAULT" ]]; then
  echo "用法：bash setup.sh /path/to/你的Obsidian库"
  exit 1
fi
mkdir -p "$VAULT"
VAULT="$(cd "$VAULT" && pwd)"
TEMPLATE="$(cd "$(dirname "$0")/vault-template" && pwd)"

echo "==> 目标库：$VAULT"

# 1. 文件夹结构
for dir in 00_Inbox 10_项目 20_领域 30_资源/PDF解读 40_归档; do
  mkdir -p "$VAULT/$dir"
done
echo "==> 文件夹结构 OK（00_Inbox / 10_项目 / 20_领域 / 30_资源/PDF解读 / 40_归档）"

# 2. 模板文件（已存在则跳过，不覆盖）
copy_if_absent() {
  local src="$1" dst="$2"
  [[ -e "$dst" ]] || cp "$src" "$dst"
}
mkdir -p "$VAULT/.claude/commands"
copy_if_absent "$TEMPLATE/.claude/commands/inbox.md" "$VAULT/.claude/commands/inbox.md"
copy_if_absent "$TEMPLATE/00_Inbox/README.md" "$VAULT/00_Inbox/README.md"
copy_if_absent "$TEMPLATE/学习打卡-Obsidian-AI.md" "$VAULT/学习打卡-Obsidian-AI.md"
echo "==> /inbox 命令 + 学习打卡笔记 OK"

# 3. 官方 obsidian-skills（Obsidian CEO 出品）
if [[ -d "$VAULT/.claude/skills/obsidian-markdown" ]]; then
  echo "==> 官方 skills 已存在，跳过"
else
  TMP="$(mktemp -d)"
  git clone --depth 1 https://github.com/kepano/obsidian-skills.git "$TMP/obsidian-skills"
  mkdir -p "$VAULT/.claude/skills"
  for skill in "$TMP/obsidian-skills/skills"/*/; do
    name="$(basename "$skill")"
    [[ -d "$VAULT/.claude/skills/$name" ]] || cp -r "$skill" "$VAULT/.claude/skills/$name"
  done
  rm -rf "$TMP"
  echo "==> 官方 obsidian-skills 安装 OK"
fi

echo
echo "全部完成 ✅  下一步："
echo "  1. cd \"$VAULT\" && claude"
echo "  2. 试三个指令：「总结我最近的笔记」「给某篇笔记补 frontmatter」「找相关笔记」"
echo "  3. 往 00_Inbox 扔几条想法，然后输入 /inbox"
echo "  4. 打开库里的「学习打卡-Obsidian-AI.md」开始勾第一项"
