#include<bits/stdc++.h>
using namespace std;
stack<char>tmp;   //�����׺���ʽ��ջ
stack<char>sml;   //������ŵ�ջ
stack<double>dgt;   //��������ջ
stack<char>temp;   //ת��ջ�� ���ַ���ת��Ϊ��ֵ
double num[1000];
int cnt = 0;
bool flag = false;   //�ж������Ƿ���С����ı�־
void getnum(bool &flag);   //���ַ���ת��Ϊ��ֵ�ĺ���
void change(char *exp);     //����׺���ʽת��Ϊ��׺���ʽ�ĺ���
void getvalue();     //�����׺���ʽ�ĺ���
int getprior(char ch);   //��ȡ�������ȼ��ĺ�����
void cal(double num1 , double num2 , char op);   //���㺯��
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
    int counted = 0;   //����С������м�λ
    int index = 0;     //�������ֵ��±�
    while(!temp.empty())
    {
        if(flag)    //�����С����
        {
            while(temp.top() != '.')
            {
                int i = temp.top() - '0';
                t = t + i * pow(10 , counted);
                counted++;
                temp.pop();
            }
            temp.pop();   //��С�����ջ
            t = t * pow(10 , -counted);
            flag = false;   //С�����ѳ�ջ
        }
        int i = temp.top() - '0';
        ans = ans + i * pow(10 , index);
        index++;
        temp.pop();
    }
    ans += t;   //��С�����ֺ������������
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
                char t = '1';  //���������
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
                        sml.pop();   //��'('��ջ
                    }
                    else
                    {
                        char ch = sml.top();
                        while(getprior(ch) >= getprior(exp[i]) && ch != '(')  //���ջ�����ŵ����ȼ�����������ţ���ѹ���׺ջ��������Ϊ��ǰ��Ҳѹ���׺ջ
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
            double num1 = dgt.top();  //ȡ����ֵջ�е�ֵ
            dgt.pop();
            cal(num1 , num2 , c);
            s.pop();   //�����ų�ջ
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
