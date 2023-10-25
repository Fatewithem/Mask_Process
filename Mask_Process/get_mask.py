import json
import pandas as pd
import os

with open('/home/ubuntu/datasets/cityscapes/gtFine_trainvaltest/gtFine/train/aachen/aachen_000000_000019_gtFine_polygons.json', 'r') as input:
    input = json.load(input)
    height = input['imgHeight']
    width = input['imgWidth']
    input = input['objects']
    for i in input:
        print(i.get('label'))
        points = []
        for j in i.get('polygon'):
            print(j)

# data = input['objects']
# print(data)
# def get_polygon