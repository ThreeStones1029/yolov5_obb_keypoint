'''
Descripttion: 
version: 
Author: ShuaiLei
Date: 2023-11-03 09:28:54
LastEditors: ShuaiLei
LastEditTime: 2024-01-18 21:20:15
'''
import json
from pycocotools.coco import COCO
from collections import defaultdict
import time
from PIL import Image
import os


class Pre_coco:
    def __init__(self, annotation_file=None, dt=None):
        """
        Constructor of Microsoft COCO helper class for reading and visualizing annotations.
        :param annotation_file (str): location of annotation file
        :param image_folder (str): location to the folder that hosts images.
        :return:
        """
        # load dataset
        self.dataset,self.anns = dict(),dict()
        self.imgToAnns = defaultdict(list)
        tic = time.time()
        # 通过路径下载
        if type(annotation_file) == str:
            print("loading annotations into memory from annotation_file...")
            with open(annotation_file, 'r') as f:
                dataset = json.load(f)
            assert type(dataset)==list, "annotation file format {} not supported".format(type(dataset))
            self.dataset = {"annotations": dataset}

        # 直接加载
        if dt:
            print("loading annotations into memory from dt...")
            assert type(dt)==list, "dt format {} not supported".format(type(dt))
            self.dataset = {"annotations": dt}

        # 都不存在
        if not dt and not annotation_file:
            print("annotation_file must be path or dt must be list")

        self.createIndex()
        print("Done (t={:0.2f}s)".format(time.time()- tic))


    def createIndex(self):
        # create index
        print("creating index...")
        anns, img_idToFilename = {}, {}
        imgToAnns = defaultdict(list)
        if "annotations" in self.dataset:
            id = 0
            for ann in self.dataset["annotations"]:
                id += 1
                imgToAnns[ann["image_id"]].append(ann)
                ann["id"] = id
                anns[id] = ann
                img_idToFilename[ann["image_id"]] = ann["file_name"]

        print("index created!")

        # create class members
        self.anns = anns
        self.imgToAnns = imgToAnns
        self.img_idToFilename = img_idToFilename


    def info(self):
        """
        Print information about the annotation file.
        :return:
        """
        if "info" in self.dataset:
            for key, value in self.dataset["info"].items():
                print('{}: {}'.format(key, value))
        else:
            print("dataset don't have info, please check your json file")



class Pre_coco2Label_studio(Pre_coco):
    def __init__(self, annotation_file=None, infer_image_folder=None):
        super(Pre_coco2Label_studio, self).__init__(annotation_file)
        self.label_studio_dataset = []
        self.infer_image_folder = infer_image_folder


    def conver_and_save(self, save_path):
        self.conver_format()
        self.save_conver_result(save_path)

    
    def conver_format(self):
        for img_id, anns in self.imgToAnns.items():
            img_info = {}
            img = Image.open(os.path.join(self.infer_image_folder, self.img_idToFilename[img_id]))
            img_info["data"] = {"image": os.path.join(self.infer_image_folder, self.img_idToFilename[img_id])}
            img_info["predictions"] = []
            model_pre = {}
            model_pre["model_version"]="logic"
            model_pre["score"] = 0.6
            model_pre["result"] = []
            
            for ann in anns:
                ann_info = {
                            "id": ann["id"],
                            "type": "rectanglelabels",        
                            "from_name": "label", "to_name": "image",
                            "original_width": img.size[0], "original_height": img.size[1],
                            "image_rotation": 0,
                            "value": {
                                    "rotation": 0,          
                                    "x": ann["bbox"][0] / img.size[0] * 100, 
                                    "y": ann["bbox"][1] / img.size[1] * 100,
                                    "width": ann["bbox"][2] / img.size[0] * 100, 
                                    "height": ann["bbox"][3] / img.size[1] * 100,
                                    "rectanglelabels": [ann["category_name"]]
                                    }
                            }
                model_pre["result"].append(ann_info)
            img_info["predictions"].append(model_pre)
            self.label_studio_dataset.append(img_info)


        # 检查是否有图片没有预测到，但是需要加入进去
        for root, dirs, files in os.walk(self.infer_image_folder):
            for file in files:
                if file not in self.img_idToFilename.values():
                    img_info = {}
                    img_info["data"] = {"image": os.path.join(self.infer_image_folder, file)}
                    img_info["predictions"] = [
                                                {
                                                 "model_version":"logic",
                                                 "score":0.6,
                                                 "result":[]  
                                                }
                                              ]
                    self.label_studio_dataset.append(img_info)



    def save_conver_result(self, save_path):
        with open(save_path, "w") as f:
            json.dump(self.label_studio_dataset, f)


if __name__ == "__main__":
    label_studio = Pre_coco2Label_studio("/home/jjf/Desktop/SymbolicSystem/infer_output/XJT/logic/rtdetr/logic_bbox.json",
                                         "/home/jjf/Desktop/RT-DETR/rtdetr_paddle/datasets/XJT20231101/all_conver")
    label_studio.conver_and_save("/home/jjf/Desktop/SymbolicSystem/infer_output/XJT/logic/rtdetr/label_studio_logic_bbox.json")