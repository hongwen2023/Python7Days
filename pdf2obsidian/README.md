# pdf2obsidian：PDF 报告 → 通俗解读 → 自动出现在 Obsidian

把 PDF 报告丢进一个「收件箱」文件夹，脚本自动完成：

```
收件箱/*.pdf ──► 提取文字 ──► Claude 生成通俗解读 ──► .md 写入 Obsidian 库 ──► 打开 Obsidian 自动出现
```

关键原理：**Obsidian 的库（Vault）就是一个普通文件夹**。任何程序往里写 `.md` 文件，
Obsidian 打开时（或正开着时）都会立刻显示出来——不需要任何插件。

## 一、准备（只做一次）

```bash
cd pdf2obsidian
pip install -r requirements.txt        # 只用 claude-cli 引擎时，装 PyMuPDF 即可
cp config.example.yaml config.yaml
```

编辑 `config.yaml`，改两个路径：

| 配置项 | 填什么 |
|---|---|
| `inbox_dir` | 你丢 PDF 的文件夹，例如 `~/PDF收件箱` |
| `vault_dir` | Obsidian 库里的子文件夹，例如 `~/Documents/MyVault/PDF解读` |

解读引擎二选一：

- **`engine: claude-cli`（推荐）**：直接调用你本机已登录的 Claude Code 命令行（`claude -p`），不需要 API key。
- **`engine: api`**：走 Anthropic API，需要 `pip install anthropic` 并设置环境变量 `ANTHROPIC_API_KEY`。

## 二、日常使用

```bash
# 方式 1：手动扫一遍收件箱，处理完退出
python pdf2obsidian.py --once

# 方式 2：常驻监控，新 PDF 一放进来 30 秒内自动处理
python pdf2obsidian.py --watch

# 方式 3：只处理某一个文件
python pdf2obsidian.py --file ~/Downloads/某研究报告.pdf
```

生成的笔记长这样：`原文件名（通俗解读）.md`，带 YAML frontmatter（日期、来源 PDF、
`#pdf解读` 标签），正文包含：一句话总结 → 报告在讲什么 → 关键结论 → 专业名词翻译 →
对我意味着什么 → 原文值得一读的部分。

想改解读的风格 / 结构，直接编辑 `prompts/interpret.md` 即可，不用动代码。

已处理过的 PDF 记录在 `.state.json`（按文件内容哈希判断），重复扫描不会重复解读；
想强制重新解读，删掉 `.state.json` 里对应条目即可。

## 三、做到「全自动」：定时任务

### macOS / Linux（cron，每 10 分钟扫一次）

```bash
crontab -e
# 加入一行（路径换成你自己的）：
*/10 * * * * cd /path/to/Python7Days/pdf2obsidian && /usr/bin/python3 pdf2obsidian.py --once >> run.log 2>&1
```

### Windows（任务计划程序）

任务计划程序 → 创建基本任务 → 触发器选「每天」+ 重复间隔 10 分钟 →
操作填 `python`，参数填 `pdf2obsidian.py --once`，起始位置填 `pdf2obsidian` 文件夹路径。

### 或者干脆开机常驻

把 `python pdf2obsidian.py --watch` 加入登录启动项（macOS 可用 `launchd`，
Windows 放进「启动」文件夹），效果是丢进 PDF 后半分钟内笔记就出现在 Obsidian 里。

## 四、手机 / 多设备也自动出现

只要 `vault_dir` 指向的库处于同步之中，笔记就会同步到所有设备：

- **Obsidian Sync**（官方付费）或 **iCloud / OneDrive / Syncthing** 同步库文件夹均可；
- 进阶玩法：`inbox_dir` 也放在同步盘里，这样手机上保存一个 PDF 到该文件夹，
  家里电脑的定时任务就会自动解读并回写笔记，手机上稍后就能看到解读版。

## 五、常见问题

- **扫描件（图片型 PDF）提取不到文字**：脚本会提示并跳过。先用
  `ocrmypdf 输入.pdf 输出.pdf` 做 OCR，再把输出文件放回收件箱。
- **报告特别长**：默认最多送 12 万字给模型（保留开头 80% + 结尾 20%），
  可在 `config.yaml` 的 `max_chars` 调整。
- **想在笔记里链接回原 PDF**：把 PDF 也放进库里（Obsidian 支持预览 PDF），
  然后在 frontmatter 的 `source_pdf` 基础上自己加 `[[文件名.pdf]]` 链接，
  或修改 `write_note()` 顺手把 PDF 复制进库。
