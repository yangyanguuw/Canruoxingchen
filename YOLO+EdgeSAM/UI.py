import gradio as gr
import os
from PIL import Image
import ffmpeg
import cv2
from ultralytics import YOLO
import cv2
import numpy as np



description_b = """ ## 框提示语义分割介绍

                在此模式下，EdgeSAM模型将采用框提式进行语义分割
                
                1. 上传图片或者点击示例图片.
                2. 选择EdgeSAM模型.
                3. 点击重置按钮重置图像.
                

              """

description_p = """ ## 点框结合语义分割介绍

                在此模式下，EdgeSAM模型将采用框提示+前景姿态点作为提式进行语义分割

                1. 上传图片或者点击示例图片.
                2. 选择EdgeSAM模型.
                3. 点击重置按钮重置图像.

              """


pic_examples = [
    ["UI/example/0001.jpg"],
    ["UI/example/0002.jpg"],
    ["UI/example/0003.jpg"],
    ["UI/example/0004.jpg"],
    ["UI/example/0005.jpg"]
]

vid_examples = [
    ["UI/example/0001.mp4","UI/example/0001.mp4"],
    ["UI/example/0002.mp4","UI/example/0002.mp4"],
    ["UI/example/0003.mp4","UI/example/0003.mp4"]
]

def pic_segment(image, mode , seg_model):
    mapping = {
        "Boxes": 2,
        "Boxes+Pose-Points": 1,
        "Boxes+Background-Points": 0,
    }
    r,g,b = cv2.split(image)
    image = cv2.merge([b,g,r])
    save_dir = "./UI/predict/"
    os.makedirs(save_dir, exist_ok=True)
    model = YOLO('../weights/best.pt')
    results = model(
                source=image,
                stream=True,
                save=True,
                save_dir=save_dir,
                show_labels=False,
                use_sam=True,
                use_boxs=True,
                use_pose_points=mapping[mode],
                model_type=seg_model
                )
    for result in results:
        boxes = result.boxes  # Boxes object for bbox outputs

    img=Image.open(save_dir+"image0.jpg")
    return img


def vid_segment(path, mode, seg_model):
    mapping = {
        "Boxes": 2,
        "Boxes+Pose-Points": 1,
        "Boxes+Background-Points": 0,
    }
    name=path.split("\\")[-1]
    save_dir="UI/predict/"
    os.makedirs(save_dir, exist_ok=True)
    model = YOLO('../weights/best.pt')
    results = model.predict(
        source=path,
        stream=True,
        save=True,
        save_dir=save_dir,
        use_sam=True,
        use_boxs=True,
        show_labels=False,
        use_pose_points=mapping[mode],
        model_type=seg_model
    )
    for result in results:
        boxes = result.boxes  # Boxes object for bbox outputs

    capture = cv2.VideoCapture(save_dir+name.replace(".mp4", ".avi"))

    fps = capture.get(cv2.CAP_PROP_FPS)  # 获取帧率
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    suc = capture.isOpened()
    allFrame = []
    while suc:
        suc, frame = capture.read()
        if suc:
            allFrame.append(frame)
    capture.release()

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    videoWriter = cv2.VideoWriter(save_dir+name, fourcc, fps, size)
    for aFrame in allFrame:
        videoWriter.write(aFrame)
    videoWriter.release()

    return  save_dir+name


def pic_reset():
   return ["Boxes","EdgeSAM",None,None]


def pic_update_markdown(mode):
    if mode=="Boxes":
        return description_b
    else:
        return description_p

def vid_reset():
   return ["Boxes","EdgeSAM",None,None]


def vid_update_markdown(mode):
    if mode=="Boxes":
        return description_b
    else:
        return description_p

def prosee(path):
    return path

with gr.Blocks(title="YOLO-OBB+EdgeSAM") as demo:
    title = "<center><strong><font size='8'>YOLO+EdgeSAM<font></strong> </center>"
    with gr.Tab("图片分割") as tab_p:
        with gr.Row():
            img_in = gr.Image(label="输入图像")
            img_out = gr.Image(label="输出图像")
        with gr.Row():
            with gr.Column(scale=1):
                pic_mode=gr.Radio(choices=["Boxes","Boxes+Pose-Points","Boxes+Background-Points"],value="Boxes",label="选择分割模式")
                pic_seg_model=gr.Dropdown(choices=["EdgeSAM", "EdgeSAM_3x"],value="EdgeSAM", label="请选择EdgeSAM模型")

                with gr.Row():
                    pic_reset_bt=gr.Button("重置")
                    pic_confirm=gr.Button("分割")
                    pic_confirm.click(
                        fn=pic_segment,
                        inputs=[img_in,pic_mode,pic_seg_model],
                        outputs=img_out
                    )
                    pic_reset_bt.click(
                        fn=pic_reset,
                        inputs=[],
                        outputs=[pic_mode,pic_seg_model,img_in,img_out]
                    )
            with gr.Column(scale=1):
                pic_markdown=gr.Markdown(description_b)
                pic_mode.change(pic_update_markdown,inputs=pic_mode, outputs=pic_markdown)

        pic_example=gr.Examples(
                examples=pic_examples,
                inputs=[img_in])
    with gr.Tab("视频分割") as tab_v:
        with gr.Row():
            vid_in = gr.Video(label="输入视频")
            vid_out = gr.Video(label="输出视频")
        with gr.Row():
            with gr.Column(scale=7):
                with gr.Row():
                    file_in = gr.File(label="选择输入文件", scale=8,height=40)
                    vid_pro_bt = gr.Button("预览", scale=2, size="sm")
                    vid_pro_bt.click(
                        fn=prosee,
                        inputs=[file_in],
                        outputs=[vid_in]
                    )
                with gr.Row():
                    vid_mode = gr.Radio(choices=["Boxes", "Boxes+Pose-Points","Boxes+Background-Points"],
                                        value="Boxes",
                                        label="选择分割模式")
                    vid_seg_model = gr.Dropdown(choices=["EdgeSAM", "EdgeSAM_3x"],
                                                value="EdgeSAM",
                                                label="请选择EdgeSAM模型")
                with gr.Row():
                    vid_reset_bt = gr.Button("重置")
                    vid_confirm = gr.Button("分割")
                    vid_confirm.click(
                        fn=vid_segment,
                        inputs=[file_in, vid_mode, vid_seg_model],
                        outputs=[vid_out]
                    )
                    vid_reset_bt.click(
                        fn=vid_reset,
                        inputs=[],
                        outputs=[vid_mode, vid_seg_model, vid_in,vid_out]
                    )
            with gr.Column(scale=3):
                gr.Examples(
                    label="分割实例",
                    examples=vid_examples,
                    inputs=[vid_in, file_in]
                )

        vid_markdown = gr.Markdown(description_b)
        vid_mode.change(vid_update_markdown, inputs=vid_mode, outputs=vid_markdown)





demo.launch()