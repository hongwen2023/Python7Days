"""B2 验收测试。"""
import math

import torch

from bigram import load_words, build_vocab, build_counts, counts_to_probs, nll, sample


def tiny_setup():
    words = ["ab", "ba", "aa"]
    stoi, itos = build_vocab(words)
    return words, stoi, itos


def test_load_words_real_dataset():
    words = load_words()
    assert len(words) == 32033
    assert "emma" in words
    assert all(w == w.lower() and w for w in words[:100])


def test_vocab():
    _, stoi, itos = tiny_setup()
    assert len(stoi) == 27 and len(itos) == 27
    assert stoi["."] == 0 and itos[0] == "."
    assert stoi["a"] == 1 and stoi["z"] == 26
    assert itos[stoi["m"]] == "m"


def test_counts_hand_checked():
    words, stoi, itos = tiny_setup()
    N = build_counts(words, stoi)
    assert N.shape == (27, 27)
    a, b, dot = stoi["a"], stoi["b"], stoi["."]
    # ".ab.": .->a, a->b, b->.
    # ".ba.": .->b, b->a, a->.
    # ".aa.": .->a, a->a, a->.
    assert N[dot, a].item() == 2
    assert N[dot, b].item() == 1
    assert N[a, b].item() == 1
    assert N[b, a].item() == 1
    assert N[a, a].item() == 1
    assert N[a, dot].item() == 2
    assert N[b, dot].item() == 1
    assert N.sum().item() == 9  # 3 个名字 x 3 个 bigram


def test_probs_rows_sum_to_one_and_smoothing():
    words, stoi, _ = tiny_setup()
    N = build_counts(words, stoi)
    P = counts_to_probs(N, smoothing=1)
    assert P.shape == (27, 27)
    assert torch.allclose(P.sum(dim=1), torch.ones(27), atol=1e-6)
    assert (P > 0).all(), "平滑后不应有零概率"
    # smoothing=0 时, 没出现过的 bigram 概率为 0
    P0 = counts_to_probs(N, smoothing=0)
    z = stoi["z"]
    assert P0[stoi["a"], z].item() == 0.0


def test_nll_hand_checked():
    words, stoi, _ = tiny_setup()
    N = build_counts(words, stoi)
    P = counts_to_probs(N, smoothing=0)
    # 只用 ["ab"]: bigrams .a, ab, b.
    # P[.,a]=2/3, P[a,b]=1/4, P[b,.]=1/2
    expected = -(math.log(2 / 3) + math.log(1 / 4) + math.log(1 / 2)) / 3
    got = nll(P, ["ab"], stoi)
    assert abs(float(got) - expected) < 1e-6


def test_nll_real_dataset_matches_karpathy():
    words = load_words()
    stoi, itos = build_vocab(words)
    N = build_counts(words, stoi)
    P = counts_to_probs(N, smoothing=1)
    loss = float(nll(P, words, stoi))
    # Karpathy 视频中该模型的 NLL ~ 2.45
    assert 2.40 < loss < 2.50, f"NLL={loss}, 应在 2.45 附近"


def test_sample_deterministic_and_valid():
    words = load_words()
    stoi, itos = build_vocab(words)
    P = counts_to_probs(build_counts(words, stoi), smoothing=1)

    g1 = torch.Generator().manual_seed(2147483647)
    out1 = sample(P, itos, g1, num=5)
    g2 = torch.Generator().manual_seed(2147483647)
    out2 = sample(P, itos, g2, num=5)

    assert out1 == out2, "同种子应产生相同样本"
    assert len(out1) == 5
    letters = set("abcdefghijklmnopqrstuvwxyz")
    for name in out1:
        assert isinstance(name, str)
        assert "." not in name
        assert set(name) <= letters
