import os
import math
import codecs
import numpy as np
from lxml import etree
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

txt_path = 'path/to/txt/'
xml_path ='./path/to/save/xml/'
image_path="path/to/image/"
long_side=3840  #请将此部分换成图片最长边的长度

def get_angle(x1,y1,x2,y2,x3,y3,x4,y4):
    if x2-x1 != 0 and x4-x3 != 0:
        theta = (math.atan((y2-y1)/(x2-x1)) + math.atan((y4-y3)/(x4-x3)))/2
    else:
        theta = np.pi/2

    if theta >= 0:
        angle = theta
    else:
        angle = theta + np.pi
    return angle,theta


def get_w_and_h(x1,y1,x2,y2,x3,y3,x4,y4):
    w = math.sqrt((x2-x1)**2+(y2-y1)**2)
    h = math.sqrt((x1-x3)**2+(y1-y3)**2)
    return w,h


def get_x_and_y(x1,y1,x2,y2,x3,y3,x4,y4,theta,w,h):
    cx = (x2+x3)/2
    cy = (y2+y3)/2
    x = cx - w/2
    y = cy - h/2
    return x,y,cx,cy


class CreateXml():
    def __init__(self,foldername,filename,imgSize,databaseSrc='Unknown',localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.roboxlist = []
        self.roboxobject = None
        self.localImgPath = localImgPath
        self.verified = False

    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf8')
        root = etree.fromstring(rough_string)
        try:
            return etree.tostring(root, pretty_print=True)
        except TypeError:
            return etree.tostring(root)
    
    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None:
            return None

        top = Element('annotation')
        top.set('verified', 'yes' if self.verified else 'no')

        folder = SubElement(top, 'folder')
        folder.text = self.foldername

        filename = SubElement(top, 'filename')
        filename.text = self.filename

        localImgPath = SubElement(top, 'path')
        localImgPath.text = self.localImgPath

        source = SubElement(top, 'source')
        database = SubElement(source, 'database')
        database.text = self.databaseSrc

        size_part = SubElement(top, 'size')
        width = SubElement(size_part, 'width')
        height = SubElement(size_part, 'height')
        depth = SubElement(size_part, 'depth')
        width.text = str(self.imgSize[1])
        height.text = str(self.imgSize[0])
        if len(self.imgSize) == 3:
            depth.text = str(self.imgSize[2])
        else:
            depth.text = '1'

        segmented = SubElement(top, 'segmented')
        segmented.text = '0'
        return top

    def addRotatedBndBox(self, cx, cy, w, h, angle, name, difficult):
        robndbox = {'cx': cx, 'cy': cy, 'w': w, 'h': h, 'angle': angle}
        robndbox['name'] = name
        robndbox['difficult'] = difficult
        self.roboxlist.append(robndbox)
        self.roboxobject = robndbox

    def appendObjects(self, top):
        # for each_object in self.roboxlist:
        each_object = self.roboxobject
        object_item = SubElement(top, 'object')
        typeItem = SubElement(object_item, 'type')
        typeItem.text = "robndbox"
        name = SubElement(object_item, 'name')
        try:
            name.text = unicode(each_object['name'])
        except NameError:
            # Py3: NameError: name 'unicode' is not defined
            name.text = each_object['name']
        pose = SubElement(object_item, 'pose')
        pose.text = "Unspecified"
        truncated = SubElement(object_item, 'truncated')
        truncated.text = "0"
        difficult = SubElement(object_item, 'difficult')
        difficult.text = str( bool(each_object['difficult']) & 1 )
        robndbox = SubElement(object_item, 'robndbox')
        cx = SubElement(robndbox, 'cx')
        cx.text = str(each_object['cx'])
        cy = SubElement(robndbox, 'cy')
        cy.text = str(each_object['cy'])
        w = SubElement(robndbox, 'w')
        w.text = str(each_object['w'])
        h = SubElement(robndbox, 'h')
        h.text = str(each_object['h'])
        angle = SubElement(robndbox, 'angle')
        angle.text = str(each_object['angle'])

    def save(self, root, targetFile=None):
        # root = self.genXML()
        # self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = codecs.open(
                os.path.join(xml_path + self.filename + '.xml'), 'w', encoding='utf-8')
        else:
            out_file = codecs.open(targetFile, 'w', encoding='utf-8')

        prettifyResult = self.prettify(root)
        out_file.write(prettifyResult.decode('utf8'))
        out_file.close()


txt_list = os.listdir(txt_path)

for txt in txt_list:
    first,_ = os.path.splitext(txt)

    create_xml = CreateXml(foldername='pixeliinkimg',
                            filename=first,
                            imgSize=[long_side,long_side],
                            databaseSrc='Unknown',
                            localImgPath=os.path.join(image_path,first+'.jpg'))
    xml_top = create_xml.genXML()

    txt_line = open(os.path.join(txt_path,txt))
    for bbox_line in txt_line.readlines():
        bbox_list = bbox_line.strip().split(' ')
        print(bbox_list[1])
        lux,luy,rux,ruy,rdx,rdy,ldx,ldy=float(bbox_list[1])*long_side,float(bbox_list[2])*long_side,\
                                        float(bbox_list[3])*long_side,float(bbox_list[4])*long_side,\
                                        float(bbox_list[5])*long_side,float(bbox_list[6])*long_side,\
                                        float(bbox_list[7])*long_side,float(bbox_list[8])*long_side
        x1,y1,x2,y2,x3,y3,x4,y4 = lux,luy,rux,ruy,ldx,ldy,rdx,rdy
        angle,theta = get_angle(x1,y1,x2,y2,x3,y3,x4,y4)
        w,h = get_w_and_h(x1,y1,x2,y2,x3,y3,x4,y4)
        x,y,cx,cy = get_x_and_y(x1,y1,x2,y2,x3,y3,x4,y4,theta,w,h)

        create_xml.addRotatedBndBox(cx,cy,w,h,angle,bbox_list[0],0)
        create_xml.appendObjects(xml_top)
    create_xml.save(xml_top)

