import os
import json
import magic
import re

def get_img_shape(img_path):
    width = 0
    height = 0
    file_magic = magic.from_file(img_path)
    pattern = ["(\d+) x (\d+)", "(\d+)x(\d+)"]
    regex_result = []
    for p in pattern:
        regex_result += re.findall(p, file_magic)
    
    if len(regex_result) > 1:
        width, height = regex_result[1]
    else:
        width, height = regex_result[0]

    return int(width), int(height)

inpath = "project-21-at-2024-06-24-13-08-35bb61e7.json"
outpath = "simpjson"
imgfolderpath = "hocba6_roi/roi/"

with open(inpath, "r") as f:
    c = json.load(f)

label_list = []
for i in c[:]:
    flabel = {"file_name": "", "class_list": ["text"], "bboxes": []}
    keys = i.keys()
    id = i["id"]
    annotations = i["annotations"]
    data = i["data"]
    ocr = data["ocr"]
    fname = ocr.split("/")[-1]
    flabel["file_name"] = fname

    fpath = os.path.join(imgfolderpath, fname)    
    imgw, imgh = get_img_shape(fpath)
    
    flabel["image_width"] = imgw
    flabel["image_height"] = imgh
#    print(fname)
    results = annotations[0]["result"]
#    print(keys)
#    print(results)

    for r in results:
        value = r["value"]
        if 'text' not in value.keys():
            continue
#        print(value)
        percent_x = int(value["x"])
        percent_y = int(value["y"])
        percent_w = value["width"]
        percent_h = value["height"]
        x1 = int(percent_x*imgw/100)
        y1 = int(percent_y*imgh/100)
        w = int(percent_w*imgw/100)
        h = int(percent_h*imgh/100)
        x2 = int(x1+w)
        y2 = int(y1+h)
        text = value["text"][0]
        box = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "metadata": text, "class_name": "text", "conf": 1.0}
        flabel["bboxes"].append(box)
    label_list.append(flabel)

print(label_list)


for flabel in label_list:
    fjson = {}
    fname = flabel["file_name"]
    fjson["file_name"] = fname
    fjson["image_width"] = flabel["image_width"]
    fjson["image_height"] = flabel["image_height"]
    class_list = flabel["class_list"]
    fjson["class_list"] = class_list
    bboxes = flabel["bboxes"]
    print(fname)
    print(class_list)
    fjson["bboxes"] = []
    for bbox in bboxes:
        print(bbox)
        fjson["bboxes"].append(bbox)
    
    print(fjson)
    fopath = os.path.join(outpath, "%s.json" %fname)
    with open(fopath, "w", encoding='utf8') as f:
        json.dump(fjson, f, ensure_ascii=False)
    






