import json
import pandas as pd
import numpy as np
import os
from PIL import Image, ImageDraw

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        print(path + ' 目录已存在')
        return False

def polygon_area(coordiates):
    area = 0
    q = coordiates[-1]
    for p in coordiates:
        area += p[0] * q[1] - p[1] * q[0]
        q = p
    area = abs(area/2)
    max = 1024 * 2048
    percentage = format(area/max, '.5f')
    return percentage

def get_priority(label):
    return 0


def masks():
    mask_set = set()
    label_queue_info = []
    for num in range(0, 174):
        n = str(num)
        n = n.zfill(3)
        filepath = '/home/ubuntu/datasets/cityscapes/gtFine_trainvaltest/gtFine/train/aachen/aachen_000' \
                   + n + '_000019_gtFine_polygons.json'
        filedir = 'acchen_000' + n
        outdirpath = '/home/ubuntu/code/Mask_Process/mask_out/aachen/' + filedir
        outjsonpath = outdirpath + '/' + filedir + '.json'
        # mkdir(outdirpath)
        with open(filepath, 'r') as input:
            input = json.load(input)
            height = input['imgHeight']
            width = input['imgWidth']
            input = input['objects']
            mask_info = {'folder': filedir}
            object_info = []
            for i in input:
                label = i.get('label')
                points = []
                for j in i.get('polygon'):
                    t = tuple(j)
                    points.append(t)
                size = polygon_area(points)
                background = Image.new('RGB', (width, height), (0, 0, 0))
                draw = ImageDraw.Draw(background)
                draw.polygon(points, fill=(255, 255, 255))
                img_name = label + ".jpg"
                save_path = outdirpath + '/' + img_name

                label_pri = {'label': label, 'priority': '0'}
                if label not in mask_set:
                    mask_set.add(label)
                    label_queue_info.append(label_pri)

                label_info = {'label': label, 'size': size, 'priority': '0'}

                object_info.append(label_info)
                # if not os.path.exists(save_path):
                background.save(save_path)
            # 保存每个图像中的label信息，保存在json格式中
            mask_info.update({'objects': object_info})
            with open(outjsonpath, 'w') as out:
                json.dump(mask_info, out, sort_keys=True, indent=4, separators=(',', ':'))

    label_queue_path = '/home/ubuntu/code/Mask_Process/save/label_queue.json'
    temp = {}
    temp.update({'objects': label_queue_info})

    # with open(label_queue_path, 'w') as w:
    #     json.dump(temp, w, sort_keys=True, indent=4, separators=(',', ':'))

if __name__ == '__main__':
    masks()





