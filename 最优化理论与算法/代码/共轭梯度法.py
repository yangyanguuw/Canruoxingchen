import math

import numpy as np
import sympy
from sympy import *
import mpmath

np.set_printoptions(precision=4)

def fast(A,x0):

    #定义函数表达式
    x1,x2,x3=symbols("x1,x2,x3")
    x=Matrix([x1,x2,x3])
    Y_x=x.T*A*x
    print("Y =",end=' ')
    print(Y_x[0])

    #求梯度的表达式
    d1=diff(Y_x[0],x1)
    d2=diff(Y_x[0],x2)
    d3=diff(Y_x[0],x3)
    Hession = hessian(Y_x, [x1,x2,x3])


    k=1
    keys = ["k", "x", "g_k","d_k", "Beta",  "lambda"]
    for key in keys:
        print('%-18s' % key, end="  ")
    print()
    while 1:

        #求x[0]点的负梯度
        df1=float(d1.evalf(subs ={'x1':x0[0],'x2':x0[1],'x3':x0[2]}))
        df2=float(d2.evalf(subs ={'x1':x0[0],'x2':x0[1],'x3':x0[2]}))
        df3=float(d3.evalf(subs ={'x1':x0[0],'x2':x0[1],'x3':x0[2]}))
        Hession_k=Hession.evalf(subs ={'x1':x0[0],'x2':x0[1],'x3':x0[2]})
        Hession_k = np.array(Hession_k).astype(float)

        g_k=np.array([df1,df2,df3])
        #梯度的二范数
        magnitude=g_k.dot(g_k)**0.5
        if(magnitude<=1e-6 or k>100):#满足精度要求，返回点x,退出循环
            break
        Beta=1
        if k!=1:
            a = d_k.dot(Hession_k).dot(g_k.T)
            b= d_k.dot(Hession_k).dot(d_k.T)
            Beta=a/b
            d_k=-g_k+Beta*d_k
        else:
            d_k=-g_k

        a=g_k.dot(d_k)
        b=d_k.dot(Hession_k)
        b=b.dot(d_k.T)
        lamb=(-a/b)
        values = [k, x0, g_k,d_k, Beta, lamb]
        for value in values:
            if isinstance(value, float):
                print("{:<18.2f}".format(value),end='  ')
            else:
                print('%-18s' % value, end="  ")
        print()

        x0 =x0+lamb * d_k
        k+=1
    return x0
A=np.array([[1,0,0],[0,0.5,0],[0,0,0.5]])
x0=np.array([1.0,1.0,1.0])
print("最优点:",fast(A,x0))
