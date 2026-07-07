#!/usr/bin/env python3
"""
pdf2obsidian —— 把 PDF 报告自动变成「通俗解读版」Markdown 笔记，直接落进 Obsidian 库。

流水线：
    收件箱文件夹里的 *.pdf
        → 提取正文文字 (PyMuPDF)
        → 调用 Claude 生成通俗解读 (claude CLI 或 Anthropic API)
        → 带 YAML frontmatter 的 .md 写入 Obsidian 库指定文件夹
        → Obsidian 打开时自动出现（库就是普通文件夹，无需任何插件）

三种运行方式：
    python pdf2obsidian.py --once            # 扫一遍收件箱，处理完退出（适合 cron / 计划任务）
    python pdf2obsidian.py --watch           # 常驻监控，新 PDF 一放进来就处理
    python pdf2obsidian.py --file 某报告.pdf  # 只处理指定的一个文件

配置见同目录 config.yaml（参考 config.example.yaml）。
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
STATE_FILE = SCRIPT_DIR / ".state.json"       # 记录已处理过的 PDF（按内容哈希），避免重复解读
PROMPT_FILE = SCRIPT_DIR / "prompts" / "interpret.md"

# ---------------------------------------------------------------- 配置 ----------


def load_config() -> dict:
    """读取 config.yaml。只用到最简单的 key: value 格式，不依赖 pyyaml。"""
    cfg_path = SCRIPT_DIR / "config.yaml"
    if not cfg_path.exists():
        sys.exit(
            "找不到 config.yaml —— 请先复制 config.example.yaml 为 config.yaml 并改成你的路径。"
        )
    cfg = {}
    for line in cfg_path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" in line:
            key, val = line.split(":", 1)
            cfg[key.strip()] = val.strip().strip('"').strip("'")
    for required in ("inbox_dir", "vault_dir"):
        if not cfg.get(required):
            sys.exit(f"config.yaml 缺少必填项 {required}")
    cfg.setdefault("engine", "claude-cli")
    cfg.setdefault("model", "claude-sonnet-5")
    cfg.setdefault("max_chars", "120000")
    return cfg


# ---------------------------------------------------------- PDF 文字提取 ----------


def extract_text(pdf_path: Path, max_chars: int) -> str:
    """用 PyMuPDF 逐页提取文字。返回空字符串说明多半是扫描件（图片型 PDF）。"""
    import fitz  # PyMuPDF，见 requirements.txt

    pages = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            pages.append(page.get_text())
    text = "\n\n".join(pages).strip()
    if len(text) > max_chars:
        # 报告太长时保留开头为主（结论、摘要通常在前面），结尾留一小段
        head = text[: int(max_chars * 0.8)]
        tail = text[-int(max_chars * 0.2):]
        text = head + "\n\n……（中间部分因篇幅省略）……\n\n" + tail
    return text


# ------------------------------------------------------------ 调用 Claude ----------


def build_prompt(pdf_name: str, text: str) -> str:
    template = PROMPT_FILE.read_text(encoding="utf-8")
    return template.replace("{filename}", pdf_name).replace("{text}", text)


def interpret_with_cli(prompt: str, model: str) -> str:
    """走本机已登录的 claude CLI（Claude Code），无需 API key。"""
    result = subprocess.run(
        ["claude", "-p", "--model", model],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude CLI 调用失败：{result.stderr.strip()[:500]}")
    return result.stdout.strip()


def interpret_with_api(prompt: str, model: str) -> str:
    """走 Anthropic API，需要环境变量 ANTHROPIC_API_KEY。"""
    import anthropic  # 见 requirements.txt

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in message.content if block.type == "text")


# ------------------------------------------------------------- 写入笔记 ----------


def safe_stem(name: str) -> str:
    """去掉 Obsidian / 文件系统不喜欢的字符。"""
    return re.sub(r'[\\/:*?"<>|#^\[\]]', "_", name).strip() or "untitled"


def write_note(vault_dir: Path, pdf_path: Path, body: str) -> Path:
    stem = safe_stem(pdf_path.stem)
    note_path = vault_dir / f"{stem}（通俗解读）.md"
    # 同名冲突时加序号，绝不覆盖已有笔记
    counter = 2
    while note_path.exists():
        note_path = vault_dir / f"{stem}（通俗解读）{counter}.md"
        counter += 1
    frontmatter = "\n".join(
        [
            "---",
            f"created: {date.today().isoformat()}",
            f'source_pdf: "{pdf_path.name}"',
            "tags:",
            "  - pdf解读",
            "  - 自动生成",
            "---",
            "",
        ]
    )
    note_path.write_text(frontmatter + body + "\n", encoding="utf-8")
    return note_path


# ------------------------------------------------------------- 主流程 ----------


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def process_pdf(pdf_path: Path, cfg: dict, state: dict) -> None:
    digest = file_hash(pdf_path)
    if state.get(digest):
        print(f"跳过（已处理过）：{pdf_path.name}")
        return

    print(f"处理中：{pdf_path.name}")
    text = extract_text(pdf_path, int(cfg["max_chars"]))
    if len(text) < 100:
        print(
            f"  ⚠ 提取不到文字，{pdf_path.name} 可能是扫描件（图片型 PDF），"
            "需要先 OCR（可用 ocrmypdf 处理后再放回收件箱）。已跳过。"
        )
        return

    prompt = build_prompt(pdf_path.name, text)
    if cfg["engine"] == "api":
        body = interpret_with_api(prompt, cfg["model"])
    else:
        body = interpret_with_cli(prompt, cfg["model"])

    vault_dir = Path(cfg["vault_dir"]).expanduser()
    vault_dir.mkdir(parents=True, exist_ok=True)
    note_path = write_note(vault_dir, pdf_path, body)
    state[digest] = {"pdf": pdf_path.name, "note": note_path.name,
                     "date": date.today().isoformat()}
    save_state(state)
    print(f"  ✓ 已生成笔记：{note_path}")


def pdf_is_stable(pdf_path: Path, wait: float = 1.5) -> bool:
    """确认文件不再变大（还在下载/复制中的 PDF 先不处理）。"""
    size1 = pdf_path.stat().st_size
    time.sleep(wait)
    return pdf_path.stat().st_size == size1


def scan_once(cfg: dict) -> None:
    inbox = Path(cfg["inbox_dir"]).expanduser()
    if not inbox.is_dir():
        sys.exit(f"收件箱文件夹不存在：{inbox}")
    state = load_state()
    pdfs = sorted(inbox.glob("*.pdf")) + sorted(inbox.glob("*.PDF"))
    if not pdfs:
        print("收件箱里没有 PDF。")
        return
    for pdf_path in pdfs:
        try:
            if pdf_is_stable(pdf_path):
                process_pdf(pdf_path, cfg, state)
        except Exception as exc:  # 单个文件失败不影响其余文件
            print(f"  ✗ 处理 {pdf_path.name} 失败：{exc}")


def watch(cfg: dict) -> None:
    """常驻模式：先补扫一遍存量，然后每 30 秒轮询一次新文件。"""
    print(f"开始监控 {cfg['inbox_dir']}（Ctrl+C 退出）…")
    while True:
        scan_once(cfg)
        time.sleep(30)


def main() -> None:
    parser = argparse.ArgumentParser(description="PDF 报告 → 通俗解读 Obsidian 笔记")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--once", action="store_true", help="扫描一遍收件箱后退出")
    group.add_argument("--watch", action="store_true", help="常驻监控收件箱")
    group.add_argument("--file", type=str, help="只处理指定 PDF 文件")
    args = parser.parse_args()

    cfg = load_config()
    if args.file:
        process_pdf(Path(args.file).expanduser(), cfg, load_state())
    elif args.watch:
        watch(cfg)
    else:
        scan_once(cfg)


if __name__ == "__main__":
    main()
