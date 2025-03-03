using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.Button;

namespace 计算器
{
    
    public partial class Form3 : Form
    {
        
        public Form3()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            double yuejun, lizong, huanzong;
            double nianxian, jine, lilv;
            nianxian  = Convert.ToDouble(textBox1.Text)*12;
            jine = Convert.ToDouble(textBox2.Text) * 10000;
            lilv=Convert.ToDouble(textBox3.Text)/100;
            if(radioButton2.Checked)
            {
                double gg;
                gg = Math.Pow(lilv + 1, nianxian);
                yuejun = (jine * lilv *gg)/(gg-1);
                huanzong = yuejun * nianxian;
                lizong = huanzong - jine;
                textBox4.Text = Convert.ToString(yuejun);
                textBox5.Text = Convert.ToString(lizong);
                textBox6.Text = Convert.ToString(huanzong);
                textBox7.Text = Convert.ToString(yuejun);
                textBox8.Text = "0";
            }
            if (radioButton1.Checked)
            { 
                double jianmian=0;
                double shouyue;
                shouyue=jine* lilv +jine / nianxian;
                for (int i=1;i<nianxian;i++)
                {
                    jianmian+=i;
                }
                jianmian = jianmian * jine / nianxian * lilv;
                huanzong = shouyue*nianxian-jianmian;
                lizong = huanzong - jine;
                textBox4.Text = "***";
                textBox5.Text = Convert.ToString(lizong);
                textBox6.Text = Convert.ToString(huanzong);
                textBox7.Text = Convert.ToString(shouyue);
                textBox8.Text = Convert.ToString(jine/nianxian*lilv);

            }
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void textBox7_TextChanged(object sender, EventArgs e)
        {

        }

        private void button23_Click(object sender, EventArgs e)
        {
            Hide();
            Form1 form1 = new Form1();
            form1.ShowDialog();
            this.Close();
        }

        private void button20_Click(object sender, EventArgs e)
        {
            Hide();
            Form2 form2 = new Form2();
            form2.ShowDialog();
            this.Close();
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
                textBox1.Clear();
                textBox2.Clear();
                textBox3.Clear();
                textBox4.Clear();
                textBox5.Clear();
                textBox6.Clear();
                textBox7.Clear();
                textBox8.Clear();  
        }

        private void Form3_Load(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
