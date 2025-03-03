import math

#定义f(x)
def f1(x):
    return x**2+2*x

def f(x):
    return math.e**x-5*x

#0.618法，进行一维搜索
def gold(a,b,L):
    lamb=a+0.382*(b-a)
    miu=a+0.618*(b-a)
    k=1
    result1=f(lamb)
    result2=f(miu)

    keys = ["k", "a", "b", "lamb", "miu", "f_labm", "f_miu", "b-a"]
    for key in keys:
        print('%-20s' % key,end=" ")
    print()
    values=[k,a,b,lamb,miu,result1,result2,b-a]
    for value in values:
        print('%-20s' % value,end=" ")
    print()

    while((b-a)>=L):
        if(result1>result2):
            a=lamb
            lamb=miu
            miu=a+0.618*(b-a)
            result1 = result2
            result2=f(miu)
            k+=1
            values = [k, a, b, lamb, miu, result1, result2, b - a]
            for value in values:
                print('%-20s' % value,end=" ")
            print()
        else:
            b=miu
            miu=lamb
            lamb=a+0.382*(b-a)
            result2 = result1
            result1=f(lamb)
            k+=1
            values=[k,a,b,lamb,miu,result1,result2,b-a]
            for value in values:
                print('%-20s' % value,end=" ")
            print()

#[a,b],L
gold(1,2,0.04)
