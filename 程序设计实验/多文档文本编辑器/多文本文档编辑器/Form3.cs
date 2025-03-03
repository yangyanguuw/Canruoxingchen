using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.TextBox;

namespace 多文本文档编辑器
{
    public partial class Form3 : Form
    {
        Form2 parentForm; //定义包含富文本框的窗体变量
        private String strSearch = ""; // 表示要查找的字符串
        private String strReplace = "";// 表示要替换成的字符串
        private int searchPos = 0, lastSearchPos = 0;// 前者表示当前的查找位置，后者表示记录上次的查找位置
        private bool find;

        public Form3(Form2 parent)
        {
            this.parentForm = parent;
            InitializeComponent();
        }

        private bool SearchText()
        {
            strSearch = findText.Text;//查找的文本
            strReplace = replaceText1.Text;//替换的文本
            if (checkCase.Checked)// 表示区分大小写查找
            {
                if (radioDown.Checked) // 表示向下查找
                {
                    this.searchPos = parentForm.rTBDoc.Find(strSearch, searchPos, parentForm.rTBDoc.Text.Length, RichTextBoxFinds.MatchCase);
                }
                else// 表示向上查找
                {
                    this.searchPos = this.parentForm.rTBDoc.Find(this.strSearch, 0, searchPos, RichTextBoxFinds.MatchCase | RichTextBoxFinds.Reverse);
                }
            }
            else// 不区分大小写进行查找
            {
                if (this.radioDown.Checked)// 表示向下查找
                {
                    this.searchPos = this.parentForm.rTBDoc.Find(this.strSearch, searchPos, this.parentForm.rTBDoc.Text.Length, RichTextBoxFinds.None);
                }
                else// 表示向上查找
                {
                    this.searchPos = this.parentForm.rTBDoc.Find(this.strSearch, 0, searchPos, RichTextBoxFinds.Reverse);
                }
            }
            if (this.searchPos < 0)//如果未找到
            {
                this.searchPos = this.lastSearchPos;//回到上次查找位置
                find = false;//表示未找到
            }
            else//找到文本
            {
                var length = this.findText.Text.Trim().Length;// 获取关键字的长度
                this.parentForm.rTBDoc.Focus();// RichTextBox文本框获得焦点
                this.parentForm.rTBDoc.Select(searchPos, length);
                this.lastSearchPos = this.searchPos;//开始查找，把查找位置保存
                if (this.radioDown.Checked)//如果是向下查找，设置新的查找位置，继续向下查找
                {
                    this.searchPos += this.strSearch.Length;//新的查找位置是本次开始的查找位置加上查找到文本的长度
                }
            }
            return find;
        }


        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.strSearch = this.findText.Text;//查找的文本
            this.strReplace = this.replaceText1.Text;//替换的文本
            if (!SearchText())//调用查找方法查找是否存在
            {
                if (this.parentForm.rTBDoc.SelectedText.Length > 0)//如果找到，则进行替换
                {

                    this.parentForm.rTBDoc.SelectedText = this.strReplace;
                }
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            SearchText();
        }

        private void Form3_Load(object sender, EventArgs e)
        {

        }
    }
}
