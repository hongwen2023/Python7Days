# AI 学习环 — Karpathy Zero to Hero 主线

从零手写神经网络到 GPT。每一课的知识以"能通过测试的代码"为凭证，而不是"看过视频"。

## 学习规则

1. **不看原码重写**：看完视频后，关掉 Karpathy 的代码，在骨架文件里独立实现。
2. **测试即验收**：`pytest bN_xxx/` 全绿才算通过这一课。
3. **每课一 commit**：通过后 commit + push，让 Claude review 并出变体题。
4. **卡住 30 分钟以上**：直接问 Claude，说清卡在哪一步、试过什么。

## 路线图

| 目录 | 视频 | 造出什么 | 状态 |
|---|---|---|---|
| `b1_micrograd/` | The spelled-out intro to neural networks and backpropagation | 自动求导引擎 | 🔄 复核中 |
| `b2_bigram/` | The spelled-out intro to language modeling: building makemore | 字符级 bigram 语言模型 | 🔄 复核中 |
| `b3_mlp/` | Building makemore Part 2: MLP | 神经网络语言模型 (Bengio 2003) | 🔄 复核中 |
| `b4_activations_batchnorm/` | makemore Part 3: Activations & Gradients, BatchNorm | 训练诊断能力 | 🔒 |
| `b5_backprop_ninja/` | makemore Part 4: Becoming a Backprop Ninja | 手动反推每层梯度 | 🔒 |
| `b6_wavenet/` | makemore Part 5: Building a WaveNet | 层次化结构 | 🔒 |
| `b7_gpt/` | Let's build GPT: from scratch | Transformer / GPT | 🔒 |
| `b8_tokenizer/` | Let's build the GPT Tokenizer | BPE 分词器 | 🔒 |
| `b9_gpt2/` | Let's reproduce GPT-2 (124M) | 真实规模训练 | 🔒 |

进度明细见 [PROGRESS.md](PROGRESS.md)。

## 环境

```bash
pip install -r requirements.txt
pytest b1_micrograd/          # 跑单课测试
pytest                        # 跑全部
```

`names.txt`（32,033 个英文名，makemore 数据集）已在仓库根目录，b2 起共用。

## 工作流

```
看视频 → 关掉原码 → 填骨架 → pytest 变绿 → commit + push → Claude review → 答变体题 → 下一课
```
