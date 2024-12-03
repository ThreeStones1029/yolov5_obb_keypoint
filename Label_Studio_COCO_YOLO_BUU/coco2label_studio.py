'''
Description: 本文件用于将coco格式数据集转为label_studio格式
version: 
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-12-03 16:16:03
LastEditors: ShuaiLei
LastEditTime: 2024-12-03 22:13:24
'''
from pycocotools.coco import COCO
from json_process import save_json_file, load_json_file
import os
from PIL import Image


class COCO2LabelStudio(COCO):
    def __init__(self, annotation_file, dataset_name):
        super(COCO2LabelStudio, self).__init__(annotation_file)
        self.default_source = "hospital"
        self.dataset_name = dataset_name
        self.image_id = 1
        self.annotation_id = 1
        self.import_id = 1
        self.label_studio_dataset = []
        

    def run(self, label_studio_annotation_file):
        for image in self.dataset["images"]:
            single_data = {"id": 1,
                            "data": {"img": "",
                                     "source": self.default_source},
                            "annotations": [
                            {
                                "id": 1,
                                "created_username": " bot@prmlk.com, 3",
                                "created_ago": "1 minutes",
                                "completed_by": {
                                "id": 3,
                                "first_name": "",
                                "last_name": "",
                                "avatar": None,
                                "email": "bot@prmlk.com",
                                "initials": "bo"
                                },
                                "result": [],
                                "was_cancelled": False,
                                "ground_truth": True,
                                "created_at": "2024-12-03T12:38:08.667557Z",
                                "updated_at": "2024-12-13T12:38:08.667577Z",
                                "draft_created_at": None,
                                "lead_time": None,
                                "import_id": 1,
                                "last_action": None,
                                "task": 1,
                                "project": 15,
                                "updated_by": None,
                                "parent_prediction": None,
                                "parent_annotation": None,
                                "last_created_by": None
                            }
                            ],
                            "predictions": []
                            }
            image_width = image["width"]
            image_height = image["height"]
            single_data["id"] = self.image_id
            single_data["annotations"][0]["id"] = self.annotation_id
            single_data["annotations"][0]["import_id"] = self.import_id
            single_data["annotations"][0]["task"] = self.image_id
            single_data["data"]["img"] = "/data/local-files/?d=" + self.dataset_name + "/" + image["file_name"]
            for ann in self.imgToAnns[image["id"]]:
                single_result = {"type": "rectanglelabels",
                                "to_name": "img-1",
                                "from_name": "bbox",
                                "image_rotation": 0,
                                "original_width": image_width,
                                "original_height": image_height}
                value = {"rotation": 0, 
                        "x": ann["bbox"][0] / image_width * 100, 
                        "y": ann["bbox"][1] / image_height * 100,
                        "width": ann["bbox"][2] / image_width * 100, 
                        "height": ann["bbox"][3] / image_height * 100,
                        "rectanglelabels": [ann["category_name"]]}
                single_result["value"] = value
                single_data["annotations"][0]["result"].append(single_result)
            self.label_studio_dataset.append(single_data)
            self.image_id += 1
            self.annotation_id += 1
            self.import_id += 1
        save_json_file(self.label_studio_dataset, label_studio_annotation_file)


def add_images(images_folder, label_studio_annotation_file, source, dataset_name, new_label_studio_annotation_file):
    """
    增加未标注的图片到转好格式的json文件中
    images_folder:需要加入的图片
    label_studio_annotation_file: 已有的label_studio格式
    source:数据集来源
    dataset_name:文件夹名称
    new_label_studio_annotation_file: 加入图片后保存的label_studio格式的图片
    """
    label_studio_dataset = load_json_file(label_studio_annotation_file)
    image_id = label_studio_dataset[-1]["id"] + 1
    annotation_id = label_studio_dataset[-1]["annotations"][0]["id"] + 1
    import_id = label_studio_dataset[-1]["annotations"][0]["import_id"] + 1
    for file_name in os.listdir(images_folder):
        single_data = {"id": 1,
                        "data": {"img": "",
                                 "source": source},
                        "annotations": [
                        {
                            "id": 1,
                            "created_username": " bot@prmlk.com, 3",
                            "created_ago": "1 minutes",
                            "completed_by": {
                            "id": 3,
                            "first_name": "",
                            "last_name": "",
                            "avatar": None,
                            "email": "bot@prmlk.com",
                            "initials": "bo"
                            },
                            "result": [],
                            "was_cancelled": False,
                            "ground_truth": True,
                            "created_at": "2024-12-03T12:38:08.667557Z",
                            "updated_at": "2024-12-13T12:38:08.667577Z",
                            "draft_created_at": None,
                            "lead_time": None,
                            "import_id": 1,
                            "last_action": None,
                            "task": 1,
                            "project": 15,
                            "updated_by": None,
                            "parent_prediction": None,
                            "parent_annotation": None,
                            "last_created_by": None
                        }
                        ],
                        "predictions": []
                        }
        single_data["id"] = image_id
        single_data["annotations"][0]["id"] = annotation_id
        single_data["annotations"][0]["import_id"] = import_id
        single_data["annotations"][0]["task"] = image_id
        image = Image.open(os.path.join(images_folder, file_name)).convert('RGB')
        single_data["data"]["img"] = "/data/local-files/?d=" + dataset_name + "/" + file_name
        image_width = image.size[0]
        image_height = image.size[1]

        label_studio_dataset.append(single_data)
        image_id += 1
        annotation_id += 1
        import_id += 1
    save_json_file(label_studio_dataset, new_label_studio_annotation_file)
    print(image_id - 1)


if __name__ == "__main__":
    format_conver = COCO2LabelStudio("dataset/xray20240119/annotations/train_instance.json", "xray20241203")
    format_conver.run("dataset/xray20240119/xray20240119_label_studio.json")
    print(format_conver.image_id - 1)
    add_images(images_folder = "dataset/xray20241203/tuodao",
               label_studio_annotation_file = "dataset/xray20240119/xray20240119_label_studio.json",
               source = "tuodao",
               dataset_name = "xray20241203",
               new_label_studio_annotation_file = "dataset/xray20241203/xray20241203_label_studio.json")
    