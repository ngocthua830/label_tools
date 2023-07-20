import os
import json
from pathlib import Path

coco_file = "instances_default.json"
simpjson_folder = Path("simpjson")
with open(coco_file, "r") as f:
    coco_json = json.load(f)

print(coco_json.keys())
print(coco_json["licenses"])
print(coco_json["info"])
print(coco_json["categories"])
label_list = [0] * len(coco_json["categories"])
for label in coco_json["categories"]:
    print(label)
    label_list[label["id"]-1] = label["name"]
print(label_list)
#print(coco_json["images"])
print(coco_json["annotations"])
for image, anno in zip(coco_json["images"], coco_json["annotations"]):
    print(image)
    print(anno)
    file_name = Path(image["file_name"])
    label_fname = "%s.txt" %file_name.stem
    fid = image["id"]
    image_width = image["width"]
    image_height = image["height"]
    file_size = 0
    manual_label = 0
    set_type = ""
    bboxes = []
    bb_x1 = anno["bbox"][0]
    bb_x2 = anno["bbox"][0]+anno["bbox"][2]
    bb_y1 = anno["bbox"][1]
    bb_y2 = anno["bbox"][1]+anno["bbox"][3]
    box = {"class_name": label_list[int(anno["category_id"])-1], "conf": 1.0, "x1": bb_x1, "y1": bb_y1, "x2": bb_x2, "y2": bb_y2}
    bboxes.append(box)
    segmentations = []
    for seg in anno["segmentation"]:
        segmentation = {"class_name": label_list[int(anno["category_id"])-1], "conf": 1.0, "points": []}
        for i in range(0, len(seg), 2):
            x = seg[i]
            y = seg[i+1]
            segmentation["points"].append({"x": x, "y": y})
        segmentations.append(segmentation)
    label = {"file_name": str(file_name), "label_fname": label_fname, "file_id": fid, "image_width": image_width, "image_height": image_height, "file_size": file_size, "manual_label": manual_label, "set_type": set_type, "bboxes": bboxes, "segmentations": segmentations}
    print(label)
    
    with open(simpjson_folder/label_fname, "w") as f:
        json.dump(label, f)
    
