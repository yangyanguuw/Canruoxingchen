# 灿若星辰
一些奇思妙想+一点点魔法
# 当 YOLO-OBB 遇上 Edge SAM
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
