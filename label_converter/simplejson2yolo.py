import os
import json


def simplejson2yolo_str(cls_list, simplejson, mode = "detection"):
    yolostr = ""
    img_width = simplejson["image_width"]
    img_height = simplejson["image_height"]
    if mode == "detection":
        for obj in simplejson["bboxes"]:
            cls_name = obj["class_name"]
            if cls_name not in cls_list:
                cls_list.append(cls_name)

            x1 = obj["x1"]
            y1 = obj["y1"]
            x2 = obj["x2"]
            y2 = obj["y2"]
            width = x2 - x1
            height = y2 - y1
            cs_x = float(x1 + (width / 2)) / img_width
            cs_y = float(y1 + (height / 2)) / img_height
            s_width = float(width / img_width)
            s_height = float(height / img_height)

            yolostr += "%s %f %f %f %f\n" % (cls_list.index(cls_name), cs_x, cs_y, s_width, s_height)
    else:
        for seg in simplejson["segmentations"]:
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


def simplejson2yolo_db_str(simplejson_folder, mode = "detection"):
    db_yolo_list = []
    cls_list = []
    for fname in os.listdir(simplejson_folder):
        fname_woext = ".".join(fname.split(".")[:-1])
        fpath = os.path.join(simplejson_folder, fname)
        with open(fpath, "r") as simple_file:
            simplejson = json.load(simple_file)
        yolostr = simplejson2yolo_str(cls_list, simplejson, mode)

        db_yolo_list.append(("%s.txt" % fname_woext, yolostr))
    return cls_list, db_yolo_list


if __name__ == "__main__":
    #    cls_list = []
    #    fpath = "1-500x500_jpg.rf.3ad4b0d86a75b6d60207fd510cc06c81.json"
    #    with open(fpath, "r") as simple_file:
    #        simplejson = json.load(simple_file)
    #    yolostr = simplejson2yolo_str(cls_list, simplejson)
    #    print(yolostr)
    yolo_folder = "yolo"
    cls_list, db_yolo_list = simplejson2yolo_db_str(simplejson_folder = "simpjson", mode = "segmentation")
    for f in db_yolo_list:
        print(f[0])
        with open(os.path.join(yolo_folder, f[0]), "w") as outf:
            outf.write(f[1])









