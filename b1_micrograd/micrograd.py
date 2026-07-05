"""micrograd: 标量自动求导引擎（骨架）。

填活所有 raise NotImplementedError 的地方。
约定:
- Value.data: float, 前向值
- Value.grad: float, dL/d(self), 初始为 0.0
- 每个运算返回新的 Value, 并在其 _backward 闭包里写好局部链式法则
- Value.backward() 从 self 出发做拓扑排序, 然后反向调用各节点的 _backward
"""
import math


class Value:
    def __init__(self, data, _children=(), _op=""):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"

    def __add__(self, other):
        """self + other。other 可能是 int/float，需要包装成 Value。"""
        raise NotImplementedError

    def __mul__(self, other):
        """self * other。"""
        raise NotImplementedError

    def __pow__(self, other):
        """self ** other，other 仅支持 int/float 常数。"""
        raise NotImplementedError

    def tanh(self):
        """双曲正切。提示: t = tanh(x) 的导数是 1 - t**2。"""
        raise NotImplementedError

    def exp(self):
        """e 的 self 次方。"""
        raise NotImplementedError

    def backward(self):
        """反向传播: 拓扑排序整个计算图, self.grad = 1.0, 反向逐节点调用 _backward。"""
        raise NotImplementedError

    # ---- 以下由上面的核心运算组合而来 ----

    def __neg__(self):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __truediv__(self, other):
        raise NotImplementedError

    def __radd__(self, other):  # other + self
        raise NotImplementedError

    def __rmul__(self, other):  # other * self
        raise NotImplementedError

    def __rsub__(self, other):  # other - self
        raise NotImplementedError
