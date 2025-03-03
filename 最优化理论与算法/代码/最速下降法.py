import math

import numpy as np
from sympy import *

def fast(x,epsilon):

    #定义函数表达式
    x1,x2=symbols("x1,x2")
    # d1,d2=symbols("d1,d2")
    lam=symbols("lam")
    Y_x=x1**2+x2**2

    #求梯度的表达式
    d1=diff(Y_x,x1)
    d2=diff(Y_x,x2)
    k=1
    print("Y=",Y_x)
    print('%-4s' % "k", end="  ")
    print('%-22s' % "x", end="  ")
    print('%-24s' % "d", end="  ")
    print('%-6s' % "lambda", end="    ")
    print('%-4s' % "df_lambda", end=" \n")

    while 1:

        #求x[0]点的负梯度
        df1=float(-d1.evalf(subs ={'x1':x[0],'x2':x[1]}))
        df2=float(-d2.evalf(subs ={'x1':x[0],'x2':x[1]}))

        #梯度的二范数
        magnitude=np.linalg.norm([df1,df2])

        if(magnitude<=epsilon):#满足精度要求，返回点x,退出循环
            print('%-4s' % k, end="  ")
            print("[", "{:.5f}".format(x[0]), ",", "{:.5f}".format(x[1]), "]", end="  \n")
            return x
            break

        #Y关于λ的函数表达式及导数
        Y_lamb = (x[0]+lam*df1)**2+(x[1]+lam*df2)**2
        df_lamb = diff(Y_lamb, lam)
        #求Y_关于λ导数的零点
        lamb=solve(Eq(df_lamb,0),lam)

        print('%-4s' % k, end="  ")
        print("[","{:.5f}".format(x[0]),",","{:.5f}".format(x[1]),"]", end="   ")
        print("[","{:.5f}".format(df1),",","{:.5f}".format(df2),"]", end="   ")
        print("{:.5f}".format(lamb[0]), end="   ")
        print(df_lamb,end="\n")

        #迭代点x
        x[0]+=lamb[0]*df1
        x[1]+=lamb[0]*df2
        k+=1


print("最优点:",fast([1,1],0.001))
