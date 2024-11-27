'''
Description: 
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-04-13 15:17:15
LastEditors: ShuaiLei
LastEditTime: 2024-04-13 15:18:06
'''
import os
import pandas as pd

def create_folder(path):
    os.makedirs(path, exist_ok=True)
    return path

def join(*args):
    return os.path.join(*args)

def export_xlsx_file(data, xlsx_save_path):
    df = pd.DataFrame(data)
    df.to_excel(xlsx_save_path, index=False)


if __name__ == "__main__":
    pass
