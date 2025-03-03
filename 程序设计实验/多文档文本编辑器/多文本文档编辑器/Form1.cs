using System.Drawing.Text;

namespace 多文本文档编辑器
{
    public partial class Form1 : Form
    {
        private int _num = 1;
        string lujin = "untitle";
        public Form1()
        {
            InitializeComponent();
        }

        private void ChangeRTBFontStyle(RichTextBox rtb, FontStyle style)
        {
            if (style != FontStyle.Bold && style != FontStyle.Italic && style != FontStyle.Underline && style != FontStyle.Strikeout)
                throw new System.InvalidProgramException("字体格式错误");
            RichTextBox tempRTB = new RichTextBox();//保存选中文本的副本
            int curRtbStart = rtb.SelectionStart;//记录选取文本起始位置
            int len = rtb.SelectionLength;//记录选取文本长度
            int tempRtbStart = 0;
            Font font = rtb.SelectionFont;//记录当前字体
            if (len <= 0 && font != null)//若未选中文本
            {
                if (style == FontStyle.Bold && font.Bold || style == FontStyle.Italic && font.Italic || style == FontStyle.Underline && font.Underline || style == FontStyle.Strikeout && font.Strikeout)
                    rtb.SelectionFont = new Font(tSCbBoxFontName.Text, Convert.ToSingle(ziti.Text), font.Style ^ style);
                else if (style == FontStyle.Bold && !font.Bold || style == FontStyle.Italic && !font.Italic || style == FontStyle.Underline && !font.Underline || style == FontStyle.Strikeout && !font.Strikeout)
                    rtb.SelectionFont = new Font(tSCbBoxFontName.Text, Convert.ToSingle(ziti.Text), font.Style | style);
                return;
            }
            tempRTB.Rtf = rtb.SelectedRtf;
            tempRTB.Select(len - 1, 1);
            Font tempFont = (Font)tempRTB.SelectionFont.Clone();
            for (int i = 0; i < len; i++)//若选中文本
            {
                tempRTB.Select(tempRtbStart + i, 1);
                if (style == FontStyle.Bold && tempFont.Bold || style == FontStyle.Italic && tempFont.Italic || style == FontStyle.Strikeout && tempFont.Strikeout || style == FontStyle.Underline && tempFont.Underline)
                    tempRTB.SelectionFont = new Font(tempRTB.SelectionFont, tempRTB.SelectionFont.Style ^ style);
                else if (style == FontStyle.Bold && !tempFont.Bold || style == FontStyle.Italic && !tempFont.Italic || style == FontStyle.Underline && !tempFont.Underline || style == FontStyle.Strikeout && !tempFont.Strikeout)
                    tempRTB.SelectionFont = new Font(tempRTB.SelectionFont, tempRTB.SelectionFont.Style | style);
            }
            tempRTB.Select(tempRtbStart, len);
            rtb.SelectedRtf = tempRTB.SelectedRtf;
            rtb.Select(curRtbStart, len);
            rtb.Focus();
            tempRTB.Dispose();
        }
        private void 文件ToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {
            //目的为获取系统所有字体，并将字体名称显示在下拉框中
            tSCbBoxFontName.Items.Clear(); //清空下拉框
            InstalledFontCollection ifc = new InstalledFontCollection();//获取系统的所有字体
            FontFamily[] ffs = ifc.Families;
            foreach (FontFamily ff in ffs)//将获取的字体放入下拉框
                tSCbBoxFontName.Items.Add(ff.GetName(1));
            LayoutMdi(MdiLayout.Cascade);
            WindowState = FormWindowState.Maximized;
        }

        private void tSCbBoxFontName_Click(object sender, EventArgs e)
        {
            RichTextBox tempRTB = new RichTextBox();//保存富文本副本
            int RtbStart = ((Form2)this.ActiveMdiChild).rTBDoc.SelectionStart;//获取选中文本起始位置
            int len = ((Form2)this.ActiveMdiChild).rTBDoc.SelectionLength;//获取选中文本长度
            int tempRtbStart = 0;
            Font font = ((Form2)this.ActiveMdiChild).rTBDoc.SelectionFont;//记录当前字体
            if (len <= 0 && null != font)//若未选中文本
            {
                ((Form2)this.ActiveMdiChild).rTBDoc.SelectionFont = new Font(tSCbBoxFontName.Text,
                Convert.ToSingle(ziti.Text), tempRTB.SelectionFont.Style);
                return;
            }
            tempRTB.Rtf = ((Form2)this.ActiveMdiChild).rTBDoc.SelectedRtf;
            for (int i = 0; i < len; i++)//若选中文本
            {
                tempRTB.Select(tempRtbStart + i, 1);
                tempRTB.SelectionFont = new Font(tSCbBoxFontName.Text, Convert.ToSingle(ziti.Text), tempRTB.SelectionFont.Style);
            }
            tempRTB.Select(tempRtbStart, len);
            ((Form2)this.ActiveMdiChild).rTBDoc.SelectedRtf = tempRTB.SelectedRtf;
            ((Form2)this.ActiveMdiChild).rTBDoc.Select(RtbStart, len);
            ((Form2)this.ActiveMdiChild).rTBDoc.Focus();
            tempRTB.Dispose();//释放
        }

        private void ziti_Click(object sender, EventArgs e)
        {
            //该部分代码与上一个类似，相关注释就不再赘述
            if (this.MdiChildren.Count() > 0)
            {
                RichTextBox tempRTB = new RichTextBox();
                int RtbStart = ((Form2)this.ActiveMdiChild).rTBDoc.SelectionStart;
                int len = ((Form2)this.ActiveMdiChild).rTBDoc.SelectionLength;
                int tempRtbStart = 0;
                if (len <= 0)
                {
                    ((Form2)this.ActiveMdiChild).rTBDoc.SelectionFont = new Font(tSCbBoxFontName.Text, Convert.ToSingle(ziti.Text), tempRTB.SelectionFont.Style);
                    return;
                }
                tempRTB.Rtf = ((Form2)this.ActiveMdiChild).rTBDoc.SelectedRtf;


                for (int i = 0; i < len; i++)
                {
                    tempRTB.Select(tempRtbStart + i, 1);
                    tempRTB.SelectionFont = new Font(tSCbBoxFontName.Text, Convert.ToSingle(ziti.Text), tempRTB.SelectionFont.Style);
                }
                tempRTB.Select(tempRtbStart, len);
                ((Form2)this.ActiveMdiChild).rTBDoc.SelectedRtf = tempRTB.SelectedRtf;
                ((Form2)this.ActiveMdiChild).rTBDoc.Select(RtbStart, len);
                ((Form2)this.ActiveMdiChild).rTBDoc.Focus();
                tempRTB.Dispose();
            }
        }

        private void toolStripButton12_Click(object sender, EventArgs e)
        {
            ColorDialog ColorDlg = new ColorDialog();
            //禁止使用自定义颜色
            ColorDlg.AllowFullOpen = false;
            //提供自己给定的颜色
            ColorDlg.CustomColors = new int[] { 6916092, 15195440, 16107657, 1836924, 3758726, 12566463, 7526079, 7405793, 6945974, 241502, 2296476, 5130294, 3102017, 7324121, 14993507, 11730944 };//设置颜色
            ColorDlg.ShowHelp = true;
            ColorDlg.ShowDialog();//打开颜色选择窗口
            if (this.MdiChildren.Count() > 0)
            {
                RichTextBox tempRTB = new RichTextBox();
                int RtbStart = ((Form2)this.ActiveMdiChild).rTBDoc.SelectionStart;
                int len = ((Form2)this.ActiveMdiChild).rTBDoc.SelectionLength;
                int tempRtbStart = 0;
                if (len <= 0)
                {
                    ((Form2)this.ActiveMdiChild).rTBDoc.SelectionColor = ColorDlg.Color;
                    return;
                }
                tempRTB.Rtf = ((Form2)this.ActiveMdiChild).rTBDoc.SelectedRtf;


                for (int i = 0; i < len; i++)
                {
                    tempRTB.Select(tempRtbStart + i, 1);
                    tempRTB.SelectionColor = ColorDlg.Color;
                }
                tempRTB.Select(tempRtbStart, len);
                ((Form2)this.ActiveMdiChild).rTBDoc.SelectedRtf = tempRTB.SelectedRtf;
                ((Form2)this.ActiveMdiChild).rTBDoc.Select(RtbStart, len);
                ((Form2)this.ActiveMdiChild).rTBDoc.Focus();
                tempRTB.Dispose();
            }
        }

        private void toolStripButton8_Click(object sender, EventArgs e)
        {
            ChangeRTBFontStyle(((Form2)this.ActiveMdiChild).rTBDoc, FontStyle.Underline);
        }

        private void toolStripButton6_Click(object sender, EventArgs e)
        {
            ChangeRTBFontStyle(((Form2)this.ActiveMdiChild).rTBDoc, FontStyle.Bold);
        }

        private void toolStripButton7_Click(object sender, EventArgs e)
        {
            ChangeRTBFontStyle(((Form2)this.ActiveMdiChild).rTBDoc, FontStyle.Italic);
        }

        private void toolStripButton9_Click(object sender, EventArgs e)
        {
            ChangeRTBFontStyle(((Form2)this.ActiveMdiChild).rTBDoc, FontStyle.Strikeout);
        }

        private void toolStripButton4_Click(object sender, EventArgs e)
        {
            ((Form2)this.ActiveMdiChild).rTBDoc.Undo();
        }

        private void toolStripButton5_Click(object sender, EventArgs e)
        {
            ((Form2)this.ActiveMdiChild).rTBDoc.Redo();
        }

        private void toolStripButton1_Click(object sender, EventArgs e)
        {
            Clipboard.SetData(DataFormats.Rtf, ((Form2)this.ActiveMdiChild).rTBDoc.SelectedRtf);//复制RTF数据到剪贴板
            ((Form2)this.ActiveMdiChild).rTBDoc.SelectedRtf = "";//再把当前选取的RTF内容清除掉
        }

        private void toolStripButton2_Click(object sender, EventArgs e)
        {
            Clipboard.SetData(DataFormats.Rtf, ((Form2)this.ActiveMdiChild).rTBDoc.SelectedRtf);//复制RTF数据到剪贴板
        }

        private void toolStripButton3_Click(object sender, EventArgs e)
        {
            ((Form2)this.ActiveMdiChild).rTBDoc.Paste();//把剪贴板上的数据粘贴到目标
        }

        private void toolStripButton10_Click(object sender, EventArgs e)
        {
            ((Form2)this.ActiveMdiChild).rTBDoc.SelectionAlignment = HorizontalAlignment.Left;
        }

        private void toolStripButton13_Click(object sender, EventArgs e)
        {
            ((Form2)this.ActiveMdiChild).rTBDoc.SelectionAlignment = HorizontalAlignment.Center;
        }

        private void toolStripButton14_Click(object sender, EventArgs e)
        {
            ((Form2)this.ActiveMdiChild).rTBDoc.SelectionAlignment = HorizontalAlignment.Right;
        }
        private void NewDoc()
        {
            Form2 fd = new Form2();//新建窗口
            fd.MdiParent = this;//该新建窗口的父亲是当前的主窗口
            fd.Text = "untitle" + "文档" + _num;//文件名
            fd.WindowState = FormWindowState.Maximized;
            fd.Show();//展示该文档
            fd.Activate();//激活窗体并给予焦点
            _num++;
        }
        private void OpenDoc()
        {
            OpenFileDialog openfiledialog1 = new OpenFileDialog();
            openfiledialog1.Filter = "文本文件(*.txt)|*.txt|所有文件(*.*)|*.*";
            openfiledialog1.Multiselect = false;//禁止多选
            if (openfiledialog1.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    NewDoc();
                    ((Form2)this.ActiveMdiChild).rTBDoc.LoadFile(openfiledialog1.FileName, RichTextBoxStreamType.PlainText);
                    string localFilePath = openfiledialog1.FileName.ToString();
                    lujin = localFilePath;
                    ((Form2)this.ActiveMdiChild).Text = localFilePath.Substring(localFilePath.LastIndexOf("\\") + 1);//设置文档名字
                }
                catch
                {
                    MessageBox.Show("打开失败！", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            openfiledialog1.Dispose();
        }

        private void saveat()
        {
            SaveFileDialog savefiledialog1 = new SaveFileDialog();//打开另存为的框框
            savefiledialog1.Filter = "文本文件(*.txt)|*.txt";
            if (savefiledialog1.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    ((Form2)this.ActiveMdiChild).rTBDoc.SaveFile(savefiledialog1.FileName, RichTextBoxStreamType.PlainText);
                    MessageBox.Show("保存成功！", "", MessageBoxButtons.OK, MessageBoxIcon.None);
                }
                catch
                {
                    MessageBox.Show("保存失败！", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            savefiledialog1.Dispose();
        }

        private void baocun()
        {
            string ext = ((Form2)this.ActiveMdiChild).Text.Substring(((Form2)this.ActiveMdiChild).rTBDoc.Text.LastIndexOf(".") + 1);
            ext = ext.ToLower();//转小写
            ((Form2)this.ActiveMdiChild).rTBDoc.SaveFile(lujin, RichTextBoxStreamType.PlainText);
            ((Form2)this.ActiveMdiChild).rTBDoc.Modified = false;
            MessageBox.Show("保存成功", ext);
        }

        private void 新建ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            NewDoc();
        }

        private void 打开ToolStripMenuItem_Click(object sender, EventArgs e)
        {
           OpenDoc();
        }

        private void 保存ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (((Form2)this.ActiveMdiChild).Text.Length < 7)//如果名字长度小于等于7，那就是“打开”，就执行保存
                baocun();
            else
            {
                if (((Form2)this.ActiveMdiChild).Text.Substring(0, 7) == "untitle")//如果名字前七个元素等于untitle，那就是“新建”，就执行另存为
                    saveat();
                else
                    baocun();
            }
        }

        private void 另存为ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            saveat();
        }

        private void 关闭选项卡ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (MessageBox.Show("确定要关闭当前文档吗？", "提示", MessageBoxButtons.OKCancel, MessageBoxIcon.Information) == DialogResult.OK)
                ((Form2)this.ActiveMdiChild).Close();
        }

        private void 窗口层叠ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            LayoutMdi(MdiLayout.Cascade);
            this.窗口层叠ToolStripMenuItem.Checked = true;
            this.垂直平铺ToolStripMenuItem.Checked = false;
            this.水平平铺ToolStripMenuItem.Checked = false;
        }

        private void 水平ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            LayoutMdi(MdiLayout.TileHorizontal);
            this.窗口层叠ToolStripMenuItem.Checked = false;
            this.垂直平铺ToolStripMenuItem.Checked = false;
            this.水平平铺ToolStripMenuItem.Checked = true;
        }

        private void 垂直平铺ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            LayoutMdi(MdiLayout.TileVertical);
            this.窗口层叠ToolStripMenuItem.Checked = false;
            this.垂直平铺ToolStripMenuItem.Checked = true;
            this.水平平铺ToolStripMenuItem.Checked = false;
        }
        public Form2 formRichText;
        private void toolStripButton11_Click(object sender, EventArgs e)
        {
            
            formRichText = (Form2)this.ActiveMdiChild;
            Form3 formFind = new Form3(formRichText);
            formFind.Show();
        }
    }
}