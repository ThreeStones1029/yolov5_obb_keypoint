from json_process import load_json_file, save_json_file


def get_instance_categories():
    """
    """
    categories = []
    for i in range(1, 6):
        categories.append({"id": i,
                            "name": "L" + str(6-i),
                            "supercategory": "vertebrae"}) 
    for i in range(6, 18):
        categories.append({"id": i,
                            "name": "T" + str(18-i),
                            "supercategory": "vertebrae"}) 
    for i in range(18, 25):
        categories.append({"id": i,
                            "name": "C" + str(25-i),
                            "supercategory": "vertebrae"})  
    return categories


def get_semantic_categories():
    """
    """
    categories = []
    categories.append({"id": 0,
                       "name": "vertebrae", 
                       "supercategory": "bone"}) 
    categories.append({"id": 1,
                        "name": "pelvis", 
                        "supercategory": "bone"})
    categories.append({"id": 2,
                        "name": "rib", 
                        "supercategory": "bone"})
    return categories


def get_instance_coco_file(all_json_file_path, instance_json_file_path):
    """
    """
    dataset = load_json_file(all_json_file_path)
    instance_categories = get_instance_categories()
    instance_categories_list = [category["name"] for category in instance_categories]
    instance_categories_dict = {category["name"]: category["id"] for category in instance_categories}
    instance_dataset = {"info": dataset["info"],
                        "categories": instance_categories,
                        "images":dataset["images"]}

    instance_annotations = []
    for ann in dataset["annotations"]:
        ann = ann
        if ann["category_name"] in instance_categories_list:
            ann["category_id"] = instance_categories_dict[ann["category_name"]]
            instance_annotations.append(ann)
    instance_dataset["annotations"] = instance_annotations
    save_json_file(instance_dataset, instance_json_file_path)


def get_semantic_coco_file(all_json_file_path, semantic_json_file_path):
    """
    """
    instance_categories = get_instance_categories()
    instance_categories_list = [category["name"] for category in instance_categories]
    dataset = load_json_file(all_json_file_path)
    semantic_categories = get_semantic_categories()
    semantic_categories_dict = {category["name"]: category["id"] for category in semantic_categories}
    semantic_dataset = {"info": dataset["info"],
                        "categories": semantic_categories,
                        "images":dataset["images"]}
    semantic_annotations = []

    for ann in dataset["annotations"]:
        if ann["category_name"] in instance_categories_list:
            ann["category_name"] = "vertebrae"
            ann["category_id"] = semantic_categories_dict["vertebrae"]
        if ann["category_name"] == "rib":
            ann["category_name"] = "rib"
            ann["category_id"] = semantic_categories_dict["rib"]
        if ann["category_name"] == "Pelvis" or ann["category_name"] == "pelvis":
            ann["category_name"] = "pelvis"
            ann["category_id"] = semantic_categories_dict["pelvis"]
        semantic_annotations.append(ann)
    semantic_dataset["annotations"] = semantic_annotations
    save_json_file(semantic_dataset, semantic_json_file_path)


def get_instance_and_semantic_coco_file(all_json_file_path, instance_json_file_path, semantic_json_file_path):
    get_instance_coco_file(all_json_file_path, instance_json_file_path)
    get_semantic_coco_file(all_json_file_path, semantic_json_file_path)
    

if __name__ == "__main__":
    get_instance_and_semantic_coco_file("dataset/xray20241203/train/rotate_bbox_keypoints_train_all2.json",
                                        "dataset/xray20241203/train/rotate_bbox_keypoints_train_instance2.json",
                                        "dataset/xray20241203/train/rotate_bbox_keypoints_train_semantic2.json")
    get_instance_and_semantic_coco_file("dataset/xray20241203/val/rotate_bbox_keypoints_val_all2.json",
                                        "dataset/xray20241203/val/rotate_bbox_keypoints_val_instance2.json",
                                        "dataset/xray20241203/val/rotate_bbox_keypoints_val_semantic2.json")
    get_instance_and_semantic_coco_file("dataset/xray20241203/test/rotate_bbox_keypoints_test_all2.json",
                                        "dataset/xray20241203/test/rotate_bbox_keypoints_test_instance2.json",
                                        "dataset/xray20241203/test/rotate_bbox_keypoints_test_semantic2.json")
    
    # get_instance_and_semantic_coco_file("dataset/xray20241203/train/bbox_train_all.json",
    #                                     "dataset/xray20241203/train/bbox_train_instance.json",
    #                                     "dataset/xray20241203/train/bbox_train_semantic.json")
    # get_instance_and_semantic_coco_file("dataset/xray20241203/val/bbox_val_all.json",
    #                                     "dataset/xray20241203/val/bbox_val_instance.json",
    #                                     "dataset/xray20241203/val/bbox_val_semantic.json")
    # get_instance_and_semantic_coco_file("dataset/xray20241203/test/bbox_test_all.json",
    #                                     "dataset/xray20241203/test/bbox_test_instance.json",
    #                                     "dataset/xray20241203/test/bbox_test_semantic.json")