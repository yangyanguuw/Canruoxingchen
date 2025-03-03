using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace 拼图游戏
{
    public partial class Form_Main : Form
    {
        
        public Form_Main()
        {
            InitializeComponent();
            InitGame();
        }

        PictureBox[] pictureList = null;
        SortedDictionary<string, Bitmap> pictureLocationDict = new SortedDictionary<string, Bitmap>();
        Point[] pointList = null;//Location List
        SortedDictionary<string, PictureBox> pictureBoxLocationDict = new SortedDictionary<string, PictureBox>();//图片控件字典
        int second = 0;//拼图时间
        PictureBox currentPictureBox = null;//所拖拽的图片
        PictureBox haveToPictureBox = null;//被迫需要移动的图片
        Point oldLocation = Point.Empty;//原位置
        Point newLocation = Point.Empty;//新位置
        Point mousedDownPoint = Point.Empty;//鼠标按下坐标（control控件的相对坐标）
        Rectangle rect = Rectangle.Empty; //显示拖动效果的矩形
        bool isDrag = false;//是否正在拖拽
        public string originalpicpath;//图片位置
        /// <summary>
        /// 每个方向上需要切割成的块数
        /// </summary>
        private int ImgNumbers
        {
            get
            {
                return (int)this.numericUpDown1.Value;
            }
        }
        /// <summary>
        /// 要切割的正方形图片边长
        /// </summary>
        private int SideLength
        {
            get
            {
                return 600 / this.ImgNumbers;
            }
        }
        private void InitRandomPictureBox()
        {
            pnl_Picture.Controls.Clear();
            pictureList = new PictureBox[ImgNumbers * ImgNumbers];
            pointList = new Point[ImgNumbers * ImgNumbers];
            for (int i = 0; i < this.ImgNumbers; i++)
            {
                for (int j = 0; j < this.ImgNumbers; j++)
                {
                    PictureBox pic = new PictureBox();
                    pic.Name = "pictureBox" + (j + i * ImgNumbers + 1).ToString();
                    pic.Location = new Point(j * SideLength, i * SideLength);
                    pic.Size = new Size(SideLength, SideLength);
                    pic.Visible = true;
                    pic.BorderStyle = BorderStyle.FixedSingle;
                    pic.MouseDown += new MouseEventHandler(pictureBox_MouseDown);
                    pic.MouseMove += new MouseEventHandler(pictureBox_MouseMove);
                    pic.MouseUp += new MouseEventHandler(pictureBox_MouseUp);
                    pnl_Picture.Controls.Add(pic);
                    pictureList[j + i * ImgNumbers] = pic;
                    pointList[j + i * ImgNumbers] = new Point(j * SideLength, i * SideLength);
                }
            }
        }
        public void Flow(string path, bool disorder)
        {
            InitRandomPictureBox();
            Image bm = CutPicture.Resize(path, 600, 600);
            CutPicture.BitMapList = new List<Bitmap>();
            for (int y = 0; y < 600; y += SideLength)
            {
                for (int x = 0; x < 600; x += SideLength)
                {
                    Bitmap temp = CutPicture.Cut(bm, x, y, SideLength, SideLength);
                    CutPicture.BitMapList.Add(temp);
                }
            }
            ImportBitMap(disorder);
        }
        public Point[] DisOrderLocation()
        {
            Point[] tempArray = (Point[])pointList.Clone();
            for (int i = tempArray.Length - 1; i > 0; i--)
            {
                Random rand = new Random();
                int p = rand.Next(i);
                Point temp = tempArray[p];
                tempArray[p] = tempArray[i];
                tempArray[i] = temp;
            }
            return tempArray;

        }
        public void ResetPictureLocation()
        {
            Point[] temp = DisOrderLocation();
            int i = 0;
            foreach (PictureBox item in pictureList)
            {
                item.Location = temp[i];
                i++;
            }
        }
        public void ImportBitMap(bool disorder)
        {
            try
            {
                int i = 0;
                foreach (PictureBox item in pictureList)
                {
                    Bitmap temp = CutPicture.BitMapList[i];
                    item.Image = temp;
                    i++;
                }
                if (disorder)
                    ResetPictureLocation();
            }
            catch (Exception exp)
            {
                Console.WriteLine(exp.Message);
            }
        }
        public void InitGame()
        {
            if (!Directory.Exists(Application.StartupPath.ToString() + "\\Picture"))
            {
                Directory.CreateDirectory(Application.StartupPath.ToString() + "\\Picture");
                Properties.Resources._1.Save(Application.StartupPath.ToString() + "\\Picture\\1.jpg");
                Properties.Resources._2.Save(Application.StartupPath.ToString() + "\\Picture\\2.jpg");
                Properties.Resources._3.Save(Application.StartupPath.ToString() + "\\Picture\\3.jpg");
                Properties.Resources._4.Save(Application.StartupPath.ToString() + "\\Picture\\4.jpg");
                Properties.Resources._5.Save(Application.StartupPath.ToString() + "\\Picture\\5.jpg");
                Properties.Resources._6.Save(Application.StartupPath.ToString() + "\\Picture\\6.jpg");
                Properties.Resources._7.Save(Application.StartupPath.ToString() + "\\Picture\\7.jpg");
            }
            Random r = new Random();
            int i = r.Next(7);
            originalpicpath = Application.StartupPath.ToString() + "\\Picture\\" + i.ToString() + ".jpg";
            Flow(originalpicpath, true);
        }
        public PictureBox GetPictureBoxByLocation(int x, int y)
        {
            PictureBox pic = null;
            foreach (PictureBox item in pictureList)
            {
                if (x > item.Location.X && y > item.Location.Y && item.Location.X + SideLength > x && item.Location.Y + SideLength > y)
                {
                    pic = item;
                }
            }
            return pic;
        }
       
        public PictureBox GetPictureBoxByHashCode(string hascode)
        {
            PictureBox pic = null;
            foreach (PictureBox item in pictureList)
            {
                if (hascode == item.GetHashCode().ToString())
                {
                    pic = item;
                }
            }
            return pic;
        }

        private void pictureBox_MouseDown(object sender, MouseEventArgs e)
        {
            oldLocation = new Point(e.X, e.Y);
            currentPictureBox = GetPictureBoxByHashCode(sender.GetHashCode().ToString());
            MoseDown(currentPictureBox, sender, e);

        }

        private void MoseDown(PictureBox pic, object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                oldLocation = e.Location;
                rect = pic.Bounds;
            }
        }

        private void pictureBox_MouseMove(object sender,MouseEventArgs e)
        {
            if(e.Button == MouseButtons.Left)
            {
                isDrag= true;
                rect.Location = getPointToForm(new Point(e.Location.X - oldLocation.X, e.Location.Y - oldLocation.Y));
                this.Refresh();
            }
        }


        private Point getPointToForm(Point p)
        {
            return this.PointToClient(pictureList[0].PointToScreen(p));
        }
        
        private void reset()
        {
            mousedDownPoint=Point.Empty;
            rect = Rectangle.Empty;
            isDrag = false;
        }

        private void pictureBox_MouseUp(object sender,MouseEventArgs e)
        {
            oldLocation =new Point(currentPictureBox.Location.X, currentPictureBox.Location.Y);
            if(oldLocation.X +e.X>600||oldLocation.Y +e.Y>600||oldLocation.X+e.X<0||oldLocation.Y+e.Y<0)
            {
                return;
            }
            haveToPictureBox = GetPictureBoxByLocation(oldLocation.X + e.X, oldLocation.Y + e.Y);
            newLocation = new Point(haveToPictureBox.Location.X, haveToPictureBox.Location.Y);
            haveToPictureBox.Location = oldLocation;
            PictureMouseUp(currentPictureBox, sender, e);
            if(Judge())
            {
                lab_result.Text = "成功！";
            }
        }

        public void PictureMouseUp(PictureBox pic,object sender,MouseEventArgs e)
        {
            if(e.Button==MouseButtons.Left)
            {
                if(isDrag)
                {
                    isDrag=false;
                    pic.Location = newLocation;
                    this.Refresh();
                }
                reset();
            }
        }

        public bool Judge()
        {
            bool result = true;
            int i = 0;
            foreach(PictureBox item in pictureList)
            {
                if (item.Location != pointList[i])
                {
                    result = false;
                }
                i++;
            }
            return result;
        }
        private void splitContainer1_Panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void button3_Click(object sender, EventArgs e)
        {
            Random r=new Random();
            int i=r.Next(7);
            originalpicpath = Application.StartupPath.ToString() + "\\Picture\\" + i.ToString() + ".jpg";
            Flow(originalpicpath, true);
        }

        private void button4_Click(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {

        }

        private void 查看原图_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void btn_import_Click(object sender, EventArgs e)
        {
            OpenFileDialog new_picture = new OpenFileDialog();
            if (new_picture.ShowDialog()==DialogResult.OK)
            {
                lab_result.Text = "";
                originalpicpath = new_picture.FileName;
                CutPicture.PicturePath = new_picture.FileName;
                Flow(CutPicture.PicturePath, true);
            }
        }

        private void btn_Reset_Click(object sender, EventArgs e)
        {
            Flow(originalpicpath, true);
        }

        private void btn_Originalpic_Click(object sender, EventArgs e)
        {
            Form_Original original = new Form_Original();
            original.picpath = originalpicpath;
            original.ShowDialog();
        }
        private void numericUpDown1_ValueChanged(object sender, EventArgs e)
        {

        }
    }
}