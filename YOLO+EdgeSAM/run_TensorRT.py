import cv2
import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
import tensorrt as trt
import cupy as cp
import time

import torch
from torch.utils.dlpack import to_dlpack,from_dlpack
from NMS import *
from loader import *

# 图像预处理
def preprocess(im):
    im = im[..., ::-1].transpose((0, 3, 1, 2))  # BGR to RGB, BHWC to BCHW, (n, 3, h, w)
    im = np.ascontiguousarray(im)  # contiguous
    im = im.astype(np.float32)  # uint8 to fp16/32
    im /= 255  # 0 - 255 to 0.0 - 1.0
    return im


# 加载engine
def load_engine(engine_path):
    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
    with open(engine_path, 'rb') as f, trt.Runtime(TRT_LOGGER) as runtime:
        engine = runtime.deserialize_cuda_engine(f.read())
    return engine


# 为输入输出分配显存
def allocate_buffers(engine,max_input_shapes=None, max_output_shapes=None,shared_buffer=None):
    inputs = []
    outputs = []

    if shared_buffer is not None:
        # 共享encoder和decoder的内存
        inputs.append(shared_buffer)

    if max_input_shapes is not None:
        # 为每个输入分配 GPU 内存
        for max_shape in max_input_shapes:
            shape = trt.volume(max_shape)
            dtype = trt.nptype(engine.get_binding_dtype(len(inputs)))
            input_buffer = cuda.mem_alloc(shape * np.dtype(dtype).itemsize)
            inputs.append(input_buffer)

    if max_output_shapes is not None:
        # 为每个输入分配 GPU 内存
        for max_shape in max_output_shapes:
            shape = trt.volume(max_shape)
            dtype = trt.nptype(engine.get_binding_dtype(len(inputs)))
            output_buffer = cuda.mem_alloc(shape * np.dtype(dtype).itemsize)
            outputs.append(output_buffer)

    stream = cuda.Stream()
    return inputs,outputs, stream


# Helper function to perform inference
def inference(context, inputs, outputs, stream):
    context.execute_async_v2(bindings=[int(input) for input in inputs]+[int(output) for output in outputs], stream_handle=stream.handle)

# 加载engine
yolo_engine = load_engine('./weights/best.engine')
encoder_engine = load_engine('./weights/EdgeSAM/edge_sam_3x_encoder.engine')
decoder_engine = load_engine('./weights/EdgeSAM/edge_sam_3x_decoder_batch.engine')

# 创建engine上下文
yolo_context = yolo_engine.create_execution_context()
encoder_context = encoder_engine.create_execution_context()
decoder_context = decoder_engine.create_execution_context()

# 获取输入,输出shape
input_shape = trt.volume(yolo_engine.get_binding_shape(0))
input_dtype = trt.nptype(yolo_engine.get_binding_dtype(0))

yolo_output_shape = trt.volume(yolo_engine.get_binding_shape(1))

# 分配共享缓冲区
shared_buffer = cuda.mem_alloc(input_shape * np.dtype(input_dtype).itemsize)

max_input_shapes = [(1, 100,2), (1, 100)]
max_output_shapes =[(100,4,256,256),(100,4)]
yolo_input, yolo_output, yolo_stream = allocate_buffers(yolo_engine, max_input_shapes=None,max_output_shapes=[(1,7,21504)],shared_buffer=shared_buffer)
encoder_input, encoder_output, encoder_stream = allocate_buffers(encoder_engine, max_input_shapes=None, max_output_shapes=[(100,256,64,64)],shared_buffer=shared_buffer)
decoder_inputs, decoder_outputs, decoder_stream= allocate_buffers(decoder_engine, max_input_shapes,max_output_shapes, shared_buffer=encoder_output[0])

s=0.0
s1=0.0
s2=0.0
s3=0.0
s4=0.0
s5=0.0

dataset=load_inference_source(0,[1024,1024],1,False)
for batch in dataset:
    time1=time.time()
    path, img, vid_cap, s = batch
    img=img[0]
    oragine_shape = img.shape
    a=(1024-img.shape[0])//2
    b=(1024-img.shape[1])//2
    img = cv2.copyMakeBorder(img, a,a,b,b, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    img = np.expand_dims(img, axis=0)
    input_data = preprocess(img)

    cuda.memcpy_htod(shared_buffer, input_data)
    inference(yolo_context, yolo_input, yolo_output, yolo_stream)
    inference(encoder_context,encoder_input, encoder_output, encoder_stream)
    cuda.Context.synchronize()

    # cuda -> Tensor
    yolo_output_ptr = cp.cuda.MemoryPointer(cp.cuda.UnownedMemory(int(yolo_output[0]), yolo_output_shape * np.dtype(np.float32).itemsize, None), 0)
    yolo_output_cupy = cp.ndarray(yolo_output_shape, dtype=cp.float32, memptr=yolo_output_ptr)
    yolo_result = from_dlpack(yolo_output_cupy.toDlpack()).reshape(-1,7,21504)

    # 后处理
    preds = non_max_suppression(
        yolo_result,
        0.6,
        0.7,
        agnostic=False,
        max_det=300,
        nc=2,
        classes=None,
        rotated=True,
    )[0]

    preds = torch.cat((preds[:, :4], preds[:, -1:], preds[:, 4:6]), dim=1)

    if preds.numel()==0:
        masks=torch.zeros((1024,1024),device="cuda" if torch.cuda.is_available() else "cpu")
        result = draw_mask(masks, img[0], oragine_shape=oragine_shape)
        show(result)
        continue
    prompt,labels=obb_process(preds)

    # time3 = time.time()

    prompt_ptr = prompt.data_ptr()
    labels_ptr = labels.data_ptr()

    cuda.memcpy_dtod_async(int(decoder_inputs[1]), prompt_ptr, prompt.numel() * prompt.element_size())
    cuda.memcpy_dtod_async(int(decoder_inputs[2]), labels_ptr, labels.numel() * labels.element_size())

    decoder_context.set_binding_shape(1, prompt.shape)
    decoder_context.set_binding_shape(2, labels.shape)

    inference(decoder_context, decoder_inputs, decoder_outputs, decoder_stream)

    cuda.Context.synchronize()

    masks_shape = trt.volume((preds.shape[0], 4, 256, 256))
    scores_shape = trt.volume((preds.shape[0], 4))

    # cuda -> Tensor
    mask_ptr = cp.cuda.MemoryPointer(
        cp.cuda.UnownedMemory(int(decoder_outputs[0]), masks_shape * np.dtype(np.float32).itemsize, None), 0)
    socore_ptr = cp.cuda.MemoryPointer(
        cp.cuda.UnownedMemory(int(decoder_outputs[1]), scores_shape * np.dtype(np.float32).itemsize, None), 0)

    masks = cp.ndarray(masks_shape, dtype=cp.float32, memptr=mask_ptr)
    scores = cp.ndarray(scores_shape, dtype=cp.float32, memptr=socore_ptr)

    masks = from_dlpack(masks.toDlpack()).reshape(-1, 4, 256, 256)
    scores = from_dlpack(scores.toDlpack()).reshape(-1, 4)

    masks = masks_postprocess_gpu(masks, scores, 0.0)
    result = draw_mask(masks, img[0],oragine_shape=oragine_shape)
    show(result)
    time2 = time.time()
    print(time2-time1)
    # cv2.imwrite("C:/Users/17339/Desktop/0000.jpg", img)

    # time4 = time.time()
    #print(time2 - time1,time3-time2,time4-time3)
    # if i != 0:
    #     s += (time2-time1)
    #     s1 += (time3-time2)
    #     s2 += (time4 - time3)
        # s3 += (time5-time4)
        # s4 += (time6-time5)
        # s5 += (time7-time6)
# print(f"yolo+encoder:",s/300)
# print(f"postprocess:",s1/300)
# print(f"decoder:",s2/300)
# print(1/((s+s1+s2)/300))
# print(f"decoder:",s3/299)
# print(f"postprocess:",s4/299)
# print(f"draw_masks:",s5/299)