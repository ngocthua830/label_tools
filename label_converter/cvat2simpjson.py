import os
import json
from pathlib import Path

import xml.etree.ElementTree as ET

def get_image_info(image):
    file_name = image.attrib["name"]
    image_width = image.attrib["width"]
    image_height = image.attrib["height"]
    bboxes = []
    polygon = []
    
    # export bboxes
    for bbox in image.findall("box"):
        label = bbox.attrib["label"]
        x1 = bbox.attrib["xtl"]
        y1 = bbox.attrib["ytl"]
        x2 = bbox.attrib["xbr"]
        y2 = bbox.attrib["ybr"]
        bboxes.append({"class_name": label, "conf": 1.0, "x1": x1, "y1": y1, "x2": x2, "y2": y2})
    
    # export polygon
    for poly in image.findall("polygon"):
        points = []
        label = poly.attrib["label"]
        pos = poly.attrib["points"].split(";")
        for i in range(len(pos)):
            x, y = pos[i].split(",")
            points.append({"x": x, "y": y})
        polygon.append({"class_name": label, "points": points, "conf": 1.0})    
    
    simpjson = {"file_name": file_name, "image_width": image_width, "image_height": image_height, "filesize": 0, "manual_label": 1, "set_type": "", "bboxes": bboxes, "polygon": polygon}
    return simpjson

def get_info(cvat_fpath, simp_folder):
    ann_tree = ET.parse(cvat_fpath)
    ann_root = ann_tree.getroot()
    
    clslist = []
    labels = ann_root.find("meta").find("job")
    if labels is None:
        labels = ann_root.find("meta").find("task").find("labels") 
    else:
        labels = ann_root.find("meta").find("job").find("labels") 
    print("labels", labels)
    for label in labels:
        clslist.append(label.findtext("name"))
    
    # save classes.txt
    with open((Path(simp_folder) / "classes.txt"), "w") as f:
        for cls in clslist:
            f.write("%s\n" %cls)
    
    for image in ann_root.findall("image"):
        simpjson = get_image_info(image)
        
        fname = image.attrib["name"]
        fname_woext = ".".join(fname.split(".")[:-1])
        ofpath = os.path.join(simp_folder, "%s.json" %fname_woext)
        
        with open(ofpath, "w") as ofile:
            json.dump(simpjson, ofile)
        
    
if __name__=="__main__":
    cvat_fpath = "annotations.xml"
    simp_folder = "simpjson"
    get_info(cvat_fpath, simp_folder)
