namespace 多文本文档编辑器
{
    partial class Form3
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.findText = new System.Windows.Forms.TextBox();
            this.replaceText1 = new System.Windows.Forms.TextBox();
            this.button1 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.radioUp = new System.Windows.Forms.RadioButton();
            this.radioDown = new System.Windows.Forms.RadioButton();
            this.checkCase = new System.Windows.Forms.CheckBox();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(47, 44);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(86, 31);
            this.label1.TabIndex = 0;
            this.label1.Text = "查找：";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(47, 106);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(86, 31);
            this.label2.TabIndex = 0;
            this.label2.Text = "替换：";
            // 
            // findText
            // 
            this.findText.Location = new System.Drawing.Point(150, 40);
            this.findText.Name = "findText";
            this.findText.Size = new System.Drawing.Size(263, 38);
            this.findText.TabIndex = 1;
            // 
            // replaceText1
            // 
            this.replaceText1.Location = new System.Drawing.Point(150, 102);
            this.replaceText1.Name = "replaceText1";
            this.replaceText1.Size = new System.Drawing.Size(263, 38);
            this.replaceText1.TabIndex = 1;
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(449, 32);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(159, 54);
            this.button1.TabIndex = 2;
            this.button1.Text = "查找下一处";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(449, 94);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(159, 54);
            this.button2.TabIndex = 2;
            this.button2.Text = "替换";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.button2_Click);
            // 
            // radioUp
            // 
            this.radioUp.AutoSize = true;
            this.radioUp.Location = new System.Drawing.Point(269, 163);
            this.radioUp.Name = "radioUp";
            this.radioUp.Size = new System.Drawing.Size(141, 35);
            this.radioUp.TabIndex = 3;
            this.radioUp.TabStop = true;
            this.radioUp.Text = "向上查找";
            this.radioUp.UseVisualStyleBackColor = true;
            // 
            // radioDown
            // 
            this.radioDown.AutoSize = true;
            this.radioDown.Location = new System.Drawing.Point(466, 163);
            this.radioDown.Name = "radioDown";
            this.radioDown.Size = new System.Drawing.Size(141, 35);
            this.radioDown.TabIndex = 3;
            this.radioDown.TabStop = true;
            this.radioDown.Text = "向下查找";
            this.radioDown.UseVisualStyleBackColor = true;
            this.radioDown.CheckedChanged += new System.EventHandler(this.radioButton2_CheckedChanged);
            // 
            // checkCase
            // 
            this.checkCase.AutoSize = true;
            this.checkCase.Location = new System.Drawing.Point(47, 163);
            this.checkCase.Name = "checkCase";
            this.checkCase.Size = new System.Drawing.Size(166, 35);
            this.checkCase.TabIndex = 4;
            this.checkCase.Text = "区分大小写";
            this.checkCase.UseVisualStyleBackColor = true;
            // 
            // Form3
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(14F, 31F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(665, 231);
            this.Controls.Add(this.checkCase);
            this.Controls.Add(this.radioDown);
            this.Controls.Add(this.radioUp);
            this.Controls.Add(this.button2);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.replaceText1);
            this.Controls.Add(this.findText);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Name = "Form3";
            this.Text = "查找和替换";
            this.Load += new System.EventHandler(this.Form3_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private Label label1;
        private Label label2;
        private TextBox findText;
        private TextBox replaceText1;
        private Button button1;
        private Button button2;
        private RadioButton radioUp;
        private RadioButton radioDown;
        private CheckBox checkCase;
    }
}