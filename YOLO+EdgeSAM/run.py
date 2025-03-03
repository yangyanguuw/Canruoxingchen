                                        # train

#from ultralytics import YOLO
# model = YOLO('yolov8n-cls.yaml')  # build a new model from YAML
# model = YOLO('yolov8n-cls.pt')  # load a pretrained model (recommended for training)
# model = YOLO('yolov8n-cls.yaml').load('weights/yolov8n.pt')  # build from YAML and transfer weights
# results = model.train(data="C:/Users/17339/Desktop/data-seg/data.yaml",epochs=300)


                                         # predict
#
from ultralytics import YOLO
model = YOLO('weights/best.pt')  # load a custom model
results = model(source='./UI/example/0003.jpg',
                show=True,
                stream=True,save=True,#save_dir="F:/GGbone/Isolator/",
                show_labels=False,show_conf=True,show_boxes=True,
                use_sam=True,use_boxs=True,use_pose_points=1,model_type="EdgeSAM_3x")

for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs


                                    # predict by tensorRT
# from ultralytics import YOLO
# tensorrt_model = YOLO('weights/best.pt',task='obb')
# results = tensorrt_model('./UI/example/0001.jpg',save=True,use_sam=True,stream=True,model_type="EdgeSAM_3x")
# for result in results:
#     boxes = result.boxes# Boxes object for bbox outputs



                                        #yolov8n-seg

# from ultralytics import YOLO
#
# # Load a model
# model = YOLO('weights/last.pt')  # load a custom model
# # Predict with the model
# results = model('./UI/example/0002.mp4',save=True,show_labels=False,show_conf=True,show_boxes=False,stream=True,)  # predict on an image
# for result in results:
#     boxes = result.boxes  # Boxes object for bbox outputs
#     masks = result.masks
