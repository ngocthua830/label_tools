import os
import json

from pathlib import Path

def simplejson2yolo_str(cls_list, simplejson):
    yolostr = ""
    img_width = int(simplejson["image_width"])
    img_height = int(simplejson["image_height"])
    for seg in simplejson["polygon"]:
        cls_name = seg["class_name"]
        if cls_name not in cls_list:
            cls_list.append(cls_name)
        points_str = ""
        for point in seg["points"]:
            x = float(point["x"])/img_width
            y = float(point["y"])/img_height
            points_str += "%s %s " %(x, y)
        yolostr += "%s %s\n" % (cls_list.index(cls_name), points_str)
    return yolostr.strip()


def simplejson2yolo_db_str(simplejson_folder):
    db_yolo_list = []
    cls_list = []
    if os.path.exists(os.path.join(simplejson_folder, "classes.txt")):
        with open(os.path.join(simplejson_folder, "classes.txt")) as f:
            c = f.readlines()
        for cls in c:
            cls = cls.strip()
            cls_list.append(cls)
    print("cls_list", cls_list)
    for fname in os.listdir(simplejson_folder):
        print(fname)
        if Path(fname).suffix != ".json":
            continue
        fname_woext = ".".join(fname.split(".")[:-1])
        fpath = os.path.join(simplejson_folder, fname)
        with open(fpath, "r") as simple_file:
            simplejson = json.load(simple_file)
        yolostr = simplejson2yolo_str(cls_list, simplejson)

        db_yolo_list.append(("%s.txt" % fname_woext, yolostr))
    return cls_list, db_yolo_list


if __name__ == "__main__":
    simplejson_folder = "simpjson"
    yolo_folder = "yolo"
    cls_list, db_yolo_list = simplejson2yolo_db_str(simplejson_folder)
    for f in db_yolo_list:
        print(f[0])
        with open(os.path.join(yolo_folder, f[0]), "w") as outf:
            outf.write(f[1])
            
    # save classes.txt
    with open(os.path.join(yolo_folder, "classes.txt"), "w") as outf:
        for cls in cls_list:
            outf.write("%s\n" %cls)








