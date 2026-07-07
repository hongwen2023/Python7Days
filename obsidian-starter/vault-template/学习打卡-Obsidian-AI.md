---
created: 2026-07-07
tags:
  - 学习计划
status: 进行中
---

# Obsidian × Claude 学习打卡

> 路线图详见仓库 `resources/obsidian-ai-learning-path.md`。达标一项勾一项，全勾完再进下一阶段。

## 阶段 0 · 地基（目标：2 小时内完成）

- [ ] 理解 `[[wikilink]]`、frontmatter、「库=文件夹」三个概念
- [ ] 官方 obsidian-skills 已装进库的 `.claude/skills/`（setup.sh 已代劳）
- [ ] 在库目录跑 `claude`，完成三个试手指令（总结笔记 / 补 frontmatter / 找相关笔记）
- [ ] ✅ 验收：让 Claude 链接两篇笔记，它用的是 `[[wikilink]]` 而非普通链接

## 阶段 1 · Inbox 零摩擦捕获（目标：连续 7 天）

- [ ] 第 1 天：往 00_Inbox 扔 3 条以上想法/摘录，跑一次 `/inbox`
- [ ] 第 2 天打卡 ／ - [ ] 第 3 天 ／ - [ ] 第 4 天 ／ - [ ] 第 5 天 ／ - [ ] 第 6 天 ／ - [ ] 第 7 天
- [ ] 根据自己的纠正情况，微调 `.claude/commands/inbox.md` 里的分诊规则至少一次
- [ ] pdf2obsidian 的输出目录已指向 `30_资源/PDF解读`
- [ ] ✅ 验收：连续 7 天捕获零思考，Inbox 每天清零，归档位置基本不用手动纠正

## 阶段 2 · 自动双链（解锁条件：阶段 1 验收通过）

- [ ] 精读 Kyle Gao 博客 + claude-obsidian 的 wiki-lint skill
- [ ] 写出 `/link` 命令（自动建实体笔记 + 双链）
- [ ] ✅ 验收：任一旧笔记 3 跳内可达 5 篇相关笔记（看 Graph View）

## 阶段 3 · 定时自动化

- [ ] pdf2obsidian 挂上 cron
- [ ] 每周日自动生成周回顾
- [ ] 每晚自动修断链 + git 备份
- [ ] ✅ 验收：连续两周零手动操作，周一自动有上周回顾

## 阶段 4 · 语义检索

- [ ] 装 Smart Connections，验证「语义相关」面板质量
- [ ] 配 MCP server，在 Claude Desktop 问库三个跨笔记问题
- [ ] ✅ 验收：「我记得在哪看过」时第一反应是问库

## 阶段 5 · 选修（按需勾选方向）

- [ ] 笔记→博客初稿 ／ - [ ] Zotero 文献流 ／ - [ ] claudian 嵌入面板 ／ - [ ] 决策日志 ／ - [ ] 自写 skills
