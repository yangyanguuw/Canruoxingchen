import math

def f1(x):
    return math.e**x-5*x

def df1(x):
    return math.e**x-5

def f(x):
    return x**3-12*x-20

def df(x):
    return 3*x**2-12
def third(x1,x2,derta):

    keys = ["k", "x1", "x2", "f(x1)", "f(x2)", "df(x1)", "df(x2)", "xbar", "f(xbar)", "df(xbar)"]
    for key in keys:
        print('%-8s' % key, end="  ")
    print()
    f1=f(x1)
    f2=f(x2)
    df1=df(x1)
    df2=df(x2)
    k=0

    if(x1>=x2 or df1>=0 or df2<=0):
        return
    else:
        while 1:
            s=3*(f2-f1)/(x2-x1)
            z=s-df1-df2
            w=z**2-df1*df2
            w=math.sqrt(w)

            #求x一拔
            xbar=df2+w+z
            xbar=xbar/(df2-df1+2*w)
            xbar=1-xbar
            xbar=(x2-x1)*xbar+x1

            fbar=f(xbar)
            dfbar=df(xbar)

            values = [k,x1,x2,f1,f2,df1,df2,xbar,fbar,dfbar]
            for value in values:
                if isinstance(value, (int)):
                    print('%-8s' % value, end="  ")
                elif value<0:
                    print("{:.5f}".format(value), end="  ")
                else:
                    print("{:.5f}".format(value), end="   ")
            print()

            if abs(x2 - x1) < derta or dfbar==0:
                return xbar
            elif dfbar<0:
                x1=xbar
                f1=fbar
                df1=dfbar
                k+=1
            else:
                x2=xbar
                f2=fbar
                df2=dfbar
                k+=1

point=third(0,5,0.001)
print("f(x)的最小值点：",point)