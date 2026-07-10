"""makemore bigram（骨架）。

约定:
- 词表 = 26 个小写字母 + 起止符 '.'，共 27 个字符
- '.' 的索引固定为 0，其余按字母序: a=1, b=2, ..., z=26
- 每个名字视作 ".name." 的字符序列（'.' 同时充当开始与结束符）
"""
from pathlib import Path

import torch


def load_words(path=None):
    """读取 names.txt, 返回名字列表(小写, 无空行)。默认路径为仓库根目录的 names.txt。"""
    if path is None:
        path = Path(__file__).resolve().parents[1] / "names.txt"
    raise NotImplementedError


def build_vocab(words):
    """返回 (stoi, itos) 两个字典。'.'=0, a=1, ..., z=26。"""
    raise NotImplementedError


def build_counts(words, stoi):
    """返回 27x27 的整型张量 N, N[i, j] = 字符 i 后面跟字符 j 出现的次数。
    每个名字按 '.' + name + '.' 处理。"""
    raise NotImplementedError


def counts_to_probs(N, smoothing=1):
    """计数矩阵 -> 行归一化的概率矩阵 P (float), 每行和为 1。
    smoothing: 归一化前给每个计数加上的常数 (拉普拉斯平滑)。"""
    raise NotImplementedError


def nll(P, words, stoi):
    """整个数据集上的平均负对数似然 (float)。
    对每个名字的每个 bigram (i, j), 累加 -log P[i, j], 最后除以 bigram 总数。"""
    raise NotImplementedError


def sample(P, itos, g, num=1):
    """从模型采样 num 个名字, 返回字符串列表 (不含 '.' )。
    g: torch.Generator, 用 torch.multinomial(..., generator=g) 保证可复现。
    从 '.'(索引0) 出发, 采到 '.' 结束。"""
    raise NotImplementedError
