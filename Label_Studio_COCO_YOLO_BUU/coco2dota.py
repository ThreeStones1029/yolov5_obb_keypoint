'''
Description: 将coco格式的数据转为dota类型
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-11-18 15:17:15
LastEditors: ShuaiLei
LastEditTime: 2024-11-18 15:18:06
'''
import numpy as np
from pycocotools.coco import COCO
from common import create_folder, join
import os


def COCO2DOTA(coco_json_path, dota_txt_save_folder, add_keypoints=False):
    """
    将coco格式数据转为dota格式
    """
    create_folder(dota_txt_save_folder)
    coco = COCO(coco_json_path)
    for image in coco.dataset["images"]:
        filename = image["file_name"]
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".bmp") or filename.endswith(".jpeg"):
            filename_no_ext = os.path.splitext(filename)[0]
        dota_file_path = join(dota_txt_save_folder, filename_no_ext + ".txt")
        dota_annotations = []
        for ann in coco.imgToAnns[image["id"]]:
            rotate_bbox = ann["rotation_bbox"]
            rotate_bbox = np.round(rotate_bbox)
            point1 = rotate_bbox[0]
            point2 = rotate_bbox[1]
            point3 = rotate_bbox[2]
            point4 = rotate_bbox[3]
            keypoints = np.round(ann["points"])
            if add_keypoints:
                dota_annotations.append(f"{point1[0]} {point1[1]} {point2[0]} {point2[1]} {point3[0]} {point3[1]} {point4[0]} {point4[1]} {keypoints[0][0]} {keypoints[0][1]} {ann['category_name']} {0}")
            else:
                dota_annotations.append(f"{point1[0]} {point1[1]} {point2[0]} {point2[1]} {point3[0]} {point3[1]} {point4[0]} {point4[1]} {ann['category_name']} {0}")
        with open(dota_file_path, "w") as f:
            for dota_annotation in dota_annotations:
                f.write(dota_annotation + "\n")
    print("conver succesfully!")


if __name__ == "__main__":
    # COCO2DOTA("dataset/BUU/train/bbox_train2.json",
    #           "dataset/BUU/train/labelTxt_points2",
    #           add_keypoints=True)
    # COCO2DOTA("dataset/BUU/val/bbox_val2.json",
    #           "dataset/BUU/val/labelTxt_points2",
    #           add_keypoints=True)
    

    COCO2DOTA("dataset/xray20241203/train/rotate_bbox_keypoints_train_instance2.json",
              "dataset/xray20241203/train/labelTxt_keypoints_instance2",
              add_keypoints=True)
    COCO2DOTA("dataset/xray20241203/val/rotate_bbox_keypoints_val_instance2.json",
              "dataset/xray20241203/val/labelTxt_keypoints_instance2",
              add_keypoints=True)
    COCO2DOTA("dataset/xray20241203/test/rotate_bbox_keypoints_test_instance2.json",
              "dataset/xray20241203/test/labelTxt_keypoints_instance2",
              add_keypoints=True)
    

    COCO2DOTA("dataset/xray20241203/train/rotate_bbox_keypoints_train_semantic2.json",
              "dataset/xray20241203/train/labelTxt_keypoints_semantic2",
              add_keypoints=True)
    COCO2DOTA("dataset/xray20241203/val/rotate_bbox_keypoints_val_semantic2.json",
              "dataset/xray20241203/val/labelTxt_keypoints_semantic2",
              add_keypoints=True)
    COCO2DOTA("dataset/xray20241203/test/rotate_bbox_keypoints_test_semantic2.json",
              "dataset/xray20241203/test/labelTxt_keypoints_semantic2",
              add_keypoints=True)
    

    # COCO2DOTA("dataset/xray20241203/train/rotate_bbox_keypoints_train_instance.json",
    #           "dataset/xray20241203/train/labelTxt_instance",
    #           add_keypoints=False)
    # COCO2DOTA("dataset/xray20241203/val/rotate_bbox_keypoints_val_instance.json",
    #           "dataset/xray20241203/val/labelTxt_instance",
    #           add_keypoints=False)
    # COCO2DOTA("dataset/xray20241203/test/rotate_bbox_keypoints_test_instance.json",
    #           "dataset/xray20241203/test/labelTxt_instance",
    #           add_keypoints=False)
    

    # COCO2DOTA("dataset/xray20241203/train/rotate_bbox_keypoints_train_semantic.json",
    #           "dataset/xray20241203/train/labelTxt_semantic",
    #           add_keypoints=False)
    # COCO2DOTA("dataset/xray20241203/val/rotate_bbox_keypoints_val_semantic.json",
    #           "dataset/xray20241203/val/labelTxt_semantic",
    #           add_keypoints=False)
    # COCO2DOTA("dataset/xray20241203/test/rotate_bbox_keypoints_test_semantic.json",
    #           "dataset/xray20241203/test/labelTxt_semantic",
    #           add_keypoints=False)

