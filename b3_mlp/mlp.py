"""makemore MLP（骨架）。Bengio et al. 2003 的字符级复现。

约定:
- 词表与 b2 相同: '.'=0, a=1, ..., z=26
- 上下文窗口 block_size: 用前 block_size 个字符预测下一个
- 名字 "ab" 在 block_size=3 时产生 3 个样本:
    [., ., .] -> a
    [., ., a] -> b
    [., a, b] -> .
"""
import torch


def build_dataset(words, stoi, block_size=3):
    """滑动窗口构造数据集。
    返回 (X, Y): X 形状 (N, block_size) 的 int64 张量, Y 形状 (N,) 的 int64 张量。"""
    raise NotImplementedError


class MLP:
    """embedding -> 拼接 -> tanh 隐藏层 -> logits。

    参数(全部用传入的 generator 以 torch.randn 初始化, 需 requires_grad_(True)):
      C  : (vocab_size, n_emb)          字符 embedding 表
      W1 : (block_size * n_emb, n_hidden)
      b1 : (n_hidden,)
      W2 : (n_hidden, vocab_size)
      b2 : (vocab_size,)
    """

    def __init__(self, vocab_size=27, block_size=3, n_emb=10, n_hidden=200, generator=None):
        raise NotImplementedError

    def parameters(self):
        """返回 [C, W1, b1, W2, b2]。"""
        raise NotImplementedError

    def forward(self, X):
        """X: (N, block_size) int64 -> logits: (N, vocab_size)。
        emb = C[X] -> view 拼接 -> tanh(@W1+b1) -> @W2+b2。"""
        raise NotImplementedError


def cross_entropy(logits, Y):
    """手写数值稳定的交叉熵, 返回标量张量(保持在计算图上, 可 backward)。
    禁止调用 torch.nn.functional.cross_entropy / log_softmax / softmax。
    提示: logits 每行先减 max, 再 exp / 求和 / 取 log。"""
    raise NotImplementedError


def train(model, X, Y, steps=200, batch_size=64, lr=0.1, generator=None):
    """小批量 SGD 训练。每步:
      随机取 batch (用 torch.randint(..., generator=generator)) ->
      forward -> cross_entropy -> 手动清零梯度 -> backward -> 参数 -= lr * grad。
    返回最后一步的 loss (float)。"""
    raise NotImplementedError
