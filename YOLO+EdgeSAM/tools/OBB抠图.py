import os
import cv2
import numpy as np
import math
image_path = "F:/data/yolo-train/GG/images/train/"        # jpg图片和对应的生成结果的txt标注文件，放在一起
label_path = "F:/data/yolo-train/GG/labels/train/"
save_path = 'C:/Users/17339/Desktop/save/'    # 裁剪出来的小图保存的根目录
size=np.array([3840,2160])
image_center=size/2

image_list = os.listdir(image_path)

for image_name in image_list:
    first,last = os.path.splitext(image_name)
    if last == ".jpg":                      # 图片的后缀名
        # img_total.append(first)
        img =  cv2.imread(image_path+image_name)
        # 打开txt文档
        if os.path.exists(label_path+"{}.txt".format(first)):
            with open(label_path+"{}.txt".format(first), 'r') as file:
                n=1
                for line in file.readlines():
                    # 按照空格拆分成多个浮点数
                    x =np.array([float(x) for x in line.split()])
                    points=x[1:]
                    points=points.reshape(-1,2)
                    rect=points*size
                    # 计算中心点以及长宽
                    center = np.mean(rect, axis=0)
                    width = np.linalg.norm(rect[1] - rect[0])+10
                    height = np.linalg.norm(rect[2] - rect[1])+10
                    # 计算旋转角
                    slope=(x[2]-x[4])/(x[1]-x[3])
                    angle = math.degrees(math.atan(slope))
                    # 进行仿射变换
                    rotation_matrix = cv2.getRotationMatrix2D(center,angle, 1.0)
                    rotated_img = cv2.warpAffine(img, rotation_matrix, (img.shape[1], img.shape[0]))
                    # 裁剪旋转后的矩形
                    x1 = center[0]-width/2
                    x2 = center[0]+width/2
                    y1 = center[1]-height/2
                    y2 = center[1]+height/2
                    cropped_img = rotated_img[int(y1):int(y2), int(x1):int(x2)]

                    # 保存裁剪后的图片
                    if cropped_img.shape[0]==0 or cropped_img.shape[1]==0:
                        continue
                    else:
                        print("{}_{}.jpg".format(first,n),width,height,angle)
                        cv2.imwrite(save_path+"{}_{}.jpg".format(first,n), cropped_img)
                        n+=1
    else:
        continue

