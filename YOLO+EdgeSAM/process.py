import numpy as np
import torch
import time
import cv2
from typing import Tuple
from copy import deepcopy

def non_max_suppression(
    prediction,
    conf_thres=0.25,
    iou_thres=0.45,
    max_det=300,
    max_time_img=0.05,
):
    bs = prediction.shape[0]  # batch size图片数
    nc = 2  # number of classes
    nm = prediction.shape[1]-6
    xc = prediction[:, 4:6].amax(1) > conf_thres  # candidates

    # Settings
    time_limit = 0.5 + max_time_img * bs  # seconds to quit after

    prediction = prediction.transpose(-1, -2)
    t = time.time()
    output = [torch.zeros((0, 6 + nm), device="cpu")] * bs

    for xi, x in enumerate(prediction):  # image index, image inference
        # Apply constraints
        x = x[xc[xi]]  # confidence

        # If none remain process next image
        if not x.shape[0]:
            continue

        # Detections matrix nx6 (xyxy, conf, cls)
        box, cls,theta = x.split((4, nc,1), 1)

        conf, j = cls.max(1, keepdim=True)
        x = torch.cat((box, theta,conf,j.float()), 1)[conf.view(-1) > conf_thres]

        # Check shape
        n = x.shape[0]  # number of boxes
        if not n:  # no boxes
            continue

        # Batched NMS
        c = x[:, 6:7] * 7680  # classes
        boxes = torch.cat((x[:, :2]+c , x[:, 2:4], x[:, 4:5]), dim=-1)  # xywhr
        i = nms_rotated(boxes, conf.reshape(-1), iou_thres)
        i = i[:max_det]  # limit detections

        output[xi] = x[i]
        if (time.time() - t) > time_limit:
            print(f"WARNING ⚠️ NMS time limit {time_limit:.3f}s exceeded")
            break  # time limit exceeded
    return output


def nms_rotated(boxes, scores, threshold=0.45):
    if len(boxes) == 0:
        return np.empty((0,), dtype=np.int8)
    sorted_idx = torch.argsort(scores, descending=True)
    boxes = boxes[sorted_idx]
    ious = batch_probiou(boxes, boxes).triu_(diagonal=1)
    pick = torch.nonzero(ious.max(dim=0)[0] < threshold).squeeze_(-1)
    return sorted_idx[pick]


def batch_probiou(obb1, obb2, eps=1e-7):
    x1, y1 = obb1[..., :2].split(1, dim=-1)
    x2, y2 = (x.squeeze(-1)[None] for x in obb2[..., :2].split(1, dim=-1))
    a1, b1, c1 = _get_covariance_matrix(obb1)
    a2, b2, c2 = (x.squeeze(-1)[None] for x in _get_covariance_matrix(obb2))

    t1 = (
        ((a1 + a2) * (torch.pow(y1 - y2, 2)) + (b1 + b2) * (torch.pow(x1 - x2, 2)))
        / ((a1 + a2) * (b1 + b2) - (torch.pow(c1 + c2, 2)) + eps)
    ) * 0.25
    t2 = (((c1 + c2) * (x2 - x1) * (y1 - y2)) / ((a1 + a2) * (b1 + b2) - (torch.pow(c1 + c2, 2)) + eps)) * 0.5
    t3 = (
        torch.log(
            ((a1 + a2) * (b1 + b2) - (torch.pow(c1 + c2, 2)))
            / (4 * torch.sqrt((a1 * b1 - torch.pow(c1, 2)).clamp_(0) * (a2 * b2 - torch.pow(c2, 2)).clamp_(0)) + eps)
            + eps
        )
        * 0.5
    )
    bd = t1 + t2 + t3
    bd = torch.clamp(bd, eps, 100.0)
    hd = torch.sqrt(1.0 - torch.exp(-bd) + eps)
    return 1 - hd


def _get_covariance_matrix(boxes):
    # Gaussian bounding boxes, ignored the center points(the first two columns) cause it's not needed here.
    gbbs = torch.cat((torch.pow(boxes[:, 2:4], 2) / 12, boxes[:, 4:]), dim=-1)
    a, b, c = gbbs.split(1, dim=-1)
    return (
        a * torch.cos(c) ** 2 + b * torch.sin(c) ** 2,
        a * torch.sin(c) ** 2 + b * torch.cos(c) ** 2,
        a * torch.cos(c) * torch.sin(c) - b * torch.sin(c) * torch.cos(c),
    )


def xywhr2xyxyxyxy(center):

    is_numpy = isinstance(center, np.ndarray)
    cos, sin = (np.cos, np.sin) if is_numpy else (torch.cos, torch.sin)

    ctr = center[..., :2]
    w, h, angle = (center[..., i : i + 1] for i in range(2, 5))
    cos_value, sin_value = cos(angle), sin(angle)
    vec1 = [w / 2 * cos_value, w / 2 * sin_value]
    vec2 = [-h / 2 * sin_value, h / 2 * cos_value]
    vec1 = np.concatenate(vec1, axis=-1) if is_numpy else torch.cat(vec1, dim=-1)
    vec2 = np.concatenate(vec2, axis=-1) if is_numpy else torch.cat(vec2, dim=-1)
    pt1 = ctr + vec1 + vec2
    pt2 = ctr + vec1 - vec2
    pt3 = ctr - vec1 - vec2
    pt4 = ctr - vec1 + vec2
    return np.stack([pt1, pt2, pt3, pt4], axis=-2) if is_numpy else torch.stack([pt1, pt2, pt3, pt4], dim=-2)


def obb_process(obb:torch.Tensor, shape=[1024,1024]):
    if obb.numel() != 0:
        xy = obb[:, :2]
        w, h = obb[:, 2], obb[:, 3]
        longsides, indexs = obb[:, 2:4].max(dim=1)

        angles = obb[:, 4]
        tran_angles = torch.where(indexs == 0, angles, angles - 0.5 * torch.pi)
        cos, sin = (torch.cos, torch.sin)
        cos_values, sin_values = cos(tran_angles), sin(tran_angles)

        vector = torch.stack((longsides * 0.25 * cos_values, longsides * 0.25 * sin_values)).T

        x3 = xy + vector
        y3 = xy - vector
        points = torch.cat((x3, y3), dim=1).reshape(-1, 2, 2)

        cos_values, sin_values = cos(angles), sin(angles)
        vct1 = 0.5 * w * cos_values
        vct2 = 0.5 * w * sin_values
        vct3 = 0.5 * h * cos_values
        vct4 = 0.5 * h * sin_values

        x1 = obb[:, 0] - vct1 - vct4
        y1 = obb[:, 1] - vct2 - vct3
        x2 = obb[:, 0] + vct1 + vct4
        y2 = obb[:, 1] + vct2 + vct3
        boxes = torch.stack((x1, y1, x2, y2), dim=1).reshape(-1, 2, 2)

        prompt = torch.cat((boxes, points), dim=1).reshape(1,-1,2)
        labels = torch.ones((1, obb.numel(),1), device="cuda" if torch.cuda.is_available() else "cpu",
                            dtype=torch.int64)

        tranformed_labels = torch.cat((labels * 2, labels * 3, labels, labels),dim=2).reshape(1,-1)
        transformed_prompt = apply_coords_torch(prompt, shape)

        print(transformed_prompt)
        return transformed_prompt, tranformed_labels


def apply_coords_torch(
    coords: torch.Tensor, original_size: Tuple[int, ...]
) -> torch.Tensor:

    old_h, old_w = original_size

    scale = 1024 * 1.0 / max(old_h, old_w)
    new_h, new_w = old_h * scale, old_w * scale
    new_w = int(new_w + 0.5)
    new_h = int(new_h + 0.5)

    coords[..., 0] = coords[..., 0] * (new_w / old_w)
    coords[..., 1] = coords[..., 1] * (new_h / old_h)
    return coords

def apply_boxes_torch(
    boxes: torch.Tensor, original_size: Tuple[int, ...]
) -> torch.Tensor:

    boxes = apply_coords_torch(boxes.reshape(-1, 2, 2), original_size)
    return boxes.reshape(-1, 4)
