'''
Descripttion: "本文件用于查看cache文件内容"
version: TODO
Author: ShuaiLei
Date: 2024-11-24 14:21:48
LastEditors: ShuaiLei
LastEditTime: 2024-11-24 11:58:38
'''
import numpy as np


if __name__ == "__main__":
    # 加载文件
    data = np.load('dataset/BUU/test/labelTxt_points.cache', allow_pickle=True)

    # 查看数据内容
    print(data)
    print(type(data))  # 确认数据类型
    print(data.shape)  # 查看数组维度
