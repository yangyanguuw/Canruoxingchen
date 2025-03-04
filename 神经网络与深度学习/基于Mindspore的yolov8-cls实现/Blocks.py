import mindspore.nn as nn
import mindspore.ops as ops

def autopad(k, p=None):  # kernel, padding
    """自适应padding"""
    if p is None:
        p = k // 2 if isinstance(k, int) else [x // 2 for x in k]  # auto-pad
    return p


class SiLU(nn.Cell):
    def __init__(self):
        super(SiLU, self).__init__()
        self.sigmoid = ops.Sigmoid()

    def construct(self, x):
        return x * self.sigmoid(x)


class Conv(nn.Cell):
    """CBS：Conv+BatchNorm+SiLU"""

    def __init__(self, c1, c2, k=1, s=1, p=None, g=1, act=True):

        super().__init__()
        self.pad = autopad(k, p)
        self.padmode = None
        if self.pad == 0:
            self.padmode = 'same'
        elif self.pad == 1:
            self.padmode = 'pad'


        self.conv = nn.Conv2d(c1, c2, k, s, padding=self.pad, pad_mode=self.padmode, group=g, has_bias=False)
        self.bn = nn.BatchNorm2d(c2)
        self.act = SiLU() if act is True else (act if isinstance(act, nn.Cell) else ops.Identity())

    def construct(self, x):
        """构造函数，类似torch的forward()"""
        x=self.act(self.bn(self.conv(x)))

        return x


class Bottleneck(nn.Cell):

    def __init__(self, c1, c2, shortcut=True, g=1, k=(3, 3), e=0.5):
        super().__init__()
        c_ = int(c2 * e)  # hidden channels
        self.cv1 = Conv(c1, c_, k[0], 1)
        self.cv2 = Conv(c_, c2, k[1], 1, g=g)
        self.add = shortcut and c1 == c2

    def construct(self, x):
        return x + self.cv2(self.cv1(x)) if self.add else self.cv2(self.cv1(x))


class C2f(nn.Cell):

    def __init__(self, c1, c2, n=1, shortcut=False, g=1, e=0.5):
        super().__init__()
        self.c = int(c2 * e)
        self.cv1 = Conv(c1, 2 * self.c, 1, 1)
        self.cv2 = Conv((2 + n) * self.c, c2, 1)  # optional act=FReLU(c2)
        self.concat=ops.Concat(1)
        self.m = nn.CellList([Bottleneck(self.c, self.c, shortcut, g, k=(3,3), e=1.0) for _ in range(n)])

    def construct(self, x):
        y = list(self.cv1(x).split((self.c, self.c), 1))
        y.extend(m(y[-1]) for m in self.m)
        x= self.cv2(self.concat(y))
        return x


class Classify(nn.Cell):

    def __init__(self, c1, c2, k=1, s=1, p=None, g=1):
        super().__init__()
        c_ = 1280
        self.conv = Conv(c1, c_, k, s, p, g)
        self.flatten=nn.Flatten()
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.drop = nn.Dropout(keep_prob=1.0)
        self.linear = nn.Dense(c_, c2)
        self.expand=ops.ExpandDims()

    def construct(self, x):
        x=self.conv(x)
        x=self.pool(x)
        x=self.flatten(x)
        x=self.drop(x)
        x = self.linear(x)
        return x #if self.training else x.softmax(1)
