from mindvision.dataset import Mnist
from Network import YOLO
from mindspore import load_checkpoint, load_param_into_net
from mindspore.train import Model
import numpy as np
from mindspore import Tensor
import matplotlib.pyplot as plt


download_eval = Mnist(path="./mnist", split="test", batch_size=32, resize=32, download=True)
dataset_eval = download_eval.run()

# 搭建YOLO分类模型
network = YOLO(10,1)
# 加载已经保存的用于测试的模型
param_dict = load_checkpoint("MyNet.ckpt")
# 加载参数到网络中
load_param_into_net(network, param_dict)

mnist = Mnist("./mnist", split="train", batch_size=6, resize=32)
dataset_infer = mnist.run()
ds_test = dataset_infer.create_dict_iterator()
data = next(ds_test)
images = data["image"].asnumpy()
labels = data["label"].asnumpy()

plt.figure()
for i in range(1, 7):
    plt.subplot(2, 3, i)
    plt.imshow(images[i-1][0], interpolation="None", cmap="gray")
plt.show()

model = Model(network)
# 使用函数model.predict预测image对应分类
output = model.predict(Tensor(data['image']))
predicted = np.argmax(output.asnumpy(), axis=1)

# 输出预测分类与实际分类
print(f'Predicted: "{predicted}", Actual: "{labels}"')