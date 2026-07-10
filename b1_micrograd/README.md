# B1 — micrograd：自动求导引擎

**视频**：The spelled-out intro to neural networks and backpropagation: building micrograd

## 你要造的东西

一个约 100 行的标量自动求导引擎：`Value` 类。它能构建计算图，
并通过 `backward()` 自动算出每个节点的梯度——这就是 PyTorch `loss.backward()` 的最小本质。

## 任务

填活 `micrograd.py` 里所有 `raise NotImplementedError` 的地方，不看 Karpathy 的原码。

```bash
pytest b1_micrograd/ -v
```

## 验收标准（全绿之外）

能向 Claude 口头解释：
1. 为什么 `backward()` 必须按拓扑序反向遍历？
2. 为什么梯度是 `+=` 累加而不是 `=` 赋值？什么情况下两者结果不同？
3. `tanh` 的局部导数是什么，链式法则在代码里体现在哪一行？
