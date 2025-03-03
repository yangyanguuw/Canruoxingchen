# 灿若星辰
一些奇思妙想+一点点魔法
# 当 YOLO-OBB 遇上 SAM

## SAM

### SAM的基本使用方法

1.获取项目源代码

Github 中搜索 segment-anything`下载zip文件`

| ![](./images/get_project.png) |
|:-----------------------------:|
或`本地克隆存储` 
```
git clone git@github.com:facebookresearch/segment-anything.git
```

2.安装 SAM

```
cd segment-anything
pip install -e .
```

3.安装 SAM 运行所需要的环境依赖

```
pip install opencv-python pycocotools matplotlib onnxruntime onnx
```
- 请注意：请务必安装`CUDA`和`Pytorch`

4.获取 SAM 权重文件

|       Name       |                                          Link                                           |
| :--------------: | :-------------------------------------------------------------------------------------: |
| Default or ViT-H | [ViT-H SAM model](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth) |
|      ViT-L       | [ViT-L SAM model](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth) |
|      ViT-B       | [ViT-B SAM model](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth) |

5.运行

引入模型和运行所需的包

```
import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
```

定义结果展示函数和结果保存函数

```
#展示掩膜
def show_mask(mask, ax, random_color=False):
    if random_color:
        #随机RGB+alpha=0.6的通道,将掩膜以彩色渲染出来
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)

#展示points_prompt
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels == 1]
    neg_points = coords[labels == 0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color=‘green’, marker=‘.’, s=marker_size, edgecolor=‘white’,
               linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color=‘red’, marker=‘.’, s=marker_size, edgecolor=‘white’,
               linewidth=1.25)

#展示boxes_prompt
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor=‘green’, facecolor=(0, 0, 0, 0), lw=2))
```

载入 SAM 模型

```
sam_checkpoint = path/to/model.pth   #加载权重,注意替换成权重所在路径
model_type = vit_b   #选择模型，注意模型应与权重一一对应
device = cuda #选择运行环境为GPU
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint) #根据选择,搭建SAM模型
sam.to(device=device) #指定运行环境为GPU
predictor = SamPredictor(sam)#加载模型
```

预测  
- 预测部分可选择`单点提示`，`单框提示`，`多点提示`，`多框提示`，`点+单框提示` 等，SAM团队同时提供了`掩膜提示`和`文本提示`
- SAM 支持 numpy 和 tensor 两套输入，但`多框提示`仅支持 tensor  
- 这里展示`多框提示`

创建box_prompt

```
#创建box_prompt
input_boxes = torch.tensor([
    [75, 275, 1725, 850],
    [425, 600, 700, 875],
    [1375, 550, 1650, 800],
    [1240, 675, 1400, 750],
], device=predictor.device)#将tensor加载到GPU
```

对框提示区域进行预测,返回结果为掩膜tensor,您可以大胆的将它们print出来,以便您更好的了解SAM给出的掩膜是怎样的一种表达形式,或者它的shape,以便您后续对掩膜进行处理

```
predictor.set_image(img) #图片预处理

transformed_boxes = predictor.transform.apply_boxes_torch(input_boxes, image.shape[:2])#将box_prompt调整，使其适应处理后的图片尺寸
masks, _, _ = predictor.predict_torch(
    point_coords=None,
    point_labels=None,
    boxes=transformed_boxes,
    multimask_output=False,
)#对图片进行预测
```
- 提示：SAM有两套预测系统，支持Numpy的ndarray和Pytorch的tensor，但程序的底层逻辑一定是将输入最终转换为`tensor`，所以再次提醒您务必安装`CUDA`和`PyTorch`  

结果展示与保存
```
plt.figure(figsize=(10, 10))
plt.imshow(image)
for mask in masks:
    show_mask(mask.cpu().numpy(), plt.gca(), random_color=True)
for box in input_boxes:
    show_box(box.cpu().numpy(), plt.gca())
plt.axis('off')
plt.show()
```
以上便是SAM模型的运行全过程，如果您想进一步了解SAM，请进入[GitHub-SAM](https://github.com/facebookresearch/segment-anything)  

----

### SAM的进阶教程

我们所做的努力不仅仅是成功运行SAM

如您所见，SAM可选择`单点提示`，`单框提示`，`多点提示`，`多框提示`，`点+单框提示` ，似乎我们更加期待`多点+多框提示`方法，因为如果我们的图片中有多个目标，这会让整个要分割的区域更加准确。  似乎SAM团队并没有真正给出我们解决方案。

| ![](./images/0018.jpg) | ![](./images/3956.jpg) |
|:----------------------:|:----------------------:|

在此部分开始之前，请您简要了解SAM的`PromptEncoder`模块是如何工作的，如果您想了解更多，请参考[【图像分割】【深度学习】SAM官方Pytorch代码-Prompt encoder模块ProEnco网络解析](https://blog.csdn.net/yangyu0515/article/details/130389786?spm=1001.2014.3001.5501)  

| ![图一](./images/prompt-encoder.png) <br> 图一  | ![图二](./images/prompt-encoder1.png) <br> 图二 |
|:-------------------------------------------:|:--:|
如图一所示，SAM由三个部分组成：
- 一个强大的图像编码器(Image encoder)计算图像嵌入
- 一个提示编码器(Prompt encoder)嵌入提示
- 将两个信息源组合在一个轻量级掩码解码器(Mask decoder)中来预测分割掩码

我们重点来看提示编码器(Prompt encoder):  

`代码路径`segment-anything-main\segment_anything\modeling\prompt_encoder.py
- 点提示  
```
def _embed_points(
    self,
    points: torch.Tensor,
    labels: torch.Tensor,
    pad: bool,
) -> torch.Tensor:
    # 移到像素中心
    points = points + 0.5
    # points和boxes联合则不需要pad
    if pad:
        padding_point = torch.zeros((points.shape[0], 1, 2), device=points.device)  # B,1,2
        padding_label = -torch.ones((labels.shape[0], 1), device=labels.device)     # B,1
        points = torch.cat([points, padding_point], dim=1)                          # B,N+1,2
        labels = torch.cat([labels, padding_label], dim=1)                          # B,N+1
    point_embedding = self.pe_layer.forward_with_coords(points, self.input_image_size)  # B,N+1,2f
    
    # labels为-1是非标记点,设为非标记点权重
    point_embedding[labels == -1] = 0.0
    point_embedding[labels == -1] += self.not_a_point_embed.weight
    # labels为0是背景点,加上背景点权重
    point_embedding[labels == 0] += self.point_embeddings[0].weight
    # labels为1的目标点,加上目标点权重
    point_embedding[labels == 1] += self.point_embeddings[1].weight
   
    return point_embedding
```
请重点注意return语句之前的几句代码，他们的作用是将点提示，加上相应的权重[ labels ]是将点提示区分为前景点和背景点的标志，如果该点为背景点就加上背景点权重，如果该点是前景点（目标点）就加上前景点权重.  

`注意`:这些权重来自于SAM训练好的权重文件，而并非我们随意选取.


- 框提示  
```
def _embed_boxes(self, boxes: torch.Tensor) -> torch.Tensor:
    # 移到像素中心
    boxes = boxes + 0.5
    coords = boxes.reshape(-1, 2, 2)
    corner_embedding = self.pe_layer.forward_with_coords(coords, self.input_image_size)    #
    # 目标框起始点的和末位点分别加上权重
    corner_embedding[:, 0, :] += self.point_embeddings[2].weight
    corner_embedding[:, 1, :] += self.point_embeddings[3].weight
    return corner_embedding
```
同样，SAM将会在框提示上加上相应的权重 

- Cat  

当传入的点提示和框提示加上相应的权重后，SAM将对它们进行融合
```
    def forward(
        self,
        points: Optional[Tuple[torch.Tensor, torch.Tensor]],
        boxes: Optional[torch.Tensor],
        masks: Optional[torch.Tensor],
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        bs = self._get_batch_size(points, boxes, masks)
        sparse_embeddings = torch.empty((bs, 0, self.embed_dim), device=self._get_device())
        if points is not None:
            coords, labels = points
            point_embeddings = self._embed_points(coords, labels, pad=(boxes is None))
            if boxes is not None:
                point_embeddings=point_embeddings.reshape(-1,1,256)
            sparse_embeddings = torch.cat([sparse_embeddings, point_embeddings], dim=1)
        if boxes is not None:
            box_embeddings = self._embed_boxes(boxes)
            sparse_embeddings = torch.cat([sparse_embeddings, box_embeddings], dim=1)
        if masks is not None:
            dense_embeddings = self._embed_masks(masks)
        else:
            dense_embeddings = self.no_mask_embed.weight.reshape(1, -1, 1, 1).expand(
                bs, -1, self.image_embedding_size[0], self.image_embedding_size[1]
            )

        return sparse_embeddings, dense_embeddings
```

言归正传，为了实现`多点+多框提示`，我们需要让加载完权重的`多点提示`和`多框提示`完成融合，就要保证二者在dim=1时有相同的形状.

于是，我们修改如下代码，保证在融合之前能够获得正确的batch_size

```
    def _get_batch_size(
        self,
        points: Optional[Tuple[torch.Tensor, torch.Tensor]],
        boxes: Optional[torch.Tensor],
        masks: Optional[torch.Tensor],
    ) -> int:

        if points is not None:
            if boxes is not None:
                return boxes.shape[0]
            else:
                return points[0].shape[0]
        elif boxes is not None:
            return boxes.shape[0]
        elif masks is not None:
            return masks.shape[0]
        else:
            return 1
```

为了您使用方便，也为提高系统运行效率，节省不必要的操作所带来的系统资源的消耗，我们特地准备了快速保存预测结果的函数。

它提供了将掩膜转换为RGB+alpha通道的方法，融合到输出图片的方法以及根据您提供的路径和名称保存结果的方法，请您放心大胆的调用

要使用save()方法，请提供如下参数：
- masks: 请您将SAM的预测结果，直接传给save()函数
- image: 请您将输入图片传给save()
- save_path: 请您将保存的路径以及文件名以字符串的形式完整地传给save()函数
- points: 如果您想保存点提示到结果上,请将点的坐标传给save()
- boxs: 如果您想保存框提示到结果上,请将点的坐标传给save()
```
#保存结果，将掩膜和图片融合，并保存到指定路径，请注意您的保存路径
def save(masks,image,save_path,points=None,boxs=None):
    if isinstance(masks,torch.Tensor):
        masks=masks.cpu().numpy()
    if isinstance(points,torch.Tensor):
        points=points.cpu().numpy()
    if isinstance(boxs,torch.Tensor):
        boxs=boxs.cpu().numpy()
    x=np.zeros_like(masks[0])
    for mask in masks:
        x=np.logical_or(x,mask)
    h, w = x.shape[-2:]
    color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    mask_image = (x.reshape(h, w, 1) * color.reshape(1, 1, -1)*255).astype(np.uint8)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    result = cv2.addWeighted(image, 1, mask_image, 0.5, 0)
    
    if points is not None:
        points=points.reshape(-1,2).astype(np.int32)
        for point in points:
            cv2.circle(result, tuple(point), 10, (0, 255, 0), -1)
    if boxs is not None:
        boxs=boxs.reshape(-1,4).astype(np.int32)
        for box in boxs:
            cv2.rectangle(result, box[:2], box[2:], (0,0,255), 5)
            
    cv2.imwrite(save_path,result)
```

-------------
## YOLO-OBB
### YOLO-OBB的基本使用方法

有关YOLO-OBB的一切使用教程，您可以进入[Ultralytics](https://github.com/ultralytics/ultralytics)查看，本文仅介绍YOLO-OBB的使用.

1.获取YOLO-OBB源代码

|![](./images/get_yolo.png)|
|:--:|
或`本地克隆存储` 
```
git clone git@github.com:facebookresearch/segment-anything.git
```

2.安装ultralytics和其他环境依赖

您可以选择进入项目所在路径，执行如下命令安装ultralytics和其他环境依赖
```
pip install ultralytics
```
以下是运行YOLO-OBB所需的全部环境依赖.如果您想启动GPU加速，建议您安装`CUDA`以及CUDA对应版本的`Pytorch`
```
    matplotlib>=3.3.0,
    numpy>=1.22.2,
    opencv-python>=4.6.0,
    pillow>=7.1.2,
    pyyaml>=5.3.1,
    requests>=2.23.0,
    scipy>=1.4.1,
    torch>=1.8.0,
    torchvision>=0.9.0,
    tqdm>=4.64.0, # progress bars
    psutil, # system utilization
    py-cpuinfo, # display CPU info
    thop>=0.1.1, # FLOPs computation
    pandas>=1.1.4,
    seaborn>=0.11.0, # plotting
```

3.运行
- Train
```
from ultralytics import YOLO

# 加载模型
model = YOLO('yolov8n.yaml')  # build a new model from YAML
model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)
model = YOLO('yolov8n.yaml').load('yolov8n.pt')  # build from YAML and transfer weights

# 模型训练
results = model.train(data='coco128.yaml', epochs=100, imgsz=640)
```
`解释`  
- 初次训练模型，预训练权重会自动下载，您也可以选择从以下链接中自行下载，自行替换权重文件路径

| Model                                                                                        | size<br><sup>(pixels) | mAP<sup>test<br>50 | Speed<br><sup>CPU ONNX<br>(ms) | Speed<br><sup>A100 TensorRT<br>(ms) | params<br><sup>(M) | FLOPs<br><sup>(B) |
| -------------------------------------------------------------------------------------------- | --------------------- | ------------------ | ------------------------------ | ----------------------------------- | ------------------ | ----------------- |
| [YOLOv8n-obb](https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n-obb.pt) | 1024                  | 76.9               | 204.77                         | 3.57                                | 3.1                | 23.3              |
| [YOLOv8s-obb](https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8s-obb.pt) | 1024                  | 78.0               | 424.88                         | 4.07                                | 11.4               | 76.3              |
| [YOLOv8m-obb](https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8m-obb.pt) | 1024                  | 80.5               | 763.48                         | 7.61                                | 26.4               | 208.6             |
| [YOLOv8l-obb](https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8l-obb.pt) | 1024                  | 80.7               | 1278.42                        | 11.83                               | 44.5               | 433.8             |
| [YOLOv8x-obb](https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8x-obb.pt) | 1024                  | 81.36              | 1759.10                        | 13.23                               | 69.5               | 676.7             |
- model.train()函数的常用参数有

|参数名| 意义                                                    |
|:--:|:------------------------------------------------------|
|data| 数据集的配置文件，它指明了训练集，验证集，测试集的路径，nc以及每一类目标的名称              |
|epochs| 训练的轮次                                                 |
|patience| 如果您指定patience=10，当观察到最近的10轮训练中模型没有改进时，就会提前结束训练        |
|batch| 一次加载到GPU进行梯度下降的图片数量                                   |
|imgsz| 图片的尺寸                                                 |
|save_period| 如果您指定save_period=25，那么每经过25轮训练，就会保存一次训练权重             |
|device| 指定运行设备，device=0 or 'cuda'在GPU上运行，device='cpu'则在cpu上运行 |
|workers| 指定线程数                                                 |
- 有关model.train()函数的所有参数写在ultralytics-main\ultralytics\cfg\default.yaml中，您可以自行打开文件查看，如果您在调用函数时未指定相应参数，程序将根据文件中的默认值传递参数



- Predict
```
from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n-obb.pt')  # load an official model
model = YOLO('path/to/best.pt')  # load a custom model

# Predict with the model
results = model(‘path/to/images/'，stream=False)  # predict on an image

#for result in results:
#    boxes = result.boxes  # Boxes object for bbox outputs
#    masks = result.masks  # Masks object for segmentation masks outputs
#    keypoints = result.keypoints  # Keypoints object for pose outputs
#    probs = result.probs  # Probs object for classification outputs
```
`提示`
- 请自行替换代码中的`path/to/best.pt`以及`path/to/images/`
- 有关model()函数的所有参数写在ultralytics-main\ultralytics\cfg\default.yaml中，您可以自行打开文件查看，如果您在调用函数时未指定相应参数，程序将根据文件中的默认值传递参数
- 如果您要预测大量的图片或视频，请设置stream=True，将注释部分的代码取消注释

## YOLO-OBB+SAM进行绝缘子目标检测和语义分割
这一部分，我们将全流程跑通YOLO-OBB+SAM进行绝缘子目标检测和语义分割，在这一章节中，我们将提供许多便捷的工具和方法，帮助您更快，更便捷完成模型训练和模型使用
我们将提供：

|工具名| 作用                                        |
|:--:|:------------------------------------------|
|xml转txt工具| 将rolabelImg制作的xml格式文件转化为YOLO-OBB可使用的txt文件 |
|数据集划分工具| 快速将数据集图片和标签按一定比例划分成数据集，验证集和测试集            |
|半自动标注方法| 快速制备YOLO-OBB数据集                           |
|txt转xml工具|将YOLO-OBB输出的txt文件转为RolabelImg可识别的xml文件|
### 制作数据集
我们将使用roLabelImg工具制作旋转框数据集，有关roLabelImg工具的获取以及使用教程，请查阅官网[GitHub-RolabelImg](https://github.com/cgvict/roLabelImg)

|![](./images/rolabel.png)|
|:--:|

制作好的数据集以*.xml的格式保存,以下是一个标注文件的实例
```
This XML file does not appear to have any style information associated with it. The document tree is shown below.
<annotation verified="no">
<folder>images</folder>
<filename>0001</filename>
<path>C:\Users\86151\Desktop\data\images\0001.jpg</path>
<source>
<database>Unknown</database>
</source>
<size>
<width>3840</width>
<height>2160</height>
<depth>3</depth>
</size>
<segmented>0</segmented>
<object>
<type>robndbox</type>
<name>1</name>
<pose>Unspecified</pose>
<truncated>0</truncated>
<difficult>0</difficult>
<robndbox>
<cx>2209.6667</cx>
<cy>1611.5</cy>
<w>135.0</w>
<h>717.0</h>
<angle>0.0</angle>
</robndbox>
</object>
</annotation>
```
而YOLO-OBB仅支持txt格式的标注文件，且其对标注的格式也有一定的要求

| ![](./images/label.png) |
|:-----------------------:|
您可以使用我们提供的[xml转txt工具](./tools/xml_to_txt.py)，将标注好的*.xml文件转换为*.txt文件，在使用过程中，请注意替换图片尺寸以及原始路径

### 划分数据集
制备好数据集后，需要将数据集按照一定的比例划分为训练集，测试集，验证集，您可以使用我们提供的[数据集划分工具](./tools/Partitioning-dataset.py)

程序将自动把数据集按照您给的比例划分成训练集，测试集和验证集。

同时还会生成指定`train.txt`,`test.txt`,`val.txt`,指明各个数据集中每张图片的路径

最后，请您自行编写`data.yaml`文件，格式如下：

```
train: path/to/train.txt
val: path/to/val.txt
test: path/to/test.txt
nc: 1
names: ["object name"]
```

### 模型训练

```
from ultralytics import YOLO
model = YOLO('yolov8n-obb.yaml')  # build a new model from YAML
model = YOLO('yolov8n-obb.pt')  # load a pretrained model (recommended for training)
model = YOLO('yolov8n-obb.yaml').load('yolov8n.pt')  # build from YAML and transfer weights
results = model.train(cfg="./ultralytics/cfg/default.yaml",epochs=1,workers=4)
```
有关model.train()函数的各个参数，在YOLO-OBB的使用章节已经阐述，这里不再过多赘述
### 模型预测
```
from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n-obb.pt')  # load an official model
model = YOLO('path/to/best.pt')  # load a custom model

# Predict with the model
results = model(‘path/to/images/'，stream=False)  # predict on an image

#for result in results:
#    boxes = result.boxes  # Boxes object for bbox outputs
#    masks = result.masks  # Masks object for segmentation masks outputs
#    keypoints = result.keypoints  # Keypoints object for pose outputs
#    probs = result.probs  # Probs object for classification outputs
```

### 半自动标注方法
- 自行制备一个小的数据集，训练一个YOLO-OBB模型
- 用该模型对剩下的图片进行预测，设置`save_txt=True`保存预测旋转框坐标的txt文件
- 利用[txt转xml工具](./tools/txt_to_xml.py)工具，将txt文件转为RolabelImg可识别的xml文件
- 在RolabelImg上微调标注

### YOLO-OBB融合SAM　

修改思路
- 将YOLO-OBB进行NMS处理之前，将预测的BOX传进SAM进行语义分割
- 利用YOLO的参数传递机制，提供友好的SAM调用API
- 将YOLO-OBB的预测结果映射成`多点+多框提示`

修改ultralytics-main\ultralytics\models\yolo\obb\predict.py文件，这样做的好处是：
- 平衡了SAM和YOLO-OBB速度差异较大的问题
- 一次性加载SAM模型和YOLO-OBB模型，运行期间只需调用模型即可，节省多次加载模型的时间
- YOLO-OBB的输出结果直接传入SAM，免去了传统的YOLO-OBB写文件，SAM读文件的繁琐
```
import torch
import numpy as np
import cv2
from ultralytics.engine.results import Results
from ultralytics.models.yolo.detect.predict import DetectionPredictor
from ultralytics.utils import DEFAULT_CFG, ops
from ultralytics.engine.results import OBB
from segment_anything import sam_model_registry, SamPredictor
class OBBPredictor(DetectionPredictor):
    """
    A class extending the DetectionPredictor class for prediction based on an Oriented Bounding Box (OBB) model.

    Example:
        ```python
        from ultralytics.utils import ASSETS
        from ultralytics.models.yolo.obb import OBBPredictor

        args = dict(model='yolov8n-obb.pt', source=ASSETS)
        predictor = OBBPredictor(overrides=args)
        predictor.predict_cli()
        ```
    """

    def __init__(self,
                 cfg=DEFAULT_CFG,
                 overrides=None,
                 _callbacks=None,
                 ):
        """Initializes OBBPredictor with optional model and data configuration overrides."""
        super().__init__(cfg, overrides, _callbacks)
        self.args.task = "obb"
        if self.args.use_sam:
            mapping = {
                "default": ["small.pth", "vit_b"],
                "small": ["small.pth", "vit_b"],
                "middle": ["middle.pth", "vit_l"],
                "large": ["large.pth", "vit_h"]
            }
            checkpoint = "../ultralytics-main/weights/SAM/" + mapping[self.args.model_type][0]
            device = "cuda"
            sam = sam_model_registry[mapping[self.args.model_type][1]](checkpoint=checkpoint)
            sam.to(device=device)
            self.predictor = SamPredictor(sam)

    def postprocess(self, preds, img, orig_imgs,):
        """Post-processes predictions and returns a list of Results objects."""
        preds = ops.non_max_suppression(
            preds,
            self.args.conf,
            self.args.iou,
            agnostic=self.args.agnostic_nms,
            max_det=self.args.max_det,
            nc=len(self.model.names),
            classes=self.args.classes,
            rotated=True,
        )

        if not isinstance(orig_imgs, list):  # input images are a torch.Tensor, not a list
            orig_imgs = ops.convert_torch2numpy_batch(orig_imgs)

        results = []
        for pred, orig_img, img_path in zip(preds, orig_imgs, self.batch[0]):
            pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], orig_img.shape, xywh=True)
            # xywh, r, conf, cls
            obb = torch.cat([pred[:, :4], pred[:, -1:], pred[:, 4:6]], dim=-1)
            if self.args.use_sam:
                image=self.sam_predict(orig_img,obb)
                results.append(Results(image, path=img_path, names=self.model.names, obb=obb))
            else:
                results.append(Results(orig_img, path=img_path, names=self.model.names, obb=obb))
        return results

    def sam_predict(self,image,obb):

        if obb.numel()!=0:
            obbs = OBB(obb, image.shape[0:2])
            obbs = obbs.xyxyxyxy.reshape(-1, 1, 8).squeeze()
            if obbs.dim()==1:
                obbs=obbs.unsqueeze(0)

            x = obbs[:, [0, 2, 4, 6]]
            y = obbs[:, [1, 3, 5, 7]]

            x_max,x_min =torch.max(x, dim=1).values,torch.min(x, dim=1).values
            y_max,y_min =torch.max(y, dim=1).values,torch.min(y, dim=1).values
            boxs=torch.stack((x_min,y_min,x_max,y_max ), dim=0).t()


            x_mid=(x_max+x_min)/2
            y_mid=(y_max+y_min)/2
            points=torch.stack((x_mid,y_mid), dim=0).t().unsqueeze(0)
            labels=torch.ones(1,points.shape[1],dtype=torch.int8)

            self.predictor.set_image(image)
            transformed_boxes = self.predictor.transform.apply_boxes_torch(boxs, image.shape[:2])
            transformed_points = self.predictor.transform.apply_coords_torch(points, image.shape[:2])

            masks, _, _ = self.predictor.predict_torch(
                point_coords=transformed_points if self.args.use_points else None,
                point_labels=labels if self.args.use_points else None,
                boxes=transformed_boxes if self.args.use_boxs else None,
                multimask_output=False,
            )
            masks=masks.cpu().numpy()
            points=points.cpu().numpy()
            x_cat = np.zeros_like(masks[0])
            for mask in masks:
                x_cat = np.logical_or(x_cat, mask)
            h, w = x_cat.shape[-2:]
            #color = np.random.random(3)
            color = np.array([0.78,0.08,0.91])
            mask_image = (x_cat.reshape(h, w, 1) * color.reshape(1, 1, -1) * 255).astype(np.uint8)
            result = cv2.addWeighted(image, 1, mask_image, 0.5, 0)

            if self.args.use_points and points is not None :
                points=points.reshape((-1,2)).astype(np.int32)
                for point in points:
                    cv2.circle(result, tuple(point), 5, (0, 255, 0), -1)
            return result
        else:
            return image
```
修改ultralytics-main\ultralytics\cfg\default.yaml文件

```
# Visualize settings ---------------------------------------------------------------------------------------------------
show: False  # (bool) show predicted images and videos if environment allows
save_frames: False  # (bool) save predicted individual video frames
save_txt: False  # (bool) save results as .txt file
save_conf: False  # (bool) save results with confidence scores
save_crop: False  # (bool) save cropped images with results
show_labels: True  # (bool) show prediction labels, i.e. 'person'
show_conf: True  # (bool) show prediction confidence, i.e. '0.99'
show_boxes: True  # (bool) show prediction boxes
line_width: 5  # (int, optional) line width of the bounding boxes. Scaled to image size if None.

use_sam: True #是否使用SAM
use_points: True #是否使用点提示
use_boxs: True #是否使用框提示
model_type: small #使用SAM的哪个模型
```
用YOLO-OBB+SAM预测
```
from ultralytics import YOLO
model = YOLO('weights/best.pt')  # load a custom model
results = model('F:/GGbone/Isolator/images/0341.jpg',stream=True,
                save=True,save_txt=False,
                show_labels=False,show_conf=False,show_boxes=True,
                use_sam=True,use_boxs=True,use_points=True,model_type="small"
                )

for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs```
```
最后，请欣赏模型之间的碰撞之美

|     Original Image      |      Points_prompt       |
|:-----------------------:|:------------------------:|
| ![](./images/0025.jpg)  | ![](./images/0025p.jpg)  |
|      Boxes_prompt       | Points and Boxes_prompt  |
| ![](./images/0025b.jpg) | ![](./images/0025bp.jpg) |
