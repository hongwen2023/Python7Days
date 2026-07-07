# Obsidian + Claude / Codex 提效资料汇总（2026-07）

> 核心逻辑：**Obsidian 的库就是一个 Markdown 文件夹，而 Claude Code / Codex 这类命令行
> Agent 的工作目录也是文件夹** —— 让 Agent 直接在库里读写，笔记系统就升级成了
> 会自己整理、自己链接、自己写摘要的「活的第二大脑」。当前生态大致分六类。

---

## 一、官方 / 基础设施（必看，先装这个）

| 项目 | 说明 |
|---|---|
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | **Obsidian CEO Steph Ango 官方出品**的 Agent Skills（12.9k+ star）。教会 Claude Code / Codex / Gemini CLI 正确使用 wikilinks、frontmatter、callout、Bases、JSON Canvas。装法：把内容放进库根目录 `.claude/` 即可 |
| [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) | 最流行的 Obsidian MCP server，通过 Local REST API 插件让 Claude Desktop / claude.ai 读写、搜索、修改库 |
| [iansinnott/obsidian-claude-code-mcp](https://github.com/iansinnott/obsidian-claude-code-mcp) | Obsidian 插件形态的 MCP server，Claude Code 通过 WebSocket 自动发现并连接库 |
| [jacksteamdev/obsidian-mcp-tools](https://github.com/jacksteamdev/obsidian-mcp-tools) | 给任意 MCP 客户端加语义搜索 + Templater 自定义提示词 |

## 二、完整「第二大脑」开源系统（拿来即用）

| 项目 | 亮点 |
|---|---|
| [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | 自组织知识引擎：丢进任何资料，Claude 自动阅读、归档、建双链，形成知识图谱。基于 Karpathy 的 LLM Wiki 模式，含 wiki-lint 等 skills |
| [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) | 跨 CLI（Claude Code / Codex / Gemini…）的 44 条命令：自我改写笔记、本地语义搜索、免 key 网络调研、**定时 agent 睡觉时维护库** |
| [ballred/obsidian-claude-pkm](https://github.com/ballred/obsidian-claude-pkm) | Obsidian + Claude Code PKM 完整入门套件（starter kit） |
| [alchaincyf/obsidian-ai-orange-book](https://github.com/alchaincyf/obsidian-ai-orange-book) | **中文「橙皮书」**：AI 时代知识管理方法论 + 7 个可直接抄的工作流（/ingest、/compile、/blog…），40 分钟上手 |
| [conorluddy/ObsidianSkills](https://github.com/conorluddy/ObsidianSkills) | 把库与 agent 计划、GitHub issues 打通的 skills |
| [az9713/claude-code-obsidian](https://github.com/az9713/claude-code-obsidian) | 6 个 vault-* 工作流 skills + 官方 skills 的组合配置 |

## 三、把 Agent 嵌进 Obsidian 界面的插件

| 项目 | 亮点 |
|---|---|
| [YishenTu/claudian](https://github.com/yishentu/claudian) | 在 Obsidian 里内嵌 Claude Code / Codex 作为协作者，库即工作目录，有完整 agent 能力 |
| [Agent Client 插件](https://forum.obsidian.md/t/new-plugin-agent-client-bring-claude-code-codex-gemini-cli-inside-obsidian/108448) | 把 Claude Code、Codex、Gemini CLI 装进 Obsidian 侧边栏 |
| [takeshy/obsidian-llm-hub](https://github.com/takeshy/obsidian-llm-hub) | AI 聊天 + 工作流自动化 + 语义搜索，支持多家模型和 CLI 后端 |

## 四、传统 AI 插件（不需要命令行）

- **Smart Connections** —— 本地嵌入语义搜索，按「意思」找相关笔记，78 万+ 下载，公认第一个该装的
- **Copilot for Obsidian** —— 和整个库聊天问答，移动端可用
- **Smart Composer** —— Cursor 风格的笔记内写作，一键 apply
- **Text Generator** —— 模板化生成，frontmatter 驱动提示词
- **Local GPT** —— 配 Ollama 全本地、隐私优先
- 大全清单：[danielrosehill/Awesome-Obsidian-AI-Tools](https://github.com/danielrosehill/awesome-obsidian-ai-tools)；测评：[SystemSculpt 2026 排名](https://systemsculpt.com/blog/best-obsidian-ai-plugins-2026)

## 五、Codex 特色玩法：定时任务型「自更新维基」

- [Obsidian + Codex：用 cron 定时维护开发者库](https://codeculture.store/blogs/developer-culture/obsidian-codex-developer-workflow) —— 核心思想：**Codex 跑在 cron 里而不是聊天里**。定时分诊 Inbox、统一 frontmatter、生成索引、git 提交库状态；移动文件时自动搜索反链并修复
- [Codex + Healthchecks + rsync 自动化我的库](https://coefficiencies.com/posts/automating-my-obsidian-vault-with-codex-healthchecks-and-rsync/) —— 加上运行监控和备份的完整生产级方案
- 经验值：库超过 500 条笔记、每天新增 5–10 条时，这种自动维护开始明显回本

## 六、学术 / 文献场景（Zotero 三件套）

- [论文写作工作流：Obsidian + Zotero + Claude](https://medium.com/@spektrl/my-thesis-writing-workflow-obsidian-zotero-and-claude-ai-2427737f531f)
- [Zotero × Obsidian × NotebookLM 的 AI 时代科研流](https://lab.nounai-librarian.com/en/aiworkflow-2/)
- [yilewang/llm-for-zotero](https://github.com/yilewang/llm-for-zotero) —— LLM 进 Zotero PDF 阅读器，笔记直接存到 Obsidian 文件夹
- [Research Hub MCP](https://mcpmarket.com/server/research-hub-1) —— 自动生成论文聚类、AI 简报

## 七、精选博客 & 视频

**英文博客**
- [Using Claude Code with Obsidian — Kyle Gao](https://kyleygao.com/blog/2025/using-claude-code-with-obsidian/)（日记自动加双链的经典示例）
- [Turning Obsidian into an AI-Native Knowledge System — Mart Kempenaar](https://medium.com/@martk/turning-obsidian-into-an-ai-native-knowledge-system-with-claude-code-27cb224404cf)
- [My Developer Second Brain — James Donnelly](https://jamesdonnelly.dev/blog/obsidian-claude-code-workflow/)（决策日志工作流）
- [Build Your Second Brain — WhyTryAI](https://www.whytryai.com/p/claude-code-obsidian)

**YouTube**
- [How To Build The Ultimate AI Second Brain (Claude Code + Obsidian)](https://www.youtube.com/watch?v=C6b1bX1HNg8)
- [Claude Code + Obsidian: Build a Second Brain That Actually Learns](https://www.youtube.com/watch?v=XuRfik_tHd4)
- [The Second Brain Setup That Actually Works](https://www.youtube.com/watch?v=Y2rpFa43jTo)

**中文资源**
- [B 站：Obsidian+Claude+Skills+云同步打造 AI 笔记](https://www.bilibili.com/video/BV1vAzzBwECr/)
- [B 站中配：Greg Isenberg 如何用 Obsidian 和 Claude Code 管理人生](https://www.bilibili.com/video/BV1M2fmBYEoh/)
- [B 站：Claude Code + Skills 完整安装指南](https://www.bilibili.com/video/BV1jEzQBzEdz/)
- [知乎：让 Obsidian + Claude Code 帮你安排一切（全网最完整教程）](https://zhuanlan.zhihu.com/p/2010367947252704798)
- [博客园：Obsidian + Claude Code 搭建个人知识库实践指南](https://www.cnblogs.com/AlayaNeW/articles/19902167)
- [SegmentFault：Karpathy 式 AI 知识库搭建指南](https://segmentfault.com/a/1190000047707371)
- [腾讯云社区：Claude Code + Obsidian 让 AI 自动化知识管理](https://cloud.tencent.com/developer/article/2646839)

---

## 八、能做哪些提效工作（idea 清单）

从以上资料提炼的高价值自动化场景，按投入产出排序：

1. **Inbox 自动分诊**：随手丢想法/网页剪藏进 `00_Inbox`，agent 定时归档到领域文件夹、补 frontmatter、加标签 —— 最普适的「零摩擦捕获」
2. **自动双链**：读日记，把提到的人、地点、书自动建实体笔记并加 `[[wikilink]]`
3. **PDF / 网页 → 通俗解读笔记**：本仓库 `pdf2obsidian/` 已实现 ✅
4. **每周回顾自动生成**：agent 汇总本周新笔记、完成任务、遗留 TODO 成周报
5. **决策日志**：做架构/人生决策前让 agent 检索 Decisions 文件夹里的历史决策
6. **语义搜索问答**：「我去年对 X 的看法是什么」直接问库（Smart Connections / MCP）
7. **RSS / 收藏 → 摘要入库**：早上剪藏，中午 /ingest 自动整理，晚上看新增概念
8. **笔记 → 博客初稿**：/blog 命令把积累的概念笔记编译成文章草稿
9. **文献综述**：Zotero 标注 → agent 提取 → Obsidian 文献笔记 → 交叉综述
10. **睡觉时维护库**：cron 定时跑 agent 修断链、去重、更新索引、git 备份

## 九、给本仓库的建议路线

1. 先装 [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) 到库的 `.claude/`（10 分钟，所有后续玩法的地基）
2. 参照 [orange-book](https://github.com/alchaincyf/obsidian-ai-orange-book) 建 `00_Inbox` 流水线，把 `pdf2obsidian` 的输出并入同一体系
3. 用已有的 cron 思路加一个「每周回顾」任务（可复用本仓库 tracking/ 的周报模式）
4. 库变大后再上 Smart Connections 做语义检索
