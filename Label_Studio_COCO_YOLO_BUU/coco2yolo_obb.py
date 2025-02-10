'''
Description: 本文件用于将coco格式数据集转为yolo_obb格式
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2025-01-18 10:33:59
LastEditors: ShuaiLei
LastEditTime: 2025-01-18 12:34:00
'''
import os
import json
from pycocotools.coco import COCO


def coco_json2yolo_obb_txt(coco_json_path, txt_save_folder, yolo_obb_catid2catname, is_add_keypoints=False):
    os.makedirs(txt_save_folder, exist_ok=True)
    coco_json = COCO(coco_json_path)
    coco_catid2catname = {}
    for category in coco_json.dataset["categories"]:
        coco_catid2catname[category["id"]] = category["name"]

    yolo_obb_catname2catid = {v:k for k, v in yolo_obb_catid2catname.items()}
    for image in coco_json.dataset["images"]:
        filename = image["file_name"]
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".bmp") or filename.endswith(".jpeg"):
            filename_no_ext = filename.split(".")[0]
        width = image["width"]
        height = image["height"]
        image_id = image["id"]
        anns = coco_json.imgToAnns[image_id]
        yolo_obb_annotations = []
        for ann in anns:
            category_id = ann["category_id"]
            category_name = coco_catid2catname[category_id]
            rotation_bbox = ann["rotation_bbox"]
            x1, y1 = rotation_bbox[0][0] / width, rotation_bbox[0][1] / height
            x2, y2 = rotation_bbox[1][0] / width, rotation_bbox[1][1] / height
            x3, y3 = rotation_bbox[2][0] / width, rotation_bbox[2][1] / height
            x4, y4 = rotation_bbox[3][0] / width, rotation_bbox[3][1] / height
            new_category_id  = yolo_obb_catname2catid[category_name]
            if is_add_keypoints:
                keypoint_x, keypoint_y = ann["points"][0][0] / width, ann["points"][0][1] / height
                yolo_obb_annotations.append(f"{new_category_id} {x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4} {keypoint_x} {keypoint_y}")
            else:
                yolo_obb_annotations.append(f"{new_category_id} {x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4}")
        yolo_obb_file_path = os.path.join(txt_save_folder, filename_no_ext + ".txt")
        with open(yolo_obb_file_path, "w") as f:
            for yolo_obb_annotation in yolo_obb_annotations:
                f.write(yolo_obb_annotation + "\n")


if __name__ == "__main__":
    yolo_obb_catid2catname = {0: "L5", 1: "L4", 2: "L3",  3: "L2", 4: "L1",
                               5: "T12", 6: "T11", 7: "T10", 8: "T9", 9: "T8", 10: "T7", 11: "T6", 12: "T5",13: "T4", 14: "T3", 15: "T2", 16: "T1", 
                               17: "C7", 18: "C6", 19: "C5", 20: "C4", 21: "C3", 22: "C2", 23: "C1"}

    coco_json2yolo_obb_txt("dataset/BUU/val/bbox_val.json",
                            "dataset/BUU/val/",
                            yolo_obb_catid2catname)