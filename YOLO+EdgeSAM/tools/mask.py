import cv2
import json
import os
import glob
import os.path as osp
import numpy as np

def labelme2yolov2Seg(jsonfilePath="", resultDirPath="", classList=["dusty", "defect", "damaged"]):
    # 0.创建保存转换结果的文件夹
    if(not os.path.exists(resultDirPath)):
        os.mkdir(resultDirPath)

    # 1.获取目录下所有的labelme标注好的Json文件，存入列表中
    jsonfileList = glob.glob(osp.join(jsonfilePath, "*.json"))

    # 2.遍历json文件，进行转换
    for jsonfile in jsonfileList:
        # 3. 打开json文件
        with open(jsonfile, "r") as f:
            file_in = json.load(f)

            # 4. 读取文件中记录的所有标注目标
            shapes = file_in["shapes"]

            # 5. 使用图像名称创建一个txt文件，用来保存数据
            with open(resultDirPath + "\\" + jsonfile.split("\\")[-1].replace(".json", ".txt"), "w") as file_handle:
                # 6. 遍历shapes中的每个目标的轮廓
                img = np.zeros((2160, 3840, 3), dtype=np.uint8)
                sum=0
                for shape in shapes:
                    mask =np.array(shape["points"], np.int32).reshape((-1,1,2))  # 坐标为顺时针方向
                    cv2.fillPoly(img,[mask], (255, 255, 255))
                    sum=sum+np.sum(img[:,:,0]== 255)

                    # 展示掩膜图片
                print(sum)
                cv2.imwrite(resultDirPath+"\\" + jsonfile.split("\\")[-1].replace(".json", ".jpg"),img)

            # 10.所有物体都遍历完，需要关闭文件
            file_handle.close()
        # 10.所有物体都遍历完，需要关闭文件
        f.close()

if __name__ == "__main__":
    jsonfilePath = "C:/Users/17339/Desktop/2/"  # 要转换的json文件所在目录
    resultDirPath = "C:/Users/17339/Desktop/4/"  # 要生成的txt文件夹
    labelme2yolov2Seg(jsonfilePath=jsonfilePath, resultDirPath=resultDirPath, classList=["0", "1"])
