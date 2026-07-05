# B2 — makemore：bigram 字符级语言模型

**视频**：The spelled-out intro to language modeling: building makemore

## 你要造的东西

一个只看"前一个字符"预测"下一个字符"的语言模型：统计计数 → 归一化成概率 →
用负对数似然评估 → 从模型中采样生成新名字。

数据集用仓库根目录的 `names.txt`（32,033 个英文名）。

## 任务

填活 `bigram.py`，不看原码。

```bash
pytest b2_bigram/ -v
```

## 验收标准（全绿之外）

能向 Claude 口头解释：
1. 为什么用负对数似然而不是直接用似然连乘？
2. 平滑（smoothing）解决什么问题？平滑系数取无穷大时模型退化成什么？
3. 这个计数模型和"用梯度下降训一个 27→27 的单层网络"为什么殊途同归？
