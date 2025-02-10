'''
Description: 根据coco文件导出yaml的names以及类别数量
version: 1.0
Author: ShuaiLei
Date: 2023-11-10 19:14:07
LastEditors: ShuaiLei
LastEditTime: 2024-03-12 10:23:33
'''
from json_process import load_json_file


def according_coco_json_export_yaml_parameter(coco_json_path):
    """
    """
    dataset = load_json_file(coco_json_path)
    exist_categories_list = []
    for ann in dataset["annotations"]:
        if ann["category_name"] not in exist_categories_list:
            exist_categories_list.append(ann["category_name"])
    print(exist_categories_list)
    print(len(exist_categories_list))


if __name__ == "__main__":
    according_coco_json_export_yaml_parameter("dataset/BUU/buu_rotate_keypoints2.json")
