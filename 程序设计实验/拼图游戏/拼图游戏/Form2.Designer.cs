namespace 拼图游戏
{
    partial class Form_Original
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
            this.pb_Original = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.pb_Original)).BeginInit();
            this.SuspendLayout();
            // 
            // pb_Original
            // 
            this.pb_Original.Dock = System.Windows.Forms.DockStyle.Fill;
            this.pb_Original.Location = new System.Drawing.Point(0, 0);
            this.pb_Original.Name = "pb_Original";
            this.pb_Original.Size = new System.Drawing.Size(774, 729);
            this.pb_Original.TabIndex = 0;
            this.pb_Original.TabStop = false;
            this.pb_Original.Click += new System.EventHandler(this.pb_Original_Click);
            // 
            // Form_Original
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(14F, 31F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(774, 729);
            this.Controls.Add(this.pb_Original);
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "Form_Original";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "原图";
            this.Load += new System.EventHandler(this.Form2_Load);
            ((System.ComponentModel.ISupportInitialize)(this.pb_Original)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private PictureBox pb_Original;
    }
}