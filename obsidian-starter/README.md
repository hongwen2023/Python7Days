# obsidian-starter：阶段 0+1 一键启动包

学习路线图（`resources/obsidian-ai-learning-path.md`）前两个阶段的落地工具：
跑一条命令，你的 Obsidian 库就具备「官方 skills + 标准文件夹结构 + /inbox 自动分诊」。

## 在你自己的电脑上执行（Mac / Linux / Windows-Git Bash）

```bash
# 1. 取到本仓库（已有则 git pull）
git clone https://github.com/hongwen2023/Python7Days.git
cd Python7Days/obsidian-starter

# 2. 一键安装到你的库（路径换成你的；库不存在会自动创建）
bash setup.sh ~/Documents/MyVault
```

脚本做三件事，全部**幂等且不覆盖已有文件**：

1. 建文件夹结构：`00_Inbox`（收件箱）/ `10_项目` / `20_领域` / `30_资源/PDF解读` / `40_归档`
2. 安装 [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)（Obsidian CEO 官方 Agent Skills）到 `.claude/skills/`
3. 安装 `/inbox` 分诊命令到 `.claude/commands/`，学习打卡笔记放到库根目录

## 安装后：阶段 0 验收（当天完成）

```bash
cd ~/Documents/MyVault
claude
```

依次试三个指令：

1. 「总结我最近的 5 篇笔记」
2. 「给 XXX 这篇笔记补上合适的 frontmatter 和标签」
3. 「我的库里关于 Python 的笔记有哪些，互相有链接吗」

✅ 验收：让它「把两篇笔记链接起来」，用的是 `[[wikilink]]` 就过关。

## 阶段 1：开始零摩擦捕获（连续 7 天）

每天：想到什么直接扔 `00_Inbox`（手机端配合同步盘也可以扔）→ 跑一次 `/inbox` → 检查归档是否合理。

- 归错了不要手动改完就算了——**把纠正规则写进 `.claude/commands/inbox.md`**，它会越来越懂你。
- 把 `pdf2obsidian/config.yaml` 的 `vault_dir` 改成 `你的库/30_资源/PDF解读`，报告解读自动并入体系。
- 进度记录在库根目录的 `学习打卡-Obsidian-AI.md`。

✅ 验收：连续 7 天捕获零思考、Inbox 每天清零 → 回到路线图解锁阶段 2（自动双链）。

## 文件清单

```
obsidian-starter/
├── setup.sh                          # 一键安装脚本
├── vault-template/
│   ├── .claude/commands/inbox.md     # /inbox 分诊命令（核心，可按需修改规则）
│   ├── 00_Inbox/README.md            # 收件箱使用说明
│   └── 学习打卡-Obsidian-AI.md        # 六阶段进度打卡
└── README.md
```
