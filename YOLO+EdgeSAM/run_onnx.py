import onnxruntime as ort
import cv2
from process import *

img = cv2.imread("C:/Users/17339/Desktop/1/0004.jpg")
img=cv2.resize(img, (1024,1024), interpolation=cv2.INTER_AREA)
input_data = img/255
input_data = np.transpose(input_data, (2, 0, 1)).astype(np.float32)
input_data = input_data.reshape([-1, 3, 1024,1024])


sess = ort.InferenceSession("weights/best.onnx",providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])#
input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name
time1=time.time()
pred= sess.run([output_name], {input_name: input_data})
time2=time.time()
pred=torch.tensor(pred[0],device="cpu")
result=non_max_suppression(pred,iou_thres=0.45)[0].numpy()
boxes=xywhr2xyxyxyxy(result[...,:6]).astype(np.int32)
for poly in boxes:
    # 绘制填充的多边形
    cv2.polylines(img, [poly], isClosed=True, color=(255, 0, 0), thickness=2)

cv2.imwrite("C:/Users/17339/Desktop/0004.jpg",img)
time3=time.time()
print(f"预测速度：{(time2 - time1) * 1E3}ms,\n后处理速度：{(time3 - time2) * 1E3}ms")
