# 进度追踪

## 能力雷达（五层框架）

> 规则：状态只由**已发生的验收事件**填写（测试全绿、口试通过、论文拆解完成），
> 不填自我感觉的百分比。空 = 尚无证据。

| 层级 | 定义 | 验收证据 | 状态 |
|---|---|---|---|
| L1 数学基础 | 能推公式：梯度下降、backprop、MLE、cross entropy、attention | 18.06 关键课完成 + B5 通过 + 口试 | |
| L2 ML 理论 | 能从第一性原理解释：正则化、偏差-方差、生成 vs 判别 | CS229 关键节点 + 口试 | |
| L3 从零实现 | 不看原码写出 MLP / Transformer / GPT / Tokenizer | B1-B8 测试全绿 + review 通过 | |
| L4 论文研究 | 读懂架构与公式、找出创新点、评估局限 | 论文线每篇的拆解笔记 | |
| L5 AI 工程 | 训练/推理/部署/agent 编排 | B9 + nanochat + 实际项目 | |

## B 线：Zero to Hero

- [ ] **B1 micrograd** — 复核：不看原码填活 `b1_micrograd/micrograd.py`，测试全绿
  - [ ] Value 四则运算与 tanh/exp
  - [ ] backward() 拓扑排序反向传播
  - [ ] 梯度累加（同一变量多次使用）
- [ ] **B2 bigram** — 复核：填活 `b2_bigram/bigram.py`，测试全绿
  - [ ] 计数矩阵 + 平滑
  - [ ] 负对数似然 ≈ 2.45
  - [ ] 采样生成名字
- [ ] **B3 MLP** — 复核：填活 `b3_mlp/mlp.py`，测试全绿
  - [ ] 滑动窗口数据集构造
  - [ ] embedding + 隐藏层前向
  - [ ] 手写数值稳定的 cross entropy
  - [ ] 训练 loss 下降
- [ ] **B4 Activations & BatchNorm**
- [ ] **B5 Backprop Ninja** ⭐ 试金石
- [ ] **B6 WaveNet**
- [ ] **B7 Let's build GPT** ⭐ 试金石
- [ ] **B8 Tokenizer**
- [ ] **B9 Reproduce GPT-2**

## 论文阅读线（B7 通过后解锁 🔒）

> 手写过 attention 之后读原论文是"验证已知"，之前读是"啃天书"。所以锁在 B7 后面。
> 每篇的验收：一页拆解笔记（架构图自己画、关键公式自己推、创新点与局限各列 2-3 条），
> commit 到 `papers/` 目录，Claude review + 口试。

- [ ] 1. Attention Is All You Need (2017) — 对照自己写的 B7 代码逐节验证
- [ ] 2. BERT (2018) — encoder 路线与双向预训练
- [ ] 3. LoRA (2021) — 低秩适配，正好用上 18.06 的秩与 SVD 直觉
- [ ] 4. FlashAttention (2022) — 从算法到硬件，衔接 L5 工程线

## 并行线

- [ ] 18.06 第 14-17 课（投影/最小二乘）— B5 前完成
- [ ] 18.06 第 21-22 课（特征值）
- [ ] 18.06 第 25-27 课（对称矩阵/正定性）
- [ ] 18.06 第 29 课（SVD）
- [ ] CS229 全速推进（概率按需唤醒）

## 错题与弱点记录

> Claude review 时发现的薄弱点记在这里，作为复习队列。

（暂无）
