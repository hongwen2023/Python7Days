# 高阶金融 Skills 学习笔记（一）：S&P Global 与 Bigdata.com 官方 Agent Skills

> 学习日期：2026-07-03
> 学习对象：两家金融数据巨头在 GitHub 上开源的 Claude Agent Skills
>
> - S&P Global（由旗下 Kensho 发布）：[kensho-technologies/spglobal-agent-skills](https://github.com/kensho-technologies/spglobal-agent-skills)（Apache 2.0）
> - Bigdata.com（RavenPack 旗下）：[Bigdata-com/skills-financial-research-analyst](https://github.com/Bigdata-com/skills-financial-research-analyst)

---

## 0. 背景：Agent Skill 是什么

Agent Skill 本质上是一组 **Markdown 文件**（入口为 `SKILL.md`，带 YAML frontmatter 的 `name`/`description`），把专业工作流"教"给 AI 助手：

- `description` 决定**何时自动触发**（用户说"earnings preview"、"tear sheet"等关键词时激活）；
- 正文定义**工作流步骤、数据规则、输出模板**；
- `references/` 子目录存放按需加载的深度知识（渐进式披露，节省上下文）；
- 两家的 skills 都依赖各自的 **MCP server** 提供实时数据——skill 负责"方法论"，MCP 负责"数据"。

这两个仓库是目前金融领域最有代表性的官方 skills，设计思路截然不同，非常适合对照学习。

---

## 1. S&P Global Plugin（Kensho 出品）

### 1.1 仓库结构

```
spglobal-agent-skills/
├── .claude-plugin/marketplace.json     # Claude 插件市场配置
├── .agents/plugins/marketplace.json    # Codex 插件市场配置（跨平台）
└── plugins/spglobal-plugin/
    ├── .mcp.json                       # MCP: https://kfinance.kensho.com/integrations/mcp
    └── skills/
        ├── tear-sheet/                 # 公司速览表（Word 输出）
        ├── earnings-preview-beta/      # 财报前瞻（HTML 输出）
        ├── funding-digest/             # 融资周报（PPT 输出）
        └── sp-capital-iq-excel-pro/    # Capital IQ Excel 建模
```

**数据依赖**：需要 Capital IQ Pro 或 S&P Global LLM-ready API 订阅，通过 Kensho 的 kfinance MCP server 取数（工具如 `get_financial_line_item_from_identifiers`、`get_transcript_from_key_dev_id`、`get_consensus_estimates_from_identifiers` 等）。

### 1.2 四个 Skill 详解

#### ① tear-sheet — 公司速览表生成器（521 行）

按**四类受众**生成 1-2 页的公司简报 Word 文档，同一家公司、不同读者、不同写法：

| 受众 | 用途 | 侧重 |
|------|------|------|
| Equity Research | 买方/卖方分析师 | 投资论点、共识预期、交易倍数 |
| IB / M&A | 投行交易场景 | 利润率轨迹、M&A 活动、pitchbook 文风 |
| Corp Dev | 内部并购团队 | 收购标的画像、战略契合、整合考量 |
| Sales / BD | 商务团队见客户 | 通俗语言、话题切入点（Conversation Starters） |

工作流五步：**识别输入 → 读受众参考文件 → MCP 取数（边查边落盘）→ 单独的派生指标计算与校验步骤 → 生成 DOCX**。

#### ② earnings-preview-beta — 财报前瞻（524 行，最工程化的一个）

生成 4-5 页 HTML 研报：投资论点 + 共识预期表 + 8 张图表（Chart.js）+ 可点击溯源附录。分 8 个 Phase：公司画像 → 财报电话会纪要分析 → 竞争对手分析 → 新闻/预期检索 → 财务数据采集 → **校验与计算** → 生成报告 → 输出。

#### ③ funding-digest — 融资周报（513 行）

把某个赛道/自选公司近期融资活动汇总成**一页 PPT**。亮点是一整套**实体解析鲁棒性规则**（详见 1.3 第 5 条）。

#### ④ sp-capital-iq-excel-pro — Capital IQ Excel 建模（821 行）

教 AI 写带 `=SPG(...)` 实时数据公式的 Excel 模型（DCF/LBO/comps）。核心规则：
- **禁止臆造数据项代码**——只能用文档中列出的 mnemonic（如 `IQ_TOTAL_REV`、`SP_MARKETCAP`），附一个官方 Excel 参考手册做查询源；
- **零公式错误**——一律 `IFERROR()` 兜底、公司标识符放专用单元格用绝对引用 `$C$2`、优先 `"NASDAQ:NVDA"` 这种交易所限定格式；
- openpyxl 写公式时**不能带 `@`**（隐式交集运算符会让公式变成文本）。

### 1.3 值得抄的工程模式（S&P 篇精华）

这套 skills 最大的价值不是模板，而是针对 **LLM 固有弱点**的系统性防御：

1. **中间文件规则（Intermediate File Rule）**：每次 MCP 调用返回后**立即**把原始数据写入 `/tmp/.../xxx.csv`，"文件而非对话记忆是每个数字的唯一事实来源"。这是对抗长对话上下文压缩失真的关键手段，生成报告前强制逐个 `cat` 回来并打印核验清单。
2. **采数与计算分离**：采集阶段只写原始值，利润率/增速/P/E 全部放到专门的计算 Phase，每个派生值记录 `metric,value,formula,components`，算式可复算、可审计。
3. **数据完整性规则**：工具没返回的数一律 "N/A"，**绝不用训练知识补数**；财年 ≠ 日历年（沃尔玛 2 月出的是 Q4 FY2026）；LTM/NTM 必须显式标注；分部收入占比用合并收入做分母（分部之和常大于合并数）；股价回报所有标的必须用同一基准日。
4. **逐字引用规则**：管理层引语必须与 transcript 逐字一致，找不到原句就降级为转述、不准用引用格式——直接封死"编造引语"这一 LLM 高发问题。
5. **实体解析防御**（funding-digest）：查数前先 `get_info_from_identifiers` 批量预校验；`status="Operating Subsidiary"` 的子公司（DeepMind、GitHub）融资轮次必为空，要在母公司层面查；品牌名解析失败时回退法定实体名（Together AI → "Together Computer, Inc."）；`role` 参数用错会**静默返回空**。
6. **组件函数强制复用**：DOCX 排版不许自由发挥，必须调用 skill 里给好的 `createTable()`/`createSectionHeader()` 等 JS 函数——用代码锁死样式一致性，防止黑底表格之类的渲染事故。
7. **全文超链接溯源**：报告正文每个数字/论断都要 `<a href="#ref-N">` 链到附录，附录里计算值的公式**每个分量也是超链接**，可以一路点回原始 MCP 调用。
8. **AI 免责声明**：黄色横幅 "Analysis is AI-generated — please confirm all outputs" 在页眉、页脚、附录三处强制出现。

---

## 2. Bigdata.com Financial Research Analyst Skill

### 2.1 仓库结构

```
skills-financial-research-analyst/
├── scripts/build-skill.sh              # 打包成 .skill 文件（可 fork 定制后重新构建）
└── bigdata-financial-research-analyst/
    ├── SKILL.md                        # 入口：路由 + 核心方法论（188 行）
    ├── assets/templates/               # 投资备忘录 / 快评 / 财报点评 三套输出模板
    ├── scripts/                        # 5 个可选 Python 量化脚本
    └── references/
        ├── public_company/             # 公司简报/财报前瞻/财报点评/风险评估/估值快照
        ├── macro/                      # 行业/国家/区域/主题宏观分析
        └── equity-analysis/            # 机构级股票研究知识库（26 个文件）
            ├── foundations/            # Graham-Dodd 价值投资原则
            ├── valuation/              # DCF、倍数、反向 DCF、分部加总
            ├── financial-analysis/     # 盈利质量、财务红旗清单
            ├── competitive-analysis/   # 护城河分类、波特五力
            ├── management/             # 资本配置评估
            ├── variant-perception/     # EPIC、FaVeS、论点构建
            ├── special-situations/     # 并购套利/激进投资/困境/做空/分拆
            └── sectors/                # 科技SaaS/银行/医药/REITs/工业/消费/能源 行业手册
```

**数据依赖**：Bigdata.com MCP 连接（Claude 里是官方 connector）。核心工具：`find_securities`（先解析 entity_id）→ `bigdata_company_tearsheet`（财务基线）/ `bigdata_search`（新闻/文件/纪要，一次一个焦点）/ `bigdata_events_calendar` / `bigdata_country_tearsheet`（宏观）。

### 2.2 架构：单一 Skill + 三层路由

入口 SKILL.md 是一个**路由器**，按请求分发到三大类：

| 类别 | 典型请求 | 参考目录 |
|------|---------|---------|
| Public company | "NVIDIA 财报前瞻"、"特斯拉风险评估"、"苹果值多少钱" | `references/public_company/` |
| Macro | "分析美国科技板块"、"德国经济展望"、"对比 G7" | `references/macro/` |
| Institutional equity | "微软做个完整 DCF"、"分部加总"、"法务会计排雷" | `references/equity-analysis/` |

### 2.3 核心分析框架（这套 skill 的真正干货）

**投资哲学三支柱**：内在价值（独立于股价估值）、**变体认知**（明确说出你和共识哪里不同）、质量优于数量（只抓最重要的 2-3 个驱动因素）。

**EPIC 框架**——筛选"什么才值得分析"，四关全过才算关键驱动因素：

| 测试 | 问题 | 通过标准 |
|------|------|---------|
| **E**ffect | 重要吗？ | 该因素变动 ~10% 能显著改变内在价值（>5%） |
| **P**redictability | 能预测吗？ | 你有分析或信息优势 |
| **I**ndependence | 共识错了吗？ | 市场系统性误判此项 |
| **C**onsensus gap | 有差距吗？ | 你的预测与共识差异有意义 |

**FaVeS 框架**——变体认知三要素：**Fa**ndamentals（哪 2-3 个 KPI 驱动价值、预期哪里会错）/ **V**aluation（内在价值多少、该给什么倍数）/ **Se**ntiment（价格已计入什么——用反向 DCF 检验、投资者如何持仓）。

**按公司类型选估值方法**（速查表）：

| 公司类型 | 主方法 | 交叉验证 |
|---------|--------|---------|
| 稳定盈利 | DCF (FCFF) | EV/EBITDA、P/E |
| 高增长未盈利 | EV/Revenue、长 CAP 的 DCF | 反向 DCF |
| 银行/保险 | P/TBV、股利折现 | P/E、剩余收益 |
| REIT | NAV、P/AFFO | 隐含资本化率 |
| 综合集团 | 分部加总 SOTP | 控股折价 |
| 困境公司 | 清算/回收价值 | 资产覆盖率 |

**盈利质量速筛**：OCF/净利润（健康 >0.8，红旗 <0.6 或趋势背离）、应计项、DSO 与收入趋势对比。深挖时有 Beneish M-Score 脚本。

**财报前瞻的强制章节**：EPIC 驱动表、FaVeS、情绪与持仓数据表、**牛/基/熊三情景**（各带概率与目标价、算出概率加权期望值且展示计算过程）、盈利质量 watch-for 列、监管/法律检索。

**输出的 PM 测试**（每份交付物必须过）：What's different?（非共识角度）/ What matters?（2-3 个主导驱动）/ What should I do about it?（净评估 + 关键风险 + 下一个催化剂）。收尾格式：`Net assessment: [正/负/中性] because [具体原因]; key risk: [X]; next catalyst: [Y]`。

**可选量化脚本**（默认不跑，用户明确要"建模输出"才用）：`dcf_model.py`、`reverse_dcf.py`、`earnings_quality.py`（Beneish M-Score）、`peer_comparables.py`、`scenario_probability.py`。

**合规要求**：每份交付物结尾必须带 "Powered by Bigdata.com" 署名和免责声明（verbatim）；宏观报告要求 [1][2] 行内引用 + 文末来源表。

---

## 3. 两家对比：两种 Skill 设计哲学

| 维度 | S&P Global | Bigdata.com |
|------|-----------|-------------|
| 结构 | 4 个独立 skill 组成 plugin | 1 个 skill + 分层 references 路由 |
| 定位 | **交付物流水线**：把取数→校验→排版工程化 | **分析方法论**：把机构投研的思维框架教给 AI |
| 输出 | 格式严控的 DOCX / HTML / PPTX / XLSX | Markdown 为主，可升级 Word/PPT |
| 防错重心 | 数据管道（中间文件、算术校验、逐字引用、全链路溯源） | 分析纪律（EPIC 过滤、变体认知、情景概率、PM 测试） |
| 知识密度 | 流程规则密集（"怎么做不出错"） | 领域知识密集（"资深分析师怎么想"） |
| 可定制性 | 改 Style Configuration 换成自家品牌模板 | fork 后改模板/风险框架，`build-skill.sh` 重新打包 |

**一句话总结**：S&P 教 AI 当"严谨的研究助理"，Bigdata 教 AI 当"有观点的分析师"。自己写金融 skill 时，理想形态是两者结合——用 S&P 的数据管道纪律 + Bigdata 的分析框架。

## 4. 可迁移的 Skill 工程通用经验

1. **description 是触发器**：把用户可能说的自然语言短语（"tear sheet"、"earnings preview"、"what is X worth"）都写进 frontmatter description。
2. **渐进式披露**：入口 SKILL.md 只放路由和核心规则，深度内容放 references/ 按需读取，控制上下文成本。
3. **对话记忆不可信**：长流程一律"边查边落盘、生成前读回"，文件是唯一事实来源。
4. **先取数、再计算、后写作**：三阶段硬隔离，每个派生数记录公式与分量。
5. **用代码锁死格式**：给现成的组件函数/模板 helper，禁止模型自由排版。
6. **枚举 API 的失败模式**：空结果 ≠ 没有数据（子公司、别名、role 参数错误），写明回退路径。
7. **合规三件套**：AI 免责声明、数据来源署名、"不构成投资建议"。

## 5. 安装使用速记

- **Claude Code / Cowork**：S&P 走 plugin marketplace（仓库含 `.claude-plugin/marketplace.json`），可按 [官方文档](https://code.claude.com/docs/en/discover-plugins#add-from-github) 从 GitHub 添加；Bigdata 从 [Releases](https://github.com/Bigdata-com/skills-financial-research-analyst/releases) 下载 `.skill` 文件，Claude Settings → Capabilities 上传。
- **数据前置条件**：S&P 需 Capital IQ Pro 或 LLM-ready API 订阅（MCP: `kfinance.kensho.com`）；Bigdata 需连接 Bigdata.com MCP connector。
- 两者都是 Markdown，任何支持 system prompt / 知识文件的平台（含 Copilot）都能移植。

## 6. 下一步学习计划

- [ ] 精读 Bigdata `references/equity-analysis/` 的估值四件套（DCF、倍数、反向 DCF、SOTP）并做笔记
- [ ] 精读盈利质量 + 红旗清单，配合 `earnings_quality.py` 理解 Beneish M-Score
- [ ] 读 7 个行业手册（sectors/），整理各行业关键 KPI 对照表
- [ ] 特殊情境五篇（并购套利/激进/困境/做空/分拆）
- [ ] 用本会话已接入的 Bigdata.com MCP 工具实操一次"财报前瞻"完整工作流
- [ ] 模仿两家的模式，为自己写一个中文投研 skill
