# Ultralytics YOLO 🚀, AGPL-3.0 license

import torch
import numpy as np
import cv2
from ultralytics.engine.results import Results
from ultralytics.models.yolo.detect.predict import DetectionPredictor
from ultralytics.utils import DEFAULT_CFG, ops
from ultralytics.engine.results import OBB
from edge_sam import sam_model_registry, SamPredictor
import time
from typing import Tuple
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
                "default": ["edge_sam.pth", "edge_sam"],
                "EdgeSAM": ["edge_sam.pth", "edge_sam"],
                "EdgeSAM_3x": ["edge_sam_3x.pth", "edge_sam"],
            }
            checkpoint = "weights/EdgeSAM/" + mapping[self.args.model_type][0]
            device = self.args.device
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
            time1 = time.time()
            xy=obb[:,:2]
            w,h=obb[:,2],obb[:,3]
            longsides,indexs=obb[:,2:4].max(dim=1)
            shortsides,indexs2=obb[:,2:4].min(dim=1)

            angles=obb[:,4]
            tran_angles = torch.where(indexs == 0, angles, angles-0.5*torch.pi)
            cos, sin = (torch.cos, torch.sin)
            cos_values, sin_values = cos(tran_angles), sin(tran_angles)

            if self.args.use_pose_points==1:
                vector = torch.stack((longsides * 0.25 * cos_values, longsides * 0.25 * sin_values)).T
                points = torch.cat((xy + vector, xy - vector), dim=1).reshape(1, -1, 2)
                labels = torch.ones((1, points.shape[1]), device=self.args.device, dtype=torch.int8)
                transformed_points = self.predictor.transform.apply_coords_torch(points, image.shape[:2])
            elif self.args.use_pose_points==0:
                vector = torch.stack((shortsides * 0.5 * sin_values, -shortsides * 0.5 * cos_values)).T
                points = torch.cat((xy + vector, xy - vector), dim=1).reshape(1, -1, 2)
                labels = torch.zeros((1, points.shape[1]), device=self.args.device, dtype=torch.int8)
                transformed_points = self.predictor.transform.apply_coords_torch(points, image.shape[:2])

            if self.args.use_boxs:
                cos_values, sin_values = cos(angles), sin(angles)
                vct1 = 0.5*w*cos_values
                vct2 = 0.5*w*sin_values
                vct3 = 0.5*h*cos_values
                vct4 = 0.5*h*sin_values
                boxes=torch.stack((obb[:,0]-vct1-vct4,obb[:,1]-vct2-vct3,obb[:,0]+vct1+vct4,obb[:,1]+vct2+vct3),dim=1).reshape(-1,4)
                transformed_boxes = self.predictor.transform.apply_boxes_torch(boxes, image.shape[:2])

            time2=time.time()
            #self.predictor.set_image(image)
            self.predictor.set_torch_image(self.img,image.shape[:2])
            time3=time.time()
            masks, _, _ = self.predictor.predict_torch(
                point_coords=transformed_points if self.args.use_pose_points in [0,1] else None,
                point_labels=labels if self.args.use_pose_points in [0,1] else None,
                boxes=transformed_boxes if self.args.use_boxs else None,
                num_multimask_outputs=1
            )

            time4 = time.time()
            masks=masks.reshape(-1,image.shape[0], image.shape[1]).type(torch.uint8)
            masks= masks.any(dim=0)
            color = torch.tensor([[[255,0,204]]],device=self.device,dtype=torch.int8)
            image_mask =masks.reshape(image.shape[0], image.shape[1],1)*color
            image_mask=image_mask.cpu().numpy()
            result=cv2.addWeighted(image, 1, image_mask.astype(np.uint8), 0.8, 0)
            time5=time.time()
            if self.args.use_pose_points in [0,1]:
                points = points.cpu().numpy().astype(np.int32)
                for point in points[0]:
                    cv2.circle(result, tuple(point), 7, (0, 255, 0)if self.args.use_pose_points==1 else (0,0,255), -1)
            time6=time.time()
            print(f"坐标计算：{(time2 - time1) * 1E3:.2f}ms\n图像编码：{(time3 - time2) * 1E3:.2f}ms\nEdgeSAM推理：{(time4 - time3) * 1E3:.2f}ms\n掩膜处理：{(time5 - time4) * 1E3:.2f}ms\n姿态点标注：{(time6 - time5) * 1E3:.2f}ms")


            return result
        else:
            return image


# def obb_process(obb:torch.Tensor, shape=[1024,1024]):
#     if obb.numel() != 0:
#         xy = obb[:, :2]
#         w, h = obb[:, 2], obb[:, 3]
#         longsides, indexs = obb[:, 2:4].max(dim=1)
#
#         angles = obb[:, 4]
#         tran_angles = torch.where(indexs == 0, angles, angles - 0.5 * torch.pi)
#         cos, sin = (torch.cos, torch.sin)
#         cos_values, sin_values = cos(tran_angles), sin(tran_angles)
#
#         vector = torch.stack((longsides * 0.25 * cos_values, longsides * 0.25 * sin_values)).T
#
#         x3 = xy + vector
#         y3 = xy - vector
#         points = torch.cat((x3, y3), dim=1).reshape(-1, 2, 2)
#
#         cos_values, sin_values = cos(angles), sin(angles)
#         vct1 = 0.5 * w * cos_values
#         vct2 = 0.5 * w * sin_values
#         vct3 = 0.5 * h * cos_values
#         vct4 = 0.5 * h * sin_values
#
#         x1 = obb[:, 0] - vct1 - vct4
#         y1 = obb[:, 1] - vct2 - vct3
#         x2 = obb[:, 0] + vct1 + vct4
#         y2 = obb[:, 1] + vct2 + vct3
#         boxes = torch.stack((x1, y1, x2, y2), dim=1).reshape(-1, 2, 2)
#
#         prompt = torch.cat((boxes, points), dim=1).reshape(1,-1,2)
#         labels = torch.ones((1, obb.numel(),1), device="cuda" if torch.cuda.is_available() else "cpu",
#                             dtype=torch.int64)
#
#         tranformed_labels = torch.cat((labels * 2, labels * 3, labels, labels),dim=2).reshape(1,-1)
#         transformed_prompt = apply_coords_torch(prompt, shape)
#         return transformed_prompt, tranformed_labels
#
# def apply_coords_torch(
#     coords: torch.Tensor, original_size: Tuple[int, ...]
# ) -> torch.Tensor:
#
#     old_h, old_w = original_size
#
#     scale = 1024 * 1.0 / max(old_h, old_w)
#     new_h, new_w = old_h * scale, old_w * scale
#     new_w = int(new_w + 0.5)
#     new_h = int(new_h + 0.5)
#
#     coords[..., 0] = coords[..., 0] * (new_w / old_w)
#     coords[..., 1] = coords[..., 1] * (new_h / old_h)
#     return coords



# alpha = 1.0  # tensor1 的权重
# beta = 0.8  # tensor2 的权重
# image = torch.from_numpy(image).float().to(self.device)
# image_mask = image_mask.to(torch.float32)
# result = alpha * image + beta * image_mask
# result = result.clamp(0, 255).to(torch.uint8)
# result=result.cpu().numpy()
# time5 = time.time()


# obbs = OBB(obb, image.shape[0:2])
# obbs = obbs.xyxyxyxy.reshape(-1, 8)
#
# time_2=time.time()
# x = obbs[:, [0, 2, 4, 6]]
# y = obbs[:, [1, 3, 5, 7]]
#
# x_max,_ = torch.max(x, dim=1)
# x_min,_ = torch.min(x, dim=1)
# y_max,_ = torch.max(y, dim=1)
# y_min,_ = torch.min(y, dim=1)
#
# boxs=torch.stack((x_min,y_min,x_max,y_max ), dim=1)

# θ_based OBB
# if self.args.use_pose_points:
#     center = obb[:, :5]
#     cos, sin = (torch.cos, torch.sin)
#     ctrs = center[..., :2]
#     w, h, angle = (center[..., i: i + 1] for i in range(2, 5))
#
#     longsides, indexes = torch.cat((w, h), dim=1).max(dim=1)
#     longsides = longsides.reshape(-1, 1)
#     cos_values, sin_values = cos(angle), sin(angle)
#     points = torch.empty((1, 0, 2), device=self.args.device)
#
#     for ctr, longside, index, cos_value, sin_value in zip(ctrs, longsides, indexes, cos_values, sin_values):
#         if index == 0:
#             vector = [longside / 4 * cos_value, longside / 4 * sin_value]
#             vector = torch.cat(vector, dim=-1)
#             pt1 = (ctr + vector).reshape(1, 1, 2)
#             pt2 = (ctr - vector.reshape(1, 1, 2))
#             points = torch.cat((points, pt1, pt2), dim=1)
#         else:
#             vector = [longside / 4 * sin_value, -longside / 4 * cos_value]
#             vector = torch.cat(vector, dim=-1)
#             pt1 = (ctr + vector).reshape(1, 1, 2)
#             pt2 = (ctr - vector).reshape(1, 1, 2)
#             points = torch.cat((points, pt1, pt2), dim=1)
#     labels = torch.ones((1, points.shape[1]), dtype=torch.int32)

# point_based OBB
#     if self.args.use_pose_points:
#         points=torch.empty(0,device=self.args.device)
#         for obb in obbs:
#             side1=torch.norm(obb[:2]-obb[2:4]) #12
#             side2=torch.norm(obb[2:4]-obb[4:6])#23
#
#             if side1>side2:
#                 lscp= ((obb[:2] + obb[2:4]) / 2)
#                 forward_point1 = ((lscp + obb[4:6]) / 2)
#                 forward_point2 = ((lscp + obb[6:]) / 2)
#                 points = torch.cat((points, forward_point1, forward_point2), dim=0)
#
#             else:
#                 lscp = ((obb[2:4] + obb[4:6]) / 2)
#                 forward_point1 = ((lscp + obb[:2]) / 2)
#                 forward_point2 = ((lscp + obb[6:]) / 2)
#                 points=torch.cat((points,forward_point1, forward_point2),dim=0)
#         points=points.reshape(1,-1,2)
#         labels = torch.ones((1,points.shape[1]), dtype=torch.int8)
#         transformed_points = self.predictor.transform.apply_coords_torch(points, image.shape[:2])
#