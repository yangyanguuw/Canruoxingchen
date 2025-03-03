# #                                         # pt to onnx
# from ultralytics import YOLO
# model = YOLO("weights/yolov8n-cls.pt")
# success = model.export(format="engine")  # export the model to onnx format


                                          # onnx to engine

import tensorrt as trt
import onnx
import onnx.numpy_helper
import numpy as np

def build_engine(onnx_file_path, engine_file_path):
    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
    EXPLICIT_BATCH = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)

    with trt.Builder(TRT_LOGGER) as builder, builder.create_network(EXPLICIT_BATCH) as network, trt.OnnxParser(network, TRT_LOGGER) as parser:

        config = builder.create_builder_config()
        config.max_workspace_size = 1 << 31  # 2GB
        with open(onnx_file_path, 'rb') as model:
            if not parser.parse(model.read()):
                for error in range(parser.num_errors()):
                    print(parser.get_error(error))
                raise ValueError('Failed to parse the ONNX file.')

        # Set dynamic shapes for inputs
        profile = builder.create_optimization_profile()

        # Input 1: (1, 256, 64, 64) - shape is fixed
        input_shape = (1, 256, 64, 64)
        profile.set_shape(network.get_input(0).name, input_shape, input_shape, input_shape)

        # Input 2: (1, num, 2) - num is dynamic
        min_shape = (1, 4, 2)
        opt_shape = (1, 20, 2)  # Example optimal shape
        max_shape = (1, 100, 2) # Example maximum shape
        profile.set_shape(network.get_input(1).name, min_shape, opt_shape, max_shape)

        # Input 3: (1, num) - num is dynamic
        min_shape = (1, 4)
        opt_shape = (1, 20)     # Example optimal shape
        max_shape = (1, 100)    # Example maximum shape
        profile.set_shape(network.get_input(2).name, min_shape, opt_shape, max_shape)

        config.add_optimization_profile(profile)

        engine = builder.build_engine(network, config)
        with open(engine_file_path, 'wb') as f:
            f.write(engine.serialize())
        return engine
#
# def main():
#     onnx_model_path = './weights/EdgeSAM/edge_sam_3x_decoder_batch.onnx'
#     engine_file_path = './weights/EdgeSAM/edge_sam_3x_decoder_batch.engine'
#     build_engine(onnx_model_path, engine_file_path)
#
# if __name__ == '__main__':
#     main()