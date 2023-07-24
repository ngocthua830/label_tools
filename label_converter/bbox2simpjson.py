#bbox format:
# x1 y1 x2 y2 classname
#
import os
import re
import json
import glob

import magic
from pathlib import Path

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

def bbox2simpjson(cls_list, imgpath, jsonpath, f):
    width, height = get_img_shape(imgpath)
    jsonfile = open(jsonpath, "w")
    
    bbox_list = []
    polygon_list = []
    for line in f[1]:
        line = line.strip()
        linesplit = line.split()
        cls = linesplit[4]
        bbox = [float(x) for x in linesplit[:4]]
        
        bbox_dict = {}
        bbox_dict["class_name"] = cls
        bbox_dict["conf"] = 1.0
        bbox_dict["x1"] = bbox[0]
        bbox_dict["y1"] = bbox[1]
        bbox_dict["x2"] = bbox[2]
        bbox_dict["y2"] = bbox[3]
        
        bbox_list.append(bbox_dict)
    
    file_size = os.path.getsize(imgpath)
    
    label_dict = {"file_name": imgpath.name}
    label_dict["image_width"] = width
    label_dict["image_height"] = height
    label_dict["class_list"] = cls_list
    label_dict["bboxes"] = bbox_list
    label_dict["polygon"] = polygon_list
    label_dict["file_size"] = file_size
    label_dict["manual_label"] = 0
    label_dict["set_type"] = ""
    
    json.dump(label_dict, jsonfile)
    jsonfile.close()

def convert_dataset(imgfopath, bboxfopath, jsonfopath):
    imgfopath = Path(imgfopath)
    bboxfopath = Path(bboxfopath)
    jsonfopath = Path(jsonfopath)
    
    cls_list = []
    filelist = []
    for fpath in bboxfopath.iterdir():
        with open(fpath) as f:
            c = f.readlines()
        filelist.append([fpath, c])
    
    # create cls_list
    for f in filelist:
        for line in f[1]:
            line = line.strip()
            linesplit = line.split()
            cls = linesplit[4]
            if cls not in cls_list:
                cls_list.append(cls)
    print("class list: ", cls_list)
    # save cls_list
    with open(jsonfopath / "classes.txt", "w") as clsf:
        for cls in cls_list:
            clsf.write("%s\n" %cls)
    
    # create dataset
    for f in filelist:
        imgpattern = "%s/%s*" %(imgfopath, f[0].stem)
        imgpath = Path(glob.glob(imgpattern)[0])
        print(imgpath)
        jsonpath = jsonfopath / str("%s.json" %(f[0].stem))
        bbox2simpjson(cls_list, imgpath, jsonpath, f)
            

if __name__=="__main__":
    imgfopath = "001"
    bboxfopath = "bbox"
    jsonfopath = "simpjson"
    
    convert_dataset(imgfopath, bboxfopath, jsonfopath)














