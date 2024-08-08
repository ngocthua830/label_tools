import os
import json
from shutil import copyfile

def simplejson2yolo_str(cls_list, simplejson):
    yolostr = ""
    img_width = int(simplejson["image_width"])
    img_height = int(simplejson["image_height"])
    for obj in simplejson["bboxes"]:
        cls_name = obj["class_name"]
        if cls_name not in cls_list:
            cls_list.append(cls_name)

        x1 = float(obj["x1"])
        y1 = float(obj["y1"])
        x2 = float(obj["x2"])
        y2 = float(obj["y2"])
        width = x2 - x1
        height = y2 - y1
        cs_x = float(x1 + (width / 2)) / img_width
        cs_y = float(y1 + (height / 2)) / img_height
        s_width = float(width / img_width)
        s_height = float(height / img_height)

        yolostr += "%s %f %f %f %f\n" % (cls_list.index(cls_name), cs_x, cs_y, s_width, s_height)
    return yolostr.strip()


def simplejson2yolo_db_str(simplejson_folder):
    db_yolo_list = []
    cls_list = []
    
    if os.path.exists(os.path.join(simplejson_folder, "classes.txt")):
        with open(os.path.join(simplejson_folder, "classes.txt"), "r") as outf:
            for cls in outf.readlines():
                cls_list.append(cls.strip())
    
    print("cls_list", cls_list)
    
    for fname in os.listdir(simplejson_folder):
        if fname.split(".")[-1] != "json":
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
            
#    # save classes.txt
    if not os.path.exists(os.path.join(simplejson_folder, "classes.txt")):
        with open(os.path.join(yolo_folder, "classes.txt"), "w") as outf:
            for cls in cls_list:
                outf.write("%s\n" %cls)
    else:
        copyfile(os.path.join(simplejson_folder, "classes.txt"), os.path.join(yolo_folder, "classes.txt"))







