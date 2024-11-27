'''
Description: 一些数据集的json处理方法
version: 1.0
Author: ShuaiLei
Date: 2023-11-10 19:14:07
LastEditors: ShuaiLei
LastEditTime: 2024-03-12 10:23:33
'''
import os
import json


def load_json_file(json_path):
    with open(json_path, "r") as f:
        dataset = json.load(f)
    return dataset


def save_json_file(data, json_path):
    dirname = os.path.dirname(json_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(json_path, 'w') as f:
        json.dump(data, f)
    print(json_path, "save successfully")