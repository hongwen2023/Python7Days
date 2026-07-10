"""B1 验收测试。不依赖 torch —— 用有限差分核对你的梯度。"""
import math

from micrograd import Value


def finite_diff(f, args, i, h=1e-6):
    """对第 i 个参数做中心差分, 估计 df/dargs[i]。f 接收 float 列表, 返回 float。"""
    a1 = list(args)
    a2 = list(args)
    a1[i] += h
    a2[i] -= h
    return (f(a1) - f(a2)) / (2 * h)


def test_add_mul_forward():
    a, b, c = Value(2.0), Value(-3.0), Value(10.0)
    out = a * b + c
    assert abs(out.data - 4.0) < 1e-12


def test_add_mul_backward():
    a, b, c = Value(2.0), Value(-3.0), Value(10.0)
    out = a * b + c
    out.backward()
    assert abs(out.grad - 1.0) < 1e-12
    assert abs(a.grad - (-3.0)) < 1e-12
    assert abs(b.grad - 2.0) < 1e-12
    assert abs(c.grad - 1.0) < 1e-12


def test_gradient_accumulation_same_variable():
    # 同一变量使用两次: grad 必须累加而不是被覆盖
    a = Value(3.0)
    out = a + a          # d(out)/da = 2
    out.backward()
    assert abs(a.grad - 2.0) < 1e-12

    b = Value(4.0)
    out2 = b * b + b     # d/db = 2b + 1 = 9
    out2.backward()
    assert abs(b.grad - 9.0) < 1e-12


def test_tanh_and_exp():
    x = Value(0.7)
    y = x.tanh()
    y.backward()
    t = math.tanh(0.7)
    assert abs(y.data - t) < 1e-9
    assert abs(x.grad - (1 - t * t)) < 1e-9

    z = Value(1.3)
    w = z.exp()
    w.backward()
    assert abs(w.data - math.exp(1.3)) < 1e-9
    assert abs(z.grad - math.exp(1.3)) < 1e-9


def test_pow_sub_div_neg():
    a = Value(5.0)
    b = Value(2.0)
    out = (a - b) ** 2 / b - (-a)
    # (5-2)^2/2 + 5 = 9.5
    out.backward()
    assert abs(out.data - 9.5) < 1e-9
    # d/da = 2(a-b)/b + 1 = 4;  d/db = -2(a-b)/b - (a-b)^2/b^2 = -3 - 2.25 = -5.25
    assert abs(a.grad - 4.0) < 1e-9
    assert abs(b.grad - (-5.25)) < 1e-9


def test_radd_rmul_rsub_with_floats():
    a = Value(3.0)
    out = 1.0 + 2.0 * a - 1.0  # = 2a, d/da = 2
    out.backward()
    assert abs(out.data - 6.0) < 1e-9
    assert abs(a.grad - 2.0) < 1e-9


def test_neuron_against_finite_difference():
    # 一个 2 输入神经元: tanh(w1*x1 + w2*x2 + b), 对照有限差分
    vals = [1.5, -0.8, 0.5, 2.0, -1.2]  # w1, w2, b, x1, x2

    def f(v):
        return math.tanh(v[0] * v[3] + v[1] * v[4] + v[2])

    w1, w2, b, x1, x2 = [Value(v) for v in vals]
    out = (w1 * x1 + w2 * x2 + b).tanh()
    out.backward()

    grads = [w1.grad, w2.grad, b.grad, x1.grad, x2.grad]
    for i, g in enumerate(grads):
        num = finite_diff(f, vals, i)
        assert abs(g - num) < 1e-5, f"param {i}: autograd {g} vs numeric {num}"


def test_deep_chain_topological_order():
    # 深链: 若拓扑序错误, 梯度会算错
    x = Value(0.5)
    y = x
    for _ in range(8):
        y = y * x + x    # 反复引用 x, 考验累加 + 拓扑序
    y.backward()

    def f(v):
        out = v[0]
        for _ in range(8):
            out = out * v[0] + v[0]
        return out

    num = finite_diff(f, [0.5], 0)
    assert abs(x.grad - num) < 1e-4, f"autograd {x.grad} vs numeric {num}"
