import os
from pathlib import Path
import json
import re

import cv2
import magic
from shutil import copyfile

def get_img_shape(img_path):
    width = 0
    height = 0
    file_magic = magic.from_file(img_path)
    regex_result = re.findall("(\d+)x(\d+)", file_magic)
    if len(regex_result) > 1:
        width, height = regex_result[1]
    else:
        width, height = regex_result[0]

    return int(width), int(height)


def yolo2simplejson(img_path, cls_list, yolo_label_path, json_label_path):
    img_filename = img_path.split("/")[-1]
    width, height = get_img_shape(img_path)
    with open(yolo_label_path, "r") as yolo_file:
        yolo_label = yolo_file.readlines()

    json_file = open(json_label_path, "w")
    label_list = []
    for line in yolo_label:
        line = line.strip()
        param_list = [float(i) for i in line.split(" ")]
        cls_id = param_list[0]
        bbox_dict = {}
        bbox_dict["class_name"] = cls_list[int(cls_id)]
        bbox_dict["points"] = []
        bbox_dict["conf"] = 1.0
        for i in range(1, len(param_list)-1, 2):
            scale_x = param_list[i]
            scale_y = param_list[i+1]
            point_x = scale_x * width
            point_y = scale_y * height

            bbox_dict["points"].append({"x": point_x, "y": point_y})
        label_list.append(bbox_dict)
            
    file_size = os.path.getsize(img_path)

    label_dict = {"file_name": img_filename}
    label_dict["image_width"] = width
    label_dict["image_height"] = height
    label_dict["bboxes"] = []
    label_dict["polygon"] = label_list
    label_dict["file_size"] = file_size
    label_dict["manual_label"] = 0
    label_dict["set_type"] = ""

    json.dump(label_dict, json_file)

    json_file.close()


def yolo2simplejson_db(img_folder, yolo_folder, json_folder):
    yolo_folder = Path(yolo_folder)

    # load class list
    cls_list_path = os.path.join(yolo_folder, "classes.txt")
    copyfile(cls_list_path, Path(json_folder) / "classes.txt")
    with open(cls_list_path, "r") as cls_file:
        cls_list = cls_file.readlines()
    cls_list = [cls.strip() for cls in cls_list]
    print(cls_list)

    for fname in os.listdir(img_folder):
        print(fname)
        img_path = os.path.join(img_folder, fname)
        fname_woext = ".".join(fname.split(".")[:-1])
        yolo_label_path = list(yolo_folder.glob("%s.*" % fname_woext))
        if len(yolo_label_path) == 0:
            continue
        else:
            yolo_label_path = yolo_label_path[0]
            
        json_label_path = os.path.join(json_folder, "%s.json" % fname_woext)
        yolo2simplejson(img_path, cls_list, yolo_label_path, json_label_path)

    return cls_list


if __name__ == "__main__":
    img_folder = "images"
    yolo_folder = "yolo"
    json_folder = "simpjson"
    yolo2simplejson_db(img_folder, yolo_folder, json_folder)
    


