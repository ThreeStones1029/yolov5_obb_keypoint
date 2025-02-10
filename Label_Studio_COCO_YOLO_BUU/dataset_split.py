import shutil
import os
from json_process import load_json_file, save_json_file
import numpy as np
from common import join, create_folder


def random_split_coco_dataset(images_folder_path, annotation_file, output_folder_path, split_info_dict):
    """
    随机划分json文件,并划分好相应的数据集
    """
    os.makedirs(output_folder_path, exist_ok=True)
    # 读取annotations.json文件
    dataset = load_json_file(annotation_file)
    # 提取images, annotations, categories
    # 随机打乱数据
    np.random.shuffle(dataset["images"])
    start_index = 0
    end_index = 0
    def filter_annotations(annotations, image_ids):
        return [ann for ann in annotations if ann["image_id"] in image_ids]
    for split_part_name, ratio in split_info_dict.items():
        end_index += int(ratio * len(dataset["images"]))
        split_part_images = dataset["images"][start_index:end_index]
        start_index += int(ratio * len(dataset["images"]))
        split_part_folder = os.path.join(output_folder_path, split_part_name)
        os.makedirs(split_part_folder, exist_ok=True)
        for img in split_part_images:
            shutil.copy(os.path.join(images_folder_path, img["file_name"]), os.path.join(split_part_folder, img["file_name"]))
        split_part_annotations = filter_annotations(dataset["annotations"], [img["id"] for img in split_part_images])
        split_part_data = {"info": dataset["info"], "images": split_part_images, "annotations": split_part_annotations, "categories": dataset["categories"]}
        save_json_file(split_part_data, os.path.join(output_folder_path,"bbox_" + split_part_name + ".json"))
    print("数据集划分完成！")


def assign_images_split(input_root, annotations_path, output_root):
    """
    手动划分数据集后,根据图片名称划分json文件
    """
    # 输出路径
    create_folder(output_root)
    # 读取annotations.json文件
    annotations_data = load_json_file(annotations_path)

    # 提取images, annotations, categories
    images = annotations_data["images"]
    annotations = annotations_data["annotations"]
    categories = annotations_data["categories"]
    # 选定图片作为训练集、验证集（从指定json文件里面选）
    assign_train_images_path = join(input_root, "train", "images")
    assign_val_images_path = join(input_root, "val", "images")
    
    def get_images(assign_images_path, images):
        assign_images = []
        for root, dirs, files in os.walk(assign_images_path):
            for img in images:
                if img["file_name"] in files:
                    assign_images.append(img)
        return assign_images
    train_images = get_images(assign_train_images_path, images)
    val_images = get_images(assign_val_images_path, images)

    # 根据图片id分配annotations
    def filter_annotations(annotations, image_ids):
        return [ann for ann in annotations if ann["image_id"] in image_ids]
    train_ann = filter_annotations(annotations, [img["id"] for img in train_images])
    val_ann = filter_annotations(annotations, [img["id"] for img in val_images])

    # 生成train.json, val.json, test.json
    train_json = {"info": annotations_data["info"], "images": train_images, "annotations": train_ann, "categories": categories}
    val_json = {"info": annotations_data["info"], "images": val_images, "annotations": val_ann, "categories": categories}

    save_json_file(train_json, join(output_root, "train", "rotate_bbox_keypoints_train_all2.json"))
    save_json_file(val_json,join(output_root, "val", "rotate_bbox_keypoints_val_all2.json"))

    if os.path.exists(join(input_root, "test")):
        assign_test_images_path = join(input_root, "test", "images")
        test_images = get_images(assign_test_images_path, images)
        test_ann = filter_annotations(annotations, [img["id"] for img in test_images])
        test_json = {"info": annotations_data["info"], "images": test_images, "annotations": test_ann, "categories": categories}
        save_json_file(test_json, join(output_root,"test", "rotate_bbox_keypoints_test_all2.json"))

    print("数据集划分完成！")


if __name__ == "__main__":
    # random_split_coco_dataset("dataset/xray20241203/images",
    #                           "dataset/xray20241203/xray20241203_rotate_keypoints_all.json",
    #                           "dataset/xray20241203/split_dataset",
    #                           {"train": 0.6, "val": 0.2, "test": 0.2})

    assign_images_split("dataset/xray20241203", "dataset/xray20241203/xray20241203_rotate_keypoints_all2.json","dataset/xray20241203")

    # assign_images_split("dataset/BUU", "dataset/BUU/buu_roate_keypoints2.json","dataset/BUU")
