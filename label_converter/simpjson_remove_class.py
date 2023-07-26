import os
import json

from pathlib import Path

if __name__=="__main__":
    infopath = "labels_combine"
    outfopath = "labels_new"
    cls_list_remove = ["tomtat"]
    
    infopath = Path(infopath)
    outfopath = Path(outfopath)    
    for fpath in infopath.iterdir():
        print(fpath)
        if fpath.suffix != ".json":
            continue
        
        with open(fpath) as f:
            c = json.load(f)
        
        simpjson = c
        # remove from box list
        bboxes = []
        for box in c["bboxes"]:
            if box["class_name"] not in cls_list_remove:
                bboxes.append(box)
        # remove from polygon list
        polygons = []
        for poly in c["polygon"]:
            if poly["class_name"] not in cls_list_remove:
                polygons.append(poly)
        # save new file
        simpjson["bboxes"] = bboxes
        simpjson["polygon"] = polygons
        with open((outfopath / fpath.name), "w") as f:
            json.dump(simpjson, f)

    # create new classes.txt
    clslist = []
    with open(infopath / "classes.txt") as f:
        c = f.readlines()
    for cls in c:
        if cls not in cls_list_remove:
            clslist.append(cls)
    with open((outfopath / "classes.txt"), "w") as f:
        for cls in clslist:
            f.write("%s\n" %cls.strip())
            
#END        







