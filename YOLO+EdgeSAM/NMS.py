import numpy as np
import torch
import torchvision
import torch.nn.functional as F
from typing import Tuple
import cv2

def non_max_suppression(
    prediction,
    conf_thres=0.25,
    iou_thres=0.45,
    classes=None,
    agnostic=False,
    multi_label=False,
    labels=(),
    max_det=300,
    nc=0,  # number of classes (optional)
    max_time_img=0.05,
    max_nms=30000,
    max_wh=7680,
    rotated=False,
):

    # Checks
    assert 0 <= conf_thres <= 1, f"Invalid Confidence threshold {conf_thres}, valid values are between 0.0 and 1.0"
    assert 0 <= iou_thres <= 1, f"Invalid IoU {iou_thres}, valid values are between 0.0 and 1.0"
    bs = prediction.shape[0]  # batch size图片数
    nc = nc or (prediction.shape[1] - 4)  # number of classes
    nm = prediction.shape[1] - nc - 4
    mi = 4 + nc  # mask start inde
    xc = prediction[:, 4:mi].amax(1) > conf_thres  # candidates
    # Settings
    multi_label &= nc > 1  # multiple labels per box (adds 0.5ms/img)

    prediction = prediction.transpose(-1, -2)  # shape(1,84,6300) to shape(1,6300,84)

    output = [torch.zeros((0, 6 + nm), device=prediction.device)] * bs
    for xi, x in enumerate(prediction):  # image index, image inference
        x = x[xc[xi]]  # confidence

        # If none remain process next image
        if not x.shape[0]:
            continue

        # Detections matrix nx6 (xyxy, conf, cls)
        box, cls, mask = x.split((4, nc, nm), 1)

        if multi_label:
            i, j = torch.where(cls > conf_thres)
            x = torch.cat((box[i], x[i, 4 + j, None], j[:, None].float(), mask[i]), 1)
        else:  # best class only
            conf, j = cls.max(1, keepdim=True)
            x = torch.cat((box, conf, j.float(), mask), 1)[conf.view(-1) > conf_thres]

        # Filter by class
        if classes is not None:
            x = x[(x[:, 5:6] == torch.tensor(classes, device=x.device)).any(1)]

        # Check shape
        n = x.shape[0]  # number of boxes
        if not n:  # no boxes
            continue
        if n > max_nms:  # excess boxes
            x = x[x[:, 4].argsort(descending=True)[:max_nms]]  # sort by confidence and remove excess boxes

        # Batched NMS
        c = x[:, 5:6] * (0 if agnostic else max_wh)  # classes
        scores = x[:, 4]  # scores
        if rotated:
            boxes = torch.cat((x[:, :2] + c, x[:, 2:4], x[:, -1:]), dim=-1)  # xywhr
            i = nms_rotated(boxes, scores, iou_thres)
        else:
            boxes = x[:, :4] + c  # boxes (offset by class)
            i = torchvision.ops.nms(boxes, scores, iou_thres)  # NMS
        i = i[:max_det]  # limit detections

        output[xi] = x[i]
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
        labels = torch.ones((1, obb.shape[0],1), device="cuda" if torch.cuda.is_available() else "cpu",
                            dtype=torch.int32)
        tranformed_labels = torch.cat((labels * 2, labels * 3, labels, labels),dim=2).reshape(1,-1)
        transformed_prompt = apply_coords_torch(prompt, shape)

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


def masks_postprocess(masks: np.ndarray,masks_threshold=0.0):
    masks = masks.squeeze(0).transpose(1, 2, 0)
    masks = cv2.resize(masks, (1024, 1024), interpolation=cv2.INTER_LINEAR)
    masks = masks[:1024, :1024, :]
    masks = cv2.resize(masks, (1024, 1024), interpolation=cv2.INTER_LINEAR)
    masks = masks.transpose(2, 0, 1)[None, :, :, :]
    masks = masks > masks_threshold
    return masks


def draw_mask(masks: torch.Tensor,image: np.ndarray,oragine_shape):

    a=(image.shape[0]-oragine_shape[0])//2
    b = (image.shape[1] - oragine_shape[1]) // 2
    masks=masks[a:image.shape[0]-a,b:image.shape[1]-b]
    image = image[a:image.shape[0] - a, b:image.shape[1] - b,:]
    color = torch.tensor([[[255, 0, 204]]], device=masks.device, dtype=torch.int8)
    image_mask = masks.reshape(image.shape[0], image.shape[1], 1) * color
    image_mask = image_mask.cpu().numpy()
    result = cv2.addWeighted(image, 1, image_mask.astype(np.uint8), 0.8, 0)

    return result


def masks_postprocess_gpu(masks:torch.Tensor,scores=torch.Tensor,masks_threshold=0.0):

    max_score_indices = torch.argmax(scores, dim=1)  # 形状为 (11,)
    batch_indices = torch.arange(masks.size(0), device="cuda" if torch.cuda.is_available() else "cpu")  # 形状为 (11,)
    masks = masks[batch_indices, max_score_indices].unsqueeze(1)  # 形状为 (11, 1, 256, 256)
    masks = F.interpolate(masks, size=(1024, 1024), mode='bilinear', align_corners=False)
    masks = F.interpolate(masks, size=(1024, 1024), mode='bilinear', align_corners=False)
    masks = masks > masks_threshold
    masks = masks.squeeze(1).any(dim=0)

    return masks

