
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace 计算器
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        static bool flag = true;
        static double x, z = 0;
        static char op = '=';

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void button20_Click(object sender, EventArgs e)
        {
            textBox1.Clear();
            flag = true;
            z = 0;
            x = 0;
        }

        private void button19_Click(object sender, EventArgs e)
        {
            if (textBox1.Text != "")
            {
                textBox1.Text += ".";
            }
            else
            {
                textBox1.Text += "0.";
                flag = false;
            }

        }

        private void button15_Click(object sender, EventArgs e)
        {
            if(textBox1.Text != "")
            x = Convert.ToDouble(textBox1.Text);
            switch (op)
            {
                case '=':
                    {
                        z = x;
                        break;
                    }
                case '+':
                    {
                        z = z + x;
                        break;
                    }
                case '-':
                    {
                        z = z - x;
                        break;
                    }
                case '*':
                    {
                        z = z * x;
                        break;
                    }
                case '/':
                    {
                        z = z / x;
                        break;
                    }
            }
            op = '=';
            textBox1.Text = Convert.ToString(z);
            flag = true;

        }

        private void button14_Click(object sender, EventArgs e)
        {
            if (textBox1.Text != "")
                x = Convert.ToDouble(textBox1.Text);
            switch (op)
            {
                case '=':
                    {
                        z = x;
                        break;
                    }
                case '+':
                    {
                        z = z + x;
                        break;
                    }
                case '-':
                    {
                        z = z - x;
                        break;
                    }
                case '*':
                    {
                        z = z * x;
                        break;
                    }
                case '/':
                    {
                        z = z / x;
                        break;
                    }
            }
            op = '/';
            textBox1.Text = Convert.ToString(z);
            flag = true;
        }

        private void button13_Click(object sender, EventArgs e)
        {
            if (textBox1.Text != "")
                x = Convert.ToDouble(textBox1.Text);
            switch (op)
            {
                case '=':
                    {
                        z = x;
                        break;
                    }
                case '+':
                    {
                        z = z + x;
                        break;
                    }
                case '-':
                    {
                        z = z - x;
                        break;
                    }
                case '*':
                    {
                        z = z * x;
                        break;
                    }
                case '/':
                    {
                        z = z / x;
                        break;
                    }
            }
            op = '*';
            textBox1.Text = Convert.ToString(z);
            flag = true;
        }

        private void button12_Click(object sender, EventArgs e)
        {
            if (textBox1.Text != "")
                x = Convert.ToDouble(textBox1.Text);
            switch (op)
            {
                case '=':
                    {
                        z = x;
                        break;
                    }
                case '+':
                    {
                        z = z + x;
                        break;
                    }
                case '-':
                    {
                        z = z - x;
                        break;
                    }
                case '*':
                    {
                        z = z * x;
                        break;
                    }
                case '/':
                    {
                        z = z / x;
                        break;
                    }
            }
            op = '-';
            textBox1.Text = Convert.ToString(z);
            flag = true;
        }

        private void button11_Click(object sender, EventArgs e)
        {
            if (textBox1.Text != "")
                x = Convert.ToDouble(textBox1.Text);
            switch (op)
            {
                case '=':
                    {
                        z = x;
                        break;
                    }
                case '+':
                    {
                        z = z + x;
                        break;
                    }
                case '-':
                    {
                        z = z - x;
                        break;
                    }
                case '*':
                    {
                        z = z * x;
                        break;
                    }
                case '/':
                    {
                        z = z / x;
                        break;
                    }
            }
            op = '+';
            textBox1.Text = Convert.ToString(z);
            flag = true;
        }

        private void button10_Click(object sender, EventArgs e)
        {
            if (flag)
            {
                textBox1.Clear();
                flag = false;
            }
            textBox1.Text += "0";
        }

        private void button9_Click(object sender, EventArgs e)
        {
            if (flag)
            {
                textBox1.Clear();
                flag = false;
            }
            textBox1.Text += "9";
        }

        private void button8_Click(object sender, EventArgs e)
        {
            if (flag)
            {
                textBox1.Clear();
                flag = false;
            }
            textBox1.Text += "8";
        }

        private void button7_Click(object sender, EventArgs e)
        {
            if (flag)
            {
                textBox1.Clear();
                flag = false;
            }
            textBox1.Text += "7";
        }
        private void button6_Click(object sender, EventArgs e)
        {
            if (flag)
            {
                textBox1.Clear();
                flag = false;
            }
            textBox1.Text += "6";
        }

        private void button5_Click(object sender, EventArgs e)
        {
            if (flag)
            {
                textBox1.Clear();
                flag = false;
            }
            textBox1.Text += "5";
        }

        private void button4_Click(object sender, EventArgs e)
        {
            if (flag)
            {
                textBox1.Clear();
                flag = false;
            }
            textBox1.Text += "4";
        }

        private void button18_Click(object sender, EventArgs e)
        {
            if(textBox1.Text!="")
            textBox1.Text = textBox1.Text.Substring(0, textBox1.Text.Length - 1);
        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (flag)
            {
                textBox1.Clear();
                flag = false;
            }
            textBox1.Text += "3";
        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (flag)
            {
                textBox1.Clear();
                flag = false;
            }
            textBox1.Text += "2";
        }


        private void button1_Click(object sender, EventArgs e)
        {
            if (flag)
            {
                textBox1.Clear();
                flag = false;
            }
            textBox1.Text += "1";
        }

        private void button19_Click_1(object sender, EventArgs e)
        {
            if (textBox1.Text != "")
            {
                x = Convert.ToDouble(textBox1.Text);
                z = Math.Sqrt(x);
                textBox1.Text = Convert.ToString(z);
            }
        }

        private void button22_Click(object sender, EventArgs e)
        {
            if (textBox1.Text != "")
            {
                x = Convert.ToDouble(textBox1.Text);
                z = x * x;
                textBox1.Text = Convert.ToString(z);
            }
        }

        private void button20_Click_1(object sender, EventArgs e)
        {
            if (textBox1.Text != "")
            {
                x = Convert.ToDouble(textBox1.Text);
                z = x*100;
                textBox1.Text = Convert.ToString(z);
                textBox1.Text +="%";
            }
        }

        private void button21_Click(object sender, EventArgs e)
        {
            if (textBox1.Text != "")
            {
                x = Convert.ToDouble(textBox1.Text);
                z = 1/x;
                textBox1.Text = Convert.ToString(z);
           
            }
        }

        private void button23_Click(object sender, EventArgs e)
        {
            Hide();
            Form2 form2 = new Form2();
            form2.ShowDialog();
            this.Close();
        }
        private void button24_Click(object sender, EventArgs e)
        {
            Hide();
            Form3 form3 = new Form3();
            form3.ShowDialog();
            this.Close();
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
                        button1_Click(sender, e);
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
    }
}
