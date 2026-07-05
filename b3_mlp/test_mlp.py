"""B3 验收测试。"""
import sys
from pathlib import Path

import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "b2_bigram"))
from bigram import load_words, build_vocab  # 复用 b2

from mlp import build_dataset, MLP, cross_entropy, train


def test_build_dataset_hand_checked():
    stoi, _ = build_vocab(["ab"])
    X, Y = build_dataset(["ab"], stoi, block_size=3)
    assert X.dtype == torch.int64 and Y.dtype == torch.int64
    assert X.shape == (3, 3) and Y.shape == (3,)
    a, b, dot = stoi["a"], stoi["b"], stoi["."]
    expected_X = torch.tensor([[dot, dot, dot], [dot, dot, a], [dot, a, b]])
    expected_Y = torch.tensor([a, b, dot])
    assert torch.equal(X, expected_X)
    assert torch.equal(Y, expected_Y)


def test_mlp_shapes_and_params():
    g = torch.Generator().manual_seed(42)
    model = MLP(vocab_size=27, block_size=3, n_emb=10, n_hidden=200, generator=g)
    params = model.parameters()
    assert len(params) == 5
    total = sum(p.numel() for p in params)
    # C: 27*10 + W1: 30*200 + b1: 200 + W2: 200*27 + b2: 27 = 11897
    assert total == 11897, f"参数量 {total} != 11897"
    assert all(p.requires_grad for p in params)

    X = torch.zeros((8, 3), dtype=torch.int64)
    logits = model.forward(X)
    assert logits.shape == (8, 27)


def test_cross_entropy_matches_pytorch():
    g = torch.Generator().manual_seed(0)
    logits = torch.randn(50, 27, generator=g)
    Y = torch.randint(0, 27, (50,), generator=g)
    ours = cross_entropy(logits, Y)
    ref = F.cross_entropy(logits, Y)
    assert abs(ours.item() - ref.item()) < 1e-5


def test_cross_entropy_numerically_stable():
    # 大 logits 下, 不稳定的实现会溢出成 inf/nan
    logits = torch.tensor([[1000.0, 999.0, 998.0], [-1000.0, -999.0, -998.0]])
    Y = torch.tensor([0, 2])
    loss = cross_entropy(logits, Y)
    assert torch.isfinite(loss), "大 logits 下 loss 应为有限值 (先减每行 max)"


def test_cross_entropy_backward_flows():
    logits = torch.randn(10, 27, requires_grad=True)
    Y = torch.randint(0, 27, (10,))
    loss = cross_entropy(logits, Y)
    loss.backward()
    assert logits.grad is not None
    ref_grad_logits = logits.detach().clone().requires_grad_(True)
    F.cross_entropy(ref_grad_logits, Y).backward()
    assert torch.allclose(logits.grad, ref_grad_logits.grad, atol=1e-5)


def test_training_reduces_loss():
    words = load_words()[:2000]
    stoi, _ = build_vocab(words)
    X, Y = build_dataset(words, stoi, block_size=3)

    g = torch.Generator().manual_seed(2147483647)
    model = MLP(vocab_size=27, block_size=3, n_emb=10, n_hidden=100, generator=g)

    with torch.no_grad():
        initial = cross_entropy(model.forward(X), Y).item()
    final = train(model, X, Y, steps=2000, batch_size=64, lr=0.1, generator=g)
    with torch.no_grad():
        full = cross_entropy(model.forward(X), Y).item()

    # 未训练时 loss 远高于 ln(27)≈3.30 的均匀基线; 2000 步后应显著下降
    assert full < initial * 0.5, f"训练后 {full} 未显著低于初始 {initial}"
    assert full < 3.0, f"训练后 {full} 应明显低于均匀分布基线 3.30"
    assert isinstance(final, float)
