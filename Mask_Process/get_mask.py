import json
import pandas as pd
import numpy as np
import os
from PIL import Image, ImageDraw

coor = [(0, 627), (777, 474), (1230, 459), (2047, 601), (2047, 1023), (0, 1023)]

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

for num in range(0,174):
    n = str(num)
    n = n.zfill(3)
    filepath = '/home/ubuntu/datasets/cityscapes/gtFine_trainvaltest/gtFine/train/aachen/aachen_000'\
               + n +'_000019_gtFine_polygons.json'
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
            background = Image.new('RGB', (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(background)
            draw.polygon(points, fill=(0, 0, 0))
            img_name = label + ".jpg"
            save_path = outdirpath + '/' + img_name
            label_info = {'label': label, 'size': size, 'priority': '0'}
            object_info.append(label_info)
            if not os.path.exists(save_path):
                background.save(save_path)
        mask_info.update({'objects': object_info})
        # mask_info = json.dumps(mask_info)
        with open(outjsonpath, 'w') as out:
            json.dump(mask_info, out, sort_keys=True, indent=4, separators=(',', ':'))







