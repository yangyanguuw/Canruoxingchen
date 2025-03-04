from mindvision.dataset import Mnist
import mindspore as ms
from mindspore import load_checkpoint, load_param_into_net
from mindspore.train.callback import ModelCheckpoint, CheckpointConfig,LossMonitor
import mindspore.nn as nn
from mindspore.train import Model
from Network import YOLO

# 下载并处理MNIST数据集
download_train = Mnist(path="./mnist", split="train", batch_size=32, repeat_num=1, shuffle=True, resize=32, download=True)

download_eval = Mnist(path="./mnist", split="test", batch_size=32, resize=32, download=True)

dataset_train = download_train.run()
dataset_eval = download_eval.run()

# 搭建YOLO分类模型
network = YOLO(10,1)

# 定义损失函数
net_loss = nn.SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')

# 定义优化器函数
net_opt = nn.Momentum(network.trainable_params(), learning_rate=0.01, momentum=0.9)

# 初始化模型参数
model = Model(network, loss_fn=net_loss, optimizer=net_opt, metrics={'accuracy'})

# 训练网络模型，并保存为YOLO-1_1875.ckpt文件
model.train(10, dataset_train,callbacks=[LossMonitor(50)])

# 定义的网络模型为net，一般在训练前或者训练后使用
ms.save_checkpoint(network, "./MyNet.ckpt")


