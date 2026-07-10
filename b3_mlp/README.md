# B3 — makemore Part 2：MLP 语言模型

**视频**：Building makemore Part 2: MLP（复现 Bengio et al. 2003）

## 你要造的东西

用前 `block_size` 个字符预测下一个字符的神经网络：
字符 embedding → 拼接 → tanh 隐藏层 → 输出 logits → cross entropy。
外加一个**手写的、数值稳定的** cross entropy（不许用 `F.cross_entropy` 实现它）。

## 任务

填活 `mlp.py`，不看原码。

```bash
pytest b3_mlp/ -v
```

## 验收标准（全绿之外）

能向 Claude 口头解释：
1. embedding 查表 `C[X]` 等价于 one-hot 乘矩阵，为什么？哪个快，为什么？
2. 手写 softmax 时为什么要先减去每行的最大值？不减会发生什么？
3. block_size 从 3 改成 8，模型哪些张量的形状会变？参数量增加多少？
