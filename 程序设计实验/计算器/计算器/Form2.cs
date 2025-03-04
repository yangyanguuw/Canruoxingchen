using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml.Schema;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;


namespace 计算器
{
    
    public partial class Form2 : Form
    {      
        public Form2()
        {  
            InitializeComponent();
        }
        Stack<char> tmp = new Stack<char>();   //储存后缀表达式的栈
        Stack<char> sml = new Stack<char>();   //储存符号的栈
        Stack<double> dgt = new Stack<double>();   //储存数的栈
        Stack<char> temp = new Stack<char>();   //转化栈， 将字符串转化为数值
        double[] num = new double[1000];
        int cnt = 0;
        bool flag = false;
        public int getprior(char ch)
        {
            if (ch == '-' || ch == '+')
                return 2;
            else if (ch == '*' || ch == '/' || ch == '%')
                return 3;
            else if (ch == '^')
                return 4;
            else if (ch == '(')
                return 5;
            else if (ch == ')')
                return 1;
            else return 0;
        }
        public void getnum(bool x)
        {
            double ans = 0;
            double t = 0;
            int counted = 0;   //计算小数点后有几位
            int index = 0;     //整数部分的下标
            while (temp.Count != 0)
            {
                if (x)    //如果有小数点
                {
                    while (temp.Peek() != '.')
                    {
                        int ij = temp.Peek() - '0';
                        t = t + ij * Math.Pow(10, counted);
                        counted++;
                        temp.Pop();
                    }
                    temp.Pop();   //将小数点出栈
                    t = t * Math.Pow(10, -counted);
                    flag = false;   //小数点已出栈
                }
                int i = temp.Peek() - '0';
                ans = ans + i * Math.Pow(10, index);
                index++;
                temp.Pop();
            }
            ans += t;   //将小数部分和整数部分相加
            num[cnt] = ans;
        }
        public void change(string exp)
        {
            int len = exp.Length;
            for (int i = 0; i < len; i++)
            {
                if (char.IsDigit(exp[i]) || exp[i] == '.')
                {
                    if (exp[i] == '.')
                        flag = true;
                    temp.Push(exp[i]);
                }
                else
                {
                    if (temp.Count != 0)
                    {
                        cnt++;
                        getnum(flag);
                        char t = '1';  //标记是数字
                        tmp.Push(t);
                    }
                    if (sml.Count == 0 || exp[i] == '(')
                        sml.Push(exp[i]);
                    else
                    {
                        if (exp[i] == ')')
                        {
                            while (sml.Peek() != '(')
                            {
                                char ch = sml.Peek();
                                tmp.Push(ch);
                                sml.Pop();
                            }
                            sml.Pop();   //将'('出栈
                        }
                        else
                        {
                            char ch = sml.Peek();
                            while (getprior(ch) >= getprior(exp[i]) && ch != '(')  //如果栈顶符号的优先级大于这个符号，则压入后缀栈，等于因为在前面也压入后缀栈
                            {
                                tmp.Push(ch);
                                sml.Pop();
                                if (sml.Count != 0) ch = sml.Peek();
                                else break;
                            }
                            sml.Push(exp[i]);
                        }
                    }
                }
            }
            if (temp.Count != 0)
            {
                cnt++;
                getnum(flag);
                char t = '1';
                tmp.Push(t);
            }
            while (sml.Count != 0)
            {
                char c = sml.Peek();
                tmp.Push(c);
                sml.Pop();
            }
        }
        public double getvalue()
        {
            Stack<char> s = new Stack<char>();
            while (tmp.Count != 0)
            {
                char c = tmp.Peek();
                s.Push(c);
                tmp.Pop();
            }
            int index = 1;
            while (s.Count != 0)
            {
                char c = s.Peek();
                if (char.IsDigit(c))
                {
                    dgt.Push(num[index]);
                    index++;
                    s.Pop();
                }
                else
                {
                    double num2 = dgt.Peek();
                    dgt.Pop();
                    double num1 = dgt.Peek();  //取出数值栈中的值
                    dgt.Pop();
                    cal(num1, num2, c);
                    s.Pop();   //将符号出栈
                }
            }
            return dgt.Peek();
        }
        public void cal(double num1, double num2, char op)
        {
            switch (op)
            {
                case '+': dgt.Push(num1 + num2); break;
                case '-': dgt.Push(num1 - num2); break;
                case '*': dgt.Push(num1 * num2); break;
                case '/': dgt.Push(num1 / num2); break;
                case '%': dgt.Push((int)num1 % (int)num2); break;
                case '^': dgt.Push(Math.Pow((int)num1, (int)num2)); break;
            }
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void button24_Click(object sender, EventArgs e)
        {
            textBox1.Text += "1";
        }

        private void button6_Click(object sender, EventArgs e)
        {
            textBox1.Text += "6";
        }


        private void button19_Click(object sender, EventArgs e)
        {
            textBox1.Text += ")";
        }

        private void button18_Click(object sender, EventArgs e)
        {
            if (textBox1.Text != "")
                textBox1.Text = textBox1.Text.Substring(0, textBox1.Text.Length - 1);
        }

        private void button16_Click(object sender, EventArgs e)
        {
            if(textBox1.Text!="")
                textBox1.Text += ".";
            else
                textBox1.Text += "0.";
        }

        private void button17_Click(object sender, EventArgs e)
        {
            textBox1.Clear();
            sml.Clear();
            tmp.Clear();
            dgt.Clear();
            temp.Clear();
            cnt = 0;
            flag = false;
        }

        private void button15_Click(object sender, EventArgs e)
        {
            string b;
            b= textBox1.Text;
            change(b);
            double result=getvalue();
            textBox1.Text = Convert.ToString(result);
            sml.Clear();
            tmp.Clear();
            dgt.Clear();
            temp.Clear();
            cnt = 0;
            flag = false;
        }

        private void button14_Click(object sender, EventArgs e)
        {
            textBox1.Text += "/";
        }

        private void button13_Click(object sender, EventArgs e)
        {
            textBox1.Text += "*";
        }

        private void button10_Click(object sender, EventArgs e)
        {
            textBox1.Text += "0";
        }

        private void button11_Click(object sender, EventArgs e)
        {
            textBox1.Text += "+";
        }

        private void button12_Click(object sender, EventArgs e)
        {
            textBox1.Text += "-";
        }

        private void button9_Click(object sender, EventArgs e)
        {
            textBox1.Text += "9";
        }

        private void button8_Click(object sender, EventArgs e)
        {
            textBox1.Text += "8";
        }

        private void button7_Click(object sender, EventArgs e)
        {
            textBox1.Text += "7";
        }

        private void button22_Click(object sender, EventArgs e)
        {
            textBox1.Text += "(";
        }

        private void button5_Click(object sender, EventArgs e)
        {
            textBox1.Text += "5";
        }

        private void button4_Click(object sender, EventArgs e)
        {
            textBox1.Text += "4";
        }

        private void button3_Click(object sender, EventArgs e)
        {
            textBox1.Text += "3";
        }

        private void button2_Click(object sender, EventArgs e)
        {
            textBox1.Text += "2";
        }
        private void Form_KeyDown(object sender, KeyEventArgs e)
        {
            switch (e.KeyCode)
            {
                case Keys.NumPad0:
                    {
                        button10_Click(sender, e);
                        break;
                    }
                case Keys.NumPad1:
                    {
                        button24_Click(sender, e);
                        break;
                    }
                case Keys.NumPad2:
                    {
                        button2_Click(sender, e);
                        break;
                    }
                case Keys.NumPad3:
                    {
                        button3_Click(sender, e);
                        break;
                    }
                case Keys.NumPad4:
                    {
                        button4_Click(sender, e);
                        break;
                    }
                case Keys.NumPad5:
                    {
                        button5_Click(sender, e);
                        break;
                    }
                case Keys.NumPad6:
                    {
                        button6_Click(sender, e);
                        break;
                    }
                case Keys.NumPad7:
                    {
                        button7_Click(sender, e);
                        break;
                    }
                case Keys.NumPad8:
                    {
                        button8_Click(sender, e);
                        break;
                    }
                case Keys.NumPad9:
                    {
                        button9_Click(sender, e);
                        break;
                    }
                case Keys.Add:
                    {
                        button11_Click(sender, e);
                        break;
                    }
                case Keys.Subtract:
                    {
                        button12_Click(sender, e);
                        break;
                    }
                case Keys.Multiply:
                    {
                        button13_Click(sender, e);
                        break;
                    }
                case Keys.Divide:
                    {
                        button14_Click(sender, e);
                        break;
                    }

                case Keys.Decimal:
                    {
                        button19_Click(sender, e);
                        break;
                    }
                case Keys.Back:
                    {
                        button18_Click(sender, e);
                        break;
                    }
            }
        }

        private void button23_Click(object sender, EventArgs e)
        {
            Hide();
            Form1 form1 = new Form1();
            form1.ShowDialog();
            this.Close();
        }

        private void button20_Click_1(object sender, EventArgs e)
        {
            Hide();
            Form3 form3 = new Form3();
            form3.ShowDialog();
            this.Close();
        }
    }
}
