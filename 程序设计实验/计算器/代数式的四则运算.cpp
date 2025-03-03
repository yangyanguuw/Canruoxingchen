#include<bits/stdc++.h>
using namespace std;
stack<char>tmp;   //储存后缀表达式的栈
stack<char>sml;   //储存符号的栈
stack<double>dgt;   //储存数的栈
stack<char>temp;   //转化栈， 将字符串转化为数值
double num[1000];
int cnt = 0;
bool flag = false;   //判断数中是否有小数点的标志
void getnum(bool &flag);   //将字符串转化为数值的函数
void change(char *exp);     //将中缀表达式转化为后缀表达式的函数
void getvalue();     //计算后缀表达式的函数
int getprior(char ch);   //获取符号优先级的函数；
void cal(double num1 , double num2 , char op);   //计算函数
int main()
{
    char exp[100];
    cin>>exp;
     change(exp);
    getvalue();
    return 0;   //12.2*(15.4+5*2^3)*12.3+4+5%6+10*12.2
}
int getprior(char ch)
{
    if(ch == '-' || ch == '+')
        return 2;
    else if(ch == '*' || ch == '/' || ch == '%')
        return 3;
    else if(ch == '^')
        return 4;
    else if(ch == '(')
        return 5;
    else if(ch == ')')
        return 1;
}
void getnum(bool &flag)
{
    double ans = 0;
    double t = 0;
    int counted = 0;   //计算小数点后有几位
    int index = 0;     //整数部分的下标
    while(!temp.empty())
    {
        if(flag)    //如果有小数点
        {
            while(temp.top() != '.')
            {
                int i = temp.top() - '0';
                t = t + i * pow(10 , counted);
                counted++;
                temp.pop();
            }
            temp.pop();   //将小数点出栈
            t = t * pow(10 , -counted);
            flag = false;   //小数点已出栈
        }
        int i = temp.top() - '0';
        ans = ans + i * pow(10 , index);
        index++;
        temp.pop();
    }
    ans += t;   //将小数部分和整数部分相加
    num[cnt] = ans;
}
void change(char *exp)
{
    int len = strlen(exp);
    for(int i = 0 ; i < len ; i++)
    {
        if(isdigit(exp[i]) || exp[i] == '.')
        {
            if(exp[i] == '.')
                flag = true;
            temp.push(exp[i]);
        }
        else
        {
            if(!temp.empty())
            {
                cnt++;
                getnum(flag);
                char t = '1';  //标记是数字
                tmp.push(t);
            }
                if(sml.empty() || exp[i] == '(')
                    sml.push(exp[i]);
                else
                {
                    if(exp[i] == ')')
                    {
                        while(sml.top() != '(')
                        {
                            char ch = sml.top();
                            tmp.push(ch);
                            sml.pop();
                        }
                        sml.pop();   //将'('出栈
                    }
                    else
                    {
                        char ch = sml.top();
                        while(getprior(ch) >= getprior(exp[i]) && ch != '(')  //如果栈顶符号的优先级大于这个符号，则压入后缀栈，等于因为在前面也压入后缀栈
                        {
                            tmp.push(ch);
                            sml.pop();
                            if(!sml.empty()) ch = sml.top();
                            else break;
                        }
                        sml.push(exp[i]);
                    }
                }
        }
    }
                if(!temp.empty())
                {
                    cnt++;
                    getnum(flag);
                    char t = '1';
                    tmp.push(t);
                }
                while(!sml.empty())
                {
                    char c = sml.top();
                    tmp.push(c);
                    sml.pop();
                }
}
void getvalue()
{
    stack<char>s;
    while(!tmp.empty())
    {
        char c = tmp.top();
        s.push(c);
        tmp.pop();
    }
    int index = 1;
    while(!s.empty())
    {
        char c = s.top();
        if(isdigit(c))
        {
            dgt.push(num[index]);
            index++;
            s.pop();
        }
        else
        {
            double num2 = dgt.top();
            dgt.pop();
            double num1 = dgt.top();  //取出数值栈中的值
            dgt.pop();
            cal(num1 , num2 , c);
            s.pop();   //将符号出栈
        }
    }
    cout<<dgt.top();
}
void cal(double num1 , double num2  , char op)
{
    switch (op)
    {
        case '+' : dgt.push(num1 + num2);break;
        case '-' : dgt.push(num1 - num2);break;
        case '*' : dgt.push(num1 * num2);break;
        case '/' : dgt.push(num1 / num2);break;
        case '%' : dgt.push( (int)num1 % (int)num2);break;
        case '^' : dgt.push(pow((int)num1 , (int)num2));break;
    }
} 
