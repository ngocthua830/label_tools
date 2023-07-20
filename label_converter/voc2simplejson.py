import os
import json
import re
import xml.etree.ElementTree as ET
import magic

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

def get_image_info(annotation_root, extract_num_from_imgid=True):
    path = annotation_root.findtext("path")
    if path is None:
        filename = annotation_root.findtext("filename")
    else:
        filename = os.path.basename(path)
    img_name = os.path.basename(filename)
    img_id = os.path.splitext(img_name)[0]
    if extract_num_from_imgid and isinstance(img_id, str):
        img_id_list = re.findall(r"\d+", img_id)
        if len(img_id_list) > 0:
            img_id = int(img_id_list[0])
        else:
            img_id = -1

    size = annotation_root.find("size")
    width = int(size.findtext("width"))
    height = int(size.findtext("height"))

    image_info = {"file_name": filename, "height": height, "width": width, "id": img_id}
    return image_info

def get_obj(obj):
    label = obj.findtext("name")
    bndbox = obj.find("bndbox")
    xmin = int(bndbox.findtext("xmin")) - 1
    ymin = int(bndbox.findtext("ymin")) - 1
    xmax = int(bndbox.findtext("xmax"))
    ymax = int(bndbox.findtext("ymax"))

    if xmax <= xmin or ymax <= ymin:
        raise Exception(
            f"Error: Box size error !: (xmin, ymin, xmax, ymax): {xmin, ymin, xmax, ymax}"
        )

    o_width = xmax - xmin
    o_height = ymax - ymin
    
    box = {}
    box["class_name"] = label
    box["x1"] = xmin
    box["y1"] = ymin
    box["x2"] = xmax
    box["y2"] = ymax
    box["width"] = o_width
    box["height"] = o_height
#    print(label, xmin, ymin, xmax, ymax, o_width, o_height)
    
    return box

def convert_file(fpath):
    ann_tree = ET.parse(fpath)
    ann_root = ann_tree.getroot()
    img_info = get_image_info(ann_root)
#    print(img_info)
    
    bboxes = []
    for obj in ann_root.findall("object"):
        box = get_obj(obj=obj)
        bboxes.append(box)
    simplejson = {"file_name": img_info["file_name"], "image_width": img_info["width"], "image_height": img_info["height"], "filesize": 0, "manual_label": 1, "set_type": "", "bboxes": bboxes}
    return simplejson

def convert_folder(voc_folder, simple_folder):
    for fname in os.listdir(voc_folder)[0:]:
        print(fname)
        fpath = os.path.join(voc_folder, fname)
        fname_woext = ".".join(fname.split(".")[:-1])
        ofpath = os.path.join(simple_folder, "%s.json" %fname_woext)
        simplejson = convert_file(fpath)
#        print(simplejson)
        with open(ofpath, "w") as ofile:
            json.dump(simplejson, ofile)

def main():
    convert_folder("xml", "json")

if __name__ == "__main__":
    main()

