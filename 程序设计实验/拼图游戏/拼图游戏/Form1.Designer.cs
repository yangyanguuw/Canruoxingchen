namespace 拼图游戏
{
    partial class Form_Main
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
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
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            this.pnl_Picture = new System.Windows.Forms.Panel();
            this.label1 = new System.Windows.Forms.Label();
            this.lab_result = new System.Windows.Forms.Label();
            this.numericUpDown1 = new System.Windows.Forms.NumericUpDown();
            this.btn_Reset = new System.Windows.Forms.Button();
            this.btn_Changepic = new System.Windows.Forms.Button();
            this.btn_import = new System.Windows.Forms.Button();
            this.btn_Originalpic = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).BeginInit();
            this.splitContainer1.Panel1.SuspendLayout();
            this.splitContainer1.Panel2.SuspendLayout();
            this.splitContainer1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown1)).BeginInit();
            this.SuspendLayout();
            // 
            // splitContainer1
            // 
            this.splitContainer1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer1.Location = new System.Drawing.Point(0, 0);
            this.splitContainer1.Name = "splitContainer1";
            // 
            // splitContainer1.Panel1
            // 
            this.splitContainer1.Panel1.Controls.Add(this.pnl_Picture);
            // 
            // splitContainer1.Panel2
            // 
            this.splitContainer1.Panel2.Controls.Add(this.label1);
            this.splitContainer1.Panel2.Controls.Add(this.lab_result);
            this.splitContainer1.Panel2.Controls.Add(this.numericUpDown1);
            this.splitContainer1.Panel2.Controls.Add(this.btn_Reset);
            this.splitContainer1.Panel2.Controls.Add(this.btn_Changepic);
            this.splitContainer1.Panel2.Controls.Add(this.btn_import);
            this.splitContainer1.Panel2.Controls.Add(this.btn_Originalpic);
            this.splitContainer1.Size = new System.Drawing.Size(1155, 594);
            this.splitContainer1.SplitterDistance = 603;
            this.splitContainer1.TabIndex = 0;
            // 
            // pnl_Picture
            // 
            this.pnl_Picture.Location = new System.Drawing.Point(0, 0);
            this.pnl_Picture.Name = "pnl_Picture";
            this.pnl_Picture.Size = new System.Drawing.Size(600, 600);
            this.pnl_Picture.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(80, 265);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(254, 31);
            this.label1.TabIndex = 3;
            this.label1.Text = "图片切割数量（单边）";
            // 
            // lab_result
            // 
            this.lab_result.AutoSize = true;
            this.lab_result.Location = new System.Drawing.Point(227, 347);
            this.lab_result.Name = "lab_result";
            this.lab_result.Size = new System.Drawing.Size(0, 31);
            this.lab_result.TabIndex = 2;
            // 
            // numericUpDown1
            // 
            this.numericUpDown1.Location = new System.Drawing.Point(340, 263);
            this.numericUpDown1.Name = "numericUpDown1";
            this.numericUpDown1.Size = new System.Drawing.Size(98, 38);
            this.numericUpDown1.TabIndex = 1;
            this.numericUpDown1.Value = new decimal(new int[] {
            3,
            0,
            0,
            0});
            this.numericUpDown1.ValueChanged += new System.EventHandler(this.numericUpDown1_ValueChanged);
            // 
            // btn_Reset
            // 
            this.btn_Reset.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.btn_Reset.Location = new System.Drawing.Point(288, 172);
            this.btn_Reset.Name = "btn_Reset";
            this.btn_Reset.Size = new System.Drawing.Size(150, 46);
            this.btn_Reset.TabIndex = 0;
            this.btn_Reset.Text = "图片重排";
            this.btn_Reset.UseVisualStyleBackColor = true;
            this.btn_Reset.Click += new System.EventHandler(this.btn_Reset_Click);
            // 
            // btn_Changepic
            // 
            this.btn_Changepic.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.btn_Changepic.Location = new System.Drawing.Point(80, 172);
            this.btn_Changepic.Name = "btn_Changepic";
            this.btn_Changepic.Size = new System.Drawing.Size(150, 46);
            this.btn_Changepic.TabIndex = 0;
            this.btn_Changepic.Text = "切换图片";
            this.btn_Changepic.UseVisualStyleBackColor = true;
            this.btn_Changepic.Click += new System.EventHandler(this.button3_Click);
            // 
            // btn_import
            // 
            this.btn_import.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.btn_import.Location = new System.Drawing.Point(288, 86);
            this.btn_import.Name = "btn_import";
            this.btn_import.Size = new System.Drawing.Size(150, 46);
            this.btn_import.TabIndex = 0;
            this.btn_import.Text = "试玩新图";
            this.btn_import.UseVisualStyleBackColor = true;
            this.btn_import.Click += new System.EventHandler(this.btn_import_Click);
            // 
            // btn_Originalpic
            // 
            this.btn_Originalpic.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.btn_Originalpic.Location = new System.Drawing.Point(80, 86);
            this.btn_Originalpic.Name = "btn_Originalpic";
            this.btn_Originalpic.Size = new System.Drawing.Size(150, 46);
            this.btn_Originalpic.TabIndex = 0;
            this.btn_Originalpic.Text = "查看原图";
            this.btn_Originalpic.UseVisualStyleBackColor = true;
            this.btn_Originalpic.Click += new System.EventHandler(this.btn_Originalpic_Click);
            // 
            // Form_Main
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(14F, 31F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1155, 594);
            this.Controls.Add(this.splitContainer1);
            this.MaximizeBox = false;
            this.Name = "Form_Main";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "拼图游戏";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.splitContainer1.Panel1.ResumeLayout(false);
            this.splitContainer1.Panel2.ResumeLayout(false);
            this.splitContainer1.Panel2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).EndInit();
            this.splitContainer1.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown1)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private SplitContainer splitContainer1;
        private Panel pnl_Picture;
        private Button btn_Reset;
        private Button btn_Changepic;
        private Button btn_import;
        private Button btn_Originalpic;
        private NumericUpDown numericUpDown1;
        private Label lab_result;
        private Label label1;
    }
}