# Obsidian × Claude/Codex 学习路线图（按价值量排序）

> 排序原则：**价值密度 = （日常使用频率 × 省时幅度）÷ 学习成本**。
> 越靠前的阶段，越是「投入一次、天天受益」的地基；越靠后的越是锦上添花。
> 每个阶段都有明确的「完成标志」，达标再进入下一阶段，全程约 6 周（每天 30–60 分钟）。

## 总览

| 阶段 | 主题 | 价值密度 | 时间 | 一句话收益 |
|---|---|---|---|---|
| 0 | 地基：库结构 + 官方 skills | ★★★★★ | 第 1 周前半 | 所有后续玩法的前提，10 分钟见效 |
| 1 | Inbox 零摩擦捕获 + 自动分诊 | ★★★★★ | 第 1–2 周 | 每天省 20 分钟整理时间，笔记再也不烂尾 |
| 2 | 自动双链 + 实体笔记 | ★★★★ | 第 3 周 | 笔记从「文件堆」变成「知识图谱」 |
| 3 | 定时自动化：会自己长大的库 | ★★★★ | 第 4 周 | 睡觉时 agent 帮你写周报、修断链、备份 |
| 4 | 语义检索问答：「问我的库」 | ★★★ | 第 5 周 | 「我去年怎么看 X」一句话得到答案 |
| 5 | 输出与专业场景（按需选修） | ★★ | 第 6 周起 | 笔记→博客初稿、Zotero 文献流、嵌入式面板 |

```
第0阶段 地基 ──► 第1阶段 捕获分诊 ──► 第2阶段 双链图谱 ──► 第3阶段 定时自动化 ──► 第4阶段 检索问答 ──► 第5阶段 选修
 (前提)          (最高频提效)          (质变点)             (复利开始)            (回报兑现)         (按兴趣)
```

---

## 阶段 0 · 地基：库结构 + 官方 skills（第 1 周前半，约 2 小时）

**为什么最先学**：这是唯一的「前置依赖」——不懂 wikilink/frontmatter、agent 不认识你的库，
后面所有自动化都是空中楼阁。而它恰好又是投入最小的：装一次 skills 只要 10 分钟。

**学什么**
1. Obsidian 三个核心概念（1 小时够了）：`[[wikilink]]` 双链、YAML frontmatter 属性、文件夹即库
2. 装 [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)（Obsidian CEO 官方出品）：
   把仓库内容放进你库根目录的 `.claude/`，Claude Code 立刻学会正确读写 Obsidian 格式
3. 在库目录里跑一次 `claude`，试三个指令感受一下：
   - 「总结我最近 5 篇笔记」
   - 「给这篇笔记补上合适的 frontmatter 和标签」
   - 「我的库里关于 Python 的笔记有哪些，互相有链接吗」

**辅助资料**：[博客园：Obsidian + Claude Code 实践指南](https://www.cnblogs.com/AlayaNeW/articles/19902167)（中文，跟着走一遍）

**✅ 完成标志**：在库里对 Claude 说「把这篇笔记链接到相关笔记」，它能正确使用 `[[wikilink]]` 而不是普通 Markdown 链接。

---

## 阶段 1 · Inbox 零摩擦捕获 + 自动分诊（第 1–2 周）⭐ 全路线价值最高

**为什么排第一**：所有资料公认的第一提效点。传统笔记系统失败的原因永远是
「捕获时要想放哪、打什么标签」，摩擦大到最后干脆不记。这一阶段把整理工作全部交给 agent：
**你只管往 `00_Inbox` 里扔，剩下的 AI 干**。每天受益、终身受益。

**学什么**
1. 精读 [alchaincyf/obsidian-ai-orange-book（中文橙皮书）](https://github.com/alchaincyf/obsidian-ai-orange-book)
   的「上手篇 + 实战篇」——7 个可以直接抄的工作流，重点抄 `/ingest`（整理 Inbox）
2. 学会写自定义 slash command：在库的 `.claude/commands/` 下建 `inbox.md`，
   内容是你的分诊规则（归到哪些文件夹、frontmatter 规范、标签体系）
3. 参考 [ballred/obsidian-claude-pkm](https://github.com/ballred/obsidian-claude-pkm) 的库结构设计
   （Inbox / 领域文件夹 / 归档 的划分方式）

**动手任务**
- 建 `00_Inbox` 文件夹，写一条 `/inbox` 命令：读取 Inbox 全部笔记 → 补 frontmatter →
  移到对应领域文件夹 → 报告处理了什么
- 把本仓库 `pdf2obsidian` 的输出目录也指向这套体系（解读笔记直接进对应领域文件夹）
- 连续一周：想到什么就扔 Inbox，每天跑一次 `/inbox`

**✅ 完成标志**：连续 7 天做到「捕获时零思考」，Inbox 每天清零，且归档位置基本不用手动纠正。

---

## 阶段 2 · 自动双链 + 实体笔记（第 3 周）

**为什么第二**：这是笔记系统的「质变点」——从文件堆变成知识图谱。但它依赖阶段 1 的
规范 frontmatter 和文件夹结构，所以放在后面。价值极高但使用频率略低于每日分诊。

**学什么**
1. 精读 [Kyle Gao：Using Claude Code with Obsidian](https://kyleygao.com/blog/2025/using-claude-code-with-obsidian/)——
   经典案例：读日记，把提到的人、地点、书自动建实体笔记并加双链
2. 研究 [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)：
   Karpathy LLM Wiki 模式的完整实现，重点看它的 `skills/wiki-lint/SKILL.md`（如何保证链接质量）
3. 理论背景（选读）：[SegmentFault：Karpathy 式 AI 知识库搭建指南](https://segmentfault.com/a/1190000047707371)

**动手任务**
- 写 `/link` 命令：扫描指定笔记，识别人物/项目/概念 → 库里有实体笔记就加 `[[链接]]`，
  没有就新建一条带 frontmatter 的实体笔记
- 对你已有的 pdf2obsidian 解读笔记跑一遍，让报告解读之间通过共同概念连起来
- 打开 Obsidian 的 Graph View，看看图谱是不是「长」出来了

**✅ 完成标志**：随便打开一篇旧笔记，能通过双链在 3 跳内到达至少 5 篇相关笔记。

---

## 阶段 3 · 定时自动化：会自己长大的库（第 4 周）

**为什么第三**：前两阶段还需要你「主动跑命令」，这一阶段把它们变成后台任务——
**复利从这里开始**。你已经有现成基础：仓库里的 tracking/ 周报模式和 pdf2obsidian 的
cron 用法，直接迁移即可，学习成本比别人低一半。

**学什么**
1. 精读 [Obsidian + Codex：用 cron 定时维护库](https://codeculture.store/blogs/developer-culture/obsidian-codex-developer-workflow)——
   核心思想一句话：**agent 跑在 cron 里而不是聊天里**（思路对 Claude Code 完全通用，`claude -p` 即可）
2. 参考 [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain)
   的 scheduled agents 设计（44 条命令里挑 3 条抄）
3. 生产级加固（选读）：[Codex + Healthchecks + rsync](https://coefficiencies.com/posts/automating-my-obsidian-vault-with-obsidian-healthchecks-and-rsync/)——监控 + 备份

**动手任务**（三个 cron 任务，从易到难）
- ① 把 `pdf2obsidian.py --once` 挂上 cron（你已经会了，5 分钟）
- ② 每周日晚：agent 汇总本周新增笔记 / 完成任务 / 遗留 TODO → 生成周回顾笔记
  （直接复用你 tracking/weekly-report-prompt.md 的模式）
- ③ 每晚：`claude -p` 跑维护命令——修断链、给漏标签的笔记补标签、`git commit` 备份库

**✅ 完成标志**：连续两周不手动跑任何命令，周一早上打开 Obsidian 就有上周回顾，库的 git log 里每天有自动提交。

---

## 阶段 4 · 语义检索问答：「问我的库」（第 5 周）

**为什么第四**：检索的价值随库的大小增长——前三阶段积累的规范笔记越多，这一步回报越大。
库小于几百条时装它属于过早优化，所以放在积累之后。

**学什么**
1. 装 **Smart Connections** 插件（本地嵌入，零配置，公认第一个该装的 AI 插件）：
   看 [SystemSculpt 2026 插件测评](https://systemsculpt.com/blog/best-obsidian-ai-plugins-2026) 的对比部分
2. 配一个 MCP server 让 Claude Desktop / claude.ai 也能问你的库：
   [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian)（需要 Local REST API 插件）
   或插件形态的 [iansinnott/obsidian-claude-code-mcp](https://github.com/iansinnott/obsidian-claude-code-mcp)
3. 想聊天式问答再加 **Copilot for Obsidian**（移动端也能用）

**动手任务**
- 用 Smart Connections 打开任一笔记，看右侧「语义相关」面板是否真的相关
- 在 Claude Desktop 里问三个跨笔记的问题：「我对 X 的观点变化过吗」「上个月的 PDF 解读里
  哪些结论互相矛盾」「帮我找所有提到 Y 但还没建双链的笔记」

**✅ 完成标志**：遇到「我记得在哪看过…」的时刻，第一反应是问库而不是翻文件夹，且能问出结果。

---

## 阶段 5 · 输出与专业场景（第 6 周起，按需选修）

到这里核心体系已完整，以下按你的实际需求挑着学，不必全学：

| 方向 | 适合谁 | 资料 |
|---|---|---|
| **笔记 → 博客初稿** | 想公开写作 | 橙皮书 `/blog` 工作流；[WhyTryAI](https://www.whytryai.com/p/claude-code-obsidian) |
| **学术文献流** | 要读论文/写综述 | [Obsidian + Zotero + Claude 论文工作流](https://medium.com/@spektrl/my-thesis-writing-workflow-obsidian-zotero-and-claude-ai-2427737f531f)；[llm-for-zotero](https://github.com/yilewang/llm-for-zotero) |
| **嵌入式 agent 面板** | 不想开终端 | [claudian](https://github.com/yishentu/claudian)（Obsidian 里内嵌 Claude Code/Codex）；[Agent Client 插件](https://forum.obsidian.md/t/new-plugin-agent-client-bring-claude-code-codex-gemini-cli-inside-obsidian/108448) |
| **决策日志** | 常做技术/人生决策 | [James Donnelly：决策工作流](https://jamesdonnelly.dev/blog/obsidian-claude-code-workflow/) |
| **自己写 skills 深入进阶** | 想造轮子 | [conorluddy/ObsidianSkills](https://github.com/conorluddy/ObsidianSkills)、官方 skills 源码 |

**视频伴学**（任何阶段卡住时看）：
- 中文：[B 站：Obsidian+Claude+Skills+云同步](https://www.bilibili.com/video/BV1vAzzBwECr/)、
  [Greg Isenberg 中配：用 Obsidian 和 Claude Code 管理人生](https://www.bilibili.com/video/BV1M2fmBYEoh/)
- 英文：[Ultimate AI Second Brain (Claude Code + Obsidian)](https://www.youtube.com/watch?v=C6b1bX1HNg8)、
  [Build a Second Brain That Actually Learns](https://www.youtube.com/watch?v=XuRfik_tHd4)

---

## 三条避坑原则（来自多篇资料的共同教训）

1. **不要跳过阶段 0/1 直接玩自动化**——库结构混乱时，agent 只会把混乱自动化。
2. **不要一次装十个 AI 插件**——先用 Claude Code + 官方 skills 打通全流程，插件按缺什么补什么。
3. **500 条笔记之前别过度建设**——定时维护、语义搜索的回报都随库变大而增长，前期把力气花在「多捕获」上。
