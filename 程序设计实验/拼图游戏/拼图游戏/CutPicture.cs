using System;
using System.Collections.Generic;
using System.Drawing.Imaging;
using System.Linq;
using System.Text;
using System.Drawing;
using System.Windows.Forms;
using System.Threading.Tasks;
using System.Transactions;

namespace 拼图游戏
{
    class CutPicture
    {
        public static string PicturePath = "";
        public static List<Bitmap> BitMapList = null;
        ///<summary>
        ///保存图片到根目录下的Pictures文件夹下
        /// </summary>
        /// <param name="path">文件路径</param>
        /// <param name="inWidth">调整的宽</param>
        /// <param name="inHeight">调整的高</param>
        /// <returns></returns>
        public static Image Resize(string path,int iWidth,int iHeight)
        {
            Image thumbnail = null;
            try
            {
                var img = Image.FromFile(path);
                thumbnail = img.GetThumbnailImage(iWidth,iHeight,null,IntPtr.Zero);
                thumbnail.Save(Application.StartupPath.ToString() + "Pictur\\img.jpeg");
            }
            catch(Exception exp)
            {
                Console.WriteLine(exp.Message);
            }
            return thumbnail;
        }
        ///<summary>
        ///复制图片
        /// </summary>
        /// <param name="b">图片</param>
        /// <param name="StartX">X坐标</param>
        /// <param name="StartY">Y坐标</param>
        /// <param name="inWidth">宽</param>
        /// <param name="inHeight">高</param>
        /// <returns></returns>
        public static Bitmap Cut(Image b,int StartX,int StartY,int iWidth,int iHeight)
        {
            if(b==null)
            {
                return null;
            }
            int w = b.Width;
            int h = b.Height;
            if(StartX>=w||StartY>=h)
            {
                return null ;
            }
            if(StartX+iWidth>w)
            {
                iWidth = w - StartX;
            }
            if (StartY + iHeight > w)
            {
                iHeight = h - StartY;
            }
            try
            {
                Bitmap bmpOut = new Bitmap(iWidth,iHeight,PixelFormat.Format24bppRgb);
                Graphics g = Graphics.FromImage(bmpOut);
                g.DrawImage(b, new Rectangle(0, 0, iWidth, iHeight), new Rectangle(StartX, StartY, iWidth, iHeight), GraphicsUnit.Pixel);               
                g.Dispose();
                return bmpOut;
            }
            catch
            {
                return null;
            }
        }
    } 
}
    
