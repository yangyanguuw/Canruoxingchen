import os
import xml.etree.ElementTree as ET
import math
import numpy as np
imagesize=[100,1000]
dir = "./path/to/xml"
def edit_xml(xml_file):
    if ".xml" not in xml_file:
        return

    tree = ET.parse(xml_file)
    objs = tree.findall('object')

    txt = xml_file.replace(".xml", ".txt")

    with open(txt, 'w') as wf:

        for ix, obj in enumerate(objs):

            x0text = ""
            y0text = ""
            x1text = ""
            y1text = ""
            x2text = ""
            y2text = ""
            x3text = ""
            y3text = ""

            obj_type = obj.find('type')
            type = obj_type.text

            obj_name = obj.find('name')
            className = obj_name.text

            obj_difficult = obj.find('difficult')
            difficulttext = obj_difficult.text

            if type == 'robndbox':  # 若用rolabelimg标注的是旋转框
                obj_bnd = obj.find('robndbox')
                obj_bnd.tag = 'bndbox'  # 修改节点名
                obj_cx = obj_bnd.find('cx')
                obj_cy = obj_bnd.find('cy')
                obj_w = obj_bnd.find('w')
                obj_h = obj_bnd.find('h')
                obj_angle = obj_bnd.find('angle')
                cx = float(obj_cx.text)
                cy = float(obj_cy.text)
                w = float(obj_w.text)
                h = float(obj_h.text)
                angle = float(obj_angle.text)

                x0text, y0text = rotatePoint(cx, cy, cx - w / 2, cy - h / 2, -angle)
                x1text, y1text = rotatePoint(cx, cy, cx + w / 2, cy - h / 2, -angle)
                x2text, y2text = rotatePoint(cx, cy, cx + w / 2, cy + h / 2, -angle)
                x3text, y3text = rotatePoint(cx, cy, cx - w / 2, cy + h / 2, -angle)

                # points = np.array([[int(float(x0text)), int(float(y0text))], [int(float(x1text)), int(float(y1text))],
                #                    [int(float(x2text)), int(float(y2text))],
                #                    [int(float(x3text)), int(float(y3text))]], np.int32)

            wf.write(
                " {} {} {} {} {} {} {} {} {}\n".format(className,x0text, y0text, x1text, y1text, x2text, y2text, x3text, y3text))


# 转换成四点坐标
def rotatePoint(xc, yc, xp, yp, theta):
    xoff = xp - xc;
    yoff = yp - yc;
    cosTheta = math.cos(theta)
    sinTheta = math.sin(theta)
    pResx = cosTheta * xoff + sinTheta * yoff
    pResy = - sinTheta * xoff + cosTheta * yoff
    return str((xc + pResx)/imagesize[0]), str((yc + pResy)/imagesize[1])


if __name__ == '__main__':
    filelist = os.listdir(dir)
    for file in filelist:
        edit_xml(os.path.join(dir, file))