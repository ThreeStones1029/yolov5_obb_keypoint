'''
Description: 本文件用于将coco格式数据集转为yolo格式
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-03-14 13:33:59
LastEditors: ShuaiLei
LastEditTime: 2024-05-27 12:34:00
'''
import os
import json
from pycocotools.coco import COCO


def coco_json2yolo_txt(coco_json_path, txt_save_folder, yolo_catid2catname):
    os.makedirs(txt_save_folder, exist_ok=True)
    coco_json = COCO(coco_json_path)
    coco_catid2catname = {}
    for category in coco_json.dataset["categories"]:
        coco_catid2catname[category["id"]] = category["name"]

    yolo_catname2catid = {v:k for k, v in yolo_catid2catname.items()}
    for image in coco_json.dataset["images"]:
        filename = image["file_name"]
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".bmp") or filename.endswith(".jpeg"):
            filename_no_ext = filename.split(".")[0]
        width = image["width"]
        height = image["height"]
        image_id = image["id"]
        anns = coco_json.imgToAnns[image_id]
        yolo_annotations = []
        for ann in anns:
            category_id = ann["category_id"]
            category_name = coco_catid2catname[category_id]
            bbox = ann["bbox"]
            x_center = bbox[0] + bbox[2] / 2
            y_center = bbox[1] + bbox[3] / 2
            x_center = x_center / width
            y_center = y_center / height
            w = bbox[2] / width
            h = bbox[3] / height
            new_category_id  = yolo_catname2catid[category_name]
            yolo_annotations.append(f"{new_category_id} {x_center} {y_center} {w} {h}")
        yolo_file_path = os.path.join(txt_save_folder, filename_no_ext + ".txt")
        with open(yolo_file_path, "w") as f:
            for yolo_annotation in yolo_annotations:
                f.write(yolo_annotation + "\n")

if __name__ == "__main__":
    ## verse_drr
    # yolo_catid2catname = { 0: "L6", 1: "L5", 2: "L4", 3: "L3", 4: "L2", 5: "L1", 6: "T12", 7: "T11", 8: "T10", 9: "T9"}

    ## xray_instance
    yolo_catid2catname = {0: "L5", 1: "L4", 2: "L3",  3: "L2", 4: "L1", 5: "T12", 6: "T11", 7: "T10", 8: "T9", 9: "T8", 10: "T7", 11: "T6", 12: "T5",
                           13: "T4", 14: "T3", 15: "T2", 16: "T1", 17: "C7", 18: "C6", 19: "C5", 20: "C4", 21: "C3", 22: "C2", 23: "C1"}

    ## xray_semantic
    # yolo_catid2catname = {0: "vertebrae", 1: "pelvis", 2: "bone_cement",  3: "rib"}

    ## buu
    # yolo_catid2catname = { 0: "Pelvis", 1: "L5", 2: "L4",  3: "L3", 4: "L2", 5: "L1", 6: "T12", 7: "T11", 8: "T10",
    #                        9: "T9", 10: "T8", 11: "T7", 12: "T6", 13: "T5", 14: "T4", 15: "T3", 16: "T2"}

    ## xray20240119_instance
    # yolo_catid2catname = {0: "L5", 1: "L4", 2: "L3",  3: "L2", 4: "L1", 5: "T12", 6: "T11", 7: "T10", 8: "T9", 9: "T8", 10: "T7", 11: "T6", 12: "T5",
    #                       13: "T4", 14: "T3", 15: "T2", 16: "T1", 17: "C7", 18: "C6", 19: "C5", 20: "C4", 21: "C3", 22: "C2", 23: "C1"}

    ## xray20240119_semantic
    # yolo_catid2catname = {0: "vertebrae", 1: "pelvis", 2: "bone_cement",  3: "rib"}

    coco_json2yolo_txt("dataset/BUU/test/bbox_test.json",
                       "dataset/BUU/test/YOLOTxt",
                       yolo_catid2catname)