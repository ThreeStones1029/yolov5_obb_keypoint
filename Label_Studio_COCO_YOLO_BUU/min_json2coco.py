'''
Descripttion: "this py file will be used to converse the label studio min json file to coco format.
version: 1.0
Author: ShuaiLei
Date: 2023-10-24 14:21:48
LastEditors: ShuaiLei
LastEditTime: 2024-07-12 11:58:38


BUU datasets annotations format:
    AP、LA
        bbox:
            C1——L5、pelvis total 24 bboxes

CoCo annotations format:
    AP、LA
        bbox:
            C1——L5、pelvis total 24 bboxes
'''
import json
import os 
from datetime import datetime
from collections import defaultdict
import numpy as np
import math
from bbox_utils import is_point_in_polygon_area


class Min_json2coco:
    def __init__(self, annotation_file=None, 
                 choose_ids="all", 
                 choose_category_name_list = "all",
                 is_horizontal_bbox_conver = False,
                 is_rotation_bbox_conver = True, 
                 is_add_keypoints = False,
                 is_del_hard=True,
                 save_path=None):
        """
        param self.is_del_hard:是否删除难标注的
        param self.choose_ids 选择需要的图片id
        param self.choose_category_name_list 选择需要的类别
        param self.is_horizontal_bbox_conver 是否进行水平框的标注转换
        param self.is_rotation_bbox_conver 是否需要旋转框标注转换
        param self.is_add_keypoints 是否加入关键点标注
        param self.is_del_hard 是否删除苦难标注
        param self.save_path 保存路径
        """
        self.annotations_file = annotation_file
        self.save_path = save_path
        self.choose_ids = choose_ids
        self.choose_category_name_list = choose_category_name_list
        self.is_horizontal_bbox_conver = is_horizontal_bbox_conver
        self.is_rotation_bbox_conver = is_rotation_bbox_conver
        self.is_add_keypoints = is_add_keypoints
        self.is_del_hard = is_del_hard
        self.ann_id = 1
        if annotation_file != None:
            print('loading annotations into memory...')
            with open(self.annotations_file, "r") as f:
                self.label_studio_annotations = json.load(f)
            self.coco_annotations = {}
            self.dataset,self.anns,self.cats,self.imgs, self.info = dict(),dict(),dict(),dict(), dict()
            self.imgToAnns, self.catToImgs = defaultdict(list), defaultdict(list)
            self.conver_coco()
            print("conver label studio min bbox json file to coco format complete!")
        else:
            print("the file path is none")


    def conver_coco(self):
        self.add_info()
        self.add_images()
        self.add_categories()
        self.add_annotations()
        self.save_dataset()

    def add_info(self):
        self.info = {"description": "This dataset is labeled as visible to the human eye and labeled: L5-C1, Pelvis, rib",
                     "contribute": "Shuai lei",
                     "version": "1.0",
                     "date": datetime.today().strftime('%Y-%m-%d')}
        self.dataset['info'] = self.info


    def add_categories(self):
        categories = []
        cats = {}
        if self.choose_category_name_list != "all":
            category_id = 1
            for category_name in self.choose_category_name_list:
                if category_name == "Pelvis" or category_name == "pelvis" or category_name == "rib" or category_name == "Rib":
                    categories.append({"id": category_id,
                                        "name": category_name, 
                                        "supercategory": "bone"})
                else:
                    categories.append({"id": category_id,
                                        "name": category_name, 
                                        "supercategory": "vertebrae"})
                category_id += 1
        else:
            categories.append({"id": 1,
                                "name": "Pelvis",
                                "supercategory": "bone"}) 
            for i in range(2, 7):
                categories.append({"id": i,
                                "name": "L" + str(7-i),
                                "supercategory": "vertebrae"}) 
            for i in range(7, 19):
                categories.append({"id": i,
                                "name": "T" + str(19-i),
                                "supercategory": "vertebrae"}) 
            for i in range(19, 26):
                categories.append({"id": i,
                                "name": "C" + str(26-i),
                                "supercategory": "vertebrae"})  
            categories.append({"id": 26,
                            "name": "rib", 
                            "supercategory": "bone"})
        # categories.append({"id": 1,
        #                    "name": "normal", 
        #                    "supercategory": "vertebrae"})
        # categories.append({"id": 2,
        #                    "name": "fracture", 
        #                    "supercategory": "vertebrae"})
        self.dataset['categories'] = categories

        for cat in self.dataset['categories']:
            cats[cat['id']] = cat
        self.cats = cats


    def add_images(self):
        images = []
        imgs = {}
        for img_info in self.label_studio_annotations:
            # BUU point: vertebrae center
            # if (img_info['type'] == "LA" and img_info["updated_at"][0:4] == "2025" and img_info["updated_at"][5:7] == "01" and int(img_info["updated_at"][8:10]) > 20) or (img_info['type'] == "AP"):
            if img_info["created_at"][0:4] == "2025" and img_info["created_at"][5:7] == "02" and img_info["updated_at"][0:4] == "2025" and img_info["updated_at"][5:7] == "02":
                if  (self.choose_ids=="all" or img_info['id'] in self.choose_ids) and img_info['annotator'] != 3: # 排除原始BUU数据自带的标注,同时挑选需要的图片
                    # 是否需要删除标注困难的
                    if self.is_del_hard:
                        if "sentiment" not in img_info.keys() or ("sentiment" in img_info.keys() and img_info["sentiment"] == "False"): # 排除标注困难的
                            img = {}
                            img['id'] = img_info['id']
                            if 'type' in img_info:
                                img['type'] = img_info['type']
                            if 'L4L6' in img_info:
                                img['L4L6'] = img_info['L4L6']
                            if 'source' in img_info:
                                img['source'] = img_info['source']
                            img['file_name'] = os.path.basename(img_info['img'])
                            img['width'] = img_info["bbox"][0]['original_width']
                            img['height'] = img_info["bbox"][0]['original_height']
                            images.append(img)
                    else:
                        img = {}
                        img['id'] = img_info['id']
                        if 'type' in img_info:
                            img['type'] = img_info['type']
                        if 'L4L6' in img_info:
                            img['L4L6'] = img_info['L4L6']
                        if 'source' in img_info:
                            img['source'] = img_info['source']
                        img['file_name'] = os.path.basename(img_info['img'])
                        img['width'] = img_info["bbox"][0]['original_width']
                        img['height'] = img_info["bbox"][0]['original_height']
                        images.append(img)
        self.dataset['images'] = images
        for img in self.dataset['images']:
            imgs[img['id']] = img
        self.imgs = imgs


    def add_annotations(self):
        self.dataset['annotations'] = []
        anns = {}
        # 对于所有图片
        for img_info in self.label_studio_annotations:
            # BUU point: vertebrae center
            # if (img_info['type'] == "LA" and img_info["updated_at"][0:4] == "2025" and img_info["updated_at"][5:7] == "01" and int(img_info["updated_at"][8:10]) > 20) or (img_info['type'] == "AP"):
            if img_info["created_at"][0:4] == "2025" and img_info["created_at"][5:7] == "02" and img_info["updated_at"][0:4] == "2025" and img_info["updated_at"][5:7] == "02":
                if  (self.choose_ids=="all" or img_info['id'] in self.choose_ids) and img_info['annotator'] != 3: # 排除原始BUU数据自带的标注,同时挑选需要的图片
                    if self.is_del_hard:
                        if "sentiment" not in img_info.keys() or ("sentiment" in img_info.keys() and img_info["sentiment"] == "False"): # 排除标注困难的
                            self.single_add_annotations(img_info)
                    else:
                        self.single_add_annotations(img_info)
        
        imgToAnns, catToImgs = defaultdict(list), defaultdict(list)
        for ann in self.dataset['annotations']:
            imgToAnns[ann['image_id']].append(ann)
            catToImgs[ann['category_id']].append(ann['image_id'])
            anns[ann['id']] = ann
        self.imgToAnns = imgToAnns
        self.anns = anns


    def single_add_annotations(self, img_info):
        cat_name2keypoints = defaultdict(list)
        # 将同一个类别的点加入到同一个列表
        if 'vertebrae-point' in img_info.keys():
            for point in img_info['vertebrae-point']:
                if point['keypointlabels'][0] != "Pelvis": # 侧位骨盆有标注框，就不需要点了
                    cat_name2keypoints[point['keypointlabels'][0]].append(point)
        cat_name2id = {category['name']: category['id'] for category in self.dataset['categories']}

        # 将单张图片 先加入标志点围成的框
        for cat_name, points in cat_name2keypoints.items():
            ann = {}
            ann['id'] = self.ann_id
            ann['image_id'] = img_info['id']
            ann['iscrowd'] = 0
            ann['category_id'] = cat_name2id[cat_name]
            ann['category_name'] = cat_name
            x = []
            y = []
            for point in points:
                x.append(point['x'] * point['original_width'] / 100)
                y.append(point['y'] * point['original_height'] / 100)
            min_x = min(x)
            min_y = min(y)
            max_x = max(x)
            max_y = max(y)
            bbox_width = max_x - min_x
            bbox_height = max_y - min_y
            bbox = [min_x, min_y, bbox_width, bbox_height]
            ann['bbox'] = bbox
            ann['area'] = bbox_height * bbox_width
            self.ann_id += 1
            self.dataset['annotations'].append(ann)


        # 加入标注的框和关键点信息
        for bbox in img_info['bbox']:
            ann = {}
            ann['id'] = self.ann_id
            ann['image_id'] = img_info['id']
            ann['iscrowd'] = 0
            cat_name = bbox["rectanglelabels"][0]
            if self.choose_category_name_list != "all" and cat_name not in self.choose_category_name_list:
                continue
            ann['category_id'] = cat_name2id[cat_name]
            ann['category_name'] = cat_name

            x1 = bbox['x'] * bbox['original_width'] / 100
            y1 = bbox['y'] * bbox['original_height'] /100
            w = bbox['width'] * bbox['original_width'] / 100
            h = bbox['height'] * bbox['original_height'] / 100

            # 加入水平检测框
            if self.is_horizontal_bbox_conver and bbox["rotation"] == 0:
                ann['bbox'] = [x1, y1, w, h]
                bbox_points = [[x1, y1], [x1 + w, y1], [x1 + w, y1 + h], [x1, y1 + h]]
                # 加入关键点
                if self.is_add_keypoints:
                    keypoints = self.get_keypoints(img_info["keypoints"], bbox_points)
                    if keypoints == []:
                        k_x = (4*x1 + 2*w) / 4
                        k_y = (4*y1 + 2*h) / 4
                        keypoints = [[k_x, k_y]]
                    ann["points"] = keypoints

            # 加入旋转检测框
            if self.is_rotation_bbox_conver:
                if bbox["rotation"] >= 0 and bbox["rotation"] <= 90:
                    radian_angle = math.radians(360 - bbox["rotation"])
                    x2 = x1 + w * abs(math.cos(radian_angle))
                    y2 = y1 + w * abs(math.sin(radian_angle))
                    x3 = x2 - h * abs(math.sin(radian_angle))
                    y3 = y2 + h * abs(math.cos(radian_angle))
                    x4 = x1 - h * abs(math.sin(radian_angle))
                    y4 = y1 + h * abs(math.cos(radian_angle))
                if bbox["rotation"] >= 270 and bbox["rotation"] <= 360:
                    radian_angle = math.radians(bbox["rotation"])
                    x2 = x1 + w * abs(math.cos(radian_angle))
                    y2 = y1 - w * abs(math.sin(radian_angle))
                    x3 = x2 + h * abs(math.sin(radian_angle))
                    y3 = y2 + h * abs(math.cos(radian_angle))
                    x4 = x1 + h * abs(math.sin(radian_angle))
                    y4 = y1 + h * abs(math.cos(radian_angle))
                ann['rotation_bbox'] = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]

                # 加入关键点
                if self.is_add_keypoints:
                    keypoints = self.get_keypoints(img_info["keypoints"], ann['rotation_bbox'])
                    if keypoints == []:
                        k_x = (x1 + x2 + x3 + x4) / 4
                        k_y = (y1 + y2 + y3 + y4) / 4
                        keypoints = [[k_x, k_y]]
                    ann["points"] = keypoints

            ann["width"] = w
            ann["height"] = h
            ann['area'] = w * h
            self.ann_id += 1
            self.dataset['annotations'].append(ann)


    def get_keypoints(self, keypoints_info, bbox_points):
        ""
        # 加入标注关键点信息
        keypoints = []
        for keypoint_info in keypoints_info:
            point_x = keypoint_info['x'] * keypoint_info['original_width'] / 100
            point_y = keypoint_info['y'] * keypoint_info['original_height'] / 100

            if is_point_in_polygon_area((point_x, point_y), bbox_points):
                keypoints.append([point_x, point_y])
        return keypoints


    def save_dataset(self):
        with open(self.save_path, "w") as w:
            json.dump(self.dataset, w)


if __name__ == "__main__":
    # choose_ids = [18086, 18094, 18101, 18116,  18122, 18126, 18153, 18188, 18207,  18322, 18329, 18344, 18365, 18376,  18420, 18452, 18470, 18488, 11409,
    #               18215,18232, 18242, 18251, 18299, 18290, 18400, 18409, 18459, 11463, 11411]

    # print(len(choose_ids))

    ["L5", "L4", "L3", "L2", "L1",
    "T12", "T11", "T10", "T9", "T8", "T7", "T6", "T5", "T4", "T3", "T2", "T1",
    "C7", "C6", "C5", "C4", "C3", "C2", "C1"]

    conversion = Min_json2coco(annotation_file="dataset/xray20241203/xray20241203_min_json2.json", 
                               choose_ids='all',
                               choose_category_name_list="all",
                               is_horizontal_bbox_conver=False,
                               is_rotation_bbox_conver=True,
                               is_add_keypoints=True,
                               is_del_hard=False,
                               save_path="dataset/xray20241203/xray20241203_rotate_keypoints_all2.json")

    print(len(conversion.imgs))