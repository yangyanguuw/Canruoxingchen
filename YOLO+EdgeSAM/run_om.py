import cv2  # 图片处理三方库，用于对图片进行前后处理
import numpy as np  # 用于对多维数组进行计算
import torch  # 深度学习运算框架，此处主要用来处理数据

from mindx.sdk import Tensor  # mxVision 中的 Tensor 数据结构
from mindx.sdk import base  # mxVision 推理接口

from det_utils import get_labels_from_txt, letterbox, scale_coords, nms, draw_bbox  # 模型前后处理相关函数

# 初始化资源和变量
base.mx_init()  # 初始化 mxVision 资源
DEVICE_ID = 0  # 设备id
model_path = '/home/HwHiAiUser/Desktop/yolo/weights/yolo.om'  # 模型路径
encoder_path='/home/HwHiAiUser/Desktop/yolo/weights/encoder.om' #编码器路径
decoder_path='/home/HwHiAiUser/Desktop/yolo/weights/decoder.om' #解码器路径
image_path = '/home/HwHiAiUser/Desktop/0001.jpg'  # 测试图片路径

# 数据前处理
img_bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)  # 读入图片
img, scale_ratio, pad_size = letterbox(img_bgr, new_shape=[1024,1024])  # 对图像进行缩放与填充，保持长宽比
img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, HWC to CHW，将形状转换为 channel first
img = np.expand_dims(img, 0).astype(np.float32)  # 得到(1, 3, 640, 640)，即扩展第一维为 batchsize
img = np.ascontiguousarray(img) / 255.0  # 转换为内存连续存储的数组
img = Tensor(img) # 将numpy转为转为Tensor类

# 模型推理, 得到模型输出
model = base.model(modelPath=model_path, deviceId=DEVICE_ID)  # 初始化 base.model 类
encoder =base.model(modelPath=encoder_path, deviceId=DEVICE_ID) # 初始化encoder
decoder =base.model(modelPath=decoder_path, deviceId=DEVICE_ID) #初始化decoder

output = model.infer([img])[0]  # 执行推理。输入数据类型：List[base.Tensor]， 返回模型推理输出的 List[base.Tensor]

# 后处理
output.to_host()  # 将Tensor数据转移到内存
output = np.array(output)  # 将数据转为 numpy array 类型
boxout = nms(torch.tensor(output), conf_thres=0.4, iou_thres=0.5)  # 利用非极大值抑制处理模型输出，conf_thres 为置信度阈值，iou_thres 为iou阈值
pred_all = boxout[0].numpy()  # 转换为numpy数组
scale_coords([640, 640], pred_all[:, :4], img_bgr.shape, ratio_pad=(scale_ratio, pad_size))  # 将推理结果缩放到原始图片大小
labels_dict = get_labels_from_txt('./coco_names.txt')  # 得到类别信息，返回序号与类别对应的字典
img_dw = draw_bbox(pred_all, img_bgr, (0, 255, 0), 2, labels_dict)  # 画出检测框、类别、概率

# 保存图片到文件
cv2.imwrite('/home/HwHiAiUser/Desktop/result.png', img_dw)
print('save infer result success')