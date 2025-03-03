import numpy as np
def gfun1(x):  # 梯度
    return np.array([4 * (x[0] - 2) ** 3 + 2 * (x[0] - 2 * x[1]), -4 * (x[0] - 2 * x[1])]).reshape(len(x), 1)

def fun1(x):  # 函数
    return (x[0] - 2) ** 4 + (x[0] - 2 * x[1]) ** 2

def fun(x):
    return x[0] ** 2 + 2*x[1] ** 2

def gfun(x):
    return np.array([2 * x[0],4 * x[1]]).reshape(len(x), 1)

def dfp(x0):
    maxk = 5000
    rho = .55
    sigma = .4
    epsilon = 1e-5
    k = 0
    n = len(x0)
    Hk = np.eye(n)
    while k < maxk:
        gk = gfun(x0)
        if np.linalg.norm(gk) < epsilon:
            break
        dk = -Hk @ gk
        m = 0
        mk = 0
        while m < 20:  # 使用Armijo搜索（非精确线搜索）
            if fun(x0 + rho ** m * dk) < fun(x0) + sigma * rho ** m * gk.T @ dk:
                mk = m
                break
            m += 1
        x = x0 + rho ** mk * dk
        sk = x - x0
        yk = gfun(x) - gk
        if sk.T @ yk > 0:
            Hk = Hk - (Hk @ yk @ yk.T @ Hk) / (yk.T @ Hk @ yk) + (sk @ sk.T) / (sk.T @ yk)
        k += 1
        x0 = x
    return x0, fun(x0), k


if __name__ == '__main__':
    x0 = np.array([[0], [0]])
    x0, val, k = dfp(x0)
    print(f'近似最优点：\n{x0}\n迭代次数：{k}\n目标函数值：{val.item()}')

