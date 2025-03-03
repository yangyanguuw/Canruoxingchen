import cv2
import json
import os
import glob
import os.path as osp
import numpy as np

def Iou(SAMDirPath="", PersonDirPath=""):

    SAMList =glob.glob(os.path.join(SAMDirPath, "*.jpg"))
    PersonList=glob.glob(os.path.join(PersonDirPath, "*.jpg"))
    sum=0.0
    sum2=0.0
    sum3=0.0
    n=0
    for SAM,Person in zip(SAMList,PersonList):

        # 读取图像，并确保它们是灰度图像
        img1 = cv2.imread(SAM, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(Person, cv2.IMREAD_GRAYSCALE)

        # 确保图像是二值图像（如果它们不是的话）
        # 假设二值化阈值为128（你可以根据图像内容调整这个值）
        _, img1_binary = cv2.threshold(img1, 1, 255, cv2.THRESH_BINARY)
        _, img2_binary = cv2.threshold(img2, 1, 255, cv2.THRESH_BINARY)

        # 计算交集
        intersection = cv2.bitwise_and(img1_binary, img2_binary)

        # 计算并集
        union = cv2.bitwise_or(img1_binary, img2_binary)

        # 计算交集和并集区域的面积
        intersection_area = np.sum(intersection == 255)
        union_area = np.sum(union == 255)
        num1=np.sum(img1_binary==255)
        num2=np.sum(img2_binary==255)

        # 为了避免除以零的情况，检查并集面积是否为零
        if union_area == 0:
            iou = 0.0  # 或者你可以设置一个特定的值来表示没有交集的情况
        else:
            iou = intersection_area / float(union_area)

        acc = intersection_area / float(num1)
        recall=intersection_area/float(num2)
        sum+=iou
        sum2+=acc
        sum3+=recall
        n+=1
        print("IoU: {:.2f}".format(iou),"PA: {:.2f}".format(acc),"Recall: {:.2f}".format(recall))

    print("mIoU: {:.2f}".format(sum/n),"mPA: {:.2f}".format(sum2/n),"mRecall: {:.2f}".format(sum3/n))


if __name__ == "__main__":
    SAMfilePath = "C:/Users/17339\Desktop\IOU/box-point\edge"  # 要转换的json文件所在目录
    PersonDirPath = "C:/Users/17339\Desktop\IOU\std-all/"  # 要生成的txt文件夹
    Iou(SAMfilePath,PersonDirPath)
