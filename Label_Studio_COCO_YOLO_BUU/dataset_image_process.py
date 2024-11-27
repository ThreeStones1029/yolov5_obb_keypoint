'''
Descripttion: "用于BUU数据集图像处理.
version: 1.0
Author: ShuaiLei
Date: 2024-11-18 14:21:48
LastEditors: ShuaiLei
LastEditTime: 2024-11-18 11:58:38
'''
from json_process import load_json_file
import shutil
import os


def according_coco_json_copy_images(coco_json_file_path, images_folder, save_images_folder):
    """
    根据coco json文件取出images
    coco_json_file_path: coco json文件位置
    images_folder: 保存的图像文件位置
    """
    dataset = load_json_file(coco_json_file_path)
    for image in dataset["images"]:
        if image["type"] == "AP":
            shutil.copy(os.path.join(images_folder, "AP",image["file_name"]), os.path.join(save_images_folder, image["file_name"]))
        if image["type"] == "LA":
            shutil.copy(os.path.join(images_folder, "LA",image["file_name"]), os.path.join(save_images_folder, image["file_name"]))
    print("copy complete!")


if __name__ == "__main__":
    according_coco_json_copy_images("dataset/BUU/buu_rotate.json", "/data/share/ShuaiLei/BUU_LSPINEv1", "dataset/BUU/images")