'''
Descripttion: "用于数据集格式转换前的检查"
version: TODO
Author: ShuaiLei
Date: 2024-11-18 14:21:48
LastEditors: ShuaiLei
LastEditTime: 2024-11-18 11:58:38
'''
from pathlib import Path
from json_process import load_json_file
from pycocotools.coco import COCO


class COCOFormatCheck(COCO):
    def __init__(self, annotation_file ):
        super().__init__(annotation_file)


def format_check(coco_json_path, is_category_check = True, is_bbox_check = True, is_small_bbox_check = True, is_continue_check = True):
    """
    标签需要连续，标签不能重复
    """
    coco = COCO(coco_json_path)

    # 排除类别重复性
    if is_category_check:
        check_category_repeatability(coco)
        print("There are no duplicate categories in the same picture, and the category repeatability check pass.")


def check_category_repeatability(coco):
    """
    检查标签重复性，同一个类别标签只能出现一次
    """
    for image in coco.dataset["images"]:
        exist_categories_list = []
        for ann in coco.imgToAnns[image["id"]]:
            if ann["category_name"] not in exist_categories_list:
                exist_categories_list.append(ann["category_name"])

        if len(exist_categories_list) != len(coco.imgToAnns[image["id"]]):
            raise ValueError(image["id"], "exist repeatable category!")
            

def check_continuity():
    """
    检查连续性
    """
    pass


def check_small_bbox():
    """
    检查误点的标签
    """
    pass


def check_bbox_repeatability():
    """
    同一个位置只能出现一个框
    """
    pass


if __name__ == "__main__":
    format_check("dataset/BUU/buu_rotate.json", 
                 is_category_check=True,
                 is_bbox_check=True,
                 is_small_bbox_check=True,
                 is_continue_check=True)