import mindspore.nn as nn
import mindspore.ops as ops
from Blocks import Conv,C2f,Classify

class YOLO(nn.Cell):

    def __init__(self, num_class=10, num_channel=3):
        super(YOLO, self).__init__()
        #Backbone:
        #Conv(c1, c2, k=1, s=1, p=None, g=1, d=1, act=True)
        #C2f(c1, c2, n=1, shortcut=False, g=1, e=0.5)
        #Classfiy(c1, c2, k=1, s=1, p=None, g=1)

        self.conv=Conv(num_channel,16,3,2)
        self.conv1=Conv(16,32,3,2)
        self.c2f1=C2f(32,32,1,True)
        self.conv2=Conv(32,64,1,1)
        self.c2f2=C2f(64,64,2,True)
        self.conv3 = Conv(64,128,1,1)
        self.c2f3 = C2f(128,128,2,True)
        self.conv4 = Conv(128,256,1,1)
        self.c2f4= C2f(256,256,1,True)
        #Head:
        self.classfiy=Classify(256,num_class)

    def construct(self, x):
        x = self.conv(x)
        x = self.conv1(x)
        x = self.c2f1(x)
        x = self.conv2(x)
        x = self.c2f2(x)
        x = self.conv3(x)
        x = self.c2f3(x)
        x = self.conv4(x)
        x = self.c2f4(x)
        x = self.classfiy(x)
        return x